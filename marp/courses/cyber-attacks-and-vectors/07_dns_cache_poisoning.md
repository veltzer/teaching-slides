# DNS Cache Poisoning
---
## What is DNS Cache Poisoning?

DNS Cache Poisoning, also known as DNS Spoofing, is a type of cyber attack where an attacker exploits vulnerabilities in the Domain Name System (DNS) to redirect traffic from legitimate websites to malicious sites.

The attacker injects forged DNS records into the cache of a recursive DNS server, causing it to return incorrect IP addresses for requested domains.

---

## How Does DNS Cache Poisoning Work?

1. The attacker sends a large number of forged DNS responses to a recursive DNS server, containing false information mapping a domain name to a malicious IP address.

2. If one of the forged responses passes the validation checks and matches an existing recursive query, the server will cache the false record.

3. When a user requests the domain associated with the poisoned record, the recursive DNS server will return the malicious IP address, redirecting the user's traffic to a malicious site.

---

## Diagram

![](../../../out/mermaid/cyber/dns_cache_poisoning.png)

---
## Consequences of DNS Cache Poisoning

- User traffic is redirected to malicious sites without their knowledge
- Sensitive information (e.g., login credentials, financial data) can be stolen
- Users can be exposed to malware, phishing attacks, or drive-by downloads
- Legitimate websites can be defaced or taken offline (Denial of Service)
- Damage to reputation and loss of customer trust

---

## Mitigating DNS Cache Poisoning

- Implementing DNS Security Extensions (DNSSEC) to digitally sign DNS records
- Using source port randomization and randomized query IDs
- Reducing the cache entry lifetime (TTL) for records
- Monitoring and filtering DNS traffic for suspicious activity
- Regularly updating DNS software and applying security patches
- Implementing redundant and diverse DNS infrastructure

---

## DNS Cache Poisoning Prevention Best Practices

- Enforce strict input validation and data sanitization
- Implement secure coding practices and code reviews
- Conduct regular security audits and penetration testing
- Monitor DNS logs and alerts for anomalies
- Educate users on the risks of DNS cache poisoning and phishing attacks
- Have an incident response plan in place for rapid mitigation
