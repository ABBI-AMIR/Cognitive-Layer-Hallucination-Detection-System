import streamlit as st
from core.hallucination_detector import HallucinationDetector

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Hallucination Detection System",
    layout="centered"
)

st.title("🧠 Hallucination Detection System")
st.caption("Local LLM + Knowledge Graph + Constraint Validation")

# --------------------------------------------------
# Initialize Detector (cached)
# --------------------------------------------------
@st.cache_resource
def load_detector():
    return HallucinationDetector()

detector = load_detector()

# --------------------------------------------------
# User Input
# --------------------------------------------------
query = st.text_area(
    "Enter your query:",
    height=100,
    placeholder="e.g. Who is Elon Musk?"
)

submit = st.button("Analyze Response")

# --------------------------------------------------
# Processing
# --------------------------------------------------
if submit and query.strip():
    with st.spinner("Generating and validating response..."):
        result = detector.run(query)

    # --------------------------------------------------
    # Display Original Response
    # --------------------------------------------------
    st.subheader("📄 LLM Response")
    st.write(result["response"])

    # --------------------------------------------------
    # Validation Summary
    # --------------------------------------------------
    st.subheader("🔍 Validation Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Entity Check",
        "PASS" if result["entity_validation"].is_valid else "FAIL"
    )

    col2.metric(
        "Topic Check",
        "PASS" if result["topic_validation"].is_valid else "FAIL"
    )

    col3.metric(
        "KG Check",
        "PASS" if result["kg_validation"].is_valid else "FAIL"
    )

    # --------------------------------------------------
    # Violations Details
    # --------------------------------------------------
    st.subheader("⚠️ Detected Issues")

    def show_violations(title, validation):
        if validation.violations:
            st.error(title)
            for v in validation.violations:
                st.write(f"- {v}")
        else:
            st.success(f"{title}: No issues detected")

    show_violations("Entity Violations", result["entity_validation"])
    show_violations("Topic Violations", result["topic_validation"])
    show_violations("Knowledge Graph Violations", result["kg_validation"])

else:
    st.info("Enter a query and click **Analyze Response**")

