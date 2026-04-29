from __future__ import annotations

import json
import time
import zipfile
from pathlib import Path
from typing import Any


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def download_and_extract_csv(dataset_url: str, output_dir: Path) -> Path:
    import requests

    ensure_directory(output_dir)
    archive_path = output_dir / "dataset_download.zip"
    temp_archive_path = output_dir / "dataset_download.zip.part"
    last_error: Exception | None = None

    for attempt in range(1, 4):
        try:
            with requests.get(dataset_url, stream=True, timeout=(30, 120)) as response:
                response.raise_for_status()
                with temp_archive_path.open("wb") as archive_file:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            archive_file.write(chunk)
            temp_archive_path.replace(archive_path)
            break
        except (requests.RequestException, OSError) as exc:
            last_error = exc
            temp_archive_path.unlink(missing_ok=True)
            archive_path.unlink(missing_ok=True)
            if attempt == 3:
                raise RuntimeError(
                    f"Failed to download dataset from {dataset_url} after {attempt} attempts."
                ) from exc
            time.sleep(attempt)
    else:
        raise RuntimeError(f"Failed to download dataset from {dataset_url}.") from last_error

    try:
        with zipfile.ZipFile(archive_path) as archive:
            csv_members = [name for name in archive.namelist() if name.lower().endswith(".csv")]
            if not csv_members:
                raise FileNotFoundError("The downloaded archive does not contain a CSV file.")

            archive.extractall(output_dir)
            return output_dir / csv_members[0]
    except zipfile.BadZipFile as exc:
        raise RuntimeError(f"Downloaded dataset archive from {dataset_url} is corrupted.") from exc
    finally:
        temp_archive_path.unlink(missing_ok=True)
        archive_path.unlink(missing_ok=True)


def read_transport_csv(csv_path: Path, *, chunksize: int | None = None) -> Any:
    import pandas as pd

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file was not found: {csv_path}")
    return pd.read_csv(csv_path, sep=";", chunksize=chunksize, low_memory=False)


def write_json(data: dict[str, Any], path: Path) -> Path:
    ensure_directory(path.parent)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def read_json(path: Path, default: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.exists():
        return {} if default is None else default
    return json.loads(path.read_text(encoding="utf-8"))
