import sys
import subprocess
import tempfile
from pathlib import Path

def execute_python_code(code: str, timeout: int = 30) -> str:
    """
    Executes arbitrary Python code in a standalone subprocess and returns the output.
    Useful for data processing, calculations, file transformations, or generating scripts on the fly.
    Example: execute_python_code(code="import math; print([math.factorial(i) for i in range(1, 10)])")
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("execute_python_code", {"code": code[:60] + "..." if len(code) > 60 else code})

    temp_py = Path(tempfile.gettempdir()) / f"eclipse_script_{int(sys.time() if hasattr(sys, 'time') else 1000)}.py"
    try:
        with open(temp_py, "w", encoding="utf-8") as f:
            f.write(code)

        proc = subprocess.run(
            [sys.executable, str(temp_py)],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()

        output = []
        if stdout:
            output.append(stdout)
        if stderr:
            output.append(f"[STDERR]\n{stderr}")
        if not output:
            output.append(f"Script executed successfully (exit code {proc.returncode}, no output).")

        res = "\n".join(output)
        print_tool_result(res)
        return res
    except subprocess.TimeoutExpired:
        res = f"Script execution timed out after {timeout} seconds."
        print_tool_result(res)
        return res
    except Exception as e:
        err = f"Error executing Python code: {str(e)}"
        print_tool_result(err)
        return err
    finally:
        if temp_py.exists():
            try:
                temp_py.unlink()
            except Exception:
                pass

