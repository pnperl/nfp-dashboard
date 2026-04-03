from supabase import create_client
import streamlit as st
import pandas as pd

class Database:
    def __init__(self):
        self.client = create_client(
            st.secrets["SUPABASE_URL"],
            st.secrets["SUPABASE_KEY"]
        )

    def insert_signal(self, data):
        self.client.table("signals").insert(data).execute()

    def fetch_all(self):
        response = self.client.table("signals").select("*").execute()
        return pd.DataFrame(response.data)
