import redis
import os
from dotenv import load_dotenv
import json

load_dotenv(".env")
HOST = os.getenv('REDIS_HOST')
PORT = os.getenv('REDIS_PORT')
PASSWORD = os.getenv('REDIS_PASSWORD')


def main():
    r = redis.Redis(host=HOST, port=PORT,password=PASSWORD,db=0, decode_responses=True)
    payload = {
        "status": "end",
        "message": "Fim ETL"
    }
    # Publish a message to a channel
    subscribers = r.publish('ETL', json.dumps(payload))
    print(f"Message delivered to {subscribers} subscribers")
