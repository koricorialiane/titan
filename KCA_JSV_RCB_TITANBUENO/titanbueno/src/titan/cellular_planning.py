import math

import pandas as pd

from .config import DistrictScenario, FestivalScenario, NetworkConfig
from .propagation import (
    estimated_sir_db,
    hexagon_area_km2,
    hexagon_radius_from_area_km2,
    inverse_erlang_b,
    maximum_allowable_path_loss_db,
    radius_from_log_path_loss_km,
    receiver_sensitivity_dbm,
    reuse_distance_km,
    reuse_ratio,
    site_count_for_area,
    thermal_noise_dbm,
    traffic_density_erlang_km2,
    traffic_per_user_erlang,
)


def district_coverage_table(
    scenario: DistrictScenario = DistrictScenario(),
    config: NetworkConfig = NetworkConfig(),
) -> pd.DataFrame:
    noise_dbm = thermal_noise_dbm(config.bandwidth_hz, config.noise_figure_db)
    sensitivity_dbm = receiver_sensitivity_dbm(noise_dbm, scenario.snr_required_db, config.implementation_losses_db)
    max_path_loss_db = maximum_allowable_path_loss_db(
        config.tx_power_dbm,
        config.tx_gain_dbi,
        config.rx_gain_dbi,
        config.additional_losses_db,
        sensitivity_dbm,
    )
    coverage_radius_km = radius_from_log_path_loss_km(
        max_path_loss_db,
        scenario.propagation_intercept_db,
        scenario.propagation_slope_db,
    )
    user_traffic_erlang = traffic_per_user_erlang(scenario.calls_per_hour_per_user, scenario.holding_time_min)
    density_traffic_erlang = traffic_density_erlang_km2(scenario.users_density_km2, user_traffic_erlang)

    return pd.DataFrame(
        [
            {
                "scenario": "A_distrito_financiero",
                "thermal_noise_dbm": noise_dbm,
                "receiver_sensitivity_dbm": sensitivity_dbm,
                "max_path_loss_db": max_path_loss_db,
                "coverage_radius_km": coverage_radius_km,
                "traffic_per_user_erlang": user_traffic_erlang,
                "traffic_density_erlang_km2": density_traffic_erlang,
                "target_area_km2": scenario.target_area_km2,
                "propagation_model": f"L_p = {scenario.propagation_intercept_db:.0f} + {scenario.propagation_slope_db:.0f} log10(d)",
            }
        ]
    )


def district_capacity_table(
    coverage_table: pd.DataFrame,
    scenario: DistrictScenario = DistrictScenario(),
    config: NetworkConfig = NetworkConfig(),
) -> pd.DataFrame:
    coverage_radius_km = float(coverage_table.iloc[0]["coverage_radius_km"])
    traffic_density = float(coverage_table.iloc[0]["traffic_density_erlang_km2"])
    rows = []

    for reuse_factor in scenario.reuse_factors:
        channels_per_site = max(config.total_channels // reuse_factor, 1)
        channels_per_sector = max(channels_per_site // scenario.sectors_per_site, 1)
        sector_capacity = inverse_erlang_b(channels_per_sector, config.blocking_probability)
        site_capacity = sector_capacity * scenario.sectors_per_site
        capacity_area = site_capacity / traffic_density if traffic_density else math.inf
        capacity_radius = hexagon_radius_from_area_km2(capacity_area)
        design_radius = min(coverage_radius_km, capacity_radius)
        design_area = hexagon_area_km2(design_radius)
        sir_sectorized = estimated_sir_db(reuse_factor, scenario.path_loss_exponent, interferers=2)
        sir_omni = estimated_sir_db(reuse_factor, scenario.path_loss_exponent, interferers=6)

        rows.append(
            {
                "reuse_factor_n": reuse_factor,
                "reuse_ratio_d_over_r": reuse_ratio(reuse_factor),
                "reuse_distance_km_if_design_radius": reuse_distance_km(design_radius, reuse_factor),
                "channels_per_site": channels_per_site,
                "channels_per_sector": channels_per_sector,
                "sector_capacity_erlang": sector_capacity,
                "site_capacity_erlang": site_capacity,
                "capacity_area_km2": capacity_area,
                "capacity_radius_km": capacity_radius,
                "coverage_radius_km": coverage_radius_km,
                "design_radius_km": design_radius,
                "design_area_km2": design_area,
                "sectorized_sir_db": sir_sectorized,
                "omnidirectional_sir_db": sir_omni,
                "sir_margin_db": sir_sectorized - scenario.snr_required_db,
                "limiting_factor": "capacity" if capacity_radius < coverage_radius_km else "coverage",
                "sites_for_target_area": site_count_for_area(scenario.target_area_km2, design_area),
            }
        )

    table = pd.DataFrame(rows).sort_values("reuse_factor_n").reset_index(drop=True)
    feasible = table[table["sectorized_sir_db"] >= scenario.snr_required_db]
    recommended_n = int(feasible.iloc[0]["reuse_factor_n"]) if not feasible.empty else int(table.iloc[0]["reuse_factor_n"])
    table["recommended"] = table["reuse_factor_n"].eq(recommended_n)
    return table


def festival_coverage_table(
    scenario: FestivalScenario = FestivalScenario(),
    config: NetworkConfig = NetworkConfig(),
) -> pd.DataFrame:
    noise_dbm = thermal_noise_dbm(config.bandwidth_hz, config.noise_figure_db)
    sensitivity_dbm = receiver_sensitivity_dbm(noise_dbm, scenario.snr_required_db, config.implementation_losses_db)
    max_path_loss_db = maximum_allowable_path_loss_db(
        config.tx_power_dbm,
        config.tx_gain_dbi,
        config.rx_gain_dbi,
        config.additional_losses_db,
        sensitivity_dbm,
    )
    coverage_radius_km = radius_from_log_path_loss_km(
        max_path_loss_db,
        scenario.propagation_intercept_db,
        scenario.propagation_slope_db,
    )
    user_traffic_erlang = traffic_per_user_erlang(scenario.calls_per_hour_per_user, scenario.holding_time_min)
    density_traffic_erlang = traffic_density_erlang_km2(scenario.users_density_km2, user_traffic_erlang)

    return pd.DataFrame(
        [
            {
                "scenario": "B_festival_global",
                "thermal_noise_dbm": noise_dbm,
                "receiver_sensitivity_dbm": sensitivity_dbm,
                "max_path_loss_db": max_path_loss_db,
                "coverage_radius_km": coverage_radius_km,
                "traffic_per_user_erlang": user_traffic_erlang,
                "traffic_density_erlang_km2": density_traffic_erlang,
                "target_area_km2": scenario.target_area_km2,
                "propagation_model": f"L_p = {scenario.propagation_intercept_db:.0f} + {scenario.propagation_slope_db:.0f} log10(d)",
            }
        ]
    )


def festival_capacity_table(
    coverage_table: pd.DataFrame,
    scenario: FestivalScenario = FestivalScenario(),
    config: NetworkConfig = NetworkConfig(),
) -> pd.DataFrame:
    coverage_radius_km = float(coverage_table.iloc[0]["coverage_radius_km"])
    traffic_density = float(coverage_table.iloc[0]["traffic_density_erlang_km2"])
    cell_capacity = inverse_erlang_b(config.total_channels, config.blocking_probability)
    capacity_area = cell_capacity / traffic_density if traffic_density else math.inf
    capacity_radius = hexagon_radius_from_area_km2(capacity_area)
    design_radius = min(coverage_radius_km, capacity_radius)
    design_area = hexagon_area_km2(design_radius)

    return pd.DataFrame(
        [
            {
                "channels_per_cell": config.total_channels,
                "cell_capacity_erlang": cell_capacity,
                "capacity_area_km2": capacity_area,
                "capacity_radius_km": capacity_radius,
                "coverage_radius_km": coverage_radius_km,
                "design_radius_km": design_radius,
                "design_area_km2": design_area,
                "limiting_factor": "capacity" if capacity_radius < coverage_radius_km else "coverage",
                "sites_for_target_area": site_count_for_area(scenario.target_area_km2, design_area),
            }
        ]
    )


def festival_splitting_table(
    coverage_table: pd.DataFrame,
    scenario: FestivalScenario = FestivalScenario(),
    config: NetworkConfig = NetworkConfig(),
) -> pd.DataFrame:
    base_radius = float(coverage_table.iloc[0]["coverage_radius_km"])
    traffic_density = float(coverage_table.iloc[0]["traffic_density_erlang_km2"])
    user_traffic = float(coverage_table.iloc[0]["traffic_per_user_erlang"])
    cell_capacity = inverse_erlang_b(config.total_channels, config.blocking_probability)
    rows = []
    recommended_stage = None

    for stage in range(scenario.max_split_stage + 1):
        radius = base_radius / (2**stage)
        area = hexagon_area_km2(radius)
        capacity_density = cell_capacity / area if area else math.inf
        supported_users = capacity_density / user_traffic if user_traffic else math.inf
        meets_demand = capacity_density >= traffic_density
        if meets_demand and recommended_stage is None:
            recommended_stage = stage

        rows.append(
            {
                "split_stage": stage,
                "radius_km": radius,
                "area_km2": area,
                "cells_per_original_footprint": 4**stage,
                "capacity_density_erlang_km2": capacity_density,
                "supported_users_km2": supported_users,
                "demand_users_km2": scenario.users_density_km2,
                "meets_demand": meets_demand,
                "sites_for_target_area": site_count_for_area(scenario.target_area_km2, area),
            }
        )

    if recommended_stage is None:
        recommended_stage = scenario.max_split_stage

    table = pd.DataFrame(rows)
    table["recommended"] = table["split_stage"].eq(recommended_stage)
    return table
