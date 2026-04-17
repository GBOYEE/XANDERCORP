#!/usr/bin/env python3
"""
XanderCorp Todo Manager
Tasks last 30 days, then auto-delete
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

TODO_DIR = "/root/xandercorp/logs/todos"
os.makedirs(TODO_DIR, exist_ok=True)

TODO_FILE = f"{TODO_DIR}/active_todos.json"
RETENTION_DAYS = 30

def load_todos():
    """Load todos from file"""
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    return {"todos": [], "created": datetime.now().isoformat()}

def save_todos(data):
    """Save todos to file"""
    data["updated"] = datetime.now().isoformat()
    with open(TODO_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_todo(task, priority="medium", category="general"):
    """Add a new todo"""
    todos = load_todos()
    
    todo = {
        "id": len(todos["todos"]) + 1,
        "task": task,
        "priority": priority,  # low, medium, high, urgent
        "category": category,  # outreach, sales, system, content
        "created": datetime.now().isoformat(),
        "status": "pending",  # pending, in_progress, done
        "due": (datetime.now() + timedelta(days=RETENTION_DAYS)).isoformat()
    }
    
    todos["todos"].append(todo)
    save_todos(todos)
    
    return todo

def list_todos(filter_status=None, filter_category=None):
    """List todos with optional filters"""
    todos = load_todos()
    items = todos["todos"]
    
    if filter_status:
        items = [t for t in items if t["status"] == filter_status]
    if filter_category:
        items = [t for t in items if t["category"] == filter_category]
    
    return items

def update_todo(todo_id, new_status):
    """Update todo status"""
    todos = load_todos()
    
    for todo in todos["todos"]:
        if todo["id"] == todo_id:
            todo["status"] = new_status
            todo["updated_at"] = datetime.now().isoformat()
            save_todos(todos)
            return todo
    
    return None

def delete_todo(todo_id):
    """Delete a todo"""
    todos = load_todos()
    todos["todos"] = [t for t in todos["todos"] if t["id"] != todo_id]
    save_todos(todos)
    return True

def cleanup_expired():
    """Delete todos older than 30 days"""
    todos = load_todos()
    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)
    
    original_count = len(todos["todos"])
    todos["todos"] = [
        t for t in todos["todos"] 
        if datetime.fromisoformat(t["created"]) > cutoff
    ]
    
    deleted = original_count - len(todos["todos"])
    if deleted > 0:
        save_todos(todos)
        print(f"🗑️ Deleted {deleted} expired todos")
    else:
        print("✅ No expired todos")
    
    return deleted

def print_board():
    """Print Kanban-style board"""
    todos = load_todos()
    
    pending = [t for t in todos["todos"] if t["status"] == "pending"]
    in_progress = [t for t in todos["todos"] if t["status"] == "in_progress"]
    done = [t for t in todos["todos"] if t["status"] == "done"]
    
    print("\n" + "=" * 60)
    print("📋 XANDERCorp TODO BOARD")
    print("=" * 60)
    
    print(f"\n🔴 PENDING ({len(pending)})")
    for t in pending:
        priority_emoji = {"urgent": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(t["priority"], "⚪")
        print(f"  {priority_emoji} [{t['id']}] {t['task']} ({t['category']})")
    
    print(f"\n🟡 IN PROGRESS ({len(in_progress)})")
    for t in in_progress:
        print(f"  🔵 [{t['id']}] {t['task']} ({t['category']})")
    
    print(f"\n🟢 DONE ({len(done)})")
    for t in done[-5:]:  # Show last 5
        print(f"  ✅ [{t['id']}] {t['task']}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "add":
            if len(sys.argv) >= 3:
                priority = sys.argv[2] if len(sys.argv) >= 3 else "medium"
                category = sys.argv[3] if len(sys.argv) >= 4 else "general"
                task = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else sys.argv[2]
                todo = add_todo(task, priority, category)
                print(f"✅ Added: {todo['task']}")
            else:
                print("Usage: todo.py add <task> [priority] [category]")
        
        elif sys.argv[1] == "list":
            status = sys.argv[2] if len(sys.argv) >= 3 else None
            for t in list_todos(status):
                print(f"  [{t['id']}] {t['task']} - {t['status']}")
        
        elif sys.argv[1] == "done":
            if len(sys.argv) >= 3:
                update_todo(int(sys.argv[2]), "done")
                print("✅ Marked as done")
        
        elif sys.argv[1] == "progress":
            if len(sys.argv) >= 3:
                update_todo(int(sys.argv[2]), "in_progress")
                print("🟡 Marked as in progress")
        
        elif sys.argv[1] == "delete":
            if len(sys.argv) >= 3:
                delete_todo(int(sys.argv[2]))
                print("🗑️ Deleted")
        
        elif sys.argv[1] == "cleanup":
            cleanup_expired()
        
        elif sys.argv[1] == "board":
            print_board()
        
        else:
            print("Commands: add, list, done, progress, delete, cleanup, board")
    else:
        print_board()