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
    import asyncio
    # Get the current event loop - Motor will use this for all operations
    loop = asyncio.get_running_loop() if hasattr(asyncio, 'get_running_loop') else asyncio.get_event_loop()
    db.client = AsyncIOMotorClient(mongo_url, io_loop=loop)
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
        # Lazy connection - create client without specifying event loop
        # Motor will use the current event loop when operations are performed
        # This works because we're called from async context (TestClient)
        mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        # Create client without io_loop - Motor will detect and use current loop
        db.client = AsyncIOMotorClient(mongo_url)
        print(f"Connected to MongoDB at {mongo_url} (lazy connection)")


def get_database():
    """Get database instance."""
    _ensure_connected()
    return db.client["agent_on_call"]


def _recreate_client():
    """Recreate the database client."""
    if db.client:
        db.client.close()
        db.client = None
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    db.client = AsyncIOMotorClient(mongo_url)
    print(f"Reconnected to MongoDB at {mongo_url} (event loop was closed)")

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
