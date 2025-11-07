from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os

class Database:
    client: Optional[AsyncIOMotorClient] = None
    
db = Database()

async def connect_to_mongo():
    """Connect to MongoDB."""
    mongo_url = os.getenv("MONGODB_URL", "mongodb://mongodb:27017")
    db.client = AsyncIOMotorClient(mongo_url)
    print(f"Connected to MongoDB at {mongo_url}")

async def close_mongo_connection():
    """Close MongoDB connection."""
    if db.client:
        db.client.close()
        print("Closed MongoDB connection")

def get_database():
    """Get database instance."""
    return db.client["agent_on_call"]

def get_tickets_collection():
    """Get tickets collection."""
    database = get_database()
    return database["tickets"]

def get_activities_collection():
    """Get activities collection."""
    database = get_database()
    return database["activities"]

def get_triage_results_collection():
    """Get triage_results collection."""
    database = get_database()
    return database["triage_results"]

def get_users_collection():
    """Get users collection."""
    database = get_database()
    return database["users"]

def get_activity_logs_collection():
    """Get activity_logs collection."""
    database = get_database()
    return database["activity_logs"]

def get_comments_collection():
    """Get comments collection."""
    database = get_database()
    return database["comments"]

def get_attachments_collection():
    """Get attachments collection (optional)."""
    database = get_database()
    return database["attachments"]
