#!/usr/bin/env python3
import subprocess

def run_command(command: str, timeout: int = 60) -> dict:
    """
    Runs a shell command and returns structured result.
    Other modules import and call this function directly.
    """
    if not command or not command.strip():
        return {
            "success": False,
            "stdout": "",
            "stderr": "Command cannot be empty.",
            "exit_code": 1
        }

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout      # Critical for pentesting — tools can hang forever
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds.",
            "exit_code": -1
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1
        }


# This block only runs when you execute the file directly
# When imported by orchestrator — this block is ignored
if __name__ == "__main__":
    command = input("Enter command: ")
    output = run_command(command)

    if output["success"]:
        print(output["stdout"], end="")
    else:
        print(f"Error (exit code {output['exit_code']}): {output['stderr']}")

























