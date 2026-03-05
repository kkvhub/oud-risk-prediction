# OUD Treatment Dropout Risk Prediction System

A clinical decision support web application that predicts
the risk of treatment dropout for patients enrolled in
Opioid Use Disorder (OUD) treatment programs.

Built as part of MIS548 — Deep Learning | University of Arizona

---

## Live App

Launch App: https://kkvhub-oud-risk-prediction.streamlit.app

---

## What This App Does

### Patient Intake
- Clinician enters patient details at admission
- Machine learning model scores dropout risk instantly
- Risk displayed as Low / Moderate / High with recommended actions
- Every patient saved to a single structured CSV file

### Patient Report
- Select any saved patient
- Generate a downloadable PDF risk assessment report
- Includes risk score, key risk factors, protective factors,
  and recommended clinical actions

### Executive Dashboard
- Population-level view of all enrolled patients
- KPI cards, risk distribution charts, demographic breakdowns
- Filterable patient table with CSV export

---

## Model Details

| Item | Detail |
|------|--------|
| Algorithm | Neural Network (TensorFlow / Keras) |
| Dataset | SAMHSA TEDS-D 2018 — 95,432 treatment episodes |
| AUC-ROC | 0.7187 |
| Recall | 92.0% at decision threshold 0.35 |
| Features | 27 patient intake characteristics |
| Class balancing | SMOTE |
| Hyperparameter tuning | GridSearchCV — 3-fold cross validation |

---

## Project Structure

    oud_app/
    |-- Home.py                         Landing page and navigation
    |-- requirements.txt                Python dependencies
    |-- pages/
    |   |-- 1_Patient_Intake.py         Intake form and risk scoring
    |   |-- 2_Patient_Report.py         PDF report generator
    |   +-- 3_Analytics_Dashboard.py   Executive analytics dashboard
    |-- model/
    |   |-- final_nn.keras              Trained Neural Network model
    |   |-- preprocessor.pkl            Fitted preprocessing pipeline
    |   +-- optimal_thresholds.pkl     Tuned decision thresholds
    |-- data/
    |   +-- patients.csv               All saved patient records
    +-- utils/
        +-- predict.py                 Prediction utility functions

---

## How to Run Locally

    git clone https://github.com/kkvhub/oud-risk-prediction.git
    cd oud-risk-prediction
    pip install -r requirements.txt
    streamlit run Home.py

---

## Clinical Disclaimer

This tool is intended for clinical decision support only.
It does not replace professional clinical judgment.
Model trained on 2018 administrative intake data.
Performance should be validated before any clinical deployment.

---

## Dataset Source

SAMHSA Treatment Episode Data Set Discharges — TEDS-D 2018
Substance Abuse and Mental Health Services Administration
https://www.samhsa.gov/data/
