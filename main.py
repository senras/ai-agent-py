import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():

    #Load API key
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY") 
    if api_key == None:
        raise RuntimeError("The GEMINI_API_KEY environment variable is not set. Please set it in the .env file.")
    client = genai.Client(api_key=api_key)

    #Args parser
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]


    for _ in range(20):
        #Making Gemini request
        response = client.models.generate_content(model="gemini-2.5-flash",contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
        
        if response.candidates != None:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.usage_metadata == None:
            raise RuntimeError("The response does not contain usage metadata. The API request may have failed or the response format may have changed.")
    
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")    
            
        function_responses = []
        if not response.function_calls:
            print(response.text)
            return
        else:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)
                if not function_call_result.parts:
                    raise Exception("The function call result does not contain any parts. The function may have failed to execute properly.")
                if function_call_result.parts[0].function_response == None:
                    raise Exception("The function call result part does not contain a function response. The function may have failed to execute properly.")
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("The function response does not contain a response field. The function may have failed to execute properly.")
                function_responses.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_responses))

    print("The conversation has reached the maximum number of turns. Ending the conversation.")
    sys.exit(1)        



if __name__ == "__main__":
    main()
