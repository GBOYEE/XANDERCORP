#!/bin/bash
# /root/xandercorp/ops/weekly_maintenance.sh
# Weekly maintenance tasks

LOG_DIR="/root/xandercorp/logs"
BACKUP_DIR="/root/xandercorp/backups"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

echo "=== XanderCorp Weekly Maintenance ==="
echo "Date: $TIMESTAMP"
echo ""

# 1. System updates
echo "--- Updating system ---"
sudo apt update -qq && sudo apt upgrade -y -qq

# 2. Run backup
echo ""
echo "--- Running backup ---"
/root/xandercorp/ops/backup.sh

# 3. Clear logs
echo ""
echo "--- Clearing old logs ---"
pm2 flush

# 4. Docker cleanup
echo ""
echo "--- Docker cleanup ---"
docker system prune -af --volumes 2>/dev/null || echo "Docker not available"

# 5. Security check
echo ""
echo "--- Security check ---"
grep "Failed" /var/log/auth.log 2>/dev/null | tail -5 || echo "No failed SSH attempts"

# 6. Log completion
echo ""
echo "$TIMESTAMP | SYSTEM | weekly_maintenance | Completed" >> $LOG_DIR/activity.log
echo "✅ Weekly maintenance complete"