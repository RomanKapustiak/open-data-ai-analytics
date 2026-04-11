from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.analysis import build_research_report, load_transport_dataframe
from src.common.config import get_settings
from src.common.db import wait_for_database, write_pipeline_metadata
from src.common.io import ensure_directory, write_json


def main() -> None:
    settings = get_settings()
    ensure_directory(settings.reports_dir)

    wait_for_database(
        settings.database_path,
        timeout_seconds=settings.db_wait_timeout_seconds,
    )
    dataframe = load_transport_dataframe(settings.database_path)
    report = build_research_report(dataframe)

    report_path = settings.reports_dir / "data_research_report.json"
    write_json(report, report_path)
    write_pipeline_metadata(
        settings.database_path,
        stage="data_research",
        status="completed",
        details=f"Saved report to {report_path.name}",
    )
    print(f"Research report saved to {report_path}")


if __name__ == "__main__":
    main()
