# 🚀 Getting Started - Visual Guide

## Step-by-Step Setup

### Prerequisites ✅

Before you begin, ensure you have:
- [ ] Windows PC with PowerShell
- [ ] Docker Desktop installed and running
- [ ] Internet connection (for Gemini API)
- [ ] Text editor (VS Code recommended)

---

## 🎯 Setup Process

### Step 1: Open PowerShell in Project Directory

```
📁 File Explorer
    └── Navigate to: c:\Users\lohit\agent-on-call
        └── Right-click → "Open in Terminal" or "Open PowerShell here"
```

### Step 2: Run Setup Script

```powershell
.\setup.ps1
```

**What happens:**
```
🚀 Agent-on-Call Setup Script
================================

✅ Docker is installed
✅ Docker Compose is available
✅ Created .env file from template

⚠️  IMPORTANT: Please edit .env and add your Gemini API key!

Do you want to enter your Gemini API key now? (y/n): _
```

### Step 3: Get Gemini API Key

```
🌐 Browser
    └── Open: https://makersuite.google.com/app/apikey
        └── Sign in with Google
            └── Click "Create API Key"
                └── Copy the key
```

### Step 4: Enter API Key

```powershell
# Either:
# 1. Enter during setup when prompted
Enter your Gemini API key: [paste key here]

# OR
# 2. Edit .env file manually
notepad .env
# Change: GEMINI_API_KEY=your_gemini_api_key_here
# To:     GEMINI_API_KEY=AIzaSy...your_actual_key
```

### Step 5: Wait for Startup

```
Starting Docker containers...

[+] Running 3/3
 ✔ Container agent-on-call-mongodb   Started
 ✔ Container agent-on-call-backend   Started  
 ✔ Container agent-on-call-frontend  Started

✅ Setup complete!

🌐 Access your application:
   Frontend:  http://localhost:5173
   Backend:   http://localhost:8000
   API Docs:  http://localhost:8000/docs
```

---

## 🖥️ Using the Application

### View 1: Ticket List (Home Page)

```
┌─────────────────────────────────────────────────────────┐
│  🎫 Agent-on-Call         [Tickets]  [➕ New Ticket]   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Helpdesk Tickets                          [🔄 Refresh] │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ 🔴 P0        │  │ 🟡 P2        │  │ 🟢 P3        │ │
│  │ Website Down │  │ Billing Issue│  │ Feature Req  │ │
│  │              │  │              │  │              │ │
│  │ Critical     │  │ Billing      │  │ Feature      │ │
│  │ DevOps       │  │ Finance      │  │ Product      │ │
│  │              │  │              │  │              │ │
│  │ [View Details│  │ [View Details│  │ [View Details│ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### View 2: Create Ticket Page

```
┌─────────────────────────────────────────────────────────┐
│  🎫 Agent-on-Call         [Tickets]  [➕ New Ticket]   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Create New Ticket                                       │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Title *                                            │ │
│  │ ┌────────────────────────────────────────────────┐ │ │
│  │ │ Website is down                                │ │ │
│  │ └────────────────────────────────────────────────┘ │ │
│  │                                                    │ │
│  │ Description *                                      │ │
│  │ ┌────────────────────────────────────────────────┐ │ │
│  │ │ Customer cannot access dashboard               │ │ │
│  │ │                                                │ │ │
│  │ │                                                │ │ │
│  │ └────────────────────────────────────────────────┘ │ │
│  │                                                    │ │
│  │ Category *                                         │ │
│  │ ┌────────────────────────────────────────────────┐ │ │
│  │ │ Critical                          ▼            │ │ │
│  │ └────────────────────────────────────────────────┘ │ │
│  │                                                    │ │
│  │ [Create Ticket]  [Cancel]                         │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### View 3: Ticket Detail with AI Triage

```
┌─────────────────────────────────────────────────────────┐
│  🎫 Agent-on-Call         [Tickets]  [➕ New Ticket]   │
├─────────────────────────────────────────────────────────┤
│  [← Back to Tickets]                                     │
│                                                          │
│  Website is down                              [Delete]   │
│  [open] [Critical]                                       │
│                                                          │
│  Description                                             │
│  Customer cannot access dashboard                        │
│                                                          │
│  Created: 10/28/2025, 10:30 AM                          │
│  Updated: 10/28/2025, 10:31 AM                          │
│                                                          │
│  [🤖 Auto-Triage with AI]                               │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ ✅ AI Triage Results                               │ │
│  │                                                    │ │
│  │ ⚡ Priority: [P0] Confidence: 92%                 │ │
│  │ 👤 Suggested Assignee: [DevOps]                   │ │
│  │                                                    │ │
│  │ Rationale:                                         │ │
│  │ Critical infrastructure issue affecting customer   │ │
│  │ access. Requires immediate DevOps attention.       │ │
│  │                                                    │ │
│  │ Suggested First Reply:                             │ │
│  │ ┌────────────────────────────────────────────────┐ │ │
│  │ │ Hello,                                         │ │ │
│  │ │                                                │ │ │
│  │ │ Thank you for reporting this critical issue.  │ │ │
│  │ │ We understand the urgency and have            │ │ │
│  │ │ immediately escalated this to our DevOps      │ │ │
│  │ │ team...                                        │ │ │
│  │ └────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  Reply Draft                           [Edit] [Save]     │
│  [Shows the AI-generated reply, editable]                │
│                                                          │
│  Activity Log                                            │
│  ○ 10:31 AM - triaged - AI triage completed              │
│  ○ 10:30 AM - created - Ticket created                   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🎮 Common Actions

### Action 1: Create a Ticket

```
1. Click "New Ticket" button
2. Fill in:
   - Title: "Website is down"
   - Description: "Customer cannot access dashboard"
   - Category: "Critical"
3. Click "Create Ticket"
4. You're redirected to ticket details
```

### Action 2: Run AI Triage

```
1. Open any ticket
2. Click "Auto-Triage with AI" button
3. Wait 2-5 seconds (loading spinner shows)
4. View results:
   ✓ Priority assigned
   ✓ Assignee suggested
   ✓ Reply draft generated
   ✓ Confidence score shown
```

### Action 3: Edit Reply Draft

```
1. Scroll to "Reply Draft" section
2. Click "Edit" button
3. Modify the text
4. Click "Save"
5. Changes persist after refresh
```

### Action 4: View All Tickets

```
1. Click "Tickets" in navigation
2. See all tickets in card view
3. Click any card to view details
4. Click "Refresh" to reload list
```

---

## 🔧 Useful Commands

### Start/Stop Services

```powershell
# Start everything
.\commands.ps1 start

# Stop everything
.\commands.ps1 stop

# Restart everything
.\commands.ps1 restart
```

### View Logs

```powershell
# All logs
.\commands.ps1 logs

# Backend logs only
.\commands.ps1 logs-backend

# Frontend logs only
.\commands.ps1 logs-frontend
```

### Testing

```powershell
# Run all tests
.\commands.ps1 test

# Run with coverage
.\commands.ps1 test-coverage
```

### Maintenance

```powershell
# Check status
.\commands.ps1 status

# Rebuild containers
.\commands.ps1 build

# Clean up
.\commands.ps1 clean

# Deep clean (removes all data)
.\commands.ps1 clean-all
```

---

## 📱 Access Points

### Frontend (User Interface)
```
🌐 http://localhost:5173

Beautiful Material-UI interface
Create, view, and manage tickets
Run AI triage
Edit reply drafts
```

### Backend API
```
🔗 http://localhost:8000

REST API endpoints
JSON responses
CORS enabled
```

### API Documentation
```
📚 http://localhost:8000/docs

Interactive Swagger UI
Try API calls in browser
See request/response schemas
Auto-generated documentation
```

---

## 🎯 Example Workflow

```
┌─────────────────────────────────────────────────────────┐
│                    User Workflow                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. User creates ticket                                  │
│     "Website is down" → Submit                           │
│                                                          │
│  2. Click "Auto-Triage"                                  │
│     🤖 AI analyzes ticket...                            │
│                                                          │
│  3. AI returns results                                   │
│     ✓ Priority: P0                                       │
│     ✓ Assignee: DevOps                                   │
│     ✓ Reply: Professional response                       │
│     ✓ Confidence: 92%                                    │
│                                                          │
│  4. User reviews and edits reply                         │
│     [Edit] → Customize → [Save]                          │
│                                                          │
│  5. All data persists                                    │
│     Refresh page → Data still there ✓                    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🆘 Quick Troubleshooting

### Issue: Can't access frontend
```
✓ Check Docker is running: docker ps
✓ Check URL: http://localhost:5173
✓ View logs: .\commands.ps1 logs-frontend
```

### Issue: AI triage fails
```
✓ Check API key in .env
✓ Enable mock mode: USE_MOCK_AI=true
✓ View logs: .\commands.ps1 logs-backend
```

### Issue: Port already in use
```
✓ Find process: netstat -ano | findstr :5173
✓ Kill process: taskkill /PID <PID> /F
✓ Or restart Docker
```

### Issue: Database connection error
```
✓ Check MongoDB: docker ps | findstr mongodb
✓ Restart: .\commands.ps1 restart
✓ View logs: .\commands.ps1 logs
```

---

## 📚 Learn More

- **[README.md](README.md)** - Complete documentation
- **[API_EXAMPLES.md](API_EXAMPLES.md)** - API usage
- **[SAMPLE_TICKETS.md](SAMPLE_TICKETS.md)** - Test data
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Detailed help

---

## ✅ Success Checklist

- [ ] Docker is running
- [ ] Setup script completed
- [ ] .env file has Gemini API key
- [ ] Frontend opens at localhost:5173
- [ ] Backend API responds at localhost:8000
- [ ] Created first test ticket
- [ ] Ran AI triage successfully
- [ ] Data persists after refresh
- [ ] Tests pass

---

**🎉 You're all set! Enjoy your AI-powered ticket triage system!**

Need help? Check **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** or run `.\commands.ps1` for available commands.
