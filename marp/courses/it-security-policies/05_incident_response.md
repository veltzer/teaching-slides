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

```text
+------------+     +------------+     +------------+     +------------+
|            |     |            |     |            |     |            |
| 1. DETECT  |---->| 2. CONTAIN |---->| 3. REMOVE  |---->| 4. RECOVER |
|            |     |            |     |            |     |            |
| Identify   |     | Stop the   |     | Eliminate  |     | Restore    |
| the issue  |     | spread     |     | the threat |     | operations |
|            |     |            |     |            |     |            |
+------------+     +------------+     +------------+     +-----+------+
                                                               |
                                                               v
                                                      +------------+
                                                      | 5. LEARN   |
                                                      | Improve    |
                                                      | for next   |
                                                      | time       |
                                                      +------------+
```

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

```text
+-------------------+
| Security Incident |
+--------+----------+
         |
         v
+-------------------+     +---------------------------+
| Report via:       |     | Include:                  |
| - Security hotline|     | - What happened           |
| - Email to        |     | - When it happened        |
|   security@co.com |     | - What device/system      |
| - Incident portal |     | - What you did so far     |
| - Your manager    |     | - Any error messages      |
+-------------------+     | - Screenshots if possible |
                          +---------------------------+
```

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

```text
+---------------------------------------------+
|                                               |
|   "The only wrong thing to do is nothing."    |
|                                               |
|   Report early. Report everything.            |
|   We will figure it out together.             |
|                                               |
+---------------------------------------------+
```

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

```text
         Data loss          Downtime
         tolerated          tolerated
    <--------------->  <----------------->

----+---+---+---+---+---+---+---+---+---+---->
    |               |                   |     time
  Last backup    Disaster           Recovery
                 occurs             complete

    |<----RPO----->|<------RTO-------->|
```

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

```text
1. Infection         2. Encryption        3. Ransom Note
+-------------+    +---------------+    +------------------+
| Malicious   |    | All files     |    | "Pay $500,000    |
| link/file   |--->| encrypted     |--->|  in Bitcoin or   |
| opened      |    | .locked       |    |  lose your data" |
+-------------+    +---------------+    +------------------+
```

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
