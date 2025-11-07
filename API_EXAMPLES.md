# API Examples

## Using curl

### 1. Create a new ticket
```bash
curl -X POST http://localhost:8000/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Login page not loading",
    "description": "Users are reporting that the login page shows a blank screen",
    "category": "Technical"
  }'
```

### 2. Get all tickets
```bash
curl http://localhost:8000/tickets
```

### 3. Get specific ticket
```bash
curl http://localhost:8000/tickets/{ticket_id}
```

### 4. Trigger AI triage
```bash
curl -X POST http://localhost:8000/tickets/{ticket_id}/triage
```

### 5. Update ticket
```bash
curl -X PUT http://localhost:8000/tickets/{ticket_id} \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in-progress",
    "ai_reply_draft": "Updated reply text"
  }'
```

### 6. Delete ticket
```bash
curl -X DELETE http://localhost:8000/tickets/{ticket_id}
```

## Using PowerShell

### Create a ticket
```powershell
$body = @{
    title = "Website is down"
    description = "Customer cannot access dashboard"
    category = "Critical"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/tickets" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### Get all tickets
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/tickets"
```

### Triage a ticket
```powershell
$ticketId = "your_ticket_id_here"
Invoke-RestMethod -Uri "http://localhost:8000/tickets/$ticketId/triage" `
    -Method POST
```

## Using Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000"

# Create ticket
ticket_data = {
    "title": "Website is down",
    "description": "Customer cannot access dashboard",
    "category": "Critical"
}
response = requests.post(f"{BASE_URL}/tickets", json=ticket_data)
ticket = response.json()
print(f"Created ticket: {ticket['id']}")

# Triage ticket
triage_response = requests.post(f"{BASE_URL}/tickets/{ticket['id']}/triage")
triage = triage_response.json()
print(f"Priority: {triage['priority']}")
print(f"Assignee: {triage['assignee']}")

# Get ticket details
ticket_response = requests.get(f"{BASE_URL}/tickets/{ticket['id']}")
updated_ticket = ticket_response.json()
print(f"Ticket status: {updated_ticket['status']}")
```

## Using JavaScript (fetch)

```javascript
const BASE_URL = 'http://localhost:8000';

// Create ticket
async function createTicket() {
  const response = await fetch(`${BASE_URL}/tickets`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      title: 'Website is down',
      description: 'Customer cannot access dashboard',
      category: 'Critical'
    })
  });
  return response.json();
}

// Triage ticket
async function triageTicket(ticketId) {
  const response = await fetch(`${BASE_URL}/tickets/${ticketId}/triage`, {
    method: 'POST'
  });
  return response.json();
}

// Usage
(async () => {
  const ticket = await createTicket();
  console.log('Created:', ticket.id);
  
  const triage = await triageTicket(ticket.id);
  console.log('Priority:', triage.priority);
  console.log('Assignee:', triage.assignee);
})();
```

## Response Examples

### Create Ticket Response
```json
{
  "id": "671a2b3c4d5e6f7890abcdef",
  "title": "Website is down",
  "description": "Customer cannot access dashboard",
  "category": "Critical",
  "status": "open",
  "priority": null,
  "assignee": null,
  "ai_rationale": null,
  "ai_reply_draft": null,
  "ai_confidence": null,
  "created_at": "2025-10-28T10:30:00.000Z",
  "updated_at": "2025-10-28T10:30:00.000Z",
  "activities": [
    {
      "timestamp": "2025-10-28T10:30:00.000Z",
      "action": "created",
      "details": "Ticket created",
      "user": "system"
    }
  ]
}
```

### Triage Response
```json
{
  "priority": "P0",
  "confidence": 0.92,
  "assignee": "DevOps",
  "rationale": "Critical infrastructure issue affecting customer access. Requires immediate DevOps attention.",
  "reply_draft": "Hello,\n\nThank you for reporting this critical issue. We understand the urgency and have immediately escalated this to our DevOps team. They are actively investigating and working on a resolution. We will provide updates every 30 minutes until this is resolved. We apologize for any inconvenience caused.\n\nBest regards,\nSupport Team"
}
```

### Get Ticket After Triage
```json
{
  "id": "671a2b3c4d5e6f7890abcdef",
  "title": "Website is down",
  "description": "Customer cannot access dashboard",
  "category": "Critical",
  "status": "open",
  "priority": "P0",
  "assignee": "DevOps",
  "ai_rationale": "Critical infrastructure issue affecting customer access. Requires immediate DevOps attention.",
  "ai_reply_draft": "Hello,\n\nThank you for reporting...",
  "ai_confidence": 0.92,
  "created_at": "2025-10-28T10:30:00.000Z",
  "updated_at": "2025-10-28T10:31:00.000Z",
  "activities": [
    {
      "timestamp": "2025-10-28T10:30:00.000Z",
      "action": "created",
      "details": "Ticket created",
      "user": "system"
    },
    {
      "timestamp": "2025-10-28T10:31:00.000Z",
      "action": "triaged",
      "details": "AI triage completed - Priority: P0, Assignee: DevOps",
      "user": "ai-system"
    }
  ]
}
```
