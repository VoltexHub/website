import socket
import requests

def get_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def get_public():
    try:
        return requests.get("https://api.ipify.org").text
    except Exception:
        return "Woopsy"

choice = input("local or public: ").strip().lower()

if choice == "local":
    print("Local:", get_local())
elif choice == "public":
    print("Public:", get_public())
else:
    print("BADD BOIII")
