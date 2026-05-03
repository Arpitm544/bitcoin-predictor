import streamlit as st
import requests
import pandas as pd
import numpy as np

st.title("BTC Next Hour Prediction")

# Fetch latest data
url = "https://data-api.binance.vision/api/v3/klines"
params = {"symbol": "BTCUSDT", "interval": "1h", "limit": 500}
data = requests.get(url, params=params).json()

df = pd.DataFrame(data, columns=[
    "time","open","high","low","close","volume",
    "close_time","qav","trades","taker_base","taker_quote","ignore"
])

df["close"] = df["close"].astype(float)

# Returns
df["returns"] = np.log(df["close"] / df["close"].shift(1))
df = df.dropna()

# Prediction function
def predict_range(returns, last_price):
    mu = returns.mean()
    sigma = returns.std()

    sims = []
    for _ in range(10000):
        shock = np.random.standard_t(df=5)
        sim_return = mu + sigma * shock
        sims.append(last_price * np.exp(sim_return))

    return np.percentile(sims, 2.5), np.percentile(sims, 97.5)

lower, upper = predict_range(df["returns"], df["close"].iloc[-1])

# Display
st.metric("Current BTC Price", df["close"].iloc[-1])
st.metric("Predicted Range", f"{lower:.2f} - {upper:.2f}")

st.line_chart(df["close"].tail(50))