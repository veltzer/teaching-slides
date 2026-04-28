---
tags:
  - networking:dns
  - security:privacy
level: intermediate
category: networking
audience:
  - audiences:sysadmins
  - audiences:network-engineers

---
# DNS over HTTPS and DNS over TLS

---
## What This Chapter Covers

- The privacy problem with traditional DNS
- DNS over TLS (DoT)
- DNS over HTTPS (DoH)
- Configuring clients and servers
- Trade-offs and enterprise concerns

---
## The Privacy Problem

- Plain DNS is unencrypted UDP
- Anyone on the network path sees queries
- ISPs log them; coffee shops can see them
- Browser history derivable from DNS alone
- Widely considered a real privacy issue

---
## What DoH and DoT Solve

- Encrypt the DNS query end-to-end
- Authenticate the resolver (TLS)
- No more passive observation by the network
- Doesn't replace DNSSEC — different layer
- Different protocols for different deployment styles

---
## DoH vs DoT Visualized

![doh_dot](svg/courses/networking/dns-deep-dive/06_doh_and_dot/doh_dot.svg)

---
## DNS over TLS (DoT)

- DNS queries inside TLS sessions
- Port 853 (well-known)
- Distinct from regular HTTPS traffic
- Easy for networks to identify and block
- Strong choice for known infrastructure

---
## DNS over HTTPS (DoH)

- DNS queries inside HTTPS POST/GET
- Port 443 — same as regular web traffic
- Indistinguishable from normal HTTPS
- Hard for networks to block
- The choice browsers have largely made

---
## DoH Wire Format

- HTTP/2 POST with `application/dns-message`
- Body is the DNS query in wire format
- Response is DNS wire format too
- Same protocol semantics over a different transport
- Caching headers can apply

---
## DoT Wire Format

- TCP connection on port 853
- TLS handshake
- DNS over the encrypted stream (with length prefix)
- Persistent connections amortize handshake
- Standard fits well into existing DNS resolvers

---
## Server Configuration: Unbound

```output
server:
    interface: 0.0.0.0@853
    tls-cert-bundle: /etc/ssl/certs/ca-bundle.crt
    tls-service-key: /etc/dns/server.key
    tls-service-pem: /etc/dns/server.pem
```

- Listen on port 853
- TLS cert and key
- Standard DoT server in a few lines

---
## Server Configuration: BIND

- More involved than Unbound
- Requires named.conf TLS configuration
- Newer versions support DoT and DoH natively
- Older versions need a TLS proxy in front
- Modern BIND is improving fast

---
## Browser DoH

- Firefox: enables Cloudflare DoH by default in some regions
- Chrome: respects the OS setting; auto-upgrades when possible
- Safari: limited; iCloud Private Relay handles DNS
- Browsers can bypass OS DNS settings — IT controversy
- Configure per browser policy if needed

---
## OS-Level DoH/DoT

- Android: built-in private DNS (DoT) for years
- iOS: configurable per profile
- Windows 11: DoH built into Windows resolver
- Linux: systemd-resolved has DoT support
- Adoption is rapid

---
## Public DoH/DoT Providers

- Cloudflare: 1.1.1.1 (DoH/DoT)
- Google: 8.8.8.8 (DoH/DoT)
- Quad9: 9.9.9.9 (DoH/DoT)
- Mullvad and others (privacy-focused)
- Most major resolvers support encrypted variants

---
## Oblivious DoH (ODoH)

- Adds a relay between client and resolver
- Resolver sees the query but not the client
- Relay sees the client but not the query
- Combined: nobody sees both
- Cloudflare and Apple support this

---
## Client Configuration: macOS

- System Settings → Network → DNS
- Or via configuration profile
- Can specify DoH/DoT per-network
- Per-app overrides via NetworkExtension
- Apple ecosystem has rich tooling

---
## Client Configuration: Linux

- systemd-resolved: `DNS=` and `DNSOverTLS=yes` in resolved.conf
- /etc/resolv.conf historically; superseded by services
- NetworkManager has its own DNS setup
- Each distro slightly different
- Container networks add complexity

---
## Enterprise Concerns

- DoH bypasses DNS-based filtering and logging
- Security teams need visibility into outbound queries
- Solution: enterprise DoH endpoint (controlled)
- Or: block public DoH and force internal resolver
- Policy decision; trade-offs all around

---
## Blocking Public DoH

- Block known public DoH IP ranges (Cloudflare, Google)
- Force traffic to enterprise DoH endpoint
- Browser policies for managed devices
- Doesn't catch all paths; partial control
- Becoming harder as adoption rises

---
## Performance: DoH vs Plain DNS

- TLS handshake adds latency on first connection
- Persistent connections amortize this
- HTTP/2 multiplexing can pipeline queries
- Cached responses are fast either way
- Real-world: typically negligible for users

---
## Performance: DoT vs DoH

- DoT: simpler protocol, slightly faster
- DoH: harder to block, larger overhead
- Difference is often noise
- Pick based on deployment, not microseconds
- Both vastly faster than the latency they hide

---
## Privacy Threats DoH/DoT Don't Solve

- The resolver still sees your queries
- ECS may leak prefix info to authoritative servers
- TLS metadata (SNI, certificate, timing)
- Logging by the encrypted resolver
- Pick a resolver you trust; don't assume

---
## DoH/DoT vs VPN

- VPN encrypts everything; DoH/DoT only DNS
- Different threat models
- DoH/DoT cheaper, less performance impact
- VPN moves trust to the VPN provider
- Combine for layered defense

---
## Common Pitfalls

- Plaintext fallback allowed silently — defeats purpose
- Configuration done at OS but apps bypass
- Resolver running encrypted but logs plaintext locally
- Forgetting that DNSSEC and DoH/DoT solve different things
- Assuming all "encrypted DNS" means the same thing

---
## Best Practices

- Configure both DoH and DoT where possible
- Use a resolver with a no-logging policy you trust
- Combine with DNSSEC for full protection
- Audit periodically — new DNS bypasses appear
- Document and educate team about DoH/DoT

---
## The Future

- DoH/DoT becoming default in most stacks
- Encrypted ClientHello (ECH) extends to TLS metadata
- Oblivious DNS continues to develop
- Enterprise tooling catching up
- Plain DNS will look anachronistic in a few years

---
## Summary

- DoT and DoH encrypt DNS in transit
- DoT on port 853; DoH inside HTTPS
- Browsers and OSes adopting fast
- Pick a trusted resolver; logs still possible there
- Combine with DNSSEC; they solve different problems
