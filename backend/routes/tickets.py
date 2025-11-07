from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
from bson import ObjectId

from schemas import TicketCreate, TicketUpdate, TicketResponse, TriageResponse
from database import get_tickets_collection, get_activity_logs_collection
from services.ai_triage import perform_triage
from models import Activity, get_ist_now
from triage import create_triage_graph

router = APIRouter()
def ticket_helper(ticket) -> dict:
    """Convert MongoDB document to dict."""
    if ticket:
        ticket["id"] = str(ticket["_id"])
        ticket.pop("_id", None)
    return ticket

@router.post("", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket: TicketCreate):
    """Create a new ticket."""
    collection = get_tickets_collection()
    
    ticket_dict = ticket.dict()
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
    collection = get_tickets_collection()
    
    if not ObjectId.is_valid(ticket_id):
        raise HTTPException(status_code=400, detail="Invalid ticket ID format")
    
    ticket = await collection.find_one({"_id": ObjectId(ticket_id)})
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return ticket_helper(ticket)

@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(ticket_id: str, ticket_update: TicketUpdate):
    """Update a ticket."""
    collection = get_tickets_collection()
    
    if not ObjectId.is_valid(ticket_id):
        raise HTTPException(status_code=400, detail="Invalid ticket ID format")
    
    # Get existing ticket
    existing_ticket = await collection.find_one({"_id": ObjectId(ticket_id)})
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
    collection = get_tickets_collection()
    
    if not ObjectId.is_valid(ticket_id):
        raise HTTPException(status_code=400, detail="Invalid ticket ID format")
    
    result = await collection.delete_one({"_id": ObjectId(ticket_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return None

@router.post("/{ticket_id}/triage", response_model=TriageResponse)
async def triage_ticket(ticket_id: str):
    """
    Trigger AI triage for a ticket using LangGraph multi-agent workflow.
    
    Flow: ContextAgent → PriorityAgent → AssigneeAgent → ReplyAgent → PersistNode
    """
    collection = get_tickets_collection()
    
    if not ObjectId.is_valid(ticket_id):
        raise HTTPException(status_code=400, detail="Invalid ticket ID format")
    
    # Get ticket from MongoDB
    ticket = await collection.find_one({"_id": ObjectId(ticket_id)})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    try:
        # Create LangGraph workflow
        graph = create_triage_graph()
        
        # Initialize state with ticket
        initial_state = {
            "ticket": ticket,
            "context": None,
            "priority": None,
            "assignee": None,
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
        reply = final_state.get("reply", "")
        
        # Return triage response (persist_node already updated MongoDB)
        return TriageResponse(
            priority=priority_info.get("priority", "P3"),
            confidence=priority_info.get("confidence", 0.0),
            assignee=assignee_info.get("assignee_user_id", "unassigned"),
            rationale=f"{priority_info.get('rationale', '')} | {assignee_info.get('rationale', '')}",
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
