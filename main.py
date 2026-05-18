import os
from dotenv import load_dotenv
from google import genai

def main():
    print("Hello from ai-agent-py!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY") 
    if api_key == None:
        raise RuntimeError("The GEMINI_API_KEY environment variable is not set. Please set it in the .env file.")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.5-flash",contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
    
    if response.usage_metadata == None:
        raise RuntimeError("The response does not contain usage metadata. The API request may have failed or the response format may have changed.")
    
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")        
    print(response.text)

if __name__ == "__main__":
    main()
