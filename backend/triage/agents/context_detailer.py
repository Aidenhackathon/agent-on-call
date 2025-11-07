"""
ContextDetailer - Fetches and compresses ticket context from MongoDB.
"""
from typing import Dict
from database import get_tickets_collection, get_comments_collection, get_attachments_collection
from triage.state import TriageState


async def context_detailer(state: TriageState) -> TriageState:
    """
    Fetch ticket, comments, and attachments from MongoDB.
    Build compact context for downstream agents.
    """
    try:
        ticket = state.get("ticket")
        if not ticket or not ticket.get("_id"):
            state["error"] = "No ticket provided to ContextDetailer"
            return state
        
        ticket_id = str(ticket["_id"])
        
        # Fetch comments
        comments_collection = get_comments_collection()
        comments_cursor = comments_collection.find({"ticket_id": ticket_id}).sort("created_at", 1).limit(10)
        comments = []
        async for comment in comments_cursor:
            comments.append({
                "text": comment.get("text", ""),
                "created_at": comment.get("created_at").isoformat() if comment.get("created_at") else ""
            })
        
        # Fetch attachments (optional)
        attachments_collection = get_attachments_collection()
        attachments_cursor = attachments_collection.find({"ticket_id": ticket_id}).limit(5)
        attachments = []
        async for attachment in attachments_cursor:
            attachments.append({
                "filename": attachment.get("filename", ""),
                "size": attachment.get("size", 0)
            })
        
        # Build compact context
        # Handle both old (description) and new (body) field names
        body_text = ticket.get("body") or ticket.get("description", "")
        
        context = {
            "title": ticket.get("title", ""),
            "body": body_text,
            "tags": ticket.get("tags", []),
            "product_area": ticket.get("product_area", ticket.get("category", "")),
            "comments": comments,
            "attachments": attachments
        }
        
        state["context"] = context
        return state
        
    except Exception as e:
        state["error"] = f"ContextDetailer error: {str(e)}"
        return state

