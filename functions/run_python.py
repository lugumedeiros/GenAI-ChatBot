from pathlib import Path
import os
import subprocess
from config import *

def _run_python(path:Path, args):
    command = ["python", path.absolute()]
    if args is not None:
        command += list(args)
    
    proccess = subprocess.run(command, timeout=PROCCESS_TIMEOUT, capture_output=True)
    response = ""
    if proccess.returncode != 0:
        response = "Process exited with code X: "
    
    if not proccess.stderr and not proccess.stdout:
        response += "No output produced"
    if proccess.stderr:
        response += f"STDERR: {proccess.stderr.decode()} "
    if proccess.stdout:
        response += f"STDOUT: {proccess.stdout.decode()} "
    return response


def run_python_file(working_directory, file_path, args=None):
    file_path_input = file_path
    try:
        working_directory = Path.cwd() / Path(working_directory)
        file_path = (working_directory / Path(file_path)).resolve()
        
        if not file_path.exists() or not file_path.is_file():
            return f'Error: "{file_path_input}" does not exist or is not a regular file'
        
        if not file_path.suffix == ".py":
            return f'Error: "{file_path_input}" is not a Python file'
                
        common_path = Path(os.path.commonpath([file_path, working_directory]))
        if common_path != working_directory:
            return f'Error: Cannot execute "{file_path_input}" as it is outside the permitted working directory'
        
        return _run_python(file_path, args)
    except Exception as e:
        return f"Error: executing Python file: {e}"