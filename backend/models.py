from datetime import datetime
import pytz
from typing import Optional, List
from pydantic import BaseModel, Field

# Indian Standard Time (IST) timezone
ist = pytz.timezone('Asia/Kolkata')

def get_ist_now():
    """Get current time in IST."""
    return datetime.now(ist)

class TriageResult(BaseModel):
    """AI Triage result model."""
    priority: str
    confidence: float
    assignee: str
    rationale: str
    reply_draft: str

class Activity(BaseModel):
    """Activity log entry."""
    timestamp: datetime = Field(default_factory=get_ist_now)
    action: str
    details: str
    user: str = "system"

class Ticket(BaseModel):
    """Ticket model."""
    id: Optional[str] = None
    title: str
    description: str
    category: str
    status: str = "open"
    priority: Optional[str] = None
    assignee: Optional[str] = None
    assignee_user_id: Optional[str] = None  # New field for multi-agent
    product_area: Optional[str] = None  # New field for multi-agent
    tags: List[str] = []  # New field for multi-agent
    ai_rationale: Optional[str] = None
    ai_reply_draft: Optional[str] = None
    ai_confidence: Optional[float] = None
    created_at: datetime = Field(default_factory=get_ist_now)
    updated_at: datetime = Field(default_factory=get_ist_now)
    activities: List[Activity] = []

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
