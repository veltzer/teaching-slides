# Wireshark Network Analysis (Optional)
## Packet Capture, Filtering, and Protocol Analysis

---
## What is Wireshark?

- Graphical network protocol analyzer
- Captures and inspects packets in real time
- Supports hundreds of protocols
- Available on `Linux`, `Windows`, `macOS`

```bash
# Install
apt install wireshark

# Allow non-root capture
dpkg-reconfigure wireshark-common
usermod -aG wireshark alice
# Log out and back in for group to take effect
```

---
## Wireshark vs tcpdump

| Feature | `Wireshark` | `tcpdump` |
|---------|-------------|-----------|
| Interface | GUI | CLI |
| Protocol decoding | Deep, hundreds of protocols | Basic |
| Filtering | Display + capture filters | Capture filters only |
| Analysis tools | Built-in (streams, stats) | Manual |
| Performance | Higher overhead | Lightweight |
| Remote servers | Needs X forwarding or file transfer | Native |

Common workflow: capture with `tcpdump` on server, analyze with `Wireshark` on workstation.

---
## Capturing Packets

```bash
# Start Wireshark GUI
wireshark &

# Command-line capture with tshark
tshark -i eth0

# Capture to file
tshark -i eth0 -w capture.pcap

# Capture with filter
tshark -i eth0 -f "port 80"

# Capture N packets
tshark -i eth0 -c 100 -w sample.pcap

# Ring buffer (rotate files)
tshark -i eth0 -b filesize:10000 -b files:5 \
  -w rotating.pcap
```

---
## Capture Filters (BPF Syntax)

Capture filters use Berkeley Packet Filter syntax (same as `tcpdump`):

```text
# By host
host 192.168.1.100
src host 10.0.0.5
dst host 10.0.0.10

# By port
port 80
port 443 or port 8080
src port 53

# By protocol
tcp
udp
icmp

# Combined
tcp port 80 and host 192.168.1.100
not arp and not icmp
tcp and (port 80 or port 443)
```

---
## Display Filters

Display filters are applied after capture for analysis. More powerful than capture filters:

```text
# By IP
ip.addr == 192.168.1.100
ip.src == 10.0.0.5
ip.dst == 10.0.0.10

# By port
tcp.port == 80
tcp.dstport == 443
udp.port == 53

# By protocol
http
dns
tls
ssh

# HTTP specific
http.request.method == "GET"
http.response.code == 404
http.host contains "example.com"
```

---
## Advanced Display Filters

```text
# TCP flags
tcp.flags.syn == 1
tcp.flags.rst == 1
tcp.flags.fin == 1

# TCP analysis
tcp.analysis.retransmission
tcp.analysis.duplicate_ack
tcp.analysis.zero_window

# DNS queries
dns.qry.name == "example.com"
dns.qry.type == 1         # A record

# TLS
tls.handshake.type == 1   # Client Hello
tls.record.version == 0x0303  # TLS 1.2

# Combine with logic
(http or dns) and ip.addr == 10.0.0.5
tcp.port == 80 && !tcp.flags.syn
```

---
## tshark: Command-Line Wireshark

```bash
# Read a capture file
tshark -r capture.pcap

# Apply display filter
tshark -r capture.pcap -Y "http.request"

# Show specific fields
tshark -r capture.pcap -Y "http.request" \
  -T fields -e http.host -e http.request.uri

# DNS queries
tshark -r capture.pcap -Y "dns.qry.name" \
  -T fields -e dns.qry.name

# Statistics: protocol hierarchy
tshark -r capture.pcap -q -z io,phs

# Statistics: conversations
tshark -r capture.pcap -q -z conv,tcp

# Statistics: endpoints
tshark -r capture.pcap -q -z endpoints,ip
```

---
## Following TCP Streams

One of `Wireshark`'s most powerful features:

```bash
# Follow TCP stream in tshark
tshark -r capture.pcap -q \
  -z follow,tcp,ascii,0

# Follow specific stream by index
tshark -r capture.pcap -q \
  -z follow,tcp,ascii,5

# Follow HTTP stream
tshark -r capture.pcap -q \
  -z follow,http,ascii,0
```

In the GUI:
1. Right-click a packet in a TCP connection
1. Select "Follow" -> "TCP Stream"
1. View the complete conversation in a single window
1. Use stream index to navigate between conversations

---
## Wireshark Statistics and Analysis

```bash
# Protocol hierarchy
tshark -r capture.pcap -q -z io,phs

# Top talkers
tshark -r capture.pcap -q -z endpoints,ip

# Conversation list
tshark -r capture.pcap -q -z conv,tcp

# HTTP request/response stats
tshark -r capture.pcap -q -z http,tree

# DNS response times
tshark -r capture.pcap -q -z dns,tree

# I/O graph data (packets per interval)
tshark -r capture.pcap -q \
  -z io,stat,1,"COUNT(frame)"
```

---
## Analyzing Common Issues

**Slow connections:**

```text
# Find retransmissions
tcp.analysis.retransmission

# Find high latency
tcp.analysis.ack_rtt > 0.5

# Find zero windows (receiver buffer full)
tcp.analysis.zero_window
```

**DNS problems:**

```text
# Failed DNS queries
dns.flags.rcode != 0

# Slow DNS responses
dns.time > 1
```

**TLS issues:**

```text
# TLS handshake failures
tls.alert.message

# View certificate details
tls.handshake.certificate
```

---
## Remote Capture Workflows

```bash
# Capture on remote server, analyze locally
# Option 1: capture to file, transfer
ssh server "tcpdump -i eth0 -w - -c 1000" > remote.pcap
wireshark remote.pcap

# Option 2: live remote capture via pipe
ssh server "tcpdump -i eth0 -w - -U" | \
  wireshark -k -i -

# Option 3: capture with tshark, analyze later
ssh server "tshark -i eth0 -w /tmp/cap.pcap -c 5000"
scp server:/tmp/cap.pcap .
wireshark cap.pcap

# Option 4: sshdump (Wireshark extcap)
# Configure in Wireshark: Capture -> Options
# Select "SSH remote capture" interface
```

---
## Wireshark Security Considerations

- Running `Wireshark` as `root` is a security risk
    - Use the `wireshark` group for non-root capture
- Packet captures may contain sensitive data
    - Passwords, tokens, personal data
    - Handle capture files as confidential
- Only capture on networks you are authorized to monitor
- Be aware of legal requirements (GDPR, company policy)

```bash
# Sanitize capture files before sharing
editcap -r capture.pcap sanitized.pcap 1-100

# Remove payload, keep headers only
tshark -r capture.pcap -w headers.pcap \
  -F pcap --capture-comment "headers only"
```

---
## Wireshark Best Practices

1. Use capture filters to limit volume
1. Capture to file, not live display (for performance)
1. Use ring buffers for long captures
1. Apply display filters for analysis, not capture filters
1. Learn to follow TCP streams for troubleshooting
1. Use `tshark` on servers, `Wireshark` GUI for analysis
1. Keep capture files organized with timestamps
1. Document findings with packet annotations

```bash
# Practical troubleshooting workflow
# 1. Reproduce the issue
# 2. Capture relevant traffic
tshark -i eth0 -f "host problem-server" -w issue.pcap
# 3. Analyze with display filters
# 4. Follow streams to understand the conversation
# 5. Check statistics for anomalies
```

---
## Wireshark Coloring Rules

Coloring rules highlight packets visually for faster analysis:

```text
# Built-in colors (Edit -> Coloring Rules)
# Green background: HTTP traffic
# Light blue: DNS
# Red: TCP errors (RST, retransmissions)
# Black on yellow: TCP warnings
```

```bash
# Export coloring rules
tshark -r capture.pcap -T fields \
  -e frame.coloring_rule.name

# Custom coloring rule examples (in GUI):
# Name: "Slow DNS"
# Filter: dns.time > 0.5
# Background: orange

# Name: "Failed HTTP"
# Filter: http.response.code >= 400
# Background: red, Foreground: white
```

Coloring rules are evaluated top-to-bottom. First match wins.
Save custom rules to share across team members.

---
## IO Graphs

IO Graphs visualize traffic patterns over time:

```bash
# CLI equivalent: packets per second
tshark -r capture.pcap -q \
  -z io,stat,1,"COUNT(frame)"

# Filtered IO stats: HTTP vs DNS traffic
tshark -r capture.pcap -q \
  -z io,stat,1,"COUNT(frame)http","COUNT(frame)dns"

# Bytes per second
tshark -r capture.pcap -q \
  -z io,stat,1,"BYTES()frame"

# TCP retransmissions over time
tshark -r capture.pcap -q \
  -z io,stat,1,"COUNT(frame)tcp.analysis.retransmission"
```

In the GUI: Statistics -> IO Graphs
- Add multiple graph lines with different display filters
- Compare normal vs problematic traffic patterns
- Identify traffic spikes and anomalies

---
## Expert Information

`Wireshark` Expert Information flags potential problems automatically:

```bash
# View expert info via tshark
tshark -r capture.pcap -q -z expert

# Filter by severity in display filter
# Errors (red)
expert.severity == error
# Warnings (yellow)
expert.severity == warn
# Notes (cyan)
expert.severity == note
```

Common expert info messages:
| Severity | Message | Meaning |
|----------|---------|---------|
| Error | `Malformed Packet` | Protocol parsing failed |
| Warning | `TCP Retransmission` | Packet was resent |
| Warning | `TCP Zero Window` | Receiver buffer full |
| Note | `TCP Keep-Alive` | Connection idle probe |
| Chat | `TCP Window Update` | Normal operation |

In the GUI: Analyze -> Expert Information

---
## Decrypting TLS with Pre-Master Secret

Decrypt `HTTPS` traffic by logging the `TLS` session keys:

```bash
# Set environment variable before starting browser
export SSLKEYLOGFILE=~/tls-keys.log
firefox &
# or
google-chrome &

# The browser logs TLS keys to the file
# Configure Wireshark to use them:
# Edit -> Preferences -> Protocols -> TLS
# -> (Pre)-Master-Secret log filename: ~/tls-keys.log
```

```bash
# Decrypt with tshark
tshark -r capture.pcap \
  -o tls.keylog_file:~/tls-keys.log \
  -Y "http" -T fields \
  -e http.host -e http.request.uri
```

Important notes:
- Only works for sessions captured while logging was active
- Key log file contains sensitive secrets - delete after use
- Works with `TLS` 1.2 and 1.3
- Does not require the server private key

---
## Wireshark Profiles

Profiles store display settings, filters, and coloring rules:

```text
# Create a profile in GUI:
# Edit -> Configuration Profiles -> New
# Each profile stores:
# - Display filter buttons
# - Coloring rules
# - Column layout
# - Protocol preferences
# - Name resolution settings
```

```bash
# Profiles are stored in:
ls ~/.config/wireshark/profiles/

# Copy a profile for sharing
cp -r ~/.config/wireshark/profiles/myprofile \
  /shared/wireshark-profiles/

# Launch with a specific profile
wireshark -C "DNS-Debug" capture.pcap
tshark -C "DNS-Debug" -r capture.pcap
```

Recommended profiles:
- **HTTP Debug**: columns for method, host, status, response time
- **DNS Analysis**: columns for query name, type, response code, latency
- **TCP Troubleshooting**: coloring for retransmissions, resets, zero windows

---
## Packet Injection Detection

Detect suspicious or injected packets on the network:

```text
# Detect TCP RST injection (censorship/MITM)
tcp.flags.rst == 1 && tcp.window_size == 0

# Find duplicate packets with different TTL
# (possible injection - legitimate retransmits
# have same TTL)
tcp.analysis.retransmission

# Detect ARP spoofing
arp.duplicate-address-detected

# Find rogue DHCP servers
bootp.type == 2
# Check multiple source IPs for DHCP offers

# Detect DNS spoofing (duplicate responses)
dns.flags.response == 1
# Look for multiple answers to same query
# with different IPs
```

```bash
# Monitor for ARP anomalies with tshark
tshark -i eth0 -Y "arp.duplicate-address-detected" \
  -T fields -e arp.src.hw_mac -e arp.src.proto_ipv4

# Alert on TCP RST floods
tshark -i eth0 -Y "tcp.flags.rst==1" \
  -q -z io,stat,10,"COUNT(frame)tcp.flags.rst==1"
```

---
## Wireshark Command-Line One-Liners

Useful `tshark` one-liners for quick analysis:

```bash
# Top 10 talkers by packet count
tshark -r capture.pcap -q -z endpoints,ip | \
  sort -t'|' -k3 -rn | head -10

# Extract all HTTP URLs from a capture
tshark -r capture.pcap -Y "http.request" \
  -T fields -e http.host -e http.request.uri | \
  sort -u

# List all unique DNS queries
tshark -r capture.pcap -Y "dns.flags.response==0" \
  -T fields -e dns.qry.name | sort -u

# Show TLS Server Name Indication (SNI) values
tshark -r capture.pcap \
  -Y "tls.handshake.extensions_server_name" \
  -T fields -e tls.handshake.extensions_server_name

# Count packets per protocol
tshark -r capture.pcap -q -z io,phs | \
  grep -E "^\s+[a-z]"

# Extract files transferred via HTTP
tshark -r capture.pcap --export-objects http,/tmp/extracted/
```

---
## `mergecap` and `editcap` Utilities

Manipulate capture files from the command line:

```bash
# Merge multiple capture files
mergecap -w combined.pcap file1.pcap file2.pcap

# Merge and sort by timestamp
mergecap -w sorted.pcap -a file1.pcap file2.pcap

# Extract a time range from a capture
editcap -A "2026-03-24 10:00:00" \
  -B "2026-03-24 10:05:00" \
  capture.pcap timerange.pcap

# Extract specific packets by number
editcap -r capture.pcap subset.pcap 1-100 500-600

# Split a large capture into smaller files
editcap -c 10000 capture.pcap split.pcap
# Creates split_00001.pcap, split_00002.pcap, ...

# Remove duplicate packets
editcap -d capture.pcap deduped.pcap

# Convert between capture formats
editcap -F pcapng capture.pcap capture.pcapng

# Truncate packets to N bytes (strip payload)
editcap -s 64 capture.pcap headers-only.pcap
```

---
## Wireless Packet Capture

Capture Wi-Fi traffic including management and control frames:

```bash
# Check wireless interface capabilities
iw list | grep -A5 "Supported interface modes"

# Enable monitor mode
ip link set wlan0 down
iw wlan0 set monitor control
ip link set wlan0 up

# Set the channel to capture
iw wlan0 set channel 6

# Capture wireless frames with tshark
tshark -i wlan0 -w wifi-capture.pcap

# Capture only beacon frames (SSID discovery)
tshark -i wlan0 -Y "wlan.fc.type_subtype == 0x08" \
  -T fields -e wlan.ssid -e wlan.bssid
```

```bash
# Useful wireless display filters
# All management frames
wlan.fc.type == 0

# Authentication and deauthentication
wlan.fc.type_subtype == 0x0b
wlan.fc.type_subtype == 0x0c

# Probe requests (device discovery)
wlan.fc.type_subtype == 0x04

# Restore managed mode when done
ip link set wlan0 down
iw wlan0 set type managed
ip link set wlan0 up
```

---
## Exercise: Network Troubleshooting with Wireshark

Diagnose a simulated application performance problem:

1. Generate test traffic and capture it:

```bash
# Start capture in background
tshark -i lo -w /tmp/exercise.pcap &
TSHARK_PID=$!

# Generate HTTP traffic
curl -s http://localhost/ > /dev/null
curl -s http://localhost/api > /dev/null

# Generate DNS traffic
dig example.com
dig nonexistent.invalid

# Stop capture
kill $TSHARK_PID
```

1. Analyze the capture:
    - Use `tshark -r /tmp/exercise.pcap -q -z io,phs` to view protocol distribution
    - Extract all HTTP request/response pairs with status codes
    - Find any DNS failures using `dns.flags.rcode != 0`

1. Merge two capture files with `mergecap` and extract a 30-second window with `editcap`
1. Use `tshark` to produce a CSV of all TCP conversations sorted by duration:

```bash
tshark -r /tmp/exercise.pcap -q -z conv,tcp
```

1. Identify any retransmissions or TCP anomalies in the capture using the expert info feature
