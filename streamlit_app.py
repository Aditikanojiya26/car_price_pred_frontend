import streamlit as st
import requests
from datetime import datetime
import joblib

API_URL = "https://car-price-prediction-tzd0.onrender.com/predict"  # Replace with your actual API endpoint

st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="🚗",
    layout="centered"
)

# ============================================================
# Styling — dashboard-cluster theme
# ============================================================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">

<style>
:root {
    --ink-navy: #10192E;
    --steel: #4B5563;
    --cloud: #F4F6F9;
    --amber: #F2A63C;
    --teal: #0E7C7B;
    --white: #FFFFFF;
}

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: var(--cloud);
}

/* Hide default Streamlit chrome for a cleaner look */
#MainMenu, footer, header {visibility: hidden;}

/* ---- Hero band ---- */
.hero {
    background: linear-gradient(135deg, var(--ink-navy) 0%, #1B2A4A 100%);
    border-radius: 18px;
    padding: 2.1rem 2rem 1.8rem 2rem;
    margin-bottom: 1.6rem;
    box-shadow: 0 10px 30px rgba(16, 25, 46, 0.25);
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: "";
    position: absolute;
    right: -40px;
    top: -40px;
    width: 160px;
    height: 160px;
    border-radius: 50%;
    border: 2px solid rgba(242, 166, 60, 0.18);
}
.hero::before {
    content: "";
    position: absolute;
    right: 10px;
    top: 10px;
    width: 100px;
    height: 100px;
    border-radius: 50%;
    border: 2px solid rgba(242, 166, 60, 0.12);
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--white);
    margin: 0;
    letter-spacing: -0.02em;
}
.hero-sub {
    color: #A9B4CC;
    font-size: 0.98rem;
    margin-top: 0.4rem;
    max-width: 34rem;
}
.hero-tag {
    display: inline-block;
    background: rgba(242, 166, 60, 0.15);
    color: var(--amber);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    padding: 0.25rem 0.6rem;
    border-radius: 6px;
    margin-bottom: 0.8rem;
    text-transform: uppercase;
}

/* ---- Section card ---- */
.section-card {
    background: var(--white);
    border-radius: 16px;
    padding: 1.6rem 1.7rem 0.6rem 1.7rem;
    margin-bottom: 1.3rem;
    box-shadow: 0 2px 14px rgba(16, 25, 46, 0.06);
    border: 1px solid rgba(16, 25, 46, 0.05);
}
.section-label {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 1.02rem;
    color: var(--ink-navy);
    margin-bottom: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label .num {
    font-family: 'JetBrains Mono', monospace;
    color: var(--amber);
    font-size: 0.85rem;
    background: rgba(242,166,60,0.12);
    padding: 0.1rem 0.5rem;
    border-radius: 5px;
}

/* ---- Inputs ---- */
div[data-testid="stSelectbox"] label, div[data-testid="stNumberInput"] label {
    color: var(--steel) !important;
    font-weight: 500;
    font-size: 0.88rem;
}
div[data-testid="stSelectbox"] > div > div, div[data-testid="stNumberInput"] input {
    border-radius: 9px !important;
}

/* ---- Button ---- */
.stButton > button {
    width: 100%;
    background: var(--amber);
    color: var(--ink-navy);
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.02rem;
    border: none;
    border-radius: 11px;
    padding: 0.75rem 0;
    box-shadow: 0 6px 18px rgba(242, 166, 60, 0.35);
    transition: transform 0.12s ease, box-shadow 0.12s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 22px rgba(242, 166, 60, 0.45);
    color: var(--ink-navy);
}

/* ---- Readout panel (signature element) ---- */
.readout {
    background: var(--ink-navy);
    border: 1px solid rgba(242, 166, 60, 0.35);
    border-radius: 16px;
    padding: 1.5rem 1.7rem;
    margin-top: 1.2rem;
    box-shadow: 0 0 0 1px rgba(242,166,60,0.08), 0 12px 28px rgba(16,25,46,0.3);
}
.readout-label {
    font-family: 'JetBrains Mono', monospace;
    color: #A9B4CC;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.readout-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.3rem;
    font-weight: 700;
    color: var(--amber);
    text-shadow: 0 0 18px rgba(242, 166, 60, 0.45);
    letter-spacing: 0.01em;
}
.readout-meta {
    color: #7C89A6;
    font-size: 0.82rem;
    margin-top: 0.5rem;
    font-family: 'Inter', sans-serif;
}

.footer-note {
    text-align: center;
    color: #9AA5B8;
    font-size: 0.8rem;
    margin-top: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# Hero
# ============================================================
st.markdown("""
<div class="hero">
    <div class="hero-tag">Valuation Engine</div>
    <p class="hero-title">🚗 Car Price Prediction</p>
    <p class="hero-sub">Enter your car's specs and get an instant, model-based
    market value estimate — like reading it straight off the dashboard.</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# Load reference data
# ============================================================
try:
    brands = joblib.load("artifacts/brands.pkl")
    car_mapping = joblib.load("artifacts/car_mapping.pkl")
except Exception as e:
    st.error(f"Could not load reference data (artifacts/brands.pkl or car_mapping.pkl): {e}")
    st.stop()

# ============================================================
# Section 1 — Identity
# ============================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label"><span class="num">01</span> Identity</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    brand = st.selectbox("Brand", brands)
with col2:
    car_names = car_mapping[brand]
    car_name = st.selectbox("Model", car_names)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# Section 2 — Condition & usage
# ============================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label"><span class="num">02</span> Condition &amp; usage</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    manufacture = st.number_input("Manufacturing year", min_value=1995, max_value=2025, value=2020)
    kms_driven = st.number_input("Kilometers driven", min_value=0, value=30000, step=1000)
    ownership = st.selectbox("Ownership (number of previous owners)", [1, 2, 3, 4])
with col2:
    fuel_type = st.selectbox("Fuel type", ["Petrol", "Diesel", "CNG", "Electric", "LPG"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# Section 3 — Specs
# ============================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label"><span class="num">03</span> Specifications</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    engine = st.number_input("Engine (CC)", min_value=500, max_value=6000, value=1200, step=50)
with col2:
    Seats = st.number_input("Seats", min_value=2, max_value=10, value=5)

st.markdown('</div>', unsafe_allow_html=True)

car_age = datetime.now().year - manufacture

# ============================================================
# Prediction
# ============================================================
if st.button("Predict price"):

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

    with st.spinner("Reading the gauges..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=15)

            if response.status_code == 200:
                prediction = response.json()["predicted_price"]
                st.markdown(f"""
                <div class="readout">
                    <div class="readout-label">Estimated market value</div>
                    <div class="readout-value">₹ {prediction:,.0f}</div>
                    <div class="readout-meta">{brand} {car_name} · {manufacture} · {kms_driven:,} km · {fuel_type} · {transmission}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"API error ({response.status_code}): {response.text}")

        except Exception as e:
            st.error(f"Connection error: {e}")

st.markdown('<div class="footer-note">Estimates are model-generated and may differ from actual sale price.</div>', unsafe_allow_html=True)