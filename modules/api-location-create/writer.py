import grpc
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime
import location_pb2
import location_pb2_grpc


"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)
timestamp = Timestamp()
timestamp.GetCurrentTime()
print(timestamp)

# Update this with desired payload
item = location_pb2.Location(
    person_id=6,
    longitude="144.361725",
    latitude="-38.149918",
    creation_time=timestamp
)


response = stub.Create(item)
