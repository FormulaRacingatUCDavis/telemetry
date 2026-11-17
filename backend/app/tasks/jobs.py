import asyncio
from pathlib import Path
from watchfiles import awatch
import shutil

from ..processing import candump
from ..core.settings import settings

can_analyzer = candump.Analyzer()
semaphore = asyncio.Semaphore(1)
staged_files = set()
processing_tasks = set()

async def watcher():
    async for changes in awatch(settings.CAN_STAGING_PATH):
        for change, path in changes:
            if path.endswith(".log") and Path(path).is_file():
                if path not in staged_files:
                    staged_files.add(path)
                    task = asyncio.create_task(handle_file(path))
                    processing_tasks.add(task)
                    task.add_done_callback(processing_tasks.discard)

def generate_reports(log: str):
    can_analyzer.decode(log)

    filename = Path(log).with_suffix(".csv").name.replace("candump", "FE14")
    output_path = Path(settings.CAN_PROCESSED_PATH) / filename

    can_analyzer.data.to_csv(output_path, index=False)
    # Generate interactive HTML

    shutil.move(log, Path(settings.CAN_RAW_PATH) / Path(log).name)

async def handle_file(path: str):
    try:
        async with semaphore:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                generate_reports,
                path
            )
    except Exception as e:
        print(f"Failed to process {path}: {e}")
    finally:
        staged_files.discard(path)