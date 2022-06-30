import asyncio
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


@app.get("/")
async def healthcheck():
    return {"message": "I'm a message consumer!"}


@app.get("/receive")
async def consume_message():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_CONSUMER_GROUP,
        auto_offset_reset='earliest',
        enable_auto_commit=False
    )
    messages = list()

    await consumer.start()
    
    # TODO: receive more messages and close the connection
    for _ in range(3):
        msg = await consumer.getone()

        log.info(f"Receiving message #{msg.key}")
        formatted_message = "{}:{:d}:{:d}: key={} value={} timestamp_ms={}".format(msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp)
        
        messages.append(formatted_message)
    
    await consumer.commit()
    await consumer.stop()

    return {"messages": messages}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7000, reload=True)
