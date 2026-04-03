import streamlit as st
import pandas as pd
import yfinance as yf
from engine import NFPEngine
from db import Database
from data_fetcher import fetch_latest_nfp
from utils import evaluate_signal_strength, compute_performance, suggest_trade

# ---------------- CONFIG ----------------
st.set_page_config(layout="wide", page_title="NFP Quant Dashboard")

engine = NFPEngine()
db = Database()

st.title("🚀 NFP QUANT TRADING DASHBOARD")
st.caption("Macro-driven trading system with real-time insights")

# ---------------- AUTO FETCH ----------------
st.subheader("🔄 Auto Fetch Latest NFP")

if st.button("Fetch Latest NFP"):
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

            st.success("✅ NFP stored and signal generated")
        else:
            st.info("ℹ️ NFP already exists in database")
    else:
        st.error("❌ Failed to fetch NFP data")

# ---------------- LATEST NFP DISPLAY ----------------
st.subheader("📊 Latest NFP Data")

nfp = fetch_latest_nfp()

if nfp:
    signal = engine.generate_signal(nfp["actual"], nfp["forecast"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Actual", nfp["actual"])
    col2.metric("Forecast", nfp["forecast"])
    col3.metric("Surprise", signal["surprise"])

    # Interpretation
    interpretation = engine.interpret_nfp(signal)

    st.markdown("### 🧠 Interpretation")
    st.info(interpretation)

    if signal["action"]:
        st.success(f"📈 Suggested Trade: {signal['action']} EURUSD")
    else:
        st.warning("⏸️ No Trade Recommended")

# ---------------- MAIN LAYOUT ----------------
col1, col2 = st.columns([1, 2])

# -------- LEFT PANEL --------
with col1:
    st.subheader("📊 Manual Signal Generator")

    actual = st.number_input("Actual NFP", value=50000)
    forecast = st.number_input("Forecast NFP", value=60000)

    if st.button("Generate Manual Signal"):
        signal = engine.generate_signal(actual, forecast)

        st.metric("Surprise", signal["surprise"])
        st.write(signal)

        strength = evaluate_signal_strength(signal)

        if strength == "HIGH_CONFIDENCE":
            st.success("🔥 HIGH CONFIDENCE TRADE")
        elif strength == "AVOID":
            st.error("⚠️ HIGH VOLATILITY - AVOID")
        else:
            st.warning("Normal Setup")

        # Live price
        df = yf.download("EURUSD=X", period="1d", interval="1m")

        if not df.empty:
            price = df["Close"].iloc[-1]
            trade = suggest_trade(price, signal)

            if trade:
                st.markdown("### 🎯 Trade Setup")
                st.write(trade)

# -------- RIGHT PANEL --------
with col2:
    st.subheader("📈 EURUSD Live Market")

    df = yf.download("EURUSD=X", period="1d", interval="1m")

    if not df.empty:
        st.line_chart(df["Close"])

# ---------------- HISTORY ----------------
st.subheader("📚 Historical NFP Data")

history = db.fetch_all()

if not history.empty:

    # Derived columns
    history["surprise"] = history["actual"] - history["forecast"]

    def classify(x):
        if x > 100000:
            return "VERY_STRONG"
        elif x >= 30000:
            return "MODERATE"
        elif x >= -30000:
            return "NEUTRAL"
        elif x >= -100000:
            return "WEAK"
        else:
            return "VERY_WEAK"

    history["category"] = history["surprise"].apply(classify)

    st.dataframe(history)

    # Category distribution
    st.markdown("### 📊 NFP Category Distribution")
    st.bar_chart(history["category"].value_counts())

# ---------------- STRATEGY INSIGHTS ----------------
st.subheader("🧠 Strategy Insights")

if not history.empty:
    bullish = history[history["action"] == "BUY"]
    bearish = history[history["action"] == "SELL"]

    col1, col2 = st.columns(2)

    col1.metric("BUY Signals", len(bullish))
    col2.metric("SELL Signals", len(bearish))

    best_cat = history["category"].value_counts().idxmax()
    st.info(f"Most frequent market condition: {best_cat}")

# ---------------- EDGE DETECTION ----------------
st.subheader("🔍 Edge Detection")

if not history.empty:
    grouped = history.groupby("category").size()

    st.write("Trades per category:")
    st.write(grouped)

    if "MODERATE" in grouped:
        st.success("✅ MODERATE NFP tends to give stable trade opportunities")

# ---------------- PERFORMANCE ----------------
st.subheader("📊 Strategy Performance")

if not history.empty:
    perf = compute_performance(history)

    if perf:
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Trades", perf.get("total_trades", 0))
        col2.metric("Win Rate", f"{perf.get('win_rate', 0)}%")
        col3.metric("Avg Win", perf.get("avg_win", 0))
