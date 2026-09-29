from __future__ import annotations

import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/")
st.set_page_config(page_title="RL Pricing Optimizer", page_icon="🧠", layout="wide")
st.title("🧠 RL Dynamic Pricing Optimizer")
st.caption("DQN-based pricing recommendations in a simulated retail environment.")

with st.sidebar:
    st.header("Product context")
    unit_cost = st.number_input("Unit cost", min_value=1.0, max_value=10000.0, value=25.0, step=1.0)
    current_price = st.number_input("Current price", min_value=1.0, max_value=10000.0, value=40.0, step=1.0)
    competitor_price = st.number_input("Competitor price", min_value=1.0, max_value=10000.0, value=39.0, step=1.0)
    demand_index = st.slider("Demand index", min_value=0.2, max_value=2.0, value=1.0, step=0.05)
    inventory = st.number_input("Inventory units", min_value=0, max_value=1000000, value=120, step=10)
    max_change = st.slider("Maximum price change (%)", min_value=5, max_value=30, value=20)

if current_price < unit_cost:
    st.warning("Current price is below unit cost. Increase the current price before requesting a recommendation.")
else:
    if st.button("Recommend price", type="primary"):
        payload = {
            "unit_cost": unit_cost,
            "current_price": current_price,
            "competitor_price": competitor_price,
            "demand_index": demand_index,
            "inventory": int(inventory),
            "max_price_change_pct": max_change,
        }
        try:
            response = requests.post(f"{API_URL}/recommend", json=payload, timeout=20)
            if response.ok:
                result = response.json()
                a, b, c = st.columns(3)
                a.metric("Recommended price", f"{result['recommended_price']:.2f}")
                b.metric("Estimated units sold", result["estimated_units_sold"])
                c.metric("Estimated simulated profit", f"{result['estimated_profit']:.2f}")
                st.subheader("Recommendation details")
                st.json(result)
                st.info(result["disclaimer"])
            else:
                st.error(f"API returned {response.status_code}: {response.text}")
        except requests.RequestException as exc:
            st.error(f"Could not connect to API at {API_URL}. Check that the API service is running. Details: {exc}")

st.divider()
st.subheader("How to interpret this demo")
st.markdown("""
- **Agent:** chooses among five bounded price actions using a trained DQN policy.
- **Reward:** simulated gross profit minus stockout and price-change penalties.
- **Important:** the demand model is synthetic. This dashboard is a portfolio demonstration, not a validated production pricing engine.
""")
with st.expander("API health"):
    try:
        health = requests.get(f"{API_URL}/health", timeout=5)
        st.json(health.json())
    except requests.RequestException:
        st.warning("API health endpoint is unreachable.")
