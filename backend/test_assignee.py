"""
Test AssigneeAgent directly.
"""
import asyncio
from database import connect_to_mongo
from triage.state import TriageState
from triage.agents.assignee_agent import assignee_agent


async def test_assignee():
    """Test assignee agent."""
    await connect_to_mongo()
    
    test_state = {
        "ticket": {"_id": "test", "title": "Test"},
        "context": {
            "title": "Payment failed on checkout",
            "body": "Customer unable to complete payment with Stripe",
            "tags": ["payment", "urgent", "stripe"],
            "product_area": "billing",
            "comments": [],
            "attachments": []
        },
        "priority": {
            "priority": "P0",
            "confidence": 0.9,
            "rationale": "Payment failure"
        },
        "assignee": None,
        "reply": None,
        "error": None
    }
    
    print("🧪 Testing AssigneeAgent...")
    result = await assignee_agent(test_state)
    
    print(f"\n📊 Result:")
    print(f"   Assignee: {result.get('assignee')}")
    print(f"   Error: {result.get('error')}")


if __name__ == "__main__":
    asyncio.run(test_assignee())
