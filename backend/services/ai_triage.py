import os
import google.generativeai as genai
from typing import Dict
import json


from models import get_ist_now

print("hit ",get_ist_now())

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_MOCK = os.getenv("USE_MOCK_AI", "false").lower() == "true"
print(GEMINI_API_KEY)

if GEMINI_API_KEY and not USE_MOCK:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    model = None

async def perform_triage(title: str, description: str, category: str) -> Dict:
    """
    Perform AI triage on a ticket using Gemini API.
    Returns priority, assignee, rationale, and reply draft.
    """
    
    # Mock fallback for development/testing
    if USE_MOCK or not GEMINI_API_KEY or not model:
        return _mock_triage(title, description, category)
    
    try:
        prompt = f"""
You are an expert helpdesk ticket triage system. Analyze the following ticket and provide triage recommendations.

Ticket Title: {title}
Description: {description}
Category: {category}

Please provide your response in the following JSON format:
{{
    "priority": "<P0, P1, P2, or P3>",
    "confidence": <float between 0 and 1>,
    "assignee": "<suggested team or role>",
    "rationale": "<brief explanation for priority and assignee>",
    "reply_draft": "<friendly first reply to customer, max 120 words>"
}}

Priority Guidelines:
- P0: Critical system outage, security breach, data loss - immediate attention
- P1: Major functionality broken, significant user impact - urgent
- P2: Moderate issues, workarounds available - normal priority
- P3: Minor issues, feature requests, questions - low priority

Assignee Guidelines:
- DevOps: Infrastructure, deployment, system outages
- Backend Support: API issues, server errors, database problems
- Frontend Support: UI bugs, display issues
- Finance: Billing, payments, invoicing
- Product: Feature requests, product questions
- Customer Support: General inquiries, account issues

Reply Draft Guidelines:
- Be professional and empathetic
- Acknowledge the issue
- Set expectations
- Keep it under 120 words
"""
        
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Extract JSON from markdown code blocks if present
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(result_text)
        
        # Validate response structure
        required_fields = ["priority", "confidence", "assignee", "rationale", "reply_draft"]
        if not all(field in result for field in required_fields):
            raise ValueError("Invalid response structure from AI")
        
        # Ensure confidence is a float
        result["confidence"] = float(result["confidence"])
        
        # Validate priority
        if result["priority"] not in ["P0", "P1", "P2", "P3"]:
            result["priority"] = "P2"  # Default fallback
        
        return result
        
    except Exception as e:
        print(f"AI Triage Error: {e}")
        # Fallback to mock on error
        return _mock_triage(title, description, category)

def _mock_triage(title: str, description: str, category: str) -> Dict:
    """
    Mock triage logic for testing and development.
    Provides sensible defaults based on keywords.
    """
    title_lower = title.lower()
    desc_lower = description.lower()
    combined = f"{title_lower} {desc_lower}"
    
    # Determine priority
    if any(word in combined for word in ["down", "outage", "broken", "not working", "crash", "critical", "urgent", "security"]):
        priority = "P0"
        confidence = 0.92
    elif any(word in combined for word in ["error", "bug", "issue", "problem", "fail"]):
        priority = "P1"
        confidence = 0.85
    elif any(word in combined for word in ["billing", "payment", "invoice", "charge"]):
        priority = "P2"
        confidence = 0.78
    else:
        priority = "P3"
        confidence = 0.75
    
    # Determine assignee
    if any(word in combined for word in ["website", "deploy", "server", "infra", "down", "outage"]):
        assignee = "DevOps"
        rationale = "Infrastructure and deployment related issue requiring immediate DevOps attention."
    elif any(word in combined for word in ["api", "backend", "database", "server error"]):
        assignee = "Backend Support"
        rationale = "Backend system issue affecting core functionality."
    elif any(word in combined for word in ["ui", "button", "display", "frontend", "page"]):
        assignee = "Frontend Support"
        rationale = "User interface issue affecting user experience."
    elif any(word in combined for word in ["billing", "payment", "invoice", "charge", "refund"]):
        assignee = "Finance"
        rationale = "Billing or payment related query requiring finance team review."
    elif any(word in combined for word in ["feature", "request", "enhancement", "suggest"]):
        assignee = "Product"
        rationale = "Feature request or product enhancement suggestion for product team evaluation."
    else:
        assignee = "Customer Support"
        rationale = "General inquiry suitable for customer support team."
    
    # Generate reply draft
    if priority == "P0":
        reply_draft = f"Hello,\n\nThank you for reporting this critical issue. We understand the urgency and have immediately escalated this to our {assignee} team. They are actively investigating and working on a resolution. We will provide updates every 30 minutes until this is resolved. We apologize for any inconvenience caused.\n\nBest regards,\nSupport Team"
    elif priority == "P1":
        reply_draft = f"Hello,\n\nThank you for bringing this to our attention. We've flagged this as a high-priority issue and our {assignee} team is investigating. We aim to provide an update within 2-4 hours. We appreciate your patience as we work to resolve this.\n\nBest regards,\nSupport Team"
    elif priority == "P2":
        reply_draft = f"Hello,\n\nThank you for contacting us. We've received your request and assigned it to our {assignee} team for review. They will investigate and respond within 24-48 hours. If you have any additional information, please feel free to add it to this ticket.\n\nBest regards,\nSupport Team"
    else:
        reply_draft = f"Hello,\n\nThank you for reaching out. We've received your request and our {assignee} team will review it. We typically respond to requests like this within 2-3 business days. We appreciate your patience.\n\nBest regards,\nSupport Team"
    
    return {
        "priority": priority,
        "confidence": confidence,
        "assignee": assignee,
        "rationale": rationale,
        "reply_draft": reply_draft
    }
