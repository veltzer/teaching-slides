# Phishing: Don't Take the Bait
---
## What is Phishing?
- Phishing is a type of cyber attack where criminals attempt to steal sensitive information like login credentials or financial information
- Phishers use fraudulent emails, texts, websites, and other tactics to trick victims into revealing this information
- Phishing attacks often impersonate legitimate companies, organizations, or individuals
- Responsible for over 80% of reported security incidents
- Average cost of a phishing attack for a mid-sized company: $1.6 million

---
## How Phishers Lure Victims

- Phishing emails and messages typically:
    - Appear to come from a trusted source
    - Create a sense of urgency
    - Ask you to update or verify account information
    - Offer an enticing deal or reward
- Malicious links and attachments can install malware on your device

```bash
┌──────────────────────────────────────────────────────────┐
│  Phishing Psychology: Triggering Action                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Urgency:  "Your account will be suspended in 24 hours" │
│  Fear:     "Unauthorized login detected on your account" │
│  Greed:    "You've won a $500 gift card"                │
│  Curiosity:"Someone shared a document with you"          │
│  Authority:"CEO: Please process this wire transfer"      │
│  Trust:    "Microsoft Security Team: Action Required"    │
└──────────────────────────────────────────────────────────┘
```

---
## Types of Phishing Attacks

| Type              | Target           | Channel       | Sophistication |
|-------------------|------------------|---------------|----------------|
| Email Phishing    | Mass / anyone    | Email         | Low            |
| Spear Phishing    | Specific person  | Email         | High           |
| Whaling           | C-suite/execs    | Email         | Very High      |
| Vishing           | Anyone           | Voice/phone   | Medium         |
| Smishing          | Anyone           | SMS/text      | Medium         |
| Angler Phishing   | Social users     | Social media  | Medium         |
| Pharming          | Anyone           | DNS redirect  | High           |
| BEC               | Finance teams    | Email         | Very High      |
| Clone Phishing    | Previous recipients| Email       | High           |

---
## Spear Phishing

```python
┌──────────────────────────────────────────────────────────┐
│          Spear Phishing Attack Flow                       │
│                                                          │
│  1. RECONNAISSANCE                                       │
│     Attacker researches target via:                      │
│     - LinkedIn (job title, connections, recent posts)    │
│     - Company website (org chart, press releases)        │
│     - Social media (personal interests, travel)          │
│     - OSINT tools (theHarvester, Maltego)                │
│                                                          │
│  2. CRAFTING                                             │
│     Attacker creates highly personalized email:          │
│     - References real colleagues, projects, events       │
│     - Mimics internal email formatting                   │
│     - Uses legitimate-looking sender address             │
│                                                          │
│  3. DELIVERY                                             │
│     - Sent during business hours                         │
│     - May come from compromised colleague account        │
│     - Contains malicious link or attachment              │
│                                                          │
│  4. EXPLOITATION                                         │
│     - Credential harvesting (fake login page)            │
│     - Malware installation (weaponized document)         │
│     - Direct data theft                                  │
└──────────────────────────────────────────────────────────┘
```

---
## Whaling: Targeting Executives

- Targets C-level executives, board members, senior managers
- Extremely well-researched and personalized
- Often impersonates legal proceedings, regulatory bodies, or other executives

**Example whaling email:**
```c
From: legal-department@company-legal-notice.com
To: ceo@company.com
Subject: URGENT: Pending Litigation - Immediate Response Required

Dear [CEO Name],

A complaint has been filed against [Company Name] in the
US District Court. Please review the attached subpoena
and respond within 48 hours to avoid default judgment.

[Malicious PDF attachment]

Regards,
[Legitimate-looking law firm name]
```

---
## Vishing (Voice Phishing)

```python
┌──────────────────────────────────────────────────────────┐
│          Vishing Attack Scenario                          │
│                                                          │
│  Phone rings: Caller ID shows "Bank of America"          │
│  (spoofed number)                                        │
│                                                          │
│  "This is the fraud department at Bank of America.       │
│   We've detected suspicious activity on your account.    │
│   A charge of $2,847 was attempted from Romania.         │
│   For your security, we need to verify your identity."   │
│                                                          │
│  Attacker asks for:                                      │
│  - Full card number (to "verify" the account)            │
│  - CVV code                                              │
│  - PIN or password                                       │
│  - SSN "for verification"                                │
│  - One-time code sent to phone (bypasses MFA!)           │
│                                                          │
│  Modern vishing uses:                                    │
│  - AI voice cloning of real employees                    │
│  - VoIP for untraceable calls                            │
│  - Caller ID spoofing                                    │
│  - Robocalls for mass targeting                          │
└──────────────────────────────────────────────────────────┘
```

---
## Smishing (SMS Phishing)

```bash
Common smishing messages:

"USPS: Your package has a delivery problem.
Update your address here: https://usps-delivery.xyz/track"

"[Bank Name] ALERT: Unusual sign-in to your account.
If this wasn't you, verify at: https://bank-secure.xyz"

"IRS: You are eligible for a $1,200 tax refund.
Claim now at: https://irs-refund.xyz/claim"

"Your Apple ID has been locked due to suspicious activity.
Unlock at: https://apple-id-verify.xyz"
```

- SMS has higher open rates than email (~98% vs ~20%)
- Short URLs hide the real destination
- Mobile browsers show less of the URL
- Users are less cautious on mobile devices
- Difficult to filter compared to email

---
## Business Email Compromise (BEC)

```python
┌──────────────────────────────────────────────────────────┐
│          BEC Attack Types                                 │
│                                                          │
│  Type 1: CEO Fraud                                       │
│  Impersonate CEO -> Email CFO -> "Wire $50K urgently"    │
│                                                          │
│  Type 2: Vendor Email Compromise                         │
│  Compromise vendor -> Send fake invoice with new         │
│  bank details -> Company pays attacker                   │
│                                                          │
│  Type 3: Account Compromise                              │
│  Hack employee email -> Request payments from contacts   │
│                                                          │
│  Type 4: Attorney Impersonation                          │
│  Impersonate lawyer -> "Time-sensitive M&A payment"      │
│                                                          │
│  Type 5: Data Theft                                      │
│  Target HR/Payroll -> "Send all W-2 forms"               │
│                                                          │
│  FBI IC3 reported $2.7 billion in BEC losses (2022)      │
│  Average BEC loss: $125,000 per incident                 │
└──────────────────────────────────────────────────────────┘
```

---
## Email Header Analysis

```bash
# Key headers to examine in suspicious emails

# 1. Check the actual sender (not just display name)
From: "Microsoft Security" <xk38f@mail-server-47.ru>
# Display name is fake, actual sender domain is suspicious

# 2. Check the Return-Path (where bounces go)
Return-Path: <attacker@evil-domain.com>

# 3. Examine Received headers (trace the route, bottom to top)
Received: from mail-server-47.ru (93.184.216.34)
    by your-mail-server.com
    Fri, 15 Mar 2024 10:23:45 +0000
# Does the originating IP match the claimed sender domain?

# 4. Check authentication results
Authentication-Results: mx.google.com;
    spf=fail (domain does not designate 93.184.216.34)
    dkim=fail (signature did not verify)
    dmarc=fail

# 5. Check Reply-To (may differ from From)
Reply-To: support@micrsooft-security.com
# Note the typo: "micrsooft"

# Command-line analysis
# View all headers
cat suspicious_email.eml | grep -E "^(From|To|Subject|Received|Return-Path|Reply-To|Authentication)"
```

---
## DMARC, DKIM, and SPF

![dmarc_dkim_and_spf](svg/courses/security/cyber-attacks-and-vectors/23_phishing/dmarc_dkim_and_spf.svg)

```bash
# Check SPF record
dig TXT example.com | grep "v=spf1"
# v=spf1 include:_spf.google.com -all

# Check DKIM record
dig TXT google._domainkey.example.com
# v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3...

# Check DMARC record
dig TXT _dmarc.example.com
# v=DMARC1; p=reject; rua=mailto:dmarc@example.com;

# DMARC policy levels:
# p=none       Monitor only (receive reports)
# p=quarantine Send failures to spam
# p=reject     Block failures entirely (strongest)
```

---
## How SPF, DKIM, and DMARC Work Together

```python
┌──────────────────────────────────────────────────────────┐
│  Email: From: ceo@company.com                            │
│  Sent from IP: 203.0.113.50                              │
│                                                          │
│  Step 1: SPF Check                                       │
│  ├── Look up company.com SPF record                      │
│  ├── "v=spf1 ip4:198.51.100.0/24 -all"                 │
│  ├── 203.0.113.50 is NOT in authorized range             │
│  └── SPF: FAIL                                           │
│                                                          │
│  Step 2: DKIM Check                                      │
│  ├── Extract DKIM signature from email header            │
│  ├── Look up public key in DNS                           │
│  ├── Signature does not match (forged email)             │
│  └── DKIM: FAIL                                          │
│                                                          │
│  Step 3: DMARC Check                                     │
│  ├── Look up _dmarc.company.com                          │
│  ├── "v=DMARC1; p=reject;"                               │
│  ├── Both SPF and DKIM failed                            │
│  ├── Policy is "reject"                                  │
│  └── ACTION: Email is REJECTED (never delivered)         │
└──────────────────────────────────────────────────────────┘
```

---
## Phishing Detection Indicators

```bash
┌──────────────────────────────────────────────────────────┐
│  Red Flags in Phishing Emails                            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Sender:                                                 │
│  [X] Display name doesn't match email address            │
│  [X] Domain is similar but not exact (g00gle.com)        │
│  [X] Free email provider for "business" communication    │
│                                                          │
│  Content:                                                │
│  [X] Generic greeting ("Dear Customer" vs your name)     │
│  [X] Urgent/threatening language                         │
│  [X] Grammar and spelling errors                         │
│  [X] Request for sensitive information                   │
│  [X] Too-good-to-be-true offers                          │
│                                                          │
│  Links/Attachments:                                      │
│  [X] Hover shows different URL than displayed text       │
│  [X] Shortened URLs (bit.ly, tinyurl.com)               │
│  [X] Unexpected attachments (.zip, .exe, .docm)         │
│  [X] URL contains @ symbol or IP address                 │
│                                                          │
│  Technical:                                              │
│  [X] SPF/DKIM/DMARC failures in headers                 │
│  [X] Mismatched Return-Path and From addresses           │
│  [X] Recently registered sender domain                   │
└──────────────────────────────────────────────────────────┘
```

---
## Modern Phishing Infrastructure

```bash
┌──────────────────────────────────────────────────────────┐
│  Phishing-as-a-Service (PhaaS) Ecosystem                 │
│                                                          │
│  ┌─────────────────────────────────────────────────┐     │
│  │  Phishing Kit Features:                          │     │
│  │  - Pre-built login page clones (100+ brands)     │     │
│  │  - Built-in CAPTCHA to block researchers         │     │
│  │  - Real-time credential relaying (defeats MFA)   │     │
│  │  - Anti-bot protection                           │     │
│  │  - Telegram bot for stolen credential delivery   │     │
│  │  - Admin panel with victim statistics            │     │
│  └─────────────────────────────────────────────────┘     │
│                                                          │
│  Notable PhaaS platforms:                                │
│  - EvilProxy: Real-time MFA bypass proxy                 │
│  - Caffeine: Open phishing platform                      │
│  - Robin Banks: Targeted financial institutions          │
│                                                          │
│  Cost: $200-$1,500/month subscription                    │
│  Skill required: Minimal (point-and-click)               │
└──────────────────────────────────────────────────────────┘
```

---
## Adversary-in-the-Middle (AiTM) Phishing

```bash
┌──────────────────────────────────────────────────────────┐
│  AiTM Phishing (Defeats Traditional MFA)                 │
│                                                          │
│  Victim          Attacker Proxy        Real Website      │
│    │                  │                    │              │
│    │  Clicks phishing │                    │              │
│    │  link             │                    │              │
│    │─────────────────>│                    │              │
│    │                  │  Proxy to real site │              │
│    │  Fake login page │────────────────────>│              │
│    │<─────────────────│                    │              │
│    │                  │                    │              │
│    │  Enter username  │  Forward creds     │              │
│    │  + password      │────────────────────>│              │
│    │─────────────────>│                    │              │
│    │                  │  MFA prompt        │              │
│    │  Enter MFA code  │  Forward MFA code  │              │
│    │─────────────────>│────────────────────>│              │
│    │                  │                    │              │
│    │                  │  Session cookie     │              │
│    │  "Login failed"  │<────────────────────│              │
│    │<─────────────────│                    │              │
│    │                  │                    │              │
│    │  Attacker now has the authenticated session cookie   │
│    │  and can access the account without MFA!             │
└──────────────────────────────────────────────────────────┘

Only FIDO2/WebAuthn hardware keys are resistant to AiTM!
(They bind to the real domain name in the authentication)
```

---
## Security Awareness Training

### Effective Training Program Elements

| Component                    | Frequency       | Purpose                         |
|------------------------------|-----------------|----------------------------------|
| Initial onboarding training  | Once            | Baseline security knowledge      |
| Simulated phishing exercises | Monthly         | Test and reinforce awareness     |
| Micro-learning modules       | Quarterly       | Focused topic updates            |
| Incident debrief             | After incidents | Learn from real events           |
| Role-specific training       | Annual          | Targeted for high-risk roles     |

![effective_training_program_elements](svg/courses/security/cyber-attacks-and-vectors/23_phishing/effective_training_program_elements.svg)

---
## Technical Defenses

```bash
┌──────────────────────────────────────────────────────────┐
│  Anti-Phishing Defense Stack                             │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Email Gateway:                                          │
│  ├── SPF, DKIM, DMARC enforcement                       │
│  ├── URL rewriting and safe links                        │
│  ├── Attachment sandboxing                               │
│  └── ML-based content analysis                           │
│                                                          │
│  Browser/Endpoint:                                       │
│  ├── Google Safe Browsing / SmartScreen                  │
│  ├── Browser extension for URL verification              │
│  ├── DNS filtering (Quad9, Cloudflare for Teams)         │
│  └── Endpoint detection and response (EDR)               │
│                                                          │
│  Identity:                                               │
│  ├── FIDO2/WebAuthn (phishing-resistant MFA)             │
│  ├── Conditional Access policies                         │
│  ├── Impossible travel detection                         │
│  └── Session anomaly detection                           │
│                                                          │
│  Organizational:                                         │
│  ├── Security awareness training                         │
│  ├── Phishing reporting button in email client           │
│  ├── Incident response playbook                          │
│  └── Executive wire transfer verification policies       │
└──────────────────────────────────────────────────────────┘
```

---
## Phishing Incident Response

1. **Report**: User clicks "Report Phishing" button or contacts security team
2. **Triage**: Determine scope -- who else received the email?
3. **Contain**: Remove email from all mailboxes (admin purge)
4. **Assess**: Did anyone click? Enter credentials? Download attachments?
5. **Respond**:
   - Force password reset for affected accounts
   - Revoke active sessions
   - Check for mail forwarding rules (persistence mechanism)
   - Scan endpoints for malware
6. **Block**: Add sender, domain, and URLs to blocklists
7. **Communicate**: Alert other users about the phishing campaign
8. **Improve**: Update email filtering rules, add to training simulations

---
## Key Takeaways

- Phishing remains the number one initial access vector for cyber attacks
- Spear phishing and BEC are highly targeted and cause the greatest financial losses
- AiTM phishing proxies defeat traditional MFA -- only FIDO2/WebAuthn is fully resistant
- Email authentication (SPF + DKIM + DMARC with p=reject) blocks domain spoofing
- Email header analysis reveals spoofed senders and failed authentication
- Security awareness training with regular simulations reduces click rates significantly
- Defense requires both technical controls and human awareness
- Always have an incident response plan specific to phishing scenarios
