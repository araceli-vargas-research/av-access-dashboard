import pandas as pd

def simple_policy_score(df: pd.DataFrame, score_columns: list[str]) -> pd.Series:
    return df[score_columns].fillna(0).mean(axis=1) * 100
