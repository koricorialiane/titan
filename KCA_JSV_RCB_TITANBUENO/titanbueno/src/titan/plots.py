from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .ui_charts import (
    figure_district_radii,
    figure_district_tradeoff,
    figure_festival_radii,
    figure_festival_splitting,
    figure_link_budget,
    figure_solution_summary,
)


def _save_figure(fig, output_path: Path) -> None:
    fig.tight_layout()
    fig.savefig(output_path, dpi=220, facecolor=fig.get_facecolor())
    plt.close(fig)


def save_link_budget_plot(coverage_df: pd.DataFrame, output_path: Path, title: str) -> None:
    _save_figure(figure_link_budget(coverage_df, title), output_path)


def save_district_radii_plot(capacity_df: pd.DataFrame, coverage_df: pd.DataFrame, output_path: Path) -> None:
    _save_figure(figure_district_radii(capacity_df, coverage_df), output_path)


def save_district_tradeoff_plot(capacity_df: pd.DataFrame, snr_required_db: float, output_path: Path) -> None:
    _save_figure(figure_district_tradeoff(capacity_df, snr_required_db), output_path)


def save_festival_radii_plot(capacity_df: pd.DataFrame, output_path: Path) -> None:
    _save_figure(figure_festival_radii(capacity_df), output_path)


def save_festival_splitting_plot(splitting_df: pd.DataFrame, output_path: Path) -> None:
    _save_figure(figure_festival_splitting(splitting_df), output_path)


def save_solution_summary_plot(
    district_capacity_df: pd.DataFrame,
    festival_capacity_df: pd.DataFrame,
    festival_splitting_df: pd.DataFrame,
    output_path: Path,
) -> None:
    _save_figure(figure_solution_summary(district_capacity_df, festival_capacity_df, festival_splitting_df), output_path)
