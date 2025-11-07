"""
PriorityAgent - Determines ticket priority using Gemini AI.
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
        model="gemini-2.5-flash",
        api_key=GEMINI_API_KEY,
        temperature=0.2
    )


async def priority_agent(state: TriageState) -> TriageState:
    """
    Determine ticket priority using Gemini AI.
    
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
        
        # Use Gemini for priority assignment if available
        if llm and not USE_MOCK:
            priority_result = await _gemini_priority(context)
        else:
            # Fallback to P3 if LLM is not available
            priority_result = {
                "priority": "P3",
                "confidence": 0.5
            }
        
        state["priority"] = priority_result
        return state
        
    except Exception as e:
        state["error"] = f"PriorityAgent error: {str(e)}"
        return state


async def _gemini_priority(context: Dict) -> Dict:
    """Use Gemini to determine ticket priority with comprehensive analysis framework."""
    prompt = f"""You are an expert ticket triage analyst. Your task is to analyze the ticket below and assign the most appropriate priority level.

TICKET INFORMATION:
Title: {context.get('title', '')}
Description: {context.get('body', '')}
Tags: {', '.join(context.get('tags', [])) if context.get('tags') else 'None'}

ANALYSIS FRAMEWORK:
Evaluate the ticket using these criteria in order:

1. SYSTEM IMPACT:
   - Is the entire system/service down? (P0)
   - Is a critical system component failing? (P0-P1)
   - Is a major feature completely broken? (P1)
   - Is a minor feature affected? (P2-P3)

2. USER IMPACT:
   - How many users are affected?
   - All users (P0-P1)
   - Large portion of users (P1)
   - Some users (P2)
   - Individual user (P3)

3. BUSINESS IMPACT:
   - Revenue loss or payment processing down? (P0)
   - Revenue-generating feature broken? (P1)
   - Customer-facing critical feature broken? (P1)
   - Non-revenue impacting issue? (P2-P3)

4. SECURITY & DATA:
   - Security breach or data breach? (P0)
   - Data loss or corruption? (P0)
   - Security vulnerability? (P0-P1)
   - Privacy concern? (P1-P2)

5. URGENCY & WORKAROUNDS:
   - No workaround available? (P0-P1)
   - Workaround exists but inconvenient? (P2)
   - Workaround is acceptable? (P2-P3)
   - Not urgent, can wait? (P3)

6. FUNCTIONALITY STATUS:
   - Completely non-functional? (P0-P1)
   - Partially functional with major issues? (P1-P2)
   - Functional but degraded? (P2)
   - Fully functional, enhancement request? (P3)

PRIORITY LEVEL DEFINITIONS:

P0 - CRITICAL (Immediate response, < 1 hour):
REQUIRES ALL OF:
- System-wide outage OR complete service unavailability
- OR security breach/data breach
- OR data loss/corruption
- OR payment processing completely down
- Affects ALL or MAJORITY of users
- No workaround available
- Immediate business/revenue impact

EXAMPLES:
✓ "Production database crashed - entire application is down, no users can access"
✓ "Security breach detected - user passwords may be compromised"
✓ "Payment gateway is completely down - zero transactions possible"
✓ "Data loss - customer order history has been deleted"
✗ "API is slow" (not P0 - system still works)
✗ "Some users reporting issues" (not P0 - not system-wide)

P1 - HIGH (Urgent, < 4 hours):
REQUIRES MOST OF:
- Major feature completely broken
- OR critical customer-facing functionality down
- OR significant revenue impact
- Affects LARGE PORTION of users (30%+)
- OR affects critical business process
- Limited or no workaround
- High business impact

EXAMPLES:
✓ "User authentication API returning 500 errors - 50% of users cannot login"
✓ "Checkout process completely broken - customers cannot complete purchases"
✓ "Mobile app crashes on launch for all iOS users"
✓ "Critical bug preventing order processing for premium customers"
✗ "Minor bug in profile page" (not P1 - not critical)
✗ "Feature request for new button" (not P1 - enhancement)

P2 - MEDIUM (Standard, < 24 hours):
REQUIRES:
- Moderate functionality issue
- OR feature partially working
- OR non-critical bug
- Affects SOME users or specific use cases
- Workaround available
- Moderate business impact
- OR billing/account questions

EXAMPLES:
✓ "User profile page - some fields not displaying correctly, but data is accessible"
✓ "Billing question - customer wants clarification on invoice charges"
✓ "Feature partially working - has workaround but needs fixing"
✓ "UI styling issue - button looks wrong but still clickable"
✓ "Performance degradation - slower response times but still functional"
✗ "Complete feature broken" (not P2 - should be P1)
✗ "Feature request" (not P2 - should be P3)

P3 - LOW (Normal queue, < 72 hours):
REQUIRES:
- Minor bug or cosmetic issue
- OR feature request/enhancement
- OR general question
- OR documentation issue
- Affects FEW or INDIVIDUAL users
- OR no functional impact
- Low or no business impact
- Can wait for normal processing

EXAMPLES:
✓ "Feature request - add dark mode to the application"
✓ "General question about account settings"
✓ "Minor typo in help documentation"
✓ "Enhancement request - improve search functionality"
✓ "Cosmetic issue - spacing looks off on one page"
✓ "Suggestion for UI improvement"
✗ "Major feature broken" (not P3 - should be P1)
✗ "System down" (not P3 - should be P0)

DECISION PROCESS:
1. Start with P0 criteria - does it meet ALL P0 requirements? If yes → P0
2. If not P0, check P1 criteria - does it meet MOST P1 requirements? If yes → P1
3. If not P1, check P2 criteria - does it meet P2 requirements? If yes → P2
4. Otherwise → P3

CONFIDENCE SCORING:
- 0.9-1.0: Very clear match to priority level criteria
- 0.7-0.89: Good match, some ambiguity
- 0.5-0.69: Moderate match, could be borderline with adjacent level
- < 0.5: Unclear, use lower priority

Now analyze the ticket above and assign the priority level.

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
        
        # Validate priority
        if result.get("priority") not in ["P0", "P1", "P2", "P3"]:
            result["priority"] = "P3"
        
        result["confidence"] = float(result.get("confidence", 0.8))
        
        # Remove rationale if present
        result.pop("rationale", None)
        
        return result
        
    except Exception as e:
        print(f"Gemini priority error: {e}")
        return {
            "priority": "P3",
            "confidence": 0.5
        }
