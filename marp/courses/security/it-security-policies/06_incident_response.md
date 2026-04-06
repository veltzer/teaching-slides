# Incident Response and Reporting

## When Things Go Wrong
- No security system is 100% effective
- Incidents will happen - what matters is how we respond
- Speed of response directly affects the damage
- Every employee plays a role in incident response

---

## What Is a Security Incident?

- Any event that threatens the confidentiality, integrity, or availability of data or systems
- Examples:
    - You clicked on a phishing link
    - Your laptop was stolen
    - You sent sensitive data to the wrong person
    - You noticed unauthorized access to a system
    - A colleague shared their password
    - You found a USB drive and plugged it in
    - Ransomware message appears on your screen

---

## Incident Severity Levels

| Level | Severity | Example | Response Time |
|-------|----------|---------|---------------|
| 1 | **Critical** | Ransomware attack, major data breach | Immediate |
| 2 | **High** | Compromised executive account, active intrusion | Within 1 hour |
| 3 | **Medium** | Phishing email clicked, lost USB drive | Within 4 hours |
| 4 | **Low** | Suspicious email received, minor policy violation | Within 24 hours |

- When in doubt, report at a higher level - it is better to over-report

---

## The Incident Response Lifecycle

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="250" font-family="sans-serif">
  <defs>
    <marker id="arr1" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <!-- Box 1: DETECT -->
  <rect x="10" y="20" width="155" height="90" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="87" y="48" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">1. DETECT</text>
  <text x="87" y="67" text-anchor="middle" font-size="13" fill="#222222">Identify</text>
  <text x="87" y="85" text-anchor="middle" font-size="13" fill="#222222">the issue</text>
  <!-- Arrow 1→2 -->
  <line x1="165" y1="65" x2="183" y2="65" stroke="#555" stroke-width="1.5" marker-end="url(#arr1)"/>
  <!-- Box 2: CONTAIN -->
  <rect x="185" y="20" width="155" height="90" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="262" y="48" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">2. CONTAIN</text>
  <text x="262" y="67" text-anchor="middle" font-size="13" fill="#222222">Stop the</text>
  <text x="262" y="85" text-anchor="middle" font-size="13" fill="#222222">spread</text>
  <!-- Arrow 2→3 -->
  <line x1="340" y1="65" x2="358" y2="65" stroke="#555" stroke-width="1.5" marker-end="url(#arr1)"/>
  <!-- Box 3: REMOVE -->
  <rect x="360" y="20" width="155" height="90" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="437" y="48" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">3. REMOVE</text>
  <text x="437" y="67" text-anchor="middle" font-size="13" fill="#222222">Eliminate</text>
  <text x="437" y="85" text-anchor="middle" font-size="13" fill="#222222">the threat</text>
  <!-- Arrow 3→4 -->
  <line x1="515" y1="65" x2="533" y2="65" stroke="#555" stroke-width="1.5" marker-end="url(#arr1)"/>
  <!-- Box 4: RECOVER -->
  <rect x="535" y="20" width="155" height="90" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="612" y="48" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">4. RECOVER</text>
  <text x="612" y="67" text-anchor="middle" font-size="13" fill="#222222">Restore</text>
  <text x="612" y="85" text-anchor="middle" font-size="13" fill="#222222">operations</text>
  <!-- Arrow 4↓5 -->
  <line x1="612" y1="110" x2="612" y2="148" stroke="#555" stroke-width="1.5" marker-end="url(#arr1)"/>
  <!-- Box 5: LEARN -->
  <rect x="535" y="150" width="155" height="90" rx="4" fill="#e8f5e9" stroke="#333333" stroke-width="1.5"/>
  <text x="612" y="183" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">5. LEARN</text>
  <text x="612" y="202" text-anchor="middle" font-size="13" fill="#222222">Improve for</text>
  <text x="612" y="220" text-anchor="middle" font-size="13" fill="#222222">next time</text>
</svg>

---

## Step 1: Detect and Identify

## How to Recognize an Incident
- Unexpected pop-ups or system behavior
- Files that have been encrypted or renamed
- Accounts locked out without reason
- Unfamiliar software installed on your computer
- Colleagues receiving strange emails from your account
- Alerts from your antivirus software
- Unusual charges or transactions

Trust your instincts - **if something feels wrong, report it**

---

## Step 2: Contain the Damage

## What You Can Do Immediately
- **Do not turn off your computer** (it may destroy evidence)
- Disconnect from Wi-Fi or unplug the network cable
- Do not log into other accounts from the affected device
- Do not try to fix the problem yourself
- Note what you were doing when the incident occurred
- Write down any error messages or unusual behavior

---

## How to Report a Security Incident

## Your Reporting Channels

<svg xmlns="http://www.w3.org/2000/svg" width="650" height="265" font-family="sans-serif">
  <defs>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <!-- Top box: Security Incident -->
  <rect x="200" y="10" width="250" height="40" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="325" y="35" text-anchor="middle" font-size="14" font-weight="bold" fill="#222222">Security Incident</text>
  <!-- Vertical line down from top box -->
  <line x1="325" y1="50" x2="325" y2="73" stroke="#555" stroke-width="1.5"/>
  <!-- Horizontal T-junction -->
  <line x1="155" y1="73" x2="495" y2="73" stroke="#555" stroke-width="1.5"/>
  <!-- Arrow down to left box -->
  <line x1="155" y1="73" x2="155" y2="88" stroke="#555" stroke-width="1.5" marker-end="url(#arr2)"/>
  <!-- Arrow down to right box -->
  <line x1="495" y1="73" x2="495" y2="88" stroke="#555" stroke-width="1.5" marker-end="url(#arr2)"/>
  <!-- Left box: Report via -->
  <rect x="20" y="90" width="270" height="160" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="155" y="112" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Report via:</text>
  <text x="40" y="133" font-size="13" fill="#222222">• Security hotline</text>
  <text x="40" y="153" font-size="13" fill="#222222">• Email to security@co.com</text>
  <text x="40" y="173" font-size="13" fill="#222222">• Incident portal</text>
  <text x="40" y="193" font-size="13" fill="#222222">• Your manager</text>
  <!-- Right box: Include -->
  <rect x="360" y="90" width="270" height="160" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="495" y="112" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Include:</text>
  <text x="380" y="133" font-size="13" fill="#222222">• What happened</text>
  <text x="380" y="153" font-size="13" fill="#222222">• When it happened</text>
  <text x="380" y="173" font-size="13" fill="#222222">• What device/system</text>
  <text x="380" y="193" font-size="13" fill="#222222">• What you did so far</text>
  <text x="380" y="213" font-size="13" fill="#222222">• Any error messages</text>
  <text x="380" y="233" font-size="13" fill="#222222">• Screenshots if possible</text>
</svg>

---

## Reporting: What to Say

## Template for Reporting an Incident
- **What happened**: "I clicked a link in an email and was taken to a login page that looked suspicious"
- **When**: "Today at 2:15 PM"
- **What system/device**: "My work laptop, Windows, connected to office Wi-Fi"
- **What I did**: "I entered my username but realized it was fake before entering my password. I disconnected from Wi-Fi"
- **Current status**: "Laptop is off the network, waiting for instructions"

---

## No-Blame Culture

- **You will not be punished** for reporting a security incident
- The biggest risk is NOT reporting
- An unreported incident can escalate from minor to catastrophic
- Early reporting saves the company time, money, and reputation

<svg xmlns="http://www.w3.org/2000/svg" width="600" height="130" font-family="sans-serif">
  <rect x="10" y="10" width="580" height="110" rx="4" fill="#fff3e0" stroke="#333333" stroke-width="1.5"/>
  <text x="300" y="47" text-anchor="middle" font-size="14" font-style="italic" font-weight="bold" fill="#222222">"The only wrong thing to do is nothing."</text>
  <text x="300" y="73" text-anchor="middle" font-size="13" fill="#222222">Report early. Report everything.</text>
  <text x="300" y="95" text-anchor="middle" font-size="13" fill="#222222">We will figure it out together.</text>
</svg>

---

## Business Continuity Planning

## What Is Business Continuity?
- The plan for keeping the business running during and after a disruption
- Covers scenarios like:
    - Cyberattack (ransomware, data breach)
    - Natural disaster (flood, earthquake, fire)
    - Infrastructure failure (power outage, network down)
    - Pandemic or health emergency

---

## Your Role in Business Continuity

- **Know your role**: understand what is expected of you during an incident
- **Know your contacts**: have emergency contact numbers saved offline
- **Know the plan**: read the business continuity plan for your department
- **Keep backups**: ensure your critical work is backed up regularly
- **Test**: participate in business continuity exercises when scheduled

---

## Disaster Recovery

## `RTO` and `RPO` Explained

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="165" font-family="sans-serif">
  <defs>
    <marker id="arr4" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <!-- Labels above spans -->
  <text x="225" y="18" text-anchor="middle" font-size="12" fill="#555">Data loss tolerated</text>
  <text x="475" y="18" text-anchor="middle" font-size="12" fill="#555">Downtime tolerated</text>
  <!-- RPO double-headed arrow -->
  <line x1="100" y1="35" x2="350" y2="35" stroke="#555" stroke-width="1.5"/>
  <polygon points="100,31 100,39 90,35" fill="#555"/>
  <polygon points="350,31 350,39 360,35" fill="#555"/>
  <text x="225" y="52" text-anchor="middle" font-size="12" font-weight="bold" fill="#444">RPO</text>
  <!-- RTO double-headed arrow -->
  <line x1="370" y1="35" x2="570" y2="35" stroke="#555" stroke-width="1.5"/>
  <polygon points="370,31 370,39 360,35" fill="#555"/>
  <polygon points="570,31 570,39 580,35" fill="#555"/>
  <text x="475" y="52" text-anchor="middle" font-size="12" font-weight="bold" fill="#444">RTO</text>
  <!-- Dashed vertical connectors -->
  <line x1="90" y1="40" x2="90" y2="78" stroke="#999" stroke-width="1" stroke-dasharray="3,2"/>
  <line x1="360" y1="40" x2="360" y2="78" stroke="#999" stroke-width="1" stroke-dasharray="3,2"/>
  <line x1="580" y1="40" x2="580" y2="78" stroke="#999" stroke-width="1" stroke-dasharray="3,2"/>
  <!-- Main timeline -->
  <line x1="40" y1="88" x2="655" y2="88" stroke="#333" stroke-width="2" marker-end="url(#arr4)"/>
  <!-- Tick marks -->
  <line x1="90" y1="80" x2="90" y2="96" stroke="#333" stroke-width="1.5"/>
  <line x1="360" y1="80" x2="360" y2="96" stroke="#333" stroke-width="1.5"/>
  <line x1="580" y1="80" x2="580" y2="96" stroke="#333" stroke-width="1.5"/>
  <!-- "time" label -->
  <text x="665" y="92" font-size="12" fill="#222222">time</text>
  <!-- Labels below timeline -->
  <text x="90" y="112" text-anchor="middle" font-size="12" fill="#222222">Last backup</text>
  <text x="360" y="112" text-anchor="middle" font-size="12" fill="#222222">Disaster</text>
  <text x="360" y="127" text-anchor="middle" font-size="12" fill="#222222">occurs</text>
  <text x="580" y="112" text-anchor="middle" font-size="12" fill="#222222">Recovery</text>
  <text x="580" y="127" text-anchor="middle" font-size="12" fill="#222222">complete</text>
</svg>

- `RPO` (Recovery Point Objective): how much data can we afford to lose?
- `RTO` (Recovery Time Objective): how quickly must we restore operations?
- Your backups determine `RPO`; your recovery plan determines `RTO`

---

## Backup Best Practices for Employees

- Save work to company-approved cloud storage (not local desktop)
- Do not rely solely on your local hard drive
- Follow the 3-2-1 rule:
    - **3** copies of your data
    - **2** different types of storage
    - **1** copy off-site (cloud)
- Verify that your backups are working periodically
- Know how to restore from backup if needed

---

## Ransomware: The Growing Threat

## What Happens in a Ransomware Attack

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="120" font-family="sans-serif">
  <defs>
    <marker id="arr5" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <!-- Box 1: Infection -->
  <rect x="10" y="10" width="205" height="100" rx="4" fill="#fff3e0" stroke="#333333" stroke-width="1.5"/>
  <text x="112" y="38" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">1. Infection</text>
  <text x="112" y="57" text-anchor="middle" font-size="13" fill="#222222">Malicious link/file</text>
  <text x="112" y="75" text-anchor="middle" font-size="13" fill="#222222">opened</text>
  <!-- Arrow 1→2 -->
  <line x1="215" y1="60" x2="243" y2="60" stroke="#555" stroke-width="1.5" marker-end="url(#arr5)"/>
  <!-- Box 2: Encryption -->
  <rect x="245" y="10" width="205" height="100" rx="4" fill="#fff3e0" stroke="#333333" stroke-width="1.5"/>
  <text x="347" y="38" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">2. Encryption</text>
  <text x="347" y="57" text-anchor="middle" font-size="13" fill="#222222">All files encrypted</text>
  <text x="347" y="75" text-anchor="middle" font-size="13" fill="#222222">.locked</text>
  <!-- Arrow 2→3 -->
  <line x1="450" y1="60" x2="478" y2="60" stroke="#555" stroke-width="1.5" marker-end="url(#arr5)"/>
  <!-- Box 3: Ransom Note -->
  <rect x="480" y="10" width="210" height="100" rx="4" fill="#fff3e0" stroke="#333333" stroke-width="1.5"/>
  <text x="585" y="38" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">3. Ransom Note</text>
  <text x="585" y="57" text-anchor="middle" font-size="13" fill="#222222">"Pay $500,000 in</text>
  <text x="585" y="75" text-anchor="middle" font-size="13" fill="#222222">Bitcoin or lose</text>
  <text x="585" y="93" text-anchor="middle" font-size="13" fill="#222222">your data"</text>
</svg>

- Average ransom payment: over $1 million
- Average downtime: 22 days
- Prevention is far cheaper than recovery

---

## If You See a Ransom Message

1. **Do not pay** - payment does not guarantee recovery
1. **Do not restart** your computer
1. **Disconnect** from the network immediately
1. **Photograph** the ransom message with your phone
1. **Report** to IT security immediately
1. **Do not** attempt to decrypt files yourself
1. **Wait** for instructions from the incident response team

---

## Lessons from Real Incidents

## What We Learn After Every Incident
- Root cause analysis identifies what went wrong
- Improvements are made to prevent recurrence
- Policies and procedures are updated
- Additional training is provided if needed
- No incident is wasted if we learn from it

## Common Root Causes
- Phishing email clicked (most common)
- Weak or reused passwords
- Unpatched software
- Misconfigured access permissions

---

## Key Takeaways

- Know how to recognize a security incident
- Report incidents immediately - speed matters
- Use the proper reporting channels and include key details
- Never try to fix a security incident on your own
- There is no blame for reporting - only for hiding
- Know your role in the business continuity plan
- Keep your work backed up to company-approved storage
- If you see ransomware, disconnect and report
