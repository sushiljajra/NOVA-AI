import os
import glob
from pathlib import Path
from typing import List, Dict, Any

def list_directory(path: str = ".") -> str:
    """
    Lists files and directories in the specified path with file size and type.
    """
    target = Path(path).resolve()
    if not target.exists():
        return f"Error: Path '{path}' does not exist."
    if not target.is_dir():
        return f"Error: Path '{path}' is not a directory."

    items = []
    try:
        for entry in os.scandir(target):
            entry_type = "[DIR] " if entry.is_dir() else "[FILE]"
            size = f"{entry.stat().st_size / 1024:.1f} KB" if entry.is_file() else "-"
            items.append(f"{entry_type:<7} {entry.name:<35} {size:>10}")
        
        header = f"Contents of {target}:\n" + f"{'TYPE':<7} {'NAME':<35} {'SIZE':>10}\n" + "-" * 55
        return header + "\n" + "\n".join(items) if items else f"Directory {target} is empty."
    except Exception as e:
        return f"Error reading directory: {str(e)}"

def read_text_file(path: str, max_lines: int = 150) -> str:
    """
    Reads and returns the contents of a text file (up to max_lines).
    """
    file_path = Path(path).resolve()
    if not file_path.exists():
        return f"Error: File '{path}' does not exist."
    if not file_path.is_file():
        return f"Error: Path '{path}' is not a regular file."

    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            lines = [f.readline() for _ in range(max_lines)]
            content = "".join(lines)
            if f.readline():
                content += f"\n... [Output truncated at {max_lines} lines]"
            return content
    except Exception as e:
        return f"Error reading file '{path}': {str(e)}"

def write_text_file(path: str, content: str, mode: str = "w") -> str:
    """
    Writes or appends text content to a file. Mode can be 'w' (overwrite) or 'a' (append).
    """
    file_path = Path(path).resolve()
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, mode, encoding="utf-8") as f:
            f.write(content)
        action = "appended to" if mode == "a" else "written to"
        return f"Successfully {action} '{path}' ({len(content)} characters)."
    except Exception as e:
        return f"Error writing to file '{path}': {str(e)}"

def find_files(pattern: str, search_dir: str = ".") -> str:
    """
    Finds files matching a glob pattern (e.g. '*.py', '*.pdf', '*report*') in search_dir.
    """
    try:
        root = Path(search_dir).resolve()
        matches = list(root.glob(pattern))
        if not matches:
            # Also try recursive search if not already recursive
            if not pattern.startswith("**/"):
                matches = list(root.glob(f"**/{pattern}"))
        
        if not matches:
            return f"No files matching '{pattern}' found in {root}."
        
        result_lines = [f"Found {len(matches)} match(es) for '{pattern}':"]
        for p in matches[:30]:
            result_lines.append(f" - {p}")
        if len(matches) > 30:
            result_lines.append(f" ... and {len(matches) - 30} more.")
        return "\n".join(result_lines)
    except Exception as e:
        return f"Error searching for files: {str(e)}"

