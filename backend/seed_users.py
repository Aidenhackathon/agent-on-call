"""
Seed script to populate MongoDB with sample teams for testing.
Run this once to initialize the users collection.
"""
import asyncio
from database import connect_to_mongo, get_users_collection


async def seed_users():
    """Seed the users collection with teams instead of individual users."""
    await connect_to_mongo()
    
    users_collection = get_users_collection()
    
    # Clear existing users (for testing)
    await users_collection.delete_many({})
    
    sample_teams = [
        {
            "_id": "devops_team",
            "name": "DevOps Team",
            "skills": ["kubernetes", "docker", "aws", "infrastructure", "deployment", "monitoring", "cicd", "terraform", "ansible"]
        },
        {
            "_id": "backend_team",
            "name": "Backend Development Team",
            "skills": ["python", "fastapi", "nodejs", "mongodb", "postgresql", "api", "database", "backend", "microservices", "rest"]
        },
        {
            "_id": "frontend_team",
            "name": "Frontend Development Team",
            "skills": ["react", "javascript", "typescript", "css", "html", "ui", "ux", "frontend", "vite", "webpack", "nextjs"]
        },
        {
            "_id": "finance_team",
            "name": "Finance Team",
            "skills": ["billing", "payment", "stripe", "invoice", "refund", "accounting", "pricing", "subscription", "revenue"]
        },
        {
            "_id": "product_team",
            "name": "Product Team",
            "skills": ["product", "feature", "roadmap", "analytics", "enhancement", "requirements", "design", "planning"]
        },
        {
            "_id": "security_team",
            "name": "Security Team",
            "skills": ["security", "authentication", "authorization", "encryption", "vulnerability", "compliance", "penetration testing", "firewall"]
        },
        {
            "_id": "data_team",
            "name": "Data & Analytics Team",
            "skills": ["data", "analytics", "reporting", "bigquery", "etl", "data warehouse", "business intelligence", "sql"]
        },
        {
            "_id": "mobile_team",
            "name": "Mobile Development Team",
            "skills": ["ios", "android", "mobile", "react native", "flutter", "swift", "kotlin", "app store"]
        },
        {
            "_id": "support_team",
            "name": "Customer Support Team",
            "skills": ["customer service", "support", "general", "troubleshooting", "help desk", "ticket management"]
        },
        {
            "_id": "qa_team",
            "name": "QA & Testing Team",
            "skills": ["testing", "qa", "quality assurance", "automation", "selenium", "bug", "test cases", "regression"]
        }
    ]
    
    result = await users_collection.insert_many(sample_teams)
    print(f"✅ Seeded {len(result.inserted_ids)} teams to MongoDB")
    
    # Verify
    count = await users_collection.count_documents({})
    print(f"📊 Total teams in database: {count}")
    
    async for team in users_collection.find():
        print(f"   - {team['name']} ({team['_id']}) - Skills: {len(team['skills'])}")


if __name__ == "__main__":
    asyncio.run(seed_users())
