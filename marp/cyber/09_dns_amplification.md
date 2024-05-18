# DNS Amplification Attacks

DNS amplification is a type of Distributed Denial of Service (DDoS) attack that exploits open DNS resolvers to amplify malicious traffic directed at a target system or network.

---

## How DNS Amplification Works

1. Attacker finds open DNS resolvers on the internet
2. Sends small DNS queries with spoofed source IP (victim's IP)
3. Open resolvers respond to the spoofed query, sending larger DNS responses to victim
4. With many open resolvers, amplified traffic overwhelms victim's resources

---

## Amplification Factor

- Attacker's query is small (e.g., few bytes)
- DNS response from open resolver is much larger (e.g., kilobytes)
- Amplification factor can range from 10x to 1000x
- Generates massive traffic with little bandwidth from attacker

---

## Diagram

![](https://veltzer.github.io/assets/mermaid/cyber/dns_amplification.png)

---

## Impact of DNS Amplification

- Overwhelms victim's network and server resources
- Causes Denial of Service for legitimate users
- Difficult to trace the source of the attack
- Can target any system or network on the internet

---

## Mitigating DNS Amplification

- Disable open DNS resolvers (only respond to legitimate sources)
- Implement DDoS protection and traffic filtering
- Use DNS Response Rate Limiting (RRL)
- Deploy Anycast DNS to distribute traffic across multiple servers
- Keep DNS software up-to-date and patched

---

## Conclusion

DNS amplification attacks are a significant threat, as they can generate massive amounts of traffic with relatively little effort from the attacker. By securing DNS infrastructure, implementing DDoS mitigation strategies, and keeping systems up-to-date, organizations can protect themselves from these types of attacks and maintain the availability of their online services.
