import logging
import time
from dotenv import load_dotenv

load_dotenv()

from app.fetch import fetch_all
from app.transform import transform_patients, transform_observations, transform_encounters
from app.load import load_all

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("data/pipeline.log"),
    ],
)


def run(force_refresh: bool = False) -> None:

    logging.info("Pipeline starting")
    start=time.time()
    raw=fetch_all(force_refresh)

    patients=transform_patients(raw["Patient"])
    observations=transform_observations(raw["Observation"])
    encounters=transform_encounters(raw["Encounter"])
    summary=load_all(patients,observations,encounters)
    logging.info(f"Load summary: {summary}")
    logging.info(f"Pipeline completed in {time.time() - start:.2f}s")


if __name__ == "__main__":
    run()
