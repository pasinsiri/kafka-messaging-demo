from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('my-test-topic',
                         bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',  # Start from beginning
                         enable_auto_commit=True,
                         group_id='my-group',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

for message in consumer:
    print(f'Received: {message.value}')