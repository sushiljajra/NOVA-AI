import subprocess
import shutil
import os
import psutil
from typing import Dict, Any

def execute_shell_command(command: str) -> str:
    """
    Executes a PowerShell command on the Windows host and returns the output.
    Useful for system administration, checking configurations, running scripts, and managing services.
    """
    from nova.core.ui import print_tool_call, print_tool_result, print_warning, confirm_action
    from nova.core.safety import check_command_safety

    is_safe, warn_msg = check_command_safety(command)
    if not is_safe:
        print_warning(warn_msg)
        if not confirm_action(f"Execute shell command: '{command}'?"):
            return "Command execution cancelled by user for safety."

    print_tool_call("execute_shell_command", {"command": command})
    try:
        process = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
            capture_output=True,
            text=True,
            timeout=45
        )
        stdout = process.stdout.strip()
        stderr = process.stderr.strip()

        output = []
        if stdout:
            output.append(stdout)
        if stderr:
            output.append(f"[STDERR]\n{stderr}")
        if not output:
            output.append(f"Command executed successfully with exit code {process.returncode} (no output).")
        result_text = "\n".join(output)
        print_tool_result(result_text)
        return result_text
    except subprocess.TimeoutExpired:
        res = "Error: Command execution timed out after 45 seconds."
        print_tool_result(res)
        return res
    except Exception as e:
        res = f"Error executing command: {str(e)}"
        print_tool_result(res)
        return res

def get_system_vitals() -> Dict[str, Any]:
    """
    Retrieves real-time system performance statistics including CPU load, RAM usage,
    disk space, and battery status.
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("get_system_vitals", {})
    try:
        cpu_percent = psutil.cpu_percent(interval=0.5)
        cpu_count = psutil.cpu_count(logical=True)
        
        mem = psutil.virtual_memory()
        mem_total_gb = round(mem.total / (1024**3), 2)
        mem_used_gb = round(mem.used / (1024**3), 2)
        mem_percent = mem.percent
        
        disk = psutil.disk_usage(os.path.splitdrive(os.getcwd())[0] or "C:")
        disk_total_gb = round(disk.total / (1024**3), 2)
        disk_free_gb = round(disk.free / (1024**3), 2)
        disk_percent = disk.percent

        battery_info = "Desktop / No battery detected"
        if hasattr(psutil, "sensors_battery"):
            battery = psutil.sensors_battery()
            if battery:
                plugged = "Plugged in" if battery.power_plugged else "On battery"
                battery_info = f"{battery.percent}% ({plugged})"

        return {
            "cpu_percent": f"{cpu_percent}% ({cpu_count} logical cores)",
            "memory": f"{mem_used_gb} GB used / {mem_total_gb} GB total ({mem_percent}%)",
            "disk": f"{disk_free_gb} GB free / {disk_total_gb} GB total ({disk_percent}% used)",
            "battery": battery_info
        }
    except Exception as e:
        return {"error": f"Failed to retrieve system vitals: {str(e)}"}

def launch_application(target: str) -> str:
    """
    Launches an application, executable, or opens a file/folder in Windows.
    Examples: 'chrome', 'brave', 'notepad', 'calc', 'code', 'spotify', 'explorer .', or an absolute path.
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("launch_application", {"target": target})

    APP_SHORTCUTS = {
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        "brave browser": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
        "edge": "msedge",
        "calculator": "calc",
        "calc": "calc",
        "notepad": "notepad",
        "explorer": "explorer",
        "cmd": "cmd",
        "terminal": "wt",
        "powershell": "powershell"
    }

    resolved = APP_SHORTCUTS.get(target.lower().strip(), target)

    try:
        os.startfile(resolved)
        msg = f"Successfully launched '{target}'."
        print_tool_result(msg)
        return msg
    except Exception:
        try:
            cmd = f"Start-Process '{resolved}'"
            subprocess.Popen(["powershell.exe", "-NoProfile", "-Command", cmd], shell=False)
            msg = f"Dispatched launch command for '{target}' via PowerShell."
            print_tool_result(msg)
            return msg
        except Exception as e:
            err = f"Error: Could not locate or launch '{target}': {str(e)}"
            print_tool_result(err)
            return err

def list_running_processes(limit: int = 8) -> str:
    """
    Returns the top running processes sorted by memory consumption.
    """
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
            try:
                info = proc.info
                processes.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        processes.sort(key=lambda p: (p.get('memory_percent') or 0), reverse=True)
        top = processes[:limit]

        lines = [f"{'PID':<8} {'PROCESS NAME':<25} {'MEM %':<8} {'CPU %':<8}"]
        lines.append("-" * 55)
        for p in top:
            mem = f"{p.get('memory_percent', 0):.1f}%"
            cpu = f"{p.get('cpu_percent', 0):.1f}%"
            lines.append(f"{p.get('pid', ''):<8} {p.get('name', '')[:24]:<25} {mem:<8} {cpu:<8}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error listing processes: {str(e)}"

