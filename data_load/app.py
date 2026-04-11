from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.config import get_settings
from src.common.db import load_csv_to_sqlite, write_pipeline_metadata
from src.common.io import download_and_extract_csv, ensure_directory


def main() -> None:
    settings = get_settings()
    ensure_directory(settings.raw_data_dir)
    ensure_directory(settings.runtime_dir)

    csv_path = settings.csv_path
    if not csv_path.exists():
        if not settings.download_if_missing:
            raise FileNotFoundError(
                f"CSV file {csv_path} is missing. Provide the dataset or enable DOWNLOAD_IF_MISSING=true."
            )
        csv_path = download_and_extract_csv(settings.dataset_url, settings.raw_data_dir)

    summary = load_csv_to_sqlite(csv_path, settings.database_path)
    write_pipeline_metadata(
        settings.database_path,
        stage="data_load",
        status="completed",
        details=f"Imported {summary['row_count']} rows into {summary['table_name']}.",
    )
    print(
        f"Loaded {summary['row_count']} rows from {summary['csv_path']} into {settings.database_path}"
    )


if __name__ == "__main__":
    main()
