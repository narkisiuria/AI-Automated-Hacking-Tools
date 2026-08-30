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

wordlist_system_prompt = (
    '''You are a wordlist generation engine for authorized password/username guessing during penetration tests.

    Your job: given a plain-English description of a target (name, company, interests, dates, etc), generate a large list of likely usernames/passwords a real person or organization might actually use.

    Rules:
    - Output ONLY the wordlist, one entry per line. No explanation, no markdown, no numbering, no extra text.
    - Generate at least 1000 unique entries.
    - Base entries on the actual details given (names, nicknames, initials, company name, years, interests, pets, etc).
    - Include realistic human variations: lowercase, capitalized, all-caps, common leetspeak substitutions (a->4, e->3, i->1, o->0, s->5), common suffixes (123, 1, !, 2023, 2024, 2025, ...), and combinations of the above.
    - Include combinations of first name + last name, initials + last name, first name + numbers, etc, matching how real people actually create usernames and passwords.
    - Do not repeat the exact same entry twice.
    - Do not include a header, footer, or any commentary.'''
    )



try:
    user_req = input("WORDLIST GEN AI (TEXT FREE REQUEST)> ")
    ai_output_wordlist = call_mistral(wordlist_system_prompt, user_req)
    wordlist_list = ai_output_wordlist.split("\n")
    
    while True:
        gen_filename = input("ENTER GENERATED FILE NEW NAME> ")
        with open(gen_filename, "w", encoding="utf-8") as f:
            for word in wordlist_list:
                f.write(word + "\n")
        
        print(f"successfuly generated wordlist file as: {gen_filename}")
        break
        
except Exception as e:
    print(f"invalid input: {e}")
    
except FileExistsError:
    print(f"file {gen_filename} already exsits. try a diferrent file name")