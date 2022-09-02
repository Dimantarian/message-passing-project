from kafka import KafkaClient, KafkaConsumer
import json
client = KafkaClient(bootstrap_servers='host.docker.internal:9092')

future = client.cluster.request_update()
client.poll(future=future)

metadata = client.cluster
print(metadata.topics())


consumer = KafkaConsumer('locations',
                         bootstrap_servers=['host.docker.internal:9092'])
for message in consumer:
    print(json.loads(message))
