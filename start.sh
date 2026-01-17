#!/bin/bash
# Start tiny web server to keep Render free tier awake
gunicorn --bind 0.0.0.0:8080 health:app &

# Change to Kafka home directory
cd /opt/kafka

# Start Kafka in KRaft mode (no ZooKeeper)
export KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties
bin/kafka-server-start.sh config/kraft/server.properties