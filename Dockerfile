FROM apache/kafka:3.8.0
WORKDIR /app

ENV KAFKA_NODE_ID=1
ENV KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
ENV KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://0.0.0.0:9092
ENV KAFKA_CONTROLLER_QUORUM_VOTERS=1@localhost:9093
ENV KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
ENV KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT
ENV KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER
ENV KAFKA_PROCESS_ROLES=controller,broker
ENV KAFKA_LOG_DIRS=/tmp/kafka-logs

# Copy our files
COPY requirements.txt start.sh health.py ./
RUN chmod +x start.sh

# Install Python dependencies
RUN apt update && apt install -y python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Expose ports
EXPOSE 9092   # Kafka
EXPOSE 8080   # Health check

CMD ["./start.sh"]