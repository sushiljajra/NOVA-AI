import os
import smtplib
import urllib.parse
import webbrowser
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from nova.tools.system_tools import get_system_vitals
from nova.tools.reminder_tools import list_active_reminders
from nova.tools.web_tools import search_web

def send_email(to_email: str, subject: str, body: str) -> str:
    """
    Sends an email to a recipient.
    If SMTP credentials are provided in .env (SMTP_USER, SMTP_PASS), dispatches directly via SMTP.
    Otherwise, opens the user's default email client (Outlook/Thunderbird/Mail) with pre-filled fields.
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("send_email", {"to_email": to_email, "subject": subject})

    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_pass = os.getenv("SMTP_PASS", "")

    if smtp_user and smtp_pass:
        try:
            msg = MIMEMultipart()
            msg["From"] = smtp_user
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            server.quit()

            res = f"Email sent successfully to {to_email} via SMTP."
            print_tool_result(res)
            return res
        except Exception as e:
            res = f"Failed to send email via SMTP ({str(e)}). Falling back to desktop mail client..."
            print_tool_result(res)

    # Fallback to mailto link
    try:
        encoded_subj = urllib.parse.quote(subject)
        encoded_body = urllib.parse.quote(body)
        mailto_url = f"mailto:{to_email}?subject={encoded_subj}&body={encoded_body}"
        webbrowser.open(mailto_url)
        res = f"Opened email draft to {to_email} in your default email client with subject '{subject}'."
        print_tool_result(res)
        return res
    except Exception as e:
        err = f"Error opening email client: {str(e)}"
        print_tool_result(err)
        return err

def get_daily_briefing() -> str:
    """
    Compiles an executive daily briefing for the operator, including current date/time,
    battery and system status, pending alarms/reminders, and top global headlines.
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("get_daily_briefing", {})

    now = datetime.datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    time_str = now.strftime("%I:%M %p")

    # Vitals
    vitals = get_system_vitals()
    cpu = vitals.get("cpu_percent", "Normal")
    mem = vitals.get("memory", "Normal")
    battery = vitals.get("battery", "Plugged in")

    # Reminders
    reminders = list_active_reminders()

    # News
    news = search_web("top global news today", max_results=3)

    report = f"""
### Executive Briefing - {date_str} ({time_str})

* **System Status:**
  - Battery: {battery}
  - CPU Load: {cpu}
  - Memory: {mem}

* **Pending Reminders & Tasks:**
{reminders}

* **World Headlines:**
{news}
"""
    print_tool_result("Briefing compiled successfully.")
    return report.strip()

