# Agent-on-Call – AI-Powered Ticket Triage System

## 📋 Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [LangGraph Architecture](#langgraph-architecture)
5. [Project Structure](#project-structure)
6. [Quick Start](#quick-start)
7. [API Documentation](#api-documentation)
8. [Database Schema](#database-schema)
9. [Configuration](#configuration)
10. [Deployment](#deployment)

---

## Overview

**Agent-on-Call** is a full-stack AI-powered helpdesk ticket triage system that automatically analyzes support tickets, assigns priority levels, suggests appropriate teams for assignment, and generates professional customer reply drafts. The system leverages **LangGraph** multi-agent workflows and **Google Gemini AI** to provide intelligent, context-aware ticket routing.

### Key Capabilities

- **Intelligent Triage**: Automatically determines ticket priority (P0-P3) based on content analysis
- **Smart Assignment**: Matches tickets to teams based on skill relevance and context
- **AI-Generated Replies**: Creates professional, empathetic customer response drafts (≤120 words)
- **Persistent Storage**: All data stored in MongoDB with complete audit trails
- **Real-time Updates**: RESTful API with instant ticket updates
- **Modern UI**: Responsive React interface with Material-UI components

---

## Features

### Core Features
- ✅ **Auto-Triage with AI**: Automatic priority assignment (P0-P3) with confidence scores
- ✅ **Context-Based Assignment**: Team assignment based purely on skill matching with ticket content
- ✅ **AI Reply Generation**: Professional customer reply drafts with priority-appropriate messaging
- ✅ **Activity Logging**: Complete audit trail of all ticket actions and triage runs
- ✅ **Editable Replies**: Users can modify AI-generated replies before sending
- ✅ **Persistent Data**: All triage results persist in MongoDB
- ✅ **Error Handling**: Graceful fallbacks if AI services are unavailable
- ✅ **Docker Support**: Complete containerized setup with docker-compose

### Technical Features
- **Multi-Agent Workflow**: LangGraph-based sequential agent pipeline
- **Async Operations**: Fully asynchronous backend with Motor (async MongoDB driver)
- **RESTful API**: FastAPI with automatic OpenAPI documentation
- **Type Safety**: Pydantic schemas for request/response validation
- **Timezone Handling**: IST (Indian Standard Time) for all timestamps
- **Mock Mode**: Test without API keys using intelligent fallback logic

---

## Tech Stack

### Backend
- **FastAPI** (0.109.0) - High-performance Python web framework
- **MongoDB** (7.0) - NoSQL database for flexible data storage
- **Motor** (3.3.2) - Async MongoDB driver
- **LangGraph** (0.2.28) - Multi-agent workflow orchestration
- **LangChain** (0.3.6) - LLM framework integration
- **Google Gemini AI** (2.0-flash-exp) - AI-powered triage and reply generation
- **Pydantic** (2.7.4) - Data validation and serialization
- **Pytest** (7.4.3) - Testing framework

### Frontend
- **React** (18) - Modern UI library
- **Vite** - Fast build tool and dev server
- **Material-UI (MUI)** - Professional React component library
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **MongoDB** - Database container

---

## LangGraph Architecture

### Overview

The system uses a **LangGraph-based multi-agent workflow** to automatically triage support tickets. The workflow consists of 5 sequential agents that analyze tickets and determine priority, assignment, and generate customer replies.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Ticket Triage Workflow                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Ticket Created │
                    │   (MongoDB)     │
                    └────────┬────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────┐
        │        1. ContextAgent                     │
        │      (fetch_context)                       │
        │  • Fetches ticket from MongoDB             │
        │  • Retrieves comments (last 10)            │
        │  • Retrieves attachments (last 5)          │
        │  • Builds compact context object           │
        └──────────────┬─────────────────────────────┘
                       │
                       ▼
        ┌────────────────────────────────────────────┐
        │       2. PriorityAgent                     │
        │    (determine_priority)                    │
        │  • Heuristic keyword analysis              │
        │  • Gemini AI validation/refinement         │
        │  • Returns: P0/P1/P2/P3 + confidence       │
        └──────────────┬─────────────────────────────┘
                       │
                       ▼
        ┌────────────────────────────────────────────┐
        │       3. AssigneeAgent                     │
        │       (assign_user)                        │
        │  • Fetches all teams from MongoDB          │
        │  • Scores teams by skill match             │
        │  • Gemini AI final selection               │
        │  • Returns: team_id + rationale            │
        └──────────────┬─────────────────────────────┘
                       │
                       ▼
        ┌────────────────────────────────────────────┐
        │        4. ReplyAgent                       │
        │      (generate_reply)                      │
        │  • Gemini AI reply generation              │
        │  • Priority-based expectations             │
        │  • Strict 120-word limit                   │
        │  • Returns: reply draft text               │
        └──────────────┬─────────────────────────────┘
                       │
                       ▼
        ┌────────────────────────────────────────────┐
        │        5. PersistNode                      │
        │       (save_results)                       │
        │  • Updates ticket in MongoDB               │
        │  • Creates triage_results document         │
        │  • Logs activity to activity_logs          │
        │  • Returns: final state                    │
        └──────────────┬─────────────────────────────┘
                       │
                       ▼
                    ┌─────┐
                    │ END │
                    └─────┘
```

### Agent Details

#### 1. ContextAgent
- **Purpose**: Gathers all relevant ticket information
- **Input**: Ticket document from MongoDB
- **Process**: 
  - Extracts title, description, tags, product_area
  - Fetches related comments and attachments
  - Builds compact context dictionary
- **Output**: Context object with ticket details

#### 2. PriorityAgent
- **Purpose**: Determines ticket priority using heuristics + AI
- **Input**: Context from ContextAgent
- **Process**:
  - Keyword-based heuristic analysis (P0/P1/P2/P3)
  - Gemini AI validation and refinement
  - Confidence score calculation
- **Output**: Priority level (P0-P3), confidence, rationale

#### 3. AssigneeAgent
- **Purpose**: Assigns ticket to best team based on skills
- **Input**: Context + Priority info
- **Process**:
  - Fetches all teams from MongoDB
  - Scores teams by skill match (context-based only)
  - Gemini AI selects best team from top candidates
- **Output**: Team ID, assignment rationale

#### 4. ReplyAgent
- **Purpose**: Generates professional customer reply draft
- **Input**: Context + Priority + Assignee info
- **Process**:
  - Gemini AI generates empathetic reply
  - Priority-based expectations (P0: 30min updates, P1: 2-4hrs, etc.)
  - Enforces 120-word limit
- **Output**: Reply draft text (≤120 words)

#### 5. PersistNode
- **Purpose**: Saves all triage results to MongoDB
- **Input**: All agent outputs
- **Process**:
  - Updates ticket document
  - Creates triage_results document
  - Logs activity to activity_logs
- **Output**: Final state (success/error)

### State Schema

```python
class TriageState(TypedDict, total=False):
    ticket: Optional[dict]      # Original ticket from MongoDB
    context: Optional[dict]     # Compact context from ContextAgent
    priority: Optional[dict]    # Priority info from PriorityAgent
    assignee: Optional[dict]    # Assignee info from AssigneeAgent
    reply: Optional[str]        # Reply draft from ReplyAgent
    error: Optional[str]        # Error message if any step fails
```

### Execution Flow

```python
# 1. Create graph
graph = create_triage_graph()

# 2. Initialize state
initial_state = {
    "ticket": ticket,  # From MongoDB
    "context": None,
    "priority": None,
    "assignee": None,
    "reply": None,
    "error": None
}

# 3. Execute workflow
final_state = await graph.ainvoke(initial_state)

# 4. Check for errors
if final_state.get("error"):
    raise Exception(final_state["error"])

# 5. Results already persisted by PersistNode
```

### Error Handling

Each agent handles errors gracefully:
- **ContextAgent**: Sets error if ticket invalid
- **PriorityAgent**: Falls back to heuristics if Gemini fails
- **AssigneeAgent**: Falls back to top-scored team if Gemini fails
- **ReplyAgent**: Falls back to template reply if Gemini fails
- **PersistNode**: Logs errors to activity_logs collection

---

## Project Structure

```
agent-on-call/
├── backend/
│   ├── main.py                    # FastAPI application entry point
│   ├── database.py                # MongoDB connection management
│   ├── models.py                  # Data models
│   ├── schemas.py                 # Pydantic schemas for validation
│   ├── seed_users.py              # Database seeding script
│   ├── clear_database.py          # Database clearing script
│   ├── routes/
│   │   └── tickets.py             # Ticket CRUD and triage endpoints
│   ├── services/
│   │   └── ai_triage.py           # Legacy Gemini AI integration
│   ├── triage/
│   │   ├── __init__.py
│   │   ├── graph.py               # LangGraph workflow definition
│   │   ├── state.py               # TriageState schema
│   │   └── agents/
│   │       ├── context_agent.py   # Context gathering agent
│   │       ├── priority_agent.py  # Priority determination agent
│   │       ├── assignee_agent.py  # Team assignment agent
│   │       ├── reply_agent.py     # Reply generation agent
│   │       └── persist_node.py    # Database persistence node
│   ├── tests/
│   │   └── test_smoke.py          # Smoke tests
│   ├── requirements.txt           # Python dependencies
│   └── Dockerfile                 # Backend container config
├── frontend/
│   ├── src/
│   │   ├── App.jsx                # Main app component
│   │   ├── main.jsx               # Entry point
│   │   ├── api/
│   │   │   └── api.js             # API client
│   │   ├── components/
│   │   │   ├── Navigation.jsx     # Navigation bar
│   │   │   ├── TicketCard.jsx     # Ticket card component
│   │   │   ├── TriageResultCard.jsx  # Triage results display
│   │   │   ├── ActivityLog.jsx    # Activity timeline
│   │   │   └── TicketForm.jsx     # Ticket creation form
│   │   └── pages/
│   │       ├── TicketList.jsx     # Ticket list page
│   │       ├── TicketDetail.jsx   # Ticket detail page
│   │       └── CreateTicket.jsx   # Create ticket page
│   ├── package.json               # Node dependencies
│   ├── vite.config.js             # Vite configuration
│   └── Dockerfile                 # Frontend container config
├── docker-compose.yml             # Multi-container orchestration
├── README.md                      # Quick start guide
├── PROJECT.md                     # This comprehensive documentation
└── LANGGRAPH_FLOW.md              # Detailed LangGraph flow documentation
```

---

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Google Gemini API key (optional, get one at https://makersuite.google.com/app/apikey)

### Setup Instructions

1. **Clone the repository** or navigate to the project directory:
   ```bash
   cd agent-on-call
   ```

2. **Set up environment variables**:
   ```bash
   # Create .env file in root directory
   GEMINI_API_KEY=your_actual_api_key_here
   USE_MOCK_AI=false
   MONGODB_URL=mongodb://mongodb:27017
   ```

3. **Start the application with Docker**:
   ```bash
   docker-compose up --build
   ```

   This will start three containers:
   - MongoDB (port 27017)
   - Backend API (port 8000)
   - Frontend UI (port 5173)

4. **Seed the database** (optional):
   ```bash
   docker exec agent-on-call-backend python seed_users.py
   ```

5. **Access the application**:
   - **Frontend UI**: http://localhost:5173
   - **Backend API Docs**: http://localhost:8000/docs
   - **Backend API**: http://localhost:8000

### Without Docker (Local Development)

#### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows PowerShell
   source venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure MongoDB is running:
   ```bash
   docker run -d -p 27017:27017 --name mongodb mongo:7.0
   ```

5. Start the backend:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the frontend:
   ```bash
   npm run dev
   ```

---

## API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Tickets

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tickets` | List all tickets |
| GET | `/tickets/{id}` | Get single ticket |
| POST | `/tickets` | Create new ticket |
| PUT | `/tickets/{id}` | Update ticket |
| DELETE | `/tickets/{id}` | Delete ticket |
| POST | `/tickets/{id}/triage` | Trigger AI triage |

### Example Requests

#### Create a Ticket
```bash
curl -X POST http://localhost:8000/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "title": "API endpoint returning 500 error",
    "description": "The /api/users endpoint is returning 500 errors for all requests."
  }'
```

**Response:**
```json
{
  "id": "65abc123def456",
  "title": "API endpoint returning 500 error",
  "description": "The /api/users endpoint is returning 500 errors for all requests.",
  "category": "General",
  "status": "open",
  "priority": null,
  "assignee": null,
  "created_at": "2025-11-07T13:30:00+05:30",
  "updated_at": "2025-11-07T13:30:00+05:30",
  "activities": [...]
}
```

#### Trigger AI Triage
```bash
curl -X POST http://localhost:8000/tickets/65abc123def456/triage
```

**Response:**
```json
{
  "priority": "P1",
  "confidence": 0.92,
  "assignee": "backend_team",
  "rationale": "API error requires backend team expertise. High priority issue affecting core functionality.",
  "reply_draft": "Hello,\n\nThank you for reporting this issue. We've flagged this as high priority and our backend team is investigating now..."
}
```

### Interactive API Documentation

Visit http://localhost:8000/docs for interactive API documentation powered by FastAPI's automatic OpenAPI generation.

---

## Database Schema

### Collections

#### 1. `tickets`
Main ticket documents.

```javascript
{
  "_id": ObjectId,
  "title": string,
  "description": string,
  "category": string,  // Default: "General"
  "status": string,    // "open", "triaged", "in-progress", "resolved", "closed"
  "priority": string,  // "P0", "P1", "P2", "P3"
  "assignee": string,  // Team name for display
  "assignee_user_id": string,  // Team ID
  "ai_rationale": string,
  "ai_reply_draft": string,
  "ai_confidence": float,
  "created_at": datetime (IST),
  "updated_at": datetime (IST),
  "activities": [
    {
      "timestamp": datetime (IST),
      "action": string,
      "details": string,
      "user": string
    }
  ]
}
```

#### 2. `users`
Team definitions.

```javascript
{
  "_id": string,  // Team ID (e.g., "backend_team")
  "name": string,  // Team name (e.g., "Backend Development Team")
  "skills": [string]  // Array of skill keywords
}
```

#### 3. `triage_results`
Historical triage results.

```javascript
{
  "_id": ObjectId,
  "ticket_id": string,
  "priority": string,
  "priority_confidence": float,
  "priority_rationale": string,
  "assignee_user_id": string,
  "assignee_rationale": string,
  "reply_draft": string,
  "created_at": datetime (IST)
}
```

#### 4. `activity_logs`
Activity events.

```javascript
{
  "_id": ObjectId,
  "ticket_id": string,
  "event_type": string,  // "triage_run", "triage_failed"
  "payload": object,
  "timestamp": datetime (IST)
}
```

#### 5. `comments`
Ticket comments (optional).

```javascript
{
  "_id": ObjectId,
  "ticket_id": string,
  "text": string,
  "created_at": datetime (IST)
}
```

#### 6. `attachments`
Ticket attachments (optional).

```javascript
{
  "_id": ObjectId,
  "ticket_id": string,
  "filename": string,
  "size": number
}
```

---

## Configuration

### Environment Variables

#### Backend (.env)
```env
MONGODB_URL=mongodb://mongodb:27017  # For Docker
# MONGODB_URL=mongodb://localhost:27017  # For local development
GEMINI_API_KEY=your_gemini_api_key_here
USE_MOCK_AI=false
```

#### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

### Mock AI Mode

For testing without Gemini API, set `USE_MOCK_AI=true` in backend `.env`. The mock triage provides intelligent fallback logic based on keywords.

### Timezone

All timestamps are stored and displayed in **IST (Indian Standard Time, UTC+5:30)**.

---

## Deployment

### Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

### Manual Deployment

1. **MongoDB**: Deploy to MongoDB Atlas or self-hosted instance
2. **Backend**: Deploy FastAPI to Heroku, AWS, GCP, etc.
3. **Frontend**: Deploy React app to Vercel, Netlify, etc.
4. **Environment Variables**: Update all environment variables accordingly

### Database Management

#### Clear Database
```bash
docker exec agent-on-call-backend python clear_database.py
```

#### Seed Teams
```bash
docker exec agent-on-call-backend python seed_users.py
```

---

## Priority Levels

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

---

## Team Assignment Logic

Teams are assigned based purely on **skill matching with ticket content**:

1. **Skill Scoring**: Each team skill that matches ticket content (title, description, tags, product_area) adds +10 points
2. **Top Candidates**: Teams are sorted by score (highest first)
3. **AI Selection**: Gemini AI selects best team from top 5 candidates
4. **Fallback**: If AI unavailable, top-scored team is selected

**Note**: Workload is NOT considered in assignment - only skill relevance.

---

## Example Workflow

1. **Create a ticket**: "API endpoint returning 500 error"
2. **Click "Auto-Triage"** button on ticket detail page
3. **Workflow executes**:
   - ContextAgent: Gathers ticket details
   - PriorityAgent: Determines P1 (API error = high priority)
   - AssigneeAgent: Assigns to Backend Team (skill match: "api", "backend")
   - ReplyAgent: Generates professional reply draft
   - PersistNode: Saves all results to MongoDB
4. **View results**: Priority, assignee, and reply draft displayed
5. **Edit reply** if needed
6. **Data persists** after page refresh

---

## Troubleshooting

### Backend Issues
- **MongoDB connection failed**: Ensure MongoDB container is running
- **AI triage fails**: Check GEMINI_API_KEY or enable USE_MOCK_AI=true
- **Timestamp issues**: All timestamps are in IST timezone

### Frontend Issues
- **Can't connect to backend**: Check VITE_API_URL in frontend .env
- **CORS errors**: Verify backend CORS settings in main.py

### Docker Issues
- **Port conflicts**: Change ports in docker-compose.yml
- **Container restarting**: Check logs with `docker-compose logs backend`

---

## Security Considerations

- Never commit `.env` files with real API keys
- Use environment variables for sensitive data
- Implement authentication for production use
- Validate and sanitize all user inputs
- Use HTTPS in production

---

## Performance

- Average triage time: 2-5 seconds
- Supports concurrent requests
- MongoDB indexing for fast queries
- Async operations with Motor driver
- Efficient LangGraph workflow execution

---

## Future Enhancements

- [ ] User authentication and authorization
- [ ] Email notifications
- [ ] Ticket assignment workflows
- [ ] SLA tracking
- [ ] Analytics dashboard
- [ ] Multi-language support
- [ ] Export to CSV/PDF
- [ ] Real-time updates with WebSockets
- [ ] Conditional workflow routing based on priority
- [ ] Parallel agent execution for performance
- [ ] Feedback loop for learning from manual overrides

---

## License

This project is provided as-is for educational and demonstration purposes.

---

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check Docker logs: `docker-compose logs`
4. Review LangGraph flow documentation: `LANGGRAPH_FLOW.md`

---

**Built with ❤️ using FastAPI, React, MongoDB, LangGraph, and Google Gemini AI**

