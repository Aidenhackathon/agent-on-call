# LangGraph Multi-Agent Triage Flow

## Overview

The Agent-on-Call system uses a **LangGraph-based multi-agent workflow** to automatically triage support tickets. The workflow consists of 6 sequential nodes (5 agents + 1 persistence node) that analyze tickets and determine priority, assignment, generate rationale explanations, and create customer replies.

## Architecture

The workflow is built using **LangGraph** (0.2.28) and orchestrates multiple specialized agents that work together to automatically triage tickets. Each agent has a specific responsibility and the workflow ensures data flows seamlessly between agents.

## Flow Diagram

```
┌─────────────────┐
│  Ticket Created │
│   (MongoDB)     │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│  1. ContextDetailer │ ◄─── Fetches ticket, comments, attachments
│  (fetch_context)    │      Builds compact context for downstream agents
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  2. PriorityAgent   │ ◄─── Heuristics + Gemini AI
│(determine_priority) │      Determines: P0, P1, P2, or P3
│                     │      Returns: priority, confidence
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  3. AssigneeAgent   │ ◄─── Skill matching + Gemini AI
│   (assign_user)     │      Scores teams based on context
│                     │      Selects best match from top 5
│                     │      Returns: assignee_user_id
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  4. RationaleAgent  │ ◄─── Gemini AI
│ (generate_rationale)│      Generates rationale for priority and assignee
│                     │      Returns: priority_rationale, assignee_rationale
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   5. ReplyAgent     │ ◄─── Gemini AI
│  (generate_reply)   │      Generates customer reply draft (≤120 words)
│                     │      Returns: reply text
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   6. PersistNode    │ ◄─── MongoDB Updates
│   (save_results)    │      Updates ticket, creates triage_results
│                     │      Logs activity to activity_logs
└──────────┬──────────┘
           │
           ▼
        ┌─────┐
        │ END │
        └─────┘
```

## State Schema

The workflow uses a `TriageState` TypedDict that is passed between agents:

```python
class TriageState(TypedDict, total=False):
    ticket: Optional[dict]      # Original ticket from MongoDB
    context: Optional[dict]     # Compact context from ContextDetailer
    priority: Optional[dict]    # Priority info from PriorityAgent
    assignee: Optional[dict]    # Assignee info from AssigneeAgent
    rationale: Optional[dict]   # Rationale from RationaleAgent
    reply: Optional[str]        # Reply draft from ReplyAgent
    error: Optional[str]        # Error message if any step fails
```

## Detailed Agent Descriptions

### 1. ContextDetailer (`fetch_context`)

**Location**: `backend/triage/agents/context_detailer.py`

**Purpose**: Gathers all relevant ticket information into a compact context object for downstream agents.

**Input State**:
```python
{
    "ticket": {
        "_id": ObjectId("..."),
        "title": str,
        "description": str,
        "tags": List[str],
        "category": str,
        ...
    },
    "context": None,
    ...
}
```

**Process**:
1. Validates ticket exists and has `_id`
2. Fetches related comments from `comments` collection (last 10, sorted by `created_at`)
3. Fetches related attachments from `attachments` collection (last 5)
4. Builds compact context dictionary:
   - Extracts title, description (or body), tags, product_area (or category)
   - Includes comments and attachments metadata
5. Handles both legacy (`description`) and new (`body`) field names

**Output State**:
```python
{
    "context": {
        "title": str,
        "body": str,  # Description text
        "tags": List[str],
        "product_area": str,
        "comments": [
            {
                "text": str,
                "created_at": str  # ISO format
            }
        ],
        "attachments": [
            {
                "filename": str,
                "size": int
            }
        ]
    },
    ...
}
```

**Error Handling**:
- Sets `state["error"] = "No ticket provided to ContextDetailer"` if ticket is missing or invalid
- Catches exceptions and sets error message in state

**Database Operations**:
- Reads from `tickets` collection
- Reads from `comments` collection
- Reads from `attachments` collection

---

### 2. PriorityAgent (`determine_priority`)

**Location**: `backend/triage/agents/priority_agent.py`

**Purpose**: Determines ticket priority (P0-P3) using Gemini AI with comprehensive analysis framework.

**Input State**:
```python
{
    "context": {
        "title": str,
        "body": str,
        "tags": List[str],
        ...
    },
    "priority": None,
    ...
}
```

**Process**:
1. Validates context exists
2. **Gemini AI Analysis** (if `GEMINI_API_KEY` available and `USE_MOCK_AI=false`):
   - Sends comprehensive prompt with ticket information
   - Uses analysis framework covering:
     - **System Impact**: Entire system down? Critical component failing?
     - **User Impact**: How many users affected?
     - **Business Impact**: Revenue loss? Payment processing down?
     - **Security & Data**: Security breach? Data loss?
     - **Urgency & Workarounds**: Workaround available?
   - Gemini returns priority (P0/P1/P2/P3) and confidence score (0.0-1.0)
3. **Fallback** (if Gemini unavailable):
   - Returns default P3 with confidence 0.5

**Output State**:
```python
{
    "priority": {
        "priority": "P0|P1|P2|P3",
        "confidence": float  # 0.0 to 1.0
    },
    ...
}
```

**Priority Levels**:
- **P0**: Critical system outage, security breach, data loss, payment failures
  - Response time: Immediate
  - Updates: Every 30 minutes
- **P1**: Major functionality broken, significant user impact, API errors
  - Response time: 2-4 hours
  - Updates: Every 2-4 hours
- **P2**: Moderate issues, workarounds available, billing questions
  - Response time: 24-48 hours
  - Updates: Standard review
- **P3**: Minor issues, feature requests, general questions
  - Response time: 2-3 business days
  - Updates: Normal queue

**Model Configuration**:
- **Model**: `gemini-2.5-flash`
- **Temperature**: 0.2 (low for consistent results)
- **API**: LangChain Google Generative AI

**Error Handling**:
- Sets `state["error"]` if context is missing
- Falls back to P3 if Gemini fails
- Catches exceptions and provides fallback priority

---

### 3. AssigneeAgent (`assign_user`)

**Location**: `backend/triage/agents/assignee_agent.py`

**Purpose**: Assigns ticket to the best available team based on skill matching with ticket content.

**Input State**:
```python
{
    "context": {
        "title": str,
        "body": str,
        "tags": List[str],
        "product_area": str,
        ...
    },
    "priority": {
        "priority": str,
        "confidence": float
    },
    "assignee": None,
    ...
}
```

**Process**:
1. Validates context exists
2. **Ambiguity Check**:
   - Checks if title/description is too vague (less than 10 characters total)
   - If ambiguous, routes to `customer_support` team
3. **Fetch Teams**: Retrieves all teams from MongoDB `users` collection
4. **Score Teams** (skill matching only, no workload consideration):
   - For each team, calculates skill score:
     - Matches team skills against ticket content (title, body, tags, product_area)
     - Each matching skill: +10 points
     - Case-insensitive matching
   - Final score based purely on skill relevance
5. **Sort Teams**: Orders teams by score (highest first)
6. **Gemini Selection** (if API key available):
   - Sends top 5 candidates to Gemini with context
   - Gemini selects best team considering:
     - Skill match relevance
     - Context understanding
     - Priority level implications
   - Validates selected team ID exists
7. **Fallback**: Picks top-scored team if Gemini fails

**Output State**:
```python
{
    "assignee": {
        "assignee_user_id": str  # Team ID (e.g., "backend_team", "devops_team")
    },
    ...
}
```

**Example Scoring**:
```
Ticket: "API endpoint returning 500 error"
Teams:
  - Backend Team (skills: ["python", "fastapi", "mongodb", "api"])
    Matches: "api" → Score: 10
  - DevOps Team (skills: ["kubernetes", "docker", "infrastructure"])
    Matches: none → Score: 0
  - Frontend Team (skills: ["react", "javascript", "ui"])
    Matches: none → Score: 0

Result: Backend Team selected (highest score)
```

**Available Teams** (from `seed_users.py`):
- `devops_team` - Infrastructure, deployment, system outages
- `backend_team` - API issues, server errors, database problems
- `frontend_team` - UI bugs, display issues
- `finance_team` - Billing, payments, invoicing
- `product_team` - Feature requests, product questions
- `customer_support` - General inquiries, account issues

**Model Configuration**:
- **Model**: `gemini-2.5-flash`
- **Temperature**: 0.2
- **Selection**: From top 5 candidates

**Error Handling**:
- Routes to `customer_support` if ticket is ambiguous
- Routes to `unassigned` if no teams exist in database
- Falls back to top-scored team if Gemini fails
- Catches exceptions and assigns to `unassigned`

---

### 4. RationaleAgent (`generate_rationale`)

**Location**: `backend/triage/agents/rationale_agent.py`

**Purpose**: Generates clear, professional rationale explanations for priority and assignee decisions.

**Input State**:
```python
{
    "context": {
        "title": str,
        "body": str,
        ...
    },
    "priority": {
        "priority": str,
        "confidence": float
    },
    "assignee": {
        "assignee_user_id": str
    },
    "rationale": None,
    ...
}
```

**Process**:
1. **Validates Inputs**:
   - Ensures context, priority, and assignee information are available
   - Validates each is a proper dictionary with required fields
2. **Fetches Team Info**: Retrieves team name and skills from MongoDB for rationale generation
3. **Gemini Generation** (if API key available):
   - Sends ticket context, priority decision, and assignee information to Gemini
   - Prompts for two separate rationales:
     - **Priority Rationale**: Explains why the priority level was assigned (50-80 words)
       - References specific ticket details
       - Explains impact and urgency
     - **Assignee Rationale**: Explains why the team was assigned (50-80 words)
       - References team skills and expertise
       - Explains how skills match ticket requirements
   - Each rationale should be specific, professional, and reference ticket details
4. **Fallback**: Uses template-based rationale generation if Gemini fails

**Output State**:
```python
{
    "rationale": {
        "priority_rationale": str,   # Explanation for priority assignment
        "assignee_rationale": str    # Explanation for team assignment
    },
    ...
}
```

**Example Output**:
```python
{
    "priority_rationale": "Critical priority assigned due to system outage affecting customer access. Immediate attention required to minimize customer impact and prevent escalation.",
    "assignee_rationale": "Assigned to DevOps Team because the ticket requires expertise in kubernetes, docker, infrastructure. This team has the necessary skills to effectively resolve this issue."
}
```

**Model Configuration**:
- **Model**: `gemini-2.5-flash`
- **Temperature**: 0.2
- **Output**: Two separate rationale strings (50-80 words each)

**Error Handling**:
- Validates all required inputs exist
- Provides fallback template rationale if Gemini fails
- Catches exceptions and provides basic rationale

---

### 5. ReplyAgent (`generate_reply`)

**Location**: `backend/triage/agents/reply_agent.py`

**Purpose**: Generates a professional customer reply draft with strict 120-word limit.

**Input State**:
```python
{
    "context": {
        "title": str,
        "body": str,
        ...
    },
    "priority": {
        "priority": str,
        "confidence": float
    },
    "assignee": {
        "assignee_user_id": str
    },
    "reply": None,
    ...
}
```

**Process**:
1. Validates context exists
2. **Gemini Generation** (if API key available):
   - Sends ticket title, body, and priority to Gemini
   - Prompts for professional, empathetic reply
   - **Strict requirement**: ≤120 words (enforced after generation)
   - Sets expectations based on priority:
     - **P0**: Immediate escalation, updates every 30 min
     - **P1**: High priority, update in 2-4 hours
     - **P2**: Standard review, response in 24-48 hours
     - **P3**: Normal queue, response in 2-3 business days
3. **Word Limit Enforcement**: Truncates to 120 words if exceeded
4. **Fallback**: Uses template-based mock reply if Gemini fails

**Output State**:
```python
{
    "reply": str,  # Customer reply draft text (≤120 words)
    ...
}
```

**Example Reply (P0)**:
```
Hello,

Thank you for reporting this critical issue. We understand the urgency and have immediately escalated this to our DevOps team. They are actively investigating and will provide updates every 30 minutes until resolved.

We sincerely apologize for the inconvenience and appreciate your patience.

Best regards,
Support Team
```

**Example Reply (P1)**:
```
Hello,

Thank you for reporting this issue. We've flagged this as high priority and our backend team is investigating now. We'll provide an update within 2-4 hours.

We appreciate your patience as we work to resolve this.

Best regards,
Support Team
```

**Model Configuration**:
- **Model**: `gemini-2.5-flash`
- **Temperature**: 0.2
- **Word Limit**: Strictly enforced at 120 words

**Error Handling**:
- Sets error if context is missing
- Falls back to template reply if Gemini fails
- Ensures reply never exceeds 120 words

---

### 6. PersistNode (`save_results`)

**Location**: `backend/triage/agents/persist_node.py`

**Purpose**: Persists all triage results to MongoDB collections.

**Input State**:
```python
{
    "ticket": {
        "_id": ObjectId("..."),
        ...
    },
    "priority": {
        "priority": str,
        "confidence": float
    },
    "assignee": {
        "assignee_user_id": str
    },
    "rationale": {
        "priority_rationale": str,
        "assignee_rationale": str
    },
    "reply": str,
    ...
}
```

**Process**:
1. **Validates Ticket**: Ensures ticket exists with `_id`
2. **Fetches Team Name**: Retrieves team name from `users` collection for display
3. **Combines Rationales**: Merges `priority_rationale` and `assignee_rationale` with ` | ` separator
4. **Update Ticket Document**:
   - Sets `priority` (P0/P1/P2/P3)
   - Sets `assignee_user_id` (team ID)
   - Sets `assignee` (team name for display - legacy field)
   - Sets `status` = "triaged"
   - Sets `ai_rationale` (combined rationales)
   - Sets `ai_reply_draft` (reply text)
   - Sets `ai_confidence` (priority confidence)
   - Updates `updated_at` timestamp
5. **Insert Triage Result**:
   - Creates document in `triage_results` collection
   - Stores: ticket_id, priority, priority_confidence, priority_rationale, assignee_user_id, assignee_rationale, reply_draft, created_at
6. **Log Activity**:
   - Inserts into `activity_logs` collection
   - Event type: `triage_run`
   - Payload: priority, assignee, confidence
   - Timestamp: current IST time

**Output State**:
```python
{
    "error": None,  # Cleared on success
    ...
}
```

**Database Operations**:
- **Updates**: `tickets` collection (ticket document)
- **Inserts**: `triage_results` collection (historical record)
- **Inserts**: `activity_logs` collection (audit trail)
- **Reads**: `users` collection (team name lookup)

**Error Handling**:
- Sets `state["error"]` if ticket is missing
- Logs failure to `activity_logs` collection if any step fails
- Catches exceptions and logs error details

---

## Execution Flow

### Entry Point

The workflow is triggered via the API endpoint:

```http
POST /tickets/{ticket_id}/triage
```

### Workflow Execution Code

```python
# 1. Create graph (from routes/tickets.py)
from triage import create_triage_graph
graph = create_triage_graph()

# 2. Get ticket from MongoDB
collection = get_tickets_collection()
ticket = await collection.find_one({"_id": ObjectId(ticket_id)})

# 3. Initialize state
initial_state = {
    "ticket": ticket,
    "context": None,
    "priority": None,
    "assignee": None,
    "rationale": None,
    "reply": None,
    "error": None
}

# 4. Execute workflow (async)
final_state = await graph.ainvoke(initial_state)

# 5. Check for errors
if final_state.get("error"):
    raise Exception(final_state["error"])

# 6. Return results (already persisted by PersistNode)
return TriageResponse(
    priority=final_state["priority"]["priority"],
    confidence=final_state["priority"]["confidence"],
    assignee=final_state["assignee"]["assignee_user_id"],
    rationale=combined_rationale,
    reply_draft=final_state["reply"]
)
```

### Graph Definition

The graph is defined in `backend/triage/graph.py`:

```python
def create_triage_graph():
    workflow = StateGraph(TriageState)
    
    # Add nodes
    workflow.add_node("fetch_context", context_detailer)
    workflow.add_node("determine_priority", priority_agent)
    workflow.add_node("assign_user", assignee_agent)
    workflow.add_node("generate_rationale", rationale_agent)
    workflow.add_node("generate_reply", reply_agent)
    workflow.add_node("save_results", persist_node)
    
    # Define edges (sequential flow)
    workflow.set_entry_point("fetch_context")
    workflow.add_edge("fetch_context", "determine_priority")
    workflow.add_edge("determine_priority", "assign_user")
    workflow.add_edge("assign_user", "generate_rationale")
    workflow.add_edge("generate_rationale", "generate_reply")
    workflow.add_edge("generate_reply", "save_results")
    workflow.add_edge("save_results", END)
    
    # Compile graph
    graph = workflow.compile()
    return graph
```

## Error Handling

### Agent-Level Error Handling

Each agent handles errors gracefully:

1. **ContextDetailer**:
   - Sets `state["error"] = "No ticket provided to ContextDetailer"` if ticket is invalid
   - Catches exceptions and sets error message

2. **PriorityAgent**:
   - Falls back to P3 with confidence 0.5 if Gemini fails
   - Sets error if context is missing

3. **AssigneeAgent**:
   - Routes to `customer_support` if ticket is ambiguous
   - Routes to `unassigned` if no teams exist
   - Falls back to top-scored team if Gemini fails
   - Catches exceptions and assigns to `unassigned`

4. **RationaleAgent**:
   - Validates all required inputs
   - Provides fallback template rationale if Gemini fails
   - Catches exceptions and provides basic rationale

5. **ReplyAgent**:
   - Falls back to template reply if Gemini fails
   - Ensures reply never exceeds 120 words
   - Sets error if context is missing

6. **PersistNode**:
   - Logs failures to `activity_logs` collection
   - Sets error if ticket is missing
   - Catches exceptions and logs error details

### Workflow-Level Error Handling

- If any agent sets `state["error"]`, the workflow continues execution
- Errors are checked at the end of workflow execution
- API endpoint catches exceptions and returns 500 error with details
- Errors are logged to `activity_logs` collection for audit

## Mock Mode

### Configuration

Set `USE_MOCK_AI=true` in environment variables to enable mock mode.

### Behavior

When mock mode is enabled:

1. **PriorityAgent**: Returns P3 with confidence 0.5 (no Gemini call)
2. **AssigneeAgent**: Selects top-scored team (no Gemini call)
3. **RationaleAgent**: Uses template-based rationale generation
4. **ReplyAgent**: Uses template-based mock replies

This allows the system to work without API keys for testing and development.

## Database Collections

### Collections Used

1. **`tickets`**: Main ticket documents (read by ContextDetailer, updated by PersistNode)
2. **`users`**: Team definitions with skills (read by AssigneeAgent and PersistNode)
3. **`triage_results`**: Historical triage results (written by PersistNode)
4. **`activity_logs`**: Activity events (written by PersistNode)
5. **`comments`**: Ticket comments (read by ContextDetailer)
6. **`attachments`**: Ticket attachments (read by ContextDetailer)

### Database Connection

- Uses **Motor** (async MongoDB driver) for all database operations
- Connections are managed lazily to handle event loop compatibility
- All operations are asynchronous (`async/await`)
- Timezone: All timestamps stored in IST (Indian Standard Time, UTC+5:30)

## Configuration

### Environment Variables

```env
GEMINI_API_KEY=your_gemini_api_key_here  # Optional
USE_MOCK_AI=false  # Set to "true" to disable AI
MONGODB_URL=mongodb://localhost:27017
```

### Model Configuration

All agents use the same Gemini model configuration:

- **Model**: `gemini-2.5-flash`
- **Temperature**: 0.2 (low for consistent, deterministic results)
- **API**: LangChain Google Generative AI (`langchain-google-genai`)
- **API Key**: From `GEMINI_API_KEY` environment variable

### LangGraph Configuration

- **Version**: 0.2.28
- **State Management**: TypedDict-based state schema
- **Execution**: Sequential flow with explicit edges
- **Error Handling**: State-based error propagation

## Example Execution

### Input Ticket

```json
{
  "_id": ObjectId("65abc123def456"),
  "title": "API endpoint returning 500 error",
  "description": "The /api/users endpoint is returning 500 errors for all requests.",
  "category": "Technical",
  "status": "open",
  "created_at": "2025-11-07T13:30:00+05:30"
}
```

### Workflow Execution

#### Step 1: ContextDetailer
```python
Input: {"ticket": {...}}
Output: {
    "context": {
        "title": "API endpoint returning 500 error",
        "body": "The /api/users endpoint is returning 500 errors for all requests.",
        "tags": [],
        "product_area": "Technical",
        "comments": [],
        "attachments": []
    }
}
```

#### Step 2: PriorityAgent
```python
Input: {"context": {...}}
Process: Gemini analyzes ticket content
Output: {
    "priority": {
        "priority": "P1",
        "confidence": 0.92
    }
}
```

#### Step 3: AssigneeAgent
```python
Input: {"context": {...}, "priority": {...}}
Process: 
  - Scores teams: Backend Team (score: 10), DevOps Team (score: 0), ...
  - Gemini selects Backend Team from top 5
Output: {
    "assignee": {
        "assignee_user_id": "backend_team"
    }
}
```

#### Step 4: RationaleAgent
```python
Input: {"context": {...}, "priority": {...}, "assignee": {...}}
Process: Gemini generates two rationales
Output: {
    "rationale": {
        "priority_rationale": "High priority assigned due to major functionality issues affecting users. API errors require immediate attention to prevent further user impact.",
        "assignee_rationale": "Assigned to Backend Team because the ticket requires expertise in python, fastapi, api. This team has the necessary skills to effectively resolve this issue."
    }
}
```

#### Step 5: ReplyAgent
```python
Input: {"context": {...}, "priority": {...}, "assignee": {...}}
Process: Gemini generates reply with P1 expectations
Output: {
    "reply": "Hello,\n\nThank you for reporting this issue. We've flagged this as high priority and our backend team is investigating now. We'll provide an update within 2-4 hours.\n\nWe appreciate your patience.\n\nBest regards,\nSupport Team"
}
```

#### Step 6: PersistNode
```python
Input: All previous outputs
Process:
  - Updates ticket: priority=P1, assignee_user_id=backend_team, status=triaged
  - Combines rationales: "High priority assigned... | Assigned to Backend Team..."
  - Creates triage_results document
  - Logs activity to activity_logs
Output: {"error": None}
```

### Final Result

```json
{
  "priority": "P1",
  "confidence": 0.92,
  "assignee": "backend_team",
  "rationale": "High priority assigned due to major functionality issues affecting users. API errors require immediate attention to prevent further user impact. | Assigned to Backend Team because the ticket requires expertise in python, fastapi, api. This team has the necessary skills to effectively resolve this issue.",
  "reply_draft": "Hello,\n\nThank you for reporting this issue. We've flagged this as high priority and our backend team is investigating now. We'll provide an update within 2-4 hours.\n\nWe appreciate your patience.\n\nBest regards,\nSupport Team"
}
```

## Architecture Benefits

1. **Modularity**: Each agent has a single, well-defined responsibility
2. **Extensibility**: Easy to add new agents or modify existing ones
3. **Error Resilience**: Fallbacks at each step ensure workflow continues
4. **Observability**: All steps logged to `activity_logs` for audit trail
5. **Testability**: Can test each agent independently
6. **Scalability**: LangGraph handles state management and execution efficiently
7. **Maintainability**: Clear separation of concerns makes debugging easier

## Performance Considerations

- **Average Execution Time**: 2-5 seconds for full workflow
- **Bottlenecks**: Gemini API calls (3-4 calls per workflow)
- **Optimization Opportunities**:
  - Parallel execution of PriorityAgent and AssigneeAgent (future enhancement)
  - Caching of team data
  - Batch API calls where possible

## Troubleshooting

### Common Issues

1. **LangChain Debug Error**: 
   - **Issue**: `module 'langchain' has no attribute 'debug'`
   - **Solution**: Workaround in `graph.py` patches `langchain.debug` if missing

2. **Event Loop Errors**:
   - **Issue**: `RuntimeError: Event loop is closed`
   - **Solution**: Database connection uses lazy initialization with event loop detection

3. **Gemini API Failures**:
   - **Issue**: API key invalid or quota exceeded
   - **Solution**: System falls back to mock mode or template responses

4. **Database Connection Issues**:
   - **Issue**: MongoDB not accessible
   - **Solution**: Check `MONGODB_URL` and ensure MongoDB is running

## Future Enhancements

- [ ] **Conditional Edges**: Route based on priority (P0 might skip some steps)
- [ ] **Parallel Execution**: Run PriorityAgent and AssigneeAgent in parallel
- [ ] **Feedback Loop**: Learn from manual overrides and improve assignments
- [ ] **Multi-language Support**: Generate replies in customer's language
- [ ] **Sentiment Analysis**: Adjust priority based on customer sentiment
- [ ] **Historical Learning**: Use past triage results to improve accuracy
- [ ] **Custom Prompts**: Allow configuration of agent prompts
- [ ] **Workflow Visualization**: Visual representation of workflow execution

## Testing

The workflow is tested via smoke tests in `backend/tests/test_smoke.py`:

- **test_create_and_triage_ticket**: Validates full workflow execution
- Tests verify: priority assignment, assignee selection, rationale generation, reply generation, data persistence

See `README.md` for testing instructions.

---

**Last Updated**: Based on latest implementation with event loop fixes and LangChain debug workaround.
