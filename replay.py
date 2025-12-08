# replay.py
from supabase import create_client
import os

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_PUBLISHABLE_KEY"))
data = supabase.table("kafka_messages").select("*").order("id").execute()
print(f"Recovered {len(data.data)} messages from Supabase!")