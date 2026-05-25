import pandas as pd

from .cellular_planning import festival_capacity_table, festival_coverage_table, festival_splitting_table
from .config import FestivalScenario, NetworkConfig


def analyze_festival(
    scenario: FestivalScenario = FestivalScenario(),
    config: NetworkConfig = NetworkConfig(),
) -> dict[str, pd.DataFrame]:
    coverage = festival_coverage_table(scenario, config)
    capacity = festival_capacity_table(coverage, scenario, config)
    splitting = festival_splitting_table(coverage, scenario, config)
    return {"coverage": coverage, "capacity": capacity, "splitting": splitting}
