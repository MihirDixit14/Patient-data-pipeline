import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def _extract_patient_id(reference: str) -> str | None:
    pass


def transform_patients(raw: list[dict]) -> pd.DataFrame:
    pass


def transform_observations(raw: list[dict]) -> pd.DataFrame:
    pass


def transform_encounters(raw: list[dict]) -> pd.DataFrame:
    pass
