#!/usr/bin/env python3
"""
XanderCorp Optimized Outreach System
Based on 2025 cold email research
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
SENT_DIR = "/root/gsd/xandercorp/sales-outreach/emails"
os.makedirs(SENT_DIR, exist_ok=True)

DAILY_LIMIT = 15  # Start small, scale up
COOLDOWN_HOURS = 72  # 3 days between follow-ups

# Best timing (based on research)
BEST_DAYS = [1, 2, 3]  # Tuesday, Wednesday, Thursday (0=Mon)
BEST_HOURS = [9, 10, 15, 16]  # 9-10 AM or 3-4 PM

def is_optimal_time():
    """Check if current time is optimal for sending"""
    now = datetime.now()
    
    # Check day
    if now.weekday() not in BEST_DAYS:
        return False, f"Not optimal day. Best: Tue-Thu. Current: {now.strftime('%A')}"
    
    # Check hour
    if now.hour not in BEST_HOURS:
        return False, f"Not optimal hour. Best: 9-10 AM or 3-4 PM. Current: {now.hour}:00"
    
    return True, "Optimal time for outreach"

def get_lead_status(lead_email):
    """Get lead's outreach status"""
    log_file = f"{SENT_DIR}/sent_log.json"
    
    if not os.path.exists(log_file):
        return {"sent": False, "followups": 0}
    
    with open(log_file, "r") as f:
        logs = json.load(f)
    
    lead_emails = [l for l in logs if l.get("to") == lead_email]
    
    if not lead_emails:
        return {"sent": False, "followups": 0}
    
    last_sent = max(lead_emails, key=lambda x: x["timestamp"])
    followups = len([l for l in lead_emails if "follow-up" in l.get("subject", "").lower()])
    
    # Check if ready for follow-up
    last_time = datetime.fromisoformat(last_sent["timestamp"])
    hours_since = (datetime.now() - last_time).total_seconds() / 3600
    
    return {
        "sent": True,
        "followups": followups,
        "last_sent": last_sent["timestamp"],
        "hours_since": hours_since,
        "ready_for_followup": hours_since >= COOLDOWN_HOURS and followups < 3
    }

def get_daily_count():
    """Get today's sent count"""
    log_file = f"{SENT_DIR}/sent_log.json"
    
    if not os.path.exists(log_file):
        return 0
    
    with open(log_file, "r") as f:
        logs = json.load(f)
    
    today = datetime.now().date().isoformat()
    return len([l for l in logs if l["timestamp"].startswith(today)])

def can_send():
    """Check if we can send today"""
    count = get_daily_count()
    
    if count >= DAILY_LIMIT:
        return False, f"Daily limit reached ({count}/{DAILY_LIMIT})"
    
    optimal, msg = is_optimal_time()
    return True, f"Can send. {count}/{DAILY_LIMIT} today. {msg}"

# Optimized email templates (short, focused, 50-100 words)

TEMPLATES = {
    "cold_intro": {
        "subject": "Quick question about {company}",
        "body": """Hi {name},

I noticed {company} {observation}.

I build AI agents that automate {pain_point} — so your team stops wasting time on repetitive tasks.

Most clients save 10-15 hours/week after implementing one.

Worth a quick 15-min call?

GBOYEE
XanderCorp"""
    },
    
    "follow_up_1": {
        "subject": "Re: Quick question about {company}",
        "body": """Hi {name},

Sent you a note earlier about automating {pain_point} at {company}.

Still happy to share how I'd approach it. No pressure — just a quick chat.

GBOYEE"""
    },
    
    "follow_up_2": {
        "subject": "Re: AI agents for {company}",
        "body": """Hi {name},

One more thing — I offer a $150 starter package. You get a working AI agent in 3 days.

No commitment to see what I'd build for you.

Worth 10 minutes?

GBOYEE"""
    },
    
    "final": {
        "subject": "Did I reach the right person?",
        "body": """Hi {name},

I've been trying to reach you about AI automation for {company}.

If this isn't relevant, no worries — just let me know and I'll stop following up.

Best,
GBOYEE"""
    }
}

def format_email(template_name, **kwargs):
    """Format email template"""
    template = TEMPLATES.get(template_name, TEMPLATES["cold_intro"])
    subject = template["subject"].format(**kwargs)
    body = template["body"].format(**kwargs)
    return subject, body

if __name__ == "__main__":
    print("📊 XanderCorp Outreach Status")
    print("=" * 40)
    
    can_send_now, msg = can_send()
    print(f"✅ {msg}")
    
    print(f"\n📅 Optimal timing:")
    print(f"   Days: Tuesday, Wednesday, Thursday")
    print(f"   Hours: 9-10 AM, 3-4 PM")
    
    print(f"\n📧 Templates available:")
    for name in TEMPLATES:
        print(f"   • {name}")