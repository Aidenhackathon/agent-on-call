"""
Script to clear all data from MongoDB database.
Use with caution - this will delete all tickets, users, and other data.
"""
import asyncio
from database import connect_to_mongo, get_database


async def clear_database():
    """Clear all collections in the database."""
    await connect_to_mongo()
    
    db = get_database()
    
    # List of collections to clear
    collections = [
        "tickets",
        "users",
        "triage_results",
        "activities",
        "activity_logs",
        "comments",
        "attachments"
    ]
    
    print("Clearing MongoDB database...")
    
    for collection_name in collections:
        collection = db[collection_name]
        result = await collection.delete_many({})
        print(f"   Cleared {collection_name}: {result.deleted_count} documents")
    
    print("Database cleared successfully!")
    print("Run seed_users.py to populate teams data.")


if __name__ == "__main__":
    asyncio.run(clear_database())

