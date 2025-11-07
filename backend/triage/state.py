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
    rationale: Optional[dict]  # Contains priority_rationale and assignee_rationale
    reply: Optional[str]
    error: Optional[str]
