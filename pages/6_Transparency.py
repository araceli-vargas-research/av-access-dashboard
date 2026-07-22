from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Data Transparency",
    page_icon="🔎",
    layout="wide",
)

DATA_DIR = Path("data/processed")

st.title("Data Transparency")
st.caption(
    "Review the sources, verification practices, coverage, and limitations behind the dashboard."
)

left, right = st.columns(2, gap="large")

with left:
    with st.container(border=True):
        st.subheader("Source Standards")
        st.write(
            "The dashboard prioritizes evidence that can be traced to a clear and reviewable source."
        )

        st.markdown(
            """
            - Federal and state government sources
            - Statutes, regulations, and official agency guidance
            - Municipal ordinances and legislative documents
            - Operator safety and deployment reports
            - Peer-reviewed or clearly documented research
            """
        )

with right:
    with st.container(border=True):
        st.subheader("Verification Practices")
        st.write(
            "Where available, records include enough context for readers to assess the claim."
        )

        st.markdown(
            """
            - Source name and direct link
            - Publication or effective date
            - Date last reviewed
            - Geographic coverage
            - Methodology or comparison notes
            - Whether evidence is company-reported or independently produced
            """
        )

st.info(
    "The dashboard combines reviewed records with some entries that remain preliminary. "
    "Preliminary records are labeled in the relevant policy pages and should not be treated "
    "as formal legal determinations."
)

st.subheader("Current Data Coverage")

datasets = [
    {
        "label": "State policy data",
        "filename": "state_access.csv",
        "description": "State-level policy conditions, scores, sources, and verification notes.",
    },
    {
        "label": "Safety evidence",
        "filename": "safety_data.csv",
        "description": "Selected AV safety findings with study context and comparison information.",
    },
    {
        "label": "Waymo scenario metrics",
        "filename": "waymo_scenario_metrics.csv",
        "description": "Processed scenario-level measures derived from the local research workflow.",
    },
]

for item in datasets:
    path = DATA_DIR / item["filename"]

    with st.container(border=True):
        title_col, count_col = st.columns([4, 1])

        with title_col:
            st.markdown(f"### {item['label']}")
            st.caption(item["description"])

        if path.exists():
            df = pd.read_csv(path)

            with count_col:
                st.metric("Records loaded", len(df))

            with st.expander(f"Preview {item['label']}"):
                st.dataframe(
                    df.head(10),
                    width="stretch",
                    hide_index=True,
                )
        else:
            with count_col:
                st.metric("Records loaded", 0)

            st.warning(f"{item['filename']} was not found.")

st.subheader("Known Limitations")

with st.container(border=True):
    st.markdown(
        """
        **Policy changes quickly.** AV statutes, agency guidance, local proposals, and deployment conditions may change after a record is reviewed.

        **Testing is not commercial deployment.** Authorization to test autonomous vehicles does not necessarily allow unrestricted commercial passenger service.

        **Announcements are not always public access.** A company may announce a market, mapping activity, testing, or a future launch before members of the public can book rides.

        **Safety studies are not always directly comparable.** Findings may use different geographies, mileage periods, crash definitions, comparison groups, or reporting methods.

        **Policy scores are analytical summaries.** Scores reflect the dashboard's coding framework and are not legal advice or official government ratings.

        **Municipal coverage is selective.** The municipal section includes only city-level measures supported by sufficiently specific sources and is not a census of every U.S. city.
        """
    )

st.subheader("How to Interpret the Dashboard")

st.write(
    "Use the dashboard as a research and comparison tool. Open the linked source when a "
    "specific legal, safety, or deployment claim is important, and review the verification "
    "status shown for the record."
)

st.caption(
    "Last-updated dates describe when records were reviewed for this project, not necessarily "
    "when the underlying law, study, or announcement first took effect."
)
