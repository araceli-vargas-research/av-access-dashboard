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

st.subheader("Safety Snapshot")

safety_cols = st.columns(len(safety_df))

for col, row in zip(safety_cols, safety_df.itertuples()):
    col.metric(row.metric, f"{row.value}% fewer")

st.subheader("State Comparison")

st.dataframe(
    reviewed_df.sort_values("overall_score", ascending=False),
    width="stretch",
    hide_index=True,
)
