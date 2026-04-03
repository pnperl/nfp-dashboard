import streamlit as st
import pandas as pd
from engine import NFPEngine
from backtester import NFPBacktester
from storage import DriveStorage

st.set_page_config(layout="wide")

st.title("📊 NFP Trading Dashboard")

engine = NFPEngine()
storage = DriveStorage()

tab1, tab2, tab3 = st.tabs(["Live Signal", "Backtest", "History"])

# ---------------- LIVE SIGNAL ----------------
with tab1:
    st.header("Live NFP Signal")

    actual = st.number_input("Actual", value=50000)
    forecast = st.number_input("Forecast", value=60000)

    if st.button("Generate Signal"):
        signal = engine.generate_signal(actual, forecast)

        st.metric("Surprise", signal["surprise"])
        st.write(signal)

        # ✅ Dashboard Alert System
        if signal["action"]:
            st.success(f"🚀 TRADE ALERT: {signal['action']} {signal['pair']}")
        elif signal["bias"] == "HIGH_VOLATILITY":
            st.error("⚠️ HIGH VOLATILITY — AVOID TRADE")
        else:
            st.warning("⏸️ NO TRADE ZONE")

        # Save to history
        df = pd.DataFrame([{
            "actual": actual,
            "forecast": forecast,
            "surprise": signal["surprise"],
            "action": signal["action"]
        }])

        storage.save(df)

# ---------------- BACKTEST ----------------
with tab2:
    st.header("Backtest")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        data = pd.read_csv(file)

        bt = NFPBacktester(engine)
        metrics = bt.run_backtest(data)

        st.write(metrics)

        if "results_df" in metrics:
            st.line_chart(metrics["results_df"]["equity"])

            # Save results
            storage.save(metrics["results_df"])

# ---------------- HISTORY ----------------
with tab3:
    st.header("Stored Historical Data")

    history = storage.load()

    if not history.empty:
        st.dataframe(history)
    else:
        st.info("No data stored yet")
