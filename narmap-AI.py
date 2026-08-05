import os
from dotenv import load_dotenv
from mistralai.client import Mistral
import subprocess
import shlex
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("target")
args = parser.parse_args()

raw_command = f"sudo nmap -sC -sV -Pn --open {args.target}"
print("~" * 40)
print(f"using the recommended nmap command flags: {raw_command}")
change = input("would you want to add or change any flags? (y/n): ")

if change == "y" or change == "":
    change_what = input("type add [flag] or rm [flag] to make your changes: ")
    parts = change_what.split()

    if parts[0] == "add":
        flag = parts[1]
        raw_command = raw_command.replace(f"{args.target}", f"{flag} {args.target}")

    elif parts[0] == "rm":
        flag = parts[1]
        raw_command = raw_command.replace(f"{flag} ", "")

print(f"final command: {raw_command}")

arguments = shlex.split(raw_command)

print("running nmap...")
result = subprocess.run(arguments, capture_output=True, text=True)

print("loading API key...")
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

print("sending API request...")
client = Mistral(api_key=api_key)

print("getting AI response...")
response = client.chat.complete(
    model="mistral-large-latest",
    messages=[
        {
            "role": "system",
            "content": '''You are a network recon assistant. You will receive raw nmap scan output.
            Summarize what was found in plain language: which ports are open, what service/version
            runs on each, and anything notable (default creds, outdated versions, anonymous access, weak configs).
            Then suggest concrete next steps for each finding. Format your response as a short plain list,
            no markdown headers, no bold text, no long explanations. For each finding use this exact style:
            Port <number> <state> - <service>
            Next step: <one short actionable line, like a command to run or link to try>
            Keep it terminal-friendly and brief.'''
        },
        {
            "role": "user",
            "content": f"{result.stdout}",
        }
    ],
)

print("")
print("AI OUTPUT RESPONSE")
print(response.choices[0].message.content)