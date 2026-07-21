from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="AV Access and Safety Tracker",
    page_icon="🚗",
    layout="wide",
)

POLICY_PATH = Path("data/processed/state_access.csv")
MARKET_PATH = Path("data/processed/market_tracker.csv")
SAFETY_PATH = Path("data/processed/safety_data.csv")
WAYMO_PATH = Path("data/processed/waymo_scenario_metrics.csv")

policy_df = pd.read_csv(POLICY_PATH)
market_df = pd.read_csv(MARKET_PATH)
safety_df = pd.read_csv(SAFETY_PATH)

reviewed_df = policy_df[
    policy_df["research_status"] != "Not reviewed"
].copy()

st.title("Autonomous Vehicle Access and Safety Tracker")
st.caption(
    "A public policy dashboard tracking consumer access, safety evidence, "
    "regulatory conditions, and data transparency."
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Active markets",
    market_df["market"].nunique(),
)

col2.metric(
    "Publicly accessible markets",
    int((market_df["public_access"] == "Yes").sum()),
)

col3.metric(
    "States reviewed",
    len(reviewed_df),
)

col4.metric(
    "Average policy score",
    f"{reviewed_df['overall_score'].mean():.0f}/100",
)

st.subheader("National Policy Landscape")

fig = px.choropleth(
    reviewed_df,
    locations="state_code",
    locationmode="USA-states",
    color="overall_score",
    scope="usa",
    hover_name="state",
    hover_data={
        "state_code": False,
        "commercial_operation_allowed": True,
        "statewide_rules": True,
        "local_rules_allowed": True,
        "human_operator_required": True,
        "overall_score": True,
    },
    range_color=(0, 100),
    color_continuous_scale=[
        "#F1F2F7",
        "#F5C58F",
        "#EE8A1D",
    ],
    labels={
        "overall_score": "Policy score",
        "commercial_operation_allowed": "Commercial operation",
        "statewide_rules": "Statewide framework",
        "local_rules_allowed": "Local rules allowed",
        "human_operator_required": "Human operator required",
    },
)

fig.update_layout(
    height=510,
    margin=dict(l=0, r=0, t=0, b=0),
)

st.plotly_chart(fig, width="stretch")

left, right = st.columns([1, 1])

with left:
    st.subheader("Consumer Access Snapshot")

    access_summary = (
        market_df.groupby("operator", as_index=False)
        .agg(
            markets=("market", "nunique"),
            states=("state", "nunique"),
        )
        .sort_values("markets", ascending=False)
    )

    access_fig = px.bar(
        access_summary,
        x="operator",
        y="markets",
        text="markets",
        color="markets",
        color_continuous_scale=[
            "#F1F2F7",
            "#F5C58F",
            "#EE8A1D",
        ],
        labels={
            "operator": "",
            "markets": "Markets",
        },
    )

    access_fig.update_layout(
        height=390,
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=10, b=0),
    )

    st.plotly_chart(access_fig, width="stretch")

with right:
    st.subheader("Safety Snapshot")

    safety_chart = px.bar(
        safety_df.sort_values("value"),
        x="value",
        y="metric",
        orientation="h",
        text="value",
        color="value",
        color_continuous_scale=[
            "#F1F2F7",
            "#F5C58F",
            "#EE8A1D",
        ],
        labels={
            "value": "Percent fewer crashes",
            "metric": "",
        },
    )

    safety_chart.update_traces(
        texttemplate="%{text}% fewer",
        textposition="outside",
    )

    safety_chart.update_layout(
        height=390,
        coloraxis_showscale=False,
        margin=dict(l=0, r=70, t=10, b=0),
        xaxis_range=[0, 105],
    )

    st.plotly_chart(safety_chart, width="stretch")

st.subheader("Research Coverage")

coverage_col1, coverage_col2, coverage_col3 = st.columns(3)

coverage_col1.metric(
    "Policy records",
    len(reviewed_df),
)

coverage_col2.metric(
    "Market records",
    len(market_df),
)

if WAYMO_PATH.exists():
    try:
        waymo_df = pd.read_csv(WAYMO_PATH)
        coverage_col3.metric(
            "Waymo scenarios processed",
            f"{len(waymo_df):,}",
        )
    except pd.errors.EmptyDataError:
        coverage_col3.metric("Waymo scenarios processed", "0")
else:
    coverage_col3.metric("Waymo scenarios processed", "0")

st.info(
    "Use the sidebar to explore consumer access, safety evidence, "
    "state policy conditions, scenario data, methodology, and source transparency."
)
