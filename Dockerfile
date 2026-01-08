FROM apache/kafka:3.8.0

# Switch to root temporarily to install stuff and fix permissions
USER root

# Create app directory and copy our files
WORKDIR /opt/kafka-scripts
COPY requirements.txt start.sh health.py ./

# Install build dependencies
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    g++ \
    make \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    zlib-dev \
    curl \
    bash \
    cargo \
    rust

# Install librdkafka from source (need v2.12.1+)
RUN curl -LO https://github.com/confluentinc/librdkafka/archive/refs/tags/v2.12.1.tar.gz && \
    tar -xzf v2.12.1.tar.gz && \
    cd librdkafka-2.12.1 && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf librdkafka-2.12.1 v2.12.1.tar.gz

# Install Python and pip
RUN apk add --no-cache python3 py3-pip

# Install Python packages
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Clean up build dependencies but keep runtime libs
RUN apk del .build-deps

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