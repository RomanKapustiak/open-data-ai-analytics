from __future__ import annotations

import sqlite3
import time
from pathlib import Path

from src.common.io import ensure_directory


TRANSPORT_TABLE = "transport_data"


def get_connection(database_path: Path) -> sqlite3.Connection:
    ensure_directory(database_path.parent)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def load_csv_to_sqlite(
    csv_path: Path,
    database_path: Path,
    table_name: str = TRANSPORT_TABLE,
    *,
    chunksize: int = 20000,
) -> dict[str, int | str]:
    import pandas as pd

    total_rows = 0

    with get_connection(database_path) as connection:
        for index, chunk in enumerate(
            pd.read_csv(csv_path, sep=";", chunksize=chunksize, low_memory=False)
        ):
            mode = "replace" if index == 0 else "append"
            chunk.to_sql(table_name, connection, if_exists=mode, index=False)
            total_rows += len(chunk)

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS pipeline_metadata (
                stage TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                details TEXT,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            INSERT INTO pipeline_metadata(stage, status, details, updated_at)
            VALUES(?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(stage) DO UPDATE SET
                status=excluded.status,
                details=excluded.details,
                updated_at=CURRENT_TIMESTAMP
            """,
            ("data_load", "completed", f"Imported {total_rows} rows from {csv_path.name}"),
        )
        connection.commit()

    return {"table_name": table_name, "row_count": total_rows, "csv_path": str(csv_path)}


def table_exists(database_path: Path, table_name: str = TRANSPORT_TABLE) -> bool:
    with get_connection(database_path) as connection:
        result = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        ).fetchone()
    return result is not None


def wait_for_database(
    database_path: Path,
    *,
    table_name: str = TRANSPORT_TABLE,
    timeout_seconds: int = 120,
    poll_interval: float = 2.0,
) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        if database_path.exists() and table_exists(database_path, table_name):
            return
        time.sleep(poll_interval)
    raise TimeoutError(
        f"Database {database_path} with table {table_name} was not ready after {timeout_seconds}s."
    )


def read_sql_query(database_path: Path, query: str):
    import pandas as pd

    with get_connection(database_path) as connection:
        return pd.read_sql_query(query, connection)


def write_pipeline_metadata(database_path: Path, stage: str, status: str, details: str) -> None:
    with get_connection(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS pipeline_metadata (
                stage TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                details TEXT,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            INSERT INTO pipeline_metadata(stage, status, details, updated_at)
            VALUES(?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(stage) DO UPDATE SET
                status=excluded.status,
                details=excluded.details,
                updated_at=CURRENT_TIMESTAMP
            """,
            (stage, status, details),
        )
        connection.commit()


def fetch_table_columns(database_path: Path, table_name: str = TRANSPORT_TABLE) -> list[str]:
    with get_connection(database_path) as connection:
        rows = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    return [str(row["name"]) for row in rows]
