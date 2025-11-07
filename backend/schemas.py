from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TicketCreate(BaseModel):
    """Schema for creating a ticket."""
    title: str
    description: str
    category: Optional[str] = "General"  # Default category, can be auto-detected later
    product_area: Optional[str] = None
    tags: List[str] = []

class TicketUpdate(BaseModel):
    """Schema for updating a ticket."""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee: Optional[str] = None
    assignee_user_id: Optional[str] = None
    product_area: Optional[str] = None
    tags: Optional[List[str]] = None
    ai_reply_draft: Optional[str] = None

class ActivityResponse(BaseModel):
    """Schema for activity response."""
    timestamp: datetime
    action: str
    details: str
    user: str

class TicketResponse(BaseModel):
    """Schema for ticket response."""
    id: str
    title: str
    description: str
    category: str
    status: str
    priority: Optional[str] = None
    assignee: Optional[str] = None
    assignee_user_id: Optional[str] = None
    product_area: Optional[str] = None
    tags: List[str] = []
    ai_rationale: Optional[str] = None
    ai_reply_draft: Optional[str] = None
    ai_confidence: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    activities: List[ActivityResponse] = []

class TriageResponse(BaseModel):
    """Schema for triage response."""
    priority: str
    confidence: float
    assignee: str
    rationale: str
    reply_draft: str
