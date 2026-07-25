import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import time
import requests
from bs4 import BeautifulSoup

# ===== 1. PAGE SETUP - DARK PRO =====
st.set_page_config(page_title="Live Medicine AI Predictor PK", layout="wide", page_icon="💊")
st.markdown("""
<style>
  .stApp {background-color: #0E1117; color: white;}
    h1, h2, h3 {color: #00FF88!important;}
   .stButton>button {background-color: #00FF88; color: black;}
</style>
""", unsafe_allow_html=True)

st.title("💊 Live Medicine Price Predictor | Pakistan")
st.markdown("**Real-Time Scraping + Supervised ML** | Data updates every time you refresh")

# ===== 2. REAL-TIME SCRAPING FUNCTION =====
@st.cache_data(ttl=600) # 10 min tak cache rakhega taake bar block na ho
def get_live_data():
    st.info("Scraping live data from pharmacies... 10-15 seconds")

    medicines = ['Panadol 500mg', 'Losec 20mg', 'Insulin', 'Brufen 400mg', 'Augmentin']
    data = []

    # YAHAN APNA PURANA SCRAPING CODE LAGANA HAI
    # Example: Fake data bana raha hun. Tum yahan apna requests + BeautifulSoup wala code dalo
    for med in medicines:
        base_price = np.random.randint(100, 800)
        for i in range(15): # Pichle 15 din ka data
            date = datetime.now() - timedelta(days=15-i)
            price = base_price + np.random.randn()*15 + i*3
            data.append([med, date, price])

    df = pd.DataFrame(data, columns=['Medicine', 'Date', 'Price'])
    df['Day'] = (df['Date'] - df['Date'].min()).dt.days
    return df

# ===== 3. TRAIN MODEL ON LIVE DATA =====
df_live = get_live_data()

models = {}
for med in df_live['Medicine'].unique():
    df_med = df_live[df_live['Medicine'] == med]
    X = df_med[['Day']]
    y = df_med['Price']
    model = LinearRegression().fit(X, y)
    models[med] = model

# ===== 4. STREAMLIT UI =====
col1, col2 = st.columns([1,2])

with col1:
    medicine = st.selectbox("Select Medicine", list(models.keys()))
    if st.button("🔄 Refresh Live Data"):
        st.cache_data.clear()
        st.rerun()

with col2:
    st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))

# Prediction for next 7 days
model = models[medicine]
last_day = df_live[df_live['Medicine']==medicine]['Day'].max()
future_days = np.array([[last_day+i] for i in range(1,8)])
predictions = model.predict(future_days)

# Plot
fig = go.Figure()
hist_data = df_live[df_live['Medicine']==medicine]
fig.add_trace(go.Scatter(x=hist_data['Date'], y=hist_data['Price'],
                         mode='lines+markers', name='Live Historical', line=dict(color='#00FF88')))
fig.add_trace(go.Scatter(x=[datetime.now() + timedelta(days=i) for i in range(1,8)],
                         y=predictions, mode='lines+markers', name='ML Prediction 7 Days',
                         line=dict(color='#FF4444', dash='dash')))

fig.update_layout(template='plotly_dark', title=f"Real-Time Forecast for {medicine}", height=500)
st.plotly_chart(fig, use_container_width=True)

st.success(f"**AI Prediction for Tomorrow:** PKR {predictions[0]:.2f}")
st.caption("Disclaimer: Predictions based on last 15 days trend. For informational purpose only.")