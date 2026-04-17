# XanderCorp Credentials Management

> **Secure credential storage and retrieval system**

---

## Overview

All sensitive credentials stored in `/root/xandercorp/.credentials/` with 600 permissions.

---

## Credential Manager

```bash
# Store a credential
/root/xandercorp/ops/credentials.sh set <key> <value>

# Retrieve a credential
/root/xandercorp/ops/credentials.sh get <key>

# List all credentials
/root/xandercorp/ops/credentials.sh list

# Delete a credential
/root/xandercorp/ops/credentials.sh delete <key>
```

---

## Currently Stored

| Key | Description |
|-----|-------------|
| `gmail_password` | Gmail app password for outreach |

---

## Adding New Credentials

### Gmail App Password
```bash
/root/xandercorp/ops/credentials.sh set gmail_password "your_16_char_password"
```

### API Keys
```bash
/root/xandercorp/ops/credentials.sh set openai_key "sk-..."
/root/xandercorp/ops/credentials.sh set github_token "ghp_..."
```

---

## Backup

Credentials are backed up daily via:
```bash
/root/xandercorp/ops/backup_credentials.sh
```

Backups stored in: `/root/xandercorp/backups/credentials/`

---

## Security

- Directory: `chmod 700` (owner only)
- Files: `chmod 600` (owner read/write)
- Never commit to git
- Never log passwords

---

## Troubleshooting

### "Key not found"
Run: `/root/xandercorp/ops/credentials.sh list`

### Need to reset password
```bash
# Delete old
/root/xandercorp/ops/credentials.sh delete gmail_password

# Add new
/root/xandercorp/ops/credentials.sh set gmail_password "new_password"
```

---

*Last updated: 2026-04-17*