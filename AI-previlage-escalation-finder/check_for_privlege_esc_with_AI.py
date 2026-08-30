from mistralai.client import Mistral
from dotenv import load_dotenv
import os
import sys
from filter_severe_lines_alg import filter_high_severity_lines
import subprocess
import shlex

privesc_system_prompt = (
    '''You are a privilege-escalation analyst reviewing real recon data collected from a target machine during an authorized penetration test.

    You will be given three sections: high-severity findings flagged by peas (linpeas/winpeas), sudo permissions (sudo -l output), and SUID binaries found on the system.

    Your job: identify the most promising real privilege-escalation paths, in priority order.

    Rules:
    - Output a short prioritized list (most promising first), each with the specific finding and a one to two sentence reason why it's exploitable.
    - Cross-reference SUID binaries against known GTFOBins-exploitable binaries (e.g. find, vim, python, awk, cp, etc) and call out any matches specifically.
    - If sudo -l output shows commands runnable as root without a password, or with NOPASSWD, flag these as high priority.
    - If any kernel or OS version is mentioned in the peas findings, and it matches a well-known CVE (e.g. Dirty Cow, PwnKit, etc), name the CVE and note it explicitly.
    - Do not repeat raw input lines verbatim as if they were new findings, synthesize and explain instead.
    - If nothing genuinely promising is found, say so plainly rather than inventing a lead.
    - Keep the whole response under 15 lines.'''
    )

print("loading API key...")
load_dotenv()
print("obtaining API key with dotenv")
api_key = os.getenv("MISTRAL_API_KEY2")
print("successfuly finished loading API key")
print("cleaning screen...")
os.system("cls" if os.name == "nt" else "clear")

if not api_key:
    print("Error: MISTRAL_API_KEY2 not found in your environment variables (.env file).")
    sys.exit(1)

print("starting client session...")
client = Mistral(api_key=api_key)

def run_command(command_to_run):
    result = subprocess.run(
    command_to_run,
    shell=True,
    capture_output=True,
    text=True
    )
    
    return result.stdout

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

print("running peas tool (this may take a minute)...")
raw_linpeas_command = "sudo winpeas.exe" if os.name == "nt" else "sudo bash linpeas.sh"
raw_peas_output = run_command(raw_linpeas_command)
print("peas scan complete")

print("filtering for high-severity findings...")
high_severity_lines = filter_high_severity_lines(raw_peas_output)
print(f"found {len(high_severity_lines)} high-severity line(s)")

print("checking sudo permissions (sudo -l)...")
raw_sudo_l_command = "sudo -l"
sudo_l_output = run_command(raw_sudo_l_command)
print("sudo check complete")

print("searching for SUID binaries (find / -perm -4000)...")
raw_suid_bits_check_command = "find / -perm -4000 -type f 2>/dev/null"
suid_bits_check_output = run_command(raw_suid_bits_check_command)
print("SUID search complete")

print("combining all findings into one context for analysis...")
combined_context = (
    f"HIGH-SEVERITY PEAS FINDINGS:\n{chr(10).join(high_severity_lines)}\n\n"
    f"SUDO -L OUTPUT:\n{sudo_l_output}\n\n"
    f"SUID BINARIES FOUND:\n{suid_bits_check_output}"
)

print("sending combined findings to AI for privilege-escalation analysis...")
mistrial_analasis_output = call_mistral(privesc_system_prompt, combined_context)

print("\n===== PRIVILEGE ESCALATION ANALYSIS =====\n")
print(mistrial_analasis_output)
print("\nFINISHED WITH NO ERRORS")