import time
import os
import json
import logging
from concurrent import futures
from kafka import KafkaProducer
import grpc

import location_pb2
import location_pb2_grpc

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("api-location-create")


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    """Class to manage incoming requests"""

    def Create(self, request, context):
        logger.info(f"Creating location from {request}")

        TOPIC_NAME = "locations"
        KAFKA_SERVER = (os.getenv("KAFKA_ADDRESS"))
        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
        print(os.getenv("KAFKA_ADDRESS"))
        request_value = {
            "person_id": request.person_id,
            "longitude": request.longitude,
            "latitude": request.latitude
        }

        encoded_request_value = json.dumps(request_value).encode()
        producer.send(TOPIC_NAME, encoded_request_value)
        logger.info(f"Message {request_value} sent to {TOPIC_NAME}")

        return location_pb2.Location(**request_value)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(
    LocationServicer(), server)

print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
