from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.common.io import ensure_directory


matplotlib.use("Agg")
sns.set_theme(style="whitegrid")


def generate_plots(df: pd.DataFrame, output_dir: Path, sample_rows: int = 10000) -> list[Path]:
    ensure_directory(output_dir)
    generated_files = [
        plot_top_brands(df, output_dir / "top_brands.png"),
        plot_make_year_distribution(df, output_dir / "make_year_distribution.png"),
    ]

    if {"CAPACITY", "OWN_WEIGHT"}.issubset(df.columns):
        generated_files.append(
            plot_capacity_vs_weight(df, output_dir / "capacity_vs_weight.png", sample_rows)
        )

    return generated_files


def plot_top_brands(df: pd.DataFrame, output_path: Path) -> Path:
    top_brands = df["BRAND"].fillna("Невідомо").value_counts().head(15)
    plt.figure(figsize=(14, 7))
    sns.barplot(x=top_brands.values, y=top_brands.index, hue=top_brands.index, legend=False, palette="viridis")
    plt.title("Топ-15 найпопулярніших марок автомобілів")
    plt.xlabel("Кількість реєстрацій")
    plt.ylabel("Марка")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path


def plot_make_year_distribution(df: pd.DataFrame, output_path: Path) -> Path:
    years = pd.to_numeric(df["MAKE_YEAR"], errors="coerce").dropna()
    years = years[years >= 1980]
    plt.figure(figsize=(12, 6))
    sns.histplot(years, bins=42, color="coral")
    plt.title("Розподіл транспортних засобів за роком випуску")
    plt.xlabel("Рік випуску")
    plt.ylabel("Кількість")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path


def plot_capacity_vs_weight(df: pd.DataFrame, output_path: Path, sample_rows: int) -> Path:
    plot_df = df[["CAPACITY", "OWN_WEIGHT"]].dropna().copy()
    plot_df["CAPACITY"] = pd.to_numeric(plot_df["CAPACITY"], errors="coerce")
    plot_df["OWN_WEIGHT"] = pd.to_numeric(plot_df["OWN_WEIGHT"], errors="coerce")
    plot_df = plot_df.dropna()
    plot_df = plot_df[(plot_df["CAPACITY"] < 6000) & (plot_df["OWN_WEIGHT"] < 4000)]
    if len(plot_df) > sample_rows:
        plot_df = plot_df.sample(sample_rows, random_state=42)

    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=plot_df, x="CAPACITY", y="OWN_WEIGHT", alpha=0.3, s=20)
    plt.title("Залежність ваги авто від об'єму двигуна")
    plt.xlabel("Об'єм двигуна")
    plt.ylabel("Власна вага")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path
