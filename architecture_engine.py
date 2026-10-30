
import pandas as pd


def load_architectures():
    df = pd.read_csv("data/architecture_data.csv")

    required_columns = [
        "architecture",
        "scalability",
        "performance",
        "cost",
        "maintainability",
        "reliability",
        "complexity"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing dataset column: {column}")

    return df


def calculate_scores(
    df,
    scalability_weight=0.25,
    performance_weight=0.20,
    cost_weight=0.15,
    maintainability_weight=0.15,
    reliability_weight=0.15,
    complexity_weight=0.10
):

    result = df.copy()

    weights = [
        scalability_weight,
        performance_weight,
        cost_weight,
        maintainability_weight,
        reliability_weight,
        complexity_weight
    ]

    if abs(sum(weights) - 1.0) > 0.001:
        raise ValueError("Architecture weights must add up to 1.")

    # Lower complexity should produce a higher score
    result["simplicity"] = 100 - result["complexity"]

    # Calculate overall architecture suitability
    result["overall_score"] = (
        result["scalability"] * scalability_weight +
        result["performance"] * performance_weight +
        result["cost"] * cost_weight +
        result["maintainability"] * maintainability_weight +
        result["reliability"] * reliability_weight +
        result["simplicity"] * complexity_weight
    )

    return result.sort_values(
        "overall_score",
        ascending=False
    ).reset_index(drop=True)
