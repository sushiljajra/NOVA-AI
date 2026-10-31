import json
from pathlib import Path
from typing import Dict, Any

CONTACTS_FILE = Path(__file__).resolve().parent.parent.parent / "contacts.json"

def _load_contacts() -> Dict[str, Any]:
    if not CONTACTS_FILE.exists():
        return {}
    try:
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_contacts(data: Dict[str, Any]):
    with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def save_contact(name: str, phone: str = "", email: str = "", relationship: str = "") -> str:
    """
    Saves or updates a contact in ECLIPSE's persistent memory.
    Example: save_contact(name="Papa", phone="+919876543210", relationship="Father")
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("save_contact", {"name": name, "phone": phone, "email": email, "relationship": relationship})

    contacts = _load_contacts()
    key = name.strip().lower()

    # Clean phone number
    clean_phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").strip()

    contacts[key] = {
        "display_name": name.strip(),
        "phone": clean_phone,
        "email": email.strip(),
        "relationship": relationship.strip()
    }
    _save_contacts(contacts)
    msg = f"Saved contact '{name}' (Phone: {clean_phone or 'N/A'}, Relationship: {relationship or 'N/A'})."
    print_tool_result(msg)
    return msg

def get_contact(name: str) -> str:
    """
    Looks up contact information by name or relationship (e.g., 'Papa', 'Mom', 'Alex').
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("get_contact", {"name": name})

    contacts = _load_contacts()
    query = name.strip().lower()

    # Direct match by name
    if query in contacts:
        c = contacts[query]
        res = f"Contact found: {c['display_name']} | Phone: {c['phone']} | Email: {c.get('email', '')} | Relationship: {c.get('relationship', '')}"
        print_tool_result(res)
        return res

    # Match by relationship or partial name
    for k, v in contacts.items():
        if query in k or query in v.get("relationship", "").lower() or query in v.get("display_name", "").lower():
            res = f"Contact found: {v['display_name']} | Phone: {v['phone']} | Email: {v.get('email', '')} | Relationship: {v.get('relationship', '')}"
            print_tool_result(res)
            return res

    err = f"No contact matching '{name}' found in memory."
    print_tool_result(err)
    return err

def list_contacts() -> str:
    """
    Lists all saved contacts in ECLIPSE's memory.
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("list_contacts", {})

    contacts = _load_contacts()
    if not contacts:
        res = "No contacts currently saved in memory."
        print_tool_result(res)
        return res

    lines = [f"{'NAME':<20} {'PHONE':<18} {'RELATIONSHIP':<15}"]
    lines.append("-" * 55)
    for c in contacts.values():
        lines.append(f"{c['display_name']:<20} {c.get('phone', 'N/A'):<18} {c.get('relationship', ''):<15}")
    res = "\n".join(lines)
    print_tool_result(res)
    return res

def delete_contact(name: str) -> str:
    """
    Removes a contact from ECLIPSE's memory.
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("delete_contact", {"name": name})

    contacts = _load_contacts()
    key = name.strip().lower()

    if key in contacts:
        del contacts[key]
        _save_contacts(contacts)
        res = f"Contact '{name}' deleted."
        print_tool_result(res)
        return res

    res = f"Contact '{name}' not found."
    print_tool_result(res)
    return res

