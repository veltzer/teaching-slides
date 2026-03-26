# Networking Basics
## Understanding UNIX Network Configuration and Tools
---
## The Client/Server Model

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_09_networking_basics)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd0_09_networking_basics)"/>
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
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_09_networking_basics)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_09_networking_basics)"/>
  <defs>
    <marker id="arrowd1_09_networking_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
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
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_09_networking_basics)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_09_networking_basics)"/>
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
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_09_networking_basics)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_09_networking_basics)"/>
  <defs>
    <marker id="arrowd3_09_networking_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
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

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_09_networking_basics)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd4_09_networking_basics)"/>
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
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_09_networking_basics)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_09_networking_basics)"/>
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
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_09_networking_basics)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_09_networking_basics)"/>
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
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_09_networking_basics)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_09_networking_basics)"/>
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
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd8_09_networking_basics)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd8_09_networking_basics)"/>
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
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd9_09_networking_basics)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd9_09_networking_basics)"/>
  <defs>
    <marker id="arrowd9_09_networking_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Key points:
- Always use encrypted protocols
- Regularly update system
- Monitor access attempts
- Maintain secure configurations
- Keep backups
