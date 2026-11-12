from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from typing import List
import contextlib
import asyncio
import os
import humanize
from datetime import datetime
from watchfiles import awatch

from .canhelper import CANHelper
from .settings import settings

class FileRequest(BaseModel):
    filenames: List[str]

DBC_DIR = settings.dbc_dir
can_helper = CANHelper()
staged_files = set()

os.makedirs(settings.can_intake_path, exist_ok=True)
os.makedirs(settings.can_staging_path, exist_ok=True)
os.makedirs(settings.can_raw_path, exist_ok=True)
os.makedirs(settings.can_processed_path, exist_ok=True)
os.makedirs(settings.can_reports_path, exist_ok=True)
os.makedirs(DBC_DIR, exist_ok=True)

semaphore = asyncio.Semaphore(1)
async def watcher(app: FastAPI):
    global staged_files
    async for changes in awatch(settings.can_staging_path):
        for change, path in changes:
            if path.endswith(".log"):
                if path not in staged_files:
                    staged_files.add(path)
                    asyncio.create_task(handle_file(path, app))

async def handle_file(path: str, app: FastAPI):
    try:
        async with semaphore:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                can_helper.process_candump,
                path
            )
    except Exception as e:
        print(f"Failed to process {path}: {e}")

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    watcher_task = asyncio.create_task(watcher(app))
    try:
        yield
    finally:
        watcher_task.cancel()

        with contextlib.suppress(asyncio.CancelledError):
            await watcher_task

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:1880",
        "http://localhost:1880"
    ],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/api/can/logs/zip/{type}")
def zip_logs(type: str, payload: FileRequest):
    log_dirs = {
        "raw": settings.can_raw_path,
        "processed": settings.can_processed_path
    }

    if type not in log_dirs:
        raise HTTPException(status_code=400, detail=f"Invalid log type: {type}")

    log_dir = Path(log_dirs[type]).resolve()
    memory_file = BytesIO()

    with ZipFile(memory_file, mode="w", compression=ZIP_DEFLATED) as zf:
        for filename in payload.filenames:
            if type == "processed":
                filename = Path(filename).with_suffix(".csv").name.replace("candump", "FE14")

            file_path = (log_dir / filename).resolve()

            if file_path.parent != log_dir:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid filename: {filename}"
                )

            if not file_path.is_file():
                raise HTTPException(
                    status_code=404,
                    detail=f"Log file not found: {filename}"
                )

            zf.write(file_path, arcname=file_path.name)

    memory_file.seek(0)

    return StreamingResponse(
        memory_file,
        media_type="application/zip",
    )

@app.get("/api/logs/list")
async def get_log_list():
    raw_path = Path(settings.can_raw_path)
    processed_path = Path(settings.can_processed_path)
    logs = []

    for file in raw_path.iterdir():
        if file.is_file():
            stats = file.stat()
            processed_file = processed_path / file.with_suffix(".csv").name.replace("candump", "FE14")

            logs.append({
                "file_name": file.name,
                "creation_date": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "file_size_raw": humanize.naturalsize(stats.st_size, binary=True),
                "file_size_processed": (humanize.naturalsize(processed_file.stat().st_size, binary=True) if processed_file.is_file() else "N/A")
            })

    logs.sort(key=lambda x: x["creation_date"], reverse=True)

    return logs