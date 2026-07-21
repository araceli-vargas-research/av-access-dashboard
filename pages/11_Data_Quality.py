from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AV Data Quality",
    page_icon="✅",
    layout="wide",
)

st.title("Data Quality")
st.caption(
    "Review missing sources, incomplete records, and outdated verification dates."
)

POLICY_PATH = Path("data/processed/state_access.csv")
MARKET_PATH = Path("data/processed/market_tracker.csv")
SAFETY_PATH = Path("data/processed/safety_data.csv")
MUNICIPAL_PATH = Path("data/processed/municipal_barriers.csv")
FEDERAL_PATH = Path("data/processed/federal_challenges.csv")


def load_csv(path):
    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def missing_text(series):
    return series.fillna("").astype(str).str.strip().eq("")


policy_df = load_csv(POLICY_PATH)
market_df = load_csv(MARKET_PATH)
safety_df = load_csv(SAFETY_PATH)
municipal_df = load_csv(MUNICIPAL_PATH)
federal_df = load_csv(FEDERAL_PATH)

checks = []

if not policy_df.empty:
    checks.append(
        {
            "Dataset": "State policy",
            "Records": len(policy_df),
            "Missing sources": int(missing_text(policy_df["source_url"]).sum()),
            "Missing summaries": int(
                missing_text(policy_df["policy_summary"]).sum()
            ),
            "Missing dates": int(
                missing_text(policy_df["last_verified"]).sum()
            ),
        }
    )

if not market_df.empty:
    checks.append(
        {
            "Dataset": "Market tracker",
            "Records": len(market_df),
            "Missing sources": int(missing_text(market_df["source_url"]).sum()),
            "Missing summaries": 0,
            "Missing dates": int(
                missing_text(market_df["last_verified"]).sum()
            ),
        }
    )

if not safety_df.empty:
    safety_source_column = (
        "source_url"
        if "source_url" in safety_df.columns
        else "source"
    )

    checks.append(
        {
            "Dataset": "Safety evidence",
            "Records": len(safety_df),
            "Missing sources": int(
                missing_text(safety_df[safety_source_column]).sum()
            ),
            "Missing summaries": 0,
            "Missing dates": (
                int(missing_text(safety_df["last_verified"]).sum())
                if "last_verified" in safety_df.columns
                else len(safety_df)
            ),
        }
    )

if not municipal_df.empty:
    checks.append(
        {
            "Dataset": "Municipal barriers",
            "Records": len(municipal_df),
            "Missing sources": int(
                missing_text(municipal_df["source_url"]).sum()
            ),
            "Missing summaries": int(
                missing_text(municipal_df["summary"]).sum()
            ),
            "Missing dates": int(
                missing_text(municipal_df["last_verified"]).sum()
            ),
        }
    )

if not federal_df.empty:
    checks.append(
        {
            "Dataset": "Federal policy",
            "Records": len(federal_df),
            "Missing sources": int(
                missing_text(federal_df["source_url"]).sum()
            ),
            "Missing summaries": 0,
            "Missing dates": int(
                missing_text(federal_df["last_verified"]).sum()
            ),
        }
    )

quality_df = pd.DataFrame(checks)

if quality_df.empty:
    st.warning("No dashboard datasets were found.")
    st.stop()

quality_df["Total issues"] = (
    quality_df["Missing sources"]
    + quality_df["Missing summaries"]
    + quality_df["Missing dates"]
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Datasets checked", len(quality_df))
col2.metric("Records checked", int(quality_df["Records"].sum()))
col3.metric(
    "Missing sources",
    int(quality_df["Missing sources"].sum()),
)
col4.metric(
    "Total issues",
    int(quality_df["Total issues"].sum()),
)

st.subheader("Dataset Completeness")

st.dataframe(
    quality_df,
    column_config={
        "Dataset": "Dataset",
        "Records": "Records",
        "Missing sources": "Missing sources",
        "Missing summaries": "Missing summaries",
        "Missing dates": "Missing dates",
        "Total issues": st.column_config.ProgressColumn(
            "Total issues",
            min_value=0,
            max_value=max(int(quality_df["Total issues"].max()), 1),
            format="%d",
        ),
    },
    width="stretch",
    hide_index=True,
)

st.subheader("State Policy Records Needing Attention")

if not policy_df.empty:
    policy_issues = policy_df[
        missing_text(policy_df["source_url"])
        | missing_text(policy_df["policy_summary"])
        | missing_text(policy_df["last_verified"])
        | policy_df["overall_score"].isna()
        | ~policy_df["overall_score"].between(0, 100)
    ].copy()

    if policy_issues.empty:
        st.success("All state policy records passed the basic checks.")
    else:
        st.dataframe(
            policy_issues[
                [
                    "state",
                    "research_status",
                    "overall_score",
                    "policy_summary",
                    "source_url",
                    "last_verified",
                ]
            ],
            column_config={
                "state": "State",
                "research_status": "Research status",
                "overall_score": "Policy score",
                "policy_summary": st.column_config.TextColumn(
                    "Policy summary",
                    width="large",
                ),
                "source_url": st.column_config.LinkColumn(
                    "Source",
                    display_text="Open source",
                ),
                "last_verified": "Last verified",
            },
            width="stretch",
            hide_index=True,
        )

st.subheader("Publication Checklist")

st.markdown(
    """
    Before publishing, confirm that:

    - Every legal claim links to an official source
    - Proposed bills are not labeled as enacted laws
    - Testing authorization is separate from commercial deployment
    - Safety figures include dates and comparison groups
    - Every policy score falls between 0 and 100
    - Verification dates are current
    """
)

st.subheader("Publication Audit Results")

audit_path = Path("data/processed/publication_audit.csv")

if audit_path.exists():
    try:
        audit_df = pd.read_csv(audit_path)

        if audit_df.empty:
            st.success("The automated publication audit found no issues.")
        else:
            high = int((audit_df["severity"] == "High").sum())
            medium = int((audit_df["severity"] == "Medium").sum())

            audit_col1, audit_col2, audit_col3 = st.columns(3)
            audit_col1.metric("Audit issues", len(audit_df))
            audit_col2.metric("High priority", high)
            audit_col3.metric("Medium priority", medium)

            st.dataframe(
                audit_df,
                column_config={
                    "dataset": "Dataset",
                    "record": "Record",
                    "issue": st.column_config.TextColumn(
                        "Issue",
                        width="large",
                    ),
                    "severity": "Priority",
                },
                width="stretch",
                hide_index=True,
            )
    except pd.errors.EmptyDataError:
        st.success("The automated publication audit found no issues.")
else:
    st.warning(
        "Run `python3 scripts/publication_audit.py` to generate the audit."
    )
