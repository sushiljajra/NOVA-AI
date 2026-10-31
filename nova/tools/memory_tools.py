import sqlite3
import datetime
from pathlib import Path
from typing import List, Dict, Any

DB_PATH = Path(__file__).resolve().parent.parent.parent / "nova_memory.db"

def _init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            fact TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

_init_db()

def remember_fact(key: str, fact: str, category: str = "general") -> str:
    """
    Stores a permanent fact, preference, habit, or note in ECLIPSE's long-term memory.
    Example: remember_fact(key="favorite_editor", fact="The user prefers VS Code with dark theme", category="preferences")
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("remember_fact", {"key": key, "fact": fact, "category": category})

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clean_key = key.strip().lower().replace(" ", "_")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO memories (key, fact, category, created_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET
            fact=excluded.fact,
            category=excluded.category,
            created_at=excluded.created_at
    """, (clean_key, fact.strip(), category.strip(), now))
    conn.commit()
    conn.close()

    res = f"Stored memory '{clean_key}': {fact} (Category: {category})."
    print_tool_result(res)
    return res

def recall_fact(search_query: str) -> str:
    """
    Searches ECLIPSE's long-term database for facts, notes, or preferences matching a query.
    Example: recall_fact(search_query="editor")
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("recall_fact", {"search_query": search_query})

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    pattern = f"%{search_query.strip()}%"
    cursor.execute("""
        SELECT key, fact, category, created_at FROM memories
        WHERE key LIKE ? OR fact LIKE ? OR category LIKE ?
    """, (pattern, pattern, pattern))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        res = f"No memories found matching '{search_query}'."
        print_tool_result(res)
        return res

    results = []
    for r in rows:
        results.append(f"[{r[2].upper()}] {r[0]}: {r[1]} (Saved: {r[3]})")
    res = "\n".join(results)
    print_tool_result(res)
    return res

def list_all_memories(category: str = "") -> str:
    """
    Lists all memories saved in ECLIPSE's permanent database, optionally filtered by category.
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("list_all_memories", {"category": category})

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if category:
        cursor.execute("SELECT key, fact, category FROM memories WHERE category = ?", (category.strip(),))
    else:
        cursor.execute("SELECT key, fact, category FROM memories ORDER BY category, key")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        res = "ECLIPSE's memory bank is currently empty."
        print_tool_result(res)
        return res

    lines = [f"{'KEY':<25} {'CATEGORY':<15} {'FACT / NOTE'}"]
    lines.append("-" * 65)
    for r in rows:
        lines.append(f"{r[0]:<25} {r[2]:<15} {r[1]}")
    res = "\n".join(lines)
    print_tool_result(res)
    return res

def delete_memory(key: str) -> str:
    """
    Deletes a memory record by its key.
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("delete_memory", {"key": key})

    clean_key = key.strip().lower().replace(" ", "_")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM memories WHERE key = ?", (clean_key,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()

    if affected > 0:
        res = f"Memory '{clean_key}' deleted from database."
    else:
        res = f"Memory key '{clean_key}' was not found."
    print_tool_result(res)
    return res

