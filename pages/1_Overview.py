from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="AV Dashboard Overview",
    page_icon="🚘",
    layout="wide",
)

st.title("Overview")
st.caption(
    "A snapshot of autonomous vehicle access, safety evidence, and state policy conditions."
)

state_df = pd.read_csv("data/processed/state_access.csv")
reviewed_df = state_df[
    state_df["research_status"] != "Not reviewed"
].copy()

safety_df = pd.read_csv("data/processed/safety_data.csv")
market_df = pd.read_csv("data/processed/market_tracker.csv")
waymo_path = Path("data/processed/waymo_scenario_metrics.csv")

col1, col2, col3, col4 = st.columns(4)

col1.metric("States tracked", len(reviewed_df))
col2.metric(
    "Commercial AV states",
    int(reviewed_df["commercial_operation_allowed"].sum()),
)
col3.metric(
    "Statewide frameworks",
    int(reviewed_df["statewide_rules"].sum()),
)
col4.metric(
    "Average policy score",
    f"{reviewed_df['overall_score'].mean():.0f}/100",
)

st.subheader("State Access Map")

fig = px.choropleth(
    state_df,
    locations="state_code",
    locationmode="USA-states",
    color="overall_score",
    scope="usa",
    hover_name="state",
    hover_data={
        "commercial_operation_allowed": True,
        "statewide_rules": True,
        "local_rules_allowed": True,
        "insurance_minimum": True,
        "research_status": True,
    },
    range_color=(0, 100),
    color_continuous_scale=["#eeeeee", "#f4b16d", "#EE8A1D"],
    labels={"overall_score": "Policy score"},
)

fig.update_layout(
    height=520,
    margin=dict(l=0, r=0, t=0, b=0),
)

st.plotly_chart(fig, width="stretch")

st.subheader("Safety Outcomes Compared With Human-Driver Benchmarks")

st.caption(
    "Reported reductions compare Waymo rider-only performance with "
    "human-driver benchmarks in comparable operating areas and driving exposure."
)

safety_cols = st.columns(2)

for index, row in enumerate(safety_df.itertuples()):
    with safety_cols[index % 2]:
        with st.container(border=True):
            st.markdown(f"## {row.value:.0f}% fewer")
            st.markdown(f"**{row.metric}**")

            study_period = getattr(row, "study_period", "")
            comparison_group = getattr(row, "comparison_group", "")
            geography = getattr(row, "geography", "")

            if comparison_group:
                st.caption(f"Baseline: {comparison_group}")

            if study_period:
                st.caption(f"Study period: {study_period}")

            if geography:
                st.caption(f"Geography: {geography}")

st.divider()

access_left, access_right = st.columns([1, 1], gap="large")

with access_left:
    st.subheader("Consumer Access Snapshot")
    st.caption(
        "Markets recorded by operator. Counts reflect the current market tracker "
        "and do not measure total rides, vehicles, or market share."
    )

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
            "markets": "Markets currently tracked",
        },
        hover_data={
            "states": True,
            "markets": True,
        },
    )

    access_fig.update_traces(textposition="outside")

    access_fig.update_layout(
        height=390,
        coloraxis_showscale=False,
        margin=dict(l=0, r=20, t=10, b=0),
    )

    st.plotly_chart(access_fig, width="stretch")

with access_right:
    st.subheader("Market Access")

    active_markets = market_df["market"].nunique()
    public_markets = int(
        market_df["public_access"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("yes")
        .sum()
    )

    market_col1, market_col2 = st.columns(2)

    market_col1.metric(
        "Active markets tracked",
        active_markets,
    )

    market_col2.metric(
        "Publicly accessible records",
        public_markets,
    )

    st.info(
        "Operator counts indicate where services are recorded in the dataset. "
        "They should not be interpreted as ridership, fleet size, or market share."
    )

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

if waymo_path.exists():
    try:
        waymo_df = pd.read_csv(waymo_path)
        coverage_col3.metric(
            "Waymo scenarios processed",
            f"{len(waymo_df):,}",
        )
    except pd.errors.EmptyDataError:
        coverage_col3.metric(
            "Waymo scenarios processed",
            "0",
        )
else:
    coverage_col3.metric(
        "Waymo scenarios processed",
        "0",
    )

st.caption(
    "Market and scenario counts describe dashboard research coverage, "
    "not the total scale of autonomous-vehicle activity in the United States."
)

st.divider()

st.subheader("State Comparison")

st.dataframe(
    reviewed_df.sort_values("overall_score", ascending=False),
    width="stretch",
    hide_index=True,
)
