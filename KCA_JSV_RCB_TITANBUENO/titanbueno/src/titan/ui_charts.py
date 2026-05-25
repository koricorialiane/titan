from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PALETTE = {
    "bg": "#f6f1ea",
    "panel": "#fffdf9",
    "ink": "#1f242c",
    "muted": "#6d7782",
    "grid": "#d8d0c4",
    "accent": "#c85f3f",
    "accent_soft": "#e5a084",
    "teal": "#2a9d8f",
    "slate": "#264653",
    "amber": "#e9c46a",
    "rose": "#b56576",
}


def _paper_axes(fig, ax) -> None:
    fig.patch.set_facecolor(PALETTE["bg"])
    ax.set_facecolor(PALETTE["panel"])
    for spine in ax.spines.values():
        spine.set_color(PALETTE["grid"])
    ax.tick_params(colors=PALETTE["ink"])
    ax.xaxis.label.set_color(PALETTE["ink"])
    ax.yaxis.label.set_color(PALETTE["ink"])
    ax.title.set_color(PALETTE["ink"])
    ax.grid(True, color=PALETTE["grid"], alpha=0.55, linewidth=0.8)


def figure_link_budget(coverage_df: pd.DataFrame, title: str):
    row = coverage_df.iloc[0]
    labels = ["Ptx", "Gtx", "Grx", "Losses", "Sensitivity"]
    increments = [
        43.0,
        18.0,
        0.0,
        -float(row["max_path_loss_db"] - row["receiver_sensitivity_dbm"]),
        -float(row["receiver_sensitivity_dbm"]),
    ]
    starts = np.cumsum([0.0] + increments[:-1])
    ends = starts + np.asarray(increments)
    colors = [PALETTE["slate"], PALETTE["teal"], PALETTE["amber"], PALETTE["rose"], PALETTE["accent"]]

    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    _paper_axes(fig, ax)

    positions = np.arange(len(labels))
    for idx, (label, start, end, color) in enumerate(zip(labels, starts, ends, colors)):
        left = min(start, end)
        width = abs(end - start)
        ax.barh(idx, width, left=left, color=color, edgecolor="none", height=0.65)
        ax.text(end + 1.0, idx, f"{end:.1f} dB", va="center", ha="left", fontsize=9, color=PALETTE["ink"])

    ax.axvline(float(row["max_path_loss_db"]), color=PALETTE["accent"], linestyle="--", linewidth=1.4)
    ax.text(
        float(row["max_path_loss_db"]) + 1.0,
        len(labels) - 0.35,
        f"Lmax = {float(row['max_path_loss_db']):.1f} dB",
        fontsize=10,
        fontweight="bold",
        color=PALETTE["accent"],
    )
    ax.set_yticks(positions)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("Cumulative budget (dB)")
    ax.set_title(title, loc="left", fontweight="bold")
    ax.grid(True, axis="x", color=PALETTE["grid"], alpha=0.6)
    fig.tight_layout()
    return fig


def figure_district_radii(capacity_df: pd.DataFrame, coverage_df: pd.DataFrame):
    coverage_radius = float(coverage_df.iloc[0]["coverage_radius_km"])
    labels = [f"N={int(value)}" for value in capacity_df["reuse_factor_n"]]
    values = capacity_df["capacity_radius_km"].to_numpy(dtype=float)
    recommended = capacity_df["recommended"].to_numpy(dtype=bool)
    colors = [PALETTE["accent"] if flag else PALETTE["slate"] for flag in recommended]

    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    _paper_axes(fig, ax)
    bars = ax.bar(labels, values, color=colors, edgecolor="none")
    ax.axhline(coverage_radius, color=PALETTE["teal"], linestyle="--", linewidth=1.8, label="Coverage radius")
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.008, f"{value:.3f} km", ha="center", fontsize=9, color=PALETTE["ink"])
    ax.set_ylabel("Radius (km)")
    ax.set_title("Scenario A: coverage radius versus traffic-limited radius", loc="left", fontweight="bold")
    ax.legend(frameon=False)
    fig.tight_layout()
    return fig


def figure_district_tradeoff(capacity_df: pd.DataFrame, snr_required_db: float):
    labels = [f"N={int(value)}" for value in capacity_df["reuse_factor_n"]]
    capacity = capacity_df["site_capacity_erlang"].to_numpy(dtype=float)
    sir = capacity_df["sectorized_sir_db"].to_numpy(dtype=float)
    recommended = capacity_df["recommended"].to_numpy(dtype=bool)
    colors = [PALETTE["accent"] if flag else PALETTE["amber"] for flag in recommended]

    fig, ax1 = plt.subplots(figsize=(8.2, 4.8))
    _paper_axes(fig, ax1)
    bars = ax1.bar(labels, capacity, color=colors, edgecolor="none", label="Site capacity")
    ax1.set_ylabel("Capacity (Erlang)")
    ax1.set_title("Scenario A: capacity and interference trade-off", loc="left", fontweight="bold")

    ax2 = ax1.twinx()
    ax2.set_facecolor("none")
    ax2.plot(labels, sir, color=PALETTE["slate"], marker="o", linewidth=2.2, label="Sectorized SIR")
    ax2.axhline(snr_required_db, color=PALETTE["rose"], linestyle=":", linewidth=1.6, label="Required SNR")
    ax2.set_ylabel("SIR / SNR (dB)", color=PALETTE["ink"])
    ax2.tick_params(colors=PALETTE["ink"])

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels2, frameon=False, loc="upper left")
    fig.tight_layout()
    return fig


def figure_festival_radii(capacity_df: pd.DataFrame):
    row = capacity_df.iloc[0]
    labels = ["Coverage", "Capacity"]
    values = [float(row["coverage_radius_km"]), float(row["capacity_radius_km"])]
    colors = [PALETTE["teal"], PALETTE["accent"]]

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    _paper_axes(fig, ax)
    bars = ax.bar(labels, values, color=colors, edgecolor="none")
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.06, f"{value:.3f} km", ha="center", fontsize=10, color=PALETTE["ink"])
    ax.set_ylabel("Radius (km)")
    ax.set_title("Scenario B: coverage does not solve the traffic problem", loc="left", fontweight="bold")
    fig.tight_layout()
    return fig


def figure_festival_splitting(splitting_df: pd.DataFrame):
    labels = [f"S{int(stage)}" for stage in splitting_df["split_stage"]]
    supported = splitting_df["supported_users_km2"].to_numpy(dtype=float)
    demand = float(splitting_df["demand_users_km2"].iloc[0])
    radius = splitting_df["radius_km"].to_numpy(dtype=float)
    recommended = splitting_df["recommended"].to_numpy(dtype=bool)
    colors = [PALETTE["accent"] if flag else PALETTE["amber"] for flag in recommended]

    fig, ax1 = plt.subplots(figsize=(8.4, 4.8))
    _paper_axes(fig, ax1)
    bars = ax1.bar(labels, supported, color=colors, edgecolor="none", label="Supported users/km2")
    ax1.axhline(demand, color=PALETTE["rose"], linestyle="--", linewidth=1.6, label="Demand")
    ax1.set_ylabel("Supported users per km2")
    ax1.set_title("Scenario B: cell splitting required to meet demand", loc="left", fontweight="bold")

    ax2 = ax1.twinx()
    ax2.set_facecolor("none")
    ax2.plot(labels, radius, color=PALETTE["slate"], marker="o", linewidth=2.0, label="Resulting radius")
    ax2.set_ylabel("Radius (km)", color=PALETTE["ink"])
    ax2.tick_params(colors=PALETTE["ink"])

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels2, frameon=False, loc="upper left")
    fig.tight_layout()
    return fig


def figure_solution_summary(
    district_capacity_df: pd.DataFrame,
    festival_capacity_df: pd.DataFrame,
    festival_splitting_df: pd.DataFrame,
):
    district = district_capacity_df.loc[district_capacity_df["recommended"]].iloc[0]
    festival = festival_capacity_df.iloc[0]
    split = festival_splitting_df.loc[festival_splitting_df["recommended"]].iloc[0]

    fig, ax = plt.subplots(figsize=(9.6, 5.2))
    fig.patch.set_facecolor(PALETTE["bg"])
    ax.set_facecolor(PALETTE["panel"])
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(PALETTE["grid"])

    ax.text(0.04, 0.92, "Operacion Nexo 5G/6G", transform=ax.transAxes, fontsize=22, fontweight="bold", color=PALETTE["ink"])
    ax.text(0.04, 0.84, "Executive figure: recommended radio design choices for Nueva Pangea", transform=ax.transAxes, fontsize=11, color=PALETTE["muted"])

    boxes = [
        (0.05, 0.14, 0.4, 0.55, "Scenario A · Financial District", [
            f"Recommended reuse: N = {int(district['reuse_factor_n'])}",
            f"Coverage radius: {float(district['coverage_radius_km']):.3f} km",
            f"Capacity radius: {float(district['capacity_radius_km']):.3f} km",
            f"Sectorized SIR: {float(district['sectorized_sir_db']):.2f} dB",
            f"Sites in 1 km2: {int(district['sites_for_target_area'])}",
        ], PALETTE["accent"]),
        (0.54, 0.14, 0.4, 0.55, "Scenario B · Global Festival", [
            f"Coverage radius: {float(festival['coverage_radius_km']):.3f} km",
            f"Capacity radius: {float(festival['capacity_radius_km']):.3f} km",
            f"Recommended split stage: S{int(split['split_stage'])}",
            f"Supported density: {float(split['supported_users_km2']):.0f} users/km2",
            f"Cells in 1 km2: {int(split['sites_for_target_area'])}",
        ], PALETTE["teal"]),
    ]

    for left, bottom, width, height, title, bullets, color in boxes:
        rect = plt.Rectangle((left, bottom), width, height, transform=ax.transAxes, facecolor="white", edgecolor=color, linewidth=2.0)
        ax.add_patch(rect)
        ax.text(left + 0.02, bottom + height - 0.08, title, transform=ax.transAxes, fontsize=14, fontweight="bold", color=color)
        y = bottom + height - 0.16
        for bullet in bullets:
            ax.text(left + 0.03, y, f"- {bullet}", transform=ax.transAxes, fontsize=11, color=PALETTE["ink"])
            y -= 0.09

    ax.text(
        0.04,
        0.05,
        "Conclusion: Scenario A is traffic-limited but still solvable with sectorization and N=4. Scenario B is dominated by density and demands cell splitting.",
        transform=ax.transAxes,
        fontsize=10,
        color=PALETTE["muted"],
    )
    fig.tight_layout()
    return fig
