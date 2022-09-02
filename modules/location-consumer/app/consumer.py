import json
import os
import logging
from datetime import datetime
from typing import Dict
from kafka import KafkaConsumer
from sqlalchemy import create_engine
from geoalchemy2.functions import ST_Point
from models import Location
from schemas import LocationSchema


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("location-consumer")

TOPIC_NAME = "locations"
logger.info(f'Consumer listening to "{TOPIC_NAME}" topic')

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
KAFKA_ADDRESS = os.environ["KAFKA_ADDRESS"]

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_ADDRESS])
engine = create_engine(
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)


def write_to_postgres(kafka_message):
    """ Validates an input against the location schema, transforms itand inserts it into the postgres database"""

    validation_results: Dict = LocationSchema().validate(kafka_message)
    if validation_results:
        logger.warning(
            f"Unexpected data format in payload: {validation_results}")
        raise Exception(f"Invalid payload: {validation_results}")

    new_location = Location()
    new_location.person_id = kafka_message["person_id"]
    new_location.creation_time = datetime.utcnow
    new_location.coordinate = ST_Point(
        kafka_message["latitude"], kafka_message["longitude"])

    # runs a transaction
    with engine.begin() as connection:
        connection.execute(Location.insert(), {"person_id": new_location.person_id,
                                               "coordinate": new_location.coordinate,
                                               "creation_time": new_location.creation_time})


for location in consumer:
    message = location.value.decode('utf-8')
    logger.info(f'Processing "{message}"')
    location_message = json.loads(message)
    write_to_postgres(location_message)
