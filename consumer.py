# consumer.py
from confluent_kafka import Consumer
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

conf = {
    'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['messages'])

while True:
    msg = consumer.poll(1.0)
    if msg is None: continue
    if msg.error():
        print("Error:", msg.error())
        continue
    print("Received:", msg.value().decode())