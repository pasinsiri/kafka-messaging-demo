FROM apache/kafka:3.8.0

# Switch to root temporarily to install stuff and fix permissions
USER root

# Create app directory and copy our files
WORKDIR /opt/kafka-scripts
COPY requirements.txt start.sh health.py ./

# Install Python + deps
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

# Fix permissions so the non-root user can execute start.sh
RUN chmod +x start.sh && \
    chown -R appuser:appuser /opt/kafka-scripts

# Switch back to the non-root user (required by the base image)
USER appuser

# Expose ports (no inline comments!)
EXPOSE 9092/tcp
EXPOSE 8080/tcp

# Start everything
CMD ["./start.sh"]