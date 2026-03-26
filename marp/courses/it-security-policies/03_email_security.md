# Email Security and Phishing Prevention

## Email: The #1 Attack Vector
- Over 90% of cyberattacks start with a phishing email
- Attackers send 3.4 billion phishing emails every day
- Email is easy to forge and hard to fully secure
- Your ability to spot phishing is critical

---

## What Is Phishing?

- Fraudulent messages designed to trick you into:
    - Clicking a malicious link
    - Opening a dangerous attachment
    - Entering credentials on a fake website
    - Transferring money or sharing sensitive data
- Named after "fishing" - casting a wide net hoping someone bites

---

## Types of Phishing

| Type | Description | Target |
|------|-------------|--------|
| **Phishing** | Mass emails to many people | Anyone |
| **Spear phishing** | Targeted at a specific person | Individual |
| **Whaling** | Targeted at executives | CEO, CFO |
| **Smishing** | Phishing via `SMS` text messages | Phone users |
| **Vishing** | Phishing via voice calls | Phone users |

---

## Anatomy of a Phishing Email

```text
From: security@amaz0n-support.com    <-- Fake domain
To: you@company.com
Subject: URGENT: Your account will be suspended!

Dear Valued Customer,                <-- Generic greeting

We detected unusual activity on your
account. Click the link below to verify
your identity within 24 hours or your   <-- Urgency/fear
account will be permanently suspended.

[Verify Now]                          <-- Malicious link
https://amaz0n-secure.phishing.com    <-- Fake URL

Amazon Customer Support               <-- Impersonation
```

---

## Red Flags to Watch For

- **Sender address** - look carefully at the domain (e.g., `@cornpany.com` vs `@company.com`)
- **Urgency or threats** - "Act now or your account will be closed"
- **Generic greetings** - "Dear Customer" instead of your name
- **Spelling and grammar errors** - though AI-generated phishing is improving
- **Suspicious links** - hover to see the real URL before clicking
- **Unexpected attachments** - especially `.exe`, `.zip`, `.docm` files

---

## The Hover Test

Before clicking any link in an email:

```text
What you see:     [Click here to verify your account]

What you get      https://totally-legit-bank.phishing-site.ru/login
when you hover:   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                  This is NOT your bank!
```

- On a computer: hover your mouse over the link without clicking
- On a phone: long-press the link to preview the URL
- If the URL looks suspicious, do not click it

---

## Real vs. Fake: Can You Tell?

## Scenario 1
- From: `helpdesk@yourcompany.com`
- Subject: "Password reset required by Friday"
- Contains a link to `https://yourcompany.okta.com/reset`

**Likely legitimate** - but verify with IT if unexpected

## Scenario 2
- From: `helpdesk@yourcompany.security-reset.com`
- Subject: "URGENT: Password expires in 1 hour!!!"
- Contains a link to `https://security-reset.com/yourcompany`

**Phishing** - the domain is wrong and the tone is overly urgent

---

## Email Attachments: Proceed with Caution

## Dangerous File Types
- `.exe`, `.bat`, `.cmd` - executable programs
- `.zip`, `.rar` - compressed files that may hide malware
- `.docm`, `.xlsm` - Office files with macros
- `.js`, `.vbs` - script files

## Safe Practices
- Do not open attachments you were not expecting
- Verify with the sender through a separate channel
- Use the company's file-sharing platform instead of email attachments
- Let your antivirus scan attachments before opening

---

## Email Best Practices

- **Think before you click** - pause and evaluate every link
- **Verify the sender** - call or message them separately if unsure
- **Never send sensitive data via email** - use secure file sharing
- **Use `BCC`** when emailing large groups to protect addresses
- **Double-check recipients** before hitting send
- **Do not auto-forward** work email to personal accounts

---

## Spam Filtering

## How It Works
```text
Incoming Email
      |
      v
+------------------+
| Spam Filter      |
| - Known bad      |     +--------+
|   senders        |---->| Spam   |
| - Suspicious     |     | Folder |
|   patterns       |     +--------+
| - Malicious      |
|   attachments    |
+--------+---------+
         |
         v
   +----------+
   |  Inbox   |
   +----------+
```

- Spam filters catch most threats, but not all
- Check your spam folder occasionally for legitimate emails
- Never whitelist a sender just because they asked you to

---

## What to Do When You Spot Phishing

1. **Do not click** any links or open attachments
1. **Do not reply** to the email
1. **Do not forward** it to colleagues (except security team)
1. **Report it** using the company's phishing report button
1. **Delete it** from your inbox after reporting
1. If you already clicked, **report immediately** to IT security

---

## If You Already Clicked...

- Do not panic, but act quickly
- **Disconnect** from the network if instructed by IT
- **Change your password** immediately for the affected account
- **Enable `MFA`** if not already active
- **Report to IT security** - they need to assess the damage
- **Monitor** your accounts for unusual activity
- The sooner you report, the better the outcome

---

## Business Email Compromise (`BEC`)

- Attackers impersonate executives or trusted partners
- Common scenarios:
    - "Please wire $25,000 to this new vendor account"
    - "I need you to buy gift cards and send me the codes"
    - "Please update our bank details for the next payment"
- Always verify financial requests by phone or in person
- Use established approval workflows for any payment changes

---

## Exercise: Spot the Phish

Review these subject lines - which are suspicious?

1. "Invoice #4829 attached - payment overdue"
1. "Meeting notes from Tuesday's project review"
1. "You've won a $500 Amazon gift card! Claim now!"
1. "Quarterly security training reminder"
1. "Your package could not be delivered - click to reschedule"

Answers: 1, 3, and 5 are classic phishing patterns

---

## Key Takeaways

- Phishing is the most common way attackers get in
- Always check the sender address, links, and tone
- Hover over links before clicking
- Report suspicious emails immediately
- If you made a mistake, report it quickly - no blame
- When in doubt, verify through a separate channel
