import pandas as pd
import json

def load_notes(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def get_patient_ids(path: str) -> list:
    with open(path, 'r') as f:
        return json.load(f)