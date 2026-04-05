# Man-in-the-Middle Attacks: Intercepting Communications
---
## What is a Man-in-the-Middle (MITM) Attack
- A type of cyber attack where an attacker intercepts and potentially alters the communication between two parties.
- The attacker secretly relays and modifies the traffic, posing as both parties to the communication.
- Allows the attacker to eavesdrop, steal data, or inject malicious content.
---
## Common MITM Attack Scenarios
- Public Wi-Fi networks (coffee shops, airports, etc.)
- Unsecured websites (HTTP instead of HTTPS)
- Rogue access points or evil twin attacks
- ARP spoofing and cache poisoning
- Compromised network devices (routers, switches)
---
## Stages of a MITM Attack
1. **Interception**: Attacker intercepts communication between two parties.
1. **Decryption**: If communication is encrypted, attacker attempts to decrypt it.
1. **Data Modification**: Attacker can alter the intercepted data.
1. **Re-encryption**: Attacker re-encrypts the modified data.
1. **Forwarding**: Attacker forwards the modified data to the intended recipient.
---
## Defending Against MITM Attacks
- Implement robust encryption and authentication mechanisms
- Use virtual private networks (VPNs) when connecting to public networks
- Verify digital certificates and check for certificate revocation
- Implement multi-factor authentication (MFA) for critical systems
- Monitor and analyze network traffic for anomalies
- Regularly audit and update network devices and infrastructure
---
## Encryption and Authentication
- Use secure protocols like HTTPS, SSH, and VPNs for communication.
- Implement strong encryption algorithms and key exchange methods.
- Authenticate servers and clients using digital certificates or other authentication mechanisms.
- Regularly update and replace encryption keys and certificates.
---
## Virtual Private Networks (VPNs)
- VPNs establish an encrypted tunnel between devices and a secure network.
- Protect against MITM attacks on public networks by encrypting all traffic.
- Use reputable VPN providers and ensure proper VPN configuration.
- Implement split-tunneling or always-on VPN policies as needed.
---
## Certificate Validation and Pinning
- Verify the digital certificates of servers and websites to ensure authenticity.
- Check for certificate revocation lists (CRLs) or use OCSP stapling.
- Implement certificate pinning to associate a specific certificate with a server or service.
- Use trusted certificate authorities (CAs) and update certificates regularly.
---
## Multi-Factor Authentication (MFA)
- Implement MFA for critical systems and privileged accounts.
- Use a combination of factors like passwords, biometrics, and hardware tokens.
- Protect against MITM attacks by requiring additional authentication factors.
- Regularly review and update MFA policies and mechanisms.
---
## Network Monitoring and Analysis
- Deploy intrusion detection and prevention systems (IDS/IPS) to monitor network traffic.
- Analyze network traffic for anomalies and suspicious patterns.
- Implement security information and event management (SIEM) solutions.
- Regularly audit and update network devices, software, and configurations.
---
## Securing Network Infrastructure
- Deploy secure network devices and regularly update firmware.
- Implement network segmentation and access controls.
- Use secure protocols and encryption for management interfaces.
- Regularly audit and update network configurations and access policies.
- Implement secure wireless network configurations and protocols (e.g., WPA2 Enterprise).
---
## User Awareness and Training
- Educate users about the risks of MITM attacks and security best practices.
- Promote the use of secure protocols, VPNs, and certificate validation.
- Encourage caution when connecting to public or untrusted networks.
- Implement regular security awareness training and phishing simulations.
---
## Continuous Monitoring and Improvement
- Regularly review and update security policies and procedures.
- Conduct penetration testing and vulnerability assessments.
- Stay informed about the latest MITM attack techniques and mitigation strategies.
- Continuously monitor and improve your organization's security posture.

## Defending against MITM attacks requires a multi-layered approach, including encryption, authentication, network monitoring, and user awareness
---
## Interesting command lines that have to do with libssl

```bash
# install the documentation for the libssl library
sudo apt install libssl-doc
# dpkg --status libssl-dev
# dpkg --status libssl3t64
# openssl ciphers -v
```

---

## MITM Attack Types and Techniques

```
┌────────────────────────────────────────────────────────────┐
│                MITM Attack Taxonomy                        │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Network-Level:                                            │
│  ├── ARP Spoofing / ARP Cache Poisoning                    │
│  ├── DNS Spoofing                                          │
│  ├── DHCP Spoofing                                         │
│  ├── BGP Hijacking                                         │
│  └── Evil Twin Wi-Fi                                       │
│                                                            │
│  Application-Level:                                        │
│  ├── SSL Stripping (downgrade HTTPS to HTTP)               │
│  ├── SSL/TLS Interception (proxy with fake cert)           │
│  ├── HTTP/2 Downgrade                                      │
│  └── WebSocket Hijacking                                   │
│                                                            │
│  Protocol-Level:                                           │
│  ├── LLMNR/NBT-NS Poisoning (Windows networks)            │
│  ├── mDNS Poisoning                                        │
│  └── WPAD Hijacking                                        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## ARP Spoofing: Step by Step

```
┌──────────────────────────────────────────────────────────┐
│              ARP Spoofing Attack                         │
│                                                          │
│  Normal:                                                 │
│  Victim (192.168.1.10) ──> Gateway (192.168.1.1)        │
│  ARP: 192.168.1.1 = AA:BB:CC:DD:EE:FF (real MAC)       │
│                                                          │
│  Attack:                                                 │
│  Attacker sends gratuitous ARP replies:                  │
│  "192.168.1.1 is at XX:XX:XX:XX:XX:XX" (attacker MAC)   │
│                                                          │
│  After poisoning:                                        │
│  ┌────────┐     ┌──────────┐     ┌─────────┐           │
│  │ Victim  │────>│ Attacker  │────>│ Gateway  │          │
│  │         │<────│ (forwards)│<────│         │          │
│  └────────┘     └──────────┘     └─────────┘           │
│                                                          │
│  Attacker sees ALL traffic between victim and gateway    │
└──────────────────────────────────────────────────────────┘
```

---

## Detecting ARP Spoofing

```bash
# Check ARP table for duplicate MAC addresses
arp -a | sort -t'(' -k2 | uniq -d -f1

# Monitor ARP traffic for gratuitous ARPs
tcpdump -i eth0 -n arp | grep "is-at"

# Use arpwatch to detect ARP changes
sudo apt install arpwatch
sudo arpwatch -i eth0
# Logs changes to /var/log/syslog

# Static ARP entries for critical hosts (manual)
sudo arp -s 192.168.1.1 AA:BB:CC:DD:EE:FF

# Enable Dynamic ARP Inspection on managed switches
# (Cisco switch example)
# ip arp inspection vlan 10
# ip arp inspection validate src-mac dst-mac ip
```

---

## SSL Stripping Attack

```
┌──────────────────────────────────────────────────────────┐
│              SSL Stripping (Moxie Marlinspike, 2009)     │
│                                                          │
│  Normal flow:                                            │
│  Browser ──HTTPS──> bank.com (encrypted)                 │
│                                                          │
│  SSL Stripping:                                          │
│  ┌────────┐  HTTP  ┌──────────┐  HTTPS  ┌─────────┐    │
│  │ Victim  │──────>│ Attacker  │────────>│bank.com  │    │
│  │ Browser │<──────│ (proxy)   │<────────│         │    │
│  └────────┘  HTTP  └──────────┘  HTTPS  └─────────┘    │
│                                                          │
│  1. Attacker intercepts initial HTTP connection          │
│  2. Attacker connects to bank.com via HTTPS              │
│  3. Attacker serves content to victim via HTTP           │
│  4. Victim sees no padlock - but most users don't check  │
│  5. All credentials transmitted in plain text!           │
│                                                          │
│  Defense: HSTS (HTTP Strict Transport Security)          │
│  Strict-Transport-Security: max-age=31536000;            │
│  includeSubDomains; preload                              │
└──────────────────────────────────────────────────────────┘
```

---

## LLMNR/NBT-NS Poisoning (Windows Networks)

```bash
# LLMNR (Link-Local Multicast Name Resolution)
# When DNS fails, Windows broadcasts LLMNR queries
# Attacker responds: "I am that server, send me your hash"

# Using Responder (for authorized pentesting only)
# sudo responder -I eth0 -wrf

# What Responder captures:
# [*] [LLMNR] Poisoned answer sent to 192.168.1.50
#     for name fileserver
# [*] [NTLMv2] Hash captured:
#     admin::DOMAIN:1122334455667788:AABB...

# Crack captured NTLMv2 hashes
# hashcat -m 5600 captured_hash.txt wordlist.txt

# Defense:
# 1. Disable LLMNR: GPO > Computer Configuration >
#    Administrative Templates > Network > DNS Client >
#    Turn off multicast name resolution = Enabled
# 2. Disable NBT-NS: Network adapter > IPv4 > Advanced >
#    WINS > Disable NetBIOS over TCP/IP
```

---

## TLS Certificate Verification

```bash
# Check a server's TLS certificate
openssl s_client -connect example.com:443 -servername example.com

# Verify certificate chain
openssl s_client -connect example.com:443 -showcerts

# Check certificate expiry
echo | openssl s_client -connect example.com:443 2>/dev/null | \
    openssl x509 -noout -dates

# Test for weak cipher suites
nmap --script ssl-enum-ciphers -p 443 example.com

# Check HSTS header
curl -sI https://example.com | grep -i strict-transport

# Test for certificate pinning
# Mobile apps and browsers maintain pin sets
# HTTP Public Key Pinning (HPKP) is deprecated
# Replaced by Certificate Transparency (CT) logs
```

---

## Real-World MITM Incidents

| Incident              | Year | Details                                   |
|-----------------------|------|-------------------------------------------|
| DigiNotar breach      | 2011 | Fake Google certs, Iranian surveillance    |
| Superfish (Lenovo)    | 2015 | Pre-installed MITM proxy on laptops        |
| Equifax redirect      | 2017 | MITM on credit monitoring redirect         |
| Kazakhstan MITM cert  | 2019 | Government mandated MITM root certificate  |
| SolarWinds Orion      | 2020 | Supply chain MITM for update mechanism     |

---

## Exercise: MITM Detection Lab

1. Set up a lab with attacker, victim, and gateway VMs on the same subnet
2. Use Wireshark on the victim to capture normal ARP traffic baseline
3. Perform ARP spoofing from the attacker VM (use arpspoof or bettercap)
4. Observe ARP table changes on the victim
5. Detect the attack using:
   - arpwatch alerts
   - Wireshark ARP anomaly detection
   - Manual ARP table inspection
6. Implement countermeasures:
   - Static ARP entries
   - Enable HSTS on a test web server
   - Configure 802.1X port authentication
7. Verify the countermeasures prevent the attack
