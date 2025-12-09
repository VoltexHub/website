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

def clear_website():
    chrome_default = Path(os.getenv("LOCALAPPDATA")) / "Google/Chrome/User Data/Default"
    chrome_ls = chrome_default / "Local Storage/leveldb"
    chrome_cookies = chrome_default / "Cookies"

    edge_default = Path(os.getenv("LOCALAPPDATA")) / "Microsoft/Edge/User Data/Default"
    edge_ls = edge_default / "Local Storage/leveldb"
    edge_cookies = edge_default / "Cookies"

    domains = ["roblox.com", ".roblox.com"]

    for p in [chrome_ls, edge_ls]:
        if p.exists():
            for f in p.iterdir():
                if any(domain in f.name.lower() for domain in domains):
                    remove_path(f)

    for cookie_db in [chrome_cookies, edge_cookies]:
        if cookie_db.exists():
            try:
                os.remove(cookie_db)
            except:
                pass

    print("Website cleared")

def clear_app():
    subprocess.run(['taskkill', '/F', '/IM', 'RobloxPlayerBeta.exe'],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    root = Path(os.getenv("LOCALAPPDATA")) / "Roblox"
    remove_path(root / "logs")
    remove_path(root / "downloads")
    remove_path(root / "LocalStorage")

    subprocess.run(['reg', 'delete', 'HKCU\\Software\\Roblox', '/f'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("App cleared")

def random_mac():
    pairs = [f"{random.randint(0, 255):02X}" for _ in range(6)]
    first = int(pairs[0], 16)
    first |= 2
    first &= 0xFE
    pairs[0] = f"{first:02X}"
    return "-".join(pairs)

def get_adapter():
    result = subprocess.run(["netsh", "interface", "show", "interface"],
                            capture_output=True, text=True)

    for line in result.stdout.splitlines():
        if "Connected" in line and "Enabled" in line:
            parts = line.split()
            return parts[-1]
    return None

def spoof_mac():
    adapter = get_adapter()
    if adapter is None:
        print("No active network adapter found")
        return

    new_mac = random_mac()

    adapter_key = r"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}"

    for i in range(0, 50):
        key = adapter_key + f"\\{i:04d}"
        subprocess.run(["reg", "add", key, "/v", "NetworkAddress", "/d", new_mac, "/f"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run(["netsh", "interface", "set", "interface", f"name={adapter}", "admin=disabled"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["netsh", "interface", "set", "interface", f"name={adapter}", "admin=enabled"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"MAC address spoofed to: {new_mac}")

if __name__ == "__main__":
    clear_website()
    clear_app() # couldnt implement the re-launching of the app
    spoof_mac()

    print("Complete, but you should probbaly use a vpn too")
