# Quick Start Guide

## First Time Setup

### 1. Prerequisites
- Docker Desktop installed and running
- Git (optional)

### 2. Setup
```powershell
# Run the setup script
.\setup.ps1
```

The script will:
- Check Docker installation
- Create .env file
- Prompt for Gemini API key
- Start all containers

### 3. Access the Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Common Commands

### Start the application
```powershell
docker-compose up -d
```

### Stop the application
```powershell
docker-compose down
```

### View logs
```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Rebuild after changes
```powershell
docker-compose up --build
```

### Run tests
```powershell
docker-compose exec backend pytest tests/test_smoke.py -v
```

## Local Development (without Docker)

### Backend
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```powershell
cd frontend
npm install
npm run dev
```

### MongoDB
```powershell
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

## Troubleshooting

### Port already in use
```powershell
# Windows - Find and kill process on port
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Reset everything
```powershell
docker-compose down -v
docker-compose up --build
```

### Check container status
```powershell
docker-compose ps
```

## Getting Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key
5. Add to `.env` file:
   ```
   GEMINI_API_KEY=your_key_here
   USE_MOCK_AI=false
   ```

## Testing the Application

### Create a test ticket
1. Open http://localhost:5173
2. Click "New Ticket"
3. Fill in:
   - Title: "Website is down"
   - Description: "Customer cannot access dashboard"
   - Category: "Critical"
4. Click "Create Ticket"

### Test AI Triage
1. Click "View Details" on the ticket
2. Click "Auto-Triage with AI"
3. Wait 2-5 seconds
4. View AI results:
   - Priority (P0-P3)
   - Confidence score
   - Suggested assignee
   - Reply draft

### Verify Persistence
1. Refresh the page
2. All triage data should still be visible

## Next Steps

- Explore the API docs at http://localhost:8000/docs
- Try different ticket types (billing, technical, feature request)
- Edit and save reply drafts
- View activity logs
- Test CRUD operations
