$ helm install uda-kafka ./kafka
NAME: uda-kafka
LAST DEPLOYED: Mon Aug 29 15:42:16 2022
NAMESPACE: udaconnect
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: kafka
CHART VERSION: 18.3.0
APP VERSION: 3.2.1
---------------------------------------------------------------------------------------------
 WARNING

    By specifying "serviceType=LoadBalancer" and not configuring the authentication
    you have most likely exposed the Kafka service externally without any
    authentication mechanism.

    For security reasons, we strongly suggest that you switch to "ClusterIP" or   
    "NodePort". As alternative, you can also configure the Kafka authentication.  

---------------------------------------------------------------------------------------------

** Please be patient while the chart is being deployed **

Kafka can be accessed by consumers via port 9092 on the following DNS name from within your cluster:

    uda-kafka.udaconnect.svc.cluster.local

Each Kafka broker can be accessed by producers via port 9092 on the following DNS name(s) from within your cluster:

    uda-kafka-0.uda-kafka-headless.udaconnect.svc.cluster.local:9092

To create a pod that you can use as a Kafka client run the following commands:    

    kubectl run uda-kafka-client --restart='Never' --image docker.io/bitnami/kafka:3.2.1-debian-11-r4 --namespace udaconnect --command -- sleep infinity
    kubectl exec --tty -i uda-kafka-client --namespace udaconnect -- bash

    PRODUCER:
        kafka-console-producer.sh \

To connect to your Kafka server from outside the cluster, follow the instructions below:

    Kafka brokers domain: You can get the external node IP from the Kafka configuration file with the following commands (Check the EXTERNAL listener)

        1. Obtain the pod name:

        kubectl get pods --namespace udaconnect -l "app.kubernetes.io/name=kafka,app.kubernetes.io/instance=uda-kafka,app.kubernetes.io/component=kafka"
        2. Obtain pod configuration:

        kubectl exec -it KAFKA_POD -- cat /opt/bitnami/kafka/config/server.properties | grep advertised.listeners
    Kafka brokers port: You will have a different node port for each Kafka broker. You can get the list of configured node ports using the command below:

        echo "$(kubectl get svc --namespace udaconnect -l "app.kubernetes.io/name=kafka,app.kubernetes.io/instance=uda-kafka,app.kubernetes.io/component=kafka,pod" -o jsonpath='{.items[*].spec.ports[0].nodePort}' | tr ' ' '\n')"