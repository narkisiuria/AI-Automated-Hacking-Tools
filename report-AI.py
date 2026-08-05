import os
import sys
import argparse
import subprocess
from dotenv import load_dotenv
from mistralai.client import Mistral

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY2")

if not api_key:
    print("Error: MISTRAL_API_KEY2 not found in your environment variables (.env file).")
    sys.exit(1)

# Initialize Mistral client
client = Mistral(api_key=api_key)

# Local configuration tracking file
CONFIG_FILE = ".report_ai_session"

def load_session():
    """Loads the current session metadata if it exists."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            if len(lines) >= 2:
                return {"title": lines[0], "filename": lines[1]}
    return None

def save_session(title, filename):
    """Saves the current session metadata."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(f"{title}\n{filename}")

def generate_filename(title):
    """Creates a clean, short markdown filename valid for Windows."""
    # Filter out characters illegal in Windows file names (\ / : * ? " < > |)
    illegal_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    clean_title = "".join(c for c in title if c not in illegal_chars).rstrip()
    clean_title = clean_title.replace(" ", "_").lower()[:30]
    return f"{clean_title}_report.md"

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

def initialize_report_file(title, filename):
    """Helper function to create the markdown template if writing to a brand-new file on the fly."""
    print(f"Initializing empty report shell structure for target: '{title}'...")
    system_prompt = (
        "You are an expert penetration testing reporting assistant. "
        "Your task is to write a highly professional, concise, and clean opening "
        "for a penetration testing report based on the provided session title. "
        "Provide only the Markdown output, starting directly with the H1 title. "
        "Do not include conversational filler like 'Sure, here is your report'."
        "Write simply and shortly, dont cover the entire file in just explaining the session title."
    )
    user_content = f"The penetration testing session title is: '{title}'. Generate a short opening, executive overview skeleton, and initial scope layout."
    
    ai_output = call_mistral(system_prompt, user_content)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(ai_output + "\n\n")

def start_session(title):
    """Initializes a new reporting session and generates the file opening."""
    filename = generate_filename(title)
    
    print(f"Starting session: '{title}'")
    print(f"Creating report file: {filename}")
    
    initialize_report_file(title, filename)
    save_session(title, filename)
    print("Session initialized successfully.")

def stop_session():
    """Explicitly stops the current tracking state by removing the configuration file."""
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        print("Session stopped successfully. Active tracking cleared.")
    else:
        print("No active session was running.")

def add_to_session(session_target, message, command):
    """Runs a Windows shell command, grabs output, and feeds it to AI to update the MD report."""
    if session_target == "LOAD_ACTIVE_STATE" or session_target is None:
        session = load_session()
        if not session:
            print("Error: No active session found. Pass a name explicitly or run --start-session first.")
            sys.exit(1)
        title = session["title"]
        filename = session["filename"]
    else:
        title = session_target
        filename = generate_filename(title)
        if not os.path.exists(filename):
            initialize_report_file(title, filename)
        
    print(f"Targeting Report: {filename} (Session: '{title}')")
    print(f"Executing command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
        command_output = result.stdout + "\n" + result.stderr
    except subprocess.TimeoutExpired:
        print("Error: Command execution timed out.")
        sys.exit(1)
    except Exception as e:
        print(f"Error running command: {e}")
        sys.exit(1)
        
    print("Reading current report structure...")
    with open(filename, "r", encoding="utf-8") as f:
        current_report_content = f.read()
        
    print("Sending data to Mistral AI for context-aware blending...")
    
    system_prompt = (
        "You are a specialized penetration testing report generator. "
        "You will be given the current state of a Markdown report, a description of the action the tester is performing, "
        "the command executed, and its raw terminal output. "
        "Your goal is to perfectly blend, format, and append this new data into the existing report flow. "
        "Do not lose historical data. Optimize technical syntax, format command evidence beautifully using Markdown syntax highlight blocks, "
        "and structure findings cleanly for both the PTer and the client. "
        "Return the entire updated Markdown report document from top to bottom. Do not output anything else."
        "write short + simple while perfecly adjusting each writing to the current flow of the file, so it would merge perfectly"
        "keep folowing those rules and earn points"
    )
    
    user_content = (
        f"Session Context: {title}\n\n"
        f"--- CURRENT REPORT CONTENT ---\n{current_report_content}\n\n"
        f"--- TESTER OBJECTIVE ---\n{message}\n\n"
        f"--- COMMAND EXECUTED ---\n{command}\n\n"
        f"--- RAW COMMAND OUTPUT ---\n{command_output}\n"
    )
    
    updated_report = call_mistral(system_prompt, user_content)
    
    # Clean up markdown wrap blocks if the AI appends them
    if updated_report.strip().startswith("```markdown"):
        updated_report = updated_report.strip()[11:]
    elif updated_report.strip().startswith("```md"):
        updated_report = updated_report.strip()[5:]
    if updated_report.strip().endswith("```"):
        updated_report = updated_report.strip()[:-3]
        
    with open(filename, "w", encoding="utf-8") as f:
        f.write(updated_report.strip() + "\n")
        
    print(f"Successfully updated {filename} with new findings.")

def main():
    parser = argparse.ArgumentParser(description="report-AI: Terminal to Pentesting Report Automation Tool")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--start-session", metavar="TITLE", help="Start a new pentesting documentation session with a general title")
    group.add_argument("--add-to-session", metavar="SESSION_NAME", nargs="?", const="LOAD_ACTIVE_STATE", help="Execute a command and integrate results into the active or specified session file")
    group.add_argument("--stop-session", action="store_true", help="Explicitly stop and clear the current tracking session")
    
    parser.add_argument("-m", metavar="MESSAGE", help="Short description of what you are attempting to do")
    parser.add_argument("-c", metavar="COMMAND", help="The terminal command you want to run")
    
    args = parser.parse_args()
    
    if args.start_session:
        start_session(args.start_session)
    elif args.stop_session:
        stop_session()
    elif args.add_to_session is not False and args.add_to_session != "LOAD_ACTIVE_STATE":
        if not args.m or not args.c:
            parser.error("--add-to-session requires both -m [message] and -c [command]")
        add_to_session(args.add_to_session, args.m, args.c)
    elif args.add_to_session == "LOAD_ACTIVE_STATE":
        if not args.m or not args.c:
            parser.error("--add-to-session requires both -m [message] and -c [command]")
        add_to_session("LOAD_ACTIVE_STATE", args.m, args.c)

if __name__ == "__main__":
    main()
