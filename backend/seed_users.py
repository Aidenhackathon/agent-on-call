"""
Seed script to populate MongoDB with sample teams for testing.
Run this once to initialize the users collection.
"""
import asyncio
from database import connect_to_mongo, get_users_collection


async def seed_users():
    """Seed the users collection with teams (departments) and their skills."""
    await connect_to_mongo()
    
    users_collection = get_users_collection()
    
    # Clear existing users (for testing)
    await users_collection.delete_many({})
    
    # Teams with department name and skills only
    teams = [
        {
            "_id": "frontend_development",
            "name": "Frontend Development",
            "skills": [
                "react", "javascript", "typescript", "css", "html", "ui", "ux", "frontend", 
                "vue", "angular", "nextjs", "svelte", "webpack", "vite", "tailwind", "bootstrap",
                "responsive design", "accessibility", "performance", "browser compatibility",
                "component library", "state management", "redux", "context api", "hooks",
                "frontend architecture", "spa", "pwa", "ui bugs","ui down", "display issues", "rendering"
            ]
        },
        {
            "_id": "backend_development",
            "name": "Backend Development",
            "skills": [
                "python", "fastapi", "django", "flask", "nodejs", "express", "java", "spring",
                "mongodb", "postgresql", "mysql", "redis", "database", "api", "rest", "graphql",
                "microservices", "backend", "server", "authentication", "authorization",
                "api errors", "server errors", "database problems", "performance", "scalability",
                "backend architecture", "caching", "message queue", "webhooks", "integration"
            ]
        },
        {
            "_id": "product_management",
            "name": "Product Management",
            "skills": [
                "product", "feature", "roadmap", "product strategy", "requirements", "user stories",
                "prioritization", "analytics", "metrics", "enhancement", "improvement",
                "design", "planning", "wireframes", "prototyping", "user research",
                "product backlog", "sprint planning", "agile", "scrum", "kanban",
                "feature requests", "product questions", "user feedback", "competitor analysis"
            ]
        },
        {
            "_id": "business_operations",
            "name": "Business / Operations",
            "skills": [
                "operations", "business", "process", "workflow", "efficiency", "automation",
                "operations management", "business process", "sop", "documentation",
                "vendor management", "procurement", "supply chain", "logistics",
                "business strategy", "kpi", "reporting", "dashboard", "analytics",
                "operations issues", "process improvement", "compliance", "audit"
            ]
        },
        {
            "_id": "human_resources",
            "name": "Human Resources (HR)",
            "skills": [
                "hr", "human resources", "recruitment", "hiring", "onboarding", "offboarding",
                "employee relations", "performance management", "compensation", "benefits",
                "payroll", "time tracking", "leave management", "policies", "procedures",
                "employee handbook", "training", "development", "career development",
                "hr policies", "employee issues", "workplace", "culture", "diversity"
            ]
        },
        {
            "_id": "finance_accounting",
            "name": "Finance / Accounting",
            "skills": [
                "finance", "accounting", "billing", "payment", "invoice", "invoice processing",
                "stripe", "paypal", "payment gateway", "refund", "reimbursement",
                "pricing", "subscription", "revenue", "expenses", "budget", "forecasting",
                "financial reporting", "tax", "accounting software", "quickbooks", "xero",
                "billing questions", "payment issues", "invoice errors", "financial data"
            ]
        },
        {
            "_id": "sales",
            "name": "Sales",
            "skills": [
                "sales", "selling", "lead generation", "prospecting", "crm", "salesforce",
                "quotation", "proposal", "deal", "opportunity", "pipeline", "forecasting",
                "contract", "negotiation", "pricing", "discount", "trial", "demo",
                "sales process", "account management", "customer acquisition", "retention",
                "sales questions", "quotes", "pricing inquiries", "contract issues"
            ]
        },
        {
            "_id": "marketing",
            "name": "Marketing",
            "skills": [
                "marketing", "advertising", "campaign", "social media", "content marketing",
                "seo", "sem", "ppc", "email marketing", "newsletter", "blog", "content",
                "branding", "brand", "messaging", "positioning", "market research",
                "analytics", "tracking", "conversion", "lead generation", "crm",
                "marketing campaigns", "advertising issues", "brand questions", "content requests"
            ]
        },
        {
            "_id": "customer_support",
            "name": "Customer Support / Customer Success",
            "skills": [
                "customer support", "customer service", "customer success", "support",
                "help desk", "troubleshooting", "ticket management", "zendesk", "intercom",
                "onboarding", "training", "documentation", "faq", "knowledge base",
                "customer questions", "general inquiries", "account issues", "guidance",
                "technical support", "product support", "user assistance", "escalation","i don't know"
            ]
        },
        {
            "_id": "devops_team",
            "name": "DevOps Team",
            "skills": [
             "infrastructure", "server", "networking", "cloud", "aws", "azure", "gcp",
                "kubernetes", "docker", "containerization", "ci/cd", "deployment", "devops",
                "monitoring", "logging", "alerting", "terraform", "ansible", "infrastructure as code",
                "system outage", "server down", "infrastructure issues", "deployment problems",
                "network issues", "ssl", "dns", "load balancing", "scalability", "uptime"
            ]
        },
        {
            "_id": "legal_compliance",
            "name": "Legal & Compliance",
            "skills": [
                "legal", "compliance", "law", "regulations", "gdpr", "privacy", "data protection",
                "terms of service", "privacy policy", "contract", "agreement", "nda",
                "intellectual property", "ip", "trademark", "copyright", "patent",
                "regulatory compliance", "audit", "risk management", "legal review",
                "legal questions", "compliance issues", "privacy concerns", "data breach"
            ]
        }
    ]
    
    # Insert teams into database
    result = await users_collection.insert_many(teams)
    print(f"Seeded {len(result.inserted_ids)} teams to MongoDB")
    
    # Display summary
    count = await users_collection.count_documents({})
    print(f"\nTotal teams in database: {count}\n")
    
    print("Teams with skills:")
    async for team in users_collection.find():
        skills_count = len(team.get('skills', []))
        print(f"  - {team['name']}: {skills_count} skills")


if __name__ == "__main__":
    asyncio.run(seed_users())
