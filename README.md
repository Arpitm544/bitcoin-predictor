# Bitcoin Next Hour Predictor

A simple Streamlit application that predicts the price range of Bitcoin (BTC) for the next hour using historical data from Binance and a Monte Carlo simulation based on T-distribution shocks.

## Features
- Fetches real-time BTC/USDT hourly data from Binance API.
- Calculates logarithmic returns.
- Predicts the 95% confidence interval for the next hour's price using 10,000 simulations.
- Visualizes the recent price trend with an interactive line chart.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Arpitm544/bitcoin-predictor.git
   cd bitcoin-predictor
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

## Dependencies
- `streamlit`
- `pandas`
- `numpy`
- `requests`
