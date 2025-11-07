# Agent-on-Call - Technical Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (React)                     │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Ticket  │  │  Ticket  │  │  Create  │  │ Activity │    │
│  │  List   │  │  Detail  │  │  Ticket  │  │   Log    │    │
│  └─────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                          ↕ REST API                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Ticket Routes (CRUD + Triage)            │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         AI Triage Service (Gemini Integration)        │  │
│  │  • Priority Assignment  • Assignee Suggestion         │  │
│  │  • Reply Generation     • Confidence Scoring          │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          Database Layer (Motor/AsyncIO)               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    MongoDB Database                          │
│  ┌─────────────────┐           ┌──────────────────┐        │
│  │ Tickets         │           │ Activities       │        │
│  │ Collection      │           │ (Embedded)       │        │
│  └─────────────────┘           └──────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack Details

### Frontend Stack
- **React 18**: Component-based UI library
- **Vite**: Fast build tool and dev server
- **Material-UI v5**: Comprehensive component library
- **React Router v6**: Client-side routing
- **Axios**: HTTP client for API calls
- **Emotion**: CSS-in-JS for styling

### Backend Stack
- **FastAPI**: Modern Python web framework
- **Motor**: Async MongoDB driver
- **Pydantic**: Data validation using Python type hints
- **Uvicorn**: ASGI server
- **Google Generative AI**: Gemini API integration

### Database
- **MongoDB 7.0**: Document-based NoSQL database
- **Collections**:
  - `tickets`: Main ticket data
  - Activities embedded within tickets

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## Data Models

### Ticket Model
```python
{
    "_id": ObjectId,
    "title": str,
    "description": str,
    "category": str,
    "status": str,  # "open", "in-progress", "resolved", "closed"
    "priority": str | None,  # "P0", "P1", "P2", "P3"
    "assignee": str | None,
    "ai_rationale": str | None,
    "ai_reply_draft": str | None,
    "ai_confidence": float | None,
    "created_at": datetime,
    "updated_at": datetime,
    "activities": [Activity]
}
```

### Activity Model (Embedded)
```python
{
    "timestamp": datetime,
    "action": str,  # "created", "updated", "triaged", "triage_failed"
    "details": str,
    "user": str
}
```

## API Architecture

### Layered Architecture

```
Routes Layer (tickets.py)
    ↓
Services Layer (ai_triage.py)
    ↓
Database Layer (database.py)
    ↓
Models/Schemas (models.py, schemas.py)
```

### Endpoints

#### Ticket Operations
- `POST /tickets` - Create new ticket
- `GET /tickets` - List all tickets
- `GET /tickets/{id}` - Get single ticket
- `PUT /tickets/{id}` - Update ticket
- `DELETE /tickets/{id}` - Delete ticket

#### AI Operations
- `POST /tickets/{id}/triage` - Trigger AI triage

### Request/Response Flow

1. **Client Request** → Frontend sends HTTP request
2. **API Gateway** → FastAPI receives and validates request
3. **Business Logic** → Routes execute business logic
4. **AI Processing** → Gemini API analyzes ticket (if triage)
5. **Data Persistence** → MongoDB saves/retrieves data
6. **Response** → JSON response sent to client

## AI Triage Architecture

### Triage Flow

```
Ticket Input → AI Service → Gemini API → Parse Response → Update Ticket
     ↓              ↓            ↓             ↓              ↓
  Title,       Prompt      API Call     Extract        Save to DB
  Desc,        Building                   JSON
  Category
```

### Prompt Engineering

The system uses structured prompts to get consistent JSON responses:

1. **Input Context**: Title, description, category
2. **Output Format**: Defined JSON schema
3. **Guidelines**: Priority rules, assignee mapping
4. **Constraints**: Reply length, tone requirements

### Fallback Mechanism

```
Try Gemini API
    ↓
  Success? ─── Yes ──→ Return AI result
    ↓
   No
    ↓
Use Mock Logic ──→ Return mock result based on keywords
    ↓
Log error for monitoring
```

## Database Design

### Why MongoDB?
- **Flexible Schema**: Easy to add new fields
- **Embedded Documents**: Activities stored with tickets
- **JSON-like Documents**: Natural fit for REST API
- **Scalability**: Horizontal scaling support
- **Async Support**: Motor driver for async operations

### Collections

#### Tickets Collection
- **Indexes**: `_id` (primary), `created_at`, `status`, `priority`
- **Size**: Variable based on description length
- **Relationships**: None (embedded activities)

### Data Access Patterns

1. **List Tickets**: Query all, sort by created_at
2. **Get Ticket**: Find by _id
3. **Create Ticket**: Insert document with default values
4. **Update Ticket**: Update specific fields, push activity
5. **Delete Ticket**: Remove document

## Frontend Architecture

### Component Hierarchy

```
App.jsx
├── Navigation.jsx
├── TicketList.jsx
│   └── TicketCard.jsx (multiple)
├── TicketDetail.jsx
│   ├── TriageResultCard.jsx
│   └── ActivityLog.jsx
└── CreateTicket.jsx
    └── TicketForm.jsx
```

### State Management

- **Local State**: useState for component-specific state
- **API State**: Fetched data stored in component state
- **Loading States**: Boolean flags for async operations
- **Error States**: Error messages for user feedback

### Routing

```
/ → TicketList
/tickets/:id → TicketDetail
/create → CreateTicket
```

## Security Considerations

### Current Implementation
- CORS configured for localhost
- Input validation with Pydantic
- MongoDB ObjectId validation
- Error messages sanitized

### Production Recommendations
1. Add authentication (JWT tokens)
2. Rate limiting on API endpoints
3. Input sanitization for XSS prevention
4. HTTPS enforcement
5. API key rotation
6. Database access controls
7. Logging and monitoring

## Performance Optimization

### Backend
- **Async Operations**: Motor uses asyncio
- **Connection Pooling**: MongoDB connection pool
- **Lazy Loading**: Only load needed data
- **Index Usage**: Queries use indexes

### Frontend
- **Code Splitting**: Vite handles automatically
- **Lazy Loading**: React.lazy for components (future)
- **Memoization**: useMemo for expensive computations (future)
- **Debouncing**: For search/filter operations (future)

## Scalability

### Horizontal Scaling
```
Load Balancer
    ↓
Backend Instance 1 ─┐
Backend Instance 2 ─┼─→ MongoDB Cluster
Backend Instance N ─┘
```

### Vertical Scaling
- Increase container resources
- MongoDB with more RAM
- Larger Gemini API quota

## Monitoring & Logging

### What to Monitor
1. **API Response Times**: Track slow endpoints
2. **AI Triage Success Rate**: Gemini API failures
3. **Database Queries**: Slow query detection
4. **Error Rates**: 4xx and 5xx responses
5. **Resource Usage**: CPU, memory, disk

### Logging Strategy
```python
# Backend logs
logger.info(f"Ticket {ticket_id} created")
logger.warning(f"AI triage failed for {ticket_id}")
logger.error(f"Database connection error: {error}")
```

## Testing Strategy

### Unit Tests
- Models and schemas validation
- AI service mock responses
- Database operations

### Integration Tests
- API endpoints with test database
- Full triage workflow
- CRUD operations

### E2E Tests (Future)
- Browser automation with Playwright
- Full user workflows
- UI interactions

## Deployment Options

### Option 1: Docker Compose (Development/Small Scale)
- Single server deployment
- Easy setup and management
- Good for demos and testing

### Option 2: Kubernetes (Production/Large Scale)
- Container orchestration
- Auto-scaling
- High availability
- Load balancing

### Option 3: Cloud Platforms
- **Backend**: AWS Lambda, Google Cloud Run, Azure Functions
- **Frontend**: Vercel, Netlify, AWS S3 + CloudFront
- **Database**: MongoDB Atlas

## Future Enhancements

1. **Authentication & Authorization**: User roles and permissions
2. **Real-time Updates**: WebSocket for live updates
3. **Email Notifications**: SMTP integration
4. **File Attachments**: Support for images and documents
5. **Advanced Analytics**: Dashboard with charts
6. **SLA Tracking**: Automatic SLA violation alerts
7. **Multi-tenancy**: Support for multiple organizations
8. **Workflow Automation**: Custom workflow rules
9. **Integration APIs**: Slack, Email, etc.
10. **Mobile App**: React Native or Flutter

## Development Workflow

```
1. Make changes locally
2. Test with docker-compose
3. Run pytest tests
4. Commit to git
5. Push to repository
6. CI/CD pipeline (future)
7. Deploy to staging
8. Deploy to production
```
