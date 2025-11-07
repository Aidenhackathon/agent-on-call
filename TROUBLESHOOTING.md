# Troubleshooting Guide

## Common Issues and Solutions

### 🔴 Docker Issues

#### Issue: "docker-compose: command not found"
**Solution:**
```powershell
# Check if Docker Desktop is installed
docker --version

# If Docker is installed but docker-compose isn't recognized, try:
docker compose up --build  # Note: no hyphen, this is Docker Compose V2
```

#### Issue: Port already in use (8000, 5173, or 27017)
**Solution:**
```powershell
# Find process using the port (example for port 8000)
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
# For backend: "8001:8000" (maps host port 8001 to container port 8000)
```

#### Issue: Container keeps restarting
**Solution:**
```powershell
# Check logs for errors
docker-compose logs backend
docker-compose logs frontend

# Check container status
docker-compose ps

# Restart with fresh build
docker-compose down -v
docker-compose up --build
```

---

### 🔴 Backend Issues

#### Issue: "ModuleNotFoundError: No module named 'fastapi'"
**Solution:**
```powershell
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt
```

#### Issue: "motor.motor_asyncio connection timeout"
**Solution:**
```powershell
# Ensure MongoDB is running
docker ps | findstr mongodb

# Start MongoDB if not running
docker-compose up mongodb -d

# Check MongoDB logs
docker-compose logs mongodb

# Verify connection string in .env
# Should be: MONGODB_URL=mongodb://mongodb:27017
```

#### Issue: "Invalid GEMINI_API_KEY"
**Solution:**
1. Get a valid API key from https://makersuite.google.com/app/apikey
2. Update `.env` file:
   ```
   GEMINI_API_KEY=your_actual_key_here
   USE_MOCK_AI=false
   ```
3. Restart containers:
   ```powershell
   docker-compose restart backend
   ```

#### Issue: "AI triage failed, please try again"
**Solution:**
```powershell
# Option 1: Enable mock AI for testing
# Edit .env:
USE_MOCK_AI=true

# Option 2: Check Gemini API quota
# Visit: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com

# Option 3: Check backend logs
docker-compose logs backend | Select-String -Pattern "error"
```

#### Issue: CORS errors in browser console
**Solution:**
Edit `backend/main.py` and add your frontend URL:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://frontend:5173",
        "http://localhost:3000"  # Add your URL here
    ],
    # ...
)
```

---

### 🔴 Frontend Issues

#### Issue: "Failed to load tickets. Please try again."
**Solution:**
```powershell
# Check if backend is running
curl http://localhost:8000/

# Check frontend environment
# Edit frontend/.env:
VITE_API_URL=http://localhost:8000

# Restart frontend
docker-compose restart frontend
```

#### Issue: npm/node errors
**Solution:**
```powershell
cd frontend

# Clean install
Remove-Item node_modules -Recurse -Force
Remove-Item package-lock.json
npm install

# Or use fresh Docker build
docker-compose build --no-cache frontend
```

#### Issue: "Cannot find module" errors
**Solution:**
```powershell
cd frontend

# Install missing dependencies
npm install

# If using Docker, rebuild
docker-compose build frontend
docker-compose up frontend
```

#### Issue: White screen / blank page
**Solution:**
1. Check browser console for errors (F12)
2. Verify backend is running: http://localhost:8000
3. Check frontend logs:
   ```powershell
   docker-compose logs frontend
   ```
4. Try hard refresh: Ctrl + Shift + R

---

### 🔴 Database Issues

#### Issue: "Database connection refused"
**Solution:**
```powershell
# Check MongoDB is running
docker-compose ps mongodb

# Start MongoDB
docker-compose up mongodb -d

# Check MongoDB logs
docker-compose logs mongodb

# Test connection
docker exec -it agent-on-call-mongodb mongosh
```

#### Issue: Data not persisting after restart
**Solution:**
```powershell
# Check Docker volumes
docker volume ls | findstr agent

# Verify volume is mounted in docker-compose.yml:
# volumes:
#   - mongodb_data:/data/db

# If data is lost, may need to recreate volume
docker-compose down
docker volume rm agent-on-call_mongodb_data
docker-compose up -d
```

#### Issue: "Invalid ObjectId format"
**Solution:**
This means you're using an invalid ticket ID. MongoDB IDs are 24-character hex strings.
- ✅ Valid: `671a2b3c4d5e6f7890abcdef`
- ❌ Invalid: `123`, `test`, `invalid-id`

Copy the ID from the browser URL or API response.

---

### 🔴 API Issues

#### Issue: 404 Not Found on API calls
**Solution:**
```powershell
# Verify endpoint exists
curl http://localhost:8000/docs

# Check correct URL format:
# ✅ http://localhost:8000/tickets
# ❌ http://localhost:8000/api/tickets
```

#### Issue: 422 Unprocessable Entity
**Solution:**
Check request body matches schema. Example:
```json
{
  "title": "Required field",
  "description": "Required field",
  "category": "Required field"
}
```

#### Issue: 500 Internal Server Error
**Solution:**
```powershell
# Check backend logs for details
docker-compose logs backend | Select-String -Pattern "ERROR"

# Common causes:
# - Database connection lost
# - AI API error
# - Invalid data format
```

---

### 🔴 Testing Issues

#### Issue: pytest not found
**Solution:**
```powershell
cd backend
.\venv\Scripts\activate
pip install pytest pytest-asyncio httpx
```

#### Issue: Tests failing with connection errors
**Solution:**
```powershell
# Ensure services are running
docker-compose up -d

# Wait for services to be ready
Start-Sleep -Seconds 10

# Run tests
docker-compose exec backend pytest tests/ -v
```

---

### 🔴 Environment Issues

#### Issue: .env file not loaded
**Solution:**
```powershell
# Ensure .env file exists in project root
Test-Path .env

# If not, create from example
Copy-Item .env.example .env

# Restart containers to load new env vars
docker-compose down
docker-compose up -d
```

#### Issue: Changes not reflecting
**Solution:**
```powershell
# For backend changes
docker-compose restart backend

# For frontend changes (sometimes needs rebuild)
docker-compose build frontend
docker-compose up frontend

# For .env changes
docker-compose down
docker-compose up -d
```

---

### 🔴 Performance Issues

#### Issue: Slow triage (>10 seconds)
**Solution:**
1. Check internet connection (Gemini API is cloud-based)
2. Try mock mode:
   ```
   USE_MOCK_AI=true
   ```
3. Check Gemini API status
4. Verify no rate limiting

#### Issue: Slow page loads
**Solution:**
```powershell
# Check container resources
docker stats

# If memory is maxed, increase Docker memory:
# Docker Desktop → Settings → Resources → Memory
```

---

### 🔴 Windows-Specific Issues

#### Issue: Line ending problems (CRLF vs LF)
**Solution:**
```powershell
# Configure Git to not auto-convert line endings
git config --global core.autocrlf false

# Or use .gitattributes file (already included in project)
```

#### Issue: Permission denied on scripts
**Solution:**
```powershell
# Run PowerShell as Administrator
# Or enable script execution:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### 🔴 Production Issues

#### Issue: Preparing for production deployment
**Solution:**
1. **Never commit .env with real API keys**
2. **Use environment-specific configs**
3. **Enable HTTPS**
4. **Add authentication**
5. **Set up monitoring**
6. **Use managed MongoDB (Atlas)**
7. **Rate limiting**
8. **Input validation**
9. **Logging**
10. **Backup strategy**

---

## Debugging Tips

### View All Logs
```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb

# Last 100 lines
docker-compose logs --tail=100
```

### Check Service Health
```powershell
# Container status
docker-compose ps

# Resource usage
docker stats

# Network connectivity
docker-compose exec backend ping mongodb
```

### Access Container Shell
```powershell
# Backend
docker-compose exec backend /bin/sh

# Frontend
docker-compose exec frontend /bin/sh

# MongoDB
docker-compose exec mongodb mongosh
```

### Test API Manually
```powershell
# Test backend health
curl http://localhost:8000/

# Test API docs
Start-Process http://localhost:8000/docs

# Create test ticket
$body = @{title="Test";description="Test";category="Test"} | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:8000/tickets -Method POST -Body $body -ContentType "application/json"
```

---

## Getting Help

### Check Documentation
1. **README.md** - Main documentation
2. **QUICKSTART.md** - Setup guide
3. **API_EXAMPLES.md** - API usage
4. **ARCHITECTURE.md** - Technical details

### Enable Debug Mode

**Backend:**
```python
# Edit backend/main.py
app = FastAPI(debug=True)
```

**Frontend:**
```javascript
// Check browser console (F12)
// Look for error messages and network requests
```

### Common Log Patterns

**Success patterns:**
```
✅ "Connected to MongoDB"
✅ "Application startup complete"
✅ "Uvicorn running on"
```

**Error patterns:**
```
❌ "Connection refused"
❌ "ModuleNotFoundError"
❌ "CORS policy"
❌ "Invalid API key"
```

---

## Reset Everything

If all else fails:

```powershell
# Stop all containers
docker-compose down -v

# Remove all images
docker-compose down --rmi all

# Clean Docker system
docker system prune -a

# Rebuild from scratch
docker-compose up --build
```

---

## Still Having Issues?

1. Check all logs: `docker-compose logs`
2. Verify .env file is configured
3. Ensure Docker Desktop is running
4. Check port availability
5. Restart Docker Desktop
6. Reboot computer (seriously, sometimes this helps!)

---

**Remember:** Most issues are related to:
- Missing .env configuration
- Docker not running
- Ports already in use
- Missing dependencies
- Network connectivity

Check these first! 🔍
