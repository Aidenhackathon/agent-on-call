# Sample Tickets for Testing

Use these sample tickets to test the AI triage functionality and see different outputs.

## Critical Infrastructure Issue (Should get P0)

**Title:** Website is down - 503 errors

**Description:**
Our production website is completely down. Customers are getting 503 Service Unavailable errors. This is affecting all users globally. Revenue impact is significant. Please investigate immediately.

**Category:** Critical

**Expected Triage:**
- Priority: P0
- Assignee: DevOps
- Fast response time

---

## Backend Error (Should get P1)

**Title:** API returning 500 errors on checkout

**Description:**
Our payment API is intermittently returning 500 errors when customers try to checkout. About 30% of checkout attempts are failing. This is impacting sales but some transactions are still going through.

**Category:** Technical

**Expected Triage:**
- Priority: P1
- Assignee: Backend Support
- Urgent attention needed

---

## Billing Issue (Should get P2)

**Title:** Invoice shows incorrect amount

**Description:**
Our latest invoice shows $500 but we were expecting $300 based on our current plan. Can you please review our billing and correct the invoice? This needs to be resolved before the payment date.

**Category:** Billing

**Expected Triage:**
- Priority: P2
- Assignee: Finance
- Normal priority

---

## Feature Request (Should get P3)

**Title:** Add dark mode to dashboard

**Description:**
It would be great if the dashboard had a dark mode option. Many users prefer dark themes, especially when working at night. This would improve the user experience.

**Category:** Feature Request

**Expected Triage:**
- Priority: P3
- Assignee: Product
- Low priority

---

## UI Bug (Should get P2)

**Title:** Button text is cut off on mobile

**Description:**
On mobile devices (iPhone 12), the "Submit" button text is cut off and shows "Subm...". This is happening on the contact form page. The button still works but looks unprofessional.

**Category:** Bug Report

**Expected Triage:**
- Priority: P2
- Assignee: Frontend Support
- Normal priority

---

## Security Concern (Should get P0)

**Title:** Possible security vulnerability in login

**Description:**
We noticed that failed login attempts don't have rate limiting. This could allow brute force attacks on user accounts. Need immediate security review and fix.

**Category:** Critical

**Expected Triage:**
- Priority: P0
- Assignee: DevOps or Backend Support
- Immediate attention

---

## Account Question (Should get P3)

**Title:** How do I change my email address?

**Description:**
I need to update the email address associated with my account. I couldn't find this option in the settings. Can you help me with this?

**Category:** Account

**Expected Triage:**
- Priority: P3
- Assignee: Customer Support
- Standard response time

---

## Database Performance (Should get P1)

**Title:** Slow database queries affecting dashboard

**Description:**
The dashboard is taking 15-20 seconds to load. Looking at logs, it seems certain database queries are timing out. This is affecting user experience significantly but the system is still operational.

**Category:** Technical

**Expected Triage:**
- Priority: P1
- Assignee: Backend Support
- Needs investigation

---

## Testing Tips

1. **Create tickets in different orders** - AI should consistently assign priorities
2. **Use keywords** - Words like "down", "critical", "security" should trigger P0
3. **Test edge cases** - Simple tickets with minimal description
4. **Verify persistence** - Refresh after triage to ensure data is saved
5. **Edit replies** - Test the reply editing functionality
6. **Check activity logs** - Ensure all actions are recorded

## API Testing with curl

### Create a ticket
```bash
curl -X POST http://localhost:8000/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Website is down",
    "description": "Customer cannot access dashboard",
    "category": "Critical"
  }'
```

### Triage a ticket (replace {id} with actual ticket ID)
```bash
curl -X POST http://localhost:8000/tickets/{id}/triage
```

### Get all tickets
```bash
curl http://localhost:8000/tickets
```
