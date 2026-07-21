from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="State Explorer",
    page_icon="🗺️",
    layout="wide",
)

DATA_PATH = Path("data/processed/state_access.csv")


def yes_no(value, yes="Yes", no="No"):
    try:
        return yes if int(value) == 1 else no
    except (TypeError, ValueError):
        return "Not verified"


def money(value):
    try:
        value = float(value)
        if value <= 0:
            return "None recorded"
        return f"${value:,.0f}"
    except (TypeError, ValueError):
        return "Not verified"


def get_category(score):
    try:
        score = float(score)
    except (TypeError, ValueError):
        return "Not scored"

    if score >= 85:
        return "Highly permissive"
    if score >= 65:
        return "Generally permissive"
    if score >= 45:
        return "Mixed framework"
    if score >= 25:
        return "Restrictive"
    return "Highly restrictive"


if not DATA_PATH.exists():
    st.error("State policy dataset was not found.")
    st.stop()

df = pd.read_csv(DATA_PATH)

st.title("State Explorer")
st.caption(
    "Review autonomous-vehicle policy conditions, scoring components, "
    "research notes, and official sources for each state."
)

selected_state = st.selectbox(
    "Choose a state",
    sorted(df["state"].dropna().unique()),
    key="state_explorer_selector",
)

row = df.loc[df["state"].eq(selected_state)].iloc[0]

score = float(row.get("overall_score", 0))
category = get_category(score)
research_status = str(row.get("research_status", "")).strip()
source_status = str(row.get("source_status", "")).strip()

is_preliminary = (
    "preliminary" in research_status.lower()
    or "review" in research_status.lower()
    or "source added" in source_status.lower()
)

score_label = (
    "Preliminary policy score"
    if is_preliminary
    else "Policy score"
)

st.markdown(f"## {selected_state} Policy Profile")

if is_preliminary:
    st.info(
        "This state record is still classified as preliminary research. "
        "The score reflects the current coding methodology and should not be "
        "interpreted as a final legal determination."
    )

header_left, header_right = st.columns([2, 1], gap="large")

with header_left:
    with st.container(border=True):
        label_col, score_col = st.columns([2, 1])

        with label_col:
            st.caption("Policy category")
            st.markdown(f"### {category}")

            commercial = yes_no(
                row.get("commercial_operation_allowed"),
                "Commercial operation allowed",
                "Commercial operation not confirmed",
            )

            testing = yes_no(
                row.get("driverless_testing_allowed"),
                "Driverless testing allowed",
                "Driverless testing not confirmed",
            )

            st.write(commercial)
            st.write(testing)

        with score_col:
            st.caption(score_label)
            st.markdown(f"# {score:.0f}/100")

        st.progress(min(max(score / 100, 0), 1))

with header_right:
    with st.container(border=True):
        st.markdown("### Research status")
        st.write(research_status or "Not provided")

        if row.get("last_verified"):
            st.caption(f"Last verified: {row.get('last_verified')}")

st.subheader("Policy Conditions")

condition_1, condition_2, condition_3, condition_4 = st.columns(4)

with condition_1:
    with st.container(border=True):
        st.caption("Statewide framework")
        st.markdown(
            f"### {yes_no(row.get('statewide_rules'))}"
        )

with condition_2:
    with st.container(border=True):
        st.caption("Separate local AV rules")
        st.markdown(
            f"### {yes_no(row.get('local_rules_allowed'), 'Allowed', 'Limited')}"
        )

with condition_3:
    with st.container(border=True):
        st.caption("Human operator")
        st.markdown(
            f"### {yes_no(row.get('human_operator_required'), 'Required', 'Not required')}"
        )

with condition_4:
    with st.container(border=True):
        st.caption("Special permit")
        st.markdown(
            f"### {yes_no(row.get('special_permit_required'), 'Required', 'Not required')}"
        )

st.subheader("Score Breakdown")

components = pd.DataFrame(
    [
        {
            "Component": "Commercial operation",
            "Points": 30 if int(row.get("commercial_operation_allowed", 0)) == 1 else 0,
            "Maximum": 30,
        },
        {
            "Component": "Driverless testing",
            "Points": 15 if int(row.get("driverless_testing_allowed", 0)) == 1 else 0,
            "Maximum": 15,
        },
        {
            "Component": "Statewide framework",
            "Points": 20 if int(row.get("statewide_rules", 0)) == 1 else 0,
            "Maximum": 20,
        },
        {
            "Component": "Limits on separate local rules",
            "Points": 15 if int(row.get("local_rules_allowed", 1)) == 0 else 0,
            "Maximum": 15,
        },
        {
            "Component": "No human-operator mandate",
            "Points": 10 if int(row.get("human_operator_required", 1)) == 0 else 0,
            "Maximum": 10,
        },
        {
            "Component": "No special permit",
            "Points": 5 if int(row.get("special_permit_required", 1)) == 0 else 0,
            "Maximum": 5,
        },
        {
            "Component": "Insurance treatment",
            "Points": (
                5
                if float(row.get("insurance_minimum", 0)) == 0
                else 3
                if float(row.get("insurance_minimum", 0)) <= 1_000_000
                else 0
            ),
            "Maximum": 5,
        },
    ]
)

st.dataframe(
    components,
    column_config={
        "Component": st.column_config.TextColumn(
            "Scoring component",
            width="large",
        ),
        "Points": st.column_config.ProgressColumn(
            "Points awarded",
            min_value=0,
            max_value=30,
            format="%d",
        ),
        "Maximum": "Maximum",
    },
    hide_index=True,
    width="stretch",
)

detail_left, detail_right = st.columns([2, 1], gap="large")

with detail_left:
    st.subheader("Policy Summary")

    summary = str(row.get("policy_summary", "")).strip()

    if summary:
        st.info(summary)
    else:
        st.warning("No policy summary has been added.")

with detail_right:
    st.subheader("Additional Details")

    with st.container(border=True):
        st.write(
            f"**Insurance minimum:** "
            f"{money(row.get('insurance_minimum'))}"
        )

        if row.get("region"):
            st.write(f"**Region:** {row.get('region')}")

        if row.get("source_name"):
            st.write(f"**Primary source:** {row.get('source_name')}")

source_url = str(row.get("source_url", "")).strip()

if source_url:
    st.link_button(
        "Open official state source",
        source_url,
    )
else:
    st.warning("An official source has not yet been added for this state.")

st.divider()

st.caption(
    "Scores summarize coded policy conditions and are not legal advice. "
    "Preliminary records require additional source review before being treated "
    "as final."
)
