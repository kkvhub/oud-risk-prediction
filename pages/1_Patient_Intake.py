# pages/1_Patient_Intake.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, datetime
import uuid
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.predict import predict_risk

st.set_page_config(page_title="Patient Intake", page_icon="📋", layout="wide")
st.title("📋 Patient Intake Form")
st.markdown("Complete all sections below and click **Calculate Risk Score**.")
st.divider()

PATIENTS_FILE = 'data/patients.csv'

# ── SECTION A — Patient Identification ──────────────────────────
st.subheader("Section A — Patient Identification")
col1, col2, col3 = st.columns(3)
with col1:
    patient_id     = st.text_input("Patient ID (leave blank to auto-generate)")
with col2:
    admission_date = st.date_input("Admission Date", value=date.today())
with col3:
    treatment_type = st.selectbox("Treatment Type", [
        "Detox", "Residential Short-Term", "Residential Long-Term",
        "Intensive Outpatient", "Standard Outpatient", "Medication-Assisted"
    ])

# ── SECTION B — Demographics ─────────────────────────────────────
st.divider()
st.subheader("Section B — Demographics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    age_group = st.selectbox("Age Group", [
        "12-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"
    ])
with col2:
    gender = st.selectbox("Gender", ["Male", "Female"])
with col3:
    race = st.selectbox("Race / Ethnicity", [
        "White", "Black / African American", "Hispanic",
        "Asian / Pacific Islander", "American Indian / Alaska Native",
        "Other / Mixed"
    ])
with col4:
    state = st.selectbox("State", [
        "Alabama","Alaska","Arizona","Arkansas","California","Colorado",
        "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho",
        "Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana",
        "Maine","Maryland","Massachusetts","Michigan","Minnesota",
        "Mississippi","Missouri","Montana","Nebraska","Nevada",
        "New Hampshire","New Jersey","New Mexico","New York",
        "North Carolina","North Dakota","Ohio","Oklahoma","Oregon",
        "Pennsylvania","Rhode Island","South Carolina","South Dakota",
        "Tennessee","Texas","Utah","Vermont","Virginia","Washington",
        "West Virginia","Wisconsin","Wyoming"
    ])

col1, col2 = st.columns(2)
with col1:
    veteran = st.selectbox("Veteran Status", ["No", "Yes"])
with col2:
    education = st.selectbox("Education Level", [
        "Less than High School", "High School / GED",
        "Some College", "College Graduate"
    ])

# ── SECTION C — Substance Use Profile ───────────────────────────
st.divider()
st.subheader("Section C — Substance Use Profile")
col1, col2, col3 = st.columns(3)
with col1:
    primary_substance = st.selectbox("Primary Substance", [
        "Heroin", "Other Opiates", "Alcohol",
        "Cocaine / Crack", "Methamphetamine",
        "Marijuana", "Other"
    ])
    heroin     = st.selectbox("Heroin Use",    ["No", "Yes"])
with col2:
    frequency  = st.selectbox("Use Frequency", [
        "No Use", "1-3 Times/Month",
        "1-2 Times/Week", "3+ Times/Week", "Daily"
    ])
    needle_use = st.selectbox("Needle / IV Use", ["No", "Yes"])
with col3:
    num_substances = st.number_input("Number of Substances",
                                     min_value=1, max_value=6, value=1)

st.markdown("**Other Substances Used:**")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    alcohol      = st.checkbox("Alcohol")
with col2:
    marijuana    = st.checkbox("Marijuana")
with col3:
    stimulant    = st.checkbox("Stimulants")
with col4:
    tranquilizer = st.checkbox("Tranquilizers")
with col5:
    sedative     = st.checkbox("Sedatives")
col1, col2 = st.columns(2)
with col1:
    hallucinogen = st.checkbox("Hallucinogens")
with col2:
    inhalant     = st.checkbox("Inhalants")

# ── SECTION D — Social and Clinical Context ──────────────────────
st.divider()
st.subheader("Section D — Social and Clinical Context")
col1, col2, col3 = st.columns(3)
with col1:
    employment = st.selectbox("Employment Status", [
        "Full-Time", "Part-Time", "Unemployed",
        "Not in Labor Force", "Student"
    ])
    prior_treatment = st.selectbox("Prior Treatment History", ["No", "Yes"])
with col2:
    living_arrangement = st.selectbox("Living Arrangement", [
        "Independent", "Dependent / Supported",
        "Homeless / Shelter", "Residential Program"
    ])
    psych_problem = st.selectbox("Psychiatric / Mental Health Condition", ["No", "Yes"])
with col3:
    marital_status = st.selectbox("Marital Status", [
        "Never Married", "Married", "Separated",
        "Divorced", "Widowed"
    ])
    referral_source = st.selectbox("Referral Source", [
        "Self / Family", "Substance Abuse Provider",
        "Criminal Justice", "School", "Employer",
        "Healthcare Provider", "Other"
    ])

arrests = st.selectbox("Recent Arrests (past 30 days)", ["None", "Once", "Two or More"])

# ── CALCULATE RISK ────────────────────────────────────────────────
st.divider()
submit = st.button("🔍 Calculate Risk Score", type="primary", use_container_width=True)

if submit:

    # Map form inputs to model feature codes
    AGE_MAP        = {"12-17":1,"18-24":2,"25-34":3,"35-44":4,
                      "45-54":5,"55-64":6,"65+":7}
    GENDER_MAP     = {"Male":1,"Female":2}
    EMPLOY_MAP     = {"Full-Time":1,"Part-Time":2,"Unemployed":3,
                      "Not in Labor Force":4,"Student":5}
    LIVING_MAP     = {"Independent":3,"Dependent / Supported":2,
                      "Homeless / Shelter":1,"Residential Program":4}
    MARSTAT_MAP    = {"Never Married":1,"Married":2,"Separated":3,
                      "Divorced":4,"Widowed":5}
    FREQ_MAP       = {"No Use":0,"1-3 Times/Month":1,"1-2 Times/Week":2,
                      "3+ Times/Week":3,"Daily":4}
    ARREST_MAP     = {"None":0,"Once":1,"Two or More":2}
    EDUC_MAP       = {"Less than High School":1,"High School / GED":2,
                      "Some College":3,"College Graduate":4}
    SERVICES_MAP   = {"Detox":1,"Residential Short-Term":2,
                      "Residential Long-Term":3,"Intensive Outpatient":4,
                      "Standard Outpatient":5,"Medication-Assisted":6}
    PSOURCE_MAP    = {"Self / Family":1,"Substance Abuse Provider":2,
                      "Other Healthcare Provider":3,"School":4,
                      "Employer":5,"Criminal Justice":7,"Other":8}
    RACE_MAP       = {"White":5,"Black / African American":4,
                      "Hispanic":3,"Asian / Pacific Islander":2,
                      "American Indian / Alaska Native":1,
                      "Other / Mixed":6}

    patient_features = {
        'AGECAT'   : AGE_MAP[age_group],
        'GENDER'   : GENDER_MAP[gender],
        'RACE'     : RACE_MAP[race],
        'EMPLOY'   : EMPLOY_MAP[employment],
        'LIVARAG'  : LIVING_MAP[living_arrangement],
        'MARSTAT'  : MARSTAT_MAP[marital_status],
        'EDUC'     : EDUC_MAP[education],
        'ARRESTS'  : ARREST_MAP[arrests],
        'SERVICES' : SERVICES_MAP[treatment_type],
        'PSOURCE'  : PSOURCE_MAP[referral_source],
        'FREQMAX'  : FREQ_MAP[frequency],
        'NUMSUBS'  : num_substances,
        'NOPRIOR'  : 0 if prior_treatment == "Yes" else 1,
        'PSYPROB'  : 1 if psych_problem == "Yes" else 2,
        'VET'      : 1 if veteran == "Yes" else 2,
        'NEEDLEUSE': 1 if needle_use == "Yes" else 0,
        'HEROIN'   : 1 if heroin == "Yes" else 0,
        'ALCFLG'   : 1 if alcohol else 0,
        'MARFLG'   : 1 if marijuana else 0,
        'STIMFLAG' : 1 if stimulant else 0,
        'TRNQFLAG' : 1 if tranquilizer else 0,
        'SEDFLAG'  : 1 if sedative else 0,
        'HALFLAG'  : 1 if hallucinogen else 0,
        'INHFLG'   : 1 if inhalant else 0,
        'STFIPS'   : 1,    # placeholder — map state names to FIPS if needed
        'ETHNIC'   : 1,    # not collected in form — default
        'REGION'   : 1,    # not collected in form — default
        'PRIMPAY'  : 1,    # not collected in form — default
        'PRIMINC'  : 1,    # not collected in form — default
    }

    risk_score, risk_level = predict_risk(patient_features)
    risk_pct = int(risk_score * 100)

    # ── Display Risk Score ──
    st.divider()
    color = {"High":"🔴","Moderate":"🟡","Low":"🟢"}[risk_level]
    bg    = {"High":"#ffe5e5","Moderate":"#fff8e1","Low":"#e8f5e9"}[risk_level]

    st.markdown(f"""
    <div style="background:{bg};padding:24px;border-radius:12px;text-align:center">
        <h2>{color} {risk_level} Risk of Dropout</h2>
        <h1 style="font-size:56px;margin:0">{risk_pct}%</h1>
        <p style="font-size:16px">Model confidence that this patient will leave treatment prematurely</p>
    </div>
    """, unsafe_allow_html=True)

    # Progress bar as gauge
    st.progress(risk_score)

    # ── Recommended Actions ──
    st.subheader("Recommended Clinical Actions")
    if risk_level == "High":
        st.error("⚠️ High priority — immediate follow-up recommended")
        st.markdown("""
        - Schedule **weekly** one-on-one counselor check-ins
        - Refer to **housing and social support** services immediately
        - Enroll in **peer support** or buddy program
        - Flag for **medication-assisted treatment** review if not already enrolled
        """)
    elif risk_level == "Moderate":
        st.warning("⚡ Moderate priority — monitor closely")
        st.markdown("""
        - Schedule **bi-weekly** counselor check-ins
        - Review social support network at next session
        - Consider peer support program enrollment
        """)
    else:
        st.success("✅ Low priority — standard follow-up")
        st.markdown("""
        - Standard check-in schedule
        - Continue monitoring at regular appointments
        """)

    # ── Save Patient Record ──
    st.divider()
    if st.button("💾 Save Patient Record", type="secondary",
                 use_container_width=True):

        final_id = patient_id.strip() if patient_id.strip() \
                   else f"OUD-{str(uuid.uuid4())[:8].upper()}"

        new_record = {
            'patient_id'        : final_id,
            'admission_date'    : str(admission_date),
            'treatment_type'    : treatment_type,
            'age_group'         : age_group,
            'gender'            : gender,
            'race'              : race,
            'state'             : state,
            'veteran'           : veteran,
            'primary_substance' : primary_substance,
            'frequency'         : frequency,
            'needle_use'        : needle_use,
            'num_substances'    : num_substances,
            'stimulant'         : stimulant,
            'tranquilizer'      : tranquilizer,
            'sedative'          : sedative,
            'hallucinogen'      : hallucinogen,
            'heroin'            : heroin,
            'employment'        : employment,
            'living_arrangement': living_arrangement,
            'marital_status'    : marital_status,
            'education'         : education,
            'prior_treatment'   : prior_treatment,
            'psych_problem'     : psych_problem,
            'referral_source'   : referral_source,
            'arrests'           : arrests,
            'risk_score'        : risk_score,
            'risk_level'        : risk_level,
            'timestamp'         : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        new_row = pd.DataFrame([new_record])

        if os.path.exists(PATIENTS_FILE) and \
           os.path.getsize(PATIENTS_FILE) > 0:
            new_row.to_csv(PATIENTS_FILE, mode='a',
                           header=False, index=False)
        else:
            new_row.to_csv(PATIENTS_FILE, mode='w',
                           header=True, index=False)

        st.success(f"✅ Patient {final_id} saved successfully.")
        st.info(f"Risk Score: {risk_pct}% — {risk_level} Risk | "
                f"Saved at {new_record['timestamp']}")
```

---

## Step 6 — Run the App

In your terminal, navigate to the `oud_app` folder and run:
```
cd oud_app
streamlit run Home.py