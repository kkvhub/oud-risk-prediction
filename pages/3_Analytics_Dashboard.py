# pages/3_Analytics_Dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.sheets import load_patients

st.set_page_config(page_title="Analytics Dashboard",
                   page_icon="📊", layout="wide")
st.title("📊 Executive Analytics Dashboard")
st.markdown("Population-level view of all enrolled patients.")
st.divider()

df = load_patients()

if df.empty:
    st.warning("No patient records yet. "
               "Add patients through the Intake page first.")
    st.stop()

df["risk_score_pct"] = (
    df["risk_score"].astype(float) * 100).round(1)
df["admission_date"] = pd.to_datetime(
    df["admission_date"], errors="coerce")

# KPI cards
total    = len(df)
high     = len(df[df["risk_level"]=="High"])
moderate = len(df[df["risk_level"]=="Moderate"])
low      = len(df[df["risk_level"]=="Low"])

col1,col2,col3,col4 = st.columns(4)
col1.metric("Total Patients", total)
col2.metric("🔴 High Risk",
            f"{high} ({int(high/total*100)}%)" if total else "0")
col3.metric("🟡 Moderate Risk",
            f"{moderate} ({int(moderate/total*100)}%)" if total else "0")
col4.metric("🟢 Low Risk",
            f"{low} ({int(low/total*100)}%)" if total else "0")
st.divider()

# Charts
col1, col2 = st.columns([6,4])
with col1:
    fig = px.histogram(df, x="risk_score_pct", nbins=20,
                       title="Risk Score Distribution",
                       color_discrete_sequence=["#2c7bb6"])
    fig.add_vrect(x0=0,  x1=40, fillcolor="green",
                  opacity=0.08, line_width=0)
    fig.add_vrect(x0=40, x1=65, fillcolor="orange",
                  opacity=0.08, line_width=0)
    fig.add_vrect(x0=65, x1=100, fillcolor="red",
                  opacity=0.08, line_width=0)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    counts = df["risk_level"].value_counts().reset_index()
    counts.columns = ["Risk Level","Count"]
    fig2 = px.pie(counts, names="Risk Level", values="Count",
                  title="Risk Level Breakdown",
                  color="Risk Level",
                  color_discrete_map={
                      "High":"#d7191c",
                      "Moderate":"#fdae61",
                      "Low":"#1a9641"})
    st.plotly_chart(fig2, use_container_width=True)

# Demographic breakdowns
st.subheader("Risk by Demographics")
col1,col2,col3 = st.columns(3)
for ax, col, title in [
    (col1, "age_group",      "Avg Risk by Age Group"),
    (col2, "treatment_type", "Avg Risk by Treatment"),
    (col3, "employment",     "Avg Risk by Employment"),
]:
    grp = df.groupby(col)["risk_score_pct"].mean().reset_index()
    fig = px.bar(grp, x=col, y="risk_score_pct",
                 title=title,
                 color="risk_score_pct",
                 color_continuous_scale="RdYlGn_r")
    fig.update_xaxes(tickangle=30)
    ax.plotly_chart(fig, use_container_width=True)

# Patient table
st.divider()
st.subheader("All Patient Records")
col1,col2,col3 = st.columns(3)
with col1:
    fr = st.multiselect("Risk Level",
         ["High","Moderate","Low"],
         default=["High","Moderate","Low"])
with col2:
    ft = st.multiselect("Treatment Type",
         df["treatment_type"].unique().tolist(),
         default=df["treatment_type"].unique().tolist())
with col3:
    fg = st.multiselect("Gender",
         df["gender"].unique().tolist(),
         default=df["gender"].unique().tolist())

filtered = df[
    df["risk_level"].isin(fr) &
    df["treatment_type"].isin(ft) &
    df["gender"].isin(fg)
]

show_cols = ["patient_id","admission_date","treatment_type",
             "age_group","gender","primary_substance",
             "employment","risk_score_pct","risk_level"]

st.dataframe(filtered[show_cols].rename(columns={
    "patient_id"       : "Patient ID",
    "admission_date"   : "Admission",
    "treatment_type"   : "Treatment",
    "age_group"        : "Age Group",
    "gender"           : "Gender",
    "primary_substance": "Primary Drug",
    "employment"       : "Employment",
    "risk_score_pct"   : "Risk Score %",
    "risk_level"       : "Risk Level"
}), use_container_width=True, height=400)

st.download_button(
    "📥 Export to CSV",
    filtered.to_csv(index=False).encode("utf-8"),
    "oud_patients_export.csv", "text/csv"
)

st.divider()
st.caption("Model: Neural Network | Threshold: 0.35 | "
           "SAMHSA TEDS-D 2018 | Clinical decision support only.")
