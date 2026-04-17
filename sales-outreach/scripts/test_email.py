#!/usr/bin/env python3
"""
XanderCorp Test Email System
All emails MUST be tested before sending to leads
CEO (GBOYEE) must approve test before first batch
"""

import os
import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# Config
TEST_EMAIL = "Oyebanjiadegboyee@gmail.com"  # CEO email
SENDER_EMAIL = os.getenv("GMAIL_USER", "xanderaicorp@gmail.com")
SENDER_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")

# Log directory
LOG_DIR = "/root/gsd/xandercorp/sales-outreach/emails"
os.makedirs(LOG_DIR, exist_ok=True)

def load_templates():
    """Load email templates"""
    templates = {}
    template_dir = Path("/root/gsd/xandercorp/sales-outreach/templates")
    
    if template_dir.exists():
        for f in template_dir.glob("*.txt"):
            with open(f, "r") as file:
                templates[f.stem] = file.read()
    
    return templates

def send_test_email(subject, body, template_name="custom"):
    """Send test email to CEO"""
    if not SENDER_PASSWORD:
        print("❌ GMAIL_APP_PASSWORD not set")
        return False
    
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = TEST_EMAIL
    msg["Subject"] = f"[TEST] {subject}"
    
    # Clean email body (no bloated signatures)
    clean_body = f"""Hi,

This is a TEST email — please review before sending to leads.

---
TEMPLATE: {template_name}
---

{body}

---
END TEST
"""
    
    msg.attach(MIMEText(clean_body, "plain"))
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Test email sent to {TEST_EMAIL}")
        log_test(subject, body, template_name, "sent")
        return True
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        log_test(subject, body, template_name, "failed", str(e))
        return False

def log_test(subject, body, template, status, error=None):
    """Log test email"""
    log_file = f"{LOG_DIR}/test_log.json"
    
    logs = []
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            logs = json.load(f)
    
    log = {
        "timestamp": datetime.now().isoformat(),
        "subject": subject,
        "body_preview": body[:100] + "..." if len(body) > 100 else body,
        "template": template,
        "status": status,
        "error": error
    }
    
    logs.append(log)
    
    with open(log_file, "w") as f:
        json.dump(logs, f, indent=2)

def send_to_lead(email_data):
    """Send email to actual lead (ONLY after test approved)"""
    approval_file = f"{LOG_DIR}/approval_status.json"
    
    if os.path.exists(approval_file):
        with open(approval_file, "r") as f:
            approval = json.load(f)
        
        if not approval.get("test_approved"):
            print("❌ TEST NOT APPROVED — Cannot send to leads")
            print("   Run: test_email.py approve")
            return False
    
    # Proceed with sending
    if not SENDER_PASSWORD:
        print("❌ GMAIL_APP_PASSWORD not set")
        return False
    
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = email_data["to"]
    msg["Subject"] = email_data["subject"]
    msg.attach(MIMEText(email_data["body"], "plain"))
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Sent to: {email_data['to']}")
        log_sent(email_data)
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def log_sent(email_data):
    """Log sent email"""
    log_file = f"{LOG_DIR}/sent_log.json"
    
    logs = []
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            logs = json.load(f)
    
    log = {
        "timestamp": datetime.now().isoformat(),
        "to": email_data["to"],
        "company": email_data.get("company", "unknown"),
        "subject": email_data["subject"],
        "template": email_data.get("template", "unknown"),
        "lead_score": email_data.get("lead_score", 0)
    }
    
    logs.append(log)
    
    with open(log_file, "w") as f:
        json.dump(logs, f, indent=2)

def approve_test():
    """Approve test email for batch sending"""
    approval_file = f"{LOG_DIR}/approval_status.json"
    
    approval = {
        "test_approved": True,
        "approved_at": datetime.now().isoformat(),
        "approved_by": "CEO"
    }
    
    with open(approval_file, "w") as f:
        json.dump(approval, f, indent=2)
    
    print("✅ TEST APPROVED — Ready to send to leads")

def check_approval():
    """Check if test is approved"""
    approval_file = f"{LOG_DIR}/approval_status.json"
    
    if os.path.exists(approval_file):
        with open(approval_file, "r") as f:
            approval = json.load(f)
        
        if approval.get("test_approved"):
            print("✅ Test approved — Can send to leads")
            return True
    
    print("❌ Test NOT approved — Cannot send to leads")
    return False

def show_stats():
    """Show email stats"""
    test_log = f"{LOG_DIR}/test_log.json"
    sent_log = f"{LOG_DIR}/sent_log.json"
    
    print("\n📊 EMAIL STATS")
    print("=" * 40)
    
    if os.path.exists(test_log):
        with open(test_log, "r") as f:
            tests = json.load(f)
        print(f"Tests sent: {len(tests)}")
        print(f"Tests failed: {len([t for t in tests if t['status'] == 'failed'])}")
    else:
        print("Tests sent: 0")
    
    if os.path.exists(sent_log):
        with open(sent_log, "r") as f:
            sent = json.load(f)
        print(f"Emails sent to leads: {len(sent)}")
    else:
        print("Emails sent to leads: 0")
    
    check_approval()
    print("=" * 40)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            # Send test email
            if len(sys.argv) >= 3:
                subject = sys.argv[2]
                body = sys.argv[3] if len(sys.argv) >= 4 else "Test body"
                template = sys.argv[4] if len(sys.argv) >= 5 else "custom"
                send_test_email(subject, body, template)
            else:
                print("Usage: test_email.py test <subject> <body> [template]")
        
        elif sys.argv[1] == "approve":
            approve_test()
        
        elif sys.argv[1] == "check":
            check_approval()
        
        elif sys.argv[1] == "stats":
            show_stats()
        
        elif sys.argv[1] == "send":
            # Send to lead (requires approval)
            if len(sys.argv) >= 3:
                email_data = json.loads(sys.argv[2])
                send_to_lead(email_data)
            else:
                print("Usage: test_email.py send <json_data>")
        
        else:
            print("Commands: test, approve, check, stats, send")
    else:
        show_stats()