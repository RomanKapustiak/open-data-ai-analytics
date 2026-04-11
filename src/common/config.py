from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CSV_NAME = "tz_opendata_z01012022_po01032022.csv"
DEFAULT_DATASET_URL = (
    "https://data.gov.ua/dataset/0ffd8b75-0628-48cc-952a-9302f9799ec0/"
    "resource/bef7b47b-7963-44b5-88a8-f84241137b5b/download/reestrtz2022.zip"
)


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    project_root: Path = PROJECT_ROOT
    data_dir: Path = PROJECT_ROOT / "data"
    raw_data_dir: Path = PROJECT_ROOT / "data" / "raw"
    reports_dir: Path = PROJECT_ROOT / "reports"
    plots_dir: Path = PROJECT_ROOT / "reports" / "plots"
    runtime_dir: Path = PROJECT_ROOT / "runtime"
    database_path: Path = PROJECT_ROOT / "runtime" / "transport_registry.sqlite3"
    csv_name: str = DEFAULT_CSV_NAME
    dataset_url: str = DEFAULT_DATASET_URL
    download_if_missing: bool = False
    web_host: str = "0.0.0.0"
    web_port: int = 8000
    db_wait_timeout_seconds: int = 120
    sample_plot_rows: int = 10000

    @property
    def csv_path(self) -> Path:
        return self.raw_data_dir / self.csv_name


def get_settings() -> Settings:
    data_dir = Path(os.getenv("DATA_DIR", PROJECT_ROOT / "data")).resolve()
    raw_data_dir = Path(os.getenv("RAW_DATA_DIR", data_dir / "raw")).resolve()
    reports_dir = Path(os.getenv("REPORTS_DIR", PROJECT_ROOT / "reports")).resolve()
    plots_dir = Path(os.getenv("PLOTS_DIR", reports_dir / "plots")).resolve()
    runtime_dir = Path(os.getenv("RUNTIME_DIR", PROJECT_ROOT / "runtime")).resolve()

    database_path = Path(
        os.getenv("DATABASE_PATH", runtime_dir / "transport_registry.sqlite3")
    ).resolve()

    return Settings(
        project_root=PROJECT_ROOT,
        data_dir=data_dir,
        raw_data_dir=raw_data_dir,
        reports_dir=reports_dir,
        plots_dir=plots_dir,
        runtime_dir=runtime_dir,
        database_path=database_path,
        csv_name=os.getenv("CSV_NAME", DEFAULT_CSV_NAME),
        dataset_url=os.getenv("DATASET_URL", DEFAULT_DATASET_URL),
        download_if_missing=_as_bool(os.getenv("DOWNLOAD_IF_MISSING"), False),
        web_host=os.getenv("WEB_HOST", "0.0.0.0"),
        web_port=int(os.getenv("WEB_PORT", "8000")),
        db_wait_timeout_seconds=int(os.getenv("DB_WAIT_TIMEOUT_SECONDS", "120")),
        sample_plot_rows=int(os.getenv("SAMPLE_PLOT_ROWS", "10000")),
    )
