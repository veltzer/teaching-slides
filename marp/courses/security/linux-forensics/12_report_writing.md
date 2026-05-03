---
tags:
  - infrastructure:linux
  - security:forensics
  - security:security
level: advanced
category: security
audience:
  - audiences:security-professionals

---

# Introduction to Report Writing

## Course: Linux Forensics - Day 5
- Forensic reports are the primary deliverable of an investigation
- Reports must be clear, accurate, and legally defensible
- This module covers report structure, evidence documentation,
  and presentation guidelines

---

## Why Reports Matter

- Reports communicate findings to stakeholders
- They may be used as evidence in legal proceedings
- Technical accuracy is paramount
- Clarity enables non-technical readers to understand findings
- Reports must withstand cross-examination and peer review
- Incomplete or inaccurate reports can invalidate an investigation

---

## Report Audience

![report_audience](svg/courses/security/linux-forensics/12_report_writing/report_audience.svg)

---

## Report Structure Overview

```misc
1. Title Page
2. Table of Contents
3. Executive Summary
4. Authorization and Scope
5. Evidence Description
6. Chain of Custody
7. Examination Environment
8. Analysis Methodology
9. Findings
10. Timeline of Events
11. Conclusions
12. Recommendations
13. Appendices
   a. Technical Details
   b. Hash Values
   c. Tool Output
   d. Screenshots
   e. Glossary
```

---

## Device Identification

```template
DEVICE IDENTIFICATION
=====================
Evidence Item: E001
Description:   Dell Latitude 5520 Laptop
Serial Number: ABC123DEF456
Service Tag:   7XY8Z9W
Condition:     Powered off, sealed in anti-static bag

Storage Device:
  Type:        Samsung SSD 860 EVO 500GB
  Interface:   SATA III
  Serial:      S3YZNB0K123456
  Firmware:    RVT04B6Q
  Capacity:    500,107,862,016 bytes (500 GB)

Acquisition Details:
  Date/Time:   2025-01-15 10:30:00 UTC
  Examiner:    [Name, Certification]
  Tool:        dc3dd version 7.2.646
  Method:      Physical acquisition via hardware write blocker
```

---

## Data Preservation Documentation

```bash
# Document every step of evidence handling

# Step 1: Initial state documentation
# Photograph the device (powered on/off state)
# Document screen contents if powered on
# Note any lights, sounds, or indicators

# Step 2: Write blocking
echo "Write blocker applied: Tableau T356789"
echo "Time: $(date -u)"
sudo blockdev --setro /dev/sdb
sudo blockdev --getro /dev/sdb

# Step 3: Pre-imaging hash
echo "Pre-imaging hash:"
echo "Time: $(date -u)"
sudo sha256sum /dev/sdb | tee /evidence/pre_hash.txt

# Step 4: Imaging
echo "Imaging started: $(date -u)"
sudo dc3dd if=/dev/sdb of=/evidence/E001.dd hash=sha256 \
  log=/evidence/E001_imaging.log
echo "Imaging completed: $(date -u)"
```

---

## Chain of Custody

```output
CHAIN OF CUSTODY LOG
====================
Case Number:  CASE-2025-001
Evidence ID:  E001

Date/Time           | Action              | From      | To        | Notes
--------------------|---------------------|-----------|-----------|------
2025-01-15 08:00    | Seized from office  | -         | Det. Smith| Sealed
2025-01-15 10:00    | Transferred to lab  | Det. Smith| J. Analyst| Bag intact
2025-01-15 10:30    | Opened for imaging  | J. Analyst| -         | Logged
2025-01-15 11:45    | Imaging complete    | J. Analyst| -         | Sealed
2025-01-15 12:00    | Returned to storage | J. Analyst| Evidence  | Logged
                    |                     |           | Room      |

All transfers witnessed and signed.
Evidence bag seal numbers recorded at each transfer.
```

---

## Evidence Collection Documentation

```output
EVIDENCE COLLECTION LOG
=======================
Item  | Source           | Method          | Hash (SHA-256)
------|-----------------|-----------------|-------------------
E001  | Physical disk   | dc3dd, raw image| abc123def456...
E002  | RAM (16 GB)     | LiME, lime fmt  | 789abc012def...
E003  | Network capture | tcpdump, pcap   | 345678901abc...
E004  | Log files       | Mounted r/o copy| def012345678...

Collection Notes:
- E001: 500GB SATA SSD, hardware write blocker used
- E002: Memory captured before disk imaging (volatile first)
- E003: 2 hours of traffic captured during live analysis
- E004: Log files copied from mounted read-only image
```

---

## Examination Environment

```misc
EXAMINATION ENVIRONMENT
=======================
Forensic Workstation:
  OS:        Ubuntu 22.04.3 LTS
  Kernel:    5.15.0-91-generic
  RAM:       64 GB
  Storage:   4 TB NVMe (analysis workspace)

Software Tools Used:
  Tool              | Version    | Purpose
  ------------------|------------|---------------------------
  dc3dd             | 7.2.646    | Disk imaging
  The Sleuth Kit    | 4.12.0     | Filesystem analysis
  Volatility 3      | 2.4.1      | Memory analysis
  Autopsy           | 4.21.0     | GUI analysis framework
  LiME              | 1.9.1      | Memory acquisition
  hashdeep          | 4.4        | Hash verification
  Wireshark         | 4.0.10     | Network analysis
  GDB               | 12.1       | Binary analysis

Time Source: NTP synchronized to pool.ntp.org
Timezone: All times in UTC
```

---

## Documenting Methodology

```misc
ANALYSIS METHODOLOGY
====================
1. Evidence Intake
   - Verified chain of custody documentation
   - Photographed evidence in sealed state
   - Opened evidence bags in controlled environment

2. Acquisition
   - Applied hardware write blocker
   - Computed pre-acquisition hashes
   - Created forensic images using dc3dd
   - Verified post-acquisition hashes match

3. Analysis
   - Mounted images read-only
   - Conducted filesystem analysis using TSK
   - Built MAC timeline using fls and mactime
   - Analyzed system logs for relevant events
   - Examined user artifacts and history
   - Performed keyword searching
   - Analyzed memory dump for volatile evidence

4. Reporting
   - Documented all findings with supporting evidence
   - Generated timeline of events
   - Prepared executive summary
```

---

## Writing Findings

### Guidelines for Findings Section
- State **facts**, not opinions
- Support every finding with evidence
- Reference specific evidence items (E001, etc.)
- Include timestamps in UTC
- Use precise language
- Avoid jargon (or define it)
- Include screenshots/exports as references

```misc
FINDING #1: Unauthorized SSH Access
Evidence: E001 (disk image), /var/log/auth.log
Time: 2025-01-15 10:30:00 UTC

The authentication log shows an SSH login from IP address
10.0.0.99 using the username "admin" at 10:30:00 UTC on
January 15, 2025. This IP address is external to the
organization's network (10.1.0.0/16).
```

---

## Finding Template

```misc
FINDING #[Number]: [Title]
========================
Severity:    [Critical/High/Medium/Low/Informational]
Evidence:    [Evidence item references]
Timestamps:  [UTC timestamps]
Artifacts:   [File paths, log entries, etc.]

Description:
[Clear description of what was found]

Supporting Evidence:
[Specific log entries, file contents, screenshots]

Analysis:
[Explanation of what this finding means]

Impact:
[What is the potential or actual impact]

Cross-references:
[Related findings, if any]
```

---

## Timeline Documentation

```output
TIMELINE OF EVENTS
==================
All times in UTC

2025-01-15 10:28:00  Failed SSH login attempts from 10.0.0.99
                     (username: root, admin, test)
                     Source: E001, /var/log/auth.log

2025-01-15 10:30:00  Successful SSH login from 10.0.0.99
                     (username: admin)
                     Source: E001, /var/log/auth.log

2025-01-15 10:30:15  Directory /tmp/.hidden created
                     Source: E001, filesystem timeline

2025-01-15 10:30:20  File /tmp/.hidden/toolkit.tar.gz created
                     Source: E001, filesystem timeline

2025-01-15 10:31:00  Cron job created: /etc/cron.d/update
                     Source: E001, filesystem timeline

2025-01-15 10:31:30  Web shell created: /var/www/html/cmd.php
                     Source: E001, filesystem timeline
```

---

## Executive Summary

```misc
EXECUTIVE SUMMARY
=================
On January 15, 2025, a forensic examination was conducted
on the server designated "web-prod-01" (Evidence Item E001)
following the detection of suspicious network activity.

Key Findings:
1. An unauthorized individual gained SSH access to the server
   from IP address 10.0.0.99 at 10:30 UTC.

2. The intruder installed malicious tools and established
   persistent access via a cron job.

3. A web shell was deployed, enabling remote command
   execution through the web server.

4. Evidence suggests the /etc/shadow file was accessed,
   potentially compromising user credentials.

5. No evidence of data exfiltration was found, but the
   possibility cannot be excluded.

Immediate Recommendations:
- Reset all user passwords
- Rebuild the affected server
- Block IP address 10.0.0.99 at the perimeter firewall
- Review access controls for SSH
```

---

## Conclusions Section

```misc
CONCLUSIONS
===========
Based on the examination of Evidence Items E001 through E004,
the following conclusions are drawn:

1. The server was compromised through SSH brute-force attack
   originating from IP 10.0.0.99 on January 15, 2025.

2. The attacker gained access using the "admin" account,
   which had a weak password.

3. Post-exploitation activities included:
   a. Installation of reconnaissance tools
   b. Establishment of persistence via cron job
   c. Deployment of a PHP web shell
   d. Access to the system password file

4. The total duration of unauthorized access was
   approximately 15 minutes (10:30-10:45 UTC).

5. The persistence mechanism (cron job) would have
   maintained access indefinitely if not discovered.

These conclusions are based solely on the evidence examined
and the methodology described in this report.
```

---

## Recommendations

```misc
RECOMMENDATIONS
===============
Immediate Actions:
[ ] Reset all user passwords on the compromised system
[ ] Rebuild the server from known-good media
[ ] Block IP 10.0.0.99 at perimeter firewall
[ ] Review all cron jobs on similar systems
[ ] Scan other systems for web shells (*.php containing exec/system)

Short-term Actions:
[ ] Implement SSH key-based authentication (disable passwords)
[ ] Deploy intrusion detection system (IDS)
[ ] Enable process accounting and auditd
[ ] Implement file integrity monitoring (AIDE/Tripwire)
[ ] Review and restrict sudo access

Long-term Actions:
[ ] Implement multi-factor authentication for SSH
[ ] Deploy Security Information and Event Management (SIEM)
[ ] Establish baseline configurations for all servers
[ ] Conduct regular vulnerability assessments
[ ] Develop incident response procedures
```

---

## Screenshots and Evidence Exhibits

- Include numbered screenshots for visual evidence
- Annotate screenshots to highlight relevant areas
- Reference exhibits by number in the report text

```misc
Exhibit A-1: SSH Authentication Log Entry
==========================================
[Screenshot of auth.log showing unauthorized login]

Annotation: Red highlight shows successful login from
external IP 10.0.0.99 at 10:30:00 UTC.

Exhibit A-2: Malicious Cron Job
================================
[Screenshot of cron file contents]

Contents: * * * * * root /tmp/.hidden/beacon.sh
Annotation: This cron job executes a script every minute
as the root user, establishing persistent access.
```

---

## Hash Verification Appendix

```output
APPENDIX B: HASH VERIFICATION
==============================

Evidence Acquisition Hashes:
Item  | Algorithm | Hash Value
------|-----------|--------------------------------------------
E001  | SHA-256   | a1b2c3d4e5f6...  (pre-acquisition)
E001  | SHA-256   | a1b2c3d4e5f6...  (post-acquisition)
E001  | MD5       | abc123def456...   (post-acquisition)
E002  | SHA-256   | f7e8d9c0b1a2...
E003  | SHA-256   | 1234567890ab...
E004  | SHA-256   | cdef01234567...

Analysis Verification:
At the start of analysis on 2025-01-16, all evidence
images were re-hashed and verified against acquisition
hashes. All hashes matched, confirming evidence integrity.

Post-Analysis Verification:
At the conclusion of analysis on 2025-01-20, all evidence
images were re-hashed. All hashes matched acquisition
values, confirming no modification during analysis.
```

---

## Glossary of Terms

```misc
APPENDIX E: GLOSSARY
=====================
ARP     - Address Resolution Protocol
dd      - Data duplicator (disk imaging tool)
E01     - EnCase evidence file format
ELF     - Executable and Linkable Format
ext4    - Fourth Extended Filesystem
FTK     - Forensic Toolkit
GDB     - GNU Debugger
Hash    - Fixed-size fingerprint of data (e.g., SHA-256)
Inode   - Index node (filesystem metadata structure)
LiME    - Linux Memory Extractor
MAC     - Modify/Access/Change timestamps
MBR     - Master Boot Record
NTP     - Network Time Protocol
PCAP    - Packet Capture file format
PID     - Process Identifier
SHA-256 - Secure Hash Algorithm (256-bit)
SSH     - Secure Shell
SUID    - Set User ID (permission bit)
TSK     - The Sleuth Kit
UTC     - Coordinated Universal Time
```

---

## Report Quality Checklist

```misc
QUALITY CHECKLIST
=================
[ ] All times in consistent timezone (UTC preferred)
[ ] All evidence items referenced by ID
[ ] All findings supported by evidence
[ ] Hash values documented for all evidence
[ ] Chain of custody complete
[ ] Tools and versions documented
[ ] Methodology clearly described
[ ] Executive summary present and clear
[ ] Technical details in appendices
[ ] Screenshots numbered and annotated
[ ] Glossary included
[ ] No speculation or opinion presented as fact
[ ] Peer review completed
[ ] Spelling and grammar checked
[ ] Page numbers on all pages
[ ] Classification/sensitivity markings present
[ ] Report signed and dated
```

---

## Common Report Writing Mistakes

| Mistake                       | Correction                    |
|------------------------------|-------------------------------|
| Using imprecise timestamps   | Always use UTC with full date |
| Stating opinions as facts    | Distinguish findings from analysis |
| Missing evidence references  | Cite evidence item for every finding |
| Incomplete chain of custody  | Document every transfer       |
| Jargon without explanation   | Include glossary, define terms|
| Missing hash verification    | Hash at acquisition AND analysis |
| Inconsistent formatting      | Use templates and style guides|
| Omitting negative results    | Report what was NOT found too |
| Tool version not documented  | Record every tool and version |

---

## Legal Considerations

- Reports may be admitted as court evidence
- Must comply with jurisdictional rules of evidence
- Expert witness testimony may be required
- Daubert standard (US): methodology must be reliable and relevant
- Document chain of custody meticulously
- Use validated tools and methods
- Be prepared to explain methodology under cross-examination
- Avoid making legal conclusions (that is for the court)
- Report only within your area of expertise
- Preserve all work products (notes, drafts, intermediate results)

---

## Peer Review Process

```template
PEER REVIEW CHECKLIST
=====================
Reviewer: [Name, Certification]
Date: [Review date]

Technical Accuracy:
[ ] Findings are technically correct
[ ] Evidence supports conclusions
[ ] Timeline is consistent
[ ] Hash values verified
[ ] Tool usage is appropriate

Completeness:
[ ] All evidence items analyzed
[ ] Relevant artifacts examined
[ ] Negative findings documented
[ ] Alternative explanations considered

Clarity:
[ ] Report readable by non-technical audience
[ ] Technical terms defined
[ ] Exhibits clearly labeled
[ ] No ambiguous language

Reviewer Comments:
[Space for detailed feedback]
```

---

## Report Presentation Guidelines

- Know your audience before presenting
- Start with the executive summary
- Use visual aids (timelines, diagrams, charts)
- Be prepared to explain technical details in simple terms
- Anticipate questions from legal counsel
- Have evidence exhibits ready for reference
- Maintain objectivity - present facts, not advocacy
- Practice explaining findings to non-technical colleagues

```misc
Presentation Structure:
1. Case overview (2 min)
2. Methodology (3 min)
3. Key findings (10 min)
4. Timeline walkthrough (5 min)
5. Conclusions (2 min)
6. Recommendations (3 min)
7. Q&A (varies)
```

---

## Documentation Best Practices

```bash
# Maintain investigation notes throughout the process
# Use a log file with timestamps

cat >> /evidence/investigation_notes.txt << EOF
$(date -u) - Analysis started on E001
$(date -u) - Mounted image read-only at /forensics/mounted
$(date -u) - Ran fls to list directory structure
$(date -u) - Found deleted files in /tmp/.hidden
$(date -u) - Extracted deleted file inode 45678
$(date -u) - File identified as ELF binary
$(date -u) - Ran strings analysis, found C2 indicators
EOF

# Automate note-taking with script wrapper
forensic_note() {
  echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $*" >> \
    /evidence/investigation_notes.txt
}

# Usage:
# forensic_note "Found suspicious cron job in /etc/cron.d/"
```

---

## Exercise: Report Writing

### Tasks:
1. Write an evidence identification section for a sample case
1. Document the chain of custody for a hard drive
1. Write three findings with evidence references
1. Create a timeline of events
1. Write an executive summary

```template
Template for exercise:

FORENSIC EXAMINATION REPORT
Case: [Exercise Case Number]
Examiner: [Your Name]
Date: [Today's Date]

EXECUTIVE SUMMARY:
[Write 3-4 sentences summarizing findings]

FINDINGS:
Finding #1: [Title]
Evidence: [Reference]
[Description and supporting evidence]
```

---

## Summary: Report Writing

- Reports are the primary deliverable of forensic investigations
- Structure includes executive summary, methodology, findings, conclusions
- All findings must be supported by referenced evidence
- Chain of custody must be documented for every evidence item
- Use consistent UTC timestamps throughout
- Include tool versions and examination environment details
- Hash verification proves evidence integrity
- Write for both technical and non-technical audiences
- Peer review improves quality and credibility
- Legal considerations guide report content and structure
- Documentation should be continuous throughout the investigation

---

## Handling Sensitive Information in Reports

```misc
CLASSIFICATION AND HANDLING
============================
- Reports may contain sensitive data:
  - Passwords and credentials
  - Personal information (PII)
  - Financial data
  - Trade secrets
  - Evidence of criminal activity

- Apply appropriate classification:
  - CONFIDENTIAL - limited distribution
  - RESTRICTED - named recipients only
  - PUBLIC - redacted version for disclosure

- Redaction guidelines:
  - Redact full passwords (show partial: ****word)
  - Mask IP addresses in public versions
  - Remove PII not relevant to findings
  - Keep unredacted version in secure storage
```

---

## Expert Witness Preparation

```misc
EXPERT WITNESS PREPARATION
============================
Before Testimony:
[ ] Review entire report thoroughly
[ ] Review all evidence and methodology
[ ] Prepare visual aids (timelines, diagrams)
[ ] Understand legal terminology
[ ] Review prior testimony transcripts (if any)
[ ] Practice explaining findings to non-experts

During Testimony:
- Speak clearly and avoid jargon
- Explain technical concepts with analogies
- Refer to report sections when answering
- Say "I don't know" when appropriate
- Distinguish fact from professional opinion
- Do not volunteer information beyond the question
- Maintain composure during cross-examination
- Acknowledge limitations of analysis

After Testimony:
- Preserve all notes and preparation materials
- Document any follow-up requests
```

---

## Incident Response Report vs Legal Report

![incident_response_report_vs_legal_report](svg/courses/security/linux-forensics/12_report_writing/incident_response_report_vs_legal_report.svg)

---

## Incident Response Report vs Legal Report: Details

- Same investigation may produce both types
- IR report feeds into forensic report
- Different audiences require different approaches

---

## Report Templates and Standards

```misc
INDUSTRY STANDARDS AND FRAMEWORKS
===================================
- NIST SP 800-86: Guide to Integrating Forensic
  Techniques into Incident Response

- ISO 27037: Guidelines for identification, collection,
  acquisition and preservation of digital evidence

- SWGDE Best Practices: Scientific Working Group on
  Digital Evidence

- RFC 3227: Guidelines for Evidence Collection and
  Archiving

- ACPO Good Practice Guide: Association of Chief Police
  Officers (UK)

Template Resources:
- SANS DFIR report templates
- NIST Computer Security Incident Handling Guide
- Organization-specific templates and SOPs
```

---

## Visualization in Reports

```tree
Types of Visualizations:
1. Timeline diagrams
   |--10:00--|--10:15--|--10:30--|--10:45--|
   Login    Upload    Persist   Logout

2. Network diagrams
   [Attacker] --SSH--> [Server] --SQL--> [Database]
   10.0.0.99           10.0.0.5           10.0.0.10

3. Process trees
   systemd(1)
   └── sshd(234)
       └── bash(5679)
           └── malware(6789)

4. Heat maps (activity over time)
   00 01 02 03 04 05 06 07 08 09 10 11 12
   .  .  .  .  .  .  .  .  .  .  X  X  .
   (X = activity, . = quiet)

5. Tables (comparison data)
   Before vs After file hashes
```

---

## Multi-Evidence Correlation

![multi_evidence_correlation](svg/courses/security/linux-forensics/12_report_writing/multi_evidence_correlation.svg)

---

## Evidence Handling Errors to Avoid

```misc
COMMON ERRORS AND CONSEQUENCES
================================
Error: Forgetting write blocker
  Result: Evidence may be modified, challenged in court

Error: Missing hash verification
  Result: Cannot prove evidence integrity

Error: Breaking chain of custody
  Result: Evidence may be inadmissible

Error: Incomplete documentation
  Result: Cannot reproduce analysis, weak testimony

Error: Using wrong timezone
  Result: Incorrect timeline, misleading conclusions

Error: Reporting opinions as facts
  Result: Credibility damage, report challenged

Error: Analyzing original evidence
  Result: Evidence contamination

Error: Not documenting negative results
  Result: Incomplete analysis, questions about thoroughness

Error: Using non-validated tools
  Result: Results may not be accepted
```

---

## Report Formatting Standards

```misc
FORMATTING GUIDELINES
======================
Headers:
- Use numbered sections (1.0, 1.1, 1.2)
- Consistent heading levels
- Table of contents with page numbers

Text:
- Professional font (Times New Roman, Calibri)
- 11-12pt body text
- 1.5 line spacing
- Justified or left-aligned

Technical Content:
- Code in monospace font
- Hex values in uppercase: 0xFF
- File paths in monospace: /etc/passwd
- Command output in code blocks

Evidence References:
- Bold evidence IDs: **E001**
- Consistent citation format throughout
- Cross-references to exhibits

Footer:
- Page numbers (Page X of Y)
- Case number
- Classification marking
- "CONFIDENTIAL" or equivalent
```

---

## Standardized Evidence Naming

```bash
# Consistent evidence naming convention

# Format: CASE-YYYY-NNN_ETYPE_ENUMBER_DESCRIPTION
# Examples:
CASE-2025-001_DISK_E001_laptop_ssd.dd
CASE-2025-001_DISK_E001_laptop_ssd.dd.sha256
CASE-2025-001_MEM_E002_laptop_ram.lime
CASE-2025-001_MEM_E002_laptop_ram.lime.sha256
CASE-2025-001_NET_E003_traffic_capture.pcap
CASE-2025-001_LOG_E004_auth_log.txt
CASE-2025-001_IMG_E005_phone_storage.dd

# Directory structure
/evidence/
├── CASE-2025-001/
│   ├── acquisition/     # Original images
│   ├── analysis/        # Analysis output
│   ├── reports/         # Final reports
│   ├── hashes/          # Hash verification files
│   ├── notes/           # Investigation notes
│   └── chain_of_custody/ # CoC documentation

# Maintain naming convention throughout entire case
```

---

## After-Action Review

```misc
AFTER-ACTION REVIEW TEMPLATE
==============================
Case: CASE-2025-001
Date Closed: 2025-02-15
Participants: [Investigation team]

What went well:
- Memory captured before disk imaging
- Timeline analysis identified attack sequence
- Report completed within deadline
- Hash verification successful throughout

What could be improved:
- Triage script should include Docker check
- Need write blocker for NVMe drives
- LiME module should be pre-compiled for common kernels
- Report template needs ATT&CK mapping section

Action items:
[ ] Update triage script with container checks
[ ] Purchase NVMe write blocker
[ ] Build LiME module library for common kernels
[ ] Update report template
[ ] Schedule team training on container forensics

Lessons learned documented and shared with team.
```

---

## Continuing Education and Staying Current

```misc
STAYING CURRENT IN LINUX FORENSICS
====================================
The Linux landscape evolves constantly:

Kernel Changes:
- New security features (lockdown, etc.)
- Filesystem changes (new features in ext4, btrfs)
- Module signing requirements
- eBPF capabilities

New Threats:
- Fileless malware techniques
- Container/Kubernetes-based attacks
- Supply chain compromises
- Cloud-native attack vectors

Tool Updates:
- Volatility plugins for new kernel versions
- Sleuth Kit filesystem support
- New acquisition tools (AVML, etc.)
- Memory analysis capabilities

Resources to Follow:
- SANS DFIR blog and webinars
- Volatility Foundation updates
- Linux kernel mailing list
- DFIR community Discord/Slack channels
- Conference talks (DFRWS, OSDFCon, SANS)
```

---

## Report Writing Principles

![report_writing_principles](svg/courses/security/linux-forensics/12_report_writing/report_writing_principles.svg)

---

## Case Documentation

![case_documentation](svg/courses/security/linux-forensics/12_report_writing/case_documentation.svg)
