import os
import logging
import pandas as pd
from sqlalchemy import create_engine, text

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

DB_URL = os.getenv("DB_URL", "sqlite:///./data/fhir.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS patients (
    patient_id   TEXT PRIMARY KEY,
    gender       TEXT,
    birth_date   DATE,
    city         TEXT,
    state        TEXT,
    country      TEXT
);

CREATE TABLE IF NOT EXISTS observations (
    observation_id   TEXT PRIMARY KEY,
    patient_id       TEXT,
    observation_type TEXT,
    value            REAL,
    unit             TEXT,
    effective_date   TIMESTAMP,
    ref_range_low    REAL,
    ref_range_high   REAL,
    status           TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

CREATE TABLE IF NOT EXISTS encounters (
    encounter_id        TEXT PRIMARY KEY,
    patient_id          TEXT,
    status              TEXT,
    admission_date      TIMESTAMP,
    discharge_date      TIMESTAMP,
    length_of_stay_days INTEGER,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);
"""


def get_engine():
    pass


def init_schema(engine) -> None:
    pass


def _upsert_dataframe(df: pd.DataFrame, table: str, pk: str, engine) -> tuple[int, int]:
    pass


def load_all(
    patients: pd.DataFrame,
    observations: pd.DataFrame,
    encounters: pd.DataFrame,
) -> dict:
    pass
