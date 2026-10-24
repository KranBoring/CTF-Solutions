"""HTTP upload interface for the one-shot WebAssembly collision judge."""

from __future__ import annotations

import json
import os
import secrets
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge


APP_DIR = Path(__file__).resolve().parent
MAX_WASM_SIZE = 1024 * 1024
MAX_BODY_SIZE = 2 * 1024 * 1024
WALL_SECONDS = max(60, int(os.environ.get("FASTCOLL_WALL_SECONDS", "900")))
WORKERS = max(1, min(4, int(os.environ.get("FASTCOLL_WORKERS", "2"))))
MAX_ACTIVE_JOBS = WORKERS * 2
RESULT_TTL_SECONDS = 3600
MAX_COMPLETED_JOBS = 2048

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_BODY_SIZE
executor = ThreadPoolExecutor(max_workers=WORKERS, thread_name_prefix="wasm-judge")
jobs_lock = threading.Lock()


@dataclass
class Job:
    status: str
    created: float
    result: dict[str, object] | None = None


jobs: dict[str, Job] = {}


def _prune_jobs(now: float) -> None:
    for job_id, job in list(jobs.items()):
        if job.result is not None and now - job.created > RESULT_TTL_SECONDS:
            del jobs[job_id]
    completed = sorted(
        ((job.created, job_id) for job_id, job in jobs.items() if job.result is not None)
    )
    for _created, job_id in completed[:-MAX_COMPLETED_JOBS]:
        del jobs[job_id]


def _flag() -> str:
    path = Path(os.environ.get("FASTCOLL_FLAG_FILE", str(APP_DIR / "flag.txt")))
    return path.read_text(encoding="utf-8").strip()


def _judge(job_id: str, wasm_bytes: bytes) -> None:
    with jobs_lock:
        jobs[job_id].status = "running"
    try:
        completed = subprocess.run(
            [sys.executable, "-I", str(APP_DIR / "runner.py")],
            input=wasm_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=APP_DIR,
            env={
                "PATH": "/usr/local/bin:/usr/bin:/bin",
                "PYTHONDONTWRITEBYTECODE": "1",
                "FASTCOLL_FUEL": os.environ.get("FASTCOLL_FUEL", "100000000000000"),
            },
            timeout=WALL_SECONDS,
            start_new_session=True,
            check=False,
        )
        if completed.returncode != 0:
            result: dict[str, object] = {
                "status": "runtime_error",
                "calls": 0,
                "message": "Judge process exited unexpectedly",
            }
        else:
            result = json.loads(completed.stdout.decode("utf-8"))
            if result.get("status") not in {"won", "no_collision", "invalid", "limit", "runtime_error"}:
                raise ValueError("Invalid judge result")
            if result["status"] == "won":
                result["flag"] = _flag()
    except subprocess.TimeoutExpired:
        result = {"status": "timeout", "calls": None, "message": "Execution time limit exceeded"}
    except Exception:
        result = {"status": "runtime_error", "calls": None, "message": "Judge failed"}

    with jobs_lock:
        jobs[job_id].result = result
        jobs[job_id].status = str(result["status"])


@app.after_request
def security_headers(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "img-src 'self' data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
    )
    return response


@app.errorhandler(RequestEntityTooLarge)
def too_large(_error):
    return jsonify(error="Upload exceeds 2 MiB"), 413


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/healthz")
def healthz():
    return jsonify(status="ok")


@app.post("/api/jobs")
def create_job():
    upload = request.files.get("file")
    if upload is None:
        return jsonify(error="Choose a .wasm file"), 400
    wasm_bytes = upload.stream.read(MAX_WASM_SIZE + 1)
    if len(wasm_bytes) > MAX_WASM_SIZE:
        return jsonify(error="WASM file exceeds 1 MiB"), 413
    if len(wasm_bytes) < 8 or wasm_bytes[:8] != b"\x00asm\x01\x00\x00\x00":
        return jsonify(error="Invalid WebAssembly module"), 400

    now = time.monotonic()
    with jobs_lock:
        _prune_jobs(now)
        active = sum(job.result is None for job in jobs.values())
        if active >= MAX_ACTIVE_JOBS:
            return jsonify(error="Judge is busy; retry shortly"), 429
        job_id = secrets.token_urlsafe(18)
        jobs[job_id] = Job(status="queued", created=now)
        executor.submit(_judge, job_id, wasm_bytes)
    return jsonify(id=job_id, status="queued"), 202


@app.get("/api/jobs/<job_id>")
def get_job(job_id: str):
    with jobs_lock:
        _prune_jobs(time.monotonic())
        job = jobs.get(job_id)
        if job is None:
            return jsonify(error="Unknown or expired job"), 404
        if job.result is None:
            return jsonify(status=job.status)
        return jsonify(job.result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True)
