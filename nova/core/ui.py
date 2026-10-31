import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.table import Table

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

console = Console()

BANNER = """
 ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗ 
 ████╗  ██║██╔═══██╗██║   ██║██╔══██╗
 ██╔██╗ ██║██║   ██║██║   ██║███████║
 ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║
 ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║
 ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝
       [Autonomous Desktop Assistant]
"""

def print_banner():
    banner_text = Text(BANNER, style="bold cyan")
    console.print(Panel(banner_text, border_style="bright_blue", title="[bold cyan]PROJECT NOVA[/bold cyan]", subtitle="[dim cyan]N.O.V.A. OS Interface[/dim cyan]"))

def print_status(provider: str, model: str, user_name: str):
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_row("[bold cyan]Protocol:[/bold cyan]", "[green]Online & Operational[/green]")
    table.add_row("[bold cyan]Operator:[/bold cyan]", f"[bold white]{user_name}[/bold white]")
    table.add_row("[bold cyan]Core Engine:[/bold cyan]", f"[cyan]{provider.upper()}[/cyan] ({model})")
    table.add_row("[bold cyan]Subsystems:[/bold cyan]", "[green]45 Subsystems (Hands, Vision, Voice, Protocols)[/green]")
    
    console.print(Panel(table, border_style="cyan", title="[bold cyan]System Initialization[/bold cyan]"))

def print_jarvis_response(message: str):
    console.print()
    console.print(Panel(Markdown(message), title="[bold cyan]N.O.V.A.[/bold cyan]", border_style="bright_blue"))

def print_tool_call(tool_name: str, args: dict):
    args_str = ", ".join(f"{k}='{v}'" for k, v in args.items()) if args else ""
    console.print(f"[bold cyan][*] Action:[/bold cyan] [yellow]{tool_name}[/yellow]([dim]{args_str}[/dim])")
    try:
        from nova.core.dynamic_island import island
        island.show_thinking(f"⚡ {tool_name}")
    except Exception:
        pass

def print_tool_result(result: str):
    preview = result.strip()
    if len(preview) > 300:
        preview = preview[:300] + "... [truncated]"
    console.print(f"[dim green]  -> Result:[/dim green] [dim]{preview}[/dim]")

def print_warning(message: str):
    console.print(f"[bold red][!] Notice:[/bold red] {message}")

def confirm_action(prompt_text: str) -> bool:
    console.print(f"[bold yellow][SAFETY] Protocol:[/bold yellow] {prompt_text}")
    res = console.input("[bold yellow]Authorize execution? (y/N): [/bold yellow]").strip().lower()
    return res in ("y", "yes")

