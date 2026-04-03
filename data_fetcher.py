import requests
import pandas as pd
from datetime import datetime

def fetch_latest_nfp():
    url = "https://api.tradingeconomics.com/calendar"
    params = {
        "c": "guest:guest",
        "country": "United States"
    }

    try:
        res = requests.get(url, params=params)
        data = pd.DataFrame(res.json())

        # Filter NFP
        data = data[data["Event"].str.contains("Non Farm Payrolls", case=False, na=False)]

        if data.empty:
            return None

        latest = data.iloc[0]

        return {
            "date": latest["Date"],
            "actual": latest["Actual"],
            "forecast": latest["Forecast"]
        }

    except:
        return None
