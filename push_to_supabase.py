# push_to_supabase.py
from supabase import create_client
import json, time
from confluent_kafka import Consumer

# Supabase – Use secret key for server-side pushes
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SECRET_KEY")  # New: secret key (replaces service_role)
)

consumer = Consumer({
    'bootstrap.servers': 'kafka-practice.onrender.com:9092',
    'group.id': 'supabase-pusher',
    'auto.offset.reset': 'latest'
})
consumer.subscribe(['wordcount-output'])   # from Level 1 or Faust

while True:
    msg = consumer.poll(1.0)
    if msg and not msg.error():
        data = json.loads(msg.value().decode())
        supabase.table("live_dashboard").upsert({
            "id": 1,
            "top_words": data["top_words"],
            "updated_at": time.time()
        }).execute()
        print("Dashboard updated →", data["top_words"])