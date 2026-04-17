#!/bin/bash
# /root/xandercorp/ops/health_check.sh
# Daily system health check

LOG_DIR="/root/xandercorp/logs"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

echo "=== XanderCorp Health Check ==="
echo "Date: $TIMESTAMP"
echo ""

# Services
echo "--- Services (PM2) ---"
pm2 status 2>/dev/null || echo "PM2 not running"

echo ""
echo "--- Disk ---"
df -h | grep -E '/$|overlay'

echo ""
echo "--- Memory ---"
free -h

echo ""
echo "--- Uptime ---"
uptime

echo ""
echo "--- Axiom Core ---"
curl -s http://localhost:8001/health 2>/dev/null || echo "Axiom Core not responding"

echo ""
echo "--- Recent Errors ---"
pm2 logs --nostream --lines 5 --err 2>/dev/null

echo ""
echo "=== Check Complete ==="

# Log check
echo "$TIMESTAMP | SYSTEM | health_check | Daily health check completed" >> $LOG_DIR/activity.log