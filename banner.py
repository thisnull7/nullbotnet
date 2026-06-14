import os
import sys
import time


R = '\033[91m'      # Red
RD = '\033[31m'     # Dark Red
G = '\033[92m'      # Green
Y = '\033[93m'      # Yellow
C = '\033[96m'      # Cyan
W = '\033[97m'      # White
M = '\033[95m'      # Magenta
B = '\033[1m'       # Bold
D = '\033[2m'       # Dim
BL = '\033[5m'      # Blink
RS = '\033[0m'      # Reset


LOGO = f"""
{R}{B}
          ███╗   ██╗ ██╗   ██╗ ██╗      ██╗
          ████╗  ██║ ██║   ██║ ██║      ██║
          ██╔██╗ ██║ ██║   ██║ ██║      ██║
          ██║╚██╗██║ ██║   ██║ ██║      ██║
          ██║ ╚████║ ╚██████╔╝ ███████╗ ██║
          ╚═╝  ╚═══╝  ╚═════╝  ╚══════╝ ╚═╝

          ███████╗ ████████╗  ██████╗  ██████╗  ███╗   ███╗
          ██╔════╝ ╚══██╔══╝ ██╔═══██╗ ██╔══██╗ ████╗ ████║
          ███████╗    ██║    ██║   ██║ ██████╔╝ ██╔████╔██║
          ╚════██║    ██║    ██║   ██║ ██╔══██╗ ██║╚██╔╝██║
          ███████║    ██║    ╚██████╔╝ ██║  ██║ ██║ ╚═╝ ██║
          ╚══════╝    ╚═╝     ╚═════╝  ╚═╝  ╚═╝ ╚═╝     ╚═╝
{RS}"""


HEADER = f"""
{R}{B}                         ◆ NULL STORM v2.1 ◆
{D}                      Zero Config Botnet Framework{RS}
"""

DIV = f"{D}  ─────────────────────────────────────────────────────────────────────────{RS}"


STATUS_BAR = f"""
{D}  ──┤ {W}SYSTEM STATUS{R} ├──────────────────────────────────────────────────────────{RS}
{RS}
  {G}●{W} C2 Server      {D}: {G}ONLINE{R}
  {G}●{W} Discovery      {D}: {G}ACTIVE{R}
  {G}●{W} Attack Vector  {D}: {R}ARMED{R}
  {G}●{W} Encryption     {D}: {G}AES-256{R}
{RS}"""


INFO = f"""
{D}  ──┤ {W}SYSTEM INFO{R} ├────────────────────────────────────────────────────────────{RS}
{RS}
  {R}▸{W} Author      {D}: {C}null7{R}
  {R}▸{W} GitHub      {D}: {C}github.com/thisnull7{R}
  {R}▸{W} Repository  {D}: {C}nullbotnet{R}
  {R}▸{W} Version     {D}: {W}v2.1 {D}Stable{R}
  {R}▸{W} License     {D}: {W}MIT{R}
{RS}"""


FEATURES = f"""
{D}  ──┤ {W}CAPABILITIES{R} ├───────────────────────────────────────────────────────────{RS}
{RS}
  {Y}◇{W} Auto-Discover C2 Server
  {Y}◇{W} Auto-Connect Without Manual IP
  {Y}◇{W} Dual Attack Vector System
  {Y}◇{W} High Concurrency Engine
  {Y}◇{W} Real-Time Bot Monitoring
{RS}"""


COMMANDS = f"""
{D}  ──┤ {W}COMMANDS{R} ├──────────────────────────────────────────────────────────────{RS}
{RS}
  {C}list{W}      Display online bots
  {C}help{W}      Show command list
  {C}banner{W}    Redisplay banner
  {C}exit{W}      Shutdown C2 server
  {C}<url>{W}     Attack target URL
{RS}"""


def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print logo
    for line in LOGO.split('\n'):
        if line.strip():
            sys.stdout.write(line + '\n')
            sys.stdout.flush()
            time.sleep(0.003)
    
    print()
    
    # Print header
    for line in HEADER.split('\n'):
        if line.strip():
            sys.stdout.write(line + '\n')
            sys.stdout.flush()
            time.sleep(0.01)
    
    print(DIV)
    
    # Print status bar
    for line in STATUS_BAR.split('\n'):
        if line.strip():
            sys.stdout.write(line + '\n')
            sys.stdout.flush()
            time.sleep(0.01)
    
    print(DIV)
    
    # Print info
    for line in INFO.split('\n'):
        if line.strip():
            sys.stdout.write(line + '\n')
            sys.stdout.flush()
            time.sleep(0.008)
    
    print(DIV)
    
    # Print features
    for line in FEATURES.split('\n'):
        if line.strip():
            sys.stdout.write(line + '\n')
            sys.stdout.flush()
            time.sleep(0.008)
    
    print(DIV)
    
  
    for line in COMMANDS.split('\n'):
        if line.strip():
            sys.stdout.write(line + '\n')
            sys.stdout.flush()
            time.sleep(0.008)
    
    print(DIV)
    
    # Footer
    print()
    print(f"  {R}☠{RS} {W}Ready for attack.{RS} {D}Enter target URL to begin.{RS}")
    print()