"""
RationaleAgent - Generates rationale for priority and assignee decisions.
"""
import os
import json
from typing import Dict
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


async def rationale_agent(state: TriageState) -> TriageState:
    """
    Generate rationale for priority and assignee decisions based on context.
    
    Input: Context, Priority info, Assignee info
    Returns:
        {
            "priority_rationale": str,
            "assignee_rationale": str
        }
    """
    try:
        context = state.get("context", {})
        priority_info = state.get("priority", {})
        assignee_info = state.get("assignee", {})
        
        if not context or not isinstance(context, dict) or not context.get("title"):
            state["error"] = "No context available for RationaleAgent"
            return state
        
        if not priority_info or not isinstance(priority_info, dict) or not priority_info.get("priority"):
            state["error"] = "No priority information available for RationaleAgent"
            return state
        
        if not assignee_info or not isinstance(assignee_info, dict):
            state["error"] = "No assignee information available for RationaleAgent"
            return state
        
        # Get team name for rationale
        assignee_user_id = assignee_info.get("assignee_user_id", "unassigned")
        team_name = assignee_user_id
        
        if assignee_user_id and assignee_user_id != "unassigned":
            users_collection = get_users_collection()
            team = await users_collection.find_one({"_id": assignee_user_id})
            if team:
                team_name = team.get("name", assignee_user_id)
                team_skills = team.get("skills", [])
            else:
                team_skills = []
        else:
            team_skills = []
        
        # Generate rationale using Gemini if available
        if llm and not USE_MOCK:
            rationale_result = await _gemini_rationale(
                context, priority_info, assignee_info, team_name, team_skills
            )
        else:
            # Fallback rationale generation
            rationale_result = _mock_rationale(
                context, priority_info, assignee_info, team_name, team_skills
            )
        
        state["rationale"] = rationale_result
        return state
        
    except Exception as e:
        print(f"⚠️  RationaleAgent Exception: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        state["error"] = f"RationaleAgent error: {str(e)}"
        # Provide fallback rationale
        state["rationale"] = {
            "priority_rationale": f"Priority {priority_info.get('priority', 'P3')} assigned based on ticket analysis.",
            "assignee_rationale": f"Assigned to {assignee_info.get('assignee_user_id', 'unassigned')} based on skill match."
        }
        return state


async def _gemini_rationale(
    context: Dict,
    priority_info: Dict,
    assignee_info: Dict,
    team_name: str,
    team_skills: list
) -> Dict:
    """Use Gemini to generate comprehensive rationale for priority and assignee."""
    
    priority = priority_info.get("priority", "P3")
    confidence = priority_info.get("confidence", 0.0)
    assignee_user_id = assignee_info.get("assignee_user_id", "unassigned")
    
    prompt = f"""You are a helpdesk triage expert. Generate clear, professional rationale for ticket triage decisions.

Ticket Information:
- Title: {context.get('title', '')}
- Description: {context.get('body', '')}
- Tags: {', '.join(context.get('tags', []))}
- Product Area: {context.get('product_area', '')}

Triage Decisions:
- Priority: {priority} (Confidence: {confidence:.2f})
- Assigned Team: {team_name}
- Team Skills: {', '.join(team_skills[:10])}

Generate TWO separate rationales:

1. Priority Rationale: Explain why this priority level ({priority}) was assigned. Consider:
   - The severity and impact of the issue
   - Urgency requirements
   - Customer impact
   - System criticality

2. Assignee Rationale: Explain why {team_name} was assigned this ticket. Consider:
   - How team skills match the ticket requirements
   - Relevance of team expertise to the issue
   - Why this team is best suited to handle it

Guidelines:
- Each rationale should be 50-80 words
- Be specific and reference ticket details
- Professional and clear language
- Focus on reasoning and justification

Respond in JSON format:
{{
    "priority_rationale": "<explanation for priority assignment>",
    "assignee_rationale": "<explanation for team assignment>"
}}"""
    
    try:
        response = await llm.ainvoke(prompt)
        result_text = response.content.strip()
        
        # Clean JSON from markdown
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(result_text)
        
        # Validate required fields
        if "priority_rationale" not in result:
            result["priority_rationale"] = f"Priority {priority} assigned based on ticket analysis."
        
        if "assignee_rationale" not in result:
            result["assignee_rationale"] = f"Assigned to {team_name} based on skill match."
        
        return result
        
    except Exception as e:
        print(f"Gemini rationale error: {e}")
        return _mock_rationale(context, priority_info, assignee_info, team_name, team_skills)


def _mock_rationale(
    context: Dict,
    priority_info: Dict,
    assignee_info: Dict,
    team_name: str,
    team_skills: list
) -> Dict:
    """Generate mock rationale based on ticket content and decisions."""
    
    priority = priority_info.get("priority", "P3")
    assignee_user_id = assignee_info.get("assignee_user_id", "unassigned")
    
    title_lower = context.get("title", "").lower()
    body_lower = context.get("body", "").lower()
    combined = f"{title_lower} {body_lower}"
    
    # Generate priority rationale
    if priority == "P0":
        priority_rationale = "Critical priority assigned due to system outage, security breach, or data loss. Immediate attention required to minimize customer impact and prevent escalation."
    elif priority == "P1":
        priority_rationale = "High priority assigned due to major functionality issues affecting users. Significant impact on user experience or revenue requires urgent resolution."
    elif priority == "P2":
        priority_rationale = "Medium priority assigned for issues with available workarounds or moderate impact. Standard review process applies with expected resolution within normal timeframe."
    else:
        priority_rationale = "Low priority assigned for minor issues, feature requests, or general inquiries. Normal queue processing with standard response timeframe."
    
    # Generate assignee rationale
    if assignee_user_id == "unassigned":
        assignee_rationale = "Unable to assign to a specific team. Manual assignment may be required."
    else:
        # Find matching skills in ticket
        matching_skills = [skill for skill in team_skills if skill.lower() in combined]
        if matching_skills:
            assignee_rationale = f"Assigned to {team_name} because the ticket requires expertise in {', '.join(matching_skills[:3])}. This team has the necessary skills to effectively resolve this issue."
        else:
            assignee_rationale = f"Assigned to {team_name} based on general team capabilities and ticket characteristics. The team's expertise aligns with the ticket requirements."
    
    return {
        "priority_rationale": priority_rationale,
        "assignee_rationale": assignee_rationale
    }

