
import streamlit as st
import pandas as pd

from architecture_engine import load_architectures, calculate_scores
from growth_model import predict_growth, determine_growth_level


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="FutureArch AI",
    page_icon="🏗️",
    layout="wide"
)

# -----------------------------------
# CUSTOM DESIGN
# -----------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #f4f7fc;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #17365d;
}

.sub-title {
    font-size: 16px;
    color: #52647a;
}

.section-title {
    color: #17365d;
    font-size: 23px;
    font-weight: 700;
}

div[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #dce5f1;
}

div[data-testid="stMetricValue"] {
    color: #17365d;
}

div.stButton > button {
    background-color: #17365d;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

div.stButton > button:hover {
    background-color: #28558b;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------------
# HEADER
# -----------------------------------

st.markdown(
    '<div class="main-title">🏗️ FutureArch AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Future-Aware Software Architecture Recommendation & Evolution System</div>',
    unsafe_allow_html=True
)

st.write(
    "An intelligent decision-support prototype for evaluating "
    "software architectures, predicting future application growth "
    "and planning architecture evolution."
)

st.divider()


# -----------------------------------
# SIDEBAR INPUT
# -----------------------------------

st.sidebar.title("⚙️ Application Inputs")

requirements = st.sidebar.text_area(
    "Application Requirements",
    placeholder=(
        "Example: E-commerce application with high traffic, "
        "online payments, large database, security and future growth."
    ),
    height=150
)

current_users = st.sidebar.number_input(
    "Current Users",
    min_value=100,
    value=10000,
    step=1000
)

annual_growth = st.sidebar.slider(
    "Expected Annual Growth (%)",
    min_value=5,
    max_value=100,
    value=30
)

analyze = st.sidebar.button(
    "🚀 Analyze Architecture",
    use_container_width=True
)

st.sidebar.divider()
st.sidebar.caption("FutureArch AI | Project Prototype")


# -----------------------------------
# INTRODUCTION
# -----------------------------------

st.markdown(
    '<div class="section-title">📊 Architecture Analysis Dashboard</div>',
    unsafe_allow_html=True
)

st.write(
    "Enter your application requirements in the sidebar "
    "and click Analyze Architecture to generate the results."
)


# -----------------------------------
# ANALYSIS
# -----------------------------------

if analyze:

    if not requirements.strip():
        st.warning("Please enter application requirements.")
        st.stop()

    # GROWTH PREDICTION

    predictions = predict_growth(
        current_users,
        annual_growth
    )

    max_users = predictions["Year 5"]

    growth_level = determine_growth_level(max_users)


    # REQUIREMENT ANALYSIS

    text = requirements.lower()

    detected = []

    keyword_groups = {
        "Scalability": [
            "scalability", "high traffic", "many users",
            "large users", "scale"
        ],
        "Transactions": [
            "payment", "transaction", "orders"
        ],
        "Large Data": [
            "database", "large data", "data storage"
        ],
        "Security": [
            "security", "secure", "privacy"
        ],
        "Performance": [
            "performance", "fast", "speed"
        ],
        "Future Growth": [
            "future", "growth", "expansion"
        ]
    }

    for category, words in keyword_groups.items():
        if any(word in text for word in words):
            detected.append(category)


    # ARCHITECTURE SCORING

    df = load_architectures()

    if max_users >= 100000:
        weights = [0.35, 0.20, 0.10, 0.15, 0.15, 0.05]
    else:
        weights = [0.20, 0.20, 0.20, 0.15, 0.15, 0.10]

    result = calculate_scores(df, *weights)

    best = result.iloc[0]

    display_result = result.copy()
    display_result["overall_score"] = (
        display_result["overall_score"].round(2)
    )


    # FUTURE ARCHITECTURE

    if max_users >= 100000:
        future_architecture = "Microservices"
    elif max_users >= 20000:
        future_architecture = "Modular Monolith"
    else:
        future_architecture = best["architecture"]


    # RISK ANALYSIS

    if max_users >= 1000000:
        risk = "High"
        cause = (
            "Very high user growth may create scalability, "
            "performance and infrastructure challenges."
        )
    elif max_users >= 100000:
        risk = "Medium"
        cause = (
            "Increasing traffic, transactions and data volume "
            "may require architectural improvements."
        )
    else:
        risk = "Low"
        cause = (
            "Projected workload remains relatively manageable."
        )


    # -----------------------------------
    # OVERVIEW METRICS
    # -----------------------------------

    st.divider()
    st.markdown("### 📌 Project Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Current Users",
        f"{current_users:,}"
    )

    c2.metric(
        "Year 5 Users",
        f"{max_users:,}"
    )

    c3.metric(
        "Growth Level",
        growth_level
    )

    c4.metric(
        "Future Risk",
        risk
    )


    # -----------------------------------
    # GROWTH PREDICTION
    # -----------------------------------

    st.divider()
    st.markdown("### 📈 1. Future Growth Prediction")

    growth_data = pd.DataFrame(
        list(predictions.items()),
        columns=["Year", "Predicted Users"]
    )

    st.line_chart(
        growth_data.set_index("Year")
    )

    st.dataframe(
        growth_data,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Prediction uses compound annual growth based on "
        "the growth rate entered by the user."
    )


    # -----------------------------------
    # REQUIREMENT ANALYSIS
    # -----------------------------------

    st.divider()
    st.markdown("### 🔍 2. Requirement Analysis")

    if detected:
        st.success(
            "Detected Requirements: " + ", ".join(detected)
        )
    else:
        st.info("General application requirements detected.")


    # -----------------------------------
    # ARCHITECTURE COMPARISON
    # -----------------------------------

    st.divider()
    st.markdown("### 🏛️ 3. Architecture Comparison")

    st.dataframe(
        display_result,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("#### Architecture Suitability Scores")

    chart_data = result.set_index(
        "architecture"
    )["overall_score"]

    st.bar_chart(chart_data)


    # -----------------------------------
    # RECOMMENDATION
    # -----------------------------------

    st.divider()
    st.markdown("### 🏆 4. Recommended Architecture")

    st.success(
        f"Recommended Architecture: {best['architecture']}"
    )

    st.metric(
        "Overall Suitability Score",
        f"{best['overall_score']:.2f}/100"
    )

    st.write(
        "The recommendation is based on weighted evaluation "
        "of scalability, performance, cost, maintainability, "
        "reliability and architectural simplicity."
    )


    # -----------------------------------
    # FUTURE ARCHITECTURE
    # -----------------------------------

    st.divider()
    st.markdown("### 🔮 5. Future Architecture Recommendation")

    st.info(
        f"Suggested Architecture for Future Growth: "
        f"**{future_architecture}**"
    )

    st.caption(
        "The future architecture is selected using prototype "
        "user-growth thresholds. It is a planning suggestion, "
        "not an automatic migration decision."
    )


    # -----------------------------------
    # RISK ANALYSIS
    # -----------------------------------

    st.divider()
    st.markdown("### ⚠️ 6. Sustainability & Risk Analysis")

    if risk == "High":
        st.error(f"Risk Level: {risk}")
    elif risk == "Medium":
        st.warning(f"Risk Level: {risk}")
    else:
        st.success(f"Risk Level: {risk}")

    st.write("**Possible Cause:**")
    st.write(cause)


    # -----------------------------------
    # EVOLUTION ROADMAP
    # -----------------------------------

    st.divider()
    st.markdown("### 🛣️ 7. Architecture Evolution Roadmap")

    if best["architecture"] == "Monolithic":

        roadmap = [
            "Current: Monolithic Architecture",
            "Stage 1: Introduce caching and load balancing",
            "Stage 2: Separate application modules",
            "Stage 3: Identify high-load modules",
            "Stage 4: Migrate selected modules into independent services"
        ]

    elif best["architecture"] == "Modular Monolith":

        roadmap = [
            "Current: Modular Monolith",
            "Stage 1: Improve module separation",
            "Stage 2: Introduce caching and load balancing",
            "Stage 3: Identify high-demand modules",
            "Stage 4: Convert selected modules into independent services"
        ]

    else:

        roadmap = [
            f"Current: {best['architecture']}",
            "Stage 1: Monitor application workload",
            "Stage 2: Optimize high-demand components",
            "Stage 3: Improve performance and reliability",
            "Stage 4: Scale components according to future requirements"
        ]

    for i, step in enumerate(roadmap):
        st.write(f"**{i + 1}.** ➡️ {step}")


    # -----------------------------------
    # FINAL SUMMARY
    # -----------------------------------

    st.divider()
    st.markdown("### 📋 8. Final Analysis Summary")

    summary = f"""
FUTUREARCH AI - ANALYSIS REPORT

Application Requirements:
{requirements}

Current Users: {current_users:,}
Expected Annual Growth: {annual_growth}%

Year 1 Predicted Users: {predictions['Year 1']:,}
Year 3 Predicted Users: {predictions['Year 3']:,}
Year 5 Predicted Users: {max_users:,}

Growth Classification: {growth_level}

Current Recommended Architecture: {best['architecture']}
Future Suggested Architecture: {future_architecture}

Suitability Score: {best['overall_score']:.2f}/100

Future Risk: {risk}
Possible Risk Cause: {cause}

Detected Requirements: {', '.join(detected) if detected else 'General Requirements'}

Note: This is a prototype decision-support system.
"""

    st.text(summary)

    st.download_button(
        label="⬇️ Download Analysis Report",
        data=summary,
        file_name="FutureArch_AI_Report.txt",
        mime="text/plain"
    )


# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.caption(
    "FutureArch AI | Future-Aware Software Architecture "
    "Recommendation & Evolution System | Academic Project Prototype"
)
