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
    4. Increment assignee workload
    
    Returns final state.
    """
    try:
        ticket = state.get("ticket")
        priority_info = state.get("priority", {})
        assignee_info = state.get("assignee", {})
        reply = state.get("reply", "")
        
        if not ticket or not ticket.get("_id"):
            state["error"] = "No ticket to persist"
            return state
        
        # Ensure assignee_info is not None
        if assignee_info is None:
            assignee_info = {}
        
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
        
        update_fields = {
            # New fields for multi-agent system
            "priority": priority_info.get("priority", "P3"),
            "assignee_user_id": assignee_user_id,
            "status": "triaged",
            "updated_at": now,
            # Legacy fields for frontend compatibility
            "assignee": assignee_name,
            "ai_rationale": f"{priority_info.get('rationale', '')} | {assignee_info.get('rationale', '')}",
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
            "priority_rationale": priority_info.get("rationale", ""),
            "assignee_user_id": assignee_info.get("assignee_user_id"),
            "assignee_rationale": assignee_info.get("rationale", ""),
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
        
        # 4. INCREMENT TEAM WORKLOAD
        assignee_user_id = assignee_info.get("assignee_user_id")
        if assignee_user_id and assignee_user_id != "unassigned":
            users_collection = get_users_collection()
            await users_collection.update_one(
                {"_id": assignee_user_id},
                {"$inc": {"workload": 1}}
            )
        
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
