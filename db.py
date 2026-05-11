from dotenv import load_dotenv
import motor.motor_asyncio
import os

load_dotenv()

def connect_to_db():
    MONGO_URI = os.getenv('MONGO_URI')
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    db = client["microservices"]
    collection = db["fact-or-phrase-generator"]
    return collection