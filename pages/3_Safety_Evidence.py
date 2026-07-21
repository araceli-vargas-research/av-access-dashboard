import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="AV Safety Evidence",
    page_icon="🛡️",
    layout="wide",
)

st.title("Safety Evidence")
st.caption(
    "Compare reported autonomous vehicle safety outcomes with human-driver benchmarks."
)

df = pd.read_csv("data/processed/safety_data.csv")

col1, col2, col3, col4 = st.columns(4)

for col, row in zip([col1, col2, col3, col4], df.itertuples()):
    col.metric(row.metric, f"{row.value}% fewer")

st.subheader("Reported Crash Reductions")

fig = px.bar(
    df,
    x="value",
    y="metric",
    orientation="h",
    text="value",
    color="value",
    color_continuous_scale=["#f7e6d5", "#f28c28"],
    labels={
        "value": "Percent fewer crashes",
        "metric": "",
    },
)

fig.update_traces(
    texttemplate="%{text}% fewer",
    textposition="outside",
)

fig.update_layout(
    height=480,
    coloraxis_showscale=False,
    margin=dict(l=0, r=80, t=10, b=0),
    xaxis_range=[0, 105],
)

st.plotly_chart(fig, width="stretch")

st.info(
    "These are temporary example figures. Replace them with verified values, "
    "dates, comparison groups, and source links before publishing."
)

st.dataframe(
    df,
    width="stretch",
    hide_index=True,
)
