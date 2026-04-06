# Port Scanning

## Understanding Network Security Vulnerabilities

---
## What is Port Scanning?

- Port scanning is the process of identifying open ports on a computer or network device
- Ports are virtual numbered connections (0-65535) that allow communication between devices
- Different ports are used for different services:

| Port   | Service        | Protocol |
|--------|----------------|----------|
| 21     | FTP            | TCP      |
| 22     | SSH            | TCP      |
| 25     | SMTP           | TCP      |
| 53     | DNS            | TCP/UDP  |
| 80     | HTTP           | TCP      |
| 443    | HTTPS          | TCP      |
| 3306   | MySQL          | TCP      |
| 3389   | RDP            | TCP      |
| 5432   | PostgreSQL     | TCP      |
| 8080   | HTTP Proxy     | TCP      |

---
## Port States

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="210" viewBox="0 0 660 210">
  <rect width="660" height="210" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="28" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">Port States</text>
  <rect x="20" y="45" width="180" height="50" fill="#e3f2fd" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="110" y="65" font-family="sans-serif" font-size="14" font-weight="bold" fill="#1565c0" text-anchor="middle">Open</text>
  <text x="110" y="83" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Service actively listening</text>
  <rect x="240" y="45" width="180" height="50" fill="#e8f5e9" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="65" font-family="sans-serif" font-size="14" font-weight="bold" fill="#2e7d32" text-anchor="middle">Closed</text>
  <text x="330" y="83" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Host reachable, no service</text>
  <rect x="460" y="45" width="180" height="50" fill="#fff3e0" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="550" y="65" font-family="sans-serif" font-size="14" font-weight="bold" fill="#e65100" text-anchor="middle">Filtered</text>
  <text x="550" y="83" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Firewall blocking probe</text>
  <text x="110" y="125" font-family="sans-serif" font-size="12" fill="#1565c0" text-anchor="middle">Responds: SYN-ACK (TCP)</text>
  <text x="330" y="125" font-family="sans-serif" font-size="12" fill="#2e7d32" text-anchor="middle">Responds: RST (TCP)</text>
  <text x="550" y="125" font-family="sans-serif" font-size="12" fill="#e65100" text-anchor="middle">No response / ICMP unreachable</text>
  <line x1="20" y1="150" x2="640" y2="150" stroke="#aaa" stroke-width="1"/>
  <text x="330" y="175" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">Nmap uses probe responses to classify each scanned port into one of these three states</text>
</svg>

- **Open**: Useful for attackers -- exploitable services
- **Closed**: Host is alive but no service on this port
- **Filtered**: A firewall is protecting this port (most secure from attacker's view)

---
## Why Port Scanning is Done

**Offensive (Red Team / Attackers):**
- Identify running services and their versions
- Find vulnerable or misconfigured services
- Map the network topology
- Identify operating systems

**Defensive (Blue Team / Admins):**
- Audit network security posture
- Verify firewall rules are working
- Find unauthorized services
- Compliance validation

---
## Nmap: The Standard Tool

```bash
# Install nmap
sudo apt install nmap          # Debian/Ubuntu
sudo yum install nmap          # RHEL/CentOS
brew install nmap              # macOS

# Basic scan (top 1000 ports)
nmap 192.168.1.1

# Scan specific ports
nmap -p 22,80,443 192.168.1.1

# Scan port range
nmap -p 1-1024 192.168.1.1

# Scan all 65535 ports
nmap -p- 192.168.1.1

# Scan entire subnet
nmap 192.168.1.0/24
```

---
## Nmap Scan Types

### TCP SYN Scan (Half-Open Scan)

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="280" viewBox="0 0 660 280">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <rect width="660" height="280" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="26" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">SYN Scan (-sS) — Default for root</text>
  <rect x="30" y="40" width="100" height="32" fill="#e3f2fd" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="80" y="61" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1565c0" text-anchor="middle">Scanner</text>
  <rect x="530" y="40" width="100" height="32" fill="#e3f2fd" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="580" y="61" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1565c0" text-anchor="middle">Target</text>
  <line x1="80" y1="72" x2="80" y2="260" stroke="#888" stroke-width="1" stroke-dasharray="4,3"/>
  <line x1="580" y1="72" x2="580" y2="260" stroke="#888" stroke-width="1" stroke-dasharray="4,3"/>
  <!-- SYN -->
  <line x1="80" y1="95" x2="570" y2="95" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="330" y="90" font-family="sans-serif" font-size="12" fill="#333" text-anchor="middle">SYN</text>
  <!-- SYN-ACK (open) -->
  <line x1="580" y1="130" x2="90" y2="130" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="330" y="126" font-family="sans-serif" font-size="12" fill="#2e7d32" text-anchor="middle">SYN-ACK → Port OPEN</text>
  <!-- RST back -->
  <line x1="80" y1="155" x2="570" y2="155" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="330" y="151" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">RST (close without completing)</text>
  <!-- RST (closed) -->
  <line x1="580" y1="190" x2="90" y2="190" stroke="#e65100" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="330" y="186" font-family="sans-serif" font-size="12" fill="#e65100" text-anchor="middle">RST → Port CLOSED</text>
  <!-- no response -->
  <text x="330" y="228" font-family="sans-serif" font-size="12" fill="#777" text-anchor="middle" font-style="italic">[no response] → Port FILTERED (firewall dropping)</text>
</svg>

```bash
# SYN scan (requires root, stealthy)
sudo nmap -sS 192.168.1.1
```

- Most popular scan type -- fast and relatively stealthy
- Does not complete the TCP handshake (half-open)
- Less likely to be logged by applications (but IDS will detect it)

---
### TCP Connect Scan

```bash
# TCP Connect scan (no root needed, uses OS connect() call)
nmap -sT 192.168.1.1
```

- Completes the full TCP three-way handshake
- More likely to be logged by the target application
- Only option when user does not have raw packet privileges
- Slower than SYN scan

---
### UDP Scan

```bash
# UDP scan (very slow, requires root)
sudo nmap -sU 192.168.1.1

# Combine TCP SYN and UDP scan
sudo nmap -sS -sU 192.168.1.1

# Scan common UDP ports only
sudo nmap -sU --top-ports 20 192.168.1.1
```

- Sends UDP packets to target ports
- Open ports may or may not respond
- Closed ports respond with ICMP Port Unreachable
- Much slower than TCP scanning (rate limiting of ICMP responses)
- Important: many services use UDP (DNS, SNMP, DHCP, NTP)

---
### Stealth Scans (FIN, NULL, Xmas)

```c
┌──────────────────────────────────────────────────────────┐
│          Stealth Scan Types                               │
│                                                          │
│  FIN Scan (-sF):                                         │
│    Sends TCP packet with only FIN flag set               │
│    Open port: no response                                │
│    Closed port: RST                                      │
│                                                          │
│  NULL Scan (-sN):                                        │
│    Sends TCP packet with no flags set                    │
│    Open port: no response                                │
│    Closed port: RST                                      │
│                                                          │
│  Xmas Scan (-sX):                                        │
│    Sends TCP packet with FIN+PSH+URG flags               │
│    (like a lit-up Christmas tree)                         │
│    Open port: no response                                │
│    Closed port: RST                                      │
│                                                          │
│  NOTE: These do NOT work against Windows systems         │
│  (Windows sends RST regardless of port state)            │
└──────────────────────────────────────────────────────────┘
```

```bash
# FIN scan
sudo nmap -sF 192.168.1.1

# NULL scan
sudo nmap -sN 192.168.1.1

# Xmas scan
sudo nmap -sX 192.168.1.1
```

---
## Scan Type Comparison

| Scan Type    | Flag | Root? | Speed  | Stealth | Works on Windows |
|-------------|------|-------|--------|---------|-----------------|
| SYN (-sS)   | SYN  | Yes   | Fast   | Medium  | Yes             |
| Connect (-sT)| Full | No   | Medium | Low     | Yes             |
| UDP (-sU)   | UDP  | Yes   | Slow   | Medium  | Yes             |
| FIN (-sF)   | FIN  | Yes   | Medium | High    | No              |
| NULL (-sN)  | None | Yes   | Medium | High    | No              |
| Xmas (-sX)  | FPU  | Yes   | Medium | High    | No              |
| ACK (-sA)   | ACK  | Yes   | Fast   | Medium  | Yes             |
| Idle (-sI)  | SYN  | Yes   | Slow   | Highest | Yes             |

---
## Service and Version Detection

```bash
# Service version detection
nmap -sV 192.168.1.1

# Aggressive version detection
nmap -sV --version-intensity 5 192.168.1.1

# Example output:
# PORT     STATE SERVICE     VERSION
# 22/tcp   open  ssh         OpenSSH 8.9p1 Ubuntu 3
# 80/tcp   open  http        Apache httpd 2.4.52
# 443/tcp  open  ssl/http    nginx 1.18.0
# 3306/tcp open  mysql       MySQL 8.0.33
```

- `-sV` probes open ports to determine service and version
- Sends service-specific probes and matches responses against a database
- Critical for vulnerability assessment -- version numbers map to known CVEs

---
## OS Fingerprinting

```bash
# OS detection
sudo nmap -O 192.168.1.1

# Aggressive OS detection with version info
sudo nmap -A 192.168.1.1

# Example output:
# OS details: Linux 5.4 - 5.15
# Network Distance: 1 hop
# TCP Sequence Prediction: Difficulty=261 (Good luck!)
```

- Analyzes TCP/IP stack implementation details
- Examines: TTL values, window sizes, TCP options ordering
- Each OS has a unique "fingerprint" of these values
- `-A` enables OS detection, version detection, script scanning, and traceroute

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="170" viewBox="0 0 660 170">
  <rect width="660" height="170" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="26" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">OS Fingerprinting Characteristics</text>
  <!-- Header row -->
  <rect x="20" y="40" width="165" height="28" fill="#333" rx="2"/>
  <rect x="185" y="40" width="115" height="28" fill="#1565c0" rx="2"/>
  <rect x="300" y="40" width="115" height="28" fill="#1565c0" rx="2"/>
  <rect x="415" y="40" width="225" height="28" fill="#1565c0" rx="2"/>
  <text x="102" y="59" font-family="sans-serif" font-size="13" font-weight="bold" fill="#fff" text-anchor="middle">Characteristic</text>
  <text x="242" y="59" font-family="sans-serif" font-size="13" font-weight="bold" fill="#fff" text-anchor="middle">Linux</text>
  <text x="357" y="59" font-family="sans-serif" font-size="13" font-weight="bold" fill="#fff" text-anchor="middle">Windows</text>
  <text x="527" y="59" font-family="sans-serif" font-size="13" font-weight="bold" fill="#fff" text-anchor="middle">macOS</text>
  <!-- rows -->
  <rect x="20" y="68" width="620" height="24" fill="#fff" rx="1" stroke="#ccc" stroke-width="1"/>
  <rect x="20" y="92" width="620" height="24" fill="#e8f5e9" rx="1" stroke="#ccc" stroke-width="1"/>
  <rect x="20" y="116" width="620" height="24" fill="#fff" rx="1" stroke="#ccc" stroke-width="1"/>
  <rect x="20" y="140" width="620" height="24" fill="#e8f5e9" rx="1" stroke="#ccc" stroke-width="1"/>
  <text x="102" y="84" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Default TTL</text>
  <text x="242" y="84" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">64</text>
  <text x="357" y="84" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">128</text>
  <text x="527" y="84" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">64</text>
  <text x="102" y="108" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Window Size</text>
  <text x="242" y="108" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">5840</text>
  <text x="357" y="108" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">65535</text>
  <text x="527" y="108" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">65535</text>
  <text x="102" y="132" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">DF Flag</text>
  <text x="242" y="132" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Set</text>
  <text x="357" y="132" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Set</text>
  <text x="527" y="132" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Set</text>
  <text x="102" y="156" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">TCP Options</text>
  <text x="242" y="156" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">MSS, SAC</text>
  <text x="357" y="156" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">MSS, NOP</text>
  <text x="527" y="156" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">MSS, WS, SAC</text>
</svg>

---
## Timing Options

```bash
# Timing templates (T0 = slowest, T5 = fastest)
nmap -T0 192.168.1.1    # Paranoid  (IDS evasion, very slow)
nmap -T1 192.168.1.1    # Sneaky    (IDS evasion, slow)
nmap -T2 192.168.1.1    # Polite    (less bandwidth, slower)
nmap -T3 192.168.1.1    # Normal    (default)
nmap -T4 192.168.1.1    # Aggressive (faster, reliable networks)
nmap -T5 192.168.1.1    # Insane    (fastest, may miss ports)

# Custom timing
nmap --min-rate 1000 192.168.1.1      # Min 1000 packets/sec
nmap --max-retries 2 192.168.1.1      # Max 2 retransmissions
nmap --host-timeout 300s 192.168.1.1  # 5 min timeout per host
```

| Template | Probe Timeout | Scan Delay | Parallelism | Use Case          |
|----------|---------------|------------|-------------|-------------------|
| T0       | 5 min         | 5 min      | Serial      | IDS evasion       |
| T1       | 15 sec        | 15 sec     | Serial      | IDS evasion       |
| T2       | 1 sec         | 0.4 sec    | Serial      | Courtesy scan     |
| T3       | 1 sec         | 0           | Parallel    | Default           |
| T4       | 500 ms        | 0           | Parallel    | Fast LAN scan     |
| T5       | 250 ms        | 0           | Parallel    | Speed over accuracy|

---
## Nmap Scripting Engine (NSE)

```bash
# List available scripts
ls /usr/share/nmap/scripts/ | wc -l    # 600+ scripts

# Run default scripts
nmap -sC 192.168.1.1
# Same as: nmap --script=default 192.168.1.1

# Run specific vulnerability scripts
nmap --script vuln 192.168.1.1

# Check for specific vulnerabilities
nmap --script smb-vuln-ms17-010 192.168.1.1   # EternalBlue
nmap --script ssl-heartbleed 192.168.1.1       # Heartbleed
nmap --script http-shellshock 192.168.1.1      # Shellshock

# HTTP enumeration
nmap --script http-enum 192.168.1.1

# Brute force scripts
nmap --script ssh-brute -p 22 192.168.1.1
nmap --script http-brute -p 80 192.168.1.1

# Script categories
nmap --script "safe and discovery" 192.168.1.1
```

### NSE Script Categories

| Category  | Purpose                                    | Example Script           |
|-----------|--------------------------------------------|--------------------------|
| auth      | Authentication bypass/brute force          | ssh-brute                |
| default   | Safe, useful scripts (run with -sC)        | ssh-hostkey              |
| discovery | Enumerate services and information         | http-enum                |
| exploit   | Actively exploit vulnerabilities           | smb-vuln-ms17-010        |
| vuln      | Check for known vulnerabilities            | ssl-heartbleed           |
| safe      | Non-intrusive, won't crash services        | http-headers             |
| intrusive | May crash services or trigger alerts       | http-sql-injection       |

---
## Comprehensive Scan Examples

```bash
# Quick network discovery (ping sweep)
nmap -sn 192.168.1.0/24

# Full audit scan (common in penetration testing)
sudo nmap -sS -sV -sC -O -p- -T4 -oA full_scan 192.168.1.1

# Flags breakdown:
#   -sS       SYN scan
#   -sV       Service version detection
#   -sC       Default scripts
#   -O        OS fingerprinting
#   -p-       All 65535 ports
#   -T4       Aggressive timing
#   -oA       Output in all formats (nmap, xml, greppable)

# Stealthy reconnaissance scan
sudo nmap -sS -T2 -f --data-length 50 \
    --randomize-hosts -D RND:5 192.168.1.0/24

# Flags:
#   -f              Fragment packets
#   --data-length   Append random data to packets
#   --randomize-hosts  Scan hosts in random order
#   -D RND:5        Use 5 random decoy addresses
```

---
## Output Formats

```bash
# Normal output to file
nmap -oN scan_results.txt 192.168.1.1

# XML output (for tools like Metasploit)
nmap -oX scan_results.xml 192.168.1.1

# Greppable output (for scripting)
nmap -oG scan_results.gnmap 192.168.1.1

# All formats at once
nmap -oA scan_results 192.168.1.1
# Creates: scan_results.nmap, scan_results.xml, scan_results.gnmap

# Parse greppable output
grep "open" scan_results.gnmap | \
    awk '{print $2, $4}' | sort
```

---
## Defense: Detecting Port Scans with iptables

```bash
# Log SYN scan attempts
iptables -A INPUT -p tcp --tcp-flags ALL SYN \
    -m limit --limit 1/s --limit-burst 4 \
    -j LOG --log-prefix "SYN_SCAN: "

# Detect and block FIN scan
iptables -A INPUT -p tcp --tcp-flags ALL FIN -j DROP

# Detect and block NULL scan
iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP

# Detect and block Xmas scan
iptables -A INPUT -p tcp \
    --tcp-flags ALL FIN,PSH,URG -j DROP

# Block invalid flag combinations
iptables -A INPUT -p tcp \
    --tcp-flags SYN,FIN SYN,FIN -j DROP
iptables -A INPUT -p tcp \
    --tcp-flags SYN,RST SYN,RST -j DROP

# Rate limit new connections (anti-scan)
iptables -A INPUT -p tcp --syn \
    -m recent --name portscan --set
iptables -A INPUT -p tcp --syn \
    -m recent --name portscan --rcheck \
    --seconds 60 --hitcount 20 -j DROP
```

---
## Defense: IDS/IPS Detection

```bash
# Snort rule examples for port scan detection

# Detect SYN scan (many SYN packets, no ACK follow-up)
# alert tcp $EXTERNAL_NET any -> $HOME_NET any \
#   (msg:"Possible SYN scan"; flags:S; \
#    threshold:type both, track by_src, count 20, seconds 10; \
#    sid:1000001;)

# Detect NULL scan
# alert tcp $EXTERNAL_NET any -> $HOME_NET any \
#   (msg:"NULL scan detected"; flags:0; sid:1000002;)

# Detect Xmas scan
# alert tcp $EXTERNAL_NET any -> $HOME_NET any \
#   (msg:"Xmas scan detected"; flags:FPU; sid:1000003;)

# Tools for port scan detection
# psad    - Port Scan Attack Detector (analyzes iptables logs)
# Snort   - Network IDS
# Suricata - Next-gen IDS/IPS
# fail2ban - Ban IPs with suspicious activity
```

```bash
# Install and configure psad
sudo apt install psad
sudo psad --sig-update
sudo psad -H  # Start in daemon mode

# View psad scan reports
sudo psad --Status
```

---
## Defense: Minimizing Attack Surface

```bash
# List all listening services
ss -tlnp    # TCP listeners
ss -ulnp    # UDP listeners

# Find and disable unnecessary services
sudo systemctl list-units --type=service --state=running

# Disable a service
sudo systemctl disable --now unnecessary-service

# Check for unexpected open ports
sudo nmap -sS -sU localhost

# Use strict firewall (default deny)
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow only necessary inbound traffic
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT   # SSH
iptables -A INPUT -p tcp --dport 80 -j ACCEPT   # HTTP
iptables -A INPUT -p tcp --dport 443 -j ACCEPT  # HTTPS
```

---
## Key Takeaways

- Port scanning is a fundamental reconnaissance technique for both attackers and defenders
- Nmap is the standard tool with numerous scan types for different scenarios
- SYN scan is fastest and most common; UDP scan covers important non-TCP services
- Service detection (-sV) and OS fingerprinting (-O) provide critical intelligence
- NSE scripts automate vulnerability checking against discovered services
- Timing options (-T0 to -T5) balance stealth against speed
- Defend with: firewall rules, IDS/IPS, service minimization, and regular self-scanning
- Know your own attack surface before an attacker maps it for you
