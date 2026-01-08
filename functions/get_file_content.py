from pathlib import Path
import os
from config import MAX_CHARS_CONTENT
from google.genai import types

schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get file contents from the specified file path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path path to get contents from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def _get_contents(path:Path) -> str:
    contents = ""
    with open(path, "r") as f:
        contents = f.read(MAX_CHARS_CONTENT)
        if f.read(1):
            contents += f'[...File "{path}" truncated at {MAX_CHARS_CONTENT} characters]'
    return contents

def get_file_content(working_directory, file_path="."):
    try:
        working_directory = Path.cwd() / Path(working_directory)
        file_path = (working_directory / Path(file_path)).resolve()
        
        if not file_path.exists() or not file_path.is_file():
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        common_path = Path(os.path.commonpath([file_path, working_directory]))
        if common_path != working_directory:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        return _get_contents(file_path)
    except:
        return "Error: Failed to get_content"