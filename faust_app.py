import faust
import re
from datetime import timedelta

app = faust.App(
    'kafka-streams-2025',
    broker='kafka://host.docker.internal:9092',  # works locally; Render uses internal networking
    store='rocksdb://',
    topic_partitions=4,
)

class Message(faust.Record):
    message: str

input_topic = app.topic('demo-topic', value_type=Message)
word_counts = app.Table('word_counts', default=int).tumbling(timedelta(seconds=30))

@app.agent(input_topic)
async def count_words(stream):
    async for msg in stream:
        words = re.findall(r'\w+', msg.message.lower())
        for word in words:
            if len(word) > 3:
                word_counts[word] += 1