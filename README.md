# DDOS — ATTACK Multi-Layer Stress Testing Suite

A comprehensive, multi-layer DDoS simulation tool for **authorized penetration testing** only. Covers Layer 3 (Network), Layer 4 (Transport), and Layer 7 (Application) attack vectors with a colorful real-time dashboard and live target status monitoring.

> **⚠️ IMPORTANT:** This tool is designed exclusively for authorized security assessments. Do not use against targets without explicit written permission. Unauthorized use is illegal.

---

# Features

- **Layer 3 (Network):** ICMP flood, IP fragmentation flood, spoofed IP packet flood
- **Layer 4 (Transport):** SYN flood, SYN-ACK flood, ACK flood, UDP flood, UDP amplification simulation
- **Layer 7 (Application):** HTTP GET/POST flood, Slowloris, Slow POST, SSL renegotiation flood
- **Live Dashboard:** Real-time colorful terminal UI with packet rate, success rate, target status, and downtime tracking
- **Multi-Layer Assault:** Run all layers simultaneously for maximum stress testing
- **Status Monitoring:** Automatic target health checks (HTTP, TCP SYN, DNS resolution)

---

# Requirements

- Python 3.7+
- [Scapy](https://scapy.net/) — for raw packet crafting

Install dependencies:

```bash
pip install scapy
```

# Usage
usage: python3 ddos_suite.py <target> [options]

# Positional Arguments
Argument	Description
target	Target URL or IP (e.g., http://example.com or 192.168.1.1)

# Options:
Flag	Default	Description
-a, --attack	http_flood	Attack type (or layer3/layer4/layer7/all/full)
-d, --duration	30	Duration in seconds
-t, --threads	100	Number of concurrent threads
--port	80	Target port (for IP targets)
--list	—	List all available attack module


# Basic Examples
Basic single attack (default: HTTP flood, 30s, 100 threads)
```python3 ddos_suite.py http://target.com```

Specific attack with options
```python3 ddos_suite.py http://target.com -a syn_flood -d 60 -t 200```

Layer-specific assault (all attacks in that layer simultaneously)
```python3 ddos_suite.py http://target.com -a layer3 -d 30```
```python3 ddos_suite.py http://target.com -a layer4 -d 60 -t 300```
```python3 ddos_suite.py http://target.com -a layer7 -d 45```

Full multi-layer assault (L3+L4+L7 all at once)
```python3 ddos_suite.py https://target.com -a full -d 60 -t 500```

Run all attacks sequentially
```python3 ddos_suite.py http://target.com -a all -d 20```

Target by IP
```sudo python3 ddos_suite.py 192.168.1.100 -a udp_flood -d 30 --port 80```

List available attacks
```python3 ddos_suite.py --list```


# Attack Modules
## Layer 3 - Network
Attack Name	Description
icmp_flood	ICMP echo request flood
ip_frag	IP fragmentation flood
ip_spoof	Spoofed IP packet flood

## Layer 4 - Transport
Attack Name	Description
syn_flood	TCP SYN flood
syn_ack	TCP SYN-ACK flood
ack_flood	TCP ACK flood
udp_flood	UDP flood
udp_amp	UDP amplification simulation

## Layer 7 - Application
Attack Name	Description
http_flood	HTTP GET/POST flood
slowloris	Slowloris — partial headers
slow_post	Slow POST body trickle
ssl_reneg	SSL renegotiation flood

# Special Mode Attacks
Attack	Description
layer3	Run all Layer 3 attacks simultaneously
layer4	Run all Layer 4 attacks simultaneously
layer7	Run all Layer 7 attacks simultaneously
all	Run all attacks sequentially
full	Full multi-layer assault (L3+L4+L7 all at once)

# Dashboard
The live dashboard shows:

Target Information: URL, host, resolved IP, port
Target Status: Alive / Slow / Degraded / Down with HTTP status codes and response times
Attack Statistics: Packets sent, failed, current rate (pkt/s), success percentage
Timing: Elapsed time, remaining time, progress bar
Events: Real-time status events (recovery, downtime, rate updates)

# Author
Hacker00X1 — Authorized penetration testing tool

# Disclaimer
## This tool is provided for educational purposes and authorized security testing only. The author assumes no liability for any misuse or damage caused by this tool. Users are responsible for complying with all applicable laws and obtaining proper authorization before testing any system.
