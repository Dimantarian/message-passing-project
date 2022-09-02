import json
import os
import logging
from kafka import KafkaConsumer
from sqlalchemy import create_engine


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
    """ Validates an input against the location schema,
    transforms itand inserts it into the postgres database"""

    insert = f"INSERT INTO location (person_id, coordinate) VALUES  \
        ({kafka_message['person_id']}, \
            ST_Point({kafka_message['latitude']}, {kafka_message['longitude']}))"
    print(insert)

    with engine.begin() as connection:
        connection.execute(insert)


for message in consumer:
    decoded_message = message.value.decode('utf-8')
    logger.info(f'Processing "{decoded_message}"')
    location_message = json.loads(decoded_message)
    write_to_postgres(location_message)
