# AI/PYTHON Automated PT Tools

A small collection of Python CLI utilities for **authorized** penetration-testing workflows. The repository currently contains three independent tools: an Nmap summarizer, a session-based Markdown report generator, and an `msfvenom` payload helper. Each tool sends relevant context to Mistral and expects a valid Mistral API key. [1] [2] [3]

> **Authorization required.** Run these tools only against systems you own or are explicitly authorized to test. The report tool executes the command you supply; the payload tool runs `msfvenom` and can start an `msfconsole` handler.

## What is included

| Tool | Purpose | External dependencies | API variable |
| --- | --- | --- | --- |
| [`custom-AI-payload-generator`](./custom-AI-payload-generator/main_payloads_AI_generator.py) | Filters local `msfvenom` payload and encoder lists, builds an `msfvenom` command, and can start a Metasploit handler. | Metasploit Framework, Mistral | `MISTRAL_API_KEY2` |
| [`narmap-AI`](./narmap-AI/narmap-AI.py) | Runs Nmap, then turns raw scan output into a short recon summary with suggested next steps. | Nmap, Mistral | `MISTRAL_API_KEY` |
| [`PT-report-AI`](./PT-report-AI/report-AI.py) | Starts a reporting session, runs a supplied command, and appends an AI-formatted Markdown finding to the report. | Mistral | `MISTRAL_API_KEY2` |


## Repository layout

```text
AI-Automated-PT-Tools/
├── narmap-AI/
│   ├── narmap-AI.py
│   └── sample_output.md
├── PT-report-AI/
│   ├── report-AI.py
│   ├── .report_ai_session     
│   ├── .report_ai_summary        
│   └── test_session_report.md     
└── custom-AI-payload-generator/
    ├── main_payloads_AI_generator.py
    ├── payloads_encoders_filter_script.py
    ├── msfvenom_payloads.txt    
    └── encoders.txt            
```

## Dependencies

Use Python **3.11+** and a Mistral API key. Install Nmap for `narmap-AI`; install the Metasploit Framework for the payload generator. Both `nmap` and, where applicable, `msfvenom` and `msfconsole` must be available on your `PATH`. The repository does not currently pin Python dependencies. [1] [2] [3]

```bash
git clone https://github.com/narkisiuria/AI-Automated-PT-Tools.git
cd AI-Automated-PT-Tools

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install mistralai python-dotenv
```

Create `.env` in the repository root:

```dotenv
# Used by narmap-AI
MISTRAL_API_KEY=replace_with_your_key

# Used by PT-report-AI and the payload generator
MISTRAL_API_KEY2=replace_with_your_key
```

The scripts use two environment-variable names. They can point to the same Mistral key. The checked-in `.gitignore` does **not** ignore `.env`; add it before committing local credentials. [1] [2] [3] [4]

```gitignore
.env
```

## Usage

### 1. Nmap summary

Run from the repository root. The tool proposes `sudo nmap -sC -sV -Pn --open <target>`, lets you add or remove flags interactively, runs the final command, and submits Nmap standard output to Mistral for a terminal-friendly summary. [1]

```bash
python narmap-AI/narmap-AI.py 192.0.2.10
```

The target is a required positional argument. Review the final Nmap command before allowing it to run. Model-suggested service versions and follow-up actions are not evidence; verify them yourself.

### 2. Report session

Run this tool from `PT-report-AI/`. It stores session state in `.report_ai_session`, maintains a rolling context summary in `.report_ai_summary`, and writes the generated Markdown report in the current directory. Each `--add-to-session` call executes the exact command supplied with `-c`, captures stdout and stderr for up to 300 seconds, and appends an AI-generated report section. [2]

```bash
cd PT-report-AI

# Create a report and persist the active session.
python report-AI.py --start-session "Internal network assessment"

# Run a command and add its results to the active report.
python report-AI.py \
  --add-to-session \
  -m "Enumerate the HTTP service" \
  -c "nmap -sV -p 80 192.0.2.10"

# Clear the active-session marker when the work is complete.
python report-AI.py --stop-session
```

You can target a named report instead of the active session:

```bash
python report-AI.py \
  --add-to-session "Internal network assessment" \
  -m "Review service exposure" \
  -c "nmap -sV 192.0.2.10"
```

### 3. Payload helper

Run this tool **from the repository root**. It uses repository-relative paths to load the static payload and encoder catalogues. The workflow accepts a plain-English request, asks Mistral for filtering keywords, filters the local catalogue, asks Mistral for a JSON payload specification, runs `msfvenom`, and optionally launches an `msfconsole` multi-handler. [3] [5]

```bash
cd /path/to/AI-Automated-PT-Tools
python custom-AI-payload-generator/main_payloads_AI_generator.py
```

Supply only values appropriate for an isolated, authorized test environment. Inspect the selected payload type, listener address, listener port, encoder, and output format before proceeding. The generated payload is written to standard output; the current implementation does not provide an output-file argument. [3]

## Data handling and operational notes

| Area | Current behavior | Practical implication |
| --- | --- | --- |
| Mistral requests | The tools submit raw Nmap output, report context plus command output, or the payload request and local catalogue data to Mistral. [1] [2] [3] | Do not send secrets, customer data, or sensitive assessment evidence unless your engagement terms and data-handling policy allow it. |
| Command execution | `PT-report-AI` executes the user-provided `-c` command. The payload tool executes a command built from model-produced JSON and may start `msfconsole`. [2] [3] | Treat all command arguments and model output as untrusted until reviewed. Run with the minimum privileges required. |
| Report state | Session metadata and a rolling AI summary are stored as local dotfiles in `PT-report-AI/`. [2] | Keep the directory with the report if you need to resume a session; remove the state files if you need a clean start. |
| Payload catalogues | Payload and encoder options come from static text files committed to the repository. [3] [5] | Refresh the catalogues from your installed Metasploit version when accuracy matters. |

## Current limitations

The project is an early CLI collection, not a packaged security platform. There is no pinned dependency file, automated test suite, continuous-integration workflow, release process, or license file in the current repository state. The existing `requirments.txt` is a handwritten note rather than an installable requirements manifest. [4] [6]

Before relying on this in a real engagement, pin the Mistral SDK version, add tests around command construction and AI response parsing, validate model-produced fields against explicit allow-lists, keep `.env` out of version control, and make report-state and output paths configurable. The source files passed a local Python 3.11 syntax check during this README review; no live scan, external API call, payload generation, or handler execution was performed.

## Contributing

Keep changes small and testable. A useful pull request should describe the security impact, include a reproducible command or test case, avoid committing credentials or client data, and update this README when setup or behavior changes.

## License

No license file is currently included. Do not assume reuse, redistribution, or modification rights until the repository owner adds an explicit license. [6]

## References

[1]: https://github.com/narkisiuria/AI-Automated-PT-Tools/blob/master/narmap-AI/narmap-AI.py "narmap-AI implementation"
[2]: https://github.com/narkisiuria/AI-Automated-PT-Tools/blob/master/PT-report-AI/report-AI.py "PT-report-AI implementation"
[3]: https://github.com/narkisiuria/AI-Automated-PT-Tools/blob/master/custom-AI-payload-generator/main_payloads_AI_generator.py "Payload generator implementation"
[4]: https://github.com/narkisiuria/AI-Automated-PT-Tools/blob/master/.gitignore "Repository ignore rules"
[5]: https://github.com/narkisiuria/AI-Automated-PT-Tools/tree/master/custom-AI-payload-generator "Payload and encoder catalogues"
[6]: https://github.com/narkisiuria/AI-Automated-PT-Tools "Repository root"
