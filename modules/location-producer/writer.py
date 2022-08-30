import grpc
import location_pb2
import location_pb2_grpc
import time


"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("udaconnect-api-location-create:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)


# Update this with desired payload
for i in [5, 6, 1, 8, 9]:
    item = location_pb2.Location(
        person_id=i, longitude="144.361725", latitude="-38.149918")
    # print(f'person_id={i}, longitude="144.361725", latitude="-38.149918"')
    response = stub.Create(item)
    time.sleep(5)
