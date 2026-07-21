from pathlib import Path

import pandas as pd

INPUT_PATH = Path("data/processed/state_access.csv")


def calculate_score(row):
    commercial_score = 30 if row["commercial_operation_allowed"] == 1 else 0
    testing_score = 15 if row["driverless_testing_allowed"] == 1 else 0
    statewide_score = 20 if row["statewide_rules"] == 1 else 0
    local_score = 15 if row["local_rules_allowed"] == 0 else 0
    operator_score = 10 if row["human_operator_required"] == 0 else 0
    permit_score = 5 if row["special_permit_required"] == 0 else 0

    insurance = float(row.get("insurance_minimum", 0) or 0)

    if insurance == 0:
        insurance_score = 5
    elif insurance <= 1_000_000:
        insurance_score = 3
    else:
        insurance_score = 0

    total = (
        commercial_score
        + testing_score
        + statewide_score
        + local_score
        + operator_score
        + permit_score
        + insurance_score
    )

    return pd.Series(
        {
            "commercial_score": commercial_score,
            "testing_score": testing_score,
            "statewide_score": statewide_score,
            "local_preemption_score": local_score,
            "human_operator_score": operator_score,
            "permit_score": permit_score,
            "insurance_score": insurance_score,
            "overall_score": total,
        }
    )


def main():
    df = pd.read_csv(INPUT_PATH)

    score_columns = df.apply(calculate_score, axis=1)

    for column in score_columns.columns:
        df[column] = score_columns[column]

    df.to_csv(INPUT_PATH, index=False)

    print(f"Recalculated policy scores for {len(df)} states.")
    print(f"Average score: {df['overall_score'].mean():.1f}/100")


if __name__ == "__main__":
    main()
