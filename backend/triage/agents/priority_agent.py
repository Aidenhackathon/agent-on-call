"""
PriorityAgent - Determines ticket priority using heuristics + Gemini AI.
"""
import os
import json
from typing import Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from triage.state import TriageState


# Initialize Gemini LLM
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_MOCK = os.getenv("USE_MOCK_AI", "false").lower() == "true"

llm = None
if GEMINI_API_KEY and not USE_MOCK:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        api_key=GEMINI_API_KEY,
        temperature=0.2
    )


async def priority_agent(state: TriageState) -> TriageState:
    """
    Determine ticket priority using heuristics first, then Gemini confirmation.
    
    Returns:
        {
            "priority": "P0|P1|P2|P3",
            "confidence": float
        }
    """
    try:
        context = state.get("context", {})
        if not context:
            state["error"] = "No context available for PriorityAgent"
            return state
        
        title = context.get("title", "").lower()
        body = context.get("body", "").lower()
        tags = [t.lower() for t in context.get("tags", [])]
        combined_text = f"{title} {body} {' '.join(tags)}"
        
        # HEURISTICS FIRST
        heuristic_priority = _apply_heuristics(combined_text)
        
        # Use Gemini for validation/refinement if available
        if llm and not USE_MOCK:
            priority_result = await _gemini_priority(context, heuristic_priority)
        else:
            priority_result = {
                "priority": heuristic_priority,
                "confidence": 0.85
            }
        
        state["priority"] = priority_result
        return state
        
    except Exception as e:
        state["error"] = f"PriorityAgent error: {str(e)}"
        return state


def _apply_heuristics(text: str) -> str:
    """Apply heuristic rules to determine initial priority."""
    # P0 keywords
    if any(keyword in text for keyword in [
        "payment failed", "site down", "outage", "security breach", 
        "data loss", "critical error", "production down", "cannot access"
    ]):
        return "P0"
    
    # P1 keywords
    if any(keyword in text for keyword in [
        "api error", "broken", "not working", "urgent", "major bug",
        "customer facing", "revenue impact"
    ]):
        return "P1"
    
    # P2 keywords
    if any(keyword in text for keyword in [
        "minor bug", "issue", "problem", "billing question",
        "feature not working", "workaround available"
    ]):
        return "P2"
    
    # Default P3
    return "P3"


async def _gemini_priority(context: Dict, heuristic_priority: str) -> Dict:
    """Use Gemini to validate/refine priority."""
    prompt = f"""You are a ticket triage expert. Analyze this ticket and confirm or adjust the priority.

Ticket Title: {context.get('title', '')}
Ticket Body: {context.get('body', '')}
Tags: {', '.join(context.get('tags', []))}
Heuristic Suggestion: {heuristic_priority}

Priority Guidelines:
- P0: Critical system outage, security breach, data loss, payment failures
- P1: Major functionality broken, significant user impact, API errors
- P2: Moderate issues, workarounds available, billing questions
- P3: Minor issues, feature requests, general questions

Respond in JSON format:
{{
    "priority": "P0|P1|P2|P3",
    "confidence": <float 0-1>
}}

Only return priority and confidence - no rationale needed."""
    
    try:
        response = await llm.ainvoke(prompt)
        result_text = response.content.strip()
        
        # Clean JSON from markdown
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(result_text)
        
        # Validate
        if result.get("priority") not in ["P0", "P1", "P2", "P3"]:
            result["priority"] = heuristic_priority
        
        result["confidence"] = float(result.get("confidence", 0.8))
        
        # Remove rationale if present
        result.pop("rationale", None)
        
        return result
        
    except Exception as e:
        print(f"Gemini priority error: {e}")
        return {
            "priority": heuristic_priority,
            "confidence": 0.75
        }
