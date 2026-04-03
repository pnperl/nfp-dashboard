import sqlite3
import pandas as pd

class Database:
    def __init__(self, db_path="data/nfp.db"):
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
