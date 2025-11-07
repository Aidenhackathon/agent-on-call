"""
LangGraph workflow definition for multi-agent ticket triage.
"""
from langgraph.graph import StateGraph, END
from triage.state import TriageState
from triage.agents.context_agent import context_agent
from triage.agents.priority_agent import priority_agent
from triage.agents.assignee_agent import assignee_agent
from triage.agents.reply_agent import reply_agent
from triage.agents.persist_node import persist_node


def create_triage_graph():
    """
    Create and compile the LangGraph triage workflow.
    
    Flow:
        context_agent → priority_agent → assignee_agent → reply_agent → persist_node → END
    """
    
    # Initialize graph with state schema
    workflow = StateGraph(TriageState)
    
    # Add nodes (using unique names that don't conflict with state keys)
    workflow.add_node("fetch_context", context_agent)
    workflow.add_node("determine_priority", priority_agent)
    workflow.add_node("assign_user", assignee_agent)
    workflow.add_node("generate_reply", reply_agent)
    workflow.add_node("save_results", persist_node)
    
    # Define edges (sequential flow)
    workflow.set_entry_point("fetch_context")
    workflow.add_edge("fetch_context", "determine_priority")
    workflow.add_edge("determine_priority", "assign_user")
    workflow.add_edge("assign_user", "generate_reply")
    workflow.add_edge("generate_reply", "save_results")
    workflow.add_edge("save_results", END)
    
    # Compile graph
    graph = workflow.compile()
    
    return graph
