import subprocess
import os

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:

    working_dir_abs_path = os.path.abspath(working_directory)
    full_path_target_dir = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs_path,full_path_target_dir]) == working_dir_abs_path

    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_path_target_dir):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", full_path_target_dir]

    if args:
        command.extend(args)

    # Use the subprocess.run() function to run the command that you built. This will return a CompletedProcess object, which you'll want to assign to a variable. Also, when calling subprocess.run(), make sure to provide the necessary arguments to:
    # Set the working directory properly.
    # Capture output (i.e., stdout and stderr).
    # Decode the output to strings, rather than bytes; this is done by setting text=True.
    # Set a timeout of 30 seconds to prevent infinite execution.
    # Build an output string based on the CompletedProcess object:
    # If the process exited with a non-zero returncode, include "Process exited with code X".
    # If both stdout and stderr contained no output (both of which are attributes of CompletedProcess), add "No output produced".
    # Otherwise, include any text in stdout prefixed with STDOUT:, and any text in stderr prefixed with STDERR:.
    # Return the output string.
    try:
        result = subprocess.run(command, cwd=working_dir_abs_path, capture_output=True, text=True, timeout=30)
        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        if not result.stdout and not result.stderr:
            output += "No output produced"
        else:
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}\n"
            if result.stderr:
                output += f"STDERR:\n{result.stderr}\n"
        return output.strip()
    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error: {str(e)}"
