#!/bin/bash
# XanderCorp Credentials Manager
# Secure credential storage and retrieval

CRED_DIR="/root/xandercorp/.credentials"
mkdir -p "$CRED_DIR"
chmod 700 "$CRED_DIR"

case "$1" in
    set)
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "Usage: $0 set <key> <value>"
            exit 1
        fi
        echo "$3" > "$CRED_DIR/$2"
        chmod 600 "$CRED_DIR/$2"
        echo "✅ $2 saved"
        ;;
    get)
        if [ -z "$2" ]; then
            echo "Usage: $0 get <key>"
            exit 1
        fi
        if [ -f "$CRED_DIR/$2" ]; then
            cat "$CRED_DIR/$2"
        else
            echo "❌ Key not found: $2"
            exit 1
        fi
        ;;
    list)
        echo "📋 Stored credentials:"
        ls -1 "$CRED_DIR" 2>/dev/null || echo "  None"
        ;;
    delete)
        if [ -z "$2" ]; then
            echo "Usage: $0 delete <key>"
            exit 1
        fi
        rm -f "$CRED_DIR/$2"
        echo "✅ Deleted: $2"
        ;;
    *)
        echo "XanderCorp Credentials Manager"
        echo ""
        echo "Usage: $0 <command> [args]"
        echo ""
        echo "Commands:"
        echo "  set <key> <value>  - Store a credential"
        echo "  get <key>          - Retrieve a credential"
        echo "  list               - List all stored credentials"
        echo "  delete <key>       - Delete a credential"
        echo ""
        echo "Stored in: $CRED_DIR"
        ;;
esac