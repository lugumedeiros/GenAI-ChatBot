import os
from pathlib import Path
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def _get_info_from_dir(path:Path) -> str:
    response = ""
    for entry in path.iterdir():
        name = entry.name
        size = entry.stat().st_size
        response += f"- {name}: file_size={size} bytes, is_dir={entry.is_dir()}\n"
    return response.rstrip()

def get_files_info(working_directory, directory=".") -> str:
    try:
        working_directory = Path.cwd() / Path(working_directory)
        directory = (working_directory / Path(directory)).resolve()
        if not directory.exists():
            return f'Error: "{directory}" is not a directory'
        
        common_path = Path(os.path.commonpath([directory, working_directory]))
        if common_path != working_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        return _get_info_from_dir(directory)
    except:
        return "Error: Failed to get_info"

if __name__ == "__main__":
    x = get_files_info("calculator", "calculator/ruh")