#!/usr/bin/env python3
"""
XanderCorp Sales Agent
Autonomous outbound sales system
"""

import sys
import os

# Add scripts dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from outreach_tracker import log_outreach, update_status, get_stats, print_dashboard
from lead_research import get_next_outreach_batch, TARGET_INDUSTRIES

def send_outreach(recipient, platform, template_num):
    """Log an outreach message"""
    template = f"cold-offer-v{template_num}"
    result = log_outreach(recipient, platform, template)
    return result

def daily_outreach_routine():
    """Run daily outreach routine"""
    print("\n🚀 XanderCorp Sales Agent — Daily Routine")
    print("=" * 50)
    
    # Get priority leads
    leads = get_next_outreach_batch(10)
    
    print(f"\n📋 Priority leads for today:")
    for i, lead in enumerate(leads, 1):
        print(f"  {i}. {lead['industry']} — {lead['pain_points'][0]}")
    
    print("\n📊 Current Stats:")
    print_dashboard()
    
    print("\n💡 Next Actions:")
    print("  1. Pick a lead")
    print("  2. Find their contact on LinkedIn/Twitter")
    print("  3. Send personalized message")
    print("  4. Log it with: log_outreach(name, platform, template_num)")
    
    return leads

def quick_outreach(industry, recipient_name, platform="linkedin"):
    """Quick outreach for a specific lead"""
    return send_outreach(recipient_name, platform, 1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "stats":
            print_dashboard()
        elif sys.argv[1] == "leads":
            leads = get_next_outreach_batch()
            for lead in leads:
                print(f"• {lead['industry']}: {lead['pain_points'][0]}")
        else:
            print(daily_outreach_routine())
    else:
        print(daily_outreach_routine())