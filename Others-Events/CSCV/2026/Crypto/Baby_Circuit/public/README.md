# Offline service

A local build of the same service the hosted instance runs, so you can develop and test your
solver offline. It carries a TEST flag; the hosted instance has the real one.

## Run

Needs Python 3.11 (x86_64 Linux) and `pycryptodome`:

```
pip install pycryptodome
python hsm_main.py
```

Connect to `127.0.0.1:1337`, raw TCP, one JSON object per line.

On another platform, or to avoid installing anything, use the Dockerfile:

```
docker build -t baby-circuit . && docker run --rm -p 1337:1337 baby-circuit
```

On an ARM host add `--platform linux/amd64` (the module is compiled for x86_64 Linux).

## Protocol

Each TCP connection is one session with its own master registers, its own linear layer and
its own round constants. Two actions:

* `{"action": "get_hardware_specs"}` — device sheet, circuit layout, linear layer, round
  constants, session parameters, and the encrypted flag with its IV.
* `{"action": "prove", "public_nonce": "0x...", "public_nonce2": "0x...",
   "core_voltage_mv": 1200, "clock_freq_mhz": 80}` — one proof.

The query budget applies per session; reconnect for a fresh one.

## What is inside

* `plonk_engine.py` — verifier-side algebra, the sponge specification, the selector table,
  the proof builder and the published timing model. Read it: this is the service's own source.
* `hsm_main.py` — the network launcher: session setup and the two actions.
* `hw_model.cpython-311-x86_64-linux-gnu.so` — the die's witness builder, compiled. It hands
  out an opaque session handle; the master registers never leave it. The register layout, the
  stage-to-register mapping and the manufacturing trim live in here.
