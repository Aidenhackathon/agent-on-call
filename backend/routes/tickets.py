from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
from bson import ObjectId
import pytz

from schemas import TicketCreate, TicketUpdate, TicketResponse, TriageResponse
from database import get_tickets_collection, get_activity_logs_collection
from services.ai_triage import perform_triage
from models import Activity, get_ist_now
from triage import create_triage_graph

# IST timezone
ist = pytz.timezone('Asia/Kolkata')

router = APIRouter()
def ticket_helper(ticket) -> dict:
    """Convert MongoDB document to dict."""
    if ticket:
        ticket["id"] = str(ticket["_id"])
        ticket.pop("_id", None)
        # Ensure datetime fields are properly formatted with timezone info
        # MongoDB may return naive datetimes, so we ensure they're timezone-aware
        
        datetime_fields = ['created_at', 'updated_at']
        for field in datetime_fields:
            if field in ticket and ticket[field]:
                if isinstance(ticket[field], datetime):
                    # If datetime is naive (no timezone), assume it's IST
                    if ticket[field].tzinfo is None:
                        ticket[field] = ist.localize(ticket[field])
                    # Convert to IST if it has a different timezone
                    elif ticket[field].tzinfo != ist:
                        ticket[field] = ticket[field].astimezone(ist)
        
        # Handle activities timestamps
        if 'activities' in ticket and ticket['activities']:
            for activity in ticket['activities']:
                if 'timestamp' in activity and activity['timestamp']:
                    # Handle datetime objects
                    if isinstance(activity['timestamp'], datetime):
                        if activity['timestamp'].tzinfo is None:
                            activity['timestamp'] = ist.localize(activity['timestamp'])
                        elif activity['timestamp'].tzinfo != ist:
                            activity['timestamp'] = activity['timestamp'].astimezone(ist)
                        # Ensure it's serialized as ISO string with timezone
                        activity['timestamp'] = activity['timestamp'].isoformat()
                    # Handle string timestamps (already ISO formatted)
                    elif isinstance(activity['timestamp'], str):
                        # If it's already a string, try to parse and ensure it's in IST
                        try:
                            # Parse the string to datetime
                            parsed_dt = datetime.fromisoformat(activity['timestamp'].replace('Z', '+00:00'))
                            if parsed_dt.tzinfo is None:
                                parsed_dt = ist.localize(parsed_dt)
                            else:
                                parsed_dt = parsed_dt.astimezone(ist)
                            activity['timestamp'] = parsed_dt.isoformat()
                        except (ValueError, AttributeError):
                            # If parsing fails, keep the original string
                            pass
    
        # Convert datetime fields to ISO strings for JSON serialization
        for field in datetime_fields:
            if field in ticket and ticket[field] and isinstance(ticket[field], datetime):
                ticket[field] = ticket[field].isoformat()
        
        # Ensure ai_rationale is always a string (not an object)
        if 'ai_rationale' in ticket and ticket['ai_rationale']:
            if not isinstance(ticket['ai_rationale'], str):
                # If it's a dict/object, try to combine priority_rationale and assignee_rationale
                if isinstance(ticket['ai_rationale'], dict):
                    priority_rationale = ticket['ai_rationale'].get('priority_rationale', '')
                    assignee_rationale = ticket['ai_rationale'].get('assignee_rationale', '')
                    if priority_rationale and assignee_rationale:
                        ticket['ai_rationale'] = f"{priority_rationale} | {assignee_rationale}"
                    else:
                        ticket['ai_rationale'] = priority_rationale or assignee_rationale or ''
                else:
                    ticket['ai_rationale'] = str(ticket['ai_rationale'])
    
    return ticket

@router.post("", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket: TicketCreate):
    """Create a new ticket."""
    collection = get_tickets_collection()
    
    ticket_dict = ticket.dict()
    # Ensure category has a default value if not provided
    if not ticket_dict.get("category"):
        ticket_dict["category"] = "General"
    
    ticket_dict.update({
        "status": "open",
        "priority": None,
        "assignee": None,
        "assignee_user_id": None,
        "ai_rationale": None,
        "ai_reply_draft": None,
        "ai_confidence": None,
        "created_at": get_ist_now(),
        "updated_at": get_ist_now(),
        "activities": [{
            "timestamp": get_ist_now(),
            "action": "created",
            "details": "Ticket created",
            "user": "system"
        }]
    })
    
    result = await collection.insert_one(ticket_dict)
    created_ticket = await collection.find_one({"_id": result.inserted_id})
    
    return ticket_helper(created_ticket)

@router.get("", response_model=List[TicketResponse])
async def list_tickets():
    """List all tickets."""
    collection = get_tickets_collection()
    tickets = []
    
    async for ticket in collection.find().sort("created_at", -1):
        tickets.append(ticket_helper(ticket))
    
    return tickets

@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: str):
    """Get a single ticket by ID."""
    from database import _recreate_client
    
    if not ObjectId.is_valid(ticket_id):
        raise HTTPException(status_code=400, detail="Invalid ticket ID format")
    
    # Get ticket - retry if event loop is closed
    collection = get_tickets_collection()
    try:
        ticket = await collection.find_one({"_id": ObjectId(ticket_id)})
    except RuntimeError as e:
        if "Event loop is closed" in str(e):
            _recreate_client()
            collection = get_tickets_collection()
            ticket = await collection.find_one({"_id": ObjectId(ticket_id)})
        else:
            raise
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return ticket_helper(ticket)

@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(ticket_id: str, ticket_update: TicketUpdate):
    """Update a ticket."""
    from database import _recreate_client
    
    if not ObjectId.is_valid(ticket_id):
        raise HTTPException(status_code=400, detail="Invalid ticket ID format")
    
    # Get existing ticket - retry if event loop is closed
    collection = get_tickets_collection()
    try:
        existing_ticket = await collection.find_one({"_id": ObjectId(ticket_id)})
    except RuntimeError as e:
        if "Event loop is closed" in str(e):
            _recreate_client()
            collection = get_tickets_collection()
            existing_ticket = await collection.find_one({"_id": ObjectId(ticket_id)})
        else:
            raise
    if not existing_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Prepare update data
    update_data = {k: v for k, v in ticket_update.dict().items() if v is not None}
    
    if update_data:
        update_data["updated_at"] = get_ist_now()
        
        # Add activity log
        activity = {
            "timestamp": get_ist_now(),
            "action": "updated",
            "details": f"Updated fields: {', '.join(update_data.keys())}",
            "user": "user"
        }
        
        await collection.update_one(
            {"_id": ObjectId(ticket_id)},
            {
                "$set": update_data,
                "$push": {"activities": activity}
            }
        )
    
    # Return updated ticket
    updated_ticket = await collection.find_one({"_id": ObjectId(ticket_id)})
    return ticket_helper(updated_ticket)

@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(ticket_id: str):
    """Delete a ticket."""
    from database import _recreate_client
    
    if not ObjectId.is_valid(ticket_id):
        raise HTTPException(status_code=400, detail="Invalid ticket ID format")
    
    # Delete ticket - retry if event loop is closed
    collection = get_tickets_collection()
    try:
        result = await collection.delete_one({"_id": ObjectId(ticket_id)})
    except RuntimeError as e:
        if "Event loop is closed" in str(e):
            _recreate_client()
            collection = get_tickets_collection()
            result = await collection.delete_one({"_id": ObjectId(ticket_id)})
        else:
            raise
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return None

@router.post("/{ticket_id}/triage", response_model=TriageResponse)
async def triage_ticket(ticket_id: str):
    """
    Trigger AI triage for a ticket using LangGraph multi-agent workflow.
    
    Flow: ContextDetailer → PriorityAgent → AssigneeAgent → RationaleAgent → ReplyAgent → PersistNode
    """
    from database import _recreate_client
    
    if not ObjectId.is_valid(ticket_id):
        raise HTTPException(status_code=400, detail="Invalid ticket ID format")
    
    # Get ticket from MongoDB - retry if event loop is closed
    collection = get_tickets_collection()
    try:
        ticket = await collection.find_one({"_id": ObjectId(ticket_id)})
    except RuntimeError as e:
        if "Event loop is closed" in str(e):
            _recreate_client()
            collection = get_tickets_collection()
            ticket = await collection.find_one({"_id": ObjectId(ticket_id)})
        else:
            raise
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Ensure database client is recreated before LangGraph workflow
    # This ensures Motor uses the correct event loop for workflow operations
    _recreate_client()
    
    try:
        # Create LangGraph workflow
        graph = create_triage_graph()
        
        # Initialize state with ticket
        initial_state = {
            "ticket": ticket,
            "context": None,
            "priority": None,
            "assignee": None,
            "rationale": None,
            "reply": None,
            "error": None
        }
        
        # Run multi-agent workflow
        final_state = await graph.ainvoke(initial_state)
        
        # Check for errors
        if final_state.get("error"):
            raise Exception(final_state["error"])
        
        # Extract results
        priority_info = final_state.get("priority", {})
        assignee_info = final_state.get("assignee", {})
        rationale_info = final_state.get("rationale", {})
        reply = final_state.get("reply", "")
        
        # Combine rationales from RationaleAgent
        priority_rationale = rationale_info.get("priority_rationale", "")
        assignee_rationale = rationale_info.get("assignee_rationale", "")
        combined_rationale = f"{priority_rationale} | {assignee_rationale}" if priority_rationale and assignee_rationale else (priority_rationale or assignee_rationale)
        
        # Return triage response (persist_node already updated MongoDB)
        return TriageResponse(
            priority=priority_info.get("priority", "P3"),
            confidence=priority_info.get("confidence", 0.0),
            assignee=assignee_info.get("assignee_user_id", "unassigned"),
            rationale=combined_rationale,
            reply_draft=reply
        )
        
    except Exception as e:
        # Log error to activity_logs
        try:
            activity_logs_collection = get_activity_logs_collection()
            await activity_logs_collection.insert_one({
                "ticket_id": str(ticket_id),
                "event_type": "triage_failed",
                "payload": {"error": str(e)},
                "timestamp": get_ist_now()
            })
        except:
            pass
        
        raise HTTPException(
            status_code=500,
            detail=f"AI triage failed: {str(e)}"
        )
