from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import tickets
from database import connect_to_mongo, close_mongo_connection

app = FastAPI(
    title="Agent-on-Call API",
    description="AI-powered helpdesk ticket triage system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://frontend:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Event handlers
@app.on_event("startup")
async def startup_db_client():
    """Connect to MongoDB on application startup."""
    try:
        await connect_to_mongo()
    except Exception as e:
        print(f"⚠️  Failed to connect to MongoDB: {e}")
        print("⚠️  Application will start but database operations will fail.")
        # Don't raise - allow app to start for health checks, but log the error

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close MongoDB connection on application shutdown."""
    await close_mongo_connection()

# Include routers
app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])

@app.get("/")
async def root():
    return {
        "message": "Agent-on-Call API",
        "docs": "/docs",
        "version": "1.0.0"
    }
