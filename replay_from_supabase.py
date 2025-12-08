# replay_from_supabase.py
from supabase import create_client
import os, json

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))
data = supabase.table("kafka_messages").select("*").order("id").execute()

for row in data.data:
    print(row["id"], row["value"])