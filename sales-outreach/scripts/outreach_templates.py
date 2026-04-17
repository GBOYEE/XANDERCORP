#!/usr/bin/env python3
"""
Branded Email Templates
XanderCorp Cold Outreach
"""

TEMPLATES = {
    "intro": {
        "subject": "Quick question about {company}",
        "html": """
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
<div style="background: #1a1a2e; padding: 25px; text-align: center;">
<h1 style="color: #fff; margin: 0; font-size: 24px;">XanderCorp</h1>
</div>
<div style="padding: 30px; background: #fff;">
<p>Hi {name},</p>
<p>I noticed {company} {observation}.</p>
<p>I build AI automation systems that help businesses like yours eliminate repetitive work, generate leads, and scale faster.</p>
<p>Most clients save 10-20 hours per week after implementing one AI agent.</p>
<p>Would you be open to a quick 15-minute call this week?</p>
<p>Best,<br>GBOYEE</p>
</div>
</body>
</html>
"""
    },
    
    "problem_focused": {
        "subject": "Automating {pain_point} at {company}",
        "html": """
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #1a1a2e; padding: 25px; text-align: center;">
                <h1 style="color: #fff; margin: 0; font-size: 24px;">XanderCorp</h1>
            </div>
            <div style="padding: 30px; background: #fff;">
                <p>Hi {name},</p>
                <p>I saw that {company} {process}.</p>
                <p>I build AI agents that automate exactly this — so your team stops wasting time on repetitive tasks.</p>
                <p>Here's what I'd build for you:</p>
                <ul>
                    <li>{feature_1}</li>
                    <li>{feature_2}</li>
                    <li>{feature_3}</li>
                </ul>
                <p>Starting at <strong>$150</strong> (delivered in 3 days).</p>
                <p>Wanna see a quick demo?</p>
                <p>Best,<br>GBOYEE</p>
            </div>
        </body>
        </html>
        """
    },
    
    "social_proof": {
        "subject": "How {similar_company} saved 15 hours/week",
        "html": """
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #1a1a2e; padding: 25px; text-align: center;">
                <h1 style="color: #fff; margin: 0; font-size: 24px;">XanderCorp</h1>
            </div>
            <div style="padding: 30px; background: #fff;">
                <p>Hi {name},</p>
                <p>I just finished building an AI agent for {similar_company} that {what_it_does}.</p>
                <p>They went from {before} to fully automated — saving {hours} hours per week.</p>
                <p>I can build something similar for {company} — starting at $150.</p>
                <p>Got 15 minutes for a quick call?</p>
                <p>Best,<br>GBOYEE</p>
            </div>
        </body>
        </html>
        """
    },
    
    "low_price": {
        "subject": "AI agents at half the price you'd pay elsewhere",
        "html": """
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #1a1a2e; padding: 25px; text-align: center;">
                <h1 style="color: #fff; margin: 0; font-size: 24px;">XanderCorp</h1>
            </div>
            <div style="padding: 30px; background: #fff;">
                <p>Hi {name},</p>
                <p>Most AI agent agencies charge $1,000+ for custom automation.</p>
                <p>I charge $150-800 depending on complexity — and I deliver in 3-7 days.</p>
                <p>I've built {num_projects} production AI systems for businesses like yours.</p>
                <p>What repetitive task is eating up your team's time? I can probably automate it.</p>
                <p>Let's chat.</p>
                <p>Best,<br>GBOYEE</p>
            </div>
        </body>
        </html>
        """
    },
    
    "follow_up": {
        "subject": "Re: AI agents — one more thing",
        "html": """
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #1a1a2e; padding: 25px; text-align: center;">
                <h1 style="color: #fff; margin: 0; font-size: 24px;">XanderCorp</h1>
            </div>
            <div style="padding: 30px; background: #fff;">
                <p>Hi {name},</p>
                <p>Sent you a message earlier about AI automation for {company}.</p>
                <p>Just wanted to add: I offer a <strong>$150 starter package</strong> — you get a working AI agent in 3 days.</p>
                <p>No commitment required to see what I'd build for you.</p>
                <p>Worth a 10-minute call?</p>
                <p>Best,<br>GBOYEE</p>
            </div>
        </body>
        </html>
        """
    }
}

def get_template(name):
    """Get email template by name"""
    return TEMPLATES.get(name, TEMPLATES["intro"])

def fill_template(template, **kwargs):
    """Fill template with variables"""
    subject = template["subject"].format(**kwargs)
    html = template["html"].format(**kwargs)
    return subject, html

if __name__ == "__main__":
    # Test
    template = get_template("low_price")
    subject, html = fill_template(
        template,
        name="John",
        num_projects="20+",
    )
    print(f"Subject: {subject}")
    print("Template ready!")