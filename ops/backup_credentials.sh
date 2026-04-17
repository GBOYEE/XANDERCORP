#!/bin/bash
# Backup credentials to encrypted location
BACKUP_DIR="/root/xandercorp/backups/credentials"
mkdir -p "$BACKUP_DIR"
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "$BACKUP_DIR/credentials_$DATE.tar.gz" /root/xandercorp/.credentials/
echo "✅ Credentials backed up to $BACKUP_DIR/credentials_$DATE.tar.gz"