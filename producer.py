from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

for i in range(10):
    message = {'event': f'Message {i}', 'data': i * 2}
    producer.send('my-test-topic', value=message)
    print(f'Sent: {message}')

producer.flush()