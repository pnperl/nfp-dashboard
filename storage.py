import pandas as pd
import os

class DriveStorage:
    def __init__(self, path="/content/drive/MyDrive/nfp_dashboard/cache.csv"):
        self.path = path

    def save(self, new_data: pd.DataFrame):
        if os.path.exists(self.path):
            old = pd.read_csv(self.path)
            combined = pd.concat([old, new_data]).drop_duplicates()
        else:
            combined = new_data

        combined.to_csv(self.path, index=False)

    def load(self):
        if os.path.exists(self.path):
            return pd.read_csv(self.path)
        return pd.DataFrame()
