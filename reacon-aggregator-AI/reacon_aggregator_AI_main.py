from mistralai.client import Mistral
from dotenv import load_dotenv
import os
import sys
import argparse

print("loading API key...")
load_dotenv()
print("obtaining API key with dotenv")
api_key = os.getenv("MISTRAL_API_KEY2")
print("successfuly finished loading API key")
print("cleaning screen...")
os.system("cls" if os.name == "nt" else "cln")

if not api_key:
    print("Error: MISTRAL_API_KEY2 not found in your environment variables (.env file).")
    sys.exit(1)

print("starting client session...")
client = Mistral(api_key=api_key)

def call_mistral(system_prompt, user_content):
    """Helper function to send data to Mistral AI."""
    try:
        print("AI proccessing request...")
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
        )
        print("AI finished proccessing request")
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error communicating with Mistral AI: {e}")
        sys.exit(1)
        
recon_aggregator_system_prompt = (
    '''You are a recon aggregation analyst reviewing raw output from multiple pentesting tools, run against the same target during an authorized engagement.

    The input contains multiple tool outputs, each wrapped in its own section like:
    ---------toolname start---------
    ...raw output...
    ---------toolname end---------

    Your job: cross-reference all sections together and produce ONE prioritized attack-surface summary.

    Rules:
    - Identify the target's real attack surface: open ports/services, discovered directories/endpoints, technologies/versions detected, and any findings that connect across multiple tools (e.g. a port nmap found running a service that gobuster then found an admin panel for).
    - Prioritize findings by how promising they are for further exploitation, most promising first.
    - Explicitly call out connections between tools' findings, don't just list each tool's results separately, actually synthesize them.
    - If a version number is mentioned anywhere, flag it if it corresponds to a well-known CVE.
    - Keep the response concise and actionable, a real pentester should be able to read it and know exactly what to try next.
    - If a tool's section is empty or shows no results, note that briefly rather than ignoring it.'''
    )

parser = argparse.ArgumentParser()
parser.add_argument("--input-file", required=True)
args = parser.parse_args()

raw_output = ""
with open(args.input_file, "r", encoding="utf-8") as f:
    raw_output = f.read()

ai_output = call_mistral(recon_aggregator_system_prompt, raw_output)

print("-----------AI OUTPUT-----------\n")
print(ai_output)