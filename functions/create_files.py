from pathlib import Path
import os
from google.genai import types

schema_create_files = types.FunctionDeclaration(
    name="write_file",
    description="Write contents to a specified file, automatically create path to the file if nonexistent relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path path to write contents to, relative to the working directory (default is the working directory itself)",
            ),
            "content" : types.Schema(
                type=types.Type.STRING,
                description="Contents that will be written to the file_path",
            )
        },
    ),
)


def _write_content(path:Path, content:str) -> None:
    os.makedirs(path.parent, exist_ok=True)
    with open(path, 'w+') as f:
        f.write(content)

def write_file(working_directory, file_path=".", content=""):
    try:
        working_directory = Path.cwd() / Path(working_directory)
        file_path = (working_directory / Path(file_path)).resolve()
               
        if file_path.is_dir():
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        common_path = Path(os.path.commonpath([file_path, working_directory]))
        if common_path != working_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        _write_content(file_path, content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        error = f"Error: Failed to write_content {e}"
        return error