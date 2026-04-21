---
tags:
  - security:security
  - security:policies
  - security:compliance
level: beginner
category: security
audience:
  - audiences:managers
  - audiences:it-staff

---

# Incident Response and Reporting

---

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

![the_incident_response_lifecycle](svg/courses/security/it-security-policies/06_incident_response/the_incident_response_lifecycle.svg)

---

## Step 1: Detect and Identify
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
- **Do not turn off your computer** (it may destroy evidence)
- Disconnect from Wi-Fi or unplug the network cable
- Do not log into other accounts from the affected device
- Do not try to fix the problem yourself
- Note what you were doing when the incident occurred
- Write down any error messages or unusual behavior

---

## Your Reporting Channels

![your_reporting_channels](svg/courses/security/it-security-policies/06_incident_response/your_reporting_channels.svg)

---

## Reporting: What to Say
- **What happened**: "I clicked a link in an email and was taken to a login page that looked suspicious"
- **When**: "Today at 2:15 PM"
- **What system/device**: "My work laptop, Windows, connected to office Wi-Fi"
- **What I did**: "I entered my username but realized it was fake before entering my password. I disconnected from Wi-Fi"
- **Current status**: "Laptop is off the network, waiting for instructions"

---

## No-Blame Culture: Details

- **You will not be punished** for reporting a security incident
- The biggest risk is NOT reporting
- An unreported incident can escalate from minor to catastrophic
- Early reporting saves the company time, money, and reputation

---

## No-Blame Culture

> **"The only wrong thing to do is nothing."**

- Report early. Report everything.
- We will figure it out together.

---

## Business Continuity Planning
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

![rto_and_rpo_explained](svg/courses/security/it-security-policies/06_incident_response/rto_and_rpo_explained.svg)

---

## Disaster Recovery: Details

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

![what_happens_in_a_ransomware_attack](svg/courses/security/it-security-policies/06_incident_response/what_happens_in_a_ransomware_attack.svg)

---

## Ransomware: The Growing Threat: Details

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
- Root cause analysis identifies what went wrong
- Improvements are made to prevent recurrence
- Policies and procedures are updated
- Additional training is provided if needed
- No incident is wasted if we learn from it

### Common Root Causes
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
