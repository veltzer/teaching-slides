# Tools for Correct Reporting

## Course: Linux Forensics - Day 5 (continued)
- Specialized tools streamline forensic reporting
- `Autopsy` provides integrated case management and analysis
- `Dradis` centralizes findings and generates reports
- This module covers tool-assisted reporting workflows

---

## Why Use Reporting Tools?

- Manual report writing is error-prone and time-consuming
- Tools enforce consistency and completeness
- Automated artifact collection reduces missed evidence
- Built-in templates ensure proper structure
- Hash verification is automated
- Collaboration features support team investigations
- Audit trails track examiner actions

---

## Autopsy Overview

<svg xmlns="http://www.w3.org/2000/svg" width="420" height="360" font-family="sans-serif">
  <!-- Outer box: Autopsy GUI -->
  <rect x="10" y="10" width="400" height="340" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="210" y="36" text-anchor="middle" font-size="15" font-weight="bold" fill="#222222">Autopsy GUI</text>
  <!-- Case Management -->
  <rect x="40" y="50" width="340" height="66" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="210" y="70" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Case Management</text>
  <text x="210" y="89" text-anchor="middle" font-size="12" fill="#444444">Create/open cases · Manage evidence sources</text>
  <!-- Analysis Modules -->
  <rect x="40" y="126" width="340" height="88" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="210" y="146" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Analysis Modules</text>
  <text x="210" y="165" text-anchor="middle" font-size="12" fill="#444444">File analysis · Keyword search · Timeline</text>
  <text x="210" y="183" text-anchor="middle" font-size="12" fill="#444444">Hash lookup · Web artifacts</text>
  <!-- Report Generation -->
  <rect x="40" y="224" width="340" height="66" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="210" y="244" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Report Generation</text>
  <text x="210" y="263" text-anchor="middle" font-size="12" fill="#444444">HTML, Excel, text · Tagged items</text>
  <!-- The Sleuth Kit -->
  <text x="210" y="320" text-anchor="middle" font-size="13" font-weight="bold" fill="#555555">The Sleuth Kit (TSK)</text>
</svg>

---

## Installing Autopsy

```bash
# Autopsy 4.x (Java-based, cross-platform)
# Download from https://www.sleuthkit.org/autopsy/

# Dependencies
sudo apt install sleuthkit autopsy

# For Autopsy 4.x standalone:
# Download the .deb or use snap
sudo snap install autopsy

# Or build from source:
git clone https://github.com/sleuthkit/autopsy.git
cd autopsy
# Follow build instructions for your platform

# Start Autopsy (web-based version)
autopsy
# Open browser: http://localhost:9999/autopsy

# Start Autopsy 4.x (GUI)
./autopsy
```

---

## Autopsy Case Management

```misc
Creating a New Case:
1. File -> New Case
2. Enter case details:
   - Case Name: CASE-2025-001
   - Case Number: 2025-001
   - Examiner: John Investigator
   - Organization: Forensic Lab Inc.

3. Add Data Source:
   - Type: Disk Image or VM File
   - Path: /forensics/images/disk.dd
   - Time Zone: UTC
   - Hash: SHA-256

4. Select Ingest Modules:
   [ ] Recent Activity
   [ ] Hash Lookup (NSRL)
   [ ] Keyword Search
   [ ] Email Parser
   [ ] Extension Mismatch Detector
   [ ] EXIF Parser
   [ ] Encryption Detection
   [ ] Interesting Files Identifier
```

---

## Autopsy Analysis Modules

| Module                    | Purpose                            |
|--------------------------|-------------------------------------|
| Recent Activity          | Browser history, downloads, cookies |
| Hash Lookup              | NSRL filtering, known bad files    |
| File Type Identification | Verify file types by signature     |
| Keyword Search           | Search for terms across all files  |
| Email Parser             | Extract email messages             |
| Extension Mismatch       | Find renamed/disguised files       |
| EXIF Parser              | Extract image metadata             |
| Encryption Detection     | Find encrypted files/volumes       |
| Interesting Files        | Flag files matching custom rules   |
| Android Analyzer         | Parse Android device data          |

---

## Autopsy File Analysis

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="380" font-family="sans-serif">
  <!-- Left pane: Directory Tree -->
  <rect x="10" y="10" width="220" height="260" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="120" y="32" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Directory Tree</text>
  <line x1="10" y1="40" x2="230" y2="40" stroke="#333333" stroke-width="1"/>
  <text x="22" y="60" font-size="12" fill="#444444" font-family="monospace">/</text>
  <text x="22" y="78" font-size="12" fill="#444444" font-family="monospace">├── etc/</text>
  <text x="22" y="96" font-size="12" fill="#444444" font-family="monospace">├── home/</text>
  <text x="22" y="114" font-size="12" fill="#444444" font-family="monospace">│   └── user/</text>
  <text x="22" y="132" font-size="12" fill="#444444" font-family="monospace">├── tmp/</text>
  <text x="22" y="150" font-size="12" fill="#444444" font-family="monospace">│   └── .hidden/</text>
  <text x="22" y="168" font-size="12" fill="#444444" font-family="monospace">├── var/</text>
  <text x="22" y="186" font-size="12" fill="#444444" font-family="monospace">│   └── log/</text>
  <text x="22" y="204" font-size="12" fill="#444444" font-family="monospace">└── ...</text>
  <!-- Right pane: File Listing -->
  <rect x="240" y="10" width="410" height="260" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="445" y="32" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">File Listing</text>
  <line x1="240" y1="40" x2="650" y2="40" stroke="#333333" stroke-width="1"/>
  <!-- Column headers -->
  <text x="255" y="58" font-size="12" font-weight="bold" fill="#222222">Name</text>
  <text x="370" y="58" font-size="12" font-weight="bold" fill="#222222">Size</text>
  <text x="425" y="58" font-size="12" font-weight="bold" fill="#222222">Modified</text>
  <text x="530" y="58" font-size="12" font-weight="bold" fill="#222222">Type</text>
  <line x1="240" y1="64" x2="650" y2="64" stroke="#aaaaaa" stroke-width="1"/>
  <!-- File rows -->
  <text x="255" y="82" font-size="12" fill="#444444">passwd</text>
  <text x="370" y="82" font-size="12" fill="#444444">2345</text>
  <text x="425" y="82" font-size="12" fill="#444444">Jan 10</text>
  <text x="530" y="82" font-size="12" fill="#444444">text</text>
  <text x="255" y="100" font-size="12" fill="#444444">shadow</text>
  <text x="370" y="100" font-size="12" fill="#444444">1890</text>
  <text x="425" y="100" font-size="12" fill="#444444">Jan 10</text>
  <text x="530" y="100" font-size="12" fill="#444444">text</text>
  <text x="255" y="118" font-size="12" fill="#444444">hostname</text>
  <text x="370" y="118" font-size="12" fill="#444444">15</text>
  <text x="425" y="118" font-size="12" fill="#444444">Jun 01</text>
  <text x="530" y="118" font-size="12" fill="#444444">text</text>
  <line x1="240" y1="128" x2="650" y2="128" stroke="#aaaaaa" stroke-width="1" stroke-dasharray="4,3"/>
  <!-- Deleted files -->
  <text x="255" y="147" font-size="12" font-weight="bold" fill="#cc0000">Deleted Files:</text>
  <text x="255" y="165" font-size="12" fill="#cc4444">toolkit.tar.gz (deleted)</text>
  <text x="255" y="183" font-size="12" fill="#cc4444">recon.sh (deleted)</text>
  <!-- File Content Viewer -->
  <rect x="10" y="280" width="640" height="84" rx="4" fill="#fff3e0" stroke="#333333" stroke-width="1.5"/>
  <text x="330" y="300" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">File Content Viewer</text>
  <rect x="28" y="310" width="52" height="24" rx="3" fill="#e3f2fd" stroke="#555555" stroke-width="1"/>
  <text x="54" y="327" text-anchor="middle" font-size="12" fill="#222222">Hex</text>
  <rect x="90" y="310" width="52" height="24" rx="3" fill="#f0f4f8" stroke="#555555" stroke-width="1"/>
  <text x="116" y="327" text-anchor="middle" font-size="12" fill="#222222">Text</text>
  <rect x="152" y="310" width="92" height="24" rx="3" fill="#f0f4f8" stroke="#555555" stroke-width="1"/>
  <text x="198" y="327" text-anchor="middle" font-size="12" fill="#222222">Application</text>
  <rect x="254" y="310" width="80" height="24" rx="3" fill="#f0f4f8" stroke="#555555" stroke-width="1"/>
  <text x="294" y="327" text-anchor="middle" font-size="12" fill="#222222">Metadata</text>
</svg>

---

## Autopsy Timeline Feature

```misc
Timeline View in Autopsy:
- Visualizes file system events chronologically
- Color-coded by event type (created, modified, accessed)
- Zoom in/out on time ranges
- Filter by file type or directory

Usage:
1. Tools -> Timeline
2. Select date range of interest
3. Zoom into suspicious activity periods
4. Click events for details
5. Tag relevant events for reporting

Timeline helps identify:
- Periods of high activity (attacker presence)
- Gaps in activity (evidence deletion?)
- Correlation between different event types
- Sequence of attack steps
```

---

## Autopsy Keyword Search

```misc
Keyword Search Configuration:
1. Create keyword list:
   - Name: "Sensitive Data"
   - Keywords:
     - password
     - credit card
     - social security
     - confidential
     - secret

2. Create regex list:
   - Name: "Patterns"
   - Regex:
     - \b\d{3}-\d{2}-\d{4}\b    (SSN)
     - \b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b  (CC)
     - [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}

3. Search scope:
   - All files
   - Unallocated space
   - Specific directories
```

---

## Autopsy Tagging and Bookmarking

```misc
Tagging System:
- Tag notable items during analysis
- Tags carry into reports automatically
- Custom tag names for organization

Built-in Tags:
- Notable Item (yellow)
- Follow Up (orange)
- Suspicious (red)
- Child Exploitation (restricted)

Custom Tags:
- Malware
- Persistence Mechanism
- Data Exfiltration
- Credential Theft
- Lateral Movement

Tag items by right-clicking:
File -> Add Tag -> "Malware"
Add comment: "ELF binary with C2 communication capability"
```

---

## Autopsy Report Generation

```misc
Generate Report:
1. Tools -> Generate Report
2. Select report type:
   - HTML Report
   - Excel Report (CSV)
   - KML Report (geolocation)
   - Text Report
   - Portable Case

3. Configure options:
   [x] Tagged Results Only
   [x] Include File Contents
   [x] Include Hash Values
   [ ] All Files (may be very large)

4. Select tagged items to include:
   [x] Malware
   [x] Persistence Mechanism
   [x] Credential Theft

5. Generate -> Save to /evidence/reports/

HTML report includes:
- Case summary
- Evidence sources
- Tagged items with details
- Hash values
- Module results
```

---

## Autopsy HTML Report Structure

```tree
Generated HTML Report:
/evidence/reports/
├── index.html           <- Main report page
├── case_summary.html    <- Case details
├── sources.html         <- Evidence sources
├── tagged/
│   ├── malware.html     <- Tagged malware files
│   ├── persistence.html <- Persistence mechanisms
│   └── credentials.html <- Credential findings
├── modules/
│   ├── recent_activity.html
│   ├── keyword_hits.html
│   ├── hash_hits.html
│   └── email.html
├── timeline.html        <- Event timeline
└── appendix/
    ├── file_hashes.html <- All file hashes
    └── tool_output.html <- Raw tool output
```

---

## Dradis Framework Overview

<svg xmlns="http://www.w3.org/2000/svg" width="420" height="430" font-family="sans-serif">
  <!-- Outer box: Dradis Web Interface -->
  <rect x="10" y="10" width="400" height="410" rx="4" fill="#e8f5e9" stroke="#333333" stroke-width="1.5"/>
  <text x="210" y="36" text-anchor="middle" font-size="15" font-weight="bold" fill="#222222">Dradis Web Interface</text>
  <!-- Project Management -->
  <rect x="40" y="50" width="340" height="78" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="210" y="70" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Project Management</text>
  <text x="210" y="89" text-anchor="middle" font-size="12" fill="#444444">Nodes (evidence items) · Notes (findings)</text>
  <text x="210" y="107" text-anchor="middle" font-size="12" fill="#444444">Issues (vulnerabilities)</text>
  <!-- Import Plugins -->
  <rect x="40" y="138" width="340" height="64" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="210" y="158" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Import Plugins</text>
  <text x="210" y="177" text-anchor="middle" font-size="12" fill="#444444">Nmap, Nessus, Burp · Custom importers</text>
  <!-- Export Plugins -->
  <rect x="40" y="212" width="340" height="64" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="210" y="232" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Export Plugins</text>
  <text x="210" y="251" text-anchor="middle" font-size="12" fill="#444444">Word, PDF, HTML, CSV</text>
  <!-- Collaboration -->
  <rect x="40" y="286" width="340" height="64" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="210" y="306" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Collaboration</text>
  <text x="210" y="325" text-anchor="middle" font-size="12" fill="#444444">Multi-user support · Activity log</text>
</svg>

---

## Installing Dradis

```bash
# Dradis CE (Community Edition)
# Ruby on Rails application

# Prerequisites
sudo apt install ruby ruby-dev build-essential \
  libsqlite3-dev nodejs npm

# Clone repository
git clone https://github.com/dradis/dradis-ce.git
cd dradis-ce

# Install dependencies
bundle install

# Setup database
bundle exec rake db:setup

# Start server
bundle exec rails server
# Access at http://localhost:3000

# Default credentials are set on first run
# Create admin account through the web interface
```

---

## Dradis Project Structure

```tree
Dradis Project Organization:
+-- Project: CASE-2025-001
    |
    +-- Nodes (Evidence Items)
    |   +-- E001: Laptop Disk Image
    |   |   +-- Note: Filesystem Analysis
    |   |   +-- Note: Deleted Files Found
    |   |   +-- Note: Web Shell Discovered
    |   |
    |   +-- E002: Memory Dump
    |   |   +-- Note: Process List
    |   |   +-- Note: Network Connections
    |   |   +-- Note: Bash History
    |   |
    |   +-- E003: Network Capture
    |       +-- Note: C2 Communication
    |       +-- Note: Data Exfiltration
    |
    +-- Issues (Findings)
    |   +-- Unauthorized SSH Access
    |   +-- Malware Installation
    |   +-- Persistence Mechanism
    |   +-- Web Shell Deployment
    |
    +-- Methodology
        +-- Evidence Handling
        +-- Analysis Steps
```

---

## Dradis Note Templates

```output
# Finding Template (in Dradis markup)

#[Title]#
Unauthorized SSH Access

#[Severity]#
Critical

#[Evidence]#
E001 - /var/log/auth.log

#[Timestamp]#
2025-01-15 10:30:00 UTC

#[Description]#
Analysis of the authentication log (E001) reveals a
successful SSH login from external IP address 10.0.0.99
using the "admin" account.

#[Supporting Evidence]#
Log entry:
Jan 15 10:30:00 server sshd[1234]: Accepted password
for admin from 10.0.0.99 port 52341 ssh2

#[Impact]#
Full system access was obtained by an unauthorized user.

#[Recommendations]#
Implement SSH key-based authentication.
Disable password-based SSH login.
```

---

## Dradis Import Capabilities

```bash
# Import tool output directly into Dradis

# Supported import formats:
# - Nmap XML output
# - Nessus scan results
# - Burp Suite reports
# - Nikto output
# - OpenVAS reports
# - Qualys reports
# - Custom CSV/XML

# Example: Import Nmap results
nmap -sV -oX nmap_results.xml target_network
# Then import via Dradis web interface:
# Upload -> Select File -> nmap_results.xml

# Custom import via API
curl -X POST http://localhost:3000/api/nodes \
  -H "Authorization: Token api_token_here" \
  -d '{"node": {"label": "E001"}}'
```

---

## Dradis Export and Report Generation

```misc
Report Generation Workflow:
1. Create report template (Word/HTML)
2. Map Dradis fields to template placeholders
3. Generate report

Template Placeholders:
- {{project.name}}
- {{project.created_at}}
- {{issue.title}}
- {{issue.severity}}
- {{issue.description}}
- {{evidence.content}}
- {{node.label}}

Export Formats:
- Microsoft Word (.docx)
- PDF
- HTML
- CSV
- Custom templates

Steps:
1. Export -> Select Template
2. Choose format (Word recommended)
3. Select issues/nodes to include
4. Generate -> Download
```

---

## Dradis Collaboration Features

<svg xmlns="http://www.w3.org/2000/svg" width="560" height="340" font-family="sans-serif">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555555"/>
    </marker>
  </defs>
  <!-- Examiner 1 -->
  <rect x="20" y="20" width="220" height="76" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="130" y="42" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Examiner 1</text>
  <text x="130" y="61" text-anchor="middle" font-size="12" fill="#444444">Disk analysis</text>
  <text x="130" y="79" text-anchor="middle" font-size="12" fill="#444444">File recovery</text>
  <!-- Examiner 2 -->
  <rect x="320" y="20" width="220" height="76" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="430" y="42" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Examiner 2</text>
  <text x="430" y="61" text-anchor="middle" font-size="12" fill="#444444">Memory analysis</text>
  <text x="430" y="79" text-anchor="middle" font-size="12" fill="#444444">Network analysis</text>
  <!-- Arrows to Dradis Server -->
  <line x1="130" y1="96" x2="230" y2="170" stroke="#555555" stroke-width="1.5" marker-end="url(#arrow)"/>
  <line x1="430" y1="96" x2="330" y2="170" stroke="#555555" stroke-width="1.5" marker-end="url(#arrow)"/>
  <!-- Dradis Server -->
  <rect x="130" y="172" width="300" height="100" rx="4" fill="#fff3e0" stroke="#333333" stroke-width="1.5"/>
  <text x="280" y="194" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Dradis Server</text>
  <text x="280" y="212" text-anchor="middle" font-size="12" fill="#444444">Centralized data · Activity log</text>
  <text x="280" y="230" text-anchor="middle" font-size="12" fill="#444444">Real-time updates · Version history</text>
  <!-- Arrow to Reports -->
  <line x1="280" y1="272" x2="280" y2="298" stroke="#555555" stroke-width="1.5" marker-end="url(#arrow)"/>
  <!-- Reports -->
  <rect x="200" y="300" width="160" height="36" rx="4" fill="#e8f5e9" stroke="#333333" stroke-width="1.5"/>
  <text x="280" y="323" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Reports</text>
</svg>

---

## Combining Autopsy and Dradis

```tree
Integrated Forensic Workflow:

1. Evidence Intake
   └── Autopsy: Add data sources

2. Automated Analysis
   └── Autopsy: Run ingest modules

3. Manual Analysis
   └── Autopsy: Tag findings

4. Export Findings
   └── Autopsy: Export tagged items

5. Import to Dradis
   └── Dradis: Import Autopsy output

6. Organize Report
   └── Dradis: Structure findings

7. Review & Collaborate
   └── Dradis: Team review

8. Generate Report
   └── Dradis: Export to Word/PDF
```

---

## Other Reporting Tools

| Tool           | Type          | Key Feature                  |
|---------------|---------------|------------------------------|
| Autopsy       | Analysis + Report | Integrated TSK frontend  |
| Dradis CE     | Collaboration     | Multi-user, templates    |
| Magnet AXIOM  | Commercial        | Comprehensive suite      |
| X-Ways        | Commercial        | Fast, efficient          |
| DFIR-IRIS     | Open source       | Incident response        |
| TheHive       | Open source       | Case management          |
| Plaso/log2timeline | Timeline     | Super timeline generation|
| Timesketch    | Timeline          | Collaborative timelines  |

---

## Plaso and Super Timelines

```bash
# Plaso creates comprehensive timelines from multiple sources
pip3 install plaso

# Process evidence image to create timeline database
log2timeline.py /evidence/plaso_timeline.dump \
  /forensics/images/disk.dd

# Filter and output timeline
psort.py -o l2tcsv /evidence/plaso_timeline.dump \
  "date > '2025-01-15 00:00:00' AND date < '2025-01-16 00:00:00'" \
  > /evidence/timeline_jan15.csv

# Plaso processes:
# - Filesystem timestamps (all partitions)
# - Windows Event Logs
# - Browser history (Chrome, Firefox, Safari)
# - Syslog entries
# - Systemd journal
# - Apache/Nginx logs
# - And 100+ other parsers

# Import into Timesketch for visual analysis
```

---

## Timesketch

```bash
# Timesketch - collaborative forensic timeline analysis
# Web-based, supports team investigations

# Install with Docker
git clone https://github.com/google/timesketch.git
cd timesketch
docker compose up -d

# Access at http://localhost:5000

# Features:
# - Import Plaso timelines
# - Collaborative annotation
# - Saved searches and views
# - Tagging and starring events
# - Timeline comparison
# - Sigma rule matching
# - Export capabilities

# Upload timeline
timesketch_importer --host http://localhost:5000 \
  --timeline_name "E001 Disk" \
  /evidence/plaso_timeline.dump
```

---

## DFIR-IRIS for Case Management

```bash
# DFIR-IRIS - Incident Response case management
# Docker-based deployment

# Install
git clone https://github.com/dfir-iris/iris-web.git
cd iris-web
docker compose up -d

# Access at https://localhost:443

# Features:
# - Case management with timeline
# - Evidence tracking
# - IOC management
# - Task assignment
# - API for automation
# - Report generation
# - Asset tracking
# - Custom modules

# API usage:
curl -X POST https://localhost/api/cases \
  -H "Authorization: Bearer TOKEN" \
  -d '{"case_name": "CASE-2025-001",
       "case_description": "Server compromise investigation"}'
```

---

## Automated Report Generation Script

```bash
#!/bin/bash
# Generate forensic report from collected evidence
CASE="CASE-2025-001"
EVIDENCE="/evidence"
REPORT="/evidence/reports/report_$(date +%Y%m%d).html"

cat > "$REPORT" << EOF
<html><head><title>Forensic Report - $CASE</title></head>
<body>
<h1>Digital Forensic Examination Report</h1>
<h2>Case: $CASE</h2>
<p>Date: $(date -u)</p>
<p>Examiner: $(whoami)</p>

<h2>Evidence Items</h2>
<table border="1">
<tr><th>Item</th><th>SHA-256</th><th>Size</th></tr>
EOF

for img in "$EVIDENCE"/*.dd "$EVIDENCE"/*.lime; do
  if [ -f "$img" ]; then
    hash=$(sha256sum "$img" | awk '{print $1}')
    size=$(stat -c %s "$img")
    name=$(basename "$img")
    echo "<tr><td>$name</td><td>$hash</td><td>$size</td></tr>" \
      >> "$REPORT"
  fi
done

cat >> "$REPORT" << EOF
</table>

<h2>System Information</h2>
<pre>$(cat "$EVIDENCE"/system/uname.txt 2>/dev/null)</pre>

<h2>User Accounts</h2>
<pre>$(cat "$EVIDENCE"/users/passwd.txt 2>/dev/null)</pre>

</body></html>
EOF

echo "Report generated: $REPORT"
```

---

## Report Review Workflow

```tree
Review Process:

Step 1: Self-Review
├── Check all findings have evidence references
├── Verify hash values are correct
├── Proofread for spelling/grammar
└── Verify timeline consistency

Step 2: Technical Peer Review
├── Another examiner reviews methodology
├── Verifies tool usage is appropriate
├── Checks technical accuracy
└── Reviews hash verification

Step 3: Quality Assurance Review
├── Checks report completeness
├── Verifies compliance with standards
├── Reviews formatting and structure
└── Checks for sensitive information handling

Step 4: Legal Review (if applicable)
├── Reviews for legal sufficiency
├── Checks evidence admissibility
├── Reviews conclusions and opinions
└── Approves for submission
```

---

## Evidence Presentation in Court

- Present findings clearly and simply
- Use visual aids (timelines, diagrams)
- Be prepared to explain methodology
- Avoid technical jargon
- Answer questions directly
- Acknowledge limitations of findings
- Distinguish between fact and opinion
- Have all supporting documentation ready

```misc
Presentation Tips:
- Practice explaining to non-technical people
- Prepare for hostile cross-examination
- Know your tools and methodology thoroughly
- Be honest about what you don't know
- Have original evidence available if needed
- Maintain professional demeanor
- Focus on facts, not conclusions of guilt/innocence
```

---

## Exercise: Reporting Lab

### Tasks:
1. Create a case in Autopsy with a sample disk image
1. Tag three findings during analysis
1. Generate an HTML report from Autopsy
1. Document findings in Dradis format
1. Write a complete executive summary

```template
Exercise Template:

CASE: EXERCISE-2025-LAB
EXAMINER: [Your Name]
DATE: [Today's Date]

Evidence:
- Lab disk image (provided)

Required Deliverables:
1. Autopsy case file with tagged findings
2. Timeline covering the incident period
3. Written report with:
   - Executive summary
   - Three findings with evidence
   - Recommendations
   - Hash verification appendix
```

---

## Course Summary: Linux Forensics

### Day 1: Hardware & OS Structure
- Drive anatomy, SSD forensic implications
- `Linux` filesystem hierarchy
- `systemd`, users, groups, shells

### Day 2: Forensic Fundamentals
- Hashes for evidence integrity
- OS artifacts and user activity
- Password files and data structures

### Day 3: Collecting Evidence
- Data carving with `foremost`, `scalpel`, `bulk_extractor`
- System and network information collection
- Drive imaging with `dd`, `dcfldd`, FTK, `LiME`

### Day 4: Analysis
- Image analysis with The Sleuth Kit
- `strace`, `ltrace`, `GDB` for advanced analysis
- Volatile memory analysis with Volatility

### Day 5: Reporting
- Report structure and documentation
- Autopsy and Dradis for report generation

---

## Resources and Further Learning

### Books
- "File System Forensic Analysis" by Brian Carrier
- "The Art of Memory Forensics" by Ligh et al.
- "Digital Forensics with Kali Linux" by Shashank Mishra

### Online Resources
- SANS DFIR: https://www.sans.org/digital-forensics-incident-response/
- Volatility Foundation: https://www.volatilityfoundation.org/
- Sleuth Kit: https://www.sleuthkit.org/
- NIST CFTT: https://www.nist.gov/itl/ssd/software-quality-group

### Certifications
- GIAC Certified Forensic Examiner (GCFE)
- GIAC Certified Forensic Analyst (GCFA)
- EnCase Certified Examiner (EnCE)
- AccessData Certified Examiner (ACE)

### Practice
- DFIR challenges and CTF competitions
- NIST CFReDS sample images

---

## TheHive Case Management

```bash
# TheHive is an open-source security incident response platform

# Install with Docker
docker pull strangebee/thehive:5
docker run -d --name thehive \
  -p 9000:9000 \
  strangebee/thehive:5

# Access at http://localhost:9000

# Key features:
# - Case creation and tracking
# - Observable management (IOCs)
# - Task assignment and workflow
# - Cortex integration (automated analysis)
# - MISP integration (threat intelligence)
# - Custom templates
# - API for automation

# Create case via API
curl -X POST http://localhost:9000/api/case \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"Server Compromise","severity":3}'
```

---

## MITRE ATT&CK Mapping in Reports

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="370" font-family="sans-serif">
  <text x="330" y="22" text-anchor="middle" font-size="14" font-weight="bold" fill="#222222">MITRE ATT&amp;CK Mapping</text>
  <!-- Table header -->
  <rect x="10" y="30" width="640" height="28" rx="0" fill="#37474f" stroke="#333333" stroke-width="1.5"/>
  <text x="100" y="49" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">Tactic</text>
  <text x="305" y="49" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">Technique</text>
  <text x="535" y="49" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">Evidence</text>
  <!-- Row 1 -->
  <rect x="10" y="58" width="640" height="26" fill="#e3f2fd" stroke="#cccccc" stroke-width="0.5"/>
  <text x="100" y="75" text-anchor="middle" font-size="12" fill="#222222">Initial Access</text>
  <text x="305" y="75" text-anchor="middle" font-size="12" fill="#222222">T1078: Valid Accts</text>
  <text x="535" y="75" text-anchor="middle" font-size="12" fill="#222222">SSH login (E001)</text>
  <!-- Row 2 -->
  <rect x="10" y="84" width="640" height="26" fill="#f5f5f5" stroke="#cccccc" stroke-width="0.5"/>
  <text x="100" y="101" text-anchor="middle" font-size="12" fill="#222222">Execution</text>
  <text x="305" y="101" text-anchor="middle" font-size="12" fill="#222222">T1059: Cmd Shell</text>
  <text x="535" y="101" text-anchor="middle" font-size="12" fill="#222222">bash history (E002)</text>
  <!-- Row 3 -->
  <rect x="10" y="110" width="640" height="26" fill="#e3f2fd" stroke="#cccccc" stroke-width="0.5"/>
  <text x="100" y="127" text-anchor="middle" font-size="12" fill="#222222">Persistence</text>
  <text x="305" y="127" text-anchor="middle" font-size="12" fill="#222222">T1053: Sched Task</text>
  <text x="535" y="127" text-anchor="middle" font-size="12" fill="#222222">cron job (E001)</text>
  <!-- Row 4 -->
  <rect x="10" y="136" width="640" height="26" fill="#f5f5f5" stroke="#cccccc" stroke-width="0.5"/>
  <text x="100" y="153" text-anchor="middle" font-size="12" fill="#222222">Persistence</text>
  <text x="305" y="153" text-anchor="middle" font-size="12" fill="#222222">T1505: Web Shell</text>
  <text x="535" y="153" text-anchor="middle" font-size="12" fill="#222222">cmd.php (E001)</text>
  <!-- Row 5 -->
  <rect x="10" y="162" width="640" height="26" fill="#e3f2fd" stroke="#cccccc" stroke-width="0.5"/>
  <text x="100" y="179" text-anchor="middle" font-size="12" fill="#222222">Credential Access</text>
  <text x="305" y="179" text-anchor="middle" font-size="12" fill="#222222">T1003: OS Cred</text>
  <text x="535" y="179" text-anchor="middle" font-size="12" fill="#222222">/etc/shadow (E001)</text>
  <!-- Row 6 -->
  <rect x="10" y="188" width="640" height="26" fill="#f5f5f5" stroke="#cccccc" stroke-width="0.5"/>
  <text x="100" y="205" text-anchor="middle" font-size="12" fill="#222222">Discovery</text>
  <text x="305" y="205" text-anchor="middle" font-size="12" fill="#222222">T1082: System Info</text>
  <text x="535" y="205" text-anchor="middle" font-size="12" fill="#222222">recon.sh (E001)</text>
  <!-- Row 7 -->
  <rect x="10" y="214" width="640" height="26" fill="#e3f2fd" stroke="#cccccc" stroke-width="0.5"/>
  <text x="100" y="231" text-anchor="middle" font-size="12" fill="#222222">Collection</text>
  <text x="305" y="231" text-anchor="middle" font-size="12" fill="#222222">T1005: Local Data</text>
  <text x="535" y="231" text-anchor="middle" font-size="12" fill="#222222">tar archive (E002)</text>
  <!-- Row 8 -->
  <rect x="10" y="240" width="640" height="26" fill="#f5f5f5" stroke="#cccccc" stroke-width="0.5"/>
  <text x="100" y="257" text-anchor="middle" font-size="12" fill="#222222">Exfiltration</text>
  <text x="305" y="257" text-anchor="middle" font-size="12" fill="#222222">T1041: C2 Channel</text>
  <text x="535" y="257" text-anchor="middle" font-size="12" fill="#222222">TCP 4443 (E003)</text>
  <!-- Outer border -->
  <rect x="10" y="30" width="640" height="236" fill="none" stroke="#333333" stroke-width="1.5"/>
  <!-- Column dividers -->
  <line x1="195" y1="30" x2="195" y2="266" stroke="#888888" stroke-width="1"/>
  <line x1="415" y1="30" x2="415" y2="266" stroke="#888888" stroke-width="1"/>
  <!-- Note section -->
  <text x="10" y="292" font-size="13" font-weight="bold" fill="#333333">Including ATT&amp;CK mapping:</text>
  <text x="22" y="311" font-size="12" fill="#444444">• Provides common language across teams</text>
  <text x="22" y="329" font-size="12" fill="#444444">• Links to known threat actor TTPs · Helps identify gaps in coverage</text>
  <text x="22" y="347" font-size="12" fill="#444444">• Enables pattern matching with threat intel</text>
</svg>

---

## Generating IOC Reports

```bash
# IOC (Indicators of Compromise) extraction for sharing

# Create IOC list from investigation
cat > /evidence/reports/iocs.json << 'IOCEOF'
{
  "case": "CASE-2025-001",
  "date": "2025-01-20",
  "indicators": [
    {
      "type": "ip",
      "value": "10.0.0.99",
      "context": "Attacker source IP"
    },
    {
      "type": "domain",
      "value": "evil.com",
      "context": "Malware download source"
    },
    {
      "type": "sha256",
      "value": "abc123def456...",
      "context": "Malware binary hash"
    },
    {
      "type": "filepath",
      "value": "/tmp/.hidden/toolkit.tar.gz",
      "context": "Attacker toolkit staging"
    },
    {
      "type": "filepath",
      "value": "/var/www/html/cmd.php",
      "context": "PHP web shell"
    }
  ]
}
IOCEOF

# Convert to STIX format for sharing
# Or import into TheHive/MISP for distribution
```

---

## Forensic Lab Setup

```bash
# Essential tools for a Linux forensic workstation

# Analysis tools
sudo apt install sleuthkit autopsy
sudo apt install volatility3  # or pip install
sudo apt install bulk-extractor
sudo apt install foremost scalpel
sudo apt install binwalk hashdeep ssdeep

# Imaging tools
sudo apt install dc3dd dcfldd
sudo apt install ewf-tools
sudo apt install gddrescue

# Binary analysis
sudo apt install gdb radare2 strace ltrace
sudo apt install upx-ucl yara

# Network analysis
sudo apt install wireshark tshark tcpdump
sudo apt install ngrep

# Misc utilities
sudo apt install exiftool plaso-tools
sudo apt install chkrootkit rkhunter

# Verify tool versions
echo "TSK: $(fls -V 2>&1 | head -1)"
echo "Volatility: $(vol --help 2>&1 | head -1)"
echo "dc3dd: $(dc3dd --version 2>&1 | head -1)"
```

---

## Write-Once Evidence Storage

```bash
# Evidence should be stored on write-once or write-protected media

# Option 1: WORM (Write Once Read Many) drives
# Enterprise storage with WORM compliance

# Option 2: Hash-verified storage
# Store evidence with integrity checks
sha256sum /evidence/disk.dd > /evidence/disk.dd.sha256
# Verify periodically
sha256sum -c /evidence/disk.dd.sha256

# Option 3: Evidence management system
# Database tracking all evidence items
# Automated hash verification
# Access logging

# Option 4: Read-only filesystem
# Mount evidence storage as read-only after writing
sudo mount -o remount,ro /evidence/

# Option 5: Immutable backups
# Use cloud storage with object lock
# AWS S3 Object Lock, Azure Immutable Blob Storage
```

---

## Courtroom Presentation Techniques

```misc
VISUAL AIDS FOR COURT
======================
1. Network Topology Diagram
   Show attacker's path through the network
   Simple boxes and arrows, labeled clearly

2. Timeline Poster
   Large-format timeline with key events
   Color-coded by evidence source
   Timestamps in local court timezone

3. Comparison Table
   Before/After state of compromised system
   Side-by-side showing what changed

4. Evidence Chain Diagram
   Visual chain of custody
   Photos of evidence at each stage

5. Screenshot Walkthrough
   Numbered exhibits showing each finding
   Annotations highlighting key elements

Tips:
- Large fonts (minimum 24pt)
- Simple language
- One concept per slide/poster
- Avoid hex dumps unless necessary
```

---

## Continuous Monitoring and Prevention

```bash
# Post-incident: implement monitoring to prevent recurrence

# OSSEC - Host-based IDS
# Monitors file integrity, logs, rootkits
sudo apt install ossec-hids

# Wazuh - Enhanced OSSEC fork
# Central management, compliance, vulnerability detection
# docker compose up (using wazuh Docker images)

# Auditd rules for ongoing monitoring
cat > /etc/audit/rules.d/forensic.rules << 'EOF'
# Monitor authentication files
-w /etc/passwd -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/group -p wa -k identity

# Monitor cron
-w /etc/crontab -p wa -k cron
-w /var/spool/cron -p wa -k cron

# Monitor SSH
-w /etc/ssh/sshd_config -p wa -k ssh_config

# Monitor command execution
-a always,exit -F arch=b64 -S execve -k exec
EOF

sudo auditctl -R /etc/audit/rules.d/forensic.rules
```

---

## Forensic Readiness Planning

```misc
FORENSIC READINESS CHECKLIST
=============================
Before an Incident:
[ ] Enable comprehensive logging (journald, auditd)
[ ] Configure log forwarding to central SIEM
[ ] Enable process accounting
[ ] Establish baseline system configurations
[ ] Deploy file integrity monitoring (AIDE)
[ ] Document network topology
[ ] Maintain hardware/software inventory
[ ] Create forensic toolkit (bootable USB with tools)
[ ] Train staff on evidence handling
[ ] Establish incident response procedures
[ ] Define chain of custody forms
[ ] Test forensic tools and procedures
[ ] Maintain relationships with law enforcement
[ ] Review and update procedures annually

During an Incident:
[ ] Follow order of volatility
[ ] Document everything with timestamps
[ ] Use write blockers
[ ] Hash all evidence
[ ] Maintain chain of custody
```

---

## Course Final Exercise

### Scenario:
A web server has been compromised. You have:
- A disk image (`server.dd`)
- A memory dump (`server.lime`)
- Network capture (`traffic.pcap`)

### Tasks:
1. Mount and analyze the disk image
1. Build a filesystem timeline
1. Analyze memory for running processes
1. Correlate network traffic with disk findings
1. Identify the attack vector and attacker actions
1. Write a complete forensic report

```misc
Deliverables:
- Timeline of events (CSV)
- List of IOCs
- Executive summary
- Full technical report
- Evidence integrity documentation
```
