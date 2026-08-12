import os
import sys
import argparse
import subprocess
from dotenv import load_dotenv
from mistralai.client import Mistral
import shlex

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY2")

if not api_key:
    print("Error: MISTRAL_API_KEY2 not found in your environment variables (.env file).")
    sys.exit(1)

client = Mistral(api_key=api_key)

def call_mistral(system_prompt, user_content):
    """Helper function to send data to Mistral AI."""
    try:
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
        )
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error communicating with Mistral AI: {e}")
        sys.exit(1)


system_prompt = (
)

user_content = 

ai_output = call_mistral(system_prompt, user_content)