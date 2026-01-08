FROM apache/kafka:3.8.0

# Switch to root temporarily to install stuff and fix permissions
USER root

# Create app directory and copy our files
WORKDIR /opt/kafka-scripts
COPY requirements.txt start.sh health.py ./

# Install Python + build dependencies for compiled packages
RUN apk add --no-cache \
    python3 \
    py3-pip \
    librdkafka && \
    apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    librdkafka-dev \
    cargo \
    rust && \
    pip3 install --no-cache-dir --break-system-packages -r requirements.txt && \
    apk del .build-deps

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