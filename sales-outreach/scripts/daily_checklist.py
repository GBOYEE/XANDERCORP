#!/usr/bin/env python3
"""
XanderCorp Daily Checklist Generator
Creates daily checklist, logs activities, runs at 00:00
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# Directories
CHECKLIST_DIR = "/root/xandercorp/logs/daily_checklists"
REVIEW_DIR = "/root/xandercorp/logs/daily_reviews"
os.makedirs(CHECKLIST_DIR, exist_ok=True)
os.makedirs(REVIEW_DIR, exist_ok=True)

# Retention: 30 days
RETENTION_DAYS = 30

def create_checklist(date=None):
    """Create daily checklist for given date"""
    if date is None:
        date = datetime.now()
    
    date_str = date.strftime("%Y-%m-%d")
    file_path = f"{CHECKLIST_DIR}/{date_str}.md"
    
    if os.path.exists(file_path):
        print(f"📋 Checklist for {date_str} already exists")
        return file_path
    
    checklist = f"""# Daily Checklist — {date_str}

> XanderCorp Operations

---

## MORNING CHECK (Before 12:00)

### Outreach
- [ ] Check email responses
- [ ] Review yesterday's follow-ups needed
- [ ] Add new leads to database

### System
- [ ] Run health check
- [ ] Check server status (Axiom Core, Brain v3)
- [ ] Review error logs

---

## DAYTIME TASKS

### Outreach (Max 15/day)
- [ ] Send cold emails to new leads
- [ ] Follow up on day-3 non-responders
- [ ] Follow up on day-6 non-responders
- [ ] Log all sent emails

### Sales
- [ ] Respond to inquiries within 2 hours
- [ ] Send proposals
- [ ] Update lead status in database

### Content
- [ ] GitHub activity (commits, repos)
- [ ] Portfolio updates if needed

---

## EVENING CHECK (Before 23:00)

### Review
- [ ] What worked today?
- [ ] What didn't work?
- [ ] Tomorrow's priorities?

### System
- [ ] Backup credentials
- [ ] Push logs to GitHub
- [ ] Verify no errors

---

## NOTES

```
(Write notes here)
```

---

*Generated: {datetime.now().isoformat()}*"""
    
    with open(file_path, "w") as f:
        f.write(checklist)
    
    print(f"✅ Created: {file_path}")
    return file_path

def run_daily_review():
    """Generate daily review report"""
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    review_file = f"{REVIEW_DIR}/{date_str}_review.md"
    
    # Get today's checklist
    checklist_file = f"{CHECKLIST_DIR}/{date_str}.md"
    checklist_content = ""
    if os.path.exists(checklist_file):
        with open(checklist_file, "r") as f:
            checklist_content = f.read()
    
    # Get email stats
    sent_log = "/root/gsd/xandercorp/sales-outreach/emails/sent_log.json"
    emails_sent_today = 0
    if os.path.exists(sent_log):
        with open(sent_log, "r") as f:
            logs = json.load(f)
        emails_sent_today = len([l for l in logs if l["timestamp"].startswith(date_str)])
    
    review = f"""# Daily Review — {date_str}

> XanderCorp Operations Review

---

## ACTIVITY SUMMARY

| Metric | Count |
|--------|-------|
| Emails Sent | {emails_sent_today} |
| Leads Added | (update) |
| Responses | (update) |
| Deals Closed | (update) |

---

## WHAT WORKED TODAY

```
1.
2.
3.
```

---

## WHAT DIDN'T WORK

```
1.
2.
3.
```

---

## BLOCKERS / NEED CEO INPUT

```
1.
2.
```

---

## TOMORROW'S PRIORITIES

```
1.
2.
3.
```

---

## LEARNINGS FOR NEXT TIME

```
1.
2.
```

---

*Review completed: {datetime.now().isoformat()}*"""
    
    with open(review_file, "w") as f:
        f.write(review)
    
    print(f"✅ Created: {review_file}")
    return review_file

def cleanup_old_files():
    """Delete files older than 30 days"""
    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)
    deleted = 0
    
    for directory in [CHECKLIST_DIR, REVIEW_DIR]:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                if mtime < cutoff:
                    os.remove(filepath)
                    deleted += 1
    
    if deleted > 0:
        print(f"🗑️ Deleted {deleted} old files")
    else:
        print("✅ No old files to clean up")

def get_today_checklist():
    """Print today's checklist"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_path = f"{CHECKLIST_DIR}/{date_str}.md"
    
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            print(f.read())
    else:
        print("📋 No checklist for today. Creating one...")
        create_checklist()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "create":
            create_checklist()
        elif sys.argv[1] == "review":
            run_daily_review()
        elif sys.argv[1] == "cleanup":
            cleanup_old_files()
        elif sys.argv[1] == "show":
            get_today_checklist()
        else:
            print("Usage: daily_checklist.py [create|review|cleanup|show]")
    else:
        # Default: show today's checklist
        get_today_checklist()