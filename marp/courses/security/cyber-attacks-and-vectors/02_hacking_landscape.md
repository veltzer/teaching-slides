# Hacking Landscape

---
## Who are the hackers?

- Script kiddies
- Hacktivists
- Cyber criminals
- State-sponsored actors
- Insiders

---

## Script Kiddies

- Use pre-built tools and scripts without deep understanding
- Often motivated by curiosity or desire for notoriety
- Typically target low-hanging fruit and unpatched systems
- Common tools: Metasploit, LOIC, pre-packaged exploit kits

---

## Script Kiddies

![script_kiddies](svg/courses/security/cyber-attacks-and-vectors/02_hacking_landscape/script_kiddies.svg)

---
## Hacktivists

- Motivated by political, social, or ideological causes
- Use hacking as a form of protest or civil disobedience
- Notable groups: Anonymous, LulzSec, Chaos Computer Club
- Techniques: DDoS, website defacement, data leaks
- Example: Anonymous "Operation Payback" (2010) targeted organizations that opposed WikiLeaks

---

## Cyber Criminals

- Financially motivated, operate like businesses
- Range from individuals to large organized crime syndicates
- Revenue streams: ransomware, data theft, fraud, cryptojacking
- Use dark web markets for buying/selling exploits and data
- Example: FIN7 group responsible for over $1 billion in theft from financial institutions

---

## Cyber Criminals

![cyber_criminals](svg/courses/security/cyber-attacks-and-vectors/02_hacking_landscape/cyber_criminals.svg)

---
## State-Sponsored Actors (APTs)

- Advanced Persistent Threat groups backed by nation-states
- Extremely well-funded with sophisticated capabilities
- Goals: espionage, sabotage, geopolitical influence
- Notable groups:

| Group Name   | Attributed To | Known Operations                |
|-------------|---------------|----------------------------------|
| APT28       | Russia        | DNC hack, Olympic attacks        |
| APT41       | China         | Supply chain, healthcare attacks |
| Lazarus     | North Korea   | WannaCry, SWIFT bank heists      |
| APT33       | Iran          | Energy sector targeting           |
| Equation    | USA (NSA)     | Stuxnet, EternalBlue             |

---
## Insider Threats

- Current or former employees, contractors, or partners
- Have legitimate access to systems and data
- Two categories:
    - **Malicious insiders**: Intentional data theft or sabotage
    - **Negligent insiders**: Accidental security breaches
- Hardest threat to detect because traffic appears legitimate
- Example: Edward Snowden (NSA), Reality Winner (NSA)
- Detection requires User Behavior Analytics (UBA)

---
## What are the hackers' motivations

- Financial gain
- Political or ideological beliefs
- Cyber warfare
- Intellectual challenge
- Revenge

---
## Motivation Deep Dive

| Motivation | Actor Type  | Typical Attack            |
|------------|-------------|---------------------------|
| Financial  | Criminal    | Ransomware, card theft    |
| Political  | Hacktivist  | DDoS, defacement, leaks   |
| Espionage  | State APT   | Zero-day, supply chain    |
| Challenge  | Script kid  | Website hacks, SQLi       |
| Revenge    | Insider     | Data theft, sabotage      |
| Warfare    | State APT   | Infrastructure attacks    |

---
## What are the hackers' goals

- Data theft
- System disruption
- Cyber espionage
- Reputation damage
- Financial fraud

---
## What are the hackers' targets

- Governments
- Corporations
- Critical infrastructure
- Financial institutions
- Individual users

---
## Target Value Assessment

Organizations should understand why they are targets:

![target_value_assessment](svg/courses/security/cyber-attacks-and-vectors/02_hacking_landscape/target_value_assessment.svg)

---
## Attack Life-cycle

1. Reconnaissance
1. Weaponization
1. Delivery
1. Exploitation
1. Installation
1. Command & Control
1. Actions on Objectives

---
## Attack Life-cycle: The Cyber Kill Chain (Lockheed Martin)

![attack_life_cycle_the_cyber_kill_chain_lockheed_martin](svg/courses/security/cyber-attacks-and-vectors/02_hacking_landscape/attack_life_cycle_the_cyber_kill_chain_lockheed_martin.svg)

Breaking the chain at any stage prevents the attack from succeeding.

---
## Reconnaissance Phase - Tools and Techniques

Attackers gather information before launching attacks:

```bash
# Passive reconnaissance - OSINT gathering
# Whois lookup for domain information
whois example.com

# DNS enumeration
dig example.com ANY
dig example.com MX
dig example.com NS

# Subdomain enumeration with tools
# amass enum -d example.com
# subfinder -d example.com

# Search engine dorking
# site:example.com filetype:pdf
# inurl:admin site:example.com
```

- Social media profiling (LinkedIn, Twitter)
- Shodan / Censys for exposed services
- Google dorking for sensitive files
- WHOIS lookups, DNS enumeration
- Job postings revealing technology stack

---
## MITRE ATT&CK Framework

An alternative model to the Kill Chain that describes adversary behavior:

| Tactic              | Description                              | Example Techniques         |
|---------------------|------------------------------------------|----------------------------|
| Initial Access      | Getting into the network                 | Phishing, exploit public app|
| Execution           | Running malicious code                   | PowerShell, scripting       |
| Persistence         | Maintaining access                       | Registry keys, scheduled tasks|
| Privilege Escalation| Getting higher permissions               | Exploit sudo, token manipulation|
| Defense Evasion     | Avoiding detection                       | Obfuscation, disabling logs |
| Credential Access   | Stealing credentials                     | Keylogging, credential dumping|
| Discovery           | Learning about the environment           | Network scanning, file enum  |
| Lateral Movement    | Moving through the network               | Pass-the-hash, RDP           |
| Collection          | Gathering target data                    | Screen capture, email collection|
| Exfiltration        | Stealing data out                        | DNS tunneling, cloud storage |

---
## Forensics Introduction

- Collecting and analyzing digital evidence
- Identifying the attack vector
- Determining the scope and impact
- Remediating and hardening systems
- Preparing for legal proceedings

---

## Digital Forensics Process

![digital_forensics_process](svg/courses/security/cyber-attacks-and-vectors/02_hacking_landscape/digital_forensics_process.svg)

---

## Digital Forensics Process

Key forensic tools:
- **Volatility**: Memory forensics framework
- **Autopsy / Sleuth Kit**: Disk forensics
- **Wireshark**: Network traffic analysis
- **SIFT Workstation**: Complete forensic toolkit
- **FTK Imager**: Forensic disk imaging

---
## Chain of Custody

Maintaining evidence integrity is critical for legal proceedings:

- Document who collected each piece of evidence
- Record timestamps for all actions
- Use write-blockers when imaging drives
- Calculate and verify cryptographic hashes (SHA-256)
- Store evidence in tamper-evident containers
- Maintain detailed logs of all access to evidence

```bash
# Create a forensic image with hash verification
dd if=/dev/sda of=evidence.img bs=4M status=progress
sha256sum /dev/sda > evidence_hash_source.txt
sha256sum evidence.img > evidence_hash_image.txt
diff evidence_hash_source.txt evidence_hash_image.txt
```

---
## Exercise: Threat Landscape Mapping

1. Choose a fictional organization (e.g., a mid-size hospital)
1. Identify the top 5 threat actors most likely to target it
1. For each actor, list their motivation, likely attack vectors, and target assets
1. Map each attack scenario to the Cyber Kill Chain
1. Propose one defensive measure at each Kill Chain stage
1. Present your findings to the class
