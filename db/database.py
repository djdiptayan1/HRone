from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "ecommerce_db")  # Default fallback


def get_db():
    if not MONGO_URI:
        raise ValueError("MONGO_URI environment variable is not set")

    if not DB_NAME:
        raise ValueError("DB_NAME environment variable is not set")

    client = MongoClient(MONGO_URI)
    try:
        client.admin.command("ping")
        print(f"Connected to MongoDB - Database: {DB_NAME}")
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        raise

    return client[DB_NAME]
