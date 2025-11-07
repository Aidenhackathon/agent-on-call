"""
Test script to debug triage workflow.
"""
import asyncio
from bson import ObjectId
from database import connect_to_mongo, get_tickets_collection
from triage import create_triage_graph


async def test_triage(ticket_id: str):
    """Test the triage workflow."""
    await connect_to_mongo()
    
    collection = get_tickets_collection()
    ticket = await collection.find_one({"_id": ObjectId(ticket_id)})
    
    if not ticket:
        print(f"❌ Ticket {ticket_id} not found")
        return
    
    print(f"✅ Found ticket: {ticket.get('title')}")
    print(f"   Description: {ticket.get('description', 'N/A')}")
    print(f"   Category: {ticket.get('category', 'N/A')}")
    
    try:
        print("\n🤖 Creating LangGraph workflow...")
        graph = create_triage_graph()
        
        print("🚀 Running multi-agent triage...")
        initial_state = {
            "ticket": ticket,
            "context": None,
            "priority": None,
            "assignee": None,
            "reply": None,
            "error": None
        }
        
        final_state = await graph.ainvoke(initial_state)
        
        print("\n📊 RESULTS:")
        print(f"   Error: {final_state.get('error')}")
        print(f"   Context Keys: {list(final_state.get('context', {}).keys()) if final_state.get('context') else 'None'}")
        print(f"   Priority: {final_state.get('priority')}")
        print(f"   Assignee: {final_state.get('assignee')}")
        print(f"   Reply Length: {len(final_state.get('reply', '')) if final_state.get('reply') else 0}")
        print(f"\n   Full State Keys: {list(final_state.keys())}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import sys
    ticket_id = sys.argv[1] if len(sys.argv) > 1 else "690d94b072b8929e5cfbac1c"
    asyncio.run(test_triage(ticket_id))
