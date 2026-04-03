import requests
import pandas as pd

def fetch_latest_nfp():
    url = "https://api.tradingeconomics.com/calendar"
    params = {"c": "guest:guest", "country": "United States"}

    try:
        res = requests.get(url, params=params)
        df = pd.DataFrame(res.json())

        df = df[df["Event"].str.contains("Non Farm Payrolls", case=False, na=False)]

        if df.empty:
            return None

        latest = df.iloc[0]

        return {
            "date": latest["Date"],
            "actual": float(latest["Actual"]),
            "forecast": float(latest["Forecast"])
        }

    except:
        return None
