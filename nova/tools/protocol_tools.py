import json
import time
from pathlib import Path
from typing import Dict, Any, List

PROTOCOLS_FILE = Path(__file__).resolve().parent.parent.parent / "protocols.json"

DEFAULT_PROTOCOLS = {
    "dev": {
        "description": "Developer Environment: Launches editor, GitHub, and background focus music.",
        "steps": [
            {"tool": "launch_application", "args": {"target": "code"}},
            {"tool": "open_browser", "args": {"url": "https://github.com"}},
            {"tool": "play_on_youtube", "args": {"query": "lofi hip hop study beats"}}
        ]
    },
    "maintenance": {
        "description": "System Diagnostic & Clean: Purges temp caches and inspects CPU/RAM vitals.",
        "steps": [
            {"tool": "get_system_vitals", "args": {}},
            {"tool": "list_running_processes", "args": {"limit": 5}},
            {"tool": "execute_shell_command", "args": {"command": "Remove-Item -Path $env:TEMP\\* -Recurse -Force -ErrorAction SilentlyContinue; Write-Output 'Temporary files purged successfully.'"}}
        ]
    },
    "focus": {
        "description": "Deep Work Focus Block: Sets volume and arms a 45-minute Pomodoro timer.",
        "steps": [
            {"tool": "control_media", "args": {"action": "volume_down", "steps": 4}},
            {"tool": "set_timer", "args": {"minutes": 45, "label": "Pomodoro Focus Block Finished"}}
        ]
    },
    "night": {
        "description": "Standby Night Mode: Lowers master audio and checks pending reminders.",
        "steps": [
            {"tool": "control_media", "args": {"action": "volume_down", "steps": 8}},
            {"tool": "list_active_reminders", "args": {}}
        ]
    }
}

def _load_protocols() -> Dict[str, Any]:
    if not PROTOCOLS_FILE.exists():
        _save_protocols(DEFAULT_PROTOCOLS)
        return DEFAULT_PROTOCOLS
    try:
        with open(PROTOCOLS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_PROTOCOLS

def _save_protocols(data: Dict[str, Any]):
    with open(PROTOCOLS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def execute_protocol(protocol_name: str) -> str:
    """
    Executes a pre-configured multi-step autonomous protocol (e.g., 'dev', 'maintenance', 'focus', 'night').
    Runs all sequenced subsystem actions in order.
    Example: execute_protocol(protocol_name="maintenance")
    """
    from nova.core.ui import print_tool_call, print_tool_result
    from nova.tools import TOOL_MAP
    print_tool_call("execute_protocol", {"protocol_name": protocol_name})

    protocols = _load_protocols()
    key = protocol_name.strip().lower()

    if key not in protocols:
        available = ", ".join(protocols.keys())
        res = f"Protocol '{protocol_name}' not found. Available protocols: {available}"
        print_tool_result(res)
        return res

    proto = protocols[key]
    steps = proto.get("steps", [])
    desc = proto.get("description", "")

    outputs = [f"Initiating Protocol '{key.upper()}': {desc}"]

    for idx, step in enumerate(steps, 1):
        tool_name = step.get("tool", "")
        args = step.get("args", {})
        if tool_name in TOOL_MAP:
            try:
                fn = TOOL_MAP[tool_name]
                result = fn(**args)
                outputs.append(f"Step {idx} [{tool_name}]: {str(result)[:120]}")
            except Exception as e:
                outputs.append(f"Step {idx} [{tool_name}] Warning: {str(e)}")
        else:
            outputs.append(f"Step {idx} Error: Tool '{tool_name}' not recognized.")
        time.sleep(0.5)

    outputs.append(f"Protocol '{key.upper()}' execution completed.")
    full_res = "\n".join(outputs)
    print_tool_result(full_res)
    return full_res

def create_protocol(name: str, description: str, steps_json: str) -> str:
    """
    Creates and saves a new custom autonomous protocol to ECLIPSE's memory.
    steps_json must be a JSON array of actions: [{"tool": "tool_name", "args": {"param": "value"}}]
    Example: create_protocol(name="gaming", description="Launches game and maxes volume", steps_json='[{"tool": "control_media", "args": {"action": "volume_up", "steps": 5}}]')
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("create_protocol", {"name": name, "description": description})

    try:
        parsed_steps = json.loads(steps_json)
        if not isinstance(parsed_steps, list):
            res = "Error: steps_json must be a JSON array of step objects."
            print_tool_result(res)
            return res

        protocols = _load_protocols()
        clean_name = name.strip().lower().replace(" ", "_")
        protocols[clean_name] = {
            "description": description.strip(),
            "steps": parsed_steps
        }
        _save_protocols(protocols)
        res = f"Successfully registered new autonomous Protocol '{clean_name.upper()}': {description} ({len(parsed_steps)} steps)."
        print_tool_result(res)
        return res
    except Exception as e:
        err = f"Failed to parse or create protocol: {str(e)}"
        print_tool_result(err)
        return err

def list_protocols() -> str:
    """
    Lists all saved autonomous protocols available in ECLIPSE.
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("list_protocols", {})

    protocols = _load_protocols()
    if not protocols:
        res = "No protocols currently registered."
        print_tool_result(res)
        return res

    lines = [f"{'PROTOCOL':<18} {'STEPS':<8} {'DESCRIPTION'}"]
    lines.append("-" * 75)
    for k, v in protocols.items():
        step_count = len(v.get("steps", []))
        lines.append(f"{k.upper():<18} {step_count:<8} {v.get('description', '')}")
    res = "\n".join(lines)
    print_tool_result(res)
    return res

