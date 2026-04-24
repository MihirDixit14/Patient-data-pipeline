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
