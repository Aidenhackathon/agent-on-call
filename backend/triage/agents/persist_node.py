"""
PersistNode - Writes triage results to MongoDB.
"""
from datetime import datetime
from bson import ObjectId
from models import get_ist_now
from database import (
    get_tickets_collection,
    get_triage_results_collection,
    get_activity_logs_collection,
    get_users_collection
)
from triage.state import TriageState


async def persist_node(state: TriageState) -> TriageState:
    """
    Persist triage results to MongoDB:
    1. Update ticket (priority, assignee_user_id, status)
    2. Insert triage_results document
    3. Insert activity_log
    
    Returns final state.
    """
    try:
        ticket = state.get("ticket")
        priority_info = state.get("priority", {})
        assignee_info = state.get("assignee", {})
        rationale_info = state.get("rationale", {})
        reply = state.get("reply", "")
        
        if not ticket or not ticket.get("_id"):
            state["error"] = "No ticket to persist"
            return state
        
        # Ensure assignee_info is not None
        if assignee_info is None:
            assignee_info = {}
        
        # Ensure rationale_info is not None
        if rationale_info is None:
            rationale_info = {}
        
        ticket_id = ticket["_id"]
        now = get_ist_now()
        
        # 1. UPDATE TICKET
        tickets_collection = get_tickets_collection()
        
        # Get team name for display (old 'assignee' field)
        assignee_user_id = assignee_info.get("assignee_user_id", "unassigned")
        assignee_name = assignee_user_id  # Default to team_id
        
        # Try to fetch team name from users collection
        if assignee_user_id and assignee_user_id != "unassigned":
            users_collection = get_users_collection()
            team = await users_collection.find_one({"_id": assignee_user_id})
            if team:
                assignee_name = team.get("name", assignee_user_id)
        
        # Combine rationales from RationaleAgent
        priority_rationale = rationale_info.get("priority_rationale", "")
        assignee_rationale = rationale_info.get("assignee_rationale", "")
        combined_rationale = f"{priority_rationale} | {assignee_rationale}" if priority_rationale and assignee_rationale else (priority_rationale or assignee_rationale)
        
        update_fields = {
            # New fields for multi-agent system
            "priority": priority_info.get("priority", "P3"),
            "assignee_user_id": assignee_user_id,
            "status": "triaged",
            "updated_at": now,
            # Legacy fields for frontend compatibility
            "assignee": assignee_name,
            "ai_rationale": combined_rationale,
            "ai_reply_draft": reply,
            "ai_confidence": priority_info.get("confidence", 0.0)
        }
        
        await tickets_collection.update_one(
            {"_id": ticket_id},
            {"$set": update_fields}
        )
        
        # 2. INSERT TRIAGE_RESULTS
        triage_results_collection = get_triage_results_collection()
        
        triage_result_doc = {
            "ticket_id": str(ticket_id),
            "priority": priority_info.get("priority", "P3"),
            "priority_confidence": priority_info.get("confidence", 0.0),
            "priority_rationale": priority_rationale,
            "assignee_user_id": assignee_info.get("assignee_user_id"),
            "assignee_rationale": assignee_rationale,
            "reply_draft": reply,
            "created_at": now
        }
        
        await triage_results_collection.insert_one(triage_result_doc)
        
        # 3. INSERT ACTIVITY_LOG
        activity_logs_collection = get_activity_logs_collection()
        
        activity_log_doc = {
            "ticket_id": str(ticket_id),
            "event_type": "triage_run",
            "payload": {
                "priority": priority_info.get("priority"),
                "assignee": assignee_info.get("assignee_user_id"),
                "confidence": priority_info.get("confidence")
            },
            "timestamp": now
        }
        
        await activity_logs_collection.insert_one(activity_log_doc)
        
        # Success - no error
        state["error"] = None
        return state
        
    except Exception as e:
        state["error"] = f"PersistNode error: {str(e)}"
        
        # Log failure to activity_logs
        try:
            activity_logs_collection = get_activity_logs_collection()
            await activity_logs_collection.insert_one({
                "ticket_id": str(ticket.get("_id", "unknown")),
                "event_type": "triage_failed",
                "payload": {"error": str(e)},
                "timestamp": get_ist_now()
            })
        except:
            pass
        
        return state
