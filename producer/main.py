import json
import logging
import os
from datetime import datetime
from random import randint

import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "quickstart")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "broker:9092")


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO)
log = logging.getLogger(__name__)


app = FastAPI(title="FastAPI - Message Producer")


def serializer(value):
    return json.dumps(value).encode()


@app.get("/send")
async def send_message():
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=serializer,
        compression_type="gzip"
    )
    await producer.start()
    try:
        msg_id = f"{randint(1, 10000)}"
        msg_body = f"Message #{msg_id} generated at {datetime.now()}"
        message = {"message_id": msg_id, "text": msg_body, "state": randint(1, 100)}
        
        log.info(f"Sending message #{msg_id}")
        await producer.send_and_wait(KAFKA_TOPIC, message)

    finally:
        await producer.stop()
    
    return {"message": f"Sending message: {message}"}



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7000, reload=True)
