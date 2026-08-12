PS C:\Users\Uria Narkisi\Documents\AI_Automated_PT_Tools> python narmap-AI/narmap-AI.py 192.168.7.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
using the recommended nmap command flags: sudo nmap -sC -sV -Pn --open 192.168.7.1
would you want to add or change any flags? (y/n): y
type add [flag] or rm [flag] to make your changes: add -p 80,4444
final command: sudo nmap -sC -sV -Pn --open -p 192.168.7.1
running nmap...
loading API key...
sending API request...
getting AI response...

AI OUTPUT RESPONSE
Port 22 open - OpenSSH 8.2p1 (Ubuntu)
Next step: Check for default/weak credentials with `hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://<target_IP>`

Port 80 open - Apache httpd 2.4.41 (Ubuntu)
Next step: Run `gobuster dir -u http://<target_IP> -w /usr/share/wordlists/dirb/common.txt` to find hidden paths

Port 443 open - Apache httpd 2.4.41 (Ubuntu) with self-signed cert
Next step: Check for Heartbleed with `nmap --script ssl-heartbleed -p 443 <target_IP>`

Port 3306 open - MySQL 5.7.31
Next step: Test for anonymous access with `mysql -u '' -h <target_IP> -p`

Notable: Outdated Apache (2.4.41) and MySQL (5.7.31) versions with known vulnerabilities.
Next step: Search for exploits with `searchsploit apache 2.4.41` and `searchsploit mysql 5.7.31`
PS C:\Users\Uria Narkisi\Documents\AI_Automated_PT_Tools> 