import contextlib
import asyncio
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.settings import settings
from .api.router import router
from .tasks.jobs import watcher, processing_tasks

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(settings.CAN_INTAKE_PATH, exist_ok=True)
    os.makedirs(settings.CAN_STAGING_PATH, exist_ok=True)
    os.makedirs(settings.CAN_RAW_PATH, exist_ok=True)
    os.makedirs(settings.CAN_PROCESSED_PATH, exist_ok=True)
    os.makedirs(settings.CAN_REPORTS_PATH, exist_ok=True)
    os.makedirs(settings.DBC_DIR, exist_ok=True)

    watcher_task = asyncio.create_task(watcher())
    try:
        yield
    finally:
        watcher_task.cancel()

        with contextlib.suppress(asyncio.CancelledError):
            await watcher_task

        if processing_tasks:
            await asyncio.gather(*processing_tasks, return_exceptions=True)

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

app.include_router(router)