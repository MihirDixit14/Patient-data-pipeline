import pandas as pd
import pytest
from app.transform import transform_patients, transform_observations, transform_encounters


@pytest.fixture
def raw_patients():
    return [
        {
            "id": "p1",
            "gender": "male",
            "birthDate": "1990-05-10",
            "address": [{"city": "Milwaukee", "state": "WI", "country": "US"}],
        },
        {
            "id": None,
            "gender": "female",
        },
    ]


@pytest.fixture
def raw_observations():
    return [
        {
            "id": "obs1",
            "subject": {"reference": "Patient/p1"},  # fixed: typo "refernce" and lowercase "patient"
            "code": {"coding": [{"display": "Heart rate"}]},
            "valueQuantity": {"value": 95.0, "unit": "bpm"},
            "effectiveDateTime": "2023-01-15T10:00:00",
            "referenceRange": [{"low": {"value": 60}, "high": {"value": 100}}],
            "status": "final",
        }
    ]


@pytest.fixture
def raw_encounters():
    return [
        {
            "id": "enc1",
            "subject": {"reference": "Patient/p1"},
            "status": "finished",
            "period": {"start": "2023-01-10T08:00:00", "end": "2023-01-13T08:00:00"},
        }
    ]


def test_transform_patients_returns_dataframe(raw_patients):
    df = transform_patients(raw_patients)
    assert isinstance(df, pd.DataFrame)


def test_transform_patients_columns(raw_patients):
    df = transform_patients(raw_patients)  # fixed: was pd.DataFrame(raw_patients)
    assert set(df.columns) == {"patient_id", "gender", "birth_date", "city", "state", "country"}


def test_transform_patients_drops_null_id(raw_patients):
    df = transform_patients(raw_patients)
    assert len(df) == 1
    assert df.iloc[0]["patient_id"] == "p1"


def test_transform_observations_returns_dataframe(raw_observations):
    df = transform_observations(raw_observations)
    assert isinstance(df, pd.DataFrame)


def test_transform_observations_columns(raw_observations):
    df = transform_observations(raw_observations)
    assert set(df.columns) == {"observation_id", "patient_id", "observation_type",  # fixed: typo "onbservation_id"
                                "value", "unit", "effective_date",
                                "ref_range_low", "ref_range_high", "status"}


def test_transform_observations_patient_id(raw_observations):
    df = transform_observations(raw_observations)  # fixed: was calling wrong function and fixture
    assert df.iloc[0]["patient_id"] == "p1"


def test_transform_encounters_returns_dataframe(raw_encounters):
    df = transform_encounters(raw_encounters)
    assert isinstance(df, pd.DataFrame)


def test_transform_encounters_columns(raw_encounters):
    df = transform_encounters(raw_encounters)
    assert set(df.columns) == {"encounter_id", "patient_id", "status",
                                "admission_date", "discharge_date", "length_of_stay_days"}


def test_transform_encounters_length_of_stay(raw_encounters):
    df = transform_encounters(raw_encounters)
    assert df.iloc[0]["length_of_stay_days"] == 3
