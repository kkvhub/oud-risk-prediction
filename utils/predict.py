# utils/predict.py
import json
import numpy as np
import pandas as pd
import os

# Cached loaded assets
_params = None
_model  = None

NOMINAL_COLS = ["EMPLOY","ETHNIC","LIVARAG","MARSTAT","PSOURCE",
                "RACE","REGION","SERVICES","STFIPS","PRIMPAY","PRIMINC"]
ORDINAL_COLS = ["ARRESTS","EDUC","FREQMAX","AGECAT","NUMSUBS"]
BINARY_COLS  = ["ALCFLG","MARFLG","INHFLG","NOPRIOR","PSYPROB",
                "VET","GENDER","NEEDLEUSE","STIMFLAG","TRNQFLAG",
                "SEDFLAG","HALFLAG","HEROIN"]

OPTIMAL_THRESHOLD = 0.35


def _get_base_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_assets():
    global _params, _model

    if _params is not None and _model is not None:
        return

    base_dir    = _get_base_dir()
    params_path = os.path.join(base_dir, "model", "preprocessor_params.json")
    model_path  = os.path.join(base_dir, "model", "final_nn.keras")

    if not os.path.exists(params_path):
        raise FileNotFoundError(
            "preprocessor_params.json not found at: " + params_path
        )
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            "final_nn.keras not found at: " + model_path
        )

    with open(params_path, "r") as f:
        _params = json.load(f)

    from tensorflow import keras
    _model = keras.models.load_model(model_path)


def _transform(patient_dict):
    """
    Manually apply preprocessing using stored JSON parameters.
    No pickle, no sklearn version dependency.
    """
    nominal_out = []
    for col in NOMINAL_COLS:
        val  = patient_dict.get(col, None)
        fill = _params["nominal_fill"][col]
        val  = fill if (val is None or (
                        isinstance(val, float) and np.isnan(val))
                        ) else val
        cats = _params["ohe_categories"][col]
        ohe  = [1.0 if (str(val) == str(c) or val == c) else 0.0
                for c in cats]
        nominal_out.extend(ohe)

    ordinal_out = []
    for col in ORDINAL_COLS:
        val  = patient_dict.get(col, None)
        fill = _params["ordinal_fill"][col]
        val  = fill if (val is None or (
                        isinstance(val, float) and np.isnan(val))
                        ) else val
        scaled = ((float(val) - _params["ordinal_mean"][col])
                  / _params["ordinal_std"][col])
        ordinal_out.append(scaled)

    binary_out = []
    for col in BINARY_COLS:
        val  = patient_dict.get(col, None)
        fill = _params["binary_fill"][col]
        val  = fill if (val is None or (
                        isinstance(val, float) and np.isnan(val))
                        ) else val
        binary_out.append(float(val))

    return np.array(nominal_out + ordinal_out + binary_out,
                    dtype=np.float32).reshape(1, -1)


def get_risk_level(score):
    if score >= 0.65:
        return "High"
    elif score >= 0.40:
        return "Moderate"
    else:
        return "Low"


def predict_risk(patient_dict):
    """
    Takes patient intake dictionary.
    Returns (risk_score float, risk_level string).
    """
    _load_assets()
    X_input = _transform(patient_dict)
    prob    = _model.predict(X_input, verbose=0).flatten()[0]
    return round(float(prob), 4), get_risk_level(float(prob))
