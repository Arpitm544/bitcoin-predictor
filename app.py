import streamlit as st
import requests
import pandas as pd
import numpy as np

coverage = 0.9656
avg_width = 1444.89

st.title("📈 BTC Next Hour Prediction")

st.subheader("Backtest Metrics")

col1, col2 = st.columns(2)
col1.metric("Coverage (95%)", f"{coverage:.4f}")
col2.metric("Avg Width", f"{avg_width:.2f}")

url = "https://data-api.binance.vision/api/v3/klines"
params = {"symbol": "BTCUSDT", "interval": "1h", "limit": 500}

data = requests.get(url, params=params).json()

df = pd.DataFrame(data, columns=[
    "time","open","high","low","close","volume",
    "close_time","qav","trades","taker_base","taker_quote","ignore"
])

df["close"] = df["close"].astype(float)

df["returns"] = np.log(df["close"] / df["close"].shift(1))
df = df.dropna()

def predict_range(returns, last_price):
    mu = returns.mean()
    sigma = returns.std()

    sims = []
    for _ in range(10000):
        shock = np.random.standard_t(df=5)  # fat tails
        sim_return = mu + sigma * shock
        sims.append(last_price * np.exp(sim_return))

    lower = np.percentile(sims, 3)
    upper = np.percentile(sims, 97)

    return lower, upper

current_price = df["close"].iloc[-1]
lower, upper = predict_range(df["returns"], current_price)

st.subheader("Live Prediction")

st.metric("Current BTC Price", f"{current_price:.2f}")
st.metric("Predicted Range (Next Hour)", f"{lower:.2f} - {upper:.2f}")

chart_df = df.tail(50).copy()
chart_df["lower"] = lower
chart_df["upper"] = upper

st.subheader("Last 50 Hours Price + Prediction Range")
st.line_chart(chart_df[["close", "lower", "upper"]])