# Networking Basics
## Understanding UNIX Network Configuration and Tools
---
## The Client/Server Model

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="60" width="120" height="80" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="95" text-anchor="middle" font-size="12" font-weight="bold">Client</text>
  <text x="90" y="115" text-anchor="middle" font-size="10">Browser / App</text>
  <rect x="450" y="60" width="120" height="80" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="95" text-anchor="middle" font-size="12" font-weight="bold">Server</text>
  <text x="510" y="115" text-anchor="middle" font-size="10">HTTP / SSH / FTP</text>
  <line x1="150" y1="85" x2="450" y2="85" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_09_networking_basics)"/>
  <text x="300" y="78" text-anchor="middle" font-size="10" fill="#1565c0">Request (SYN)</text>
  <line x1="450" y1="120" x2="150" y2="120" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd0_09_networking_basics)"/>
  <text x="300" y="138" text-anchor="middle" font-size="10" fill="#7b1fa2">Response (SYN-ACK)</text>
  <rect x="210" y="155" width="180" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="175" text-anchor="middle" font-size="10">TCP/IP Connection (Port)</text>
  <defs>
    <marker id="arrowd0_09_networking_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Common examples:
- Web servers (HTTP)
- File transfer (FTP)
- Remote login (SSH)
- Email (SMTP/POP3)
---
## Network Interface Configuration

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="30" width="110" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="75" y="52" text-anchor="middle" font-size="11" font-weight="bold">eth0</text>
  <text x="75" y="68" text-anchor="middle" font-size="9">192.168.1.10</text>
  <rect x="170" y="30" width="110" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="225" y="52" text-anchor="middle" font-size="11" font-weight="bold">wlan0</text>
  <text x="225" y="68" text-anchor="middle" font-size="9">192.168.1.20</text>
  <rect x="320" y="30" width="110" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="375" y="52" text-anchor="middle" font-size="11" font-weight="bold">lo</text>
  <text x="375" y="68" text-anchor="middle" font-size="9">127.0.0.1</text>
  <rect x="470" y="30" width="110" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="525" y="52" text-anchor="middle" font-size="11" font-weight="bold">docker0</text>
  <text x="525" y="68" text-anchor="middle" font-size="9">172.17.0.1</text>
  <rect x="100" y="120" width="400" height="45" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="140" text-anchor="middle" font-size="11" font-weight="bold">Linux Kernel Network Stack</text>
  <text x="300" y="155" text-anchor="middle" font-size="9">ifconfig / ip addr show</text>
  <line x1="75" y1="80" x2="200" y2="120" stroke="#333" stroke-width="1"/>
  <line x1="225" y1="80" x2="275" y2="120" stroke="#333" stroke-width="1"/>
  <line x1="375" y1="80" x2="350" y2="120" stroke="#333" stroke-width="1"/>
  <line x1="525" y1="80" x2="425" y2="120" stroke="#333" stroke-width="1"/>
</svg>

Using ifconfig:

```bash
# Show all interfaces
ifconfig

# Configure interface
ifconfig eth0 192.168.1.100 netmask 255.255.255.0

# Enable/disable interface
ifconfig eth0 up
ifconfig eth0 down
```

---
## Modern IP Command

```bash
# Show IP addresses
ip addr show

# Add IP address
ip addr add 192.168.1.100/24 dev eth0

# Delete IP address
ip addr del 192.168.1.100/24 dev eth0

# Show routing
ip route show

# Add route
ip route add default via 192.168.1.1
```

---
## Interface Management

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="20" width="130" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="45" text-anchor="middle" font-size="11" font-weight="bold">eth0 (UP)</text>
  <text x="95" y="62" text-anchor="middle" font-size="9" fill="#2e7d32">RUNNING, MTU 1500</text>
  <rect x="235" y="20" width="130" height="60" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="45" text-anchor="middle" font-size="11" font-weight="bold">eth0 (DOWN)</text>
  <text x="300" y="62" text-anchor="middle" font-size="9" fill="#c62828">NOT RUNNING</text>
  <rect x="440" y="20" width="130" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="45" text-anchor="middle" font-size="11" font-weight="bold">eth0 (CONFIG)</text>
  <text x="505" y="62" text-anchor="middle" font-size="9" fill="#1565c0">Assigning IP...</text>
  <line x1="160" y1="50" x2="235" y2="50" stroke="#c62828" stroke-width="2" marker-end="url(#arrowd2_09_networking_basics)"/>
  <text x="197" y="42" text-anchor="middle" font-size="9">ifdown</text>
  <line x1="365" y1="50" x2="440" y2="50" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd2_09_networking_basics)"/>
  <text x="402" y="42" text-anchor="middle" font-size="9">ifup</text>
  <line x1="440" y1="70" x2="160" y2="70" stroke="#2e7d32" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd2_09_networking_basics)"/>
  <text x="300" y="90" text-anchor="middle" font-size="9" fill="#2e7d32">configured and running</text>
  <rect x="100" y="130" width="400" height="50" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="150" text-anchor="middle" font-size="11" font-weight="bold">Interface Lifecycle</text>
  <text x="300" y="168" text-anchor="middle" font-size="10">ifup / ifdown / ifconfig / ip link set</text>
  <defs>
    <marker id="arrowd2_09_networking_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Basic commands:

```bash
# Bring interface up
ifup eth0

# Bring interface down
ifdown eth0

# Check status
ifconfig eth0
ip link show eth0
```

---
## Network Statistics (netstat)

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="10" width="170" height="80" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="30" text-anchor="middle" font-size="11" font-weight="bold">Active Connections</text>
  <text x="105" y="48" text-anchor="middle" font-size="9">tcp  0.0.0.0:80  LISTEN</text>
  <text x="105" y="62" text-anchor="middle" font-size="9">tcp  :22  ESTABLISHED</text>
  <text x="105" y="76" text-anchor="middle" font-size="9">udp  0.0.0.0:53  *</text>
  <rect x="215" y="10" width="170" height="80" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="30" text-anchor="middle" font-size="11" font-weight="bold">Routing Table</text>
  <text x="300" y="48" text-anchor="middle" font-size="9">0.0.0.0 -> 192.168.1.1</text>
  <text x="300" y="62" text-anchor="middle" font-size="9">192.168.1.0/24 dev eth0</text>
  <text x="300" y="76" text-anchor="middle" font-size="9">172.17.0.0/16 dev docker0</text>
  <rect x="410" y="10" width="170" height="80" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="30" text-anchor="middle" font-size="11" font-weight="bold">Statistics</text>
  <text x="495" y="48" text-anchor="middle" font-size="9">TCP: 15 active</text>
  <text x="495" y="62" text-anchor="middle" font-size="9">UDP: 3 active</text>
  <text x="495" y="76" text-anchor="middle" font-size="9">ICMP: 0 errors</text>
  <rect x="100" y="120" width="400" height="60" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="142" text-anchor="middle" font-size="12" font-weight="bold">netstat / ss</text>
  <text x="300" y="162" text-anchor="middle" font-size="10">-t (TCP) | -u (UDP) | -l (listening) | -r (routes) | -s (stats)</text>
</svg>

Common options:

```bash
# Show all connections
netstat -a

# Show TCP connections
netstat -t

# Show listening ports
netstat -l

# Show statistics
netstat -s

# Show routing table
netstat -r
```

---
## SSH (Secure Shell)

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="30" width="120" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="55" text-anchor="middle" font-size="12" font-weight="bold">SSH Client</text>
  <text x="90" y="72" text-anchor="middle" font-size="9">~/.ssh/config</text>
  <rect x="450" y="30" width="120" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="55" text-anchor="middle" font-size="12" font-weight="bold">SSH Server</text>
  <text x="510" y="72" text-anchor="middle" font-size="9">sshd (port 22)</text>
  <line x1="150" y1="50" x2="450" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_09_networking_basics)"/>
  <text x="300" y="43" text-anchor="middle" font-size="10" fill="#1565c0">Key Exchange / Auth</text>
  <line x1="450" y1="75" x2="150" y2="75" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd4_09_networking_basics)"/>
  <text x="300" y="96" text-anchor="middle" font-size="10" fill="#7b1fa2">Encrypted Channel</text>
  <rect x="180" y="130" width="240" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="152" text-anchor="middle" font-size="11" font-weight="bold">Encrypted Tunnel</text>
  <text x="300" y="168" text-anchor="middle" font-size="9">AES-256 / ChaCha20</text>
  <defs>
    <marker id="arrowd4_09_networking_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Basic usage:

```bash
# Connect to remote host
ssh user@remote.host

# Use specific port
ssh -p 2222 user@remote.host

# Run remote command
ssh user@remote.host 'ls -l'
```

---
## SSH Configuration and Keys

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="150" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="42" text-anchor="middle" font-size="11" font-weight="bold">ssh-keygen</text>
  <text x="95" y="58" text-anchor="middle" font-size="9">id_rsa (private)</text>
  <text x="95" y="72" text-anchor="middle" font-size="9">id_rsa.pub (public)</text>
  <rect x="225" y="20" width="150" height="70" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="42" text-anchor="middle" font-size="11" font-weight="bold">ssh-copy-id</text>
  <text x="300" y="58" text-anchor="middle" font-size="9">Copies public key</text>
  <text x="300" y="72" text-anchor="middle" font-size="9">to remote server</text>
  <rect x="430" y="20" width="150" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="42" text-anchor="middle" font-size="11" font-weight="bold">authorized_keys</text>
  <text x="505" y="58" text-anchor="middle" font-size="9">~/.ssh/authorized_keys</text>
  <text x="505" y="72" text-anchor="middle" font-size="9">on remote server</text>
  <line x1="170" y1="55" x2="225" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_09_networking_basics)"/>
  <line x1="375" y1="55" x2="430" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_09_networking_basics)"/>
  <rect x="100" y="120" width="400" height="55" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="142" text-anchor="middle" font-size="11" font-weight="bold">~/.ssh/config</text>
  <text x="300" y="160" text-anchor="middle" font-size="10">Host aliases, port, user, identity file</text>
  <defs>
    <marker id="arrowd5_09_networking_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Key management:

```bash
# Generate key pair
ssh-keygen -t rsa -b 4096

# Copy public key to server
ssh-copy-id user@remote.host

# SSH config file
Host server1
    HostName remote.host
    User username
    Port 2222
```

---
## Remote File Transfer

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="40" width="120" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="62" text-anchor="middle" font-size="11" font-weight="bold">Local Host</text>
  <text x="80" y="78" text-anchor="middle" font-size="9">file.txt</text>
  <rect x="240" y="15" width="120" height="45" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="35" text-anchor="middle" font-size="11" font-weight="bold">scp</text>
  <text x="300" y="50" text-anchor="middle" font-size="9">Secure Copy</text>
  <rect x="240" y="75" width="120" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="95" text-anchor="middle" font-size="11" font-weight="bold">rsync</text>
  <text x="300" y="110" text-anchor="middle" font-size="9">Delta Sync</text>
  <rect x="460" y="40" width="120" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="520" y="62" text-anchor="middle" font-size="11" font-weight="bold">Remote Host</text>
  <text x="520" y="78" text-anchor="middle" font-size="9">~/backup/</text>
  <line x1="140" y1="55" x2="240" y2="37" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_09_networking_basics)"/>
  <line x1="360" y1="37" x2="460" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_09_networking_basics)"/>
  <line x1="140" y1="80" x2="240" y2="97" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_09_networking_basics)"/>
  <line x1="360" y1="97" x2="460" y2="80" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_09_networking_basics)"/>
  <rect x="150" y="145" width="300" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="162" text-anchor="middle" font-size="10" font-weight="bold">Encrypted SSH Tunnel (port 22)</text>
  <text x="300" y="177" text-anchor="middle" font-size="9">scp, rsync -e ssh, sftp</text>
  <defs>
    <marker id="arrowd6_09_networking_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Examples:

```bash
# Copy file to remote
scp file.txt user@remote.host:~/

# Copy from remote
scp user@remote.host:file.txt .

# Sync directories
rsync -av local/ user@remote.host:backup/
```

---
## Legacy Remote Commands

```bash
# Remote login
rlogin remote.host

# Remote copy
rcp file remote.host:

# Remote shell
rsh remote.host command

# Remote execution
rexec remote.host command
```

Note: These commands are insecure and should be avoided in favor of SSH.

---
## Trust Relationships

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="130" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="42" text-anchor="middle" font-size="11" font-weight="bold">Host A</text>
  <text x="85" y="58" text-anchor="middle" font-size="9">~/.ssh/known_hosts</text>
  <text x="85" y="72" text-anchor="middle" font-size="9">~/.rhosts (legacy)</text>
  <rect x="235" y="20" width="130" height="70" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="42" text-anchor="middle" font-size="11" font-weight="bold">Trust Chain</text>
  <text x="300" y="58" text-anchor="middle" font-size="9">Public Key Auth</text>
  <text x="300" y="72" text-anchor="middle" font-size="9">Host Verification</text>
  <rect x="450" y="20" width="130" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="515" y="42" text-anchor="middle" font-size="11" font-weight="bold">Host B</text>
  <text x="515" y="58" text-anchor="middle" font-size="9">authorized_keys</text>
  <text x="515" y="72" text-anchor="middle" font-size="9">hosts.equiv (legacy)</text>
  <line x1="150" y1="55" x2="235" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_09_networking_basics)"/>
  <line x1="365" y1="55" x2="450" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_09_networking_basics)"/>
  <rect x="50" y="120" width="220" height="55" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="160" y="140" text-anchor="middle" font-size="10" font-weight="bold">Legacy (INSECURE)</text>
  <text x="160" y="160" text-anchor="middle" font-size="9">.rhosts, hosts.equiv, rlogin</text>
  <rect x="330" y="120" width="220" height="55" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="440" y="140" text-anchor="middle" font-size="10" font-weight="bold">Modern (SECURE)</text>
  <text x="440" y="160" text-anchor="middle" font-size="9">SSH keys, authorized_keys</text>
  <defs>
    <marker id="arrowd7_09_networking_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Configuration files:

```bash
# System-wide trust
/etc/hosts.equiv

# User-specific trust
~/.rhosts

# SSH trust
~/.ssh/authorized_keys
```

---
## Network Troubleshooting

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="90" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="65" y="42" text-anchor="middle" font-size="10" font-weight="bold">Local</text>
  <text x="65" y="56" text-anchor="middle" font-size="9">ping</text>
  <rect x="135" y="20" width="90" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="180" y="42" text-anchor="middle" font-size="10" font-weight="bold">Router 1</text>
  <text x="180" y="56" text-anchor="middle" font-size="9">hop 1</text>
  <rect x="250" y="20" width="90" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="295" y="42" text-anchor="middle" font-size="10" font-weight="bold">Router 2</text>
  <text x="295" y="56" text-anchor="middle" font-size="9">hop 2</text>
  <rect x="365" y="20" width="90" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="410" y="42" text-anchor="middle" font-size="10" font-weight="bold">Router 3</text>
  <text x="410" y="56" text-anchor="middle" font-size="9">hop 3</text>
  <rect x="480" y="20" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="530" y="42" text-anchor="middle" font-size="10" font-weight="bold">Destination</text>
  <text x="530" y="56" text-anchor="middle" font-size="9">google.com</text>
  <line x1="110" y1="45" x2="135" y2="45" stroke="#333" stroke-width="2" marker-end="url(#arrowd8_09_networking_basics)"/>
  <line x1="225" y1="45" x2="250" y2="45" stroke="#333" stroke-width="2" marker-end="url(#arrowd8_09_networking_basics)"/>
  <line x1="340" y1="45" x2="365" y2="45" stroke="#333" stroke-width="2" marker-end="url(#arrowd8_09_networking_basics)"/>
  <line x1="455" y1="45" x2="480" y2="45" stroke="#333" stroke-width="2" marker-end="url(#arrowd8_09_networking_basics)"/>
  <rect x="50" y="90" width="500" height="30" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="110" text-anchor="middle" font-size="10">traceroute: shows each hop with latency (ms)</text>
  <rect x="50" y="135" width="240" height="45" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="170" y="155" text-anchor="middle" font-size="10" font-weight="bold">ping / traceroute</text>
  <text x="170" y="170" text-anchor="middle" font-size="9">ICMP echo, TTL probing</text>
  <rect x="310" y="135" width="240" height="45" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="430" y="155" text-anchor="middle" font-size="10" font-weight="bold">dig / nslookup</text>
  <text x="430" y="170" text-anchor="middle" font-size="9">DNS resolution debugging</text>
  <defs>
    <marker id="arrowd8_09_networking_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Common commands:

```bash
# Test connectivity
ping google.com

# Trace route
traceroute google.com

# DNS lookup
dig google.com
nslookup google.com

# Packet capture
tcpdump -i eth0
```

---
## Network Security Basics

```bash
# Check open ports
netstat -tuln

# Configure firewall
iptables -L
ufw status

# Check SSH access attempts
tail -f /var/log/auth.log

# Monitor network traffic
iftop -i eth0
```

---
## Practical Examples

1. Remote Server Setup:

```bash
# Generate SSH key
ssh-keygen -t rsa

# Copy key to server
ssh-copy-id user@server

# Create SSH config
cat >> ~/.ssh/config << EOF
Host myserver
    HostName server.example.com
    User admin
    Port 2222
EOF
```

1. File Synchronization:

```bash
# Sync with remote
rsync -avz --progress /local/dir/ \
    user@remote:/backup/
```

---
## Best Practices

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="170" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="42" text-anchor="middle" font-size="11" font-weight="bold">Use SSH/SCP</text>
  <text x="105" y="60" text-anchor="middle" font-size="9">Encrypted connections</text>
  <rect x="215" y="20" width="170" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="42" text-anchor="middle" font-size="11" font-weight="bold">Key-Based Auth</text>
  <text x="300" y="60" text-anchor="middle" font-size="9">Disable password login</text>
  <rect x="410" y="20" width="170" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="42" text-anchor="middle" font-size="11" font-weight="bold">Firewall Rules</text>
  <text x="495" y="60" text-anchor="middle" font-size="9">iptables / ufw</text>
  <rect x="20" y="100" width="170" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="122" text-anchor="middle" font-size="11" font-weight="bold">Monitor Logs</text>
  <text x="105" y="140" text-anchor="middle" font-size="9">/var/log/auth.log</text>
  <rect x="215" y="100" width="170" height="55" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="122" text-anchor="middle" font-size="11" font-weight="bold">Avoid Legacy</text>
  <text x="300" y="140" text-anchor="middle" font-size="9">No rlogin/rsh/telnet</text>
  <rect x="410" y="100" width="170" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="122" text-anchor="middle" font-size="11" font-weight="bold">Regular Updates</text>
  <text x="495" y="140" text-anchor="middle" font-size="9">Patch vulnerabilities</text>
</svg>

Key points:
- Always use encrypted protocols
- Regularly update system
- Monitor access attempts
- Maintain secure configurations
- Keep backups
