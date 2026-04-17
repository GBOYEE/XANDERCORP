# Server Maintenance Protocol

## Server Info
- **Main Server:** 207.180.223.192
- **Worker Server:** 109.199.120.23
- **OS:** Ubuntu/Linux

---

## Daily Checks (Automated)

### System Health
```bash
# Check all services
pm2 status

# Check disk space
df -h

# Check memory
free -h

# Check CPU
top -bn1 | head -5

# Check uptime
uptime
```

### Service Status
| Service | Port | Manager | Check Command |
|---------|------|---------|---------------|
| Axiom Core | 8001 | PM2 | `curl localhost:8001/health` |
| Brain v3 | 3000 | PM2 | `pm2 status` |
| Redis | 6379 | PM2 | `pm2 status` |
| Ollama | 11434 | Systemd | `curl localhost:11434/api/tags` |
| Postgres | 5432 | PM2 | `pm2 status` |

---

## Weekly Maintenance

### 1. Security Updates
```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Check for vulnerabilities
sudo apt list --upgradable
```

### 2. Log Rotation
```bash
# Check log sizes
du -sh /var/log/*

# Rotate logs
sudo logrotate -f /etc/logrotate.conf
```

### 3. Backup Verification
```bash
# Check backup exists
ls -la /root/xandercorp/backups/

# Verify backup integrity
cd /root/xandercorp/backups && tar -tzf latest.tar.gz | head
```

### 4. Clean Up
```bash
# Clear temp files
rm -rf /tmp/*

# Clear npm cache
npm cache clean --force

# Clear PM2 logs
pm2 flush

# Docker cleanup
docker system prune -af
```

---

## Monthly Maintenance

### 1. Full System Audit
- Review all logs for errors
- Check all services auto-restart settings
- Verify SSL certificates
- Test backup restoration

### 2. Resource Optimization
- Review memory usage patterns
- Check for memory leaks
- Optimize PM2 cluster count
- Review Docker image sizes

### 3. Dependency Updates
```bash
# Update Node dependencies
cd /path/to/project && npm update

# Update Python dependencies
pip list --outdated
pip install -r requirements.txt --upgrade
```

---

## Maintenance Scripts

### Health Check Script
```bash
#!/bin/bash
# /root/xandercorp/ops/health_check.sh

echo "=== XanderCorp Health Check ==="
echo "Date: $(date)"
echo ""

echo "--- Services ---"
pm2 status

echo ""
echo "--- Disk ---"
df -h | grep -E '/$'

echo ""
echo "--- Memory ---"
free -h

echo ""
echo "--- Recent Errors ---"
pm2 logs --nostream --lines 10 --err
```

### Auto-Maintenance Cron
```bash
# Add to crontab
0 2 * * 0 /root/xandercorp/ops/weekly_maintenance.sh
0 3 * * * /root/xandercorp/ops/health_check.sh >> /root/xandercorp/logs/health.log
```

---

## Incident Response

### Service Down
1. Check PM2 status: `pm2 status`
2. Check logs: `pm2 logs <service>`
3. Restart if needed: `pm2 restart <service>`
4. Document incident in `/root/xandercorp/logs/`

### High Memory
1. Identify culprit: `pm2 monit`
2. Restart service: `pm2 restart <service>`
3. Log incident

### Disk Full
1. Find large files: `du -sh /* | sort -h`
2. Clean up: `docker system prune -af`
3. Log incident

---

## Emergency Contacts

| Role | Contact |
|------|---------|
| Owner | GBOYEE (Telegram) |
| System | nanobot (AI Agent) |

---

*Last updated: 2026-04-17*