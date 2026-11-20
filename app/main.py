import os
from pathlib import Path
import joblib
from dotenv import load_dotenv

import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel

# Get project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Read model path
MODEL_PATH = Path(
    os.getenv(
        "MODEL_PATH",
        "model/customer_churn_model.pkl"
    )
)

# Resolve relative paths from project root
if not MODEL_PATH.is_absolute():
    MODEL_PATH = BASE_DIR / MODEL_PATH

# Load trained ML model
model = joblib.load(MODEL_PATH)


app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predict customer churn using Machine Learning",
    version="1.0"
)

class Customer(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


@app.get("/")
def home():
    return {"message": "Customer Churn Prediction API is running"}


@app.post("/predict")
def predict_churn(customer: Customer):

    customer_data = pd.DataFrame([customer.model_dump()])

    prediction = model.predict(customer_data)[0]
    probability = model.predict_proba(customer_data)[0][1]

    return {
        "prediction": int(prediction),
        "churn_status": (
            "Likely to Churn" if prediction == 1
            else "Unlikely to Churn"
        ),
        "churn_probability": round(float(probability), 4)
    }