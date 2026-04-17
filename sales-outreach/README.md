# XanderCorp Sales Outreach System

> **Autonomous outbound sales engine. Find leads, send offers, close deals.**

---

## Overview

Complete cold outreach system with:
- Lead research and database
- Email templates (branded)
- Outreach tracking
- Timing optimization
- Follow-up sequences

---

## Quick Start

### 1. Setup Gmail
```bash
# Follow setup guide
bash scripts/setup_gmail.sh

# Save app password
echo 'GMAIL_APP_PASSWORD=your_16_char_password' > /root/xandercorp/.env
chmod 600 /root/xandercorp/.env

# Test email
python3 scripts/email_sender.py test
```

### 2. Check System
```bash
# View leads dashboard
python3 scripts/lead_finder.py dashboard

# Check outreach status
python3 scripts/optimized_outreach.py

# View stats
python3 scripts/sales_agent.py stats
```

### 3. Add Leads
```bash
python3 scripts/lead_finder.py add "John Doe" "Acme Corp" "john@acme.com" "saas_startup" "https://acme.com"
```

### 4. Send Outreach
```python
from email_sender import send_email
from optimized_outreach import format_email

# Get next lead
from lead_finder import get_next_outreach
lead = get_next_outreach()

# Format email
subject, body = format_email("cold_intro",
    name=lead["name"],
    company=lead["company"],
    observation=lead["observation"],
    pain_point=lead["pain_point"]
)

# Send
send_email(lead["email"], subject, body)
```

---

## Scripts

| Script | Purpose |
|--------|---------|
| `lead_finder.py` | Find, add, manage leads |
| `lead_research.py` | Research target industries |
| `email_sender.py` | Send branded emails |
| `optimized_outreach.py` | Timing & follow-up logic |
| `outreach_tracker.py` | Track all activity |
| `sales_agent.py` | Main agent, daily routine |
| `setup_gmail.sh` | Gmail setup guide |

---

## Email Templates

### Cold Intro
Subject: "Quick question about {company}"
- Short intro
- Pain point focus
- 15-min call ask

### Follow-up 1
Subject: "Re: Quick question about {company}"
- Reminder
- No pressure
- Still interested?

### Follow-up 2
Subject: "Re: AI agents for {company}"
- $150 starter offer
- 3-day delivery
- No commitment

### Final
Subject: "Did I reach the right person?"
- Exit strategy
- Stop if not relevant

---

## Best Timing (Research-Backed)

| Day | Hours | Status |
|-----|-------|--------|
| Tuesday | 9-10 AM, 3-4 PM | ✅ BEST |
| Wednesday | 9-10 AM, 3-4 PM | ✅ BEST |
| Thursday | 9-10 AM, 3-4 PM | ✅ BEST |
| Monday | Any | ⚠️ Risky |
| Friday | Any | ❌ Avoid |

---

## Daily Limits

- **Safe limit:** 15 emails/day
- **Scale up:** After 1 week, increase to 20-30
- **Goal:** 50-100/day after warm-up

---

## Lead Industries

### HIGH PRIORITY
1. SaaS Startups — customer support, onboarding
2. Ecommerce — customer service, order tracking
3. Agencies — client reporting, content creation

### MEDIUM PRIORITY
4. Real Estate — lead follow-up, scheduling
5. Recruitment — candidate sourcing, screening

---

## Tracking

All activity logged in:
- `leads/lead_database.json` — Lead status
- `emails/sent_log.json` — Emails sent
- `/root/xandercorp/logs/activity.log` — All activity

---

## Research Notes

See `/root/xandercorp/docs/RESEARCH.md` for:
- Cold email best practices
- Deliverability tips
- Competitor analysis
- Market insights

---

*Last updated: 2026-04-17*