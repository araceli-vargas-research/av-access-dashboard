from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="AV Dashboard Overview",
    page_icon="🚘",
    layout="wide",
)


# ---------------------------------------------------------
# COLORS
# ---------------------------------------------------------

NAVY = "#13264F"
BLUE = "#1768B3"
LIGHT_BLUE = "#E7F0FC"

ORANGE = "#EE8A1D"
LIGHT_ORANGE = "#FBE9D5"

TEXT = "#3F4653"
MUTED = "#6C7483"
LIGHT_GRAY = "#F4F6F9"
BORDER = "#E2E6EC"
WHITE = "#FFFFFF"


# ---------------------------------------------------------
# PAGE STYLING
# ---------------------------------------------------------

st.markdown(
    f"""
<style>
.block-container {{
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 4rem;
    padding-left: 2rem;
    padding-right: 2rem;
}}

[data-testid="stAppViewContainer"] {{
    background-color: #F4F6F9;
}}

[data-testid="stHeader"] {{
    background-color: transparent;
}}

.overview-title {{
    color: {NAVY};
    font-size: clamp(2.5rem, 4vw, 4rem);
    line-height: 1.05;
    letter-spacing: -0.045em;
    font-weight: 800;
    margin: 0;
}}

.overview-caption {{
    color: {MUTED};
    font-size: 1.15rem;
    line-height: 1.6;
    max-width: 900px;
    margin-top: 1rem;
    margin-bottom: 2.5rem;
}}

.section-card {{
    background: {WHITE};
    border: 1px solid {BORDER};
    border-radius: 20px;
    padding: 2rem;
    height: 100%;
}}

.section-label {{
    color: {ORANGE};
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}}

.section-title {{
    color: {NAVY};
    font-size: clamp(1.8rem, 2.7vw, 2.7rem);
    line-height: 1.15;
    font-weight: 800;
    letter-spacing: -0.035em;
    margin: 0 0 1rem 0;
}}

.section-description {{
    color: {MUTED};
    font-size: 1.03rem;
    line-height: 1.7;
    margin: 0;
}}

.takeaway-title {{
    color: {NAVY};
    font-size: clamp(1.75rem, 2.5vw, 2.5rem);
    line-height: 1.17;
    letter-spacing: -0.035em;
    font-weight: 800;
    margin: 0 0 1.4rem 0;
}}

.takeaway-text {{
    color: {MUTED};
    font-size: 1.04rem;
    line-height: 1.65;
    margin-bottom: 1rem;
}}

.takeaway-highlight {{
    color: {NAVY};
    font-weight: 750;
}}

.metric-grid {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 1rem;
    margin: 1rem 0 2.5rem 0;
}}

.metric-card {{
    background: {WHITE};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 1.35rem 1.5rem;
}}

.metric-accent-blue {{
    border-top: 5px solid {BLUE};
}}

.metric-accent-orange {{
    border-top: 5px solid {ORANGE};
}}

.metric-label {{
    color: {MUTED};
    font-size: 0.88rem;
    font-weight: 650;
    margin-bottom: 0.6rem;
}}

.metric-value {{
    color: {NAVY};
    font-size: 2.25rem;
    line-height: 1;
    font-weight: 800;
}}

.metric-note {{
    color: {MUTED};
    font-size: 0.8rem;
    margin-top: 0.55rem;
}}

.info-box-blue {{
    background: {LIGHT_BLUE};
    color: {BLUE};
    border-radius: 14px;
    padding: 1.25rem 1.4rem;
    font-size: 1rem;
    line-height: 1.55;
    margin-top: 1rem;
}}

.info-box-orange {{
    background: {LIGHT_ORANGE};
    color: #A55200;
    border-radius: 14px;
    padding: 1.25rem 1.4rem;
    font-size: 1rem;
    line-height: 1.55;
    margin-top: 1rem;
}}

.small-heading {{
    color: {NAVY};
    font-size: 1.35rem;
    font-weight: 800;
    margin-bottom: 0.4rem;
}}

.small-caption {{
    color: {MUTED};
    font-size: 0.95rem;
    line-height: 1.55;
    margin-bottom: 1rem;
}}

.safety-card {{
    background: {WHITE};
    border: 1px solid {BORDER};
    border-left: 6px solid {BLUE};
    border-radius: 16px;
    padding: 1.5rem;
    height: 100%;
}}

.safety-number {{
    color: {BLUE};
    font-size: 2.2rem;
    line-height: 1;
    font-weight: 800;
    margin-bottom: 0.6rem;
}}

.safety-title {{
    color: {NAVY};
    font-size: 1rem;
    font-weight: 750;
    margin-bottom: 0.7rem;
}}

.safety-detail {{
    color: {MUTED};
    font-size: 0.84rem;
    line-height: 1.5;
}}

.divider {{
    height: 1px;
    background: {BORDER};
    margin: 2.5rem 0;
}}

.color-key {{
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    margin-top: 1rem;
    color: {MUTED};
    font-size: 0.85rem;
}}

.key-item {{
    display: flex;
    align-items: center;
    gap: 0.45rem;
}}

.key-dot-blue {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: {BLUE};
}}

.key-dot-orange {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: {ORANGE};
}}

.key-dot-gray {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #C9CED7;
}}

@media (max-width: 900px) {{
    .metric-grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }}
}}

@media (max-width: 600px) {{
    .block-container {{
        padding-left: 1rem;
        padding-right: 1rem;
    }}

    .metric-grid {{
        grid-template-columns: 1fr;
    }}
}}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

state_df = pd.read_csv("data/processed/state_access.csv")

reviewed_df = state_df[
    state_df["research_status"].fillna("Not reviewed") != "Not reviewed"
].copy()

safety_df = pd.read_csv("data/processed/safety_data.csv")
market_df = pd.read_csv("data/processed/market_tracker.csv")

waymo_path = Path("data/processed/waymo_scenario_metrics.csv")


# ---------------------------------------------------------
# SUMMARY VALUES
# ---------------------------------------------------------

states_tracked = len(reviewed_df)

commercial_states = int(
    reviewed_df["commercial_operation_allowed"]
    .fillna(False)
    .astype(bool)
    .sum()
)

statewide_frameworks = int(
    reviewed_df["statewide_rules"]
    .fillna(False)
    .astype(bool)
    .sum()
)

average_policy_score = (
    reviewed_df["overall_score"].mean()
    if not reviewed_df.empty
    else 0
)

active_markets = market_df["market"].nunique()

public_market_rows = market_df[
    market_df["public_access"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("yes")
]

public_markets = public_market_rows["market"].nunique()


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------

st.markdown(
    """
<h1 class="overview-title">
Autonomous vehicle access in the United States
</h1>

<p class="overview-caption">
A national snapshot of consumer availability, state policy conditions,
safety evidence, and the geographic reach of autonomous vehicle services.
</p>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# TOP METRICS
# ---------------------------------------------------------

st.markdown(
    f"""
<div class="metric-grid">

    <div class="metric-card metric-accent-blue">
        <div class="metric-label">States reviewed</div>
        <div class="metric-value">{states_tracked}</div>
        <div class="metric-note">Policy research coverage</div>
    </div>

    <div class="metric-card metric-accent-orange">
        <div class="metric-label">Commercial AV states</div>
        <div class="metric-value">{commercial_states}</div>
        <div class="metric-note">Commercial operation recorded</div>
    </div>

    <div class="metric-card metric-accent-blue">
        <div class="metric-label">Statewide frameworks</div>
        <div class="metric-value">{statewide_frameworks}</div>
        <div class="metric-note">State-level regulatory structure</div>
    </div>

    <div class="metric-card metric-accent-blue">
        <div class="metric-label">Average policy score</div>
        <div class="metric-value">{average_policy_score:.0f}</div>
        <div class="metric-note">Out of 100</div>
    </div>

</div>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# KEY TAKEAWAY + MAP
# ---------------------------------------------------------

takeaway_col, map_col = st.columns(
    [0.78, 1.55],
    gap="large",
    vertical_alignment="top",
)

with takeaway_col:
    st.markdown(
        """
<div class="section-label">Key takeaway</div>

<h2 class="takeaway-title">
Access depends on both commercial deployment and state-level policy
</h2>

<p class="takeaway-text">
Autonomous vehicle access remains concentrated in a limited number of
markets. A state may permit testing or commercial operation without
consumers having access to a publicly available service.
</p>

<p class="takeaway-text">
Policy scores describe the legal and regulatory environment, while market
records describe where services are currently documented.
</p>

<p class="takeaway-text takeaway-highlight">
A favorable policy framework can enable deployment, but it does not by
itself guarantee consumer access.
</p>

<div class="color-key">
    <div class="key-item">
        <span class="key-dot-blue"></span>
        Policy and regulatory conditions
    </div>

    <div class="key-item">
        <span class="key-dot-orange"></span>
        Consumer access and deployment
    </div>

    <div class="key-item">
        <span class="key-dot-gray"></span>
        Not reviewed or unavailable
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

with map_col:
    st.markdown(
        """
<div class="section-card">
<div class="small-heading">State policy environment</div>
<div class="small-caption">
Policy score from 0 to 100. Higher scores indicate a regulatory
environment that is more accommodating to autonomous vehicle access.
</div>
""",
        unsafe_allow_html=True,
    )

    map_fig = px.choropleth(
        state_df,
        locations="state_code",
        locationmode="USA-states",
        color="overall_score",
        scope="usa",
        hover_name="state",
        hover_data={
            "state_code": False,
            "overall_score": ":.0f",
            "commercial_operation_allowed": True,
            "statewide_rules": True,
            "local_rules_allowed": True,
            "insurance_minimum": True,
            "research_status": True,
        },
        range_color=(0, 100),
        color_continuous_scale=[
            [0.00, "#E9EDF3"],
            [0.35, "#B7CCE5"],
            [0.70, "#5F91C4"],
            [1.00, BLUE],
        ],
        labels={
            "overall_score": "Policy score",
            "commercial_operation_allowed": "Commercial operation",
            "statewide_rules": "Statewide rules",
            "local_rules_allowed": "Local rules allowed",
            "insurance_minimum": "Insurance minimum",
            "research_status": "Research status",
        },
    )

    map_fig.update_geos(
        bgcolor="rgba(0,0,0,0)",
        lakecolor="white",
        showlakes=False,
    )

    map_fig.update_layout(
        height=520,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=5, b=0),
        coloraxis_colorbar=dict(
            title="Policy score",
            tickvals=[0, 20, 40, 60, 80, 100],
            ticktext=["0", "20", "40", "60", "80", "100"],
            thickness=12,
            len=0.72,
        ),
        font=dict(
            family="Arial",
            color=TEXT,
        ),
    )

    st.plotly_chart(
        map_fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# SAFETY EVIDENCE
# ---------------------------------------------------------

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown(
    """
<div class="section-label">Safety evidence</div>

<h2 class="section-title">
Reported outcomes compared with human-driver benchmarks
</h2>

<p class="section-description">
Reported reductions compare rider-only autonomous driving performance with
human-driver benchmarks in comparable operating areas and driving exposure.
Blue is used here because these figures describe evidence and benchmarks,
rather than consumer availability.
</p>
""",
    unsafe_allow_html=True,
)

safety_columns = st.columns(2, gap="large")

for index, row in enumerate(safety_df.itertuples()):
    study_period = getattr(row, "study_period", "")
    comparison_group = getattr(row, "comparison_group", "")
    geography = getattr(row, "geography", "")

    detail_lines = []

    if comparison_group:
        detail_lines.append(
            f"<strong>Baseline:</strong> {comparison_group}"
        )

    if study_period:
        detail_lines.append(
            f"<strong>Study period:</strong> {study_period}"
        )

    if geography:
        detail_lines.append(
            f"<strong>Geography:</strong> {geography}"
        )

    details = "<br>".join(detail_lines)

    with safety_columns[index % 2]:
        st.markdown(
            f"""
<div class="safety-card">
    <div class="safety-number">{row.value:.0f}% fewer</div>
    <div class="safety-title">{row.metric}</div>
    <div class="safety-detail">{details}</div>
</div>
""",
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------
# CONSUMER ACCESS
# ---------------------------------------------------------

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

access_left, access_right = st.columns(
    [1.25, 1],
    gap="large",
    vertical_alignment="top",
)

with access_left:
    st.markdown(
        """
<div class="section-card">
<div class="section-label">Consumer access</div>

<h2 class="section-title">
Markets recorded by operator
</h2>

<p class="section-description">
Counts represent distinct markets documented in the tracker. They do not
measure total rides, fleet size, vehicles deployed, or market share.
</p>
""",
        unsafe_allow_html=True,
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
        custom_data=["states"],
        labels={
            "operator": "Operator",
            "markets": "Markets tracked",
        },
    )

    access_fig.update_traces(
        marker_color=ORANGE,
        textposition="outside",
        textfont=dict(
            color=NAVY,
            size=14,
        ),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Markets tracked: %{y}<br>"
            "States represented: %{customdata[0]}"
            "<extra></extra>"
        ),
    )

    chart_max = max(access_summary["markets"].max(), 1)

    access_fig.update_yaxes(
        title="Markets currently tracked",
        range=[0, chart_max + max(2, chart_max * 0.18)],
        rangemode="tozero",
        tickmode="linear",
        dtick=2 if chart_max > 6 else 1,
        gridcolor="#E1E6ED",
        zerolinecolor="#C9D0DA",
        tickfont=dict(color=MUTED),
        title_font=dict(color=MUTED),
    )

    access_fig.update_xaxes(
        title="",
        tickfont=dict(color=MUTED),
        showgrid=False,
    )

    access_fig.update_layout(
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=20, r=20, t=35, b=20),
        bargap=0.28,
        font=dict(
            family="Arial",
            color=TEXT,
        ),
    )

    st.plotly_chart(
        access_fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )

    st.markdown("</div>", unsafe_allow_html=True)

with access_right:
    st.markdown(
        f"""
<div class="section-card">
<div class="section-label">Market access</div>

<h2 class="section-title">
Current tracker coverage
</h2>

<div class="metric-grid" style="grid-template-columns: repeat(2, 1fr); margin-bottom: 1.25rem;">

    <div class="metric-card metric-accent-orange">
        <div class="metric-label">Active markets tracked</div>
        <div class="metric-value">{active_markets}</div>
        <div class="metric-note">Distinct markets in the dataset</div>
    </div>

    <div class="metric-card metric-accent-orange">
        <div class="metric-label">Publicly accessible markets</div>
        <div class="metric-value">{public_markets}</div>
        <div class="metric-note">Distinct markets marked public</div>
    </div>

</div>

<div class="info-box-orange">
Operator counts indicate where services are recorded in the dataset.
They should not be interpreted as ridership, fleet size, or market share.
</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# RESEARCH COVERAGE
# ---------------------------------------------------------

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

scenario_count = 0

if waymo_path.exists():
    try:
        waymo_df = pd.read_csv(waymo_path)
        scenario_count = len(waymo_df)
    except pd.errors.EmptyDataError:
        scenario_count = 0

st.markdown(
    f"""
<div class="section-label">Research coverage</div>

<h2 class="section-title">
Records supporting the dashboard
</h2>

<div class="metric-grid">

    <div class="metric-card metric-accent-blue">
        <div class="metric-label">Policy records</div>
        <div class="metric-value">{len(reviewed_df):,}</div>
        <div class="metric-note">Reviewed state records</div>
    </div>

    <div class="metric-card metric-accent-orange">
        <div class="metric-label">Market records</div>
        <div class="metric-value">{len(market_df):,}</div>
        <div class="metric-note">Operator-market observations</div>
    </div>

    <div class="metric-card metric-accent-blue">
        <div class="metric-label">Safety records</div>
        <div class="metric-value">{len(safety_df):,}</div>
        <div class="metric-note">Reported safety outcomes</div>
    </div>

    <div class="metric-card metric-accent-blue">
        <div class="metric-label">Waymo scenarios processed</div>
        <div class="metric-value">{scenario_count:,}</div>
        <div class="metric-note">Scenario-level research coverage</div>
    </div>

</div>

<div class="info-box-blue">
These totals describe dashboard research coverage. They do not represent
the total scale of autonomous vehicle activity in the United States.
</div>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# STATE COMPARISON
# ---------------------------------------------------------

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown(
    """
<div class="section-label">State comparison</div>

<h2 class="section-title">
Detailed policy records
</h2>

<p class="section-description">
Review the underlying state policy indicators and compare scores,
commercial permissions, statewide rules, and research status.
</p>
""",
    unsafe_allow_html=True,
)

comparison_columns = [
    column
    for column in [
        "state",
        "state_code",
        "overall_score",
        "commercial_operation_allowed",
        "statewide_rules",
        "local_rules_allowed",
        "insurance_minimum",
        "research_status",
    ]
    if column in reviewed_df.columns
]

comparison_df = (
    reviewed_df[comparison_columns]
    .sort_values("overall_score", ascending=False)
)

st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "state": st.column_config.TextColumn("State"),
        "state_code": st.column_config.TextColumn("Code"),
        "overall_score": st.column_config.ProgressColumn(
            "Policy score",
            min_value=0,
            max_value=100,
            format="%.0f",
        ),
        "commercial_operation_allowed": st.column_config.CheckboxColumn(
            "Commercial operation"
        ),
        "statewide_rules": st.column_config.CheckboxColumn(
            "Statewide framework"
        ),
        "local_rules_allowed": st.column_config.CheckboxColumn(
            "Local rules allowed"
        ),
        "insurance_minimum": st.column_config.TextColumn(
            "Insurance minimum"
        ),
        "research_status": st.column_config.TextColumn(
            "Research status"
        ),
    },
)