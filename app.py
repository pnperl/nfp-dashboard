import streamlit as st
import pandas as pd
import yfinance as yf
from engine import NFPEngine
from db import Database
from data_fetcher import fetch_latest_nfp
from utils import evaluate_signal_strength, compute_performance, suggest_trade

st.set_page_config(layout="wide", page_title="NFP Quant Dashboard")

engine = NFPEngine()
db = Database()

st.title("🚀 NFP QUANT TRADING DASHBOARD")

# -------- AUTO FETCH --------
if st.button("🔄 Fetch Latest NFP"):
    nfp = fetch_latest_nfp()

    if nfp:
        if not db.exists(nfp["date"]):
            signal = engine.generate_signal(nfp["actual"], nfp["forecast"])

            db.insert_signal({
                "date": nfp["date"],
                "actual": nfp["actual"],
                "forecast": nfp["forecast"],
                "surprise": signal["surprise"],
                "action": signal["action"]
            })

            st.success("NFP stored + signal generated")
        else:
            st.info("Already exists")

# -------- LAYOUT --------
col1, col2 = st.columns([1, 2])

# -------- SIGNAL PANEL --------
with col1:
    st.subheader("📊 Manual Input")

    actual = st.number_input("Actual", value=50000)
    forecast = st.number_input("Forecast", value=60000)

    if st.button("Generate Signal"):
        signal = engine.generate_signal(actual, forecast)

        st.metric("Surprise", signal["surprise"])
        st.write(signal)

        strength = evaluate_signal_strength(signal)

        if strength == "HIGH_CONFIDENCE":
            st.success("🔥 HIGH CONFIDENCE TRADE")
        elif strength == "AVOID":
            st.error("⚠️ HIGH VOLATILITY")
        else:
            st.warning("Normal Setup")

        df = yf.download("EURUSD=X", period="1d", interval="1m")

        if not df.empty:
            price = df["Close"].iloc[-1]
            trade = suggest_trade(price, signal)

            if trade:
                st.markdown("### 🎯 Trade Setup")
                st.write(trade)

# -------- LIVE MARKET --------
with col2:
    st.subheader("📈 EURUSD Live")

    df = yf.download("EURUSD=X", period="1d", interval="1m")

    if not df.empty:
        st.line_chart(df["Close"])

# -------- HISTORY --------
st.subheader("📚 Trade History")

history = db.fetch_all()

if not history.empty:
    st.dataframe(history)

    perf = compute_performance(history)

    if perf:
        col1, col2, col3 = st.columns(3)

        col1.metric("Trades", perf["total_trades"])
        col2.metric("Win Rate", f"{perf['win_rate']}%")
        col3.metric("Avg Win", perf["avg_win"])
