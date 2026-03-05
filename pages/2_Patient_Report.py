# pages/2_Patient_Report.py
import streamlit as st
import pandas as pd
import os
from fpdf import FPDF
import tempfile
from datetime import datetime

st.set_page_config(
    page_title="Patient Report",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Patient Risk Assessment Report")
st.markdown("Select a saved patient to generate their PDF report.")
st.divider()

PATIENTS_FILE = 'data/patients.csv'

# ── Load saved patients ───────────────────────────────────────
if not os.path.exists(PATIENTS_FILE) or    os.path.getsize(PATIENTS_FILE) == 0:
    st.warning("No patient records found. "
               "Please save a patient from the Intake page first.")
    st.stop()

df = pd.read_csv(PATIENTS_FILE)

if df.empty:
    st.warning("No patient records found.")
    st.stop()

# ── Patient selector ──────────────────────────────────────────
patient_ids = df['patient_id'].tolist()
selected_id = st.selectbox("Select Patient ID", patient_ids)
patient     = df[df['patient_id'] == selected_id].iloc[0]

# ── Patient summary preview ───────────────────────────────────
st.subheader("Patient Summary")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Patient ID",     patient['patient_id'])
    st.metric("Admission Date", patient['admission_date'])
with col2:
    st.metric("Age Group",      patient['age_group'])
    st.metric("Gender",         patient['gender'])
with col3:
    st.metric("Treatment Type", patient['treatment_type'])
    st.metric("Primary Drug",   patient['primary_substance'])
with col4:
    risk_pct = int(float(patient['risk_score']) * 100)
    level    = patient['risk_level']
    color    = {"High":"🔴","Moderate":"🟡","Low":"🟢"}.get(level,"⚪")
    st.metric("Risk Score",  f"{risk_pct}%")
    st.metric("Risk Level",  f"{color} {level}")

st.divider()

# ── Risk factor summary ───────────────────────────────────────
st.subheader("Risk Factor Summary")

risk_factors     = []
protective       = []
score            = float(patient['risk_score'])

# Identify risk factors from patient data
if patient['living_arrangement'] in ["Homeless / Shelter"]:
    risk_factors.append("Unstable housing situation")
if patient['prior_treatment'] == "No":
    risk_factors.append("No prior treatment history")
if patient['needle_use'] == "Yes":
    risk_factors.append("Needle / IV drug use reported")
if patient['employment'] == "Unemployed":
    risk_factors.append("Unemployed at time of admission")
if patient['psych_problem'] == "Yes":
    risk_factors.append("Co-occurring psychiatric condition")
if patient['arrests'] != "None":
    risk_factors.append("Recent criminal justice involvement")
if int(patient['num_substances']) >= 3:
    risk_factors.append("Multiple substance dependencies")
if patient['frequency'] == "Daily":
    risk_factors.append("Daily substance use reported")

# Identify protective factors
if patient['employment'] in ["Full-Time", "Part-Time"]:
    protective.append("Currently employed")
if patient['marital_status'] == "Married":
    protective.append("Married / has partner support")
if patient['prior_treatment'] == "Yes":
    protective.append("Has prior treatment experience")
if patient['arrests'] == "None":
    protective.append("No recent criminal history")
if patient['living_arrangement'] == "Independent":
    protective.append("Stable independent living")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Factors Increasing Risk:**")
    if risk_factors:
        for r in risk_factors:
            st.markdown(f"🔴 {r}")
    else:
        st.markdown("No major risk factors identified")
with col2:
    st.markdown("**Protective Factors:**")
    if protective:
        for p in protective:
            st.markdown(f"🟢 {p}")
    else:
        st.markdown("No protective factors identified")

# ── Recommended actions ───────────────────────────────────────
st.divider()
st.subheader("Recommended Clinical Actions")
level = patient['risk_level']
if level == "High":
    actions = [
        "Schedule weekly one-on-one counselor check-ins",
        "Refer to housing and social support services immediately",
        "Enroll in peer support or buddy program",
        "Review medication-assisted treatment options",
        "Flag for priority case management"
    ]
elif level == "Moderate":
    actions = [
        "Schedule bi-weekly counselor check-ins",
        "Review social support network at next session",
        "Consider peer support program enrollment",
        "Monitor attendance closely for first 30 days"
    ]
else:
    actions = [
        "Standard check-in schedule applies",
        "Continue monitoring at regular appointments",
        "Reassess risk score at 30-day review"
    ]

for a in actions:
    st.markdown(f"→ {a}")

# ── Generate PDF ──────────────────────────────────────────────
st.divider()
if st.button("📥 Generate PDF Report", type="primary",
             use_container_width=True):

    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(20, 20, 20)

    # Header
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_fill_color(44, 123, 182)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 12, "OUD DROPOUT RISK ASSESSMENT REPORT",
             ln=True, fill=True, align="C")
    pdf.ln(4)

    # Patient info block
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, "PATIENT INFORMATION", ln=True, fill=True)
    pdf.set_font("Helvetica", "", 10)
    info_lines = [
        f"Patient ID     : {patient['patient_id']}",
        f"Admission Date : {patient['admission_date']}",
        f"Treatment Type : {patient['treatment_type']}",
        f"Primary Drug   : {patient['primary_substance']}",
        f"Age Group      : {patient['age_group']}",
        f"Gender         : {patient['gender']}",
        f"Report Date    : {datetime.now().strftime('%B %d, %Y at %H:%M')}",
    ]
    for line in info_lines:
        pdf.cell(0, 7, line, ln=True)
    pdf.ln(4)

    # Risk score block
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, "RISK SCORE", ln=True, fill=True)
    pdf.set_font("Helvetica", "B", 24)
    risk_color = {"High":(215,25,28),
                  "Moderate":(253,174,97),
                  "Low":(26,150,65)}.get(level,(100,100,100))
    pdf.set_text_color(*risk_color)
    pdf.cell(0, 14,
             f"{int(float(patient['risk_score'])*100)}%  —  {level} Risk",
             ln=True, align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    # Risk factors
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, "KEY RISK FACTORS", ln=True, fill=True)
    pdf.set_font("Helvetica", "", 10)
    if risk_factors:
        for r in risk_factors:
            pdf.cell(0, 7, f"  [+] {r}", ln=True)
    else:
        pdf.cell(0, 7, "  No major risk factors identified", ln=True)
    pdf.ln(2)

    # Protective factors
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, "PROTECTIVE FACTORS", ln=True, fill=True)
    pdf.set_font("Helvetica", "", 10)
    if protective:
        for p in protective:
            pdf.cell(0, 7, f"  [-] {p}", ln=True)
    else:
        pdf.cell(0, 7, "  No protective factors identified", ln=True)
    pdf.ln(2)

    # Recommended actions
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, "RECOMMENDED CLINICAL ACTIONS", ln=True, fill=True)
    pdf.set_font("Helvetica", "", 10)
    for a in actions:
        pdf.cell(0, 7, f"  -> {a}", ln=True)
    pdf.ln(4)

    # Disclaimer
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(120, 120, 120)
    pdf.set_fill_color(250, 250, 250)
    pdf.multi_cell(0, 6,
        "DISCLAIMER: This report is generated by a machine learning model "
        "trained on SAMHSA TEDS-D 2018 data. It is intended as clinical "
        "decision support only and does not replace professional clinical "
        "judgment. Model: Neural Network | Threshold: 0.35 | "
        "AUC-ROC: 0.7187 | Recall: 92.0%",
        fill=True)

    # Save and offer download
    with tempfile.NamedTemporaryFile(delete=False,
                                     suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        with open(tmp.name, "rb") as f:
            pdf_bytes = f.read()

    st.download_button(
        label      = "⬇️ Download PDF Report",
        data       = pdf_bytes,
        file_name  = f"OUD_Risk_Report_{selected_id}.pdf",
        mime       = "application/pdf",
        use_container_width = True
    )
    st.success("PDF ready. Click the button above to download.")
