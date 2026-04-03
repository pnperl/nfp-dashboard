import streamlit as st
import pandas as pd
import yfinance as yf
from engine import NFPEngine
from db import Database
from data_fetcher import fetch_latest_nfp
from utils import evaluate_signal_strength

st.set_page_config(layout="wide")
engine = NFPEngine()
db = Database()

st.title("NFP Dashboard")

if st.button("Fetch NFP"):
    nfp = fetch_latest_nfp()
    if nfp and not db.exists(nfp["date"]):
        signal = engine.generate_signal(nfp["actual"], nfp["forecast"])
        db.insert_signal({
            "date": nfp["date"],
            "actual": nfp["actual"],
            "forecast": nfp["forecast"],
            "surprise": signal["surprise"],
            "action": signal["action"]
        })
        st.success("Stored")

df = yf.download("EURUSD=X", period="1d", interval="1m")
if not df.empty:
    st.line_chart(df["Close"])

history = db.fetch_all()
if not history.empty:
    st.dataframe(history)
