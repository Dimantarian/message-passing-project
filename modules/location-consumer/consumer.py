import json
import os
import logging
from datetime import datetime
from kafka import KafkaConsumer
from sqlalchemy import create_engine, MetaData
from geoalchemy2.functions import ST_Point

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("location-consumer")

TOPIC_NAME = "locations"
logger.info(f'Consumer listening to "{TOPIC_NAME}" topic')

KAFKA_ADDRESS = os.environ["KAFKA_ADDRESS"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]


consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_ADDRESS])
engine = create_engine(
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)
metadata = MetaData()

# reflect db schema to MetaData
metadata.reflect(bind=engine)
location = metadata.tables['location']


def write_to_postgres(kafka_message):
    """ Validates an input against the location schema,
    transforms itand inserts it into the postgres database"""

    # new_location = models.Location(kafka_message)
    # insert = f"INSERT INTO {models.Location} (person_id, coordinate) VALUES  \
    #     ({kafka_message['person_id']}, \
    #         ST_Point({kafka_message['latitude']}, {kafka_message['longitude']}))"
    # print(insert)

    insert = location.insert().values(
        person_id=kafka_message['person_id'],
        creation_time=datetime.utcnow,
        coordinate=ST_Point(
            kafka_message['latitude'], kafka_message['longitude'])
    )

    with engine.begin() as connection:
        connection.execute(insert)


for message in consumer:
    decoded_message = message.value.decode('utf-8')
    logger.info(f'Processing "{decoded_message}"')
    location_message = json.loads(decoded_message)
    write_to_postgres(location_message)
