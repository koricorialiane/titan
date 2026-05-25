import pandas as pd

from .config import DistrictScenario, FestivalScenario, NetworkConfig


def system_parameter_table(config: NetworkConfig = NetworkConfig()) -> pd.DataFrame:
    rows = [
        ("Operating frequency", f"{config.frequency_mhz:g} MHz", "Shared by both scenarios"),
        ("System bandwidth", f"{config.bandwidth_mhz:g} MHz", "Used for thermal noise"),
        ("Base station transmit power", f"{config.tx_power_dbm:g} dBm", "Equivalent to 20 W"),
        ("TX antenna gain", f"{config.tx_gain_dbi:g} dBi", "Base station sector antenna"),
        ("RX antenna gain", f"{config.rx_gain_dbi:g} dBi", "Mobile terminal"),
        ("Additional losses", f"{config.additional_losses_db:g} dB", "Cables, connectors and design margin"),
        ("Receiver noise figure", f"{config.noise_figure_db:g} dB", "NF for sensitivity estimate"),
        ("Implementation losses", f"{config.implementation_losses_db:g} dB", "L_impl term in sensitivity"),
        ("Blocking probability", f"{config.blocking_probability:.2%}", "GoS objective for Erlang B"),
        ("Total physical channels", f"{config.total_channels:d}", "Simplified PRB-like capacity pool"),
    ]
    return pd.DataFrame(rows, columns=["parameter", "value", "engineering_role"])


def modulation_context_table() -> pd.DataFrame:
    rows = [
        ("QPSK", "High robustness", "Cell edge and difficult propagation", "Lower spectral efficiency, lower SNR need"),
        ("16QAM", "Balanced", "Typical urban load", "Intermediate throughput and robustness"),
        ("64QAM", "High throughput", "Good SINR zones", "Higher spectral efficiency at higher SNR"),
        ("256QAM", "Peak efficiency", "Excellent channel quality", "Representative of modern LTE/5G adaptation logic"),
    ]
    return pd.DataFrame(rows, columns=["modulation", "design_tradeoff", "typical_use", "interpretation"])


def scenario_goal_table(
    district: DistrictScenario = DistrictScenario(),
    festival: FestivalScenario = FestivalScenario(),
) -> pd.DataFrame:
    rows = [
        (
            "A_distrito_financiero",
            "Dense urban core",
            f"{district.users_density_km2:g} active users/km2",
            "Coverage plus strong capacity pressure",
            "Three sectors per site and N = 3, 4, 7 comparison",
        ),
        (
            "B_festival_global",
            "Open suburban esplanade",
            f"{festival.users_density_km2:g} active users/km2",
            "Extreme temporal congestion",
            "Omnidirectional cells plus cell splitting evaluation",
        ),
    ]
    return pd.DataFrame(rows, columns=["scenario", "environment", "density", "design_priority", "required_analysis"])
