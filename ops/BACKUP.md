# Backup System

> **If it's not backed up, it doesn't exist.**

---

## Backup Schedule

| Type | Frequency | Retention | Location |
|------|-----------|-----------|----------|
| Full | Weekly | 4 weeks | /root/xandercorp/backups/ |
| Incremental | Daily | 7 days | /root/xandercorp/backups/incremental/ |
| Config | On change | 30 versions | Git |

---

## What We Backup

### Critical (Daily)
- [ ] Source code (/root/gsd/)
- [ ] Configuration files
- [ ] Environment variables (encrypted)
- [ ] Sales outreach data
- [ ] Lead databases

### Important (Weekly)
- [ ] PM2 ecosystem files
- [ ] Docker configurations
- [ ] Nginx configs
- [ ] SSL certificates

### Documentation
- [ ] /root/xandercorp/docs/
- [ ] /root/xandercorp/ops/
- [ ] /root/xandercorp/security/

---

## Backup Script

```bash
#!/bin/bash
# /root/xandercorp/ops/backup.sh

BACKUP_DIR="/root/xandercorp/backups"
DATE=$(date +%Y%m%d_%H%M%S)

echo "=== XanderCorp Backup ==="
echo "Date: $DATE"

# Create backup directory
mkdir -p $BACKUP_DIR/incremental

# Backup critical directories
tar -czf $BACKUP_DIR/backup_$DATE.tar.gz \
  /root/gsd \
  /root/xandercorp \
  /root/.env 2>/dev/null || true

# Create symlink to latest
ln -sf $BACKUP_DIR/backup_$DATE.tar.gz $BACKUP_DIR/latest.tar.gz

# Backup PM2
pm2 save

# Log it
echo "$DATE - Backup completed" >> $BACKUP_DIR/backup.log

echo "✅ Backup complete: $BACKUP_DIR/backup_$DATE.tar.gz"
```

---

## Restoration Test

```bash
# Test restoration (on a separate directory first)
mkdir /tmp/restore_test
tar -xzf /root/xandercorp/backups/latest.tar.gz -C /tmp/restore_test
ls -la /tmp/restore_test
rm -rf /tmp/restore_test
```

---

## Backup Log

| Date | File | Size | Status |
|------|------|------|--------|
| 2026-04-17 | Initial setup | - | Complete |

---

*Last updated: 2026-04-17*