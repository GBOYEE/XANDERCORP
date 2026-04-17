#!/usr/bin/env python3
"""
Outreach Tracker
Logs all outreach activities and tracks responses
"""

import json
import os
from datetime import datetime
from pathlib import Path

OUTREACH_DIR = "/root/gsd/xandercorp/sales-outreach"
TRACKER_FILE = f"{OUTREACH_DIR}/outreach_tracker.json"

def init_tracker():
    """Initialize the outreach tracker"""
    if not os.path.exists(TRACKER_FILE):
        data = {
            "created": datetime.now().isoformat(),
            "total_sent": 0,
            "total_responses": 0,
            "total_converted": 0,
            "conversations": []
        }
        with open(TRACKER_FILE, "w") as f:
            json.dump(data, f, indent=2)
    return load_tracker()

def load_tracker():
    """Load outreach tracker"""
    with open(TRACKER_FILE, "r") as f:
        return json.load(f)

def save_tracker(data):
    """Save outreach tracker"""
    with open(TRACKER_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_outreach(recipient, platform, template_used, status="sent"):
    """Log an outreach message"""
    data = init_tracker()
    
    conversation = {
        "id": len(data["conversations"]) + 1,
        "recipient": recipient,
        "platform": platform,
        "template": template_used,
        "status": status,
        "sent_at": datetime.now().isoformat(),
        "last_update": datetime.now().isoformat(),
        "notes": ""
    }
    
    data["conversations"].append(conversation)
    data["total_sent"] += 1
    save_tracker(data)
    
    return conversation

def update_status(conversation_id, new_status, notes=""):
    """Update conversation status"""
    data = load_tracker()
    
    for conv in data["conversations"]:
        if conv["id"] == conversation_id:
            conv["status"] = new_status
            conv["last_update"] = datetime.now().isoformat()
            if notes:
                conv["notes"] = notes
            break
    
    if new_status == "responded":
        data["total_responses"] += 1
    elif new_status == "converted":
        data["total_converted"] += 1
    
    save_tracker(data)

def get_stats():
    """Get outreach statistics"""
    data = init_tracker()
    
    total = data["total_sent"]
    responses = data["total_responses"]
    converted = data["total_converted"]
    
    response_rate = (responses / total * 100) if total > 0 else 0
    conversion_rate = (converted / total * 100) if total > 0 else 0
    
    return {
        "total_sent": total,
        "total_responses": responses,
        "total_converted": converted,
        "response_rate": f"{response_rate:.1f}%",
        "conversion_rate": f"{conversion_rate:.1f}%"
    }

def get_pending():
    """Get pending conversations"""
    data = load_tracker()
    return [c for c in data["conversations"] if c["status"] in ["sent", "responded"]]

def print_dashboard():
    """Print outreach dashboard"""
    stats = get_stats()
    
    print("\n" + "=" * 50)
    print("📊 XANDERCorp OUTREACH DASHBOARD")
    print("=" * 50)
    print(f"Total Sent:        {stats['total_sent']}")
    print(f"Responses:         {stats['total_responses']}")
    print(f"Converted:         {stats['total_converted']}")
    print(f"Response Rate:     {stats['response_rate']}")
    print(f"Conversion Rate:   {stats['conversion_rate']}")
    print("=" * 50)
    
    pending = get_pending()
    if pending:
        print(f"\n📬 PENDING ({len(pending)}):")
        for p in pending[:5]:
            print(f"  [{p['id']}] {p['recipient']} — {p['platform']} — {p['status']}")

if __name__ == "__main__":
    init_tracker()
    print_dashboard()