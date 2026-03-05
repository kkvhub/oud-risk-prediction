# utils/sheets.py
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Column order must match patients.csv header exactly
COLUMNS = [
    "patient_id", "admission_date", "treatment_type",
    "age_group", "gender", "race", "state", "veteran",
    "primary_substance", "frequency", "needle_use",
    "num_substances", "stimulant", "tranquilizer",
    "sedative", "hallucinogen", "heroin", "employment",
    "living_arrangement", "marital_status", "education",
    "prior_treatment", "psych_problem", "referral_source",
    "arrests", "risk_score", "risk_level", "timestamp"
]

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


def get_sheets_service():
    """
    Build and return authenticated Google Sheets service.
    Credentials come from Streamlit secrets manager.
    """
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    service = build("sheets", "v4", credentials=creds)
    return service


def get_sheet_id():
    return st.secrets["sheets"]["sheet_id"]


def load_patients():
    """
    Load all patient records from Google Sheet.
    Returns a pandas DataFrame.
    Returns empty DataFrame if sheet is empty.
    """
    try:
        service  = get_sheets_service()
        sheet_id = get_sheet_id()

        result = service.spreadsheets().values().get(
            spreadsheetId = sheet_id,
            range         = "Sheet1"
        ).execute()

        values = result.get("values", [])

        if not values or len(values) < 2:
            # Sheet is empty or only has header
            return pd.DataFrame(columns=COLUMNS)

        # First row is header
        header = values[0]
        rows   = values[1:]

        # Pad short rows to match header length
        rows = [r + [""] * (len(header) - len(r)) for r in rows]

        df = pd.DataFrame(rows, columns=header)
        return df

    except Exception as e:
        st.error(f"Could not load patient records: {e}")
        return pd.DataFrame(columns=COLUMNS)


def save_patient(patient_dict):
    """
    Append one patient record to Google Sheet.
    If sheet is empty, writes header row first.
    """
    try:
        service  = get_sheets_service()
        sheet_id = get_sheet_id()

        # Check if header exists
        result = service.spreadsheets().values().get(
            spreadsheetId = sheet_id,
            range         = "Sheet1!A1:A1"
        ).execute()

        existing = result.get("values", [])

        # Write header if sheet is empty
        if not existing:
            service.spreadsheets().values().append(
                spreadsheetId          = sheet_id,
                range                  = "Sheet1",
                valueInputOption       = "RAW",
                insertDataOption       = "INSERT_ROWS",
                body                   = {"values": [COLUMNS]}
            ).execute()

        # Build row in correct column order
        row = [str(patient_dict.get(col, "")) for col in COLUMNS]

        # Append patient row
        service.spreadsheets().values().append(
            spreadsheetId          = sheet_id,
            range                  = "Sheet1",
            valueInputOption       = "RAW",
            insertDataOption       = "INSERT_ROWS",
            body                   = {"values": [row]}
        ).execute()

        return True

    except Exception as e:
        st.error(f"Could not save patient record: {e}")
        return False
