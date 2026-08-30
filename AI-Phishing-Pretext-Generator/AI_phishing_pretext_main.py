from mistralai.client import Mistral
from dotenv import load_dotenv
import os
import sys

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

phishing_pretext_system_prompt = (
    '''You are a phishing pretext generator for authorized social engineering assessments and red-team exercises.

    Your job: given a plain-English description of a target (company, role, context, trigger event, etc), write ONE complete, realistic phishing email ready to send.

    Rules:
    - Output ONLY the finished email: a Subject line, followed by the full body. No explanation, no markdown, no commentary.
    - Make it genuinely convincing: correct tone for the claimed sender (IT, HR, vendor, exec, etc), realistic urgency, and no obvious red flags like poor grammar or generic greetings unless the target details call for that style.
    - Use the specific details given (company name, target role, trigger event) naturally throughout the email, don't just insert them awkwardly.
    - Include a clear, plausible call to action (click a link, reply with info, open an attachment) worded the way real phishing emails word it, without inserting an actual malicious link, just a placeholder like [LINK] or [ATTACHMENT].
    - Sign off with a realistic sender name and title fitting the pretext.'''
    )

try:
    user_req = input("PHISHING PRETEXT GEN AI (TEXT FREE REQUEST)> ")
    ai_output_pretext = call_mistral(phishing_pretext_system_prompt, user_req)
    
    while True:
        gen_filename = input("ENTER GENERATED FILE NEW NAME> ")
        with open(gen_filename, "w", encoding="utf-8") as f:
            f.write(ai_output_pretext)
        
        print(f"successfuly generated phishing pretext file as: {gen_filename}")
        break
        
except Exception as e:
    print(f"invalid input: {e}")
    
except FileExistsError:
    print(f"file {gen_filename} already exsits. try a diferrent file name")