# narmap-AI
 
Runs nmap and uses AI (Mistral) to turn raw scan output into a plain, actionable summary with next-step commands.
 
## Setup
 
1. Install dependencies:
```
pip install mistralai python-dotenv
```
 
2. Create a `.env` file in the project folder:
```
MISTRAL_API_KEY=your_key_here
```
 
3. Make sure `nmap` is installed and on your PATH.
## Usage
 
```
python narmap-AI.py <target>
```
 
Example:
```
python narmap-AI.py 192.168.1.0/24
```
 
You'll be shown the recommended nmap command and can add/remove flags before it runs.
 
## What it does
 
1. Runs nmap against the target (default: `-sC -sV -Pn --open`)
2. Sends the raw output to Mistral with a system prompt telling it to act as a recon assistant
3. Prints a clean, terminal-friendly summary: open ports, services, notable findings, and a concrete next step for each
## Notes
 
- Only use on networks/hosts you own or have permission to test.
- AI-suggested versions/services are guesses in some cases - verify manually before acting on them.
- `.env` is gitignored (add it) - never commit your API key.
 
