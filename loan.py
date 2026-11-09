from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import os


# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# =========================================================
# MODEL PATH
# =========================================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "loan_id.pkl"
)


# =========================================================
# ENCODER PATH
# =========================================================

ENCODER_PATH = os.path.join(
    BASE_DIR,
    "label_encoders.pkl"
)


print("Loading model from:")
print(MODEL_PATH)

print("Loading encoders from:")
print(ENCODER_PATH)


# =========================================================
# LOAD MODEL
# =========================================================

try:

    model = joblib.load(MODEL_PATH)

    print("Model loaded successfully:")
    print(model)

except Exception as e:

    print("Error loading model:")
    print(e)

    raise e


# =========================================================
# LOAD ENCODERS
# =========================================================

try:

    encoders = joblib.load(ENCODER_PATH)

    print("Encoders loaded successfully")

    print("Encoder columns:")
    print(encoders.keys())

except Exception as e:

    print("Error loading encoders:")
    print(e)

    raise e


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Loan Approval Prediction API",
    description="Loan approval prediction using Decision Tree",
    version="1.0"
)


# =========================================================
# INPUT MODEL
# =========================================================

class LoanInput(BaseModel):

    Gender: str

    Married: str

    Dependents: str

    Education: str

    Self_Employed: str

    ApplicantIncome: float

    CoapplicantIncome: float

    LoanAmount: float

    Loan_Amount_Term: float

    Credit_History: float

    Property_Area: str


# =========================================================
# HOME ROUTE
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Loan Approval API is running"
    }


# =========================================================
# PREPROCESS INPUT
# =========================================================

def preprocess_input(data: LoanInput):

    # -----------------------------------------------------
    # Create DataFrame using ORIGINAL values
    # -----------------------------------------------------

    input_data = pd.DataFrame([{

        "Gender": data.Gender,

        "Married": data.Married,

        "Dependents": data.Dependents,

        "Education": data.Education,

        "Self_Employed": data.Self_Employed,

        "ApplicantIncome": data.ApplicantIncome,

        "CoapplicantIncome": data.CoapplicantIncome,

        "LoanAmount": data.LoanAmount,

        "Loan_Amount_Term": data.Loan_Amount_Term,

        "Credit_History": data.Credit_History,

        "Property_Area": data.Property_Area

    }])


    # -----------------------------------------------------
    # CATEGORICAL COLUMNS
    # -----------------------------------------------------

    categorical_columns = [

        "Gender",

        "Married",

        "Dependents",

        "Education",

        "Self_Employed",

        "Property_Area"

    ]


    # -----------------------------------------------------
    # ENCODE CATEGORICAL VALUES
    # -----------------------------------------------------

    for col in categorical_columns:

        if col not in encoders:

            raise ValueError(
                f"Encoder not found for column: {col}"
            )

        le = encoders[col]

        try:

            input_data[col] = le.transform(
                input_data[col].astype(str)
            )

        except ValueError:

            raise ValueError(
                f"Invalid value '{input_data[col].iloc[0]}' "
                f"for column '{col}'. "
                f"Allowed values: {list(le.classes_)}"
            )


    # -----------------------------------------------------
    # DISPLAY ENCODED DATA
    # -----------------------------------------------------

    print("\nINPUT AFTER ENCODING:")
    print(input_data)

    print("\nDTYPES:")
    print(input_data.dtypes)


    return input_data


# =========================================================
# PREDICT ROUTE
# =========================================================

@app.post("/predict")
def predict(data: LoanInput):

    try:

        # -------------------------------------------------
        # PREPROCESS
        # -------------------------------------------------

        input_data = preprocess_input(data)


        # -------------------------------------------------
        # MODEL PREDICTION
        # -------------------------------------------------

        prediction = model.predict(input_data)[0]


        print("\nPREDICTION:")
        print(prediction)


        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return {

            "prediction": str(prediction)

        }


    except Exception as e:

        print("\nERROR:")
        print(e)

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )