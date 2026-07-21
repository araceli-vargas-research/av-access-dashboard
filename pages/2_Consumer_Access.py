import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="AV Consumer Access",
    page_icon="📍",
    layout="wide",
)

st.title("Consumer Access")
st.caption(
    "Track where autonomous passenger and freight services are operating across the United States."
)

df = pd.read_csv("data/processed/market_tracker.csv")

with st.sidebar:
    st.header("Market Filters")

    operators = st.multiselect(
        "Operator",
        sorted(df["operator"].unique()),
        default=sorted(df["operator"].unique()),
    )

    uses = st.multiselect(
        "Vehicle use",
        sorted(df["vehicle_use"].unique()),
        default=sorted(df["vehicle_use"].unique()),
    )

    access = st.selectbox(
        "Public access",
        ["All", "Yes", "Limited", "No"],
    )

filtered_df = df[
    df["operator"].isin(operators)
    & df["vehicle_use"].isin(uses)
].copy()

if access != "All":
    filtered_df = filtered_df[
        filtered_df["public_access"] == access
    ]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Markets shown", len(filtered_df))
col2.metric("Operators", filtered_df["operator"].nunique())
col3.metric("States represented", filtered_df["state"].nunique())
col4.metric(
    "Publicly accessible",
    int((filtered_df["public_access"] == "Yes").sum()),
)

st.subheader("Active AV Markets")

map_df = (
    filtered_df.groupby(
        ["state", "state_code"],
        as_index=False,
    )
    .agg(
        active_markets=("market", "nunique"),
        operators=("operator", lambda x: ", ".join(sorted(set(x)))),
    )
)

fig = px.choropleth(
    map_df,
    locations="state_code",
    locationmode="USA-states",
    color="active_markets",
    scope="usa",
    hover_name="state",
    hover_data={
        "state_code": False,
        "active_markets": True,
        "operators": True,
    },
    color_continuous_scale=[
        "#F1F2F7",
        "#F5C58F",
        "#EE8A1D",
    ],
    labels={"active_markets": "Active markets"},
)

fig.update_layout(
    height=520,
    margin=dict(l=0, r=0, t=0, b=0),
    coloraxis_colorbar_title="Markets",
)

st.plotly_chart(fig, width="stretch")

st.subheader("Market Directory")

st.dataframe(
    filtered_df[
        [
            "operator",
            "market",
            "state",
            "vehicle_use",
            "service_status",
            "public_access",
            "booking_method",
            "source_url",
            "last_verified",
        ]
    ].sort_values(["operator", "state", "market"]),
    column_config={
        "operator": "Operator",
        "market": "Market",
        "state": "State",
        "vehicle_use": "Vehicle use",
        "service_status": "Service status",
        "public_access": "Public access",
        "booking_method": "How to access",
        "source_url": st.column_config.LinkColumn(
            "Official source",
            display_text="Open source",
        ),
        "last_verified": "Last verified",
    },
    width="stretch",
    hide_index=True,
)

st.caption(
    "Commercial, limited-access, testing, and announced markets should be tracked separately."
)
