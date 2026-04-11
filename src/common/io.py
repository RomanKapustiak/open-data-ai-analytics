from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path
from typing import Any


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def download_and_extract_csv(dataset_url: str, output_dir: Path) -> Path:
    import requests

    ensure_directory(output_dir)
    response = requests.get(dataset_url, timeout=120)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        csv_members = [name for name in archive.namelist() if name.lower().endswith(".csv")]
        if not csv_members:
            raise FileNotFoundError("The downloaded archive does not contain a CSV file.")

        archive.extractall(output_dir)
        return output_dir / csv_members[0]


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
