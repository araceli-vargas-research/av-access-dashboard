from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Federal AV Policy",
    page_icon="🏛️",
    layout="wide",
)

DATA_PATH = Path("data/processed/federal_challenges.csv")

st.title("Federal AV Policy")
st.caption(
    "Explore how federal agencies shape autonomous vehicle safety, freight, "
    "infrastructure, transit, and communications policy."
)

df = pd.read_csv(DATA_PATH)

tab1, tab2, tab3 = st.tabs(
    [
        "Federal Overview",
        "Agency Profiles",
        "Compare Responsibilities",
    ]
)

with tab1:
    st.subheader("The Federal Policy Landscape")

    st.write(
        "Federal AV oversight is divided among several agencies. "
        "Each institution regulates a different part of the transportation "
        "system, which can create overlap, gaps, and uncertainty."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Federal bodies",
        df["agency"].nunique(),
    )

    col2.metric(
        "Challenges tracked",
        len(df),
    )

    col3.metric(
        "Policy categories",
        df["category"].nunique(),
    )

    col4.metric(
        "Recommendations",
        df["recommendation"].nunique(),
    )

    st.subheader("Key Federal Bottlenecks")

    bottlenecks = [
        {
            "title": "Outdated vehicle standards",
            "text": (
                "Some federal safety standards were written for conventional "
                "vehicles with steering wheels, pedals, mirrors, and human drivers."
            ),
        },
        {
            "title": "Limited exemption pathway",
            "text": (
                "Purpose-built autonomous vehicles may need temporary exemptions "
                "while permanent safety standards are updated."
            ),
        },
        {
            "title": "Fragmented authority",
            "text": (
                "Passenger vehicles, commercial freight, infrastructure, transit, "
                "and communications fall under different federal institutions."
            ),
        },
        {
            "title": "No unified national framework",
            "text": (
                "Federal rules, agency guidance, state laws, and testing programs "
                "do not yet operate as one consistent national system."
            ),
        },
    ]

    for item in bottlenecks:
        with st.container(border=True):
            st.markdown(f"### {item['title']}")
            st.write(item["text"])

    st.subheader("Current Federal Research")

    for row in df.itertuples():
        with st.container(border=True):
            top_left, top_right = st.columns([3, 1])

            with top_left:
                st.markdown(f"### {row.challenge}")
                st.caption(f"{row.agency} · {row.category}")

            with top_right:
                st.caption(f"Last verified: {row.last_verified}")

            condition_col, effect_col = st.columns(2)

            with condition_col:
                st.markdown("**Current condition**")
                st.write(row.current_condition)

            with effect_col:
                st.markdown("**Potential consumer effect**")
                st.write(row.consumer_effect)

            st.markdown("**Policy recommendation**")
            st.info(row.recommendation)

            if isinstance(row.source_url, str) and row.source_url.strip():
                st.link_button(
                    "Open official source",
                    row.source_url,
                )
            else:
                st.caption("Official source still needs to be added.")

with tab2:
    st.subheader("Agency Profiles")

    selected_agency = st.selectbox(
        "Choose a federal body",
        sorted(df["agency"].unique()),
    )

    agency_df = df[df["agency"] == selected_agency].copy()

    st.markdown(f"## {selected_agency}")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Challenges tracked",
        len(agency_df),
    )

    col2.metric(
        "Policy categories",
        agency_df["category"].nunique(),
    )

    col3.metric(
        "Recommendations",
        agency_df["recommendation"].nunique(),
    )

    for row in agency_df.itertuples():
        with st.container(border=True):
            st.markdown(f"### {row.challenge}")
            st.write(f"**Category:** {row.category}")

            st.markdown("**Current condition**")
            st.write(row.current_condition)

            st.markdown("**Potential consumer effect**")
            st.write(row.consumer_effect)

            st.markdown("**Policy recommendation**")
            st.write(row.recommendation)

            if isinstance(row.source_url, str) and row.source_url.strip():
                st.link_button(
                    "Open official source",
                    row.source_url,
                )
            else:
                st.caption("Official source still needs to be added.")

            st.caption(f"Last verified: {row.last_verified}")

with tab3:
    st.subheader("Compare Federal Responsibilities")

    responsibility_data = pd.DataFrame(
        [
            {
                "Federal body": "NHTSA",
                "Vehicle design": "Primary",
                "Passenger AVs": "Primary",
                "Freight": "Shared",
                "Infrastructure": "Limited",
                "Communications": "Limited",
            },
            {
                "Federal body": "FMCSA",
                "Vehicle design": "Limited",
                "Passenger AVs": "Limited",
                "Freight": "Primary",
                "Infrastructure": "Shared",
                "Communications": "Limited",
            },
            {
                "Federal body": "FHWA",
                "Vehicle design": "Limited",
                "Passenger AVs": "Shared",
                "Freight": "Shared",
                "Infrastructure": "Primary",
                "Communications": "Shared",
            },
            {
                "Federal body": "FTA",
                "Vehicle design": "Limited",
                "Passenger AVs": "Transit",
                "Freight": "Limited",
                "Infrastructure": "Transit",
                "Communications": "Limited",
            },
            {
                "Federal body": "FCC",
                "Vehicle design": "Limited",
                "Passenger AVs": "Limited",
                "Freight": "Limited",
                "Infrastructure": "Shared",
                "Communications": "Primary",
            },
            {
                "Federal body": "Congress",
                "Vehicle design": "Legislation",
                "Passenger AVs": "Legislation",
                "Freight": "Legislation",
                "Infrastructure": "Legislation",
                "Communications": "Legislation",
            },
        ]
    )

    st.dataframe(
        responsibility_data,
        width="stretch",
        hide_index=True,
    )

    st.info(
        "This matrix is a simplified policy overview. Responsibilities may "
        "overlap depending on the vehicle, service, and operating environment."
    )

st.divider()

st.subheader("Methodology and Data")

st.write(
    "A federal challenge is included when a law, rule, standard, exemption "
    "process, or division of authority may affect autonomous vehicle testing, "
    "manufacturing, deployment, or consumer access."
)

st.markdown(
    """
    Records should distinguish between:

    - Existing law or regulation
    - Proposed rule or legislation
    - Agency guidance
    - Research finding
    - CCC policy recommendation
    """
)

st.download_button(
    label="Download federal policy data",
    data=df.to_csv(index=False),
    file_name="federal_av_policy.csv",
    mime="text/csv",
)

st.info(
    "Federal policy records are sourced to official government materials and "
    "should be reviewed periodically as rules, guidance, and legislation change."
)

st.divider()
st.header("Federal Policy Timeline")

timeline_path = Path("data/processed/federal_sources.csv")
timeline_df = pd.read_csv(timeline_path)

timeline_df["date"] = pd.to_datetime(timeline_df["date"])
timeline_df = timeline_df.sort_values("date", ascending=False)

for row in timeline_df.itertuples():
    with st.container(border=True):
        date_col, content_col = st.columns([1, 4])

        with date_col:
            st.markdown(f"### {row.date:%Y}")
            st.caption(f"{row.date:%B %d}")

        with content_col:
            st.markdown(f"### {row.development}")
            st.caption(
                f"{row.agency} · {row.policy_area} · {row.status}"
            )
            st.write(row.why_it_matters)
            st.link_button("Open official source", row.source_url)

st.divider()
st.header("Federal Source Library")

selected_area = st.multiselect(
    "Filter by policy area",
    sorted(timeline_df["policy_area"].unique()),
    default=sorted(timeline_df["policy_area"].unique()),
    key="federal_source_library_filter",
)

source_view = timeline_df[
    timeline_df["policy_area"].isin(selected_area)
].copy()

st.dataframe(
    source_view[
        [
            "date",
            "agency",
            "development",
            "policy_area",
            "status",
            "source_url",
        ]
    ],
    column_config={
        "date": st.column_config.DateColumn(
            "Date",
            format="MMM D, YYYY",
        ),
        "agency": "Agency",
        "development": st.column_config.TextColumn(
            "Development",
            width="large",
        ),
        "policy_area": "Policy area",
        "status": "Status",
        "source_url": st.column_config.LinkColumn(
            "Official source",
            display_text="Open source",
        ),
    },
    width="stretch",
    hide_index=True,
)

st.download_button(
    "Download federal source library",
    source_view.to_csv(index=False),
    file_name="federal_av_sources.csv",
    mime="text/csv",
)

