# DNS Amplification Attacks

- DNS amplification is a type of Distributed Denial of Service (DDoS) attack that exploits open DNS resolvers to amplify malicious traffic directed at a target system or network
---
## How DNS Amplification Works

1. Attacker finds open DNS resolvers on the internet
1. Sends small DNS queries with spoofed source IP (victim's IP)
1. Open resolvers respond to the spoofed query, sending larger DNS responses to victim
1. With many open resolvers, amplified traffic overwhelms victim's resources
---
## Amplification Factor

- Attacker's query is small (e.g., few bytes)
- DNS response from open resolver is much larger (e.g., kilobytes)
- Amplification factor can range from 10x to 1000x
- Generates massive traffic with little bandwidth from attacker
---
## Diagram

<svg width="700" height="400" xmlns="http://www.w3.org/2000/svg">
  <!-- Attacker -->
  <rect x="50" y="180" width="100" height="40" fill="#ffcdd2" stroke="#d32f2f" stroke-width="2" rx="5"/>
  <text x="100" y="205" text-anchor="middle" font-size="14" font-weight="bold">Attacker</text>

  <!-- Primary Open DNS Resolver -->
  <rect x="300" y="50" width="150" height="40" fill="#c8e6c9" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="375" y="75" text-anchor="middle" font-size="14">Open DNS Resolver</text>

  <!-- Additional Open DNS Resolvers -->
  <rect x="300" y="120" width="150" height="40" fill="#c8e6c9" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="375" y="145" text-anchor="middle" font-size="14">Open DNS Resolver</text>

  <rect x="300" y="190" width="150" height="40" fill="#c8e6c9" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="375" y="215" text-anchor="middle" font-size="14">Open DNS Resolver</text>

  <rect x="300" y="260" width="150" height="40" fill="#c8e6c9" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="375" y="285" text-anchor="middle" font-size="14">Open DNS Resolver</text>

  <!-- Victim -->
  <rect x="550" y="180" width="100" height="40" fill="#ffecb3" stroke="#f57c00" stroke-width="2" rx="5"/>
  <text x="600" y="205" text-anchor="middle" font-size="14" font-weight="bold">Victim</text>

  <!-- Arrow from Attacker to Primary DNS Resolver -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>

  <!-- Small spoofed query -->
  <path d="M 150 190 Q 225 120 300 70" stroke="#d32f2f" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
  <text x="225" y="125" text-anchor="middle" font-size="11" fill="#d32f2f">Small spoofed query</text>

  <!-- Large DNS responses from all resolvers -->
  <path d="M 450 70 Q 500 125 550 180" stroke="#ff6b6b" stroke-width="3" fill="none" marker-end="url(#arrowhead)"/>
  <text x="490" y="115" text-anchor="middle" font-size="11" fill="#ff6b6b">Large DNS response</text>

  <path d="M 450 140 Q 500 160 550 185" stroke="#ff6b6b" stroke-width="3" fill="none" marker-end="url(#arrowhead)"/>

  <path d="M 450 210 L 550 205" stroke="#ff6b6b" stroke-width="3" fill="none" marker-end="url(#arrowhead)"/>

  <path d="M 450 280 Q 500 240 550 195" stroke="#ff6b6b" stroke-width="3" fill="none" marker-end="url(#arrowhead)"/>

  <!-- Amplification indicator -->
  <text x="375" y="350" text-anchor="middle" font-size="14" font-weight="bold" fill="#d32f2f">Amplification Factor: 10x - 1000x</text>
</svg>

---
## Demo

```bash
dig . NS +trace
```

### Look at the large response
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
