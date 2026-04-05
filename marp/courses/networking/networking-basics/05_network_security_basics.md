# Network Security Basics
## Encryption, Firewalls, and VPNs

---

## Why Network Security Matters

- Data in transit is vulnerable to interception, modification, and impersonation
- Every packet crosses multiple networks and devices you do not control
- Threats range from passive eavesdropping to active man-in-the-middle attacks
- Security must be layered -- no single mechanism is sufficient

```text
┌────────┐                                              ┌────────┐
│ Client │──→ [Your LAN] ──→ [ISP] ──→ [Internet] ──→ │ Server │
└────────┘        ↑            ↑           ↑            └────────┘
              Attacker     Attacker     Attacker
              can sniff    can sniff    can sniff
              here         here         here
```

---

## Symmetric vs Asymmetric Encryption

Two fundamental approaches to encryption, both used in network security.

**Symmetric Encryption** -- same key for encryption and decryption:

```text
┌────────┐   Key: "s3cr3t"   ┌────────────┐   Key: "s3cr3t"   ┌────────┐
│  Plain  │ ───────────────→ │ Ciphertext  │ ───────────────→ │  Plain  │
│  Text   │    Encrypt        │ xK9#mP2...  │    Decrypt        │  Text   │
└────────┘                   └────────────┘                   └────────┘
```

| Algorithm | Key Size | Speed | Use Case |
|-----------|----------|-------|----------|
| AES-128 | 128 bits | Very fast | Bulk data encryption |
| AES-256 | 256 bits | Fast | High-security data |
| ChaCha20 | 256 bits | Very fast | TLS, mobile devices |

**Problem**: How do you securely share the key?

---

## Asymmetric Encryption

Uses a key pair: public key (shared freely) and private key (kept secret).

```text
                    ┌──────────────┐
                    │  Key Pair    │
                    │              │
                    │ Public Key   │ ← Anyone can have this
                    │ Private Key  │ ← Only owner has this
                    └──────────────┘

Encryption:                              Digital Signature:
┌───────┐  Public Key   ┌──────────┐    ┌───────┐  Private Key  ┌──────────┐
│ Plain  │ ──────────→  │ Cipher   │    │ Data  │ ──────────→  │ Signed   │
│ Text   │  Encrypt     │ Text     │    │       │  Sign         │ Data     │
└───────┘               └──────────┘    └───────┘               └──────────┘
                              │                                       │
┌───────┐  Private Key  ┌────┘          ┌───────┐  Public Key   ┌────┘
│ Plain  │ ←──────────  │              │ Valid  │ ←──────────  │
│ Text   │  Decrypt                     │ ?     │  Verify
└───────┘                               └───────┘
```

| Algorithm | Key Size | Speed | Use Case |
|-----------|----------|-------|----------|
| RSA | 2048-4096 bits | Slow | Key exchange, signatures |
| ECDSA | 256-384 bits | Moderate | TLS certificates |
| Ed25519 | 256 bits | Fast | SSH keys, modern TLS |

---

## How TLS Uses Both

TLS combines symmetric and asymmetric encryption for the best of both worlds:

```text
Phase 1: Asymmetric (Key Exchange)          Phase 2: Symmetric (Bulk Data)
┌────────┐         ┌────────┐              ┌────────┐         ┌────────┐
│ Client │ ←─────→ │ Server │              │ Client │ ←─────→ │ Server │
│        │ Public  │        │              │        │ Shared  │        │
│        │ Key     │        │              │        │ Session │        │
│        │ Crypto  │        │              │        │ Key     │        │
└────────┘         └────────┘              └────────┘         └────────┘
Slow but solves                            Fast, used for all
key distribution                           application data
```

1. Asymmetric crypto establishes a shared secret (session key)
2. Symmetric crypto (AES/ChaCha20) encrypts all subsequent data
3. This is why TLS has a "handshake" phase and a "data" phase

---

## TLS/SSL Overview

- **SSL** (Secure Sockets Layer): original protocol by Netscape, versions 1.0-3.0, now deprecated
- **TLS** (Transport Layer Security): successor to SSL, current version is TLS 1.3
- Provides: **confidentiality** (encryption), **integrity** (MAC), **authentication** (certificates)

| Version | Year | Status |
|---------|------|--------|
| SSL 2.0 | 1995 | Deprecated, insecure |
| SSL 3.0 | 1996 | Deprecated (POODLE attack) |
| TLS 1.0 | 1999 | Deprecated |
| TLS 1.1 | 2006 | Deprecated |
| TLS 1.2 | 2008 | Widely used, still secure |
| TLS 1.3 | 2018 | Recommended, fastest |

```bash
# Check which TLS versions a server supports
$ nmap --script ssl-enum-ciphers -p 443 example.com

# Test TLS connection with OpenSSL
$ openssl s_client -connect example.com:443 -tls1_3
```

---

## TLS 1.2 Handshake

The TLS 1.2 handshake requires 2 round trips before data can flow:

```text
Client                                          Server
  │                                                │
  │──── ClientHello ─────────────────────────────→│
  │     (TLS version, cipher suites,              │
  │      client random)                            │
  │                                                │
  │←─── ServerHello ──────────────────────────────│
  │     (chosen cipher, server random)             │
  │←─── Certificate ──────────────────────────────│
  │     (server's X.509 certificate)               │
  │←─── ServerKeyExchange ────────────────────────│
  │←─── ServerHelloDone ──────────────────────────│
  │                                                │
  │──── ClientKeyExchange ────────────────────────→│
  │     (pre-master secret, encrypted)             │
  │──── ChangeCipherSpec ─────────────────────────→│
  │──── Finished (encrypted) ─────────────────────→│
  │                                                │
  │←─── ChangeCipherSpec ─────────────────────────│
  │←─── Finished (encrypted) ─────────────────────│
  │                                                │
  │ ═══ Encrypted Application Data ═══════════════ │
```

Total: 2 round trips (2-RTT) before first data byte

---

## TLS 1.3 Handshake

TLS 1.3 reduces the handshake to just 1 round trip:

```text
Client                                          Server
  │                                                │
  │──── ClientHello ─────────────────────────────→│
  │     (TLS version, cipher suites,              │
  │      key share, supported groups)              │
  │                                                │
  │←─── ServerHello ──────────────────────────────│
  │     (chosen cipher, key share)                 │
  │←─── EncryptedExtensions ──────────────────────│
  │←─── Certificate ──────────────────────────────│
  │←─── CertificateVerify ────────────────────────│
  │←─── Finished ─────────────────────────────────│
  │                                                │
  │──── Finished ─────────────────────────────────→│
  │                                                │
  │ ═══ Encrypted Application Data ═══════════════ │
```

**TLS 1.3 improvements:**
- 1-RTT handshake (vs 2-RTT in TLS 1.2)
- 0-RTT resumption for returning clients (with caveats -- replay risk)
- Removed insecure algorithms (RC4, DES, MD5, SHA-1, static RSA)
- All handshake messages after ServerHello are encrypted
- Only 5 cipher suites (vs dozens in TLS 1.2)

---

## Certificates and PKI

**PKI** (Public Key Infrastructure) is the trust framework that makes TLS work.

```text
┌────────────────────────┐
│    Root CA (trusted)   │  Self-signed, embedded in browsers/OS
│    e.g., DigiCert      │
└───────────┬────────────┘
            │ Signs
            ▼
┌────────────────────────┐
│   Intermediate CA      │  Signed by Root CA
│   e.g., Let's Encrypt  │
└───────────┬────────────┘
            │ Signs
            ▼
┌────────────────────────┐
│  Server Certificate    │  Signed by Intermediate CA
│  e.g., example.com     │  Contains: domain name, public key,
└────────────────────────┘  validity period, issuer info
```

**Certificate chain verification:**
1. Server sends its certificate + intermediate CA certificates
2. Client finds the Root CA in its trusted store
3. Client verifies each signature in the chain
4. Client checks domain name matches, certificate is not expired, not revoked

---

## X.509 Certificate Contents

```bash
# View a server's certificate
$ openssl s_client -connect example.com:443 < /dev/null 2>/dev/null | \
    openssl x509 -text -noout

Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 0a:bc:de:f0:12:34:56:78
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1
        Validity
            Not Before: Jan  1 00:00:00 2024 GMT
            Not After : Dec 31 23:59:59 2024 GMT
        Subject: C=US, ST=California, O=Example Inc, CN=www.example.com
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                RSA Public-Key: (2048 bit)
        X509v3 extensions:
            X509v3 Subject Alternative Name:
                DNS:www.example.com, DNS:example.com
            X509v3 Key Usage: critical
                Digital Signature, Key Encipherment
```

---

## Let's Encrypt and ACME Protocol

Let's Encrypt provides free, automated TLS certificates using the ACME protocol.

```bash
# Install certbot
$ sudo apt install certbot python3-certbot-nginx

# Obtain a certificate (HTTP challenge)
$ sudo certbot --nginx -d example.com -d www.example.com

# Obtain a certificate (DNS challenge, for wildcards)
$ sudo certbot certonly --manual --preferred-challenges dns \
    -d "*.example.com" -d example.com

# Certificate files location
$ ls /etc/letsencrypt/live/example.com/
cert.pem        # Server certificate
chain.pem       # Intermediate CA certificate
fullchain.pem   # cert.pem + chain.pem (use this in server config)
privkey.pem     # Private key (keep secret!)

# Auto-renewal (certbot sets up a systemd timer)
$ sudo certbot renew --dry-run

# Check certificate expiry
$ openssl s_client -connect example.com:443 < /dev/null 2>/dev/null | \
    openssl x509 -noout -dates
notBefore=Jan  1 00:00:00 2024 GMT
notAfter=Mar 31 23:59:59 2024 GMT
```

---

## Firewalls: Concept

A firewall controls network traffic based on predefined rules.

```text
                    ┌──────────────────────────────┐
  Incoming          │          FIREWALL             │         Internal
  Traffic  ────────→│                               │────────→ Network
                    │  Rule 1: Allow SSH (port 22)  │
  Outgoing          │  Rule 2: Allow HTTP (port 80) │         Servers
  Traffic  ←────────│  Rule 3: Allow HTTPS (443)    │←────────
                    │  Rule 4: Drop all other       │
                    └──────────────────────────────┘
```

**Types of firewalls:**

| Type | Layer | Description |
|------|-------|-------------|
| Packet filter | L3-L4 | Inspects headers (IP, port, protocol) |
| Stateful | L3-L4 | Tracks connection state |
| Application | L7 | Inspects application-layer data |
| Next-gen (NGFW) | L3-L7 | Deep packet inspection, IDS/IPS |

---

## iptables Basics

`iptables` is the traditional Linux firewall tool (uses Netfilter framework).

**Chains and tables:**

```text
┌─────────────────────────────────────────────────┐
│                  Netfilter                       │
│                                                  │
│  PREROUTING → INPUT → [Local Process] → OUTPUT → POSTROUTING
│       │                                    │
│       └──→ FORWARD ──────────────────────→─┘
│            (routing)
└─────────────────────────────────────────────────┘
```

```bash
# View current rules
$ sudo iptables -L -n -v

# Allow incoming SSH
$ sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow incoming HTTP and HTTPS
$ sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
$ sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow established connections (stateful)
$ sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow loopback
$ sudo iptables -A INPUT -i lo -j ACCEPT

# Drop everything else
$ sudo iptables -A INPUT -j DROP

# Allow outgoing traffic
$ sudo iptables -A OUTPUT -j ACCEPT
```

---

## iptables: More Examples

```bash
# Block a specific IP
$ sudo iptables -A INPUT -s 10.0.0.100 -j DROP

# Allow a specific subnet
$ sudo iptables -A INPUT -s 192.168.1.0/24 -j ACCEPT

# Rate limit SSH connections (prevent brute force)
$ sudo iptables -A INPUT -p tcp --dport 22 \
    -m conntrack --ctstate NEW \
    -m recent --set --name SSH
$ sudo iptables -A INPUT -p tcp --dport 22 \
    -m conntrack --ctstate NEW \
    -m recent --update --seconds 60 --hitcount 4 --name SSH \
    -j DROP

# Log dropped packets
$ sudo iptables -A INPUT -j LOG --log-prefix "IPTables-Drop: "
$ sudo iptables -A INPUT -j DROP

# Port forwarding (DNAT)
$ sudo iptables -t nat -A PREROUTING -p tcp --dport 8080 \
    -j DNAT --to-destination 10.0.0.50:80

# Save rules (persist across reboot)
$ sudo iptables-save > /etc/iptables/rules.v4

# Restore rules
$ sudo iptables-restore < /etc/iptables/rules.v4

# Flush all rules (careful!)
$ sudo iptables -F
```

---

## nftables: The Modern Replacement

`nftables` replaces iptables with a cleaner syntax and better performance.

```bash
# View current ruleset
$ sudo nft list ruleset

# Create a table and chain
$ sudo nft add table inet filter
$ sudo nft add chain inet filter input { type filter hook input priority 0 \; policy drop \; }
$ sudo nft add chain inet filter output { type filter hook output priority 0 \; policy accept \; }

# Allow loopback
$ sudo nft add rule inet filter input iif lo accept

# Allow established connections
$ sudo nft add rule inet filter input ct state established,related accept

# Allow SSH, HTTP, HTTPS
$ sudo nft add rule inet filter input tcp dport { 22, 80, 443 } accept

# Allow ICMP (ping)
$ sudo nft add rule inet filter input icmp type echo-request accept

# Rate limit SSH
$ sudo nft add rule inet filter input tcp dport 22 ct state new \
    limit rate 3/minute accept

# Log and drop everything else
$ sudo nft add rule inet filter input log prefix \"nft-drop: \" drop
```

---

## nftables Configuration File

```bash
# /etc/nftables.conf
#!/usr/sbin/nft -f

flush ruleset

table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;

        # Allow loopback
        iif lo accept

        # Allow established/related connections
        ct state established,related accept

        # Allow ICMP
        icmp type { echo-request, echo-reply } accept
        icmpv6 type { echo-request, echo-reply, nd-neighbor-solicit,
                      nd-neighbor-advert, nd-router-solicit,
                      nd-router-advert } accept

        # Allow specific services
        tcp dport { 22, 80, 443 } accept

        # Rate limit SSH
        tcp dport 22 ct state new limit rate 3/minute accept

        # Log dropped packets
        log prefix "nft-drop: " drop
    }

    chain forward {
        type filter hook forward priority 0; policy drop;
    }

    chain output {
        type filter hook output priority 0; policy accept;
    }
}
```

```bash
# Apply configuration
$ sudo nft -f /etc/nftables.conf

# Enable on boot
$ sudo systemctl enable nftables
```

---

## VPN Overview

A VPN (Virtual Private Network) creates an encrypted tunnel between two points over an untrusted network.

```text
Without VPN:
┌────────┐     ┌─────────┐     ┌──────────┐     ┌────────┐
│ Client │────→│  ISP    │────→│ Internet │────→│ Server │
│        │ !!  │ Can see │ !!  │ Can see  │     │        │
└────────┘     │ traffic │     │ traffic  │     └────────┘
               └─────────┘     └──────────┘

With VPN:
┌────────┐     ┌─────────┐     ┌──────────┐     ┌────────┐
│ Client │════→│  ISP    │════→│ Internet │════→│  VPN   │────→ Server
│        │     │ Sees    │     │ Sees     │     │ Server │
└────────┘     │ encrypted│    │ encrypted│     └────────┘
               │ tunnel  │     │ tunnel   │
               └─────────┘     └──────────┘
     ═══ = encrypted tunnel
```

**VPN use cases:**
- Remote access to corporate networks
- Privacy (hide traffic from ISP)
- Site-to-site connectivity (connect offices)
- Bypass geographic restrictions

---

## IPSec VPN

IPSec operates at the network layer (L3), encrypting IP packets.

**Two modes:**

```text
Transport Mode:
┌──────────┬───────────────────┬──────────────────┐
│ IP Header│   IPSec Header    │   Original Data  │
│ (original)│  (ESP/AH)        │   (encrypted)    │
└──────────┴───────────────────┴──────────────────┘

Tunnel Mode:
┌──────────┬───────────────────┬──────────┬──────────────────┐
│ New IP   │   IPSec Header    │ Original │   Original Data  │
│ Header   │   (ESP/AH)        │ IP Header│   (encrypted)    │
└──────────┴───────────────────┴──────────┴──────────────────┘
  Outer IP    Everything inside is encrypted    Inner IP
```

**IPSec protocols:**
- **ESP** (Encapsulating Security Payload): encryption + authentication
- **AH** (Authentication Header): authentication only (no encryption)
- **IKE** (Internet Key Exchange): negotiates security parameters

```bash
# Check IPSec status (using strongSwan)
$ sudo ipsec status
$ sudo ipsec statusall

# View Security Associations
$ sudo ip xfrm state
$ sudo ip xfrm policy
```

---

## WireGuard VPN

WireGuard is a modern, high-performance VPN protocol with a minimal codebase.

**WireGuard vs IPSec:**

| Feature | WireGuard | IPSec |
|---------|-----------|-------|
| Codebase | ~4,000 lines | ~400,000 lines |
| Crypto | ChaCha20, Curve25519 | Configurable (many options) |
| Performance | Very fast | Good |
| Configuration | Simple | Complex |
| Key exchange | Static public keys | IKE negotiation |
| Roaming | Built-in | Complex |

```bash
# Install WireGuard
$ sudo apt install wireguard

# Generate key pair
$ wg genkey | tee privatekey | wg pubkey > publickey

# Server configuration (/etc/wireguard/wg0.conf)
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <server_private_key>
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
PublicKey = <client_public_key>
AllowedIPs = 10.0.0.2/32
```

---

## WireGuard Client Configuration

```bash
# Client configuration (/etc/wireguard/wg0.conf)
[Interface]
Address = 10.0.0.2/24
PrivateKey = <client_private_key>
DNS = 1.1.1.1

[Peer]
PublicKey = <server_public_key>
Endpoint = vpn.example.com:51820
AllowedIPs = 0.0.0.0/0, ::/0     # Route all traffic through VPN
PersistentKeepalive = 25           # Keep connection alive behind NAT

# Start the VPN
$ sudo wg-quick up wg0

# Check status
$ sudo wg show
interface: wg0
  public key: <client_public_key>
  private key: (hidden)
  listening port: 43210

peer: <server_public_key>
  endpoint: vpn.example.com:51820
  allowed ips: 0.0.0.0/0, ::/0
  latest handshake: 12 seconds ago
  transfer: 1.23 MiB received, 456.78 KiB sent

# Stop the VPN
$ sudo wg-quick down wg0

# Enable on boot
$ sudo systemctl enable wg-quick@wg0
```

---

## Network Segmentation

Dividing a network into isolated segments limits the blast radius of security breaches.

```text
┌─────────────────────────────────────────────────────────┐
│                     Corporate Network                    │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   VLAN 10    │  │   VLAN 20    │  │   VLAN 30    │  │
│  │   Office     │  │  Development │  │  Production  │  │
│  │              │  │              │  │              │  │
│  │ 10.10.0.0/24│  │ 10.20.0.0/24│  │ 10.30.0.0/24│  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                  │                  │          │
│         └──────────┬───────┘──────────┬───────┘          │
│                    │                  │                   │
│              ┌─────┴──────┐    ┌─────┴──────┐           │
│              │  Firewall   │    │  Firewall   │           │
│              │  Rules      │    │  Rules      │           │
│              └────────────┘    └────────────┘           │
└─────────────────────────────────────────────────────────┘
```

**Segmentation benefits:**
- Limits lateral movement by attackers
- Reduces attack surface per segment
- Enables different security policies per segment
- Regulatory compliance (PCI DSS requires cardholder data isolation)

---

## DMZ (Demilitarized Zone)

A DMZ is a network segment that sits between the public internet and the internal network, hosting public-facing services.

```text
                    ┌──────────────┐
     Internet ─────→│   Outer      │
                    │   Firewall   │
                    └──────┬───────┘
                           │
                    ┌──────┴───────┐
                    │     DMZ      │
                    │              │
                    │ Web Server   │
                    │ Mail Server  │
                    │ DNS Server   │
                    └──────┬───────┘
                           │
                    ┌──────┴───────┐
                    │   Inner      │
                    │   Firewall   │
                    └──────┬───────┘
                           │
                    ┌──────┴───────┐
                    │   Internal   │
                    │   Network    │
                    │              │
                    │ Database     │
                    │ App Servers  │
                    │ Workstations │
                    └──────────────┘
```

**DMZ rules:**
- Internet can reach DMZ services (ports 80, 443, 25, 53)
- DMZ servers can reach specific internal services (e.g., database)
- Internet cannot reach internal network directly
- Internal network can reach DMZ and internet

---

## Common Network Attacks

### 1. Man-in-the-Middle (MITM)

```text
┌────────┐         ┌──────────┐         ┌────────┐
│ Client │ ──────→ │ Attacker │ ──────→ │ Server │
│        │ ←────── │ (proxy)  │ ←────── │        │
└────────┘         └──────────┘         └────────┘
  Thinks it's           Intercepts and
  talking to            optionally modifies
  the server            all traffic
```

**Mitigations:** TLS with certificate validation, certificate pinning, HSTS

### 2. ARP Spoofing

```bash
# Attacker sends fake ARP replies
# "I am the gateway" → all traffic flows through attacker

# Detect ARP spoofing
$ arp -a | sort
# Look for duplicate MAC addresses

# Prevention: static ARP entries, Dynamic ARP Inspection (DAI)
$ sudo arp -s 192.168.1.1 aa:bb:cc:dd:ee:ff
```

---

## Common Network Attacks (continued)

### 3. DNS Spoofing / Cache Poisoning

Attacker injects false DNS records into a resolver's cache.

**Mitigation:** DNSSEC, DNS over HTTPS/TLS

### 4. SYN Flood (DoS)

```text
Attacker sends thousands of SYN packets with spoofed source IPs.
Server allocates resources for each half-open connection.
Server's connection table fills up, legitimate clients can't connect.
```

```bash
# Enable SYN cookies (Linux kernel defense)
$ sudo sysctl -w net.ipv4.tcp_syncookies=1

# Limit SYN rate with iptables
$ sudo iptables -A INPUT -p tcp --syn -m limit --limit 1/s \
    --limit-burst 3 -j ACCEPT
```

### 5. Port Scanning

```bash
# Common port scan (attacker's tool, also useful for defense)
$ nmap -sS 192.168.1.0/24        # SYN scan (stealthy)
$ nmap -sV -p 1-1000 target.com  # Version detection

# Defense: minimize open ports, use firewall, monitor logs
$ sudo ss -tlnp    # Check what's listening
```

---

## Common Network Attacks (continued)

### 6. DNS Amplification DDoS

```text
┌──────────┐  Spoofed query    ┌──────────┐   Large response    ┌────────┐
│ Attacker │ ────────────────→ │ Open DNS │ ────────────────→   │ Victim │
│          │  (src=victim IP)  │ Resolver │   (~50x amplified)  │        │
└──────────┘  Small query      └──────────┘   Huge response     └────────┘
```

**Mitigation:** Disable open resolvers, BCP38 (ingress filtering), rate limiting

### 7. SSL Stripping

Downgrades HTTPS connections to HTTP, allowing eavesdropping.

```text
Client ──HTTP──→ Attacker ──HTTPS──→ Server
       ←HTTP───          ←HTTPS───
```

**Mitigation:** HSTS (HTTP Strict Transport Security), HSTS preload list

```bash
# HSTS header (server sends this)
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

---

## Network Security: Practical Hardening

```bash
# 1. Disable unnecessary services
$ sudo systemctl list-units --type=service --state=active
$ sudo systemctl disable --now avahi-daemon  # Example

# 2. Check open ports
$ sudo ss -tlnp
State    Recv-Q  Send-Q  Local Address:Port   Peer Address:Port  Process
LISTEN   0       128     0.0.0.0:22           0.0.0.0:*          sshd
LISTEN   0       511     0.0.0.0:80           0.0.0.0:*          nginx

# 3. Harden SSH
$ sudo vi /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no
MaxAuthTries 3
AllowUsers deploy admin
Protocol 2

# 4. Enable automatic security updates
$ sudo apt install unattended-upgrades
$ sudo dpkg-reconfigure unattended-upgrades

# 5. Set up fail2ban
$ sudo apt install fail2ban
$ sudo systemctl enable --now fail2ban

# 6. Kernel network hardening
$ sudo sysctl -w net.ipv4.conf.all.rp_filter=1        # Reverse path filter
$ sudo sysctl -w net.ipv4.conf.all.accept_redirects=0  # Disable ICMP redirects
$ sudo sysctl -w net.ipv4.conf.all.send_redirects=0
$ sudo sysctl -w net.ipv4.icmp_echo_ignore_broadcasts=1 # Ignore broadcast pings
```

---

## TLS in Practice: Inspecting Connections

```bash
# Full TLS connection details
$ openssl s_client -connect example.com:443 -servername example.com

CONNECTED(00000003)
depth=2 C = US, O = DigiCert Inc, CN = DigiCert Global Root G2
verify return:1
---
Certificate chain
 0 s:CN = www.example.org
   i:C = US, O = DigiCert Inc, CN = DigiCert TLS RSA SHA256 2020 CA1
 1 s:C = US, O = DigiCert Inc, CN = DigiCert TLS RSA SHA256 2020 CA1
   i:C = US, O = DigiCert Inc, CN = DigiCert Global Root G2
---
SSL handshake has read 3476 bytes and written 423 bytes
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
Server public key is 2048 bit

# Check certificate with curl
$ curl -vI https://example.com 2>&1 | grep -E "SSL|TLS|issuer|expire"

# Test specific TLS version
$ openssl s_client -connect example.com:443 -tls1_2
$ openssl s_client -connect example.com:443 -tls1_3

# Check certificate expiry
$ echo | openssl s_client -connect example.com:443 2>/dev/null | \
    openssl x509 -noout -enddate
notAfter=Mar 14 23:59:59 2025 GMT
```

---

## Zero Trust Network Architecture

The traditional "castle and moat" model (trust everything inside the network) is outdated. Zero Trust assumes no implicit trust.

**Principles:**
1. **Never trust, always verify** -- authenticate and authorize every request
2. **Least privilege access** -- grant minimum necessary permissions
3. **Assume breach** -- design as if attackers are already inside

```text
Traditional Model:                    Zero Trust Model:
┌─────────────────────┐              ┌─────────────────────┐
│  Trusted Network    │              │  No implicit trust  │
│  ┌───┐ ┌───┐ ┌───┐│              │  ┌───┐ ┌───┐ ┌───┐│
│  │ A │→│ B │→│ C ││              │  │ A │⇥│ B │⇥│ C ││
│  └───┘ └───┘ └───┘│              │  └───┘ └───┘ └───┘│
│  Free lateral       │              │  Every connection   │
│  movement           │              │  authenticated      │
└─────────────────────┘              └─────────────────────┘
```

**Implementation components:**
- Identity-aware proxy (BeyondCorp, Tailscale)
- Mutual TLS (mTLS) between services
- Microsegmentation
- Continuous authentication and authorization

---

## Network Security Monitoring

```bash
# Monitor network connections in real-time
$ sudo ss -tnp | head -20
State    Recv-Q  Send-Q  Local Address:Port  Peer Address:Port
ESTAB    0       0       10.0.0.5:22        203.0.113.50:54321  sshd
ESTAB    0       0       10.0.0.5:443       198.51.100.1:38742  nginx

# Watch for new connections
$ sudo conntrack -E

# Check firewall logs
$ sudo journalctl -k | grep "nft-drop"

# Monitor failed SSH attempts
$ sudo journalctl -u ssh | grep "Failed"
$ sudo grep "Failed password" /var/log/auth.log | tail -20

# Check for listening services
$ sudo ss -tlnp
$ sudo nmap -sT localhost

# Monitor bandwidth per connection
$ sudo iftop -i eth0

# Check for unusual DNS queries
$ sudo tcpdump -i eth0 port 53 -nn
```

---

## Review: Network Security Key Concepts

- **Symmetric encryption** (AES, ChaCha20): fast, used for bulk data
- **Asymmetric encryption** (RSA, ECDSA): slow, used for key exchange and authentication
- **TLS** combines both: asymmetric for handshake, symmetric for data
- **TLS 1.3** is faster (1-RTT) and more secure than TLS 1.2
- **PKI** and certificates create the chain of trust for TLS
- **Firewalls** (iptables/nftables) filter traffic based on rules
- **VPNs** (IPSec, WireGuard) create encrypted tunnels
- **Network segmentation** and **DMZ** limit attack blast radius
- **Zero Trust** assumes no implicit trust -- verify everything
- Defense is layered: encryption + firewalls + segmentation + monitoring
