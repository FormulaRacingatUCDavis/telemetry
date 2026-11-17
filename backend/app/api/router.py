from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from pydantic import BaseModel
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from typing import List
import humanize
from datetime import datetime

from ..core.settings import settings

router = APIRouter()

class FileRequest(BaseModel):
    filenames: List[str]

@router.post("/api/can/logs/zip/{type}")
def zip_logs(type: str, payload: FileRequest):
    log_dirs = {
        "raw": settings.CAN_RAW_PATH,
        "processed": settings.CAN_PROCESSED_PATH
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

@router.get("/api/logs/list")
async def get_log_list():
    raw_path = Path(settings.CAN_RAW_PATH)
    processed_path = Path(settings.CAN_PROCESSED_PATH)
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