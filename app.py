from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import re

app = FastAPI()

# Cleaning functions
def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip().lower()

def fill_missing_values(df):
    return df.fillna("unknown")

def standardize_diagnosis(df):
    condition_map = {
        "flu": "influenza",
        "influenza": "influenza",
        "cold": "common cold",
        "obesity": "obesity",
        "cancer": "cancer",
        "diabetes": "diabetes"
    }
    df["Medical Condition"] = df["Medical Condition"].str.lower().map(condition_map).fillna(df["Medical Condition"])
    return df

def clean_dataframe(df):
    for col in ["Name", "Medical Condition", "Medication"]:
        df[col] = df[col].apply(clean_text)
    df = fill_missing_values(df)
    df = standardize_diagnosis(df)
    return df

# Request body here
class HealthRecord(BaseModel):
    Name: str
    Medical_Condition: str
    Medication: str

@app.post("/clean-record")
def clean_record(record: HealthRecord):
    input_df = pd.DataFrame([{
        "Name": record.Name,
        "Medical Condition": record.Medical_Condition,
        "Medication": record.Medication
    }])
    cleaned = clean_dataframe(input_df)
    return cleaned.to_dict(orient="records")[0]
