from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os


class Database:
    client: Optional[AsyncIOMotorClient] = None


db = Database()


async def connect_to_mongo():
    """Connect to MongoDB."""
    # Default to localhost for local development (MongoDB exposed on host port 27017)
    # In Docker, MONGODB_URL env var will override this to mongodb://mongodb:27017
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    db.client = AsyncIOMotorClient(mongo_url)
    print(f"Connected to MongoDB at {mongo_url}")


async def close_mongo_connection():
    """Close MongoDB connection."""
    if db.client:
        db.client.close()
        db.client = None
        print("Closed MongoDB connection")


def _ensure_connected():
    """Ensure database connection is established."""
    if db.client is None:
        raise RuntimeError(
            "Database not connected. Call connect_to_mongo() first."
        )


def get_database():
    """Get database instance."""
    _ensure_connected()
    return db.client["agent_on_call"]


def get_tickets_collection():
    """Get tickets collection."""
    _ensure_connected()
    database = get_database()
    return database["tickets"]


def get_activities_collection():
    """Get activities collection."""
    _ensure_connected()
    database = get_database()
    return database["activities"]


def get_triage_results_collection():
    """Get triage_results collection."""
    _ensure_connected()
    database = get_database()
    return database["triage_results"]


def get_users_collection():
    """Get users collection."""
    _ensure_connected()
    database = get_database()
    return database["users"]


def get_activity_logs_collection():
    """Get activity_logs collection."""
    _ensure_connected()
    database = get_database()
    return database["activity_logs"]


def get_comments_collection():
    """Get comments collection."""
    _ensure_connected()
    database = get_database()
    return database["comments"]


def get_attachments_collection():
    """Get attachments collection (optional)."""
    _ensure_connected()
    database = get_database()
    return database["attachments"]
