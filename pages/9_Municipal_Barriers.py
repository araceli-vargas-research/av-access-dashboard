from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Municipal AV Policy",
    page_icon="🏙️",
    layout="wide",
)

DATA_PATH = Path("data/processed/municipal_barriers.csv")

st.title("Municipal AV Policy")
st.caption(
    "Explore city-level proposals, operating conditions, and local coordination affecting autonomous vehicles."
)

df = pd.read_csv(DATA_PATH)

tab1, tab2, tab3 = st.tabs(
    [
        "Municipal Overview",
        "City Profiles",
        "Compare Policies",
    ]
)

with tab1:
    left, right = st.columns([1, 2], gap="large")

    with left:
        st.markdown(
            """
            ## Local rules can determine whether AV access is practical

            Autonomous vehicles face a third regulatory layer at the municipal level.

            Even when federal standards are satisfied and state law permits AV operation,
            cities may still influence deployment through:

            - Special permits
            - Human-operator requirements
            - Fleet limits
            - Operating-area restrictions
            - Permit fees
            - Local review processes

            Ordinary city responsibilities such as curb management, traffic enforcement,
            and emergency coordination are not automatically classified as barriers.
            """
        )

        st.info(
            "This page currently covers a small group of verified cities. "
            "The chart describes cities tracked in this dataset, not every U.S. municipality."
        )

    with right:
        with st.container(border=True):
            st.markdown("### Municipal policy mix by city")
            st.caption(
                "Each stacked segment represents one recorded policy condition."
            )

            status_options = sorted(df["status"].dropna().unique())
            record_options = sorted(df["record_type"].dropna().unique())

            filter_col1, filter_col2 = st.columns(2)

            with filter_col1:
                selected_status = st.multiselect(
                    "Policy status",
                    status_options,
                    default=status_options,
                    key="municipal_overview_status",
                )

            with filter_col2:
                selected_record_types = st.multiselect(
                    "Record type",
                    record_options,
                    default=record_options,
                    key="municipal_overview_record_type",
                )

            filtered_df = df[
                df["status"].isin(selected_status)
                & df["record_type"].isin(selected_record_types)
            ].copy()

            filtered_df["Human operator"] = (
                filtered_df["human_operator_required"] == 1
            ).astype(int)

            filtered_df["Special permit"] = (
                filtered_df["special_permit_required"] == 1
            ).astype(int)

            filtered_df["Fleet cap"] = (
                filtered_df["fleet_cap"] > 0
            ).astype(int)

            filtered_df["Insurance minimum"] = (
                filtered_df["insurance_minimum"] > 0
            ).astype(int)

            filtered_df["Operating-hours limit"] = (
                filtered_df["operating_hours_limit"] == 1
            ).astype(int)

            filtered_df["Geographic restriction"] = (
                filtered_df["geographic_restriction"] == 1
            ).astype(int)

            condition_columns = [
                "Human operator",
                "Special permit",
                "Fleet cap",
                "Insurance minimum",
                "Operating-hours limit",
                "Geographic restriction",
            ]

            stacked_df = filtered_df.melt(
                id_vars=["city", "state"],
                value_vars=condition_columns,
                var_name="Policy condition",
                value_name="Condition present",
            )

            stacked_df = stacked_df[
                stacked_df["Condition present"] == 1
            ].copy()

            if stacked_df.empty:
                st.warning("No policy conditions match the selected filters.")
            else:
                fig = px.bar(
                    stacked_df,
                    x="city",
                    y="Condition present",
                    color="Policy condition",
                    barmode="stack",
                    hover_data={
                        "state": True,
                        "Condition present": False,
                    },
                    labels={
                        "city": "",
                        "Condition present": "Policy conditions recorded",
                    },
                    color_discrete_sequence=[
                        "#EE8A1D",
                        "#F3AA57",
                        "#F7C98F",
                        "#53607D",
                        "#8A94A9",
                        "#C4CBD7",
                    ],
                )

                fig.update_layout(
                    height=470,
                    margin=dict(l=0, r=20, t=20, b=0),
                    legend_title_text="Policy condition",
                    yaxis=dict(
                        dtick=1,
                        title="Number of conditions recorded",
                    ),
                )

                st.plotly_chart(fig, width="stretch")

            metric1, metric2, metric3 = st.columns(3)

            metric1.metric(
                "Cities shown",
                filtered_df["city"].nunique(),
            )

            metric2.metric(
                "Proposed measures",
                int((filtered_df["status"] == "Proposed").sum()),
            )

            metric3.metric(
                "Official sources",
                int(
                    filtered_df["source_url"]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                    .ne("")
                    .sum()
                ),
            )

    st.divider()
    st.subheader("Current Municipal Research")

    for row in filtered_df.itertuples():
        with st.container(border=True):
            title_col, date_col = st.columns([4, 1])

            with title_col:
                st.markdown(f"### {row.city}, {row.state}")
                st.caption(
                    f"{row.proposal_or_rule} · {row.status} · {row.record_type}"
                )

            with date_col:
                st.caption(f"Verified: {row.last_verified}")

            st.write(row.summary)

            condition_cols = st.columns(4)

            condition_cols[0].metric(
                "Human operator",
                "Required"
                if row.human_operator_required == 1
                else "Not required",
            )

            condition_cols[1].metric(
                "Special permit",
                "Required"
                if row.special_permit_required == 1
                else "Not required",
            )

            condition_cols[2].metric(
                "Fleet cap",
                f"{int(row.fleet_cap):,}"
                if row.fleet_cap > 0
                else "None recorded",
            )

            condition_cols[3].metric(
                "Permit fee",
                f"${row.permit_fee:,.0f}"
                if row.permit_fee > 0
                else "None recorded",
            )

            if isinstance(row.source_url, str) and row.source_url.strip():
                st.link_button(
                    "Open official municipal source",
                    row.source_url,
                )

            st.caption(f"Research status: {row.research_status}")

with tab2:
    st.subheader("City Profiles")

    selected_city = st.selectbox(
        "Choose a city",
        sorted(df["city"].unique()),
        key="municipal_city_profile",
    )

    city_df = df[df["city"] == selected_city].copy()

    for row in city_df.itertuples():
        st.markdown(f"## {row.city}, {row.state}")
        st.caption(f"{row.proposal_or_rule} · {row.status}")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Human operator",
            "Required"
            if row.human_operator_required == 1
            else "Not required",
        )

        col2.metric(
            "Special permit",
            "Required"
            if row.special_permit_required == 1
            else "Not required",
        )

        col3.metric(
            "Fleet cap",
            f"{int(row.fleet_cap):,}"
            if row.fleet_cap > 0
            else "None recorded",
        )

        col4.metric(
            "Insurance minimum",
            f"${row.insurance_minimum:,.0f}"
            if row.insurance_minimum > 0
            else "None recorded",
        )

        st.subheader("Policy Summary")
        st.info(row.summary)

        if isinstance(row.source_url, str) and row.source_url.strip():
            st.link_button(
                "Open official municipal source",
                row.source_url,
            )

with tab3:
    st.subheader("Compare Municipal Policies")

    st.dataframe(
        df[
            [
                "city",
                "state",
                "proposal_or_rule",
                "status",
                "barrier_type",
                "human_operator_required",
                "special_permit_required",
                "fleet_cap",
                "insurance_minimum",
                "permit_fee",
                "operating_hours_limit",
                "geographic_restriction",
                "source_url",
                "research_status",
            ]
        ],
        column_config={
            "source_url": st.column_config.LinkColumn(
                "Official source",
                display_text="Open source",
            ),
        },
        width="stretch",
        hide_index=True,
    )

st.divider()

st.subheader("Methodology")

st.write(
    "Municipal records distinguish proposed AV-specific restrictions from "
    "active rules and ordinary city responsibilities such as curb management, "
    "traffic enforcement, and incident coordination."
)

st.download_button(
    "Download municipal policy data",
    data=df.to_csv(index=False),
    file_name="municipal_av_policy.csv",
    mime="text/csv",
)
