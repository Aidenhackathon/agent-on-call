# Agent-on-Call – AI-Powered Ticket Triage System

A full-stack AI-powered helpdesk ticket system that automatically triages tickets to assign priority, suggest assignees, and generate first reply drafts using Google Gemini AI and LangGraph multi-agent workflows.

## 🎯 Features

- **Auto-Triage with AI**: Automatically assigns priority (P0-P3), suggests assignee, and generates reply drafts using LangGraph multi-agent workflow
- **Multi-Agent System**: 5 specialized agents working in sequence (Context, Priority, Assignee, Rationale, Reply)
- **Persistent Data**: All triage results persist in MongoDB and remain after refresh
- **Real-time Updates**: Instant ticket updates via REST API
- **Activity Logging**: Complete audit trail of all ticket actions
- **Editable Reply Drafts**: Users can modify AI-generated replies before saving
- **Responsive UI**: Modern Material-UI interface with clean design
- **Fallback Handling**: Graceful error handling if AI triage fails
- **Docker Support**: Complete containerized setup with docker-compose
- **Comprehensive Testing**: Full smoke test suite with 6 passing tests

## 🏗️ Tech Stack

### Backend
- **FastAPI** (0.109.0) - High-performance Python web framework
- **MongoDB** (7.0) - NoSQL database for flexible data storage
- **Motor** (3.3.2) - Async MongoDB driver
- **LangGraph** (0.2.28) - Multi-agent workflow orchestration
- **LangChain** (0.3.6) - LLM framework integration
- **Google Gemini AI** (2.0-flash) - AI-powered triage logic
- **Pydantic** (2.7.4) - Data validation and serialization
- **Pytest** (7.4.3) - Testing framework

### Frontend
- **React 18** - Modern UI library
- **Vite** - Fast build tool
- **Material-UI (MUI)** - Professional React components
- **React Router** - Client-side routing
- **Axios** - HTTP client

## 📁 Project Structure

```
agent-on-call/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # MongoDB connection management
│   ├── models.py               # Data models
│   ├── schemas.py              # Pydantic schemas for validation
│   ├── seed_users.py           # Database seeding script
│   ├── routes/
│   │   └── tickets.py          # Ticket CRUD and triage endpoints
│   ├── services/
│   │   └── ai_triage.py        # Legacy Gemini AI integration
│   ├── triage/
│   │   ├── state.py            # LangGraph state definition
│   │   ├── graph.py            # LangGraph workflow definition
│   │   └── agents/
│   │       ├── context_detailer.py    # Extracts ticket context
│   │       ├── priority_agent.py   # Determines priority
│   │       ├── assignee_agent.py   # Assigns ticket to team
│   │       ├── rationale_agent.py  # Generates rationale explanations
│   │       ├── reply_agent.py      # Generates reply draft
│   │       └── persist_node.py     # Persists results to MongoDB
│   ├── tests/
│   │   ├── conftest.py         # Pytest configuration
│   │   └── test_smoke.py       # Smoke tests (6 tests)
│   ├── requirements.txt        # Python dependencies
│   ├── requirements-dev.txt    # Development dependencies
│   └── Dockerfile              # Backend container config
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main app component
│   │   ├── main.jsx            # Entry point
│   │   ├── api/
│   │   │   └── api.js          # API client
│   │   ├── components/
│   │   │   ├── Navigation.jsx
│   │   │   ├── TicketCard.jsx
│   │   │   ├── TriageResultCard.jsx
│   │   │   ├── ActivityLog.jsx
│   │   │   └── TicketForm.jsx
│   │   └── pages/
│   │       ├── TicketList.jsx
│   │       ├── TicketDetail.jsx
│   │       └── CreateTicket.jsx
│   ├── package.json            # Node dependencies
│   ├── vite.config.js          # Vite configuration
│   └── Dockerfile              # Frontend container config
├── docker-compose.yml          # Multi-container orchestration
├── README.md                   # This file
└── LANGGRAPH_FLOW.md           # Detailed LangGraph workflow documentation
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Google Gemini API key (optional, get one at https://makersuite.google.com/app/apikey)
- Python 3.12+ (for local development)
- Node.js 18+ (for local frontend development)

### Setup Instructions

1. **Clone the repository** (if applicable) or navigate to the project directory:
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
   pip install -r requirements-dev.txt  # For development
   ```

4. Set environment variables:
   ```bash
   # Create .env file
   MONGODB_URL=mongodb://localhost:27017
   GEMINI_API_KEY=your_api_key_here
   USE_MOCK_AI=false
   ```

5. Ensure MongoDB is running (install locally or use Docker):
   ```bash
   docker run -d -p 27017:27017 --name mongodb mongo:7.0
   ```

6. Start the backend:
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

3. Set environment variables:
   ```bash
   # Create .env file
   VITE_API_URL=http://localhost:8000
   ```

4. Start the frontend:
   ```bash
   npm run dev
   ```

## 🧪 Testing

### Run Smoke Tests

```bash
cd backend
pytest tests/test_smoke.py -v
```

### Test Coverage

The smoke test suite includes 6 comprehensive tests:

1. ✅ **test_root** - Root endpoint health check
2. ✅ **test_create_ticket** - Ticket creation functionality
3. ✅ **test_list_tickets** - Ticket listing functionality
4. ✅ **test_create_and_triage_ticket** - Full triage workflow (create → triage → verify)
5. ✅ **test_update_ticket** - Ticket update functionality
6. ✅ **test_delete_ticket** - Ticket deletion functionality

All tests validate:
- API endpoint responses
- Data persistence in MongoDB
- AI triage execution
- Priority assignment
- Assignee suggestion
- Reply draft generation
- Error handling

See [TESTING.md](TESTING.md) for detailed testing documentation.

## 📡 API Endpoints

### Tickets

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint (health check) |
| GET | `/tickets` | List all tickets |
| GET | `/tickets/{id}` | Get single ticket |
| POST | `/tickets` | Create new ticket |
| PUT | `/tickets/{id}` | Update ticket |
| DELETE | `/tickets/{id}` | Delete ticket |
| POST | `/tickets/{id}/triage` | Trigger AI triage |

### Example API Requests

#### Create a Ticket
```bash
curl -X POST http://localhost:8000/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Website is down",
    "description": "Customer cannot access dashboard",
    "category": "Critical"
  }'
```

**Response:**
```json
{
  "id": "65abc123def456",
  "title": "Website is down",
  "description": "Customer cannot access dashboard",
  "category": "Critical",
  "status": "open",
  "priority": null,
  "assignee": null,
  "created_at": "2025-10-28T10:30:00+05:30",
  "updated_at": "2025-10-28T10:30:00+05:30",
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
  "priority": "P0",
  "confidence": 0.92,
  "assignee": "devops_team",
  "rationale": "Critical priority assigned due to system outage affecting customer access. Immediate attention required to minimize customer impact and prevent escalation. | Assigned to DevOps Team because the ticket requires expertise in kubernetes, docker, infrastructure. This team has the necessary skills to effectively resolve this issue.",
  "reply_draft": "Hello,\n\nThank you for reporting this critical issue. We understand the urgency and have immediately escalated this to our DevOps team..."
}
```

Visit http://localhost:8000/docs for interactive API documentation.

## 🤖 AI Triage Logic (LangGraph Multi-Agent System)

The AI triage system uses a **LangGraph-based multi-agent workflow** with 5 specialized agents working in sequence:

### Workflow Flow

1. **ContextDetailer** → Extracts ticket context (title, description, tags, comments, attachments)
2. **PriorityAgent** → Determines priority (P0/P1/P2/P3) using heuristics + Gemini AI
3. **AssigneeAgent** → Assigns ticket to best team based on skill matching
4. **RationaleAgent** → Generates explanations for priority and assignee decisions
5. **ReplyAgent** → Generates professional customer reply draft (≤120 words)
6. **PersistNode** → Saves all results to MongoDB

### Priority Assignment
- **P0**: Critical system outage, security breach, data loss (immediate attention)
- **P1**: Major functionality broken, significant user impact (urgent)
- **P2**: Moderate issues with workarounds (normal priority)
- **P3**: Minor issues, feature requests, questions (low priority)

### Assignee Suggestions
- **DevOps**: Infrastructure, deployment, system outages
- **Backend Support**: API issues, server errors, database problems
- **Frontend Support**: UI bugs, display issues
- **Finance**: Billing, payments, invoicing
- **Product**: Feature requests, product questions
- **Customer Support**: General inquiries, account issues

See [LANGGRAPH_FLOW.md](LANGGRAPH_FLOW.md) for detailed workflow documentation.

## 🔧 Configuration

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

## 📊 Example Workflow

1. **Create a ticket**: "Customer cannot access dashboard"
2. **Click "Auto-Triage"** button
3. **AI responds with**:
   - Priority: P0
   - Confidence: 92%
   - Assignee: "DevOps"
   - Rationale: "Critical infrastructure issue affecting customer access"
   - Reply draft: Professional response ready to send
4. **Edit the reply** if needed
5. **Save changes** - all data persists
6. **Refresh page** - triage results remain visible

## 🚢 Deployment

### Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

### Manual Deployment

1. Deploy MongoDB (Atlas, self-hosted, etc.)
2. Deploy FastAPI backend (Heroku, AWS, GCP, etc.)
3. Deploy React frontend (Vercel, Netlify, etc.)
4. Update environment variables accordingly

## 🛠️ Troubleshooting

### Backend won't start
- Ensure MongoDB is running: `docker ps | grep mongodb`
- Check environment variables in `.env`
- Verify Python dependencies: `pip install -r requirements.txt`

### Frontend can't connect to backend
- Verify backend is running: `curl http://localhost:8000/`
- Check VITE_API_URL in frontend `.env`
- Ensure CORS is configured correctly in backend

### AI triage fails
- Verify GEMINI_API_KEY is set correctly
- Check API quota and limits
- Enable mock mode: `USE_MOCK_AI=true`
- Check logs for detailed error messages

### Docker issues
- Clear Docker cache: `docker-compose down -v`
- Rebuild containers: `docker-compose up --build`
- Check logs: `docker-compose logs backend`

### Test failures
- Ensure MongoDB is running
- Check database connection: `MONGODB_URL=mongodb://localhost:27017`
- Run tests with verbose output: `pytest tests/test_smoke.py -v -s`

## 📝 Documentation

- **[LANGGRAPH_FLOW.md](LANGGRAPH_FLOW.md)** - Detailed LangGraph workflow documentation
- **API Docs** - Interactive API documentation at http://localhost:8000/docs

## 🔒 Security Considerations

- Never commit `.env` files with real API keys
- Use environment variables for sensitive data
- Implement authentication for production use
- Validate and sanitize all user inputs
- Use HTTPS in production

## 📈 Performance

- Average triage time: 2-5 seconds
- Supports concurrent requests
- MongoDB indexing for fast queries
- Async operations with Motor driver
- Efficient LangGraph workflow execution

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run tests: `pytest tests/test_smoke.py -v`
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is provided as-is for educational and demonstration purposes.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check Docker logs: `docker-compose logs`
4. Review LangGraph workflow documentation: [LANGGRAPH_FLOW.md](LANGGRAPH_FLOW.md)

## 🎯 Recent Updates

### Latest Changes
- ✅ Fixed event loop issues with Motor/MongoDB in test environment
- ✅ Added comprehensive smoke test suite (6 tests, all passing)
- ✅ Fixed LangChain debug attribute error in LangGraph workflow
- ✅ Improved error handling and database connection management
- ✅ Added lazy database connection for better test compatibility

## 🎯 Future Enhancements

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

**Built with ❤️ using FastAPI, React, MongoDB, LangGraph, and Google Gemini AI**
