#!/bin/bash
# /root/xandercorp/ops/log_activity.sh
# Log activities to the activity log

LOG_DIR="/root/xandercorp/logs"
ACTIVITY_LOG="$LOG_DIR/activity.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

log() {
    local type="$1"
    local actor="$2"
    local action="$3"
    local details="$4"
    
    echo "$TIMESTAMP | $type | $actor | $action | $details" >> "$ACTIVITY_LOG"
    echo "✅ Logged: [$type] $action"
}

case "$1" in
    "revenue")
        log "REVENUE" "$2" "$3" "$4"
        ;;
    "outreach")
        log "OUTREACH" "$2" "$3" "$4"
        ;;
    "system")
        log "SYSTEM" "$2" "$3" "$4"
        ;;
    "decision")
        log "DECISION" "$2" "$3" "$4"
        ;;
    "error")
        log "ERROR" "$2" "$3" "$4"
        ;;
    *)
        log "ACTIVITY" "$1" "$2" "$3"
        ;;
esac