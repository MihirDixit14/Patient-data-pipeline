import os
import json
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

BASE_URL = os.getenv("FHIR_BASE_URL", "https://hapi.fhir.org/baseR4")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def fetch_resource(resource_type: str, count: int = 100) -> list[dict]:
    """Fetch all pages of a FHIR resource type up to count entries."""
    entries = []
    url = f"{BASE_URL}/{resource_type}?_count={count}"

    while url:
        logging.info(f"Fetching {url}")
        response = requests.get(url, headers={"Accept": "application/fhir+json"}, timeout=30)
        response.raise_for_status()
        bundle = response.json()

        for entry in bundle.get("entry", []):
            entries.append(entry.get("resource", {}))

        # follow the next page link if present
        url = next(
            (link["url"] for link in bundle.get("link", []) if link["relation"] == "next"),
            None,
        )

    logging.info(f"Fetched {len(entries)} {resource_type} records")
    return entries


def save_raw(resource_type: str, data: list[dict]) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, f"raw_{resource_type.lower()}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    logging.info(f"Saved raw {resource_type} to {path}")


def load_raw(resource_type: str) -> list[dict]:
    path = os.path.join(DATA_DIR, f"raw_{resource_type.lower()}.json")
    with open(path) as f:
        return json.load(f)


def fetch_all(force_refresh: bool = False) -> dict[str, list[dict]]:
    """
    Fetch Patient, Observation, and Encounter resources.
    Uses cached local JSON if available unless force_refresh=True.
    """
    resources = {
        "Patient": 100,
        "Observation": 300,
        "Encounter": 200,
    }
    result = {}

    for resource_type, count in resources.items():
        cache_path = os.path.join(DATA_DIR, f"raw_{resource_type.lower()}.json")
        if not force_refresh and os.path.exists(cache_path):
            logging.info(f"Using cached {resource_type} data from {cache_path}")
            result[resource_type] = load_raw(resource_type)
        else:
            data = fetch_resource(resource_type, count)
            save_raw(resource_type, data)
            result[resource_type] = data

    return result
