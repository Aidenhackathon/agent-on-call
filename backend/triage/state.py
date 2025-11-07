"""
TriageState - State model for LangGraph multi-agent workflow.
"""
from typing import Optional, TypedDict


class TriageState(TypedDict, total=False):
    """State passed between agents in the triage workflow."""
    ticket: Optional[dict]
    context: Optional[dict]
    priority: Optional[dict]
    assignee: Optional[dict]
    reply: Optional[str]
    error: Optional[str]
