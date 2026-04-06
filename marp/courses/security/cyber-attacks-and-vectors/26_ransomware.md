# Ransomware: Understanding and Defending Against Digital Extortion

---
## What is Ransomware?

- Ransomware is malware that encrypts victim's files or locks systems, demanding payment for restoration
- Modern ransomware often uses "double extortion": encrypt data AND threaten to leak it
- Payments typically demanded in cryptocurrency (Bitcoin, Monero)
- Average ransomware payment in 2023: $1.54 million (Sophos)
- Total ransomware damages estimated at $20 billion annually

---
## Evolution of Ransomware

```bash
┌──────────────────────────────────────────────────────────┐
│          Ransomware Evolution Timeline                    │
│                                                          │
│  1989  AIDS Trojan (PC Cyborg)                           │
│        First known ransomware, floppy disk delivery      │
│        Symmetric encryption, $189 demand                 │
│                                                          │
│  2013  CryptoLocker                                      │
│        First to use strong asymmetric encryption (RSA)   │
│        Bitcoin payments, $300-$3000 demands              │
│                                                          │
│  2016  Locky / Cerber / SamSam                           │
│        Mass distribution via email, exploit kits         │
│        Ransomware-as-a-Service (RaaS) emerges            │
│                                                          │
│  2017  WannaCry / NotPetya                               │
│        Self-propagating worms, nation-state weaponized   │
│        Billions in damages globally                      │
│                                                          │
│  2019  Maze                                              │
│        Introduces double extortion (encrypt + leak)      │
│                                                          │
│  2021  Colonial Pipeline / Kaseya / JBS                  │
│        Critical infrastructure targeted                  │
│        Multi-million dollar ransoms                      │
│                                                          │
│  2023+ LockBit / BlackCat / Cl0p                         │
│        Triple extortion (encrypt + leak + DDoS)          │
│        Supply chain ransomware attacks                   │
└──────────────────────────────────────────────────────────┘
```

---
## How Ransomware Works

```bash
┌──────────────────────────────────────────────────────────┐
│          Ransomware Attack Chain                          │
│                                                          │
│  1. INITIAL ACCESS                                       │
│     Phishing, RDP brute force, vulnerability exploit     │
│                                                          │
│  2. EXECUTION & PERSISTENCE                              │
│     Dropper installs ransomware, creates scheduled tasks │
│                                                          │
│  3. PRIVILEGE ESCALATION                                 │
│     Local exploits, credential theft (Mimikatz)          │
│                                                          │
│  4. LATERAL MOVEMENT                                     │
│     PsExec, WMI, RDP, SMB to spread across network      │
│                                                          │
│  5. DATA EXFILTRATION (double extortion)                 │
│     Copy sensitive files to attacker's infrastructure    │
│                                                          │
│  6. DEFENSE EVASION                                      │
│     Disable antivirus, delete shadow copies              │
│                                                          │
│  7. ENCRYPTION                                           │
│     Encrypt files on all reachable systems               │
│                                                          │
│  8. RANSOM DEMAND                                        │
│     Drop ransom note, set payment deadline               │
└──────────────────────────────────────────────────────────┘
```

---
## Encryption Techniques

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="348" font-family="sans-serif">
  <defs>
    <marker id="arw3" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <rect x="1" y="1" width="658" height="346" rx="4" fill="#fff" stroke="#333" stroke-width="1.5"/>
  <rect x="1" y="1" width="658" height="34" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="23" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">Ransomware Encryption Architecture</text>
  <!-- Attacker section -->
  <text x="14" y="54" font-size="13" font-weight="bold" fill="#c62828">Attacker has:</text>
  <text x="14" y="72" font-size="13" fill="#333">&#8226; Master RSA key pair — private key kept by attacker only</text>
  <!-- Per-victim section -->
  <text x="14" y="98" font-size="13" font-weight="bold" fill="#1565c0">Per-victim:</text>
  <text x="14" y="116" font-size="13" fill="#333">1. Generate unique RSA key pair for this victim</text>
  <text x="14" y="134" font-size="13" fill="#333">2. Encrypt victim RSA private key with master public key (stored in ransom note)</text>
  <!-- Per-file section -->
  <text x="14" y="160" font-size="13" font-weight="bold" fill="#e65100">Per-file:</text>
  <text x="14" y="178" font-size="13" fill="#333">3. Generate random AES-256 key</text>
  <text x="14" y="196" font-size="13" fill="#333">4. Encrypt file contents with AES-256 (fast)</text>
  <text x="14" y="214" font-size="13" fill="#333">5. Encrypt AES key with victim RSA public key</text>
  <text x="14" y="232" font-size="13" fill="#333">6. Append encrypted AES key to encrypted file</text>
  <!-- Flow diagram -->
  <rect x="30" y="252" width="120" height="52" rx="4" fill="#fff3e0" stroke="#e65100" stroke-width="1.5"/>
  <text x="90" y="274" font-size="12" font-weight="bold" fill="#333" text-anchor="middle">Original</text>
  <text x="90" y="292" font-size="12" fill="#333" text-anchor="middle">File</text>
  <line x1="150" y1="278" x2="230" y2="278" stroke="#555" stroke-width="1.5" marker-end="url(#arw3)"/>
  <text x="190" y="270" font-size="11" fill="#555" text-anchor="middle">AES-256</text>
  <rect x="230" y="252" width="180" height="52" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="320" y="274" font-size="12" font-weight="bold" fill="#333" text-anchor="middle">Encrypted File</text>
  <text x="320" y="292" font-size="11" fill="#555" text-anchor="middle">+ Encrypted AES key (RSA)</text>
  <text x="14" y="334" font-size="13" fill="#555" font-style="italic">Only the attacker's master private key can start the decryption chain</text>
</svg>

- AES-256 for file encryption (fast, symmetric)
- RSA-2048/4096 for key encryption (slow, asymmetric)
- Without the private key, decryption is mathematically infeasible
- Some ransomware families have had implementation bugs allowing free decryption

---
## Delivery Methods

| Method                   | Prevalence | Description                              |
|--------------------------|------------|------------------------------------------|
| Phishing emails          | ~45%       | Malicious attachments or links           |
| RDP brute force          | ~25%       | Exposed RDP with weak credentials        |
| Software vulnerabilities | ~15%       | Unpatched VPN, Exchange, etc.            |
| Drive-by downloads       | ~5%        | Compromised websites serving exploits    |
| USB/physical access      | ~3%        | Infected removable media                 |
| Supply chain             | ~5%        | Compromised updates (Kaseya, MOVEit)    |
| Insider threat           | ~2%        | Malicious or compromised employee        |

---
## Lateral Movement Techniques

```python
┌──────────────────────────────────────────────────────────┐
│          Lateral Movement in Ransomware Attacks           │
│                                                          │
│  Initial                                                 │
│  Foothold                                                │
│  ┌───┐     Mimikatz      ┌───────────────────┐          │
│  │PC1│─────(credential───>│ Domain Controller │          │
│  └───┘      theft)        └────────┬──────────┘          │
│                                    │                     │
│              PsExec/WMI/SMB        │                     │
│         ┌──────────────────────────┼─────────┐           │
│         v              v           v         v           │
│      ┌─────┐       ┌─────┐    ┌─────┐   ┌──────┐       │
│      │ PC2 │       │ PC3 │    │ PC4 │   │Server│       │
│      └─────┘       └─────┘    └─────┘   └──────┘       │
│                                                          │
│  Common tools:                                           │
│  - Mimikatz: Dump credentials from memory                │
│  - PsExec: Remote command execution                      │
│  - CobaltStrike: Post-exploitation framework             │
│  - BloodHound: Map Active Directory attack paths         │
│  - RDP: Lateral movement via remote desktop              │
│  - WMI: Windows Management Instrumentation               │
│  - SMB: File share access and propagation                │
└──────────────────────────────────────────────────────────┘
```

---
## Pre-Encryption Actions

```bash
# Commands commonly run by ransomware before encryption
# (understanding these helps with detection)

# Delete Volume Shadow Copies (prevents file recovery)
vssadmin delete shadows /all /quiet
wmic shadowcopy delete

# Disable Windows Recovery
bcdedit /set {default} recoveryenabled No
bcdedit /set {default} bootstatuspolicy ignoreallfailures

# Stop backup and security services
net stop "Volume Shadow Copy"
net stop "Windows Backup"
net stop "Windows Defender"
sc config WinDefend start=disabled

# Disable and clear event logs
wevtutil cl System
wevtutil cl Security
wevtutil cl Application

# Kill processes that lock files (databases, email)
taskkill /F /IM sqlservr.exe
taskkill /F /IM oracle.exe
taskkill /F /IM outlook.exe
```

> Understanding pre-encryption behavior enables detection before encryption begins.

---
## Ransomware-as-a-Service (RaaS)

```bash
┌──────────────────────────────────────────────────────────┐
│          RaaS Business Model                              │
│                                                          │
│  ┌──────────────────────────────────────────────┐        │
│  │  RaaS Operator (Developer)                    │        │
│  │  - Develops the ransomware                    │        │
│  │  - Maintains infrastructure (C2, payment)     │        │
│  │  - Provides admin panel / builder              │        │
│  │  - Handles decryption key management          │        │
│  │  - Takes 20-40% cut of ransoms                │        │
│  └───────────────────────┬──────────────────────┘        │
│                          │                               │
│         ┌────────────────┼────────────────┐              │
│         v                v                v              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐           │
│  │Affiliate │    │Affiliate │    │Affiliate │           │
│  │    #1    │    │    #2    │    │    #3    │           │
│  │          │    │          │    │          │           │
│  │Gains     │    │Gains     │    │Gains     │           │
│  │access,   │    │access,   │    │access,   │           │
│  │deploys   │    │deploys   │    │deploys   │           │
│  │ransomware│    │ransomware│    │ransomware│           │
│  │60-80% cut│    │60-80% cut│    │60-80% cut│           │
│  └──────────┘    └──────────┘    └──────────┘           │
│                                                          │
│  Lowers barrier to entry: affiliates need no             │
│  development skills, just initial access ability         │
└──────────────────────────────────────────────────────────┘
```

---
## Notable Ransomware Campaigns

### WannaCry (2017)

| Aspect          | Detail                                         |
|-----------------|------------------------------------------------|
| Propagation     | EternalBlue (SMBv1 exploit), self-spreading worm|
| Encryption      | AES-128 + RSA-2048                             |
| Ransom          | $300-$600 in Bitcoin                           |
| Scale           | 230,000+ systems in 150 countries              |
| Notable victims | UK NHS (hospitals shut down), Renault, FedEx   |
| Damage          | ~$4 billion estimated                          |
| Kill switch     | Marcus Hutchins found unregistered domain      |
| Attribution     | North Korea (Lazarus Group)                    |

---
### NotPetya (2017)

```python
┌──────────────────────────────────────────────────────────┐
│          NotPetya: "The Most Devastating Cyberattack      │
│           in History" -- Wired                            │
│                                                          │
│  Delivery:    Compromised M.E.Doc (Ukrainian tax software)│
│  Propagation: EternalBlue + Mimikatz + PsExec/WMI       │
│  Target:      Initially Ukraine, spread globally          │
│                                                          │
│  Key difference from ransomware:                         │
│  - Master boot record overwritten (not recoverable!)     │
│  - Payment mechanism intentionally broken                │
│  - Goal was DESTRUCTION, not profit                      │
│  - Disguised as ransomware to create confusion           │
│                                                          │
│  Damage:                                                 │
│  - Maersk (shipping): $300M, rebuilt 45,000 PCs          │
│  - Merck (pharma): $870M                                 │
│  - FedEx/TNT: $400M                                      │
│  - Total: ~$10 billion estimated                         │
│                                                          │
│  Attribution: Russian GRU (Sandworm team)                │
│  Purpose: Cyberweapon against Ukraine, collateral global │
└──────────────────────────────────────────────────────────┘
```

---
### REvil / Sodinokibi

- Responsible for JBS meatpacking ($11M ransom paid) and Kaseya supply chain attack
- Kaseya attack: compromised VSA software used by MSPs, affecting ~1500 businesses
- Demanded $70M for universal decryptor
- Operated as RaaS with sophisticated affiliate program
- Taken down by international law enforcement in 2022

### LockBit

- Most prolific ransomware group (2022-2024)
- LockBit 3.0 introduced bug bounty program for finding bugs in their ransomware
- Targeted thousands of organizations globally
- Disrupted by Operation Cronos (Feb 2024) -- FBI/NCA seized infrastructure
- Partial recovery and continued operations post-takedown

---
## Double and Triple Extortion

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="296" font-family="sans-serif">
  <rect x="1" y="1" width="658" height="294" rx="4" fill="#fff" stroke="#333" stroke-width="1.5"/>
  <rect x="1" y="1" width="658" height="34" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="23" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">Extortion Models</text>
  <!-- Single Extortion -->
  <rect x="14" y="44" width="630" height="58" rx="4" fill="#f0f4f8" stroke="#555" stroke-width="1"/>
  <text x="26" y="62" font-size="13" font-weight="bold" fill="#222">Single Extortion</text>
  <text x="26" y="80" font-size="13" fill="#333">Encrypt files &#8594; demand payment for decryption key   |   Defense: Backups</text>
  <!-- Double Extortion -->
  <rect x="14" y="110" width="630" height="58" rx="4" fill="#fff9c4" stroke="#f9a825" stroke-width="1.5"/>
  <text x="26" y="128" font-size="13" font-weight="bold" fill="#e65100">Double Extortion</text>
  <text x="26" y="146" font-size="13" fill="#333">Exfiltrate data + encrypt &#8594; Pay or we leak your data   |   Defense: Backups + data protection</text>
  <!-- Triple Extortion -->
  <rect x="14" y="176" width="630" height="58" rx="4" fill="#ffccbc" stroke="#bf360c" stroke-width="1.5"/>
  <text x="26" y="194" font-size="13" font-weight="bold" fill="#bf360c">Triple Extortion</text>
  <text x="26" y="212" font-size="13" fill="#333">Exfiltrate + encrypt + DDoS + contact customers   |   Defense: Comprehensive security program</text>
  <!-- Quadruple Extortion -->
  <rect x="14" y="242" width="630" height="44" rx="4" fill="#ffcdd2" stroke="#c62828" stroke-width="2"/>
  <text x="26" y="260" font-size="13" font-weight="bold" fill="#c62828">Quadruple Extortion (emerging)</text>
  <text x="26" y="278" font-size="13" fill="#333">All of above + report regulatory violations &#8594; "Pay or we report your data breach to regulators"</text>
</svg>

---
## Backup Strategies: The 3-2-1-1-0 Rule

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="348" font-family="sans-serif">
  <rect x="1" y="1" width="658" height="346" rx="4" fill="#fff" stroke="#333" stroke-width="1.5"/>
  <rect x="1" y="1" width="658" height="34" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="23" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">3-2-1-1-0 Backup Rule</text>
  <!-- Number rows -->
  <circle cx="34" cy="58" r="14" fill="#1565c0"/>
  <text x="34" y="63" font-size="14" font-weight="bold" fill="#fff" text-anchor="middle">3</text>
  <text x="56" y="63" font-size="13" fill="#333">Copies of data (production + 2 backups)</text>
  <circle cx="34" cy="92" r="14" fill="#1565c0"/>
  <text x="34" y="97" font-size="14" font-weight="bold" fill="#fff" text-anchor="middle">2</text>
  <text x="56" y="97" font-size="13" fill="#333">Different storage media types (disk + tape, disk + cloud, etc.)</text>
  <circle cx="34" cy="126" r="14" fill="#1565c0"/>
  <text x="34" y="131" font-size="14" font-weight="bold" fill="#fff" text-anchor="middle">1</text>
  <text x="56" y="131" font-size="13" fill="#333">Copy offsite (different physical location)</text>
  <circle cx="34" cy="160" r="14" fill="#e65100"/>
  <text x="34" y="165" font-size="14" font-weight="bold" fill="#fff" text-anchor="middle">1</text>
  <text x="56" y="160" font-size="13" fill="#333">Copy offline or air-gapped</text>
  <text x="56" y="178" font-size="12" fill="#c62828" font-weight="bold">CRITICAL: ransomware targets connected backups!</text>
  <circle cx="34" cy="204" r="14" fill="#2e7d32"/>
  <text x="34" y="209" font-size="14" font-weight="bold" fill="#fff" text-anchor="middle">0</text>
  <text x="56" y="209" font-size="13" fill="#333">Zero errors — verify backup integrity regularly</text>
  <!-- Three boxes diagram -->
  <rect x="30" y="230" width="130" height="70" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="95" y="256" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Production</text>
  <text x="95" y="274" font-size="12" fill="#222" text-anchor="middle">Data</text>
  <rect x="250" y="230" width="130" height="70" rx="4" fill="#fff9c4" stroke="#f9a825" stroke-width="1.5"/>
  <text x="315" y="256" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Local Backup</text>
  <text x="315" y="274" font-size="12" fill="#222" text-anchor="middle">(NAS)</text>
  <rect x="470" y="230" width="140" height="70" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="540" y="252" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Offsite Backup</text>
  <text x="540" y="268" font-size="11" fill="#222" text-anchor="middle">(Cloud / Tape)</text>
  <text x="540" y="284" font-size="11" fill="#2e7d32" font-weight="bold" text-anchor="middle">AIR-GAPPED ✓</text>
  <text x="95" y="318" font-size="11" fill="#c62828" text-anchor="middle">Connected</text>
  <text x="95" y="332" font-size="11" fill="#c62828" text-anchor="middle">(vulnerable)</text>
  <text x="315" y="318" font-size="11" fill="#e65100" text-anchor="middle">Connected</text>
  <text x="315" y="332" font-size="11" fill="#e65100" text-anchor="middle">(vulnerable)</text>
  <text x="540" y="318" font-size="11" fill="#2e7d32" text-anchor="middle">Immutable /</text>
  <text x="540" y="332" font-size="11" fill="#2e7d32" text-anchor="middle">Air-gapped (SAFE)</text>
</svg>

---
## Immutable Backups

```bash
# AWS S3 Object Lock (WORM - Write Once Read Many)
aws s3api put-object-lock-configuration \
    --bucket my-backup-bucket \
    --object-lock-configuration '{
        "ObjectLockEnabled": "Enabled",
        "Rule": {
            "DefaultRetention": {
                "Mode": "COMPLIANCE",
                "Days": 30
            }
        }
    }'
# COMPLIANCE mode: Even root/admin cannot delete during retention

# Veeam immutable backup repository (Linux)
# Uses immutable flag on XFS filesystem
# Backups cannot be modified or deleted during retention period

# ZFS snapshots (immutable by nature)
zfs snapshot pool/data@backup-$(date +%Y%m%d)
# Snapshots are read-only; ransomware cannot encrypt them

# Verify backup integrity
sha256sum /backup/data/*.tar.gz > /backup/checksums.txt
# Compare checksums during restore testing
```

---
## Ransomware Prevention

```bash
┌──────────────────────────────────────────────────────────┐
│  Prevention Controls                                     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Initial Access Prevention:                              │
│  [ ] Email filtering with attachment sandboxing          │
│  [ ] Disable or restrict RDP (use VPN + MFA)             │
│  [ ] Patch management (priority: internet-facing)        │
│  [ ] Security awareness training                         │
│  [ ] Web filtering (block known malicious sites)         │
│                                                          │
│  Lateral Movement Prevention:                            │
│  [ ] Network segmentation (VLANs, microsegmentation)     │
│  [ ] Least privilege (no admin rights for users)         │
│  [ ] Disable SMBv1 and unnecessary protocols             │
│  [ ] LAPS (Local Admin Password Solution)                │
│  [ ] Privileged Access Workstations (PAWs)               │
│                                                          │
│  Encryption Prevention:                                  │
│  [ ] Endpoint Detection and Response (EDR)               │
│  [ ] Application whitelisting                            │
│  [ ] Controlled folder access (Windows)                  │
│  [ ] Volume shadow copy protection                       │
│  [ ] Canary files (detect encryption activity)           │
└──────────────────────────────────────────────────────────┘
```

---
## Ransomware Detection

```bash
# Canary files: Place decoy files and monitor for changes
# If these files are modified, encryption is likely in progress

# Linux: inotifywait for file system monitoring
inotifywait -m -r /data --format '%T %w%f %e' \
    --timefmt '%Y-%m-%d %H:%M:%S' \
    -e modify -e create -e delete \
    /data/canary/ 2>/dev/null | while read line; do
    echo "[ALERT] Canary file touched: $line"
    # Trigger incident response automation
done

# Monitor for mass file renaming (ransomware indicators)
# Rapid extension changes (.docx -> .encrypted)
inotifywait -m -r /data --format '%f' -e moved_to | \
    grep -c "\.encrypted$\|\.locked$\|\.crypto$"
```

### Detection Indicators

| Indicator                            | Stage              | Tool                |
|--------------------------------------|--------------------|---------------------|
| Unusual login activity (RDP, VPN)    | Initial access     | SIEM                |
| Mimikatz/credential dumping          | Privilege escalation| EDR                |
| Mass SMB/WMI connections             | Lateral movement   | NDR                 |
| Large data uploads to cloud storage  | Exfiltration       | DLP/NDR             |
| Shadow copy deletion commands        | Pre-encryption     | EDR/Sysmon          |
| Rapid file modifications/renames     | Encryption         | File integrity mon. |
| Ransom note creation                 | Post-encryption    | EDR                 |

---
## Incident Response Playbook

```python
┌──────────────────────────────────────────────────────────┐
│  Ransomware Incident Response                            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  HOUR 0-1: DETECTION & INITIAL RESPONSE                  │
│  1. Confirm it is ransomware (not wiper)                 │
│  2. Identify the ransomware variant (ransom note, ext.)  │
│  3. Activate incident response team                      │
│  4. DO NOT pay immediately (assess first)                │
│  5. Preserve evidence (memory dumps, logs)               │
│                                                          │
│  HOUR 1-4: CONTAINMENT                                   │
│  6. Isolate affected systems (disconnect from network)   │
│  7. Disable shared drives and network shares             │
│  8. Block C2 communication (firewall rules)              │
│  9. Reset compromised credentials                        │
│  10. Identify patient zero and attack vector             │
│                                                          │
│  HOUR 4-24: ASSESSMENT                                   │
│  11. Determine scope (how many systems affected)         │
│  12. Check backup integrity and availability             │
│  13. Check for data exfiltration indicators              │
│  14. Check nomoreransom.org for decryptors               │
│  15. Engage legal counsel and law enforcement            │
│                                                          │
│  DAY 1-7: RECOVERY                                       │
│  16. Rebuild from clean images (do not decrypt in place) │
│  17. Restore from verified clean backups                 │
│  18. Patch the vulnerability that was exploited          │
│  19. Implement additional security controls              │
│  20. Gradual service restoration with monitoring         │
│                                                          │
│  DAY 7+: POST-INCIDENT                                   │
│  21. Lessons learned documentation                       │
│  22. Regulatory notification (if required)               │
│  23. Customer/stakeholder communication                  │
│  24. Update incident response plan                       │
│  25. Security posture improvements                       │
└──────────────────────────────────────────────────────────┘
```

---
## To Pay or Not to Pay?

| Factor                        | Pay                        | Don't Pay                  |
|-------------------------------|----------------------------|----------------------------|
| Backup availability           | No viable backups          | Clean backups available    |
| Business impact               | Critical systems down      | Systems recoverable        |
| Decryptor availability        | None (check nomoreransom.org)| Free decryptor exists   |
| Legal considerations          | Varies by jurisdiction     | OFAC sanctions risk        |
| Data exfiltration             | Sensitive data stolen      | No data exfiltration       |
| Attacker reliability          | Reputable RaaS group       | Unknown/unreliable group   |
| Insurance coverage            | Cyber insurance covers it  | No coverage                |

**Key considerations:**
- Paying funds criminal operations and encourages more attacks
- No guarantee of receiving working decryptor (~8% of paying victims do not)
- OFAC sanctions: paying certain groups (e.g., in North Korea, Russia) may violate US law
- Check https://www.nomoreransom.org for free decryption tools
- Law enforcement strongly recommends NOT paying

---
## Free Decryption Resources

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="268" font-family="sans-serif">
  <rect x="1" y="1" width="658" height="266" rx="4" fill="#fff" stroke="#333" stroke-width="1.5"/>
  <rect x="1" y="1" width="658" height="34" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="330" y="23" font-size="15" font-weight="bold" fill="#1b5e20" text-anchor="middle">No More Ransom Project (nomoreransom.org)</text>
  <text x="14" y="56" font-size="13" fill="#333">&#8226; Joint initiative: Europol, Dutch Police, Kaspersky, McAfee, and 170+ partners</text>
  <text x="14" y="74" font-size="13" fill="#333">&#8226; Free decryption tools for 150+ ransomware families</text>
  <text x="14" y="92" font-size="13" fill="#333">&#8226; Upload encrypted file + ransom note to identify variant and check for decryptors</text>
  <line x1="14" y1="104" x2="646" y2="104" stroke="#ddd" stroke-width="1"/>
  <text x="14" y="122" font-size="13" font-weight="bold" fill="#1565c0">Other resources:</text>
  <text x="14" y="140" font-size="13" fill="#333">&#8226; ID Ransomware (id-ransomware.malwarehunterteam.com) — upload sample to identify family</text>
  <text x="14" y="158" font-size="13" fill="#333">&#8226; Emsisoft decryption tools</text>
  <text x="14" y="176" font-size="13" fill="#333">&#8226; Avast decryption tools</text>
  <text x="14" y="194" font-size="13" fill="#333">&#8226; Bitdefender decryption tools</text>
  <rect x="14" y="210" width="630" height="44" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="329" y="237" font-size="14" font-weight="bold" fill="#1b5e20" text-anchor="middle">&#128273; Always try free decryption before considering payment!</text>
</svg>

---
## Key Takeaways

- Ransomware has evolved from simple encryption malware to sophisticated extortion operations
- RaaS lowers the barrier to entry, enabling non-technical criminals to deploy ransomware
- Double/triple extortion means backups alone are not sufficient -- data protection is critical
- The 3-2-1-1-0 backup rule with immutable/air-gapped copies is the foundation of resilience
- Prevention requires defense in depth: email security, patching, MFA, segmentation, EDR
- Detection should focus on pre-encryption indicators (shadow copy deletion, lateral movement)
- Have a tested incident response playbook before an attack occurs
- Paying ransoms is discouraged: it funds criminals and does not guarantee recovery
- Check nomoreransom.org for free decryption tools before considering payment
