import sqlite3
import pandas as pd
import os

class Database:
    def __init__(self, db_path="data/nfp.db"):
        # ✅ Ensure folder exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            actual REAL,
            forecast REAL,
            surprise REAL,
            action TEXT
        )
        """)

    def insert_signal(self, data):
        self.conn.execute("""
        INSERT INTO signals (date, actual, forecast, surprise, action)
        VALUES (?, ?, ?, ?, ?)
        """, (data["date"], data["actual"], data["forecast"],
              data["surprise"], data["action"]))
        self.conn.commit()

    def fetch_all(self):
        return pd.read_sql("SELECT * FROM signals", self.conn)
