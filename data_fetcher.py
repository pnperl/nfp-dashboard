import requests
import pandas as pd

def fetch_nfp_data():
    url = "https://api.tradingeconomics.com/calendar"
    params = {
        "c": "guest:guest",
        "country": "United States"
    }

    try:
        data = requests.get(url, params=params).json()

        df = pd.DataFrame(data)
        df = df[df["Category"] == "Employment Situation"]

        return df[["Date", "Actual", "Forecast"]]

    except:
        return pd.DataFrame()
