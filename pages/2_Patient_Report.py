# pages/2_Patient_Report.py
import streamlit as st
import pandas as pd
import os, sys, tempfile
from fpdf import FPDF
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.sheets import load_patients

st.set_page_config(page_title="Patient Report",
                   page_icon="📄", layout="wide")
st.title("📄 Patient Risk Assessment Report")
st.markdown("Select a saved patient to generate their PDF report.")
st.divider()

df = load_patients()

if df.empty:
    st.warning("No patient records found. "
               "Save a patient from the Intake page first.")
    st.stop()

patient_ids = df["patient_id"].tolist()
selected_id = st.selectbox("Select Patient ID", patient_ids)
patient     = df[df["patient_id"] == selected_id].iloc[0]

# Patient summary
st.subheader("Patient Summary")
col1,col2,col3,col4 = st.columns(4)
with col1:
    st.metric("Patient ID",     patient["patient_id"])
    st.metric("Admission Date", patient["admission_date"])
with col2:
    st.metric("Age Group", patient["age_group"])
    st.metric("Gender",    patient["gender"])
with col3:
    st.metric("Treatment", patient["treatment_type"])
    st.metric("Primary Drug", patient["primary_substance"])
with col4:
    risk_pct = int(float(patient["risk_score"]) * 100)
    level    = patient["risk_level"]
    icon     = {"High":"🔴","Moderate":"🟡","Low":"🟢"}.get(level,"⚪")
    st.metric("Risk Score", f"{risk_pct}%")
    st.metric("Risk Level", f"{icon} {level}")

st.divider()

# Risk factors
risk_factors = []
protective   = []

if patient["living_arrangement"] == "Homeless / Shelter":
    risk_factors.append("Unstable housing situation")
if patient["prior_treatment"] == "No":
    risk_factors.append("No prior treatment history")
if patient["needle_use"] == "Yes":
    risk_factors.append("Needle / IV drug use reported")
if patient["employment"] == "Unemployed":
    risk_factors.append("Unemployed at time of admission")
if patient["psych_problem"] == "Yes":
    risk_factors.append("Co-occurring psychiatric condition")
if patient["arrests"] != "None":
    risk_factors.append("Recent criminal justice involvement")
if int(float(patient["num_substances"])) >= 3:
    risk_factors.append("Multiple substance dependencies")
if patient["frequency"] == "Daily":
    risk_factors.append("Daily substance use reported")

if patient["employment"] in ["Full-Time","Part-Time"]:
    protective.append("Currently employed")
if patient["marital_status"] == "Married":
    protective.append("Married / has partner support")
if patient["prior_treatment"] == "Yes":
    protective.append("Has prior treatment experience")
if patient["arrests"] == "None":
    protective.append("No recent criminal history")
if patient["living_arrangement"] == "Independent":
    protective.append("Stable independent living")

st.subheader("Risk Factor Summary")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Factors Increasing Risk:**")
    for r in risk_factors or ["None identified"]:
        st.markdown(f"🔴 {r}")
with col2:
    st.markdown("**Protective Factors:**")
    for p in protective or ["None identified"]:
        st.markdown(f"🟢 {p}")

# Actions
level = patient["risk_level"]
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

st.divider()
st.subheader("Recommended Clinical Actions")
for a in actions:
    st.markdown(f"→ {a}")

# PDF generation
st.divider()
if st.button("📥 Generate PDF Report", type="primary",
             use_container_width=True):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(20, 20, 20)

    pdf.set_font("Helvetica","B",16)
    pdf.set_fill_color(44,123,182)
    pdf.set_text_color(255,255,255)
    pdf.cell(0,12,"OUD DROPOUT RISK ASSESSMENT REPORT",
             ln=True, fill=True, align="C")
    pdf.ln(4)

    pdf.set_text_color(0,0,0)
    for label, val in [
        ("Patient ID",     patient["patient_id"]),
        ("Admission Date", patient["admission_date"]),
        ("Treatment Type", patient["treatment_type"]),
        ("Primary Drug",   patient["primary_substance"]),
        ("Age Group",      patient["age_group"]),
        ("Gender",         patient["gender"]),
        ("Report Date",    datetime.now().strftime("%B %d, %Y")),
    ]:
        pdf.set_font("Helvetica","B",10)
        pdf.cell(50,7,f"{label}:",ln=0)
        pdf.set_font("Helvetica","",10)
        pdf.cell(0,7,str(val),ln=True)
    pdf.ln(3)

    pdf.set_font("Helvetica","B",10)
    pdf.set_fill_color(240,240,240)
    pdf.cell(0,8,"RISK SCORE",ln=True,fill=True)
    rc = {"High":(215,25,28),"Moderate":(253,174,97),
          "Low":(26,150,65)}.get(level,(100,100,100))
    pdf.set_font("Helvetica","B",24)
    pdf.set_text_color(*rc)
    pdf.cell(0,14,
             f"{int(float(patient['risk_score'])*100)}%  —  {level} Risk",
             ln=True,align="C")
    pdf.set_text_color(0,0,0)
    pdf.ln(2)

    for section, items in [
        ("KEY RISK FACTORS",       risk_factors or ["None identified"]),
        ("PROTECTIVE FACTORS",     protective   or ["None identified"]),
        ("RECOMMENDED ACTIONS",    actions)
    ]:
        pdf.set_font("Helvetica","B",10)
        pdf.set_fill_color(240,240,240)
        pdf.cell(0,8,section,ln=True,fill=True)
        pdf.set_font("Helvetica","",10)
        for item in items:
            pdf.cell(0,7,f"  - {item}",ln=True)
        pdf.ln(2)

    pdf.set_font("Helvetica","I",8)
    pdf.set_text_color(120,120,120)
    pdf.multi_cell(0,6,
        "DISCLAIMER: Clinical decision support only. "
        "Does not replace professional judgment. "
        "Model: Neural Network | Threshold: 0.35 | "
        "AUC-ROC: 0.7187 | Recall: 92.0%")

    with tempfile.NamedTemporaryFile(delete=False,
                                     suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        pdf_bytes = open(tmp.name,"rb").read()

    st.download_button(
        label     = "⬇️ Download PDF Report",
        data      = pdf_bytes,
        file_name = f"OUD_Risk_{selected_id}.pdf",
        mime      = "application/pdf",
        use_container_width=True
    )
    st.success("PDF ready — click button above to download.")
