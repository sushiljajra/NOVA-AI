import re

DANGEROUS_PATTERNS = [
    r"rmdir\s+/[sS]",
    r"Remove-Item\s+.*-Recurse",
    r"format\s+[a-zA-Z]:",
    r"diskpart",
    r"reg\s+delete",
    r"del\s+/[fF]\s+/[sS]\s+/[qQ]",
    r":\(\)\s*\{\s*:\|:&\s*\};:",  # fork bomb
    r"shutdown\s+/[sS]",
    r"Stop-Computer",
    r"Clear-Disk",
]

def check_command_safety(command: str) -> tuple[bool, str]:
    """
    Checks if a command contains potentially destructive operations.
    Returns (is_safe, warning_message).
    """
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return False, f"Potentially destructive command detected: matches pattern '{pattern}'"
    return True, ""

