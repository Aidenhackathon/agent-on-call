# LangGraph Multi-Agent Triage System

## Architecture Overview

This system uses **LangGraph** to orchestrate a multi-agent workflow for intelligent ticket triage.

### Agents

1. **ContextAgent** - Fetches ticket, comments, and attachments from MongoDB
2. **PriorityAgent** - Determines priority using heuristics + Gemini AI validation
3. **AssigneeAgent** - Assigns ticket to best user based on skills, workload, and Gemini selection
4. **ReplyAgent** - Generates customer reply draft (≤120 words) using Gemini
5. **PersistNode** - Writes triage results to MongoDB

### Workflow

```
START → ContextAgent → PriorityAgent → AssigneeAgent → ReplyAgent → PersistNode → END
```

## MongoDB Collections

### tickets
```json
{
  "_id": ObjectId,
  "title": str,
  "description": str,  // legacy field (maps to body in context)
  "body": str,         // new field
  "status": "open|triaged|pending|waiting|closed",
  "priority": "P0|P1|P2|P3|null",
  "assignee": str,     // legacy field
  "assignee_user_id": str|null,  // new field
  "product_area": str,
  "tags": [str],
  "created_at": datetime,
  "updated_at": datetime
}
```

### triage_results
```json
{
  "_id": ObjectId,
  "ticket_id": str,
  "priority": str,
  "priority_confidence": float,
  "priority_rationale": str,
  "assignee_user_id": str,
  "assignee_rationale": str,
  "reply_draft": str,
  "created_at": datetime
}
```

### users
```json
{
  "_id": str,
  "name": str,
  "skills": [str],
  "workload": int,
  "active": bool
}
```

### activity_logs
```json
{
  "_id": ObjectId,
  "ticket_id": str,
  "event_type": "triage_run|triage_failed|reply_saved",
  "payload": dict,
  "timestamp": datetime
}
```

### comments
```json
{
  "_id": ObjectId,
  "ticket_id": str,
  "text": str,
  "created_at": datetime
}
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

New dependencies added:
- `langgraph==0.2.28`
- `langchain-core==0.3.6`
- `langchain-google-genai==2.0.0`

### 2. Seed Users Collection

Before running triage, populate the `users` collection:

```bash
cd backend
python seed_users.py
```

This creates 6 sample users with different skills:
- Alice (DevOps)
- Bob (Backend)
- Carol (Frontend)
- David (Finance)
- Emma (Product)
- Frank (Support)

### 3. Start Services

```bash
docker-compose up --build
```

## API Usage

### Create Ticket (with new fields)

```bash
POST /tickets
{
  "title": "Payment failed on checkout",
  "description": "Customer unable to complete payment",
  "category": "billing",
  "product_area": "payments",
  "tags": ["payment", "urgent", "stripe"]
}
```

### Trigger Multi-Agent Triage

```bash
POST /tickets/{ticket_id}/triage
```

**Response:**
```json
{
  "priority": "P0",
  "confidence": 0.92,
  "assignee": "david_finance",
  "rationale": "Payment failure requires immediate attention | Assigned to David Kim based on billing expertise",
  "reply_draft": "Hello,\n\nThank you for reporting this payment issue..."
}
```

## How It Works

### 1. ContextAgent
- Fetches ticket from MongoDB
- Loads related comments (up to 10)
- Loads attachments (up to 5)
- Builds compact context JSON

### 2. PriorityAgent
- **Heuristics First**: Checks for keywords like "payment failed", "site down", etc.
- **Gemini Validation**: Uses Gemini to confirm or adjust heuristic priority
- **Output**: Priority (P0-P3), confidence score, rationale

### 3. AssigneeAgent
- **Fetch Users**: Loads active users from MongoDB
- **Skill Scoring**: Matches user skills against ticket content
- **Workload Penalty**: Considers current workload
- **Gemini Selection**: Final assignee chosen by Gemini from top 5 candidates
- **Output**: User ID, rationale

### 4. ReplyAgent
- **Gemini Generation**: Creates professional customer reply
- **Word Limit**: Strictly enforced ≤120 words
- **Priority-Aware**: Reply tone/urgency matches priority
- **Output**: Reply text

### 5. PersistNode
- Updates `tickets` collection (priority, assignee_user_id, status)
- Inserts `triage_results` document
- Inserts `activity_logs` entry
- Increments assignee workload

## Configuration

### Environment Variables

```bash
GEMINI_API_KEY=your_key_here
USE_MOCK_AI=false
MONGODB_URL=mongodb://mongodb:27017
```

### Priority Heuristics

Edit `triage/agents/priority_agent.py`:

```python
# P0 keywords
"payment failed", "site down", "outage", "security breach"

# P1 keywords
"api error", "broken", "not working", "urgent"

# P2 keywords
"minor bug", "issue", "billing question"

# Default: P3
```

### Skill Matching

Edit `triage/agents/assignee_agent.py`:

```python
# Skill match score
if skill in combined_text:
    skill_score += 10.0

# Workload penalty
workload_penalty = workload * 2.0
```

## Testing

### Unit Tests

```bash
pytest backend/tests/
```

### Manual Testing

1. Create ticket with tags and product_area
2. Trigger triage
3. Check MongoDB collections:
   - `tickets` - updated with priority and assignee_user_id
   - `triage_results` - new document inserted
   - `activity_logs` - triage_run event logged
   - `users` - assignee workload incremented

## Troubleshooting

### Error: "No active users available"
- Run `python seed_users.py` to populate users collection

### Error: "ContextAgent error"
- Check MongoDB connection
- Verify ticket exists with valid _id

### Error: "Gemini API error"
- Verify GEMINI_API_KEY is set
- Check API quota/limits
- System falls back to heuristics on Gemini errors

## State Flow

```python
{
  "ticket": {...},           # Input from MongoDB
  "context": {...},          # ContextAgent output
  "priority": {...},         # PriorityAgent output
  "assignee": {...},         # AssigneeAgent output
  "reply": "...",            # ReplyAgent output
  "error": None              # Error tracking
}
```

## File Structure

```
backend/
├── triage/
│   ├── __init__.py
│   ├── state.py                    # TriageState definition
│   ├── graph.py                    # LangGraph workflow
│   └── agents/
│       ├── __init__.py
│       ├── context_agent.py
│       ├── priority_agent.py
│       ├── assignee_agent.py
│       ├── reply_agent.py
│       └── persist_node.py
├── routes/
│   └── tickets.py                   # Updated triage endpoint
├── database.py                      # New collection accessors
├── seed_users.py                    # User seeding script
└── requirements.txt                 # Updated dependencies
```

## Next Steps

1. Add more sophisticated skill matching algorithms
2. Implement machine learning for priority prediction
3. Add user preference/availability tracking
4. Create agent performance metrics dashboard
5. Implement A/B testing for different triage strategies
