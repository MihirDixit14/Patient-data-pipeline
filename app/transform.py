import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def _extract_patient_id(reference: str) -> str | None:
    if not reference:
        return None
    parts = reference.split("/")
    return parts[-1] if len(parts) == 2 else None


def transform_patients(raw: list[dict]) -> pd.DataFrame:
    rows = []
    for p in raw:
        address = p.get("address", [{}])[0]
        rows.append({
            "patient_id": p.get("id"),
            "gender":     p.get("gender"),
            "birth_date": p.get("birthDate"),
            "city":       address.get("city"),
            "state":      address.get("state"),
            "country":    address.get("country"),
        })
    df = pd.DataFrame(rows).dropna(subset=["patient_id"])
    logging.info(f"Transformed {len(df)} patients")
    return df


def transform_observations(raw: list[dict]) -> pd.DataFrame:
    rows = []
    for o in raw:
        ref_range = o.get("referenceRange", [{}])[0]
        vq = o.get("valueQuantity", {})
        rows.append({
            "observation_id":   o.get("id"),
            "patient_id":       _extract_patient_id(o.get("subject", {}).get("reference", "")),
            "observation_type": o.get("code", {}).get("coding", [{}])[0].get("display"),
            "value":            vq.get("value"),
            "unit":             vq.get("unit"),
            "effective_date":   o.get("effectiveDateTime"),
            "ref_range_low":    ref_range.get("low", {}).get("value"),
            "ref_range_high":   ref_range.get("high", {}).get("value"),
            "status":           o.get("status"),
        })
    df = pd.DataFrame(rows).dropna(subset=["observation_id"])
    logging.info(f"Transformed {len(df)} observations")
    return df


def transform_encounters(raw: list[dict]) -> pd.DataFrame:
    rows = []
    for e in raw:
        period = e.get("period", {})
        start = period.get("start")
        end = period.get("end")
        los = None
        if start and end:
            los = (pd.Timestamp(end) - pd.Timestamp(start)).days
        rows.append({
            "encounter_id":        e.get("id"),
            "patient_id":          _extract_patient_id(e.get("subject", {}).get("reference", "")),
            "status":              e.get("status"),
            "admission_date":      start,
            "discharge_date":      end,
            "length_of_stay_days": los,
        })
    df = pd.DataFrame(rows).dropna(subset=["encounter_id"])
    logging.info(f"Transformed {len(df)} encounters")
    return df
