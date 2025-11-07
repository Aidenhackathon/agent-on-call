# 📚 Documentation Index

Welcome to Agent-on-Call! This index will help you find the information you need quickly.

## 🚀 Getting Started

**New to the project? Start here:**

1. **[README.md](README.md)** - Complete project documentation
   - Project overview and features
   - Tech stack details
   - Setup instructions
   - API endpoints
   - Configuration guide

2. **[QUICKSTART.md](QUICKSTART.md)** - Fast setup guide
   - Step-by-step setup
   - Common commands
   - Testing the application
   - Getting Gemini API key

3. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - What's been built
   - Complete feature list
   - Quick start methods
   - Test instructions
   - Project structure overview

## 🛠️ Development

**Working on the project:**

4. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical deep dive
   - System architecture
   - Data models
   - API design
   - Scalability considerations
   - Future enhancements

5. **[commands.ps1](commands.ps1)** - Convenient commands
   - Start/stop services
   - View logs
   - Run tests
   - Database management
   - Build commands

## 📖 Usage Guides

**Using the application:**

6. **[API_EXAMPLES.md](API_EXAMPLES.md)** - API usage
   - curl examples
   - PowerShell examples
   - Python examples
   - JavaScript examples
   - Response formats

7. **[SAMPLE_TICKETS.md](SAMPLE_TICKETS.md)** - Test data
   - Sample tickets for testing
   - Expected triage outputs
   - Testing tips
   - API testing examples

## 🔧 Support

**Having problems?**

8. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Problem solving
   - Common issues and solutions
   - Docker problems
   - Backend errors
   - Frontend issues
   - Database problems
   - Debugging tips

## 📁 Project Files

### Configuration Files
- **[.env.example](.env.example)** - Environment variables template
- **[docker-compose.yml](docker-compose.yml)** - Docker orchestration
- **[.gitignore](.gitignore)** - Git ignore rules

### Setup Scripts
- **[setup.ps1](setup.ps1)** - Automated setup script
- **[commands.ps1](commands.ps1)** - Convenience commands

### Backend Files
- **[backend/main.py](backend/main.py)** - FastAPI application
- **[backend/database.py](backend/database.py)** - MongoDB connection
- **[backend/models.py](backend/models.py)** - Data models
- **[backend/schemas.py](backend/schemas.py)** - Pydantic schemas
- **[backend/routes/tickets.py](backend/routes/tickets.py)** - API routes
- **[backend/services/ai_triage.py](backend/services/ai_triage.py)** - AI integration
- **[backend/tests/test_smoke.py](backend/tests/test_smoke.py)** - Tests
- **[backend/requirements.txt](backend/requirements.txt)** - Python dependencies
- **[backend/Dockerfile](backend/Dockerfile)** - Backend container

### Frontend Files
- **[frontend/src/App.jsx](frontend/src/App.jsx)** - Main app component
- **[frontend/src/api/api.js](frontend/src/api/api.js)** - API client
- **[frontend/src/pages/](frontend/src/pages/)** - Page components
- **[frontend/src/components/](frontend/src/components/)** - UI components
- **[frontend/package.json](frontend/package.json)** - Node dependencies
- **[frontend/vite.config.js](frontend/vite.config.js)** - Vite config
- **[frontend/Dockerfile](frontend/Dockerfile)** - Frontend container

## 🎯 Quick Navigation by Task

### I want to...

#### Set up the project for the first time
→ **[QUICKSTART.md](QUICKSTART.md)** or **[README.md](README.md)**

#### Run the application
```powershell
.\setup.ps1          # Automated setup
# or
.\commands.ps1 start # Start services
```

#### Create and test tickets
→ **[SAMPLE_TICKETS.md](SAMPLE_TICKETS.md)**

#### Use the API
→ **[API_EXAMPLES.md](API_EXAMPLES.md)**

#### Understand the architecture
→ **[ARCHITECTURE.md](ARCHITECTURE.md)**

#### Fix an error
→ **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

#### Customize the project
→ **[ARCHITECTURE.md](ARCHITECTURE.md)** (Customization section)

#### Deploy to production
→ **[README.md](README.md)** (Deployment section)

#### Run tests
```powershell
.\commands.ps1 test
```

#### View logs
```powershell
.\commands.ps1 logs
```

## 📊 Documentation by Role

### For Developers
1. [ARCHITECTURE.md](ARCHITECTURE.md) - Technical details
2. [backend/](backend/) - Backend code
3. [frontend/](frontend/) - Frontend code
4. [commands.ps1](commands.ps1) - Dev commands

### For Users
1. [QUICKSTART.md](QUICKSTART.md) - Getting started
2. [SAMPLE_TICKETS.md](SAMPLE_TICKETS.md) - Examples
3. Frontend UI at http://localhost:5173

### For DevOps
1. [docker-compose.yml](docker-compose.yml) - Container setup
2. [.env.example](.env.example) - Configuration
3. [README.md](README.md) - Deployment guide

### For QA/Testers
1. [SAMPLE_TICKETS.md](SAMPLE_TICKETS.md) - Test cases
2. [backend/tests/](backend/tests/) - Automated tests
3. [API_EXAMPLES.md](API_EXAMPLES.md) - API testing

## 🔗 External Resources

### Tools & Services
- **Gemini API**: https://makersuite.google.com/app/apikey
- **Docker Desktop**: https://www.docker.com/products/docker-desktop
- **MongoDB**: https://www.mongodb.com/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **Material-UI**: https://mui.com/

### API Documentation
- **Interactive API Docs**: http://localhost:8000/docs (when running)
- **Alternative API Docs**: http://localhost:8000/redoc (when running)

## 📝 Documentation Standards

### Markdown Files
- **README.md**: Main project documentation (comprehensive)
- **QUICKSTART.md**: Fast setup guide (concise)
- **ARCHITECTURE.md**: Technical deep dive (detailed)
- **TROUBLESHOOTING.md**: Problem-solution pairs (specific)
- **API_EXAMPLES.md**: Code examples (practical)
- **SAMPLE_TICKETS.md**: Test data (examples)

### Code Comments
- Backend: Python docstrings
- Frontend: JSDoc comments
- Configuration: Inline comments

## 🆘 Need Help?

### Check in order:
1. **[QUICKSTART.md](QUICKSTART.md)** - Basic setup
2. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues
3. **[README.md](README.md)** - Detailed docs
4. **Logs**: `.\commands.ps1 logs`
5. **API Docs**: http://localhost:8000/docs

### Common Commands

```powershell
# Start everything
.\setup.ps1

# View all commands
.\commands.ps1

# Check status
.\commands.ps1 status

# View logs
.\commands.ps1 logs

# Run tests
.\commands.ps1 test

# Open application
Start-Process http://localhost:5173
Start-Process http://localhost:8000/docs
```

## 📈 Learning Path

### Beginner
1. Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
2. Follow [QUICKSTART.md](QUICKSTART.md)
3. Try [SAMPLE_TICKETS.md](SAMPLE_TICKETS.md) examples
4. Explore UI at http://localhost:5173

### Intermediate
1. Study [ARCHITECTURE.md](ARCHITECTURE.md)
2. Practice with [API_EXAMPLES.md](API_EXAMPLES.md)
3. Review backend code in [backend/](backend/)
4. Modify frontend components in [frontend/src/](frontend/src/)

### Advanced
1. Customize AI triage logic
2. Add new features
3. Optimize performance
4. Deploy to production
5. Contribute improvements

## 🗺️ File Map

```
agent-on-call/
│
├── 📘 Documentation (You are here!)
│   ├── README.md              # Start here
│   ├── QUICKSTART.md          # Fast setup
│   ├── PROJECT_SUMMARY.md     # Overview
│   ├── ARCHITECTURE.md        # Technical details
│   ├── API_EXAMPLES.md        # API usage
│   ├── SAMPLE_TICKETS.md      # Test data
│   ├── TROUBLESHOOTING.md     # Problem solving
│   └── INDEX.md               # This file
│
├── 🔧 Configuration
│   ├── .env.example           # Environment template
│   ├── .gitignore            # Git ignore rules
│   └── docker-compose.yml     # Docker config
│
├── 📜 Scripts
│   ├── setup.ps1             # Setup script
│   └── commands.ps1           # Convenience commands
│
├── 🔙 Backend (FastAPI + MongoDB + Gemini)
│   └── [See backend README]
│
└── 🎨 Frontend (React + Vite + Material-UI)
    └── [See frontend structure]
```

## 🎯 Success Checklist

- [ ] Read [README.md](README.md)
- [ ] Complete [QUICKSTART.md](QUICKSTART.md) setup
- [ ] Application running at http://localhost:5173
- [ ] Created first test ticket
- [ ] Ran AI triage successfully
- [ ] Reviewed [API_EXAMPLES.md](API_EXAMPLES.md)
- [ ] Checked [ARCHITECTURE.md](ARCHITECTURE.md)
- [ ] Ran tests successfully
- [ ] Customized something!

## 📞 Quick Reference

| Need | Go To |
|------|-------|
| Setup | [QUICKSTART.md](QUICKSTART.md) |
| API Usage | [API_EXAMPLES.md](API_EXAMPLES.md) |
| Problems | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| Architecture | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Test Data | [SAMPLE_TICKETS.md](SAMPLE_TICKETS.md) |
| Commands | [commands.ps1](commands.ps1) |
| Complete Docs | [README.md](README.md) |

---

**Happy coding! 🚀**

*Last updated: 2025-10-28*
