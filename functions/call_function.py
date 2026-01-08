from google.genai import types
from functions.create_files import write_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
FUNCTION_MAP = {
    "get_file_content": get_file_content,
    "create_files" : write_file,
    "get_files_info" : get_files_info,
    "run_python_file" : run_python_file
    }
WORKING_DIR = "./calculator"

def call_function(function_call:types.FunctionCall, verbose=False):
    def print_start():
        if verbose:
            print(f"Calling function: {function_call.name}({function_call.args})")
        else:
            print(f" - Calling function: {function_call.name}")

    def get_error():
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(name=function_name,response={"error": f"Unknown function: {function_name}"})])

    def get_name():
        return function_call.name

    def get_args():
        return function_call.args.copy() if function_call.args is not None else {}
    
    def get_return_obj():
        return_obj = types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ]
        )
        return return_obj

    try:
        function_name = get_name()
        target_function_call = FUNCTION_MAP.get(function_name)
        args = get_args()
        function_result = target_function_call(WORKING_DIR, **args)
        print_start()
        return get_return_obj()
    except Exception as e:
        print(e)
        return get_error()

