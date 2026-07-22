from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Autonomous Vehicle Access Overview",
    page_icon="🚘",
    layout="wide",
)


# ---------------------------------------------------------
# DATA PATHS
# ---------------------------------------------------------

STATE_PATH = Path("data/processed/state_access.csv")
MARKET_PATH = Path("data/processed/market_tracker.csv")
SAFETY_PATH = Path("data/processed/safety_data.csv")
WAYMO_PATH = Path("data/processed/waymo_scenario_metrics.csv")


# ---------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------

@st.cache_data
def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        return pd.DataFrame()


state_df = load_csv(STATE_PATH)
market_df = load_csv(MARKET_PATH)
safety_df = load_csv(SAFETY_PATH)

if state_df.empty:
    st.error("The state policy dataset could not be loaded.")
    st.stop()

if "research_status" in state_df.columns:
    reviewed_df = state_df[
        state_df["research_status"]
        .fillna("")
        .astype(str)
        .str.strip()
        .ne("Not reviewed")
    ].copy()
else:
    reviewed_df = state_df.copy()


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------

st.title("Autonomous vehicle access in the United States")

st.caption(
    "A national snapshot of consumer availability, state policy conditions, "
    "safety evidence, and the geographic reach of autonomous vehicle services."
)


# ---------------------------------------------------------
# HEADLINE METRICS
# ---------------------------------------------------------

active_markets = (
    market_df["market"].nunique()
    if not market_df.empty and "market" in market_df.columns
    else 0
)

public_market_records = 0

if not market_df.empty and "public_access" in market_df.columns:
    public_market_records = int(
        market_df["public_access"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("yes")
        .sum()
    )

commercial_states = (
    int(reviewed_df["commercial_operation_allowed"].fillna(0).sum())
    if "commercial_operation_allowed" in reviewed_df.columns
    else 0
)

average_score = (
    reviewed_df["overall_score"].mean()
    if "overall_score" in reviewed_df.columns
    else 0
)

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

metric_col1.metric(
    "Active markets tracked",
    active_markets,
    help=(
        "Unique markets currently included in the dashboard's market tracker. "
        "This is not a measure of total national AV activity."
    ),
)

metric_col2.metric(
    "Public-access records",
    public_market_records,
    help=(
        "Market records coded as publicly accessible. A single market may have "
        "more than one operator record."
    ),
)

metric_col3.metric(
    "Commercial AV states",
    commercial_states,
    help=(
        "States currently coded as allowing commercial autonomous-vehicle "
        "operation under the dashboard methodology."
    ),
)

metric_col4.metric(
    "Average policy score",
    f"{average_score:.0f}/100",
    help=(
        "Average of the dashboard's coded policy-access scores for reviewed states."
    ),
)

st.divider()


# ---------------------------------------------------------
# NATIONAL POLICY MAP
# ---------------------------------------------------------

st.subheader("National Policy Landscape")

st.caption(
    "Higher scores reflect broader commercial authorization, driverless testing "
    "permission, statewide rules, limits on conflicting local requirements, and "
    "fewer additional operating mandates."
)

map_hover = {
    "state_code": False,
    "overall_score": True,
}

optional_hover_columns = {
    "commercial_operation_allowed": "Commercial operation",
    "driverless_testing_allowed": "Driverless testing",
    "statewide_rules": "Statewide framework",
    "local_rules_allowed": "Separate local rules allowed",
    "human_operator_required": "Human operator required",
    "special_permit_required": "Special permit required",
    "research_status": "Research status",
}

for column in optional_hover_columns:
    if column in reviewed_df.columns:
        map_hover[column] = True

map_labels = {
    "overall_score": "Policy score",
    **optional_hover_columns,
}

policy_map = px.choropleth(
    reviewed_df,
    locations="state_code",
    locationmode="USA-states",
    color="overall_score",
    scope="usa",
    hover_name="state",
    hover_data=map_hover,
    range_color=(0, 100),
    color_continuous_scale=[
        "#F1F2F7",
        "#F5C58F",
        "#EE8A1D",
    ],
    labels=map_labels,
)

policy_map.update_layout(
    height=535,
    margin=dict(l=0, r=0, t=0, b=0),
    coloraxis_colorbar=dict(
        title="Policy score",
        thickness=16,
    ),
)

st.plotly_chart(
    policy_map,
    width="stretch",
    config={"displayModeBar": False},
)

st.caption(
    "Policy scores summarize coded conditions and are not legal opinions. "
    "Some state records remain preliminary pending additional source review."
)

st.divider()


# ---------------------------------------------------------
# CONSUMER ACCESS AND SAFETY
# ---------------------------------------------------------

access_col, safety_col = st.columns([1, 1], gap="large")


# ---------------------------------------------------------
# CONSUMER ACCESS
# ---------------------------------------------------------

with access_col:
    st.subheader("Consumer Access Snapshot")

    st.caption(
        "Markets currently recorded for each operator. Bar height represents "
        "the number of unique markets in this dataset, not ridership, fleet size, "
        "revenue, or market share."
    )

    if (
        not market_df.empty
        and "operator" in market_df.columns
        and "market" in market_df.columns
    ):
        aggregation = {
            "markets": ("market", "nunique"),
        }

        if "state" in market_df.columns:
            aggregation["states"] = ("state", "nunique")

        access_summary = (
            market_df.groupby("operator", as_index=False)
            .agg(**aggregation)
            .sort_values("markets", ascending=False)
        )

        if "states" not in access_summary.columns:
            access_summary["states"] = 0

        access_chart = px.bar(
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
                "states": "States represented",
            },
            hover_data={
                "states": True,
                "markets": True,
            },
        )

        access_chart.update_traces(
            textposition="outside",
            cliponaxis=False,
        )

        access_chart.update_layout(
            height=415,
            coloraxis_showscale=False,
            margin=dict(l=0, r=20, t=15, b=0),
            yaxis=dict(
                title="Markets currently tracked",
                rangemode="tozero",
            ),
        )

        st.plotly_chart(
            access_chart,
            width="stretch",
            config={"displayModeBar": False},
        )

        st.info(
            "Operator totals describe the dashboard's research coverage. "
            "They do not indicate how many vehicles or rides each operator provides."
        )
    else:
        st.warning("Consumer-access market data is not currently available.")


# ---------------------------------------------------------
# SAFETY SNAPSHOT
# ---------------------------------------------------------

with safety_col:
    st.subheader("Safety Snapshot")

    st.caption(
        "Reported crash reductions compared with human-driver benchmarks in "
        "comparable operating areas and driving exposure."
    )

    if (
        not safety_df.empty
        and "metric" in safety_df.columns
        and "value" in safety_df.columns
    ):
        safety_chart_df = safety_df.copy()

        safety_chart_df["value"] = pd.to_numeric(
            safety_chart_df["value"],
            errors="coerce",
        )

        safety_chart_df = safety_chart_df.dropna(
            subset=["value"]
        ).sort_values("value")

        safety_chart_df["display_value"] = (
            safety_chart_df["value"]
            .round(0)
            .astype(int)
            .astype(str)
            + "% fewer"
        )

        safety_chart = px.bar(
            safety_chart_df,
            x="value",
            y="metric",
            orientation="h",
            text="display_value",
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
            textposition="inside",
            insidetextanchor="end",
            textfont=dict(size=13),
            cliponaxis=False,
        )

        safety_chart.update_layout(
            height=415,
            coloraxis_showscale=False,
            margin=dict(l=0, r=15, t=15, b=0),
            xaxis=dict(
                title="Percent fewer crashes",
                range=[0, 100],
                ticksuffix="%",
            ),
            yaxis=dict(
                automargin=True,
            ),
        )

        st.plotly_chart(
            safety_chart,
            width="stretch",
            config={"displayModeBar": False},
        )

        study_periods = []

        if "study_period" in safety_df.columns:
            study_periods = [
                str(value).strip()
                for value in safety_df["study_period"].dropna().unique()
                if str(value).strip()
            ]

        geographies = []

        if "geography" in safety_df.columns:
            geographies = [
                str(value).strip()
                for value in safety_df["geography"].dropna().unique()
                if str(value).strip()
            ]

        comparison_groups = []

        if "comparison_group" in safety_df.columns:
            comparison_groups = [
                str(value).strip()
                for value in safety_df["comparison_group"].dropna().unique()
                if str(value).strip()
            ]

        with st.expander("View safety baseline and study context"):
            if comparison_groups:
                st.markdown("**Comparison baseline**")
                for value in comparison_groups:
                    st.write(value)

            if study_periods:
                st.markdown("**Study periods represented**")
                for value in study_periods:
                    st.write(value)

            if geographies:
                st.markdown("**Geographies represented**")
                for value in geographies:
                    st.write(value)

            if not comparison_groups and not study_periods and not geographies:
                st.write(
                    "Detailed safety-study context has not yet been added."
                )

        st.caption(
            "Safety figures may come from different study periods. "
            "See the Safety Evidence page for full source context."
        )
    else:
        st.warning("Safety evidence data is not currently available.")

st.divider()


# ---------------------------------------------------------
# RESEARCH COVERAGE
# ---------------------------------------------------------

st.subheader("Research Coverage")

st.caption(
    "These totals describe the information currently included in the dashboard, "
    "not the entire autonomous-vehicle industry."
)

coverage_col1, coverage_col2, coverage_col3 = st.columns(3)

coverage_col1.metric(
    "State policy records",
    len(reviewed_df),
)

coverage_col2.metric(
    "Market records",
    len(market_df),
)

scenario_count = 0

if WAYMO_PATH.exists():
    try:
        waymo_df = pd.read_csv(WAYMO_PATH)
        scenario_count = len(waymo_df)
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        scenario_count = 0

coverage_col3.metric(
    "Waymo scenarios processed",
    f"{scenario_count:,}",
)

st.info(
    "Use the sidebar to explore consumer access, safety evidence, state policy "
    "conditions, scenario data, methodology, and source transparency."
)

st.divider()


# ---------------------------------------------------------
# STATE COMPARISON
# ---------------------------------------------------------

st.subheader("State Comparison")

st.caption(
    "Review the current policy coding for all states included in the tracker."
)

preferred_columns = [
    "state",
    "state_code",
    "overall_score",
    "commercial_operation_allowed",
    "driverless_testing_allowed",
    "statewide_rules",
    "local_rules_allowed",
    "human_operator_required",
    "special_permit_required",
    "insurance_minimum",
    "research_status",
    "last_verified",
    "source_url",
]

display_columns = [
    column
    for column in preferred_columns
    if column in reviewed_df.columns
]

comparison_df = reviewed_df[
    display_columns
].sort_values(
    "overall_score",
    ascending=False,
)

column_config = {}

if "state" in comparison_df.columns:
    column_config["state"] = "State"

if "state_code" in comparison_df.columns:
    column_config["state_code"] = "Code"

if "overall_score" in comparison_df.columns:
    column_config["overall_score"] = st.column_config.ProgressColumn(
        "Policy score",
        min_value=0,
        max_value=100,
        format="%d",
    )

if "commercial_operation_allowed" in comparison_df.columns:
    column_config["commercial_operation_allowed"] = st.column_config.CheckboxColumn(
        "Commercial operation"
    )

if "driverless_testing_allowed" in comparison_df.columns:
    column_config["driverless_testing_allowed"] = st.column_config.CheckboxColumn(
        "Driverless testing"
    )

if "statewide_rules" in comparison_df.columns:
    column_config["statewide_rules"] = st.column_config.CheckboxColumn(
        "Statewide framework"
    )

if "local_rules_allowed" in comparison_df.columns:
    column_config["local_rules_allowed"] = st.column_config.CheckboxColumn(
        "Separate local rules"
    )

if "human_operator_required" in comparison_df.columns:
    column_config["human_operator_required"] = st.column_config.CheckboxColumn(
        "Human operator required"
    )

if "special_permit_required" in comparison_df.columns:
    column_config["special_permit_required"] = st.column_config.CheckboxColumn(
        "Special permit required"
    )

if "insurance_minimum" in comparison_df.columns:
    column_config["insurance_minimum"] = st.column_config.NumberColumn(
        "Insurance minimum",
        format="$%d",
    )

if "source_url" in comparison_df.columns:
    column_config["source_url"] = st.column_config.LinkColumn(
        "Official source",
        display_text="Open source",
    )

st.dataframe(
    comparison_df,
    column_config=column_config,
    width="stretch",
    hide_index=True,
)
