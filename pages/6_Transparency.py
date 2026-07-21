import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Data Transparency",
    page_icon="🔎",
    layout="wide",
)

st.title("Data Transparency")
st.caption(
    "Review the sources, verification dates, and limitations behind the dashboard."
)

st.subheader("Source Standards")

st.markdown(
    """
    Dashboard records should prioritize:

    - Federal and state government sources
    - Statutes, regulations, and official agency guidance
    - Municipal ordinances and legislative documents
    - Operator safety and deployment reports
    - Peer-reviewed or clearly documented research
    """
)

st.subheader("Verification Requirements")

st.markdown(
    """
    Each record should include:

    - Source name
    - Source link
    - Publication or effective date
    - Date last checked
    - Geographic coverage
    - Methodology notes
    - Whether the evidence is company-reported or independently produced
    """
)

st.warning(
    "The current dashboard contains preliminary example data. "
    "Figures should be verified before public release."
)

st.subheader("Current Data Files")

files = {
    "State policy data": "data/processed/state_access.csv",
    "Safety evidence": "data/processed/safety_data.csv",
    "Waymo scenario metrics": "data/processed/waymo_scenario_metrics.csv",
}

for label, path in files.items():
    try:
        df = pd.read_csv(path)
        st.success(f"{label}: {len(df):,} records loaded")
        with st.expander(f"Preview {label}"):
            st.dataframe(df.head(20), width="stretch", hide_index=True)
    except FileNotFoundError:
        st.error(f"{label}: file not found")
    except pd.errors.EmptyDataError:
        st.warning(f"{label}: file exists but is empty")

st.subheader("Known Limitations")

st.write(
    "AV deployment and policy conditions can change quickly. "
    "Service announcements do not always mean that the general public can book a ride. "
    "Testing authorization should also be distinguished from commercial deployment."
)
