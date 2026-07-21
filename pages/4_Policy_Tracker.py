import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="AV Policy Tracker",
    page_icon="⚖️",
    layout="wide",
)

st.title("Policy Tracker")
st.caption(
    "Compare state rules affecting autonomous vehicle testing, deployment, and consumer access."
)

df = pd.read_csv("data/processed/state_access.csv")

reviewed_df = df[
    df["research_status"] != "Not reviewed"
].copy()

with st.sidebar:
    st.header("Filters")

    commercial_filter = st.selectbox(
        "Commercial operation",
        ["All", "Allowed", "Restricted"],
    )

    framework_filter = st.selectbox(
        "Statewide framework",
        ["All", "Yes", "No"],
    )

    permit_filter = st.selectbox(
        "Special permit",
        ["All", "Required", "Not required"],
    )

filtered_df = reviewed_df.copy()

if commercial_filter == "Allowed":
    filtered_df = filtered_df[
        filtered_df["commercial_operation_allowed"] == 1
    ]
elif commercial_filter == "Restricted":
    filtered_df = filtered_df[
        filtered_df["commercial_operation_allowed"] == 0
    ]

if framework_filter == "Yes":
    filtered_df = filtered_df[
        filtered_df["statewide_rules"] == 1
    ]
elif framework_filter == "No":
    filtered_df = filtered_df[
        filtered_df["statewide_rules"] == 0
    ]

if permit_filter == "Required":
    filtered_df = filtered_df[
        filtered_df["special_permit_required"] == 1
    ]
elif permit_filter == "Not required":
    filtered_df = filtered_df[
        filtered_df["special_permit_required"] == 0
    ]

col1, col2, col3, col4 = st.columns(4)

col1.metric("States shown", len(filtered_df))
col2.metric(
    "Commercial AV states",
    int(filtered_df["commercial_operation_allowed"].sum()),
)
col3.metric(
    "Statewide frameworks",
    int(filtered_df["statewide_rules"].sum()),
)
col4.metric(
    "Average policy score",
    f"{filtered_df['overall_score'].mean():.0f}/100"
    if len(filtered_df)
    else "—",
)

barriers = pd.DataFrame(
    {
        "Barrier": [
            "Local AV rules allowed",
            "Human operator required",
            "Commercial operation restricted",
            "Special permit required",
            "No statewide framework",
        ],
        "States": [
            int(filtered_df["local_rules_allowed"].sum()),
            int(filtered_df["human_operator_required"].sum()),
            int(
                (
                    filtered_df["commercial_operation_allowed"] == 0
                ).sum()
            ),
            int(filtered_df["special_permit_required"].sum()),
            int((filtered_df["statewide_rules"] == 0).sum()),
        ],
    }
).sort_values("States")

st.subheader("Regulatory Barriers")

fig = px.bar(
    barriers,
    x="States",
    y="Barrier",
    orientation="h",
    text="States",
    color="States",
    color_continuous_scale=[
        "#F1F2F7",
        "#F5C58F",
        "#EE8A1D",
    ],
)

fig.update_traces(textposition="outside")

fig.update_layout(
    height=460,
    coloraxis_showscale=False,
    margin=dict(l=0, r=50, t=10, b=0),
    xaxis_title="Number of states",
    yaxis_title="",
)

st.plotly_chart(fig, width="stretch")

st.subheader("State Policy Research")

display_df = filtered_df.copy()

display_df["Commercial operation"] = display_df[
    "commercial_operation_allowed"
].map({1: "Allowed", 0: "Restricted"})

display_df["Statewide framework"] = display_df[
    "statewide_rules"
].map({1: "Yes", 0: "No"})

display_df["Local AV rules"] = display_df[
    "local_rules_allowed"
].map({1: "Allowed", 0: "Limited"})

display_df["Human operator"] = display_df[
    "human_operator_required"
].map({1: "Required", 0: "Not required"})

display_df["Special permit"] = display_df[
    "special_permit_required"
].map({1: "Required", 0: "Not required"})

st.dataframe(
    display_df[
        [
            "state",
            "Commercial operation",
            "Statewide framework",
            "Local AV rules",
            "Human operator",
            "Special permit",
            "insurance_minimum",
            "overall_score",
            "policy_summary",
            "source_url",
            "last_verified",
        ]
    ].sort_values("overall_score", ascending=False),
    column_config={
        "state": "State",
        "insurance_minimum": st.column_config.NumberColumn(
            "Insurance minimum",
            format="$%d",
        ),
        "overall_score": st.column_config.ProgressColumn(
            "Policy score",
            min_value=0,
            max_value=100,
            format="%d",
        ),
        "policy_summary": st.column_config.TextColumn(
            "Policy summary",
            width="large",
        ),
        "source_url": st.column_config.LinkColumn(
            "Official source",
            display_text="Open source",
        ),
        "last_verified": "Last verified",
    },
    width="stretch",
    hide_index=True,
)

st.divider()
st.header("Regional Comparison")

regional_summary = (
    reviewed_df.groupby("region", as_index=False)
    .agg(
        average_policy_score=("overall_score", "mean"),
        states_reviewed=("state", "count"),
        commercial_states=("commercial_operation_allowed", "sum"),
        statewide_frameworks=("statewide_rules", "sum"),
    )
)

region_col1, region_col2 = st.columns(2)

with region_col1:
    st.subheader("Average Policy Score by Region")

    regional_score_fig = px.bar(
        regional_summary.sort_values("average_policy_score"),
        x="average_policy_score",
        y="region",
        orientation="h",
        text="average_policy_score",
        color="average_policy_score",
        color_continuous_scale=[
            "#F1F2F7",
            "#F5C58F",
            "#EE8A1D",
        ],
        labels={
            "average_policy_score": "Average policy score",
            "region": "",
        },
    )

    regional_score_fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside",
    )

    regional_score_fig.update_layout(
        height=400,
        coloraxis_showscale=False,
        xaxis_range=[0, 100],
        margin=dict(l=0, r=40, t=10, b=0),
    )

    st.plotly_chart(regional_score_fig, width="stretch")

with region_col2:
    st.subheader("Commercial AV States by Region")

    commercial_region_fig = px.bar(
        regional_summary,
        x="region",
        y=["commercial_states", "states_reviewed"],
        barmode="group",
        labels={
            "value": "States",
            "region": "",
            "variable": "",
        },
    )

    commercial_region_fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
    )

    st.plotly_chart(commercial_region_fig, width="stretch")

st.subheader("Regional Policy Summary")

st.dataframe(
    regional_summary.sort_values(
        "average_policy_score",
        ascending=False,
    ),
    column_config={
        "region": "Region",
        "average_policy_score": st.column_config.ProgressColumn(
            "Average policy score",
            min_value=0,
            max_value=100,
            format="%.1f",
        ),
        "states_reviewed": "States",
        "commercial_states": "Commercial AV states",
        "statewide_frameworks": "Statewide frameworks",
    },
    width="stretch",
    hide_index=True,
)
