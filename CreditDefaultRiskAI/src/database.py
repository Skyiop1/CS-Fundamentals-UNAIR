import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd

from .config import DATABASE_PATH, ensure_directories


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS prediction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    waktu_prediksi TEXT NOT NULL,
    limit_balance REAL,
    sex INTEGER,
    education INTEGER,
    marriage INTEGER,
    age INTEGER,
    pay_0 INTEGER,
    pay_2 INTEGER,
    pay_3 INTEGER,
    pay_4 INTEGER,
    pay_5 INTEGER,
    pay_6 INTEGER,
    bill_amt1 REAL,
    bill_amt2 REAL,
    bill_amt3 REAL,
    bill_amt4 REAL,
    bill_amt5 REAL,
    bill_amt6 REAL,
    pay_amt1 REAL,
    pay_amt2 REAL,
    pay_amt3 REAL,
    pay_amt4 REAL,
    pay_amt5 REAL,
    pay_amt6 REAL,
    prediction_result TEXT,
    default_probability REAL,
    risk_level TEXT,
    model_used TEXT
);
"""


def get_connection(db_path: str | Path = DATABASE_PATH):
    ensure_directories()
    connection = sqlite3.connect(db_path)
    connection.execute(CREATE_TABLE_SQL)
    connection.commit()
    return connection


def insert_prediction(data: dict, db_path: str | Path = DATABASE_PATH) -> None:
    payload = {key.lower(): value for key, value in data.items()}
    if "limit_bal" in payload and "limit_balance" not in payload:
        payload["limit_balance"] = payload["limit_bal"]
    payload["waktu_prediksi"] = payload.get("waktu_prediksi") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    columns = [
        "waktu_prediksi",
        "limit_balance",
        "sex",
        "education",
        "marriage",
        "age",
        "pay_0",
        "pay_2",
        "pay_3",
        "pay_4",
        "pay_5",
        "pay_6",
        "bill_amt1",
        "bill_amt2",
        "bill_amt3",
        "bill_amt4",
        "bill_amt5",
        "bill_amt6",
        "pay_amt1",
        "pay_amt2",
        "pay_amt3",
        "pay_amt4",
        "pay_amt5",
        "pay_amt6",
        "prediction_result",
        "default_probability",
        "risk_level",
        "model_used",
    ]
    values = [payload.get(column) for column in columns]
    placeholders = ", ".join(["?"] * len(columns))
    query = f"INSERT INTO prediction_history ({', '.join(columns)}) VALUES ({placeholders})"

    with get_connection(db_path) as connection:
        connection.execute(query, values)
        connection.commit()


def fetch_prediction_history(db_path: str | Path = DATABASE_PATH) -> pd.DataFrame:
    with get_connection(db_path) as connection:
        return pd.read_sql_query("SELECT * FROM prediction_history ORDER BY id DESC", connection)


def clear_prediction_history(db_path: str | Path = DATABASE_PATH) -> None:
    with get_connection(db_path) as connection:
        connection.execute("DELETE FROM prediction_history")
        connection.commit()
