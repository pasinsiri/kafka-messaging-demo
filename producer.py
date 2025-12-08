# producer.py
from confluent_kafka import Producer
from supabase import create_client
import json, os, time

# Supabase — use publishable key locally (safe)
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_PUBLISHABLE_KEY")   # sb_publishable_...
)

producer = Producer({'bootstrap.servers': 'kafka-free.onrender.com:9092'})

def delivery_report(err, msg):
    if err:
        print("Failed:", err)
    else:
        print(f"Sent → {msg.topic()} [{msg.partition()}] offset {msg.offset()}")

for i in range(50):
    msg = {
        "id": i,
        "text": f"This is message number {i}. Let's count words!",
        "user": f"user{i%7}"
    }
    
    # 1. Send to Kafka
    producer.produce("messages", key=f"user{i%7}", value=json.dumps(msg).encode(), callback=delivery_report)
    producer.poll(0)
    
    # 2. Persist to Supabase (survives Render restarts)
    supabase.table("kafka_messages").insert({
        "topic": "messages",
        "key_text": f"user{i%7}",
        "value": msg
    }).execute()
    
    time.sleep(0.5)

producer.flush()
print("All messages sent & persisted!")