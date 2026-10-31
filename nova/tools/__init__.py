from .system_tools import execute_shell_command, get_system_vitals, launch_application, list_running_processes
from .file_tools import list_directory, read_text_file, write_text_file, find_files
from .web_tools import search_web, open_browser
from .contact_tools import save_contact, get_contact, list_contacts, delete_contact
from .whatsapp_tools import send_whatsapp_message
from .gui_tools import press_hotkey, type_text, click_mouse, scroll_screen, take_screenshot, get_clipboard, set_clipboard
from .media_tools import control_media, play_on_youtube
from .vision_tools import analyze_screen, click_ui_element
from .reminder_tools import set_timer, set_reminder, list_active_reminders
from .memory_tools import remember_fact, recall_fact, list_all_memories, delete_memory
from .email_tools import send_email, get_daily_briefing
from .window_tools import list_open_windows, focus_window, minimize_window, maximize_window, close_window, snap_window
from .protocol_tools import execute_protocol, create_protocol, list_protocols
from .code_tools import execute_python_code

AVAILABLE_TOOLS = [
    # System & Telemetry
    execute_shell_command,
    get_system_vitals,
    launch_application,
    list_running_processes,
    
    # Filesystem
    list_directory,
    read_text_file,
    write_text_file,
    find_files,
    
    # Web & Media
    search_web,
    open_browser,
    play_on_youtube,
    control_media,
    
    # WhatsApp & Contacts
    save_contact,
    get_contact,
    list_contacts,
    delete_contact,
    send_whatsapp_message,
    
    # GUI & Screen Control
    press_hotkey,
    type_text,
    click_mouse,
    scroll_screen,
    take_screenshot,
    get_clipboard,
    set_clipboard,

    # Multimodal Vision & Visual Grounding (Phase 3)
    analyze_screen,
    click_ui_element,

    # Window Management (Phase 3)
    list_open_windows,
    focus_window,
    minimize_window,
    maximize_window,
    close_window,
    snap_window,

    # Alarms, Timers & Reminders
    set_timer,
    set_reminder,
    list_active_reminders,

    # Long-term Memory
    remember_fact,
    recall_fact,
    list_all_memories,
    delete_memory,

    # Email & Executive Briefing
    send_email,
    get_daily_briefing,

    # Autonomous Protocols & Code Sandbox (Phase 4)
    execute_protocol,
    create_protocol,
    list_protocols,
    execute_python_code
]

TOOL_MAP = {func.__name__: func for func in AVAILABLE_TOOLS}

