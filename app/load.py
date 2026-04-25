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
   
    engine=create_engine(DB_URL)

    return engine


def init_schema(engine) -> None:

    with engine.begin() as conn:
        conn.execute(text(SCHEMA))
    logging.info("Schema initialized")



def _upsert_dataframe(df: pd.DataFrame, table: str, pk: str, engine) -> tuple[int, int]:

    try:
        existing=pd.read_sql(f"SLEECT {pk} FROM {table}",engine)
        existing_ids=set(existing[pk].tolist())
    except:
        existing_ids=set()
    
    mask=df[pk].isin(existing_ids)
    new_rows=df[~mask]
    update_rows=df[mask]

    if not new_rows.empty:
        new_rows.to_sql(table,engine,if_exists="replace",index=False)
    
    if not update_rows.empty:
        update_rows.to_sql("_temp",engine,if_exists="replace",index=False)
        with engine.begin() as conn:
            cols=", ".join(df.columns)
            conn.execute(text(f"INSERT OR REPLACE INTO {table} ({cols}) SELECT {cols} FROM _temp"))
    
    inserted=len(new_rows)
    updated=len(update_rows)
    logging.info(f"{table}:{inserted} inserted,{updated} updated")
    return (inserted,updated)



def load_all(
    patients: pd.DataFrame,
    observations: pd.DataFrame,
    encounters: pd.DataFrame,
) -> dict:
    engine=get_engine()
    init_schema(engine)
    p=_upsert_dataframe(patients,"patients","patients_id",engine)
    o=_upsert_dataframe(observations,"observations","observation_id",engine)
    e=_upsert_dataframe(encounters,"encounters","encounter_id",engine)

    return {
        "patients":{"inserted":p[0],"updated":p[1]},
        "observations":{"inserted":o[0],"updated":o[1]},
        "encounters":{"inserted":e[0],"updated":e[1]},
    }