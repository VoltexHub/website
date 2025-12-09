import os
import shutil
import subprocess
import random
from pathlib import Path

def remove_path(path):
    try:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
        print(f"Deleted: {path}")
    except Exception:
        pass

# ---------------------------
# ROBLOX WEBSITE DATA (Chrome/Edge only)
# ---------------------------

def clear_roblox_website_data():
    roblox_domains = ["roblox.com", ".roblox.com"]

    # Chrome
    chrome_default = Path(os.getenv("LOCALAPPDATA")) / "Google/Chrome/User Data/Default"
    chrome_ls = chrome_default / "Local Storage/leveldb"
    chrome_cookies = chrome_default / "Cookies"

    # Edge
    edge_default = Path(os.getenv("LOCALAPPDATA")) / "Microsoft/Edge/User Data/Default"
    edge_ls = edge_default / "Local Storage/leveldb"
    edge_cookies = edge_default / "Cookies"

    # Delete only Roblox localStorage keys
    for p in [chrome_ls, edge_ls]:
        if p.exists():
            for f in p.iterdir():
                if any(domain in f.name.lower() for domain in roblox_domains):
                    remove_path(f)

    # Delete only Roblox cookies
    for cookie_db in [chrome_cookies, edge_cookies]:
        if cookie_db.exists():
            try:
                os.remove(cookie_db)
            except:
                pass

    print("[✔] Roblox WEBSITE tracking wiped.")


# ---------------------------
# ROBLOX APP DATA
# ---------------------------

def clear_roblox_app_data():
    # Kill Roblox processes
    subprocess.run(['taskkill', '/F', '/IM', 'RobloxPlayerBeta.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    root = Path(os.getenv("LOCALAPPDATA")) / "Roblox"
    remove_path(root / "logs")
    remove_path(root / "downloads")
    remove_path(root / "LocalStorage")

    # Remove registry-based identifiers
    subprocess.run(['reg', 'delete', 'HKCU\\Software\\Roblox', '/f'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("[✔] Roblox APP data wiped.")


# ---------------------------
# MAC ADDRESS SPOOFER
# ---------------------------

def random_mac():
    hex_pairs = []
    for _ in range(6):
        hex_pairs.append(f"{random.randint(0, 255):02X}")
    # Ensure unicast + locally administered
    first = int(hex_pairs[0], 16)
    first |= 2
    first &= 0xFE
    hex_pairs[0] = f"{first:02X}"
    return "-".join(hex_pairs)

def spoof_mac():
    new_mac = random_mac()
    
    # Find network adapter registry keys
    adapter_key = r"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}"

    # Apply MAC to *all* active adapters
    for i in range(0, 50):
        key = adapter_key + f"\\{i:04d}"
        subprocess.run(['reg', 'add', key, '/v', 'NetworkAddress', '/d', new_mac, '/f'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Restart networking so mac takes effect
    subprocess.run(["netsh", "interface", "set", "interface", "name=\"Ethernet\"", "admin=disabled"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["netsh", "interface", "set", "interface", "name=\"Ethernet\"", "admin=enabled"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"[✔] MAC address spoofed to: {new_mac}")


# ---------------------------
# RUN EVERYTHING
# ---------------------------

if __name__ == "__main__":
    print("Clearing Roblox website tracking…")
    clear_roblox_website_data()

    print("Clearing Roblox app tracking…")
    clear_roblox_app_data()

    print("Spoofing MAC address…")
    spoof_mac()

    print("\n[✔] COMPLETED — Roblox tracking wiped + MAC address spoofed.")
