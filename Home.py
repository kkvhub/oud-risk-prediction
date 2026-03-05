# Home.py
import streamlit as st

st.set_page_config(
    page_title = "OUD Risk Prediction System",
    page_icon  = "🏥",
    layout     = "wide"
)

# Header
st.title("🏥 OUD Treatment Dropout Risk Prediction")
st.markdown("#### Clinical Decision Support System")
st.divider()

# Three navigation cards
col1, col2, col3 = st.columns(3)

with col1:
    st.info("### 📋 Patient Intake\n"
            "Register a new patient, enter intake details, "
            "and receive an instant dropout risk score.")
    st.page_link("pages/1_Patient_Intake.py",
                 label="Go to Patient Intake →")

with col2:
    st.success("### 📄 Patient Report\n"
               "Select any saved patient and generate "
               "a downloadable PDF risk assessment report.")
    st.page_link("pages/2_Patient_Report.py",
                 label="Go to Patient Report →")

with col3:
    st.warning("### 📊 Analytics Dashboard\n"
               "Executive view — track risk distribution, "
               "trends, and demographic breakdowns.")
    st.page_link("pages/3_Analytics_Dashboard.py",
                 label="Go to Dashboard →")

st.divider()
st.caption("⚠️ This tool is for clinical decision support only. "
           "It does not replace professional clinical judgment. "
           "Model trained on SAMHSA TEDS-D 2018 data.")
