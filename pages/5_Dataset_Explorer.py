from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Waymo Dataset Explorer",
    page_icon="🚗",
    layout="wide",
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "waymo_scenario_metrics.parquet"
)


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        return pd.DataFrame()

    return pd.read_parquet(DATA_PATH)


df = load_data()

st.title("Waymo Open Motion Dataset Explorer")

st.caption(
    "This page describes the composition and complexity of the sampled "
    "research scenarios. It does not measure Waymo's commercial driving "
    "performance or safety."
)

if df.empty:
    st.warning(
        "No processed dataset was found. Run "
        "`python scripts/process_motion_scenarios.py --max-scenarios 500`."
    )
    st.stop()

scenario_count = len(df)
pedestrian_scenarios = int((df["pedestrian_count"] > 0).sum())
cyclist_scenarios = int((df["cyclist_count"] > 0).sum())
signal_scenarios = int((df["traffic_signal_count"] > 0).sum())

col1, col2, col3, col4 = st.columns(4)

col1.metric("Scenarios sampled", f"{scenario_count:,}")
col2.metric(
    "With pedestrians",
    f"{pedestrian_scenarios:,}",
    f"{pedestrian_scenarios / scenario_count:.1%}",
)
col3.metric(
    "With cyclists",
    f"{cyclist_scenarios:,}",
    f"{cyclist_scenarios / scenario_count:.1%}",
)
col4.metric(
    "With traffic signals",
    f"{signal_scenarios:,}",
    f"{signal_scenarios / scenario_count:.1%}",
)

st.divider()

st.subheader("Filter scenarios")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    require_pedestrians = st.checkbox("Pedestrians present")

with filter_col2:
    require_cyclists = st.checkbox("Cyclists present")

with filter_col3:
    require_signals = st.checkbox("Traffic signals present")

filtered = df.copy()

if require_pedestrians:
    filtered = filtered[filtered["pedestrian_count"] > 0]

if require_cyclists:
    filtered = filtered[filtered["cyclist_count"] > 0]

if require_signals:
    filtered = filtered[filtered["traffic_signal_count"] > 0]

st.write(f"Showing **{len(filtered):,}** of **{len(df):,}** scenarios.")

if filtered.empty:
    st.info("No scenarios match the selected filters.")
    st.stop()

st.subheader("Road-user mix")

agent_totals = pd.DataFrame(
    {
        "Road user": ["Vehicles", "Pedestrians", "Cyclists", "Other"],
        "Count": [
            filtered["vehicle_count"].sum(),
            filtered["pedestrian_count"].sum(),
            filtered["cyclist_count"].sum(),
            filtered["other_agent_count"].sum(),
        ],
    }
)

fig_agents = px.bar(
    agent_totals,
    x="Road user",
    y="Count",
    title="Total labelled agents in the selected scenarios",
)

st.plotly_chart(fig_agents, width="stretch")

left, right = st.columns(2)

with left:
    fig_complexity = px.histogram(
        filtered,
        x="complexity_index_v1",
        nbins=25,
        title="Scenario complexity distribution",
        labels={
            "complexity_index_v1": "Constructed complexity index"
        },
    )

    st.plotly_chart(fig_complexity, width="stretch")

with right:
    fig_tracks = px.histogram(
        filtered,
        x="total_track_count",
        nbins=25,
        title="Agents tracked per scenario",
        labels={"total_track_count": "Track count"},
    )

    st.plotly_chart(fig_tracks, width="stretch")

left, right = st.columns(2)

with left:
    fig_speed = px.scatter(
        filtered,
        x="total_track_count",
        y="mean_agent_speed_mps",
        size="moving_agent_count",
        hover_data=[
            "scenario_id",
            "vehicle_count",
            "pedestrian_count",
            "cyclist_count",
        ],
        title="Scenario size and average agent speed",
        labels={
            "total_track_count": "Tracked agents",
            "mean_agent_speed_mps": "Mean speed (m/s)",
            "moving_agent_count": "Moving agents",
        },
    )

    st.plotly_chart(fig_speed, width="stretch")

with right:
    fig_map = px.scatter(
        filtered,
        x="lane_count",
        y="crosswalk_count",
        size="traffic_signal_count",
        hover_data=[
            "scenario_id",
            "road_edge_count",
            "stop_sign_count",
            "driveway_count",
        ],
        title="Map complexity",
        labels={
            "lane_count": "Lane features",
            "crosswalk_count": "Crosswalks",
            "traffic_signal_count": "Traffic signals",
        },
    )

    st.plotly_chart(fig_map, width="stretch")

st.subheader("Most complex sampled scenarios")

display_columns = [
    "scenario_id",
    "complexity_index_v1",
    "total_track_count",
    "moving_agent_count",
    "vehicle_count",
    "pedestrian_count",
    "cyclist_count",
    "lane_count",
    "crosswalk_count",
    "traffic_signal_count",
]

top_scenarios = (
    filtered[display_columns]
    .sort_values("complexity_index_v1", ascending=False)
    .head(20)
)

st.dataframe(
    top_scenarios,
    width="stretch",
    hide_index=True,
)

csv_data = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download filtered scenario metrics",
    data=csv_data,
    file_name="waymo_scenario_metrics_filtered.csv",
    mime="text/csv",
)

with st.expander("How to interpret this page"):
    st.write(
        """
        The charts summarize a sample of the Waymo Open Motion Dataset.
        The complexity index is a constructed research indicator based on
        agent counts, moving agents, lanes, crosswalks, and traffic signals.

        The underlying dataset contains an unidentified mixture of manually
        and autonomously driven segments. These figures therefore cannot be
        interpreted as measures of commercial Waymo safety, intervention
        rates, or driving success.
        """
    )