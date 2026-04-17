#!/usr/bin/env python3
"""
XanderCorp Email Sender
Branded cold outreach system
"""

import yagmail
import json
import os
from datetime import datetime
from pathlib import Path

# Configuration
SENDER_EMAIL = "Xanderaicorp@gmail.com"
SENDER_NAME = "Oyebanji Adegboyega | XanderCorp"
LOGO_PATH = "/root/gsd/email-branding/xandercorp-logo.jpg"

# Storage
SENT_DIR = "/root/gsd/xandercorp/sales-outreach/emails"
os.makedirs(SENT_DIR, exist_ok=True)

def load_credentials():
    """Load Gmail app password from secure storage"""
    cred_file = "/root/xandercorp/.env"
    if os.path.exists(cred_file):
        with open(cred_file, "r") as f:
            for line in f:
                if line.startswith("GMAIL_APP_PASSWORD"):
                    return line.split("=")[1].strip()
    return None

def load_signature():
    """Load branded email signature"""
    return """
    <p style="margin: 0; padding: 0;">
      <strong>Oyebanji Adegboyega</strong><br>
      <span style="color: #e94560;">Founder, XanderCorp</span>
    </p>
    <p style="margin: 10px 0 0 0; padding: 0;">
      📧 Xanderaicorp@gmail.com<br>
      🌐 github.com/GBOYEE | gboyee.github.io<br>
      🔗 https://calendly.com/xanderaicorp
    </p>
    <p style="margin: 15px 0 0 0; padding: 0; font-size: 12px; color: #666;">
      <em>AI Agent Systems & Multi-Agent Orchestration</em>
    </p>
    """

def send_email(to_email, subject, html_content, track_open=True):
    """Send branded email"""
    app_password = load_credentials()
    
    if not app_password:
        return {"success": False, "error": "No app password. Run setup first."}
    
    try:
        yag = yagmail.SMTP(SENDER_EMAIL, app_password, sender_name=SENDER_NAME)
        
        # Add signature
        full_html = html_content + load_signature()
        
        # Send with inline logo
        yag.send(
            to=to_email,
            subject=subject,
            contents=full_html,
            inline_image_logo=LOGO_PATH if os.path.exists(LOGO_PATH) else None
        )
        
        # Log it
        log_sent(to_email, subject)
        
        return {"success": True, "to": to_email}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def log_sent(to_email, subject):
    """Log sent email"""
    log_file = f"{SENT_DIR}/sent_log.json"
    
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            logs = json.load(f)
    else:
        logs = []
    
    logs.append({
        "timestamp": datetime.now().isoformat(),
        "to": to_email,
        "subject": subject
    })
    
    with open(log_file, "w") as f:
        json.dump(logs, f, indent=2)

def send_test_email():
    """Send test email to verify setup"""
    test_email = "Oyebanjiadegboyee@gmail.com"
    
    test_html = """
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: #1a1a2e; padding: 30px; text-align: center;">
            <img src="cid:logo" alt="XanderCorp" style="width: 150px;">
        </div>
        <div style="padding: 30px; background: #f9f9f9;">
            <h2 style="color: #1a1a2e;">🚀 Outreach System Ready!</h2>
            <p>This is a test email from <strong>XanderCorp</strong>.</p>
            <p>If you're reading this, our email system is working correctly!</p>
            <p>Next step: Start sending cold outreach to potential clients.</p>
        </div>
    </body>
    </html>
    """
    
    result = send_email(test_email, "✅ XanderCorp Email System Test", test_html)
    return result

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            print("📧 Sending test email...")
            result = send_test_email()
            if result["success"]:
                print(f"✅ Test email sent to {result['to']}")
            else:
                print(f"❌ Error: {result['error']}")
        elif sys.argv[1] == "credentials":
            cred = load_credentials()
            if cred:
                print("✅ App password loaded")
            else:
                print("❌ No app password found. Add to /root/xandercorp/.env")
    else:
        print("XanderCorp Email Sender")
        print("Usage:")
        print("  python3 email_sender.py test         - Send test email")
        print("  python3 email_sender.py credentials  - Check credentials")