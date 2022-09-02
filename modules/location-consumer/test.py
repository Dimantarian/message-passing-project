
import os
import logging
from sqlalchemy import create_engine, MetaData, select, func
from datetime import datetime
from geoalchemy2.functions import ST_Point

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

engine = create_engine(
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)

conn = engine.connect()
# Create a MetaData instance
metadata = MetaData()

# reflect db schema to MetaData
metadata.reflect(bind=engine)
location = metadata.tables['location']

select_st = select([location])
res = conn.execute(select_st).fetchall()

print(f"there are {len(res)} rows")
# for _row in res:
#     print(_row)

coordinate = ST_Point(30, 164)

insert = location.insert().values(
    person_id=1,
    creation_time=datetime.utcnow(),
    coordinate=coordinate)

conn.execute(insert)

resafter = conn.execute(select_st).fetchall()

print(f"Now there are {len(resafter)} rows")
