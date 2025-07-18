from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
MONGO_URI = dotenv.get_key(".env", "MONGO_URI")
DB_NAME = dotenv.get_key(".env", "DB_NAME")


def get_db():
    client = MongoClient(MONGO_URI)
    try:
        client.admin.command("ping")
        print("Connected to MongoDB")
    except ConnectionFailure:
        print("MongoDB connection failed")
    return client[DB_NAME]
