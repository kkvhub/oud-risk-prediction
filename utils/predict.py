# utils/predict.py
import joblib
import numpy as np
import pandas as pd
from tensorflow import keras

# Load model assets once when app starts
preprocessor     = joblib.load('model/preprocessor.pkl')
model            = keras.models.load_model('model/final_nn.keras')
optimal_threshold = 0.35   # your Neural Network optimal threshold

# These must match exactly what your model was trained on
NOMINAL_COLS = ['EMPLOY','ETHNIC','LIVARAG','MARSTAT','PSOURCE',
                'RACE','REGION','SERVICES','STFIPS','PRIMPAY','PRIMINC']
ORDINAL_COLS = ['ARRESTS','EDUC','FREQMAX','AGECAT','NUMSUBS']
BINARY_COLS  = ['ALCFLG','MARFLG','INHFLG','NOPRIOR','PSYPROB',
                'VET','GENDER','NEEDLEUSE','STIMFLAG','TRNQFLAG',
                'SEDFLAG','HALFLAG','HEROIN']

def get_risk_level(score):
    if score >= 0.65:
        return 'High'
    elif score >= 0.40:
        return 'Moderate'
    else:
        return 'Low'

def predict_risk(patient_dict):
    """
    Takes a dictionary of raw patient intake values,
    runs through preprocessor and model,
    returns risk score (float) and risk level (string)
    """
    # Convert to dataframe with one row
    input_df = pd.DataFrame([patient_dict])

    # Run through the same preprocessor used in training
    input_processed = preprocessor.transform(input_df)

    # Get probability from Neural Network
    prob = model.predict(input_processed, verbose=0).flatten()[0]

    risk_level = get_risk_level(prob)

    return round(float(prob), 4), risk_level