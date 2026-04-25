#!/usr/bin/env python3
import requests
import os
from colorama import Fore, Style, init

init(autoreset=True)

def show_banner():
    print(rf"""{Fore.CYAN}{Style.BRIGHT}
  _______ ____   _____ _    _          _____  _____  
 |__   __|  _ \ / ____| |  | |   /\   |  __ \|  __ \ 
    | |  | |_) | |  __| |  | |  /  \  | |__) | |  | |
    | |  |  _ <| | |_ | |  | | / /\ \ |  _  /| |  | |
    | |  | |_) | |__| | |__| |/ ____ \| | \ \| |__| |
    |_|  |____/ \_____|\____//_/    \_\_|  \_\_____/ 
{Fore.YELLOW}          [!] Slogan: Secure the Web, Byte by Byte
{Fore.GREEN}          TB GUARD v1.6 - Security Audit Only
-------------------------------------------------------""")

def check_url(url):
    if not url.startswith('http'): url = 'http://' + url.strip()
    print(f"\n{Fore.BLUE}[+]{Fore.WHITE} Auditing: {url}")
    
    try:
        res = requests.get(url, timeout=10, allow_redirects=True)
        h = res.headers
        
        # 1. SSL/HTTPS
        if res.url.startswith('https'):
            print(f"  {Fore.GREEN}[V] PASS: Connection is secure (HTTPS)")
        else:
            print(f"  {Fore.RED}[!] RISK: Connection is not secure (HTTP)")

        # 2. X-Frame-Options (Clickjacking)
        if 'X-Frame-Options' in h:
            print(f"  {Fore.GREEN}[V] PASS: Clickjacking protection active")
        else:
            print(f"  {Fore.RED}[!] RISK: Clickjacking protection missing!")

        # 3. Content Security Policy (XSS)
        if 'Content-Security-Policy' in h:
            print(f"  {Fore.GREEN}[V] PASS: XSS protection (CSP) active")
        else:
            print(f"  {Fore.RED}[!] RISK: XSS protection (CSP) missing!")

        # 4. Server Identity
        if 'Server' in h:
            print(f"  {Fore.RED}[!] RISK: Server info leaked ({h['Server']})")
        else:
            print(f"  {Fore.GREEN}[V] PASS: Server info is hidden")
            
    except Exception as e:
        print(f"  {Fore.RED}[X] Connection Error: {e}")

if __name__ == "__main__":
    show_banner()
    inp = input(f"{Fore.CYAN}Target (URL/TXT): {Fore.WHITE}").strip()
    if os.path.isfile(inp):
        with open(inp, 'r') as f:
            for line in f: 
                if line.strip(): check_url(line.strip())
    elif inp:
        check_url(inp)
