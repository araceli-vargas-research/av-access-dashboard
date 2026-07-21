import streamlit as st

st.set_page_config(
    page_title="AV Dashboard Methodology",
    page_icon="📘",
    layout="wide",
)

st.title("Methodology")
st.caption(
    "How the Autonomous Vehicle Access and Safety Tracker organizes evidence and evaluates policy conditions."
)

st.subheader("Dashboard Purpose")
st.write(
    "This dashboard tracks consumer access to autonomous vehicle services, "
    "reported safety evidence, and the regulatory conditions affecting deployment."
)

st.subheader("State Policy Score")

st.write(
    "Each state receives a preliminary score from 0 to 100. Higher scores represent "
    "a clearer and more permissive environment for autonomous vehicle deployment."
)

st.markdown(
    """
    **The score currently considers:**

    - Whether commercial autonomous vehicle operation is allowed
    - Whether the state has a uniform statewide framework
    - Whether municipalities can create separate AV restrictions
    - Whether a human operator is required
    - Insurance and liability requirements
    """
)

st.info(
    "The current scoring model is preliminary and will be updated as additional "
    "states, regulations, and source documents are reviewed."
)

st.subheader("Safety Evidence")

st.write(
    "Safety statistics should be reported with the relevant operator, comparison "
    "group, geography, study period, mileage exposure, and source. Company-reported "
    "results should not automatically be generalized to every autonomous vehicle system."
)

st.subheader("Access Categories")

st.markdown(
    """
    - **Commercial:** The public can book or use the service
    - **Limited access:** Service is available through a waitlist, invitation, or restricted program
    - **Driverless testing:** Vehicles operate without a safety driver but are not broadly available
    - **Safety-driver testing:** Testing occurs with a human safety operator
    - **Planned:** A future market has been announced but service has not launched
    """
)

st.subheader("Data Limitations")

st.write(
    "Autonomous vehicle policy and deployment conditions change quickly. The dashboard "
    "should be treated as a living research product and each record should include a "
    "source link and the date it was last verified."
)

st.subheader("Preliminary Scoring Weights")

weights = {
    "Policy component": [
        "Commercial driverless operation allowed",
        "Driverless testing allowed",
        "Uniform statewide framework",
        "Limits on separate local AV regulation",
        "No human-operator mandate",
        "No special AV permit",
        "Neutral insurance requirement",
    ],
    "Maximum points": [30, 15, 20, 15, 10, 5, 5],
}

import pandas as pd

st.dataframe(
    pd.DataFrame(weights),
    width="stretch",
    hide_index=True,
)

st.caption(
    "The score measures regulatory openness and consumer access. "
    "It does not measure the safety performance of an AV system."
)
