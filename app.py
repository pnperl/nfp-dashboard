import streamlit as st
import pandas as pd
from engine import NFPEngine
from backtester import NFPBacktester
from db import Database
from data_fetcher import fetch_nfp_data
from optimizer import StrategyOptimizer
import yfinance as yf

st.set_page_config(layout="wide")
st.title("🚀 NFP PRO TRADING DASHBOARD")

engine = NFPEngine()
db = Database()

tab1, tab2, tab3, tab4 = st.tabs(
    ["Live Signal", "Backtest", "Live Market", "Optimization"]
)

# ---------------- LIVE SIGNAL ----------------
with tab1:
    actual = st.number_input("Actual", value=50000)
    forecast = st.number_input("Forecast", value=60000)

    if st.button("Generate Signal"):
        signal = engine.generate_signal(actual, forecast)

        st.write(signal)

        if signal["action"]:
            st.success(f"{signal['action']} EURUSD")
        else:
            st.warning("No Trade")

        db.insert_signal({
            "date": str(pd.Timestamp.now()),
            "actual": actual,
            "forecast": forecast,
            "surprise": signal["surprise"],
            "action": signal["action"]
        })
history = db.fetch_all()

if not history.empty:
    st.dataframe(history)
# ---------------- BACKTEST ----------------
with tab2:
    file = st.file_uploader("Upload Data", type=["csv"])

    if file:
        data = pd.read_csv(file)
        bt = NFPBacktester(engine)
        metrics = bt.run_backtest(data)

        st.write(metrics)

        if "results_df" in metrics:
            st.line_chart(metrics["results_df"]["equity"])

# ---------------- LIVE MARKET ----------------
with tab3:
    st.subheader("EURUSD Live Chart")

    df = yf.download("EURUSD=X", period="1d", interval="1m")

    if not df.empty:
        st.line_chart(df["Close"])

# ---------------- OPTIMIZATION ----------------
with tab4:
    st.subheader("Strategy Optimization")

    file = st.file_uploader("Upload Data for Optimization", type=["csv"], key="opt")

    if file:
        data = pd.read_csv(file)

        bt = NFPBacktester(engine)
        optimizer = StrategyOptimizer(engine, bt)

        params, result = optimizer.optimize(data)

        st.write("Best Params:", params)
        st.write("Best Result:", result)
