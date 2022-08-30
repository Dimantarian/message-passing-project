$ helm install my-release bitnami/kafka
NAME: my-release
LAST DEPLOYED: Sun Aug 28 20:15:07 2022
NAMESPACE: udaconnect
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: kafka
CHART VERSION: 18.0.0
APP VERSION: 3.2.0

** Please be patient while the chart is being deployed **

Kafka can be accessed by consumers via port 9092 on the following DNS name from within your cluster:

    my-release-kafka.udaconnect.svc.cluster.local

Each Kafka broker can be accessed by producers via port 9092 on the following DNS name(s) from within your cluster:

    my-release-kafka-0.my-release-kafka-headless.udaconnect.svc.cluster.local:9092

To create a pod that you can use as a Kafka client run the following commands:

    kubectl run my-release-kafka-client --restart='Never' --image docker.io/bitnami/kafka:3.2.0-debian-11-r3 --namespace udaconnect --command -- sleep infinity
    kubectl exec --tty -i my-release-kafka-client --namespace udaconnect -- bash

    PRODUCER:
        kafka-console-producer.sh \
            --broker-list my-release-kafka-0.my-release-kafka-headless.udaconnect.svc.cluster.local:9092 \
            --topic test123

    CONSUMER:
        kafka-console-consumer.sh \
            --bootstrap-server my-release-kafka.udaconnect.svc.cluster.local:9092 \
            --topic test123 \
            --from-beginning