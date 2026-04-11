from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.analysis import load_transport_dataframe
from src.common.config import get_settings
from src.common.db import wait_for_database, write_pipeline_metadata
from src.common.io import ensure_directory, write_json
from src.common.visuals import generate_plots


def main() -> None:
    settings = get_settings()
    ensure_directory(settings.plots_dir)

    wait_for_database(
        settings.database_path,
        timeout_seconds=settings.db_wait_timeout_seconds,
    )
    dataframe = load_transport_dataframe(settings.database_path)
    plot_paths = generate_plots(
        dataframe,
        settings.plots_dir,
        sample_rows=settings.sample_plot_rows,
    )

    manifest_path = settings.reports_dir / "visualization_manifest.json"
    write_json(
        {
            "plots": [path.name for path in plot_paths],
            "count": len(plot_paths),
        },
        manifest_path,
    )
    write_pipeline_metadata(
        settings.database_path,
        stage="visualization",
        status="completed",
        details=f"Generated {len(plot_paths)} plots.",
    )
    print(f"Generated plots: {', '.join(path.name for path in plot_paths)}")


if __name__ == "__main__":
    main()
