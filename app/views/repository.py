import streamlit as st
import pandas as pd
import sqlalchemy
import os
from dotenv import load_dotenv

def connect():
    load_dotenv()
    conn = sqlalchemy.create_engine(
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?charset=utf8mb4"
    )
    return conn.connect()

@st.cache_data(ttl=3600)
def load_mart_monthly_de_facto_population_per_time() -> pd.DataFrame:
    with connect() as con:
        q = """
        SELECT * FROM mart_monthly_de_facto_population_per_time
        WHERE CAST(time_hour AS UNSIGNED) BETWEEN 8 AND 22;
        """
        return pd.read_sql(q, con)

@st.cache_data(ttl=3600)
def load_mart_state_monthly() -> pd.DataFrame:
    with connect() as con:
        q = """
        SELECT * FROM mart_state_monthly;
        """
        return pd.read_sql(q, con)

@st.cache_data(ttl=3600)
def load_mart_state_hourly() -> pd.DataFrame:
    with connect() as con:
        q = """
        SELECT * FROM mart_state_hourly
        WHERE CAST(time_hour AS UNSIGNED) BETWEEN 8 AND 22;
        """
        return pd.read_sql(q, con)

@st.cache_data(ttl=3600)
def load_mart_priority_score() -> pd.DataFrame:
    with connect() as con:
        q = """
        SELECT * FROM mart_priority_score;
        """
        return pd.read_sql(q, con)