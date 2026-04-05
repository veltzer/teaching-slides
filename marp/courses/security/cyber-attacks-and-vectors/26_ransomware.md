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

```
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

```
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

```
┌──────────────────────────────────────────────────────────┐
│          Ransomware Encryption Architecture               │
│                                                          │
│  Attacker has:                                           │
│  - Master RSA key pair (private key kept by attacker)    │
│                                                          │
│  Per-victim:                                             │
│  1. Generate unique RSA key pair for this victim         │
│  2. Encrypt victim RSA private key with master public    │
│     key (stored in ransom note)                          │
│                                                          │
│  Per-file:                                               │
│  3. Generate random AES-256 key                          │
│  4. Encrypt file contents with AES-256 (fast)            │
│  5. Encrypt AES key with victim RSA public key           │
│  6. Append encrypted AES key to encrypted file           │
│                                                          │
│  ┌────────┐   AES-256    ┌──────────────────────┐       │
│  │Original│──────────────>│Encrypted file        │       │
│  │ File   │              │+ Encrypted AES key   │       │
│  └────────┘              │  (RSA encrypted)     │       │
│                          └──────────────────────┘       │
│                                                          │
│  Only the attacker's master private key can              │
│  start the decryption chain                              │
└──────────────────────────────────────────────────────────┘
```

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

```
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

```
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

```
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

```
┌──────────────────────────────────────────────────────────┐
│  Extortion Models                                        │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Single Extortion:                                       │
│  Encrypt files -> demand payment for decryption key      │
│  Defense: Backups                                        │
│                                                          │
│  Double Extortion:                                       │
│  Exfiltrate data + encrypt files                         │
│  -> Pay or we leak your data publicly                    │
│  Defense: Backups + data protection                      │
│                                                          │
│  Triple Extortion:                                       │
│  Exfiltrate + encrypt + DDoS + contact customers         │
│  -> Pay or: data leaked + systems down + customers told  │
│  Defense: Comprehensive security program                 │
│                                                          │
│  Quadruple Extortion (emerging):                         │
│  All of above + report regulatory violations             │
│  -> "Pay or we report your data breach to regulators"    │
└──────────────────────────────────────────────────────────┘
```

---
## Backup Strategies: The 3-2-1-1-0 Rule

```
┌──────────────────────────────────────────────────────────┐
│          3-2-1-1-0 Backup Rule                           │
│                                                          │
│  3  Copies of data (production + 2 backups)              │
│                                                          │
│  2  Different storage media types                        │
│     (disk + tape, disk + cloud, etc.)                    │
│                                                          │
│  1  Copy offsite (different location)                    │
│                                                          │
│  1  Copy offline or air-gapped                           │
│     (CRITICAL: ransomware targets connected backups!)    │
│                                                          │
│  0  Zero errors (verify backup integrity regularly)      │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│  │Production│  │ Local    │  │ Offsite  │               │
│  │  Data    │  │ Backup   │  │ Backup   │               │
│  │          │  │ (NAS)    │  │ (Cloud/  │               │
│  │          │  │          │  │  Tape)   │               │
│  └──────────┘  └──────────┘  └──────────┘               │
│       │              │              │                    │
│       │  Connected   │  Air-gapped  │                    │
│       │  (vulnerable │  or immutable│                    │
│       │  to ransomware) (SAFE)      │                    │
└──────────────────────────────────────────────────────────┘
```

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

```
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

```
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

```
┌──────────────────────────────────────────────────────────┐
│  No More Ransom Project (nomoreransom.org)               │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  - Joint initiative: Europol, Dutch Police, Kaspersky,   │
│    McAfee, and 170+ partners                             │
│  - Free decryption tools for 150+ ransomware families    │
│  - Upload encrypted file + ransom note to identify       │
│    the variant and check for available decryptors        │
│                                                          │
│  Other resources:                                        │
│  - ID Ransomware (id-ransomware.malwarehunterteam.com)   │
│    Upload sample to identify the ransomware family       │
│  - Emsisoft decryption tools                             │
│  - Avast decryption tools                                │
│  - Bitdefender decryption tools                          │
│                                                          │
│  Always try free decryption before considering payment!  │
└──────────────────────────────────────────────────────────┘
```

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
