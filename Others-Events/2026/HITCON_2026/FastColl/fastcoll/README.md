# fastcoll challenge service

From this directory, run `sudo docker compose up --build`. Open <http://localhost:8080>. Set `PORT` to choose another host port. The container reads the flag from a Compose secret; the uploaded module has no filesystem access.

## Guest ABI

- Export `memory` and `xx_hash() -> ()`. The judge invokes `xx_hash` once per uploaded module.
- Import only `env.xx_hash(ptr: i32, len: i32, out_ptr: i32) -> i32`.
- The import reads `len` bytes at `ptr`, writes the canonical 16-byte XXH3-128 digest at `out_ptr`, and returns `0`. The byte order is identical to Python `xxhash.xxh3_128_digest`.
- Messages must be 256–1024 bytes, inclusive. Invalid pointers or lengths return `-1` and still consume a seed and one call. Calling beyond the 1,000,000-call budget returns `-2` and terminates execution.
- On an accepted collision, the import returns `1` and execution ends immediately. The flag appears only in the HTTP result, never in guest memory.

Every upload receives a fresh secret 64-bit `C`. The first host hash uses seed `C`, the next uses `C+1 mod 2^64`, and so on. The judge accepts if two **different** submitted byte strings, on two distinct valid calls, produce the same complete 128-bit digest. Repeating the same message does not count. The seed is not returned.

## Limits and endpoints

The upload limit is 1 MiB. A module has 64 MiB linear memory, a 1,000,000-call host budget, a fuel limit, and a 900-second wall limit. No WASI imports are provided. The service accepts up to four queued or running jobs (two concurrent runners by default); further submissions receive HTTP 429.

The page uses `POST /api/jobs` with multipart field `file`, then polls `GET /api/jobs/<id>` until the result is ready. Completed results expire after one hour. The service runs a single Gunicorn web worker so job IDs remain available across polling requests.
