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

# Password Security and Access Management

---

## Why Passwords Matter

- Passwords are the keys to your digital life
- 81% of hacking-related breaches use stolen or weak passwords
- One compromised password can unlock multiple accounts
- This chapter: how to create, manage, and protect your credentials

---

## Most Common Passwords (Still!)

| Rank | Password | Time to Crack |
|------|----------|---------------|
| 1 | `123456` | Instant |
| 2 | `password` | Instant |
| 3 | `qwerty` | Instant |
| 4 | `abc123` | Instant |
| 5 | `letmein` | Instant |

- If your password is on this list, change it today
- If it is based on your name, birthday, or pet's name, it is nearly as weak

---

## How Attackers Crack Passwords

- **Brute force** - trying every possible combination
- **Dictionary attack** - trying common words and phrases
- **Credential stuffing** - reusing leaked passwords from other sites
- **Shoulder surfing** - literally watching you type
- **Phishing** - tricking you into entering your password on a fake site

---

## Password Strength Visualized

```misc
Weak:       cat         --> cracked in < 1 second
            |||
Fair:       Cat2024     --> cracked in ~3 minutes
            |||||||
Good:       C@t$2024!x  --> cracked in ~2 years
            |||||||||||
Excellent:  correct-horse-battery-staple
            --> cracked in ~550 years
```

- Length beats complexity
- A long passphrase is stronger than a short complex password

---

## Creating Strong Passwords: The Passphrase Method
- Pick 4-5 random, unrelated words
- Add a number or symbol between them
- Example: `purple-hammer-cloud-bicycle-9`
- Easy to remember, hard to crack

### Rules to Follow
- Minimum 12 characters (16+ is better)
- Never reuse passwords across accounts
- Never use personal information
- Change passwords if a breach is suspected

---

## Password Managers
- Store all your passwords in one encrypted vault
- Generate strong, unique passwords for every account
- Auto-fill login forms securely
- You only need to remember one master password

### Recommended by Our Organization
- Use the company-approved password manager
- Store work passwords only in the approved tool
- Never store passwords in browsers, sticky notes, or spreadsheets

---

## Password Manager Workflow

![password_manager_workflow](svg/courses/security/it-security-policies/02_password_security/password_manager_workflow.svg)

---

## Multi-Factor Authentication (MFA)
- Something you **know** (password)
- Something you **have** (phone, security key)
- Something you **are** (fingerprint, face)

Using two or more of these factors dramatically improves security

---

## MFA in Practice: Common Second Factors

| Method | Security Level | Convenience |
|--------|---------------|-------------|
| `SMS` code | Fair | High |
| Authenticator app | Good | High |
| Hardware key (`YubiKey`) | Excellent | Medium |
| Biometrics | Good | High |

- Enable `MFA` on every account that supports it
- Authenticator apps are preferred over `SMS` codes
- `SMS` can be intercepted via SIM swapping attacks

---

## Role-Based Access Control (`RBAC`)
- You should only have access to what you need for your job
- No more, no less
- If you change roles, your access should be updated

### Why This Matters
- Limits damage if your account is compromised
- Reduces accidental exposure of sensitive data
- Meets compliance requirements (`GDPR`, `SOX`, `HIPAA`)

---

## Access Management Best Practices

- **Request** only the access you actually need
- **Report** if you have access to systems you should not
- **Revoke** access immediately when someone leaves your team
- **Review** your access permissions annually
- **Never** share your credentials with anyone, including IT staff

---

## What to Do If Your Password Is Compromised

1. Change the compromised password immediately
1. Change it on any other site where you used the same password
1. Enable `MFA` if not already active
1. Notify your IT security team
1. Monitor your accounts for unusual activity
1. Check if your email appears on `haveibeenpwned.com`

---

## Exercise: Check Your Password Hygiene

Ask yourself:
- Do I reuse passwords across accounts?
- Is my password based on personal information?
- Do I have `MFA` enabled on my critical accounts?
- Am I using a password manager?
- Have I shared my password with anyone?

If you answered "yes" to the first three or "no" to the last two, take action today.

---

## Key Takeaways

- Use long passphrases, not short complex passwords
- Never reuse passwords across different accounts
- Use the company-approved password manager
- Enable `MFA` everywhere possible
- Follow the principle of least privilege
- Report any suspected credential compromise immediately
