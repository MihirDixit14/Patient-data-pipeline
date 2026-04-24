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
    pass


if __name__ == "__main__":
    pass
