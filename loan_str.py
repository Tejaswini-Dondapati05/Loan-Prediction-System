import streamlit as st
import requests


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Loan Approval Prediction",
    page_icon="🏦",
    layout="centered"
)


# =========================
# TITLE
# =========================

st.title("🏦 Loan Approval Prediction")
st.write("Enter the applicant details below.")


# =========================
# INPUTS
# =========================

Gender = st.selectbox(
    "Gender",
    ["Male", "Female"]
)

Married = st.selectbox(
    "Married",
    ["Yes", "No"]
)

Dependents = st.selectbox(
    "Dependents",
    ["0", "1", "2", "3+"]
)

Education = st.selectbox(
    "Education",
    ["Graduate", "Not Graduate"]
)

Self_Employed = st.selectbox(
    "Self Employed",
    ["Yes", "No"]
)

ApplicantIncome = st.number_input(
    "Applicant Income",
    min_value=0.0,
    value=5000.0
)

CoapplicantIncome = st.number_input(
    "Coapplicant Income",
    min_value=0.0,
    value=2000.0
)

LoanAmount = st.number_input(
    "Loan Amount",
    min_value=0.0,
    value=150.0
)

Loan_Amount_Term = st.number_input(
    "Loan Amount Term",
    min_value=0.0,
    value=360.0
)

Credit_History = st.selectbox(
    "Credit History",
    [1.0, 0.0]
)

Property_Area = st.selectbox(
    "Property Area",
    ["Urban", "Semiurban", "Rural"]
)


# =========================
# PREDICT BUTTON
# =========================

if st.button("Predict Loan Status"):

    data = {
        "Gender": Gender,
        "Married": Married,
        "Dependents": Dependents,
        "Education": Education,
        "Self_Employed": Self_Employed,
        "ApplicantIncome": ApplicantIncome,
        "CoapplicantIncome": CoapplicantIncome,
        "LoanAmount": LoanAmount,
        "Loan_Amount_Term": Loan_Amount_Term,
        "Credit_History": Credit_History,
        "Property_Area": Property_Area
    }

    try:

        # Send data to FastAPI
        response = requests.post(
            "http://127.0.0.1:8051/predict",
            json=data
        )

        # Check response
        if response.status_code == 200:

            result = response.json()

            prediction = result["prediction"]

            st.success(
                f"Prediction: {prediction}"
            )

        else:

            st.error(
                f"API Error: {response.status_code}"
            )

            st.write(response.text)

    except requests.exceptions.ConnectionError:

        st.error(
            "FastAPI is not running. "
            "Please start FastAPI first."
        )

    except Exception as e:

        st.error(
            f"Error: {e}"
        )