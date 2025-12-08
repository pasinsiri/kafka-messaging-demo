FROM apache/kafka:3.8.0
WORKDIR /app

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