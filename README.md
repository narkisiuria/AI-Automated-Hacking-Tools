# AI/Python Automated PT Tools

A small collection of Python CLI utilities for authorized penetration-testing workflows. **AI Automated PT Tools** takes manual, syntax-heavy recon and reporting work and lets an operator describe intent in plain English, with Mistral generating the real commands and writeups behind it.

---

## 🚀 Key Features

### 🧠 AI-Assisted Payload Generation
*   **Plain-English Payload Requests:** Describe the payload you want, the AI extracts real filter keywords (OS family, connection type, payload style) and filters the local msfvenom payload and encoder catalogues by them.
*   **Two-Stage Mistral Pipeline:** One call filters the catalogue by keyword, a second call builds the full configuration (target OS, lhost, lport, payload type, encoder, iterations, output format), only asking the operator for lhost and lport.
*   **Real Command Execution:** The finished msfvenom command runs for real, and on confirmation an msfconsole multi-handler is launched to catch the session.

### 🔍 Nmap Recon Summarizer
*   **Interactive Scan Building:** Proposes a real Nmap command, lets you add or remove flags before running it.
*   **AI Recon Summary:** Feeds the real Nmap output to Mistral and gets back a short, terminal-friendly summary with suggested next steps.

### 📝 Session-Based Report Generator
*   **Persistent Report Sessions:** Start a named session, run real commands against a target, and each result gets appended as an AI-formatted Markdown finding.
*   **Rolling Context Summary:** Keeps a running summary of the session so later findings stay consistent with earlier ones.

---

## 📂 Project Structure

```text
AI-Automated-PT-Tools/
├── custom-AI-payload-generator/
│   ├── main_payloads_AI_generator.py
│   ├── payloads_encoders_filter_script.py
│   ├── msfvenom_payloads.txt
│   ├── encoders.txt
│   ├── requirments.txt
│   └── sample_input.txt
├── narmap-AI/
│   ├── narmap-AI.py
│   └── sample_output.md
├── PT-report-AI/
│   ├── report-AI.py
│   ├── .report_ai_session
│   ├── .report_ai_summary
│   └── test_session_report.md
├── .gitignore
└── README.md
```

---

## 🛠️ Requirements and System Setup

*   **Runtime Environment:** Python 3.11 or higher.
*   **External Tools:** Nmap (for narmap-AI), Metasploit Framework (msfvenom and msfconsole, for the payload generator). Both must be available on your PATH.
*   **Dependencies:** mistralai, python-dotenv.

```bash
git clone https://github.com/narkisiuria/AI-Automated-PT-Tools.git
cd AI-Automated-PT-Tools

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install mistralai python-dotenv
```

Create a `.env` file in the repository root:

```dotenv
# Used by narmap-AI
MISTRAL_API_KEY=replace_with_your_key

# Used by PT-report-AI and the payload generator
MISTRAL_API_KEY2=replace_with_your_key
```

---

## 💻 How to Run

### 1. Nmap Summary
Run from the repository root:
```bash
python narmap-AI/narmap-AI.py 192.0.2.10
```
Review the proposed Nmap command before it runs. The AI summary and suggested next steps are a starting point, verify them yourself.

### 2. Report Session
Run from `PT-report-AI/`:
```bash
cd PT-report-AI

python report-AI.py --start-session "Internal network assessment"

python report-AI.py \
  --add-to-session \
  -m "Enumerate the HTTP service" \
  -c "nmap -sV -p 80 192.0.2.10"

python report-AI.py --stop-session
```

### 3. Payload Helper
Run from the repository root:
```bash
python custom-AI-payload-generator/main_payloads_AI_generator.py
```
Describe the payload you want, confirm the listener address and port when asked, and review the final msfvenom command and encoder before running it.

---

## ⚠️ Warning

These tools execute real commands on your real machine, including offensive payload generation and remote scanning. Run only against systems you own or are explicitly authorized to test, and review every AI-generated command before confirming it.

---

## 🗺️ Roadmap

*   [x] Plain-English to msfvenom payload pipeline
*   [x] Automated listener and session catching via msfconsole
*   [x] Nmap scan builder with AI recon summary
*   [x] Session-based Markdown reporting with rolling context
*   [ ] AV/EDR evasion (currently blocked by Windows Defender/AMSI signature detection, not yet attempted)
*   [ ] Pinned dependency file and automated tests
