"""
ReplyAgent - Generates customer reply draft (≤120 words) using Gemini.
"""
import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from triage.state import TriageState


# Initialize Gemini LLM
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_MOCK = os.getenv("USE_MOCK_AI", "false").lower() == "true"

llm = None
if GEMINI_API_KEY and not USE_MOCK:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=GEMINI_API_KEY,
        temperature=0.2
    )


async def reply_agent(state: TriageState) -> TriageState:
    """
    Generate a customer reply draft using Gemini.
    
    STRICT REQUIREMENT: Reply must be ≤120 words.
    
    Returns:
        state with reply: str
    """
    try:
        context = state.get("context", {})
        priority_info = state.get("priority", {})
        assignee_info = state.get("assignee", {})
        
        if not context:
            state["error"] = "No context available for ReplyAgent"
            return state
        
        # Use Gemini for reply generation
        if llm and not USE_MOCK:
            reply = await _gemini_reply(context, priority_info, assignee_info)
        else:
            reply = _mock_reply(context, priority_info, assignee_info)
        
        state["reply"] = reply
        return state
        
    except Exception as e:
        state["error"] = f"ReplyAgent error: {str(e)}"
        return state


async def _gemini_reply(context: dict, priority_info: dict, assignee_info: dict) -> str:
    """Generate reply using Gemini with strict 120-word limit."""
    
    priority = priority_info.get("priority", "P3")
    title = context.get("title", "")
    body = context.get("body", "")
    
    prompt = f"""You are a professional customer support agent. Write a friendly first reply to this ticket.

Ticket Title: {title}
Ticket Body: {body}
Priority: {priority}

CRITICAL REQUIREMENTS:
1. Maximum 120 words (STRICT LIMIT)
2. Professional and empathetic tone
3. Acknowledge the issue
4. Set expectations based on priority:
   - P0: Immediate escalation, updates every 30 min
   - P1: High priority, update in 2-4 hours
   - P2: Standard review, response in 24-48 hours
   - P3: Normal queue, response in 2-3 business days
5. Sign off professionally

Respond ONLY with the reply text (no JSON, no extra formatting).
Word count must be ≤120 words."""
    
    try:
        response = await llm.ainvoke(prompt)
        reply_text = response.content.strip()
        
        # Ensure word count ≤120
        words = reply_text.split()
        if len(words) > 120:
            reply_text = " ".join(words[:120]) + "..."
        
        return reply_text
        
    except Exception as e:
        print(f"Gemini reply error: {e}")
        return _mock_reply(context, priority_info, assignee_info)


def _mock_reply(context: dict, priority_info: dict, assignee_info: dict) -> str:
    """Generate mock reply for testing."""
    
    priority = priority_info.get("priority", "P3")
    
    if priority == "P0":
        return (
            "Hello,\n\n"
            "Thank you for reporting this critical issue. We have immediately escalated this "
            "to our engineering team and they are actively investigating. We will provide "
            "updates every 30 minutes until resolved. We sincerely apologize for the inconvenience.\n\n"
            "Best regards,\n"
            "Support Team"
        )
    elif priority == "P1":
        return (
            "Hello,\n\n"
            "Thank you for bringing this to our attention. We have flagged this as high priority "
            "and our team is investigating now. We aim to provide an update within 2-4 hours. "
            "We appreciate your patience as we work to resolve this quickly.\n\n"
            "Best regards,\n"
            "Support Team"
        )
    elif priority == "P2":
        return (
            "Hello,\n\n"
            "Thank you for contacting us. We have received your request and assigned it to "
            "our team for review. They will investigate and respond within 24-48 hours. "
            "If you have additional information, please feel free to add it here.\n\n"
            "Best regards,\n"
            "Support Team"
        )
    else:  # P3
        return (
            "Hello,\n\n"
            "Thank you for reaching out. We have received your request and our team will "
            "review it. We typically respond to requests like this within 2-3 business days. "
            "We appreciate your patience.\n\n"
            "Best regards,\n"
            "Support Team"
        )
