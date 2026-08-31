# AI Automated PT Tools

A collection of Python CLI utilities for authorized penetration-testing workflows. **AI Automated PT Tools** takes manual, repetitive recon, exploitation, and reporting work and lets an operator describe intent in plain English, or feed in raw tool output, with Mistral handling the analysis and generation behind it.

---

## 🚀 Key Features

### 🧠 AI-Assisted Payload Generation
*   **Plain-English Payload Requests:** Describe the payload you want, the AI extracts real filter keywords and filters the local msfvenom payload and encoder catalogues by them.
*   **Two-Stage Mistral Pipeline:** One call filters the catalogue by keyword, a second builds the full configuration, only asking the operator for lhost and lport.
*   **Real Command Execution:** The finished msfvenom command runs for real, and on confirmation an msfconsole multi-handler is launched to catch the session.

### 🔍 Nmap Recon Summarizer
*   **Interactive Scan Building:** Proposes a real Nmap command, lets you add or remove flags before running it.
*   **AI Recon Summary:** Feeds the real Nmap output to Mistral and gets back a short, terminal-friendly summary with suggested next steps.

### 📝 Session-Based Report Generator
*   **Persistent Report Sessions:** Start a named session, run real commands against a target, and each result gets appended as an AI-formatted Markdown finding.
*   **Rolling Context Summary:** Keeps a running summary of the session so later findings stay consistent with earlier ones.

### 💣 AI Exploit Finder
*   **Searchsploit Integration:** Given a service and version, runs searchsploit and has the AI pick the most reliable matching exploit, favoring standalone scripts over Metasploit modules when the tool can't run msfconsole itself.
*   **AI-Written Usage Guide:** Reads the actual exploit file and returns a clear usage guide, including required parameters and hardcoded values to watch for.

### 🔑 AI Wordlist Generator
*   **Plain-English Target Description:** Describe a target's name, company, interests, and other real details, get back 1000+ realistic username and password variations.
*   **Realistic Human Patterns:** Case variants, leetspeak substitutions, year and number suffixes, and name/initial combinations, the way real people actually build credentials.

### 🎣 AI Phishing Pretext Generator
*   **Ready-to-Send Pretexts:** Describe the target, company, and trigger event, get back one complete, convincing phishing email for authorized social engineering assessments.
*   **Safe Placeholders:** Links and attachments are always placeholders, never real malicious content.

### 🛡️ AI Privilege Escalation Checker
*   **Automated Recon:** Runs peas (linpeas/winpeas), a sudo permissions check, and a SUID binary search directly on the target.
*   **Signal Filtering:** Filters peas' huge output down to only its flagged high-severity lines before sending anything to the AI.
*   **Prioritized Real Leads:** Cross-references SUID binaries against known exploitable binaries, flags risky sudo entries, and matches kernel/OS versions against known CVEs.

### 🌐 AI Recon Aggregator
*   **Multi-Tool Cross-Referencing:** Feed in one file containing multiple tools' raw output, each wrapped in its own labeled section, and get back one prioritized attack-surface summary.
*   **Connects the Dots:** Explicitly links findings across tools instead of listing them separately, for example, a leaked config file from one tool paired with an open service from another.

---

## 📂 Project Structure

```text
AI-Automated-PT-Tools/
├── custom-AI-payload-generator/
├── narmap-AI/
├── PT-report-AI/
├── AI-Exploit-Finder/
├── AI-custom-wordlist-generator/
├── AI-Phishing-Pretext-Generator/
├── AI-previlage-escalation-finder/
├── reacon-aggregator-AI/
├── .gitignore
└── README.md
```

---

## 🛠️ Requirements and System Setup

*   **Runtime Environment:** Python 3.10 or higher.
*   **External Tools:** Nmap, Metasploit Framework (msfvenom and msfconsole), searchsploit, linpeas/winpeas, as needed per tool. Must be available on your PATH.
*   **Dependencies:** mistralai, python-dotenv.

```bash
git clone https://github.com/narkisiuria/AI-Automated-PT-Tools.git
cd AI-Automated-PT-Tools

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install mistralai python-dotenv
```

Create a `.env` file in the repository root with your Mistral API key(s):

```dotenv
MISTRAL_API_KEY=replace_with_your_key
MISTRAL_API_KEY2=replace_with_your_key
```

> **Note:** On systems like Kali with an externally-managed Python environment, use a virtual environment as shown above. When running a tool with elevated privileges, call the venv's own Python binary directly, elevation does not inherit an activated venv's PATH.

---

## 💻 How to Run

Each tool lives in its own folder and is run directly:

```bash
python custom-AI-payload-generator/main_payloads_AI_generator.py
python narmap-AI/narmap-AI.py <target>
python PT-report-AI/report-AI.py --start-session "Session name"
python AI-Exploit-Finder/AI_Exploit_Finder.py -s <service> -v <version>
python AI-custom-wordlist-generator/main_wordlist_AI_gen.py
python AI-Phishing-Pretext-Generator/AI_phishing_pretext_main.py
python AI-previlage-escalation-finder/check_for_privlege_esc_with_AI.py
python reacon-aggregator-AI/reacon_aggregator_AI_main.py --input-file <path>
```

Each tool will prompt for whatever it needs, a plain-English description, a target, or a file path, and most require confirmation before anything real runs.

---

## ⚠️ Warning

These tools execute real commands on real machines, including offensive payload generation, remote scanning, and social engineering content generation. Run only against systems you own or are explicitly authorized to test, and review every AI-generated command or output before acting on it.

---

## 🗺️ Roadmap

*   [x] Plain-English to msfvenom payload pipeline
*   [x] Automated listener and session catching via msfconsole
*   [x] Nmap scan builder with AI recon summary
*   [x] Session-based Markdown reporting with rolling context
*   [x] Searchsploit-integrated exploit finder with AI usage guides
*   [x] AI wordlist/credential generator
*   [x] AI phishing pretext generator
*   [x] AI privilege escalation checker
*   [x] AI multi-tool recon aggregator
*   [ ] AV/EDR evasion (currently blocked by Windows Defender/AMSI signature detection, not yet attempted)
*   [ ] Pinned dependency file and automated tests
*   [ ] Windows-native support for the privilege escalation checker
