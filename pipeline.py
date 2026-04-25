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
    # TODO 1: log that pipeline is starting
    # TODO 2: record start time using time.time()
    # TODO 3: call fetch_all(force_refresh) to get raw data
    # TODO 4: call transform_patients, transform_observations, transform_encounters
    # TODO 5: call load_all with the three DataFrames
    # TODO 6: log the summary dict returned by load_all
    # TODO 7: log total elapsed time using time.time() - start
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
