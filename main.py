# Resources ##########################################
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types as gentypes

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

def get_parser_args() -> argparse.Namespace:
    return _parser.parse_args()

######################################################

MODEL = "gemini-2.5-flash"

def print_genai(response:gentypes.GenerateContentResponse):
    p_tokens = response.usage_metadata.prompt_token_count
    r_tokens = response.usage_metadata.candidates_token_count
    response_str = response.text
    if r_tokens is None:
        raise RuntimeError("genai request failed, no response token used")
    output = f"Prompt tokens: {p_tokens}\n" \
        f"Response tokens: {r_tokens}\n" \
        f"{response_str}"
    print(output)

def main():
    print("Hello from aiagent!")
    parser_args = get_parser_args()
    messages = [gentypes.Content(role="user", parts=[gentypes.Part(text=parser_args.user_prompt)])]
    client = get_genai_client()
    response = client.models.generate_content(model=MODEL, contents=messages)
    print_genai(response)

if __name__ == "__main__":
    main()
