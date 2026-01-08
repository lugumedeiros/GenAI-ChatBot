# Resources ##########################################
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types as gentypes
import prompts
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_files_content
from functions.create_files import schema_create_files
from functions.run_python import schema_run_python_file
from  functions.call_function import call_function

load_dotenv()

def get_genai_key() -> str:
    genai_key = os.environ.get("GEMINI_API_KEY")
    if genai_key is None:
        raise RuntimeError("genai api key not found in env")
    return genai_key

def get_genai_client() -> genai.Client:
    genai_client = genai.Client(api_key=get_genai_key())
    return genai_client

# ArgParser ##########################################
import argparse
_parser = argparse.ArgumentParser(description="GEN-AI Chatbot")
_parser.add_argument("user_prompt", type=str, help="User prompt")
_parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

def get_parser_args() -> argparse.Namespace:
    return _parser.parse_args()

######################################################

MODEL = "gemini-2.5-flash"
available_functions = gentypes.Tool(
    function_declarations=[schema_get_files_info, schema_run_python_file, schema_get_files_content, schema_create_files],
)

def print_genai(response:gentypes.GenerateContentResponse, verbose=True):
    p_tokens = response.usage_metadata.prompt_token_count
    r_tokens = response.usage_metadata.candidates_token_count
    response_str = response.text
    output = ""
    if verbose:
        output += f"Prompt tokens: {p_tokens}\n" \
        f"Response tokens: {r_tokens}\n" \
        
    if r_tokens is None:
        raise RuntimeError("genai request failed, no response token used")
    
    if response.function_calls is not None and len(response.function_calls) > 0:
        for function in response.function_calls:
            output += f"Calling function: {function.name}({function.args})\n"
    else:
        output += f"Response: {response_str}"
    print(output)

def main():
    def raise_if_response_invalid(fcr:gentypes.Content):
        if (
            fcr is None
            or fcr.parts is None
            or not fcr.parts
            or fcr.parts[0] is None
            or fcr.parts[0].function_response is None
            or fcr.parts[0].function_response.response is None
        ):
            raise Exception("a part is none")
        
    def add_messages_from_response(messages, response):
        messages.append(
            gentypes.Content(
                role="model",
                parts=response.candidates[0].content.parts
            )
        )
        return messages

    parser_args = get_parser_args()
    messages = [gentypes.Content(role="user", parts=[gentypes.Part(text=parser_args.user_prompt)])]
    client = get_genai_client()
    response = None
    ## CALL 

    for _ in range(3):
        response = client.models.generate_content(
            model=MODEL,
            contents=messages,
            config=gentypes.GenerateContentConfig(
                system_instruction=prompts.system_prompt,
                tools=[available_functions]
                )
            )

        if response.function_calls is None:
            print("END")
            exit(0)
        
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=parser_args.verbose)
            raise_if_response_invalid(function_call_result)
            print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(function_call_result)
        
        # Add for next iteration
        messages = add_messages_from_response(messages, response)
    sys.exit(1)

if __name__ == "__main__":
        main()
