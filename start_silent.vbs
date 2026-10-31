Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "D:\Projects\Eclipse"
WshShell.Run """D:\Projects\Eclipse\.venv\Scripts\pythonw.exe"" run_nova.py --wake", 0, False
