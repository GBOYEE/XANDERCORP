#!/usr/bin/env python3
"""
Lead Finder
Finds companies that need AI agents
"""

import json
import os
from datetime import datetime
from pathlib import Path

LEADS_DIR = "/root/gsd/xandercorp/sales-outreach/leads"
DB_FILE = f"{LEADS_DIR}/lead_database.json"

# Lead templates by industry
INDUSTRY_TEMPLATES = {
    "saas_startup": {
        "pain_points": ["customer support", "user onboarding", "lead qualification", "feature requests"],
        "observation_prompts": [
            "is growing fast but customer support might be stretched",
            "might be spending too much time on manual onboarding",
            "could be automating lead qualification",
            "probably gets a lot of repetitive feature requests"
        ],
        "price_range": "$400-800"
    },
    "ecommerce": {
        "pain_points": ["customer service", "inventory questions", "order status", "return requests"],
        "observation_prompts": [
            "probably gets a lot of 'where is my order' messages",
            "might be drowning in customer service tickets",
            "could be spending hours on return requests",
            "probably answers the same product questions over and over"
        ],
        "price_range": "$150-400"
    },
    "agency": {
        "pain_points": ["client reporting", "content creation", "social media", "lead gen"],
        "observation_prompts": [
            "probably spends too much time on manual client reports",
            "might be looking to automate content workflows",
            "could be scaling their social media manually",
            "probably does a lot of repetitive outreach"
        ],
        "price_range": "$400-800"
    },
    "real_estate": {
        "pain_points": ["lead follow-up", "property inquiries", "scheduling", "viewing coordination"],
        "observation_prompts": [
            "probably loses leads because they can't follow up fast enough",
            "might be spending hours on scheduling",
            "could be missing follow-ups on property inquiries",
            "probably does a lot of repetitive listing updates"
        ],
        "price_range": "$150-400"
    },
    "recruitment": {
        "pain_points": ["candidate sourcing", "resume screening", "interview scheduling", "follow-ups"],
        "observation_prompts": [
            "probably spends hours on resume screening",
            "might be looking to automate candidate follow-ups",
            "could be doing a lot of manual scheduling",
            "probably sources candidates the same way every time"
        ],
        "price_range": "$400-800"
    }
}

def load_database():
    """Load lead database"""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"version": "1.0", "last_updated": "", "leads": []}

def save_database(data):
    """Save lead database"""
    data["last_updated"] = datetime.now().isoformat()
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_lead(name, company, email, industry, website="", linkedin=""):
    """Add a lead to database"""
    db = load_database()
    
    # Check if already exists
    for lead in db["leads"]:
        if lead["email"].lower() == email.lower():
            return {"success": False, "message": "Lead already exists"}
    
    template = INDUSTRY_TEMPLATES.get(industry, INDUSTRY_TEMPLATES["saas_startup"])
    
    lead = {
        "id": len(db["leads"]) + 1,
        "name": name,
        "company": company,
        "email": email,
        "industry": industry,
        "website": website,
        "linkedin": linkedin,
        "pain_point": template["pain_points"][0],
        "observation": template["observation_prompts"][0],
        "price_range": template["price_range"],
        "status": "new",
        "added_at": datetime.now().isoformat(),
        "contacted": False,
        "responded": False,
        "converted": False
    }
    
    db["leads"].append(lead)
    save_database(db)
    
    return {"success": True, "lead": lead}

def get_leads_by_status(status):
    """Get leads by status"""
    db = load_database()
    return [l for l in db["leads"] if l["status"] == status]

def get_next_outreach():
    """Get next lead to outreach"""
    db = load_database()
    
    # Priority: new leads first, then follow-ups
    new_leads = [l for l in db["leads"] if l["status"] == "new" and not l["contacted"]]
    followups = [l for l in db["leads"] if l["status"] in ["contacted", "follow_up_1", "follow_up_2"]]
    
    if new_leads:
        return new_leads[0]
    elif followups:
        return followups[0]
    
    return None

def update_lead_status(lead_id, new_status):
    """Update lead status"""
    db = load_database()
    
    for lead in db["leads"]:
        if lead["id"] == lead_id:
            lead["status"] = new_status
            if new_status in ["contacted", "follow_up_1", "follow_up_2", "responded"]:
                lead["contacted"] = True
            if new_status == "responded":
                lead["responded"] = True
            if new_status == "converted":
                lead["converted"] = True
            save_database(db)
            return {"success": True, "lead": lead}
    
    return {"success": False, "message": "Lead not found"}

def print_dashboard():
    """Print leads dashboard"""
    db = load_database()
    leads = db["leads"]
    
    total = len(leads)
    new_leads = len([l for l in leads if l["status"] == "new"])
    contacted = len([l for l in leads if l["contacted"]])
    responded = len([l for l in leads if l["responded"]])
    converted = len([l for l in leads if l["converted"]])
    
    print("\n" + "=" * 50)
    print("📊 XANDERCorp LEAD DASHBOARD")
    print("=" * 50)
    print(f"Total Leads:    {total}")
    print(f"New:            {new_leads}")
    print(f"Contacted:      {contacted}")
    print(f"Responded:      {responded}")
    print(f"Converted:      {converted}")
    print("=" * 50)
    
    if leads:
        print("\n📋 RECENT LEADS:")
        for lead in leads[-5:]:
            status_emoji = "🆕" if lead["status"] == "new" else "📧" if lead["contacted"] else "✅"
            print(f"  {status_emoji} {lead['name']} | {lead['company']} | {lead['industry']}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "dashboard":
            print_dashboard()
        elif sys.argv[1] == "add":
            if len(sys.argv) >= 7:
                result = add_lead(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
                print(f"✅ Added: {result['lead']['name']}" if result["success"] else f"❌ {result['message']}")
            else:
                print("Usage: python3 lead_finder.py add <name> <company> <email> <industry> <website>")
        elif sys.argv[1] == "next":
            lead = get_next_outreach()
            if lead:
                print(f"\n📬 NEXT LEAD:")
                print(f"   Name: {lead['name']}")
                print(f"   Company: {lead['company']}")
                print(f"   Email: {lead['email']}")
                print(f"   Pain Point: {lead['pain_point']}")
            else:
                print("No leads to contact. Add leads first!")
        else:
            print("Commands: dashboard, add, next")
    else:
        print_dashboard()