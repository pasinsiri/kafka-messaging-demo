# wordcount.py  ← This is your Kafka Streams replacement
from confluent_kafka import Consumer, Producer
from dotenv import load_dotenv
import json, re, time
from collections import defaultdict
from supabase import create_client
import os

# Load environment variables
load_dotenv()

# Supabase — use secret key for server-side writes
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SECRET_KEY")  # sb_secret_... (or publishable if running locally)
)

consumer = Consumer({
    'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    'group.id': 'wordcount-group-v2',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False   # manual commit for reliability
})

producer = Producer({'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS")})

consumer.subscribe(['messages'])

word_counts = defaultdict(int)
processed = 0

print("Word count stream processor started...")

while True:
    msg = consumer.poll(1.0)
    if msg is None: continue
    if msg.error():
        print("Error:", msg.error())
        continue

    data = json.loads(msg.value().decode())
    words = re.findall(r'\w+', data["text"].lower())
    
    for word in words:
        if len(word) > 3:
            word_counts[word] += 1

    processed += 1
    
    # Every 10 messages → publish result + update Supabase dashboard
    if processed % 10 == 0:
        top10 = dict(sorted(word_counts.items(), key=lambda x: -x[1])[:10])
        print(f"Processed {processed} → Top words:", top10)
        
        # 1. Push to Kafka topic (optional)
        producer.produce("wordcount-results", json.dumps(top10).encode())
        producer.poll(0)
        
        # 2. Push to Supabase live table (visible instantly in dashboard)
        supabase.table("stream_results").upsert({
            "id": 1,
            "result": {"top_words": top10, "total_messages": processed}
        }).execute()
        
        # Commit offset only after successful processing
        consumer.commit(asynchronous=False)

producer.flush()