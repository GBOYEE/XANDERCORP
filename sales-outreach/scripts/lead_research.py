#!/usr/bin/env python3
"""
Lead Research Agent
Finds companies that need AI agents
"""

import json
import os
from datetime import datetime

LEADS_DIR = "/root/gsd/xandercorp/sales-outreach/leads"

# Target industries + their pain points
TARGET_INDUSTRIES = {
    "saas_startups": {
        "keywords": ["saas", "startup", "founder", "cto", "tech"],
        "pain_points": ["customer support", "onboarding", "user research", "lead qualification"],
        "platforms": ["linkedin", "producthunt", "twitter"]
    },
    "ecommerce": {
        "keywords": ["ecommerce", "shopify", "woocommerce", "store owner"],
        "pain_points": ["customer service", "inventory management", "order processing", "review responses"],
        "platforms": ["shopify app store", "ecommerce forums", "linkedin"]
    },
    "agencies": {
        "keywords": ["agency", "marketing agency", "digital agency", "creative agency"],
        "pain_points": ["client reporting", "content creation", "social media", "lead gen"],
        "platforms": ["linkedin", "clutch", "upwork"]
    },
    "real_estate": {
        "keywords": ["real estate", "realtor", "property manager"],
        "pain_points": ["lead follow-up", "scheduling", "listing updates", "inquiry responses"],
        "platforms": ["linkedin", "real estate forums", "facebook groups"]
    },
    "healthcare": {
        "keywords": ["healthcare", "clinic", "medical", "doctor"],
        "pain_points": ["appointment scheduling", "patient follow-up", "records management"],
        "platforms": ["linkedin", "healthcare forums"]
    },
    "restaurants": {
        "keywords": ["restaurant", "cafe", "food business", "restaurant owner"],
        "pain_points": ["reservation management", "order taking", "review responses", "delivery coordination"],
        "platforms": ["google maps", "yelp", "linkedin"]
    },
    "logistics": {
        "keywords": ["logistics", "shipping", "delivery", "trucking"],
        "pain_points": ["tracking updates", "customer communication", "dispatch", "route optimization"],
        "platforms": ["linkedin", "logistics forums"]
    },
    "recruitment": {
        "keywords": ["recruitment", "hr", "talent acquisition", "staffing"],
        "pain_points": ["candidate sourcing", "resume screening", "interview scheduling", "follow-ups"],
        "platforms": ["linkedin", "recruitment forums"]
    },
    "finance": {
        "keywords": ["fintech", "accountant", "bookkeeper", "financial advisor"],
        "pain_points": ["data entry", "report generation", "client communication", "compliance tracking"],
        "platforms": ["linkedin", "finance forums"]
    },
    "education": {
        "keywords": ["edtech", "tutoring", "online course", "school admin"],
        "pain_points": ["student communication", "assignment grading", "enrollment", "parent updates"],
        "platforms": ["linkedin", "education forums"]
    }
}

def generate_lead_profile(industry, niche):
    """Generate a sample lead profile for an industry"""
    return {
        "industry": industry,
        "niche": niche,
        "pain_points": TARGET_INDUSTRIES[industry]["pain_points"],
        "platforms": TARGET_INDUSTRIES[industry]["platforms"],
        "outreach_priority": "HIGH" if niche in ["saas_startups", "agencies", "ecommerce"] else "MEDIUM",
        "offer_suggestion": f"AI agent for {TARGET_INDUSTRIES[industry]['pain_points'][0]}",
        "estimated_budget": "$150-800"
    }

def save_leads():
    """Save lead profiles to file"""
    os.makedirs(LEADS_DIR, exist_ok=True)
    
    all_leads = []
    for industry, data in TARGET_INDUSTRIES.items():
        lead = generate_lead_profile(industry, industry)
        all_leads.append(lead)
    
    # Save to JSON
    with open(f"{LEADS_DIR}/lead_profiles.json", "w") as f:
        json.dump(all_leads, f, indent=2)
    
    # Save to readable format
    with open(f"{LEADS_DIR}/lead_profiles.md", "w") as f:
        f.write("# Lead Profiles — XanderCorp\n\n")
        f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
        for lead in all_leads:
            f.write(f"## {lead['industry'].upper()}\n")
            f.write(f"**Priority:** {lead['outreach_priority']}\n\n")
            f.write(f"**Pain Points:** {', '.join(lead['pain_points'])}\n\n")
            f.write(f"**Platforms:** {', '.join(lead['platforms'])}\n\n")
            f.write(f"**Suggested Offer:** {lead['offer_suggestion']}\n\n")
            f.write(f"**Budget:** {lead['estimated_budget']}\n\n")
            f.write("---\n\n")
    
    return all_leads

def get_next_outreach_batch(count=5):
    """Get next batch of leads to outreach"""
    leads = save_leads()
    high_priority = [l for l in leads if l["outreach_priority"] == "HIGH"]
    return high_priority[:count]

if __name__ == "__main__":
    print("🔍 XanderCorp Lead Research Agent")
    print("=" * 40)
    leads = save_leads()
    print(f"\n✅ Generated {len(leads)} lead profiles")
    print(f"📁 Saved to: {LEADS_DIR}")
    print("\n📊 Priority Leads:")
    for lead in get_next_outreach_batch():
        print(f"  • {lead['industry']} — {lead['pain_points'][0]}")