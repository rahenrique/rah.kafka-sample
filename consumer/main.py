import json
import logging
import os

import uvicorn
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "quickstart")
KAFKA_CONSUMER_GROUP = os.getenv("KAFKA_CONSUMER_GROUP", "group")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "broker:9092")


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO)
log = logging.getLogger(__name__)


app = FastAPI(title="FastAPI - Message Consumer")


def deserializer(serialized):
    return json.loads(serialized)


@app.get("/receive")
async def consume_message():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=deserializer,
        group_id=KAFKA_CONSUMER_GROUP,
        auto_offset_reset='earliest',
        enable_auto_commit=False
    )

    await consumer.start()
    
    messages = list()
    
    data = await consumer.getmany(timeout_ms=1000)
    for topic, items in data.items():
        for msg in items:
            messages.append(msg)
    
    await consumer.commit()
    await consumer.stop()

    return {"messages": messages}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7000, reload=True)
