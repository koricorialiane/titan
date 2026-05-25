import pandas as pd

from .config import DistrictScenario, FestivalScenario, NetworkConfig


def assumptions_table(
    config: NetworkConfig = NetworkConfig(),
    district: DistrictScenario = DistrictScenario(),
    festival: FestivalScenario = FestivalScenario(),
) -> pd.DataFrame:
    rows = [
        (
            "Reference target area",
            f"{district.target_area_km2:g} km2 for both scenarios",
            "The statement asks for the number of cells over a proposed target area but does not provide a fixed value. A common normalized 1 km2 area is assumed to compare cell density without bias.",
        ),
        (
            "Channel partition in scenario A",
            "floor(100 / N) channels per site, then uniform split across 3 sectors",
            "The statement requests N = 3, 4, 7 and three sectors per site, but it does not define a more detailed PRB scheduler. The uniform split is the simplest reproducible assumption.",
        ),
        (
            "Interference approximation",
            "2 first-tier interferers for sectorized cells and 6 for omnidirectional reference",
            "This is the standard first-tier hexagonal approximation used to compare reuse strategies in teaching-oriented planning exercises.",
        ),
        (
            "Hexagonal geometry",
            "Regular hexagonal cell area model",
            "Needed to convert traffic-limited area into an equivalent cell radius and then into the number of required sites.",
        ),
        (
            "Modern radio context",
            "OFDMA/LTE/5G design logic with adaptive MCS",
            "The statement explicitly asks for a modern mobile-network framing even though the numerical exercise is simplified to link budget and Erlang B.",
        ),
    ]
    return pd.DataFrame(rows, columns=["assumption", "applied_value", "justification"])


def validation_checklist() -> pd.DataFrame:
    rows = [
        ("Structure and presentation", "Static web includes summary, scenarios, assumptions and code section", "Supports rubric presentation block"),
        ("State of the art", "Project exports a modulation context table and OFDMA framing", "Connects calculations with modern mobile systems"),
        ("Methodology", "Main pipeline reproduces noise, sensitivity, coverage, capacity, reuse and splitting", "Step-by-step reproducibility is explicit"),
        ("Mathematical precision", "Outputs keep units, formulas and CSV traces", "Facilitates annex verification"),
        ("Discussion", "Root web explains limiting factors and design trade-offs", "Moves beyond raw numbers"),
        ("Conclusions and future view", "Report builder includes recommendations and 2030 extension note", "Aligns with final rubric block"),
    ]
    return pd.DataFrame(rows, columns=["rubric_area", "project_evidence", "why_it_matters"])
