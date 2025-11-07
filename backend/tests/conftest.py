"""
Test configuration for pytest
"""
import pytest
import asyncio
from typing import Generator
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import close_mongo_connection, db

@pytest.fixture(scope="function", autouse=True)
def reset_database_client():
    """Reset database client before each test to ensure it uses the TestClient's event loop."""
    # Close existing connection if any
    if db.client:
        db.client.close()
        db.client = None
    yield
    # Clean up after test
    if db.client:
        db.client.close()
        db.client = None

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Set up database connection before tests and close after."""
    # Don't connect here - let it connect lazily when first needed
    # This ensures Motor uses the TestClient's event loop
    yield
    # Close database connection
    if db.client:
        db.client.close()
        db.client = None
        print("Closed MongoDB connection")
