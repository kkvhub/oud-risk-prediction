# utils/predict.py
import joblib
import numpy as np
import pandas as pd
import os

# These are loaded lazily — only when first prediction is made
_preprocessor = None
_model        = None

# Column definitions — must match training exactly
NOMINAL_COLS = ["EMPLOY","ETHNIC","LIVARAG","MARSTAT","PSOURCE",
                "RACE","REGION","SERVICES","STFIPS","PRIMPAY","PRIMINC"]
ORDINAL_COLS = ["ARRESTS","EDUC","FREQMAX","AGECAT","NUMSUBS"]
BINARY_COLS  = ["ALCFLG","MARFLG","INHFLG","NOPRIOR","PSYPROB",
                "VET","GENDER","NEEDLEUSE","STIMFLAG","TRNQFLAG",
                "SEDFLAG","HALFLAG","HEROIN"]

OPTIMAL_THRESHOLD = 0.35


def _load_models():
    """
    Load models once and cache them.
    Called only when first prediction is requested.
    """
    global _preprocessor, _model

    if _preprocessor is not None and _model is not None:
        return  # Already loaded

    # Get base directory — works both locally and on Streamlit Cloud
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    preprocessor_path = os.path.join(base_dir, "model", "preprocessor.pkl")
    model_path        = os.path.join(base_dir, "model", "final_nn.keras")

    # Validate files exist before loading
    if not os.path.exists(preprocessor_path):
        raise FileNotFoundError(
            f"preprocessor.pkl not found at: {preprocessor_path}"
        )
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"final_nn.keras not found at: {model_path}"
        )

    _preprocessor = joblib.load(preprocessor_path)

    # Import tensorflow only when needed
    from tensorflow import keras
    _model = keras.models.load_model(model_path)


def get_risk_level(score):
    if score >= 0.65:
        return "High"
    elif score >= 0.40:
        return "Moderate"
    else:
        return "Low"


def predict_risk(patient_dict):
    """
    Takes a dictionary of raw patient intake values.
    Returns risk score (float 0-1) and risk level (string).
    """
    # Load models if not already loaded
    _load_models()

    # Build single-row dataframe
    input_df = pd.DataFrame([patient_dict])

    # Ensure all expected columns are present
    all_cols = NOMINAL_COLS + ORDINAL_COLS + BINARY_COLS
    for col in all_cols:
        if col not in input_df.columns:
            input_df[col] = 0

    # Reorder to match training column order
    input_df = input_df[all_cols]

    # Preprocess
    input_processed = _preprocessor.transform(input_df)

    # Predict
    import numpy as np
    prob = _model.predict(
        np.array(input_processed, dtype=np.float32),
        verbose=0
    ).flatten()[0]

    risk_level = get_risk_level(float(prob))

    return round(float(prob), 4), risk_level
