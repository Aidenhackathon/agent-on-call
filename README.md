# Agent-on-Call – AI-Powered Ticket Triage System

A full-stack AI-powered helpdesk ticket system that automatically triages tickets to assign priority, suggest assignees, and generate first reply drafts using Google Gemini AI.

## 🎯 Features

- **Auto-Triage with AI**: Automatically assigns priority (P0-P3), suggests assignee, and generates reply drafts
- **Persistent Data**: All triage results persist in MongoDB and remain after refresh
- **Real-time Updates**: Instant ticket updates via REST API
- **Activity Logging**: Complete audit trail of all ticket actions
- **Editable Reply Drafts**: Users can modify AI-generated replies before saving
- **Responsive UI**: Modern Material-UI interface with clean design
- **Fallback Handling**: Graceful error handling if AI triage fails
- **Docker Support**: Complete containerized setup with docker-compose

## 🏗️ Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **MongoDB** - NoSQL database for flexible data storage
- **Motor** - Async MongoDB driver
- **Google Gemini AI** - AI-powered triage logic
- **pytest** - Testing framework

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
│   ├── routes/
│   │   └── tickets.py          # Ticket CRUD and triage endpoints
│   ├── services/
│   │   └── ai_triage.py        # Gemini AI integration
│   ├── tests/
│   │   └── test_smoke.py       # Smoke tests
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Backend container config
│   └── .env.example            # Environment variables template
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
│   ├── Dockerfile              # Frontend container config
│   └── .env.example            # Environment variables template
├── docker-compose.yml          # Multi-container orchestration
├── .env.example                # Root environment variables
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Google Gemini API key (get one at https://makersuite.google.com/app/apikey)

### Setup Instructions

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd agent-on-call
   ```

2. **Set up environment variables**:
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env and add your Gemini API key
   # GEMINI_API_KEY=your_actual_api_key_here
   ```

3. **Start the application with Docker**:
   ```bash
   docker-compose up --build
   ```

   This will start three containers:
   - MongoDB (port 27017)
   - Backend API (port 8000)
   - Frontend UI (port 5173)

4. **Access the application**:
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
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
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
   cp .env.example .env
   # Edit .env if needed
   ```

4. Start the frontend:
   ```bash
   npm run dev
   ```

## 📡 API Endpoints

### Tickets

| Method | Endpoint | Description |
|--------|----------|-------------|
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
  "created_at": "2025-10-28T10:30:00",
  "updated_at": "2025-10-28T10:30:00",
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
  "assignee": "DevOps",
  "rationale": "Critical infrastructure issue affecting customer access. Requires immediate DevOps attention.",
  "reply_draft": "Hello,\n\nThank you for reporting this critical issue. We understand the urgency and have immediately escalated this to our DevOps team..."
}
```

#### Get Ticket Details
```bash
curl http://localhost:8000/tickets/65abc123def456
```

## 🤖 AI Triage Logic

The AI triage system analyzes tickets and provides:

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

### Reply Draft Generation
- Professional and empathetic tone
- Acknowledges the issue
- Sets clear expectations
- Maximum 120 words

## 🧪 Testing

### Run Smoke Tests

```bash
cd backend
pytest tests/test_smoke.py -v
```

### Test Coverage

The smoke test validates:
- ✅ Ticket creation
- ✅ AI triage execution
- ✅ Data persistence
- ✅ Priority assignment
- ✅ Assignee suggestion
- ✅ Reply draft generation

## 🎨 UI Features

### Ticket Board View
- Card-based layout showing all tickets
- Status and priority badges
- Quick navigation to ticket details

### Ticket Detail View
- Complete ticket information
- AI triage results with confidence scores
- Editable reply drafts
- Activity timeline
- Delete functionality

### Create Ticket Form
- Title, description, and category fields
- Form validation
- Immediate redirect to created ticket

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
MONGODB_URL=mongodb://mongodb:27017
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

### Docker issues
- Clear Docker cache: `docker-compose down -v`
- Rebuild containers: `docker-compose up --build`

## 📝 API Documentation

Visit http://localhost:8000/docs for interactive API documentation powered by FastAPI's automatic OpenAPI generation.

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

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run tests: `pytest`
4. Submit a pull request

## 📄 License

This project is provided as-is for educational and demonstration purposes.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check Docker logs: `docker-compose logs`

## 🎯 Future Enhancements

- [ ] User authentication and authorization
- [ ] Email notifications
- [ ] Ticket assignment workflows
- [ ] SLA tracking
- [ ] Analytics dashboard
- [ ] Multi-language support
- [ ] Export to CSV/PDF
- [ ] Real-time updates with WebSockets

---

**Built with ❤️ using FastAPI, React, MongoDB, and Google Gemini AI**
