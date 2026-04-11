from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from src.common.db import TRANSPORT_TABLE, read_sql_query


NUMERIC_COLUMNS = ["REG_ADDR_KOATUU", "OPER_CODE", "MAKE_YEAR", "CAPACITY", "OWN_WEIGHT", "TOTAL_WEIGHT"]


def load_transport_dataframe(database_path: Path, table_name: str = TRANSPORT_TABLE) -> pd.DataFrame:
    return read_sql_query(database_path, f"SELECT * FROM {table_name}")


def build_quality_report(df: pd.DataFrame) -> dict[str, Any]:
    null_counts = df.isna().sum().sort_values(ascending=False)
    duplicate_rows = int(df.duplicated().sum())

    numeric_type_issues: dict[str, int] = {}
    for column in NUMERIC_COLUMNS:
        if column not in df.columns:
            continue
        converted = pd.to_numeric(df[column], errors="coerce")
        issue_mask = df[column].notna() & converted.isna()
        numeric_type_issues[column] = int(issue_mask.sum())

    invalid_make_year = 0
    if "MAKE_YEAR" in df.columns:
        years = pd.to_numeric(df["MAKE_YEAR"], errors="coerce")
        invalid_make_year = int(((years < 1886) | (years > 2030)).fillna(False).sum())

    invalid_capacity = 0
    if "CAPACITY" in df.columns:
        capacities = pd.to_numeric(df["CAPACITY"], errors="coerce")
        invalid_capacity = int((capacities < 0).fillna(False).sum())

    invalid_own_weight = 0
    if "OWN_WEIGHT" in df.columns:
        own_weight = pd.to_numeric(df["OWN_WEIGHT"], errors="coerce")
        invalid_own_weight = int((own_weight < 0).fillna(False).sum())

    return {
        "dataset_shape": {"rows": int(df.shape[0]), "columns": int(df.shape[1])},
        "missing_values": {column: int(count) for column, count in null_counts.items()},
        "duplicate_rows": duplicate_rows,
        "numeric_type_issues": numeric_type_issues,
        "value_validations": {
            "invalid_make_year": invalid_make_year,
            "invalid_capacity": invalid_capacity,
            "invalid_own_weight": invalid_own_weight,
        },
        "top_columns_with_missing_values": [
            {"column": column, "missing_count": int(count)}
            for column, count in null_counts.head(10).items()
        ],
    }


def build_research_report(df: pd.DataFrame) -> dict[str, Any]:
    make_year = pd.to_numeric(df.get("MAKE_YEAR"), errors="coerce")
    capacity = pd.to_numeric(df.get("CAPACITY"), errors="coerce")
    own_weight = pd.to_numeric(df.get("OWN_WEIGHT"), errors="coerce")

    top_brands = (
        df["BRAND"].fillna("Невідомо").value_counts().head(10).to_dict()
        if "BRAND" in df.columns
        else {}
    )
    fuel_distribution = (
        df["FUEL"].fillna("Невідомо").value_counts().head(10).to_dict()
        if "FUEL" in df.columns
        else {}
    )
    body_distribution = (
        df["BODY"].fillna("Невідомо").value_counts().head(10).to_dict()
        if "BODY" in df.columns
        else {}
    )

    return {
        "dataset_overview": {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "unique_brands": int(df["BRAND"].nunique(dropna=True)) if "BRAND" in df.columns else 0,
            "unique_models": int(df["MODEL"].nunique(dropna=True)) if "MODEL" in df.columns else 0,
        },
        "numeric_summary": {
            "make_year": _summarize_series(make_year),
            "capacity": _summarize_series(capacity),
            "own_weight": _summarize_series(own_weight),
        },
        "top_brands": top_brands,
        "fuel_distribution": fuel_distribution,
        "body_distribution": body_distribution,
    }


def _summarize_series(series: pd.Series) -> dict[str, float | int | None]:
    cleaned = series.dropna()
    if cleaned.empty:
        return {"count": 0, "min": None, "max": None, "mean": None, "median": None}
    return {
        "count": int(cleaned.count()),
        "min": float(cleaned.min()),
        "max": float(cleaned.max()),
        "mean": float(cleaned.mean()),
        "median": float(cleaned.median()),
    }
