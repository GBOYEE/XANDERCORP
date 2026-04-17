#!/bin/bash
# /root/gsd/xandercorp/sales-outreach/scripts/setup_gmail.sh
# Gmail setup guide for XanderCorp

echo "=========================================="
echo "   XANDERCorp Gmail Setup"
echo "=========================================="
echo ""

echo "📧 STEP 1: Enable 2-Factor Authentication"
echo "   1. Go to: https://myaccount.google.com/security"
echo "   2. Click '2-Step Verification' → Get Started"
echo "   3. Follow the prompts"
echo ""

echo "🔑 STEP 2: Generate App Password"
echo "   1. Go to: https://myaccount.google.com/apppasswords"
echo "   2. Select app: 'Mail'"
echo "   3. Select device: 'Other (Custom name)' → type 'XanderCorp'"
echo "   4. Click 'Generate'"
echo "   5. Copy the 16-character password"
echo ""

echo "📝 STEP 3: Save Your App Password"
echo "   Run this command and paste your password:"
echo ""
echo "   echo 'GMAIL_APP_PASSWORD=your_password_here' > /root/xandercorp/.env"
echo "   chmod 600 /root/xandercorp/.env"
echo ""

echo "✅ STEP 4: Test Setup"
echo "   python3 /root/gsd/xandercorp/sales-outreach/scripts/email_sender.py test"
echo ""

echo "=========================================="
echo "   Gmail Sending Limits"
echo "=========================================="
echo "   • 500 emails/day (personal Gmail)"
echo "   • Safe limit: 50-100/day"
echo "   • Use 'Resend' or 'Loops' for bulk"
echo "=========================================="