import subprocess
import random

def random_mac():
    pairs = [f"{random.randint(0, 255):02X}" for _ in range(6)]
    first = int(pairs[0], 16)
    first |= 2  # locally administered
    first &= 0xFE # unicast
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

def spoof_mac(new_mac):
    adapter = get_adapter()
    if adapter is None:
        print("Could not find an active network adapter.")
        return

    adapter_key = r"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}"

    for i in range(0, 50):
        key = adapter_key + f"\\{i:04d}"
        subprocess.run(["reg", "add", key, "/v", "NetworkAddress", "/d", new_mac, "/f"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run(["netsh", "interface", "set", "interface", f"name={adapter}", "admin=disabled"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["netsh", "interface", "set", "interface", f"name={adapter}", "admin=enabled"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"Mad address successfully changed to: {new_mac}")

def main():
    mode = input("Custom mac address or random? (custom/random): ").strip().lower()
    if mode == "custom":
        custom_mac = input("Enter custom mac format: XX-XX-XX-XX-XX-XX): ").strip().upper()
        if len(custom_mac) != 17 or any(c not in "0123456789ABCDEF-" for c in custom_mac):
            print("Invalid format, defaulting to random address")
            new_mac = random_mac()
        else:
            new_mac = custom_mac
    else:
        new_mac = random_mac()

    spoof_mac(new_mac)

if __name__ == "__main__":
    main()
