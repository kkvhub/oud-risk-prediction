# Home.py
import streamlit as st

st.set_page_config(
    page_title = "OUD Risk Prediction System",
    page_icon  = "hospital",
    layout     = "wide"
)

# ── Sidebar Branding ──────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 10px 0 5px 0;">
        <div style="font-size:48px;">🏥</div>
        <div style="font-size:16px; font-weight:700;
                    color:#2c7bb6; line-height:1.3;
                    margin-top:6px;">
            OUD Risk<br>Prediction System
        </div>
        <div style="font-size:11px; color:#888;
                    margin-top:4px;">
            Clinical Decision Support
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style="font-size:11px; color:#aaa;
                text-align:center; padding: 4px 0;">
        <b>Model</b><br>
        Neural Network<br>
        AUC-ROC: 0.7187<br>
        Recall: 92.0%<br>
        Threshold: 0.35
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Creator info
    st.markdown("""
    <div style="font-size:11px; color:#aaa; text-align:center;">
        <div style="margin-bottom:4px;">Created by</div>
        <div style="font-size:13px; font-weight:600;
                    color:#ccc;">
            Kashulendra Verma
        </div>
        <div style="margin-top:6px;">
            <a href="https://kkvhub.github.io/"
               target="_blank"
               style="color:#2c7bb6;
                      text-decoration:none;
                      font-size:12px;">
                🌐 Portfolio
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Disclaimer
    st.markdown("""
    <div style="font-size:9px; color:#777;
                text-align:center; line-height:1.5;
                padding: 0 4px;">
        <b style="color:#999;">DISCLAIMER</b><br>
        This application is developed for
        academic purposes only under an
        academic project.<br><br>
        Shall not be used for any commercial
        purpose.<br><br>
        All rights reserved &copy; 2025
        Kashulendra Verma
    </div>
    """, unsafe_allow_html=True)

# ── Main Page ─────────────────────────────────────────────────
st.title("OUD Treatment Dropout Risk Prediction")
st.markdown("#### Clinical Decision Support System")
st.markdown(
    "Predicting treatment dropout risk at admission "
    "to enable early clinical intervention."
)
st.divider()

# Navigation cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background:#1e3a5f; padding:24px;
                border-radius:12px; text-align:center;
                border-left: 4px solid #2c7bb6;
                min-height:160px;">
        <div style="font-size:36px;">📋</div>
        <div style="font-size:16px; font-weight:700;
                    color:#fff; margin:10px 0 8px 0;">
            Patient Intake
        </div>
        <div style="font-size:12px; color:#aaa;">
            Register a new patient and receive
            an instant dropout risk score
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Patient_Intake.py",
                 label="Go to Patient Intake")

with col2:
    st.markdown("""
    <div style="background:#1a3d2b; padding:24px;
                border-radius:12px; text-align:center;
                border-left: 4px solid #1a9641;
                min-height:160px;">
        <div style="font-size:36px;">📄</div>
        <div style="font-size:16px; font-weight:700;
                    color:#fff; margin:10px 0 8px 0;">
            Patient Report
        </div>
        <div style="font-size:12px; color:#aaa;">
            Generate a downloadable PDF risk
            assessment report for any patient
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Patient_Report.py",
                 label="Go to Patient Report")

with col3:
    st.markdown("""
    <div style="background:#3d2a1a; padding:24px;
                border-radius:12px; text-align:center;
                border-left: 4px solid #fdae61;
                min-height:160px;">
        <div style="font-size:36px;">📊</div>
        <div style="font-size:16px; font-weight:700;
                    color:#fff; margin:10px 0 8px 0;">
            Analytics Dashboard
        </div>
        <div style="font-size:12px; color:#aaa;">
            Executive view of all enrolled
            patients and risk trends
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_Analytics_Dashboard.py",
                 label="Go to Dashboard")

st.divider()

# Model summary strip
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Training Records",  "95,432")
with col2:
    st.metric("Model AUC-ROC",     "0.7187")
with col3:
    st.metric("Recall",            "92.0%")
with col4:
    st.metric("Features Used",     "27")

st.divider()

# Clinical disclaimer banner
st.markdown("""
<div style="background:#2a2a2a; border:1px solid #555;
            border-left: 5px solid #d7191c;
            padding:16px; border-radius:8px;
            font-size:12px; color:#bbb;">
    <b style="color:#e88;">CLINICAL DISCLAIMER</b><br>
    This tool is intended for <b>clinical decision support only</b>.
    It does not replace professional clinical judgment.
    Model trained on SAMHSA TEDS-D 2018 administrative intake data.
    Performance should be validated before any real-world clinical deployment.
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Academic disclaimer footer
st.markdown("""
<div style="background:#1a1a2e; border:1px solid #333;
            padding:14px; border-radius:8px;
            font-size:11px; color:#888;
            text-align:center; line-height:1.8;">
    <b style="color:#aaa;">ACADEMIC USE ONLY</b><br>
    This application is developed exclusively for academic
    purposes as part of a university project.<br>
    It shall not be used for any commercial purpose.<br>
    All rights reserved &copy; 2025
    <a href="https://kkvhub.github.io/"
       target="_blank"
       style="color:#2c7bb6; text-decoration:none;">
       Kashulendra Verma
    </a>
</div>
""", unsafe_allow_html=True)
