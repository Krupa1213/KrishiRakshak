import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)

db = client["KrishiRakshak"]

farmers_collection = db["farmers"]

print("MongoDB connection successful!")