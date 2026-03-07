# utils/sheets.py
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

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
    try:
        creds = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=SCOPES
        )
        service = build("sheets", "v4",
                        credentials=creds,
                        cache_discovery=False)
        return service
    except KeyError:
        raise KeyError(
            "gcp_service_account not found in Streamlit secrets. "
            "Go to App Settings → Secrets and add credentials."
        )
    except Exception as e:
        raise Exception(f"Failed to build Sheets service: {str(e)}")


def get_sheet_id():
    try:
        return st.secrets["sheets"]["sheet_id"]
    except KeyError:
        raise KeyError(
            "sheets.sheet_id not found in Streamlit secrets."
        )


def load_patients():
    try:
        service  = get_sheets_service()
        sheet_id = get_sheet_id()

        result = service.spreadsheets().values().get(
            spreadsheetId = sheet_id,
            range         = "Sheet1"
        ).execute()

        values = result.get("values", [])

        if not values or len(values) < 2:
            return pd.DataFrame(columns=COLUMNS)

        header = values[0]
        rows   = values[1:]
        rows   = [r + [""] * (len(header) - len(r)) for r in rows]
        df     = pd.DataFrame(rows, columns=header)
        return df

    except Exception as e:
        st.error(f"Could not load records: {str(e)}")
        return pd.DataFrame(columns=COLUMNS)


def save_patient(patient_dict):
    try:
        service  = get_sheets_service()
        sheet_id = get_sheet_id()

        # Check if header row exists
        result = service.spreadsheets().values().get(
            spreadsheetId = sheet_id,
            range         = "Sheet1!A1:A1"
        ).execute()

        existing = result.get("values", [])

        # Write header if sheet is empty
        if not existing:
            service.spreadsheets().values().append(
                spreadsheetId    = sheet_id,
                range            = "Sheet1",
                valueInputOption = "RAW",
                insertDataOption = "INSERT_ROWS",
                body             = {"values": [COLUMNS]}
            ).execute()

        # Build row in correct column order
        row = [str(patient_dict.get(col, "")) for col in COLUMNS]

        # Append patient row
        result = service.spreadsheets().values().append(
            spreadsheetId    = sheet_id,
            range            = "Sheet1",
            valueInputOption = "RAW",
            insertDataOption = "INSERT_ROWS",
            body             = {"values": [row]}
        ).execute()

        # Confirm rows were updated
        updates = result.get("updates", {})
        updated = updates.get("updatedRows", 0)

        if updated > 0:
            return True
        else:
            st.warning(
                "Sheets API responded but reported 0 rows updated. "
                "Check sheet permissions."
            )
            return False

    except Exception as e:
        st.error(f"Save error: {str(e)}")
        return False
