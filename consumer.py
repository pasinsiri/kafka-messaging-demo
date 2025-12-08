# consumer.py
from confluent_kafka import Consumer

conf = {
    'bootstrap.servers': 'kafka-practice.onrender.com:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['demo-topic'])

while True:
    msg = consumer.poll(1.0)
    if msg is None: continue
    if msg.error():
        print("Error:", msg.error())
        continue
    print("Received:", msg.value().decode())