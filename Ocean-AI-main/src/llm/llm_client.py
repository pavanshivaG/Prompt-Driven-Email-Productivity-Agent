import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("API Key not found. Please set OPENAI_API_KEY in .env file.")

        # Initialize the OpenAI Client
        self.client = OpenAI(api_key=self.api_key)
        
        # "gpt-4o-mini" is perfect for students: Smarter than 3.5, cheaper than 4o
        self.model = "gpt-4o-mini" 

    def generate_response(self, prompt, temperature=0.7):
        """
        Generates a plain text response. 
        Used for: Drafting emails, Summaries, General Chat.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful email productivity assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM Error: {e}")
            return "Error: The AI Agent encountered an issue connecting to the server."

    def generate_structured_response(self, prompt):
        """
        Generates a JSON response using OpenAI's 'JSON Mode'.
        This is a 'Rank 1' feature because it guarantees the code won't crash.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data extraction assistant. Output strictly valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0, # Keep it deterministic
                response_format={"type": "json_object"} # THE SECRET WEAPON: Forces valid JSON
            )
            
            raw_content = response.choices[0].message.content
            return json.loads(raw_content)

        except json.JSONDecodeError:
            print("Failed to decode JSON.")
            return {}
        except Exception as e:
            print(f"LLM Error: {e}")
            return {}

# Simple test block
if __name__ == "__main__":
    client = LLMClient()
    print("Testing OpenAI connection...")
    print(client.generate_response("Say 'System Operational'"))