"""
AssigneeAgent - Assigns ticket to best user based on skills and context only.
"""
import os
import json
from typing import Dict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from database import get_users_collection
from triage.state import TriageState


# Initialize Gemini LLM
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_MOCK = os.getenv("USE_MOCK_AI", "false").lower() == "true"

llm = None
if GEMINI_API_KEY and not USE_MOCK:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=GEMINI_API_KEY,
        temperature=0.2
    )


async def assignee_agent(state: TriageState) -> TriageState:
    """
    Determine best team assignment based on:
    1. Skill matching with ticket context
    2. Gemini AI selection (if available)
    
    Returns:
        {
            "assignee_user_id": str  # team_id
        }
    """
    try:
        context = state.get("context", {})
        priority_info = state.get("priority", {})
        
        if not context:
            state["error"] = "No context available for AssigneeAgent"
            return state
        
        # Check if title and description are ambiguous - route to customer support if so
        title = context.get("title", "").strip()
        body = context.get("body", "").strip()
        
        is_ambiguous = await _check_ambiguity(title, body)
        if is_ambiguous:
            state["assignee"] = {
                "assignee_user_id": "customer_support"
            }
            return state
        
        # Fetch all teams from MongoDB
        users_collection = get_users_collection()
        users_cursor = users_collection.find({})
        teams = []
        async for team in users_cursor:
            teams.append({
                "user_id": team["_id"],
                "name": team.get("name", ""),
                "skills": team.get("skills", [])
            })
        
        if not teams:
            # Fallback if no teams in DB
            state["assignee"] = {
                "assignee_user_id": "unassigned"
            }
            return state
        
        # Score teams by skill match only (no workload consideration)
        scored_teams = _score_users(teams, context, priority_info)
        
        # Use Gemini to make final selection
        if llm and not USE_MOCK:
            assignee_result = await _gemini_assignee(context, priority_info, scored_teams)
        else:
            # Pick top scorer
            best_team = scored_teams[0]
            assignee_result = {
                "assignee_user_id": best_team["user_id"]
            }
        
        state["assignee"] = assignee_result
        return state
        
    except Exception as e:
        print(f"⚠️  AssigneeAgent Exception: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        state["error"] = f"AssigneeAgent error: {str(e)}"
        state["assignee"] = {
            "assignee_user_id": "unassigned"
        }
        return state


async def _check_ambiguity(title: str, body: str) -> bool:
    """
    Check if ticket title and description are ambiguous.
    Returns True if ambiguous (should route to customer support).
    """
    # Basic heuristic check
    is_ambiguous_heuristic = _check_ambiguity_heuristic(title, body)
    
    # Use Gemini for validation if available
    if llm and not USE_MOCK:
        try:
            is_ambiguous = await _gemini_clarity_check(title, body, is_ambiguous_heuristic)
            return is_ambiguous
        except Exception as e:
            print(f"Gemini clarity check error: {e}")
            return is_ambiguous_heuristic
    
    return is_ambiguous_heuristic


def _check_ambiguity_heuristic(title: str, body: str) -> bool:
    """
    Heuristic check for ambiguous tickets.
    Returns True if ticket appears ambiguous.
    """
    # Check if title or body is too short
    if len(title) < 5 or len(body) < 10:
        return True
    
    # Check for vague phrases
    vague_phrases = [
        "i don't know", "not sure", "maybe", "i think", "something",
        "help", "issue", "problem", "broken", "doesn't work",
        "not working", "error", "bug", "question", "?"
    ]
    
    title_lower = title.lower()
    body_lower = body.lower()
    
    # If title is very vague and body doesn't add clarity
    vague_title_count = sum(1 for phrase in vague_phrases if phrase in title_lower)
    if vague_title_count >= 2 and len(body) < 50:
        return True
    
    # If body is very short and vague
    if len(body) < 30 and any(phrase in body_lower for phrase in vague_phrases[:5]):
        return True
    
    # If title is just "help" or similar with minimal body
    if title_lower in ["help", "issue", "problem", "error", "bug", "question"] and len(body) < 40:
        return True
    
    return False


async def _gemini_clarity_check(title: str, body: str, heuristic_ambiguous: bool) -> bool:
    """Use Gemini to check if ticket is clear and unambiguous."""
    prompt = f"""You are a ticket triage expert. Analyze if this ticket's title and description are clear and unambiguous.

Ticket Title: {title}
Ticket Description: {body}

A ticket is considered AMBIGUOUS if:
1. The title is too vague (e.g., "help", "issue", "problem", "error" without context)
2. The description lacks sufficient detail to understand what the customer needs
3. The description is too short or doesn't explain the actual problem
4. It's unclear what the customer is asking for or what problem they're experiencing
5. The ticket lacks specific details about the issue

A ticket is considered CLEAR if:
1. The title is specific and descriptive
2. The description provides enough context to understand the issue
3. It's clear what the customer needs or what problem they're facing
4. There are enough details to route the ticket to the appropriate team

Heuristic Suggestion: {"AMBIGUOUS" if heuristic_ambiguous else "CLEAR"}

Respond in JSON format:
{{
    "is_ambiguous": <true if ambiguous, false if clear>
}}

Only return is_ambiguous - true if the ticket should be routed to customer support for clarification."""
    
    try:
        response = await llm.ainvoke(prompt)
        result_text = response.content.strip()
        
        # Clean JSON from markdown
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(result_text)
        return bool(result.get("is_ambiguous", heuristic_ambiguous))
        
    except Exception as e:
        print(f"Gemini clarity check error: {e}")
        return heuristic_ambiguous


def _score_users(users: List[Dict], context: Dict, priority_info: Dict) -> List[Dict]:
    """
    Score teams based on skill match with ticket context only.
    Returns sorted list (highest score first).
    """
    title = (context.get("title") or "").lower()
    body = (context.get("body") or "").lower()
    tags = [t.lower() for t in (context.get("tags") or [])]
    product_area = (context.get("product_area") or "").lower()
    
    combined_text = f"{title} {body} {product_area} {' '.join(tags)}"
    
    for team in users:
        skill_score = 0.0
        team_skills = [s.lower() for s in team.get("skills", [])]
        
        # Skill matching - count how many team skills match the ticket context
        for skill in team_skills:
            if skill in combined_text:
                skill_score += 10.0
        
        # Score is based purely on skill match
        team["score"] = skill_score
    
    # Sort by score descending
    users.sort(key=lambda u: u["score"], reverse=True)
    return users


async def _gemini_assignee(context: Dict, priority_info: Dict, scored_users: List[Dict]) -> Dict:
    """Use Gemini to select final team from scored candidates based on context only."""
    
    # Build team roster summary
    team_summary = []
    for i, team in enumerate(scored_users[:5]):  # Top 5 candidates
        team_summary.append(
            f"{i+1}. {team['name']} (ID: {team['user_id']}) - "
            f"Skills: {', '.join(team.get('skills', [])[:5])}... - "
            f"Match Score: {team['score']:.1f}"
        )
    
    prompt = f"""You are assigning a support ticket to the best available team based on context and skills.

Ticket Title: {context.get('title', '')}
Ticket Body: {context.get('body', '')}
Priority: {priority_info.get('priority', 'P3')}
Product Area: {context.get('product_area', '')}
Tags: {', '.join(context.get('tags', []))}

Available Teams (sorted by skill match score):
{chr(10).join(team_summary)}

Select the BEST team considering:
1. Team skills relevance to ticket content and context
2. How well the team's expertise matches the ticket requirements
3. Priority urgency (higher priority may need more specialized teams)

DO NOT consider workload - only match based on skills and context.

Respond in JSON format:
{{
    "assignee_user_id": "<team_id from list>"
}}

Only return assignee_user_id - no rationale needed."""
    
    try:
        response = await llm.ainvoke(prompt)
        result_text = response.content.strip()
        
        # Clean JSON from markdown
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(result_text)
        
        # Validate team_id exists in scored_users
        valid_ids = [u["user_id"] for u in scored_users]
        if result.get("assignee_user_id") not in valid_ids:
            result["assignee_user_id"] = scored_users[0]["user_id"]
        
        # Remove rationale if present
        result.pop("rationale", None)
        
        return result
        
    except Exception as e:
        print(f"Gemini assignee error: {e}")
        best_team = scored_users[0]
        return {
            "assignee_user_id": best_team["user_id"]
        }
