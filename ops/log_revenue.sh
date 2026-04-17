#!/bin/bash
# /root/xandercorp/ops/log_revenue.sh
# Log revenue transactions

TRACKER="/root/xandercorp/docs/REVENUE_TRACKER.md"
LOG_DIR="/root/xandercorp/logs"
TIMESTAMP=$(date '+%Y-%m-%d')

log_revenue() {
    local amount="$1"
    local source="$2"
    local notes="$3"
    
    # Add to tracker
    sed -i "/|^$|a| $TIMESTAMP | \$$amount | $source | $notes |" "$TRACKER"
    
    # Log to activity
    echo "$TIMESTAMP | REVENUE | manual | Income: \$$amount from $source | $notes" >> $LOG_DIR/activity.log
    
    echo "✅ Logged: \$$amount from $source"
}

case "$1" in
    "upwork")
        log_revenue "$2" "Upwork" "$3"
        ;;
    "outreach")
        log_revenue "$2" "Cold Outreach" "$3"
        ;;
    "direct")
        log_revenue "$2" "Direct Client" "$3"
        ;;
    *)
        echo "Usage: log_revenue.sh <upwork|outreach|direct> <amount> <notes>"
        ;;
esac