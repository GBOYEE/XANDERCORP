# Security Protocol

> **Security is not an afterthought. It's part of running a company.**

---

## Core Security Rules

1. **No secrets in code** — Use environment variables
2. **No credentials in logs** — Sanitize everything
3. **No default passwords** — Change everything
4. **No open ports** — Close what you don't use
5. **No shared accounts** — Individual access only
6. **Log everything** — Audit trail for everything

---

## Access Control

### Server Access
| User | Access Level | SSH Key |
|------|--------------|---------|
| root | Full | Restricted |
| gboyee | Admin | Required |
| nanobot | Service | Limited |

### API Keys & Secrets
| Service | Storage | Rotation |
|---------|---------|----------|
| Upwork API | Env vars | 90 days |
| Gmail API | Env vars | 90 days |
| GitHub Token | Env vars | 90 days |
| Database | Env vars | 180 days |

---

## Network Security

### Firewall Rules
```bash
# Allow only necessary ports
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 8001/tcp  # Axiom Core
ufw allow 3000/tcp  # Brain v3
```

### Port Exposure
| Port | Service | Public? |
|------|---------|---------|
| 22 | SSH | Restricted |
| 80 | HTTP | Yes |
| 443 | HTTPS | Yes |
| 8001 | Axiom | Yes |
| 3000 | Brain | Internal |
| 11434 | Ollama | Internal |

---

## Application Security

### API Endpoints
- [ ] All endpoints require authentication
- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention
- [ ] XSS protection headers

### Data Handling
- [ ] No PII in logs
- [ ] No credentials in responses
- [ ] Encrypted at rest (where possible)
- [ ] Encrypted in transit (HTTPS)

---

## Secrets Management

### Environment Variables (REQUIRED)
```bash
# Never commit these
GMAIL_CLIENT_ID=
GMAIL_CLIENT_SECRET=
GMAIL_REFRESH_TOKEN=
UPWORK_API_KEY=
GITHUB_TOKEN=
DATABASE_URL=
REDIS_URL=
```

### Secret Rotation
- API keys: Every 90 days
- Database: Every 180 days
- SSH keys: Every 365 days

---

## Security Checklist

### Daily
- [ ] Check for unauthorized access attempts
- [ ] Verify services are running correctly
- [ ] Review error logs for suspicious activity

### Weekly
- [ ] Check failed SSH attempts: `grep "Failed" /var/log/auth.log`
- [ ] Review API usage for anomalies
- [ ] Update system packages

### Monthly
- [ ] Full security audit
- [ ] Rotate API keys
- [ ] Review access logs
- [ ] Test backup restoration
- [ ] Pen test critical endpoints

---

## Incident Response

### Suspected Breach
1. **Isolate** — Stop affected service
2. **Document** — Log everything
3. **Assess** — What was accessed?
4. **Fix** — Patch vulnerability
5. **Restore** — Bring service back
6. **Review** — Prevent future incidents

### Data Breach
1. Identify scope
2. Notify affected parties
3. Document timeline
4. Fix vulnerability
5. Report to authorities if required

---

## Backup Security

- Backups encrypted at rest
- Backups stored in secure location
- Access restricted to owner only
- Regular backup restoration tests
- Backup retention: 30 days

---

## Compliance

### Client Data
- No client data stored without consent
- No PII in development logs
- Client data deleted on request
- Secure file transfer only

### Financial Data
- Invoices stored securely
- Payment info never stored locally
- Use secure payment processors

---

## Security Audit Log

| Date | Auditor | Findings | Status |
|------|---------|----------|--------|
| 2026-04-17 | nanobot | Initial setup | Complete |

---

*Last updated: 2026-04-17*