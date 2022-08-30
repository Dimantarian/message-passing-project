import time
import os
from concurrent import futures
from kafka import KafkaProducer
import grpc
import json
import location_pb2
import location_pb2_grpc


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    """Class to manage incoming requests"""

    def Create(self, request, context):
        TOPIC_NAME = "locations"
        # KAFKA_SERVER = (os.getenv("KAFKA_ADDRESS") )
        # producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
        print(os.getenv("KAFKA_ADDRESS"))
        request_value = {
            "person_id": request.person_id,
            "longitude": request.longitude,
            "latitude": request.latitude
            # "creation_time": request.creation_time #this is a nightmare!
        }

        # this is where I want to send to kafka!
        encoded_request_value = json.dumps(request_value).encode()
        # producer.send(TOPIC_NAME, encoded_request_value)
        # producer.flush()
        print(f"Message {request_value} sent to {TOPIC_NAME}")

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
