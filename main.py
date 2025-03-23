import argparse
import asyncio
import logging
import shutil
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def copy_file(file_path: Path, output_folder: Path):
    try:
        ext = file_path.suffix[1:] or "unknown"
        target_folder = output_folder / ext
        target_folder.mkdir(parents=True, exist_ok=True)

        output = target_folder / file_path.name

        loop = asyncio.get_running_loop()

        await loop.run_in_executor(None, shutil.copy2, file_path, output)

        logging.info(f"Copied: {file_path} -> {output}")
    except Exception as e:
        logging.error(f"Error copying {file_path}: {e}")


async def read_folder(source_folder: Path, output_folder: Path):
    tasks = []

    for file_path in source_folder.rglob("*.*"):
        if file_path.is_file():
            tasks.append(copy_file(file_path, output_folder))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Async file sorter by extension")
    parser.add_argument(
        "--source", "-s", required=True, type=str, help="Source folder path"
    )
    parser.add_argument(
        "--output", "-o", required=True, type=str, help="Output folder path"
    )
    args = parser.parse_args()

    source_folder = Path(args.source)
    output_folder = Path(args.output)

    if not source_folder.exists() or not source_folder.is_dir():
        logging.error("Source folder does not exist or is not a directory.")
        exit(1)

    asyncio.run(read_folder(source_folder, output_folder))

    logging.info("Sorting completed.")
