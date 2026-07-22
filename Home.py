import base64
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="Autonomous Vehicle Access Tracker",
    page_icon="🚘",
    layout="wide",
)


# ---------------------------------------------------------
# HERO IMAGE
# Put your image here:
# assets/av_hero.jpg
# ---------------------------------------------------------

hero_image = Path("assets/av_hero.jpg")

if hero_image.exists():
    encoded_image = base64.b64encode(
        hero_image.read_bytes()
    ).decode("utf-8")

    hero_image_style = (
        "background-image: "
        f"url('data:image/jpeg;base64,{encoded_image}'); "
        "background-size: cover; "
        "background-position: center;"
    )
else:
    hero_image_style = (
        "background: linear-gradient(135deg, #dbe4ef, #9fb0c8);"
    )


# ---------------------------------------------------------
# PAGE STYLING
# ---------------------------------------------------------

st.markdown(
    """
<style>
.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
}

.hero {
    display: grid;
    grid-template-columns: 1fr 1fr;
    min-height: 650px;
    overflow: hidden;
    border-radius: 22px;
    margin-bottom: 2.5rem;
}

.hero-text {
    background-color: #13264f;
    padding: 5rem 4rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.hero-label {
    color: #ee8a1d;
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

st.image(
    "assets/av-dashboard-hero.jpg",
    width="stretch",
)}

.hero-title {
    color: #ffffff;
    font-size: clamp(3.5rem, 6vw, 6rem);
    line-height: 0.98;
    letter-spacing: -0.05em;
    font-weight: 800;
    margin: 0 0 2rem 0;
}

.hero-description {
    color: #d8dfed;
    font-size: clamp(1.1rem, 1.5vw, 1.4rem);
    line-height: 1.6;
    max-width: 650px;
    margin: 0;
}

.hero-image {
    min-height: 650px;
}

.intro-section {
    max-width: 950px;
    margin: 0 auto;
    text-align: center;
    padding: 1rem 1rem 2rem 1rem;
}

.intro-label {
    color: #ee8a1d;
    font-size: 0.8rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

.intro-title {
    font-size: clamp(2rem, 3.5vw, 3rem);
    line-height: 1.2;
    font-weight: 750;
    margin: 0 0 1rem 0;
}

.intro-description {
    font-size: 1.1rem;
    line-height: 1.7;
    opacity: 0.8;
    margin: 0;
}

@media (max-width: 900px) {
    .hero {
        grid-template-columns: 1fr;
    }

    .hero-text {
        padding: 4rem 2rem;
    }

    .hero-image {
        min-height: 375px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------

st.markdown(
f"""
<section class="hero">
<div class="hero-text">
<div class="hero-label">Autonomous Vehicle Policy</div>

<h1 class="hero-title">
Autonomous vehicle access
</h1>

<p class="hero-description">
Autonomous vehicles have the potential to make roads safer, expand mobility,
lower transportation costs, and give consumers more choice. This tracker
examines where Americans can access autonomous vehicle services and which
regulatory barriers continue to limit deployment.
</p>
</div>

<div class="hero-image" style="{hero_image_style}"></div>
</section>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# INTRO SECTION
# ---------------------------------------------------------

st.markdown(
    """
<section class="intro-section">
<div class="intro-label">Explore the tracker</div>

<h2 class="intro-title">
Access, safety, and regulation across the United States
</h2>

<p class="intro-description">
Use the pages in the sidebar to compare state policies, review consumer
access, examine safety evidence, and understand the methodology behind
the tracker.
</p>
</section>
""",
    unsafe_allow_html=True,
)