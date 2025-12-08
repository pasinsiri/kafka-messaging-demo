# producer.py
from confluent_kafka import Producer
from supabase import create_client
import json, os, time

# Supabase
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")   # use service_role key locally too
)

# Kafka
conf = {
    'bootstrap.servers': 'kafka-practice.onrender.com:9092',
    'message.timeout.ms': 5000
}
producer = Producer(conf)

def delivery_report(err, msg):
    if err: print('Failed:', err)
    else:   print(f"Delivered to {msg.topic()} [partition {msg.partition()}]")

topic = "demo-topic"
for i in range(20):
    message = {"id": i, "message": f"Hello from Render #{i}", "ts": time.time()}
    
    # 1. Send to Kafka
    producer.produce(topic, json.dumps(message).encode(), callback=delivery_report)
    producer.poll(0)
    
    # 2. Persist to Supabase (survives restarts)
    supabase.table("kafka_messages").insert({
        "topic": topic,
        "key": f"user-{i%5}",
        "value": message
    }).execute()
    
    print(f"Sent & persisted #{i}")
    time.sleep(1)

producer.flush()