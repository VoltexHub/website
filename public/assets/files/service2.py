import subprocess
import random
import sys
import ctypes
import re

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def random_mac():
    mac = [random.randint(0x00, 0xFF) for _ in range(6)]
    mac[0] = (mac[0] | 2) & 0xFE  # locally administered + unicast
    return "-".join(f"{b:02X}" for b in mac)

def get_adapter():
    result = subprocess.run(
        ["netsh", "interface", "show", "interface"],
        capture_output=True, text=True
    )
    for line in result.stdout.splitlines():
        if "Connected" in line and "Enabled" in line:
            return line.split()[-1]
    return None

def valid_mac(mac):
    return bool(re.fullmatch(r"[0-9A-F]{2}(-[0-9A-F]{2}){5}", mac))

def spoof_mac(new_mac):
    adapter = get_adapter()
    if not adapter:
        print("No active network adapter found.")
        return

    base_key = r"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}"

    for i in range(50):
        key = f"{base_key}\\{i:04d}"
        subprocess.run(
            ["reg", "add", key, "/v", "NetworkAddress", "/d", new_mac.replace("-", ""), "/f"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    subprocess.run(["netsh", "interface", "set", "interface", adapter, "admin=disabled"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["netsh", "interface", "set", "interface", adapter, "admin=enabled"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"MAC address set to: {new_mac}")
    print("Reconnect to Wi‑Fi/Ethernet if needed.")

def main():
    if not is_admin():
        print("Run this script as Administrator.")
        input("Press Enter to exit...")
        sys.exit(1)

    choice = input("Press Enter for random MAC, or type custom: ").strip().lower()

    if choice == "custom":
        mac = input("Enter MAC (XX-XX-XX-XX-XX-XX): ").strip().upper()
        if not valid_mac(mac):
            print("Invalid MAC. Using random instead.")
            mac = random_mac()
    else:
        mac = random_mac()

    spoof_mac(mac)
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
