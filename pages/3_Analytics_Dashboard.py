# pages/3_Analytics_Dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title = "Analytics Dashboard",
    page_icon  = "📊",
    layout     = "wide"
)

st.title("📊 Executive Analytics Dashboard")
st.markdown("Population-level view of all enrolled patients and risk distribution.")
st.divider()

PATIENTS_FILE = 'data/patients.csv'

if not os.path.exists(PATIENTS_FILE) or    os.path.getsize(PATIENTS_FILE) == 0:
    st.warning("No patient records found. "
               "Add patients through the Intake page first.")
    st.stop()

df = pd.read_csv(PATIENTS_FILE)
if df.empty:
    st.warning("No patient records yet.")
    st.stop()

df['risk_score_pct'] = (df['risk_score'].astype(float) * 100).round(1)
df['admission_date'] = pd.to_datetime(df['admission_date'])

# ── KPI Cards ─────────────────────────────────────────────────
total    = len(df)
high     = len(df[df['risk_level'] == 'High'])
moderate = len(df[df['risk_level'] == 'Moderate'])
low      = len(df[df['risk_level'] == 'Low'])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Patients",    total)
col2.metric("🔴 High Risk",
            f"{high} ({int(high/total*100)}%)" if total else "0")
col3.metric("🟡 Moderate Risk",
            f"{moderate} ({int(moderate/total*100)}%)" if total else "0")
col4.metric("🟢 Low Risk",
            f"{low} ({int(low/total*100)}%)" if total else "0")

st.divider()

# ── Row 2: Risk Distribution + Admissions Trend ───────────────
col1, col2 = st.columns([6, 4])

with col1:
    fig_hist = px.histogram(
        df, x='risk_score_pct',
        nbins=20,
        title="Risk Score Distribution",
        labels={'risk_score_pct':'Risk Score (%)'},
        color_discrete_sequence=['#2c7bb6']
    )
    fig_hist.add_vrect(x0=0,  x1=40, fillcolor="green",
                       opacity=0.08, line_width=0)
    fig_hist.add_vrect(x0=40, x1=65, fillcolor="orange",
                       opacity=0.08, line_width=0)
    fig_hist.add_vrect(x0=65, x1=100, fillcolor="red",
                       opacity=0.08, line_width=0)
    fig_hist.update_layout(bargap=0.1)
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    risk_counts = df['risk_level'].value_counts().reset_index()
    risk_counts.columns = ['Risk Level', 'Count']
    color_map = {"High":"#d7191c",
                 "Moderate":"#fdae61",
                 "Low":"#1a9641"}
    fig_pie = px.pie(
        risk_counts,
        names  = 'Risk Level',
        values = 'Count',
        title  = "Risk Level Breakdown",
        color  = 'Risk Level',
        color_discrete_map = color_map
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Row 3: Demographic Breakdowns ─────────────────────────────
st.subheader("Risk by Patient Demographics")
col1, col2, col3 = st.columns(3)

with col1:
    age_risk = df.groupby('age_group')['risk_score_pct']                 .mean().reset_index()
    fig_age  = px.bar(
        age_risk, x='age_group', y='risk_score_pct',
        title  = "Avg Risk Score by Age Group",
        labels = {'risk_score_pct':'Avg Risk (%)',
                  'age_group':'Age Group'},
        color  = 'risk_score_pct',
        color_continuous_scale = 'RdYlGn_r'
    )
    st.plotly_chart(fig_age, use_container_width=True)

with col2:
    treat_risk = df.groupby('treatment_type')['risk_score_pct']                   .mean().reset_index()
    fig_treat  = px.bar(
        treat_risk, x='treatment_type', y='risk_score_pct',
        title  = "Avg Risk by Treatment Type",
        labels = {'risk_score_pct':'Avg Risk (%)',
                  'treatment_type':'Treatment'},
        color  = 'risk_score_pct',
        color_continuous_scale = 'RdYlGn_r'
    )
    fig_treat.update_xaxes(tickangle=30)
    st.plotly_chart(fig_treat, use_container_width=True)

with col3:
    emp_risk = df.groupby('employment')['risk_score_pct']                 .mean().reset_index()
    fig_emp  = px.bar(
        emp_risk, x='employment', y='risk_score_pct',
        title  = "Avg Risk by Employment",
        labels = {'risk_score_pct':'Avg Risk (%)',
                  'employment':'Employment'},
        color  = 'risk_score_pct',
        color_continuous_scale = 'RdYlGn_r'
    )
    fig_emp.update_xaxes(tickangle=30)
    st.plotly_chart(fig_emp, use_container_width=True)

# ── Row 4: Patient Table ───────────────────────────────────────
st.divider()
st.subheader("All Patient Records")

col1, col2, col3 = st.columns(3)
with col1:
    filter_risk = st.multiselect(
        "Filter by Risk Level",
        ["High","Moderate","Low"],
        default=["High","Moderate","Low"]
    )
with col2:
    filter_treat = st.multiselect(
        "Filter by Treatment Type",
        df['treatment_type'].unique().tolist(),
        default=df['treatment_type'].unique().tolist()
    )
with col3:
    filter_gender = st.multiselect(
        "Filter by Gender",
        df['gender'].unique().tolist(),
        default=df['gender'].unique().tolist()
    )

filtered = df[
    df['risk_level'].isin(filter_risk) &
    df['treatment_type'].isin(filter_treat) &
    df['gender'].isin(filter_gender)
]

display_cols = ['patient_id','admission_date','treatment_type',
                'age_group','gender','primary_substance',
                'employment','risk_score_pct','risk_level']

st.dataframe(
    filtered[display_cols].rename(columns={
        'patient_id'      :'Patient ID',
        'admission_date'  :'Admission',
        'treatment_type'  :'Treatment',
        'age_group'       :'Age Group',
        'gender'          :'Gender',
        'primary_substance':'Primary Drug',
        'employment'      :'Employment',
        'risk_score_pct'  :'Risk Score %',
        'risk_level'      :'Risk Level'
    }),
    use_container_width=True,
    height=400
)

# Export button
csv_data = filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label     = "📥 Export Table to CSV",
    data      = csv_data,
    file_name = "oud_patients_export.csv",
    mime      = "text/csv"
)

st.divider()
st.caption(
    "Dashboard reflects all patients saved through the Intake page. "
    "Model: Neural Network | Threshold: 0.35 | "
    "Trained on SAMHSA TEDS-D 2018 | For clinical decision support only."
)
