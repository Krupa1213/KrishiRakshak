import os
import socket
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(
    MONGODB_URI,
    connectTimeoutMS=20000,
    family=socket.AF_INET
)

db = client["KrishiRakshak"]

farmers_collection = db["farmers"]
farms_collection = db["farms"]

print("MongoDB connection successful!")
