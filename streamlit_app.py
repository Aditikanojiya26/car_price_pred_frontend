import streamlit as st
import requests
from datetime import datetime
API_URL = "https://car-price-prediction-tzd0.onrender.com/predict"  # Replace with your actual API endpoint
import joblib

st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 Car Price Prediction")
st.write("Enter the car details below to estimate its price.")

# -----------------------------
# Inputs
# -----------------------------

brands = joblib.load(
    "artifacts/brands.pkl"
)

car_mapping = joblib.load(
    "artifacts/car_mapping.pkl"
)


brand = st.selectbox(
    "Select Brand",
    brands
)


car_names = car_mapping[brand]


car_name = st.selectbox(
    "Select Car Name",
    car_names
)

manufacture = st.number_input(
    "Manufacturing Year",
    min_value=1995,
    max_value=2025,
    value=2020
)

kms_driven = st.number_input(
    "Kilometers Driven",
    min_value=0,
    value=30000
)

fuel_type = st.selectbox(
    "Fuel Type",
    [
        "Petrol",
        "Diesel",
        "CNG",
        "Electric",
        "LPG"
    ]
)

transmission = st.selectbox(
    "Transmission",
    [
        "Manual",
        "Automatic"
    ]
)

ownership = st.selectbox(
    "Ownership",
    [1, 2, 3, 4]
)

engine = st.number_input(
    "Engine (CC)",
    min_value=500,
    max_value=6000,
    value=1200
)

Seats = st.number_input(
    "Seats",
    min_value=2,
    max_value=10,
    value=5
)
car_age = datetime.now().year - manufacture

# -----------------------------
# Prediction
# -----------------------------

if st.button("Predict Price"):

    payload = {
        "brand": brand,
        "car_name": car_name,
        "manufacture": manufacture,
        "kms_driven": kms_driven,
        "fuel_type": fuel_type,
        "transmission": transmission,
        "ownership": ownership,
        "engine": engine,
        "Seats": Seats,
        "car_age": car_age
    }


    try:

        response = requests.post(
            API_URL,
            json=payload
        )


        if response.status_code == 200:

            prediction = response.json()["predicted_price"]

            st.success(
                f"Estimated Price: ₹ {prediction:,.0f}"
            )

        else:

            st.error(
                f"API Error: {response.text}"
            )


    except Exception as e:

        st.error(
            f"Connection Error: {e}"
        )