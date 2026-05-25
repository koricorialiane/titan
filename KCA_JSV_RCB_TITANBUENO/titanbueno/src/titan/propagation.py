import math


def thermal_noise_dbm(bandwidth_hz: float, noise_figure_db: float) -> float:
    if bandwidth_hz <= 0:
        raise ValueError("bandwidth_hz must be positive.")
    return -174.0 + 10.0 * math.log10(bandwidth_hz) + noise_figure_db


def receiver_sensitivity_dbm(
    thermal_noise_value_dbm: float,
    snr_required_db: float,
    implementation_losses_db: float,
) -> float:
    return thermal_noise_value_dbm + snr_required_db + implementation_losses_db


def maximum_allowable_path_loss_db(
    tx_power_dbm: float,
    tx_gain_dbi: float,
    rx_gain_dbi: float,
    additional_losses_db: float,
    receiver_sensitivity_value_dbm: float,
) -> float:
    return tx_power_dbm + tx_gain_dbi + rx_gain_dbi - additional_losses_db - receiver_sensitivity_value_dbm


def radius_from_log_path_loss_km(max_path_loss_db: float, intercept_db: float, slope_db: float) -> float:
    if slope_db <= 0:
        raise ValueError("slope_db must be positive.")
    return 10.0 ** ((max_path_loss_db - intercept_db) / slope_db)


def traffic_per_user_erlang(calls_per_hour_per_user: float, holding_time_min: float) -> float:
    if calls_per_hour_per_user < 0 or holding_time_min < 0:
        raise ValueError("Traffic parameters must be non-negative.")
    return calls_per_hour_per_user * (holding_time_min / 60.0)


def traffic_density_erlang_km2(users_density_km2: float, traffic_per_user_value_erlang: float) -> float:
    if users_density_km2 < 0:
        raise ValueError("users_density_km2 must be non-negative.")
    return users_density_km2 * traffic_per_user_value_erlang


def erlang_b_blocking(offered_traffic_erlang: float, channels: int) -> float:
    if channels <= 0:
        raise ValueError("channels must be positive.")
    if offered_traffic_erlang < 0:
        raise ValueError("offered_traffic_erlang must be non-negative.")

    blocking = 1.0
    for channel in range(1, channels + 1):
        blocking = (offered_traffic_erlang * blocking) / (channel + offered_traffic_erlang * blocking)
    return blocking


def inverse_erlang_b(channels: int, blocking_probability: float) -> float:
    if channels <= 0:
        raise ValueError("channels must be positive.")
    if not 0.0 < blocking_probability < 1.0:
        raise ValueError("blocking_probability must be between 0 and 1.")

    low = 0.0
    high = float(max(20, channels * 20))
    while erlang_b_blocking(high, channels) < blocking_probability:
        high *= 2.0

    for _ in range(80):
        mid = (low + high) / 2.0
        if erlang_b_blocking(mid, channels) > blocking_probability:
            high = mid
        else:
            low = mid
    return (low + high) / 2.0


def hexagon_area_km2(radius_km: float) -> float:
    if radius_km < 0:
        raise ValueError("radius_km must be non-negative.")
    return 1.5 * math.sqrt(3.0) * radius_km**2


def hexagon_radius_from_area_km2(area_km2: float) -> float:
    if area_km2 < 0:
        raise ValueError("area_km2 must be non-negative.")
    if area_km2 == 0:
        return 0.0
    return math.sqrt((2.0 * area_km2) / (3.0 * math.sqrt(3.0)))


def reuse_ratio(reuse_factor_n: int) -> float:
    if reuse_factor_n <= 0:
        raise ValueError("reuse_factor_n must be positive.")
    return math.sqrt(3.0 * reuse_factor_n)


def reuse_distance_km(radius_km: float, reuse_factor_n: int) -> float:
    if radius_km < 0:
        raise ValueError("radius_km must be non-negative.")
    return radius_km * reuse_ratio(reuse_factor_n)


def estimated_sir_db(reuse_factor_n: int, path_loss_exponent: float, interferers: int) -> float:
    if path_loss_exponent <= 0:
        raise ValueError("path_loss_exponent must be positive.")
    if interferers <= 0:
        raise ValueError("interferers must be positive.")
    sir_linear = (reuse_ratio(reuse_factor_n) ** path_loss_exponent) / interferers
    return 10.0 * math.log10(sir_linear)


def site_count_for_area(target_area_km2: float, cell_area_km2: float) -> int:
    if cell_area_km2 <= 0:
        return 0
    return math.ceil(target_area_km2 / cell_area_km2)
