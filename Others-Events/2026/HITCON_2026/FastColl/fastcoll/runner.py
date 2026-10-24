"""Isolated, single-submission XXH3-128 WebAssembly judge.

The guest exports ``xx_hash()`` as its entry point and linear ``memory``.
Its only allowed import is ``env.xx_hash(i32 ptr, i32 len, i32 out_ptr) -> i32``.
Each import invocation consumes one seed, including invalid requests.
"""

from __future__ import annotations

import hashlib
import json
import os
import resource
import sys
from dataclasses import dataclass, field
from typing import Callable

import wasmtime
import xxhash


MASK64 = (1 << 64) - 1
MIN_MESSAGE_SIZE = 256
MAX_MESSAGE_SIZE = 1024
MAX_WASM_SIZE = 1024 * 1024
MAX_CALLS = 1_000_000
MEMORY_LIMIT = 64 * 1024 * 1024
DEFAULT_FUEL = 100_000_000_000_000

DigestFn = Callable[[bytes, int], bytes]


def _xxh3_digest(message: bytes, seed: int) -> bytes:
    return xxhash.xxh3_128_digest(message, seed)


@dataclass
class JudgeState:
    base_seed: int
    max_calls: int
    digest_fn: DigestFn
    calls: int = 0
    invalid_calls: int = 0
    over_budget: bool = False
    won: bool = False
    # A differing SHA-256 proves differing payload bytes. Equal fingerprints
    # are conservatively treated as duplicates; this never awards a false win.
    seen: dict[bytes, bytes] = field(default_factory=dict)


def _signature_is(ty: wasmtime.FuncType, params: list[wasmtime.ValType], results: list[wasmtime.ValType]) -> bool:
    return list(ty.params) == params and list(ty.results) == results


def _validate_module(module: wasmtime.Module) -> None:
    imports = module.imports
    i32 = wasmtime.ValType.i32()
    for item in imports:
        if item.module != "env" or item.name != "xx_hash" or not isinstance(item.type, wasmtime.FuncType):
            raise ValueError("Only the env.xx_hash function may be imported")
        if not _signature_is(item.type, [i32, i32, i32], [i32]):
            raise ValueError("env.xx_hash must have type (i32, i32, i32) -> i32")

    exports = {item.name: item.type for item in module.exports}
    if not isinstance(exports.get("memory"), wasmtime.MemoryType):
        raise ValueError("The module must export its linear memory as memory")
    entry = exports.get("xx_hash")
    if not isinstance(entry, wasmtime.FuncType) or not _signature_is(entry, [], []):
        raise ValueError("The module must export xx_hash() -> ()")


def run_wasm(
    wasm_bytes: bytes,
    *,
    seed: int | None = None,
    digest_fn: DigestFn = _xxh3_digest,
    max_calls: int = MAX_CALLS,
    fuel: int = DEFAULT_FUEL,
) -> dict[str, object]:
    """Run one module with fresh state; parameters beyond wasm_bytes are for tests.

    No seed or per-call digest is returned by this Python function. The digest
    is written only to guest memory by the host import.
    """
    if len(wasm_bytes) > MAX_WASM_SIZE:
        return {"status": "invalid", "calls": 0, "message": "WASM file exceeds 1 MiB"}
    if len(wasm_bytes) < 8 or wasm_bytes[:8] != b"\x00asm\x01\x00\x00\x00":
        return {"status": "invalid", "calls": 0, "message": "Invalid WebAssembly module"}
    if not 0 <= max_calls <= MAX_CALLS:
        raise ValueError("Invalid call limit")
    if seed is None:
        seed = int.from_bytes(os.urandom(8), "little")
    state = JudgeState(seed & MASK64, max_calls, digest_fn)

    config = wasmtime.Config()
    config.consume_fuel = True
    # Wasmtime requires this to stay below its async stack reservation.
    config.max_wasm_stack = 1024 * 1024
    config.wasm_threads = False
    config.wasm_memory64 = False
    config.wasm_multi_memory = False
    engine = wasmtime.Engine(config)
    try:
        module = wasmtime.Module(engine, wasm_bytes)
        _validate_module(module)
    except (ValueError, wasmtime.WasmtimeError) as exc:
        return {"status": "invalid", "calls": 0, "message": str(exc)[:300]}

    store = wasmtime.Store(engine)
    store.set_limits(memory_size=MEMORY_LIMIT, table_elements=100_000, instances=1, tables=1, memories=1)
    store.set_fuel(fuel)
    linker = wasmtime.Linker(engine)

    def imported_hash(caller: wasmtime.Caller, ptr: int, length: int, out_ptr: int) -> int:
        if state.calls >= state.max_calls:
            state.over_budget = True
            store.set_fuel(0)
            return -2

        # Consume the seed before *any* validation, including bad pointers.
        call_seed = (state.base_seed + state.calls) & MASK64
        state.calls += 1

        memory = caller.get("memory")
        if not isinstance(memory, wasmtime.Memory):
            state.invalid_calls += 1
            return -1
        size = memory.data_len(caller)
        if (
            length < MIN_MESSAGE_SIZE
            or length > MAX_MESSAGE_SIZE
            or ptr < 0
            or out_ptr < 0
            or ptr > size - length
            or out_ptr > size - 16
        ):
            state.invalid_calls += 1
            return -1

        # Snapshot the message before writing the digest: the buffers may overlap.
        message = bytes(memory.read(caller, ptr, ptr + length))
        digest = state.digest_fn(message, call_seed)
        if len(digest) != 16:
            raise RuntimeError("Host digest function produced an invalid digest")
        memory.write(caller, digest, out_ptr)

        fingerprint = hashlib.sha256(message).digest()
        previous = state.seen.get(digest)
        if previous is None:
            state.seen[digest] = fingerprint
        elif previous != fingerprint:
            state.won = True
            # The import returns 1, then the next guest instruction traps. This
            # prevents a malicious guest from hiding a collision by looping.
            store.set_fuel(0)
            return 1
        return 0

    linker.define_func(
        "env",
        "xx_hash",
        wasmtime.FuncType(
            [wasmtime.ValType.i32(), wasmtime.ValType.i32(), wasmtime.ValType.i32()],
            [wasmtime.ValType.i32()],
        ),
        imported_hash,
        access_caller=True,
    )

    try:
        instance = linker.instantiate(store, module)
        entry = instance.exports(store)["xx_hash"]
        entry(store)
    except (wasmtime.Trap, wasmtime.WasmtimeError) as exc:
        if state.won:
            return {"status": "won", "calls": state.calls, "message": "Collision found"}
        if state.over_budget:
            return {"status": "limit", "calls": state.calls, "message": "Call limit exceeded"}
        if "fuel" in str(exc).lower():
            return {"status": "limit", "calls": state.calls, "message": "Computation fuel exhausted"}
        return {"status": "runtime_error", "calls": state.calls, "message": "WebAssembly trapped"}
    except Exception:
        if state.won:
            return {"status": "won", "calls": state.calls, "message": "Collision found"}
        # Never disclose host internals or the hidden seed to a guest.
        return {"status": "runtime_error", "calls": state.calls, "message": "WebAssembly execution failed"}

    if state.won:
        return {"status": "won", "calls": state.calls, "message": "Collision found"}
    if state.over_budget:
        return {"status": "limit", "calls": state.calls, "message": "Call limit exceeded"}
    return {"status": "no_collision", "calls": state.calls, "message": "No collision found"}


def main() -> None:
    # The outer web process also imposes a wall-time timeout and Docker limits.
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
    wasm_bytes = sys.stdin.buffer.read(MAX_WASM_SIZE + 1)
    fuel = int(os.environ.get("FASTCOLL_FUEL", str(DEFAULT_FUEL)))
    result = run_wasm(wasm_bytes, fuel=fuel)
    sys.stdout.write(json.dumps(result, separators=(",", ":")) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
