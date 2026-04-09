# DNS Denial of Service

## DNS (Domain Name System) is a critical component of the internet, responsible for translating human-readable domain names into IP addresses. However, this essential service is vulnerable to various types of attacks, including Denial of Service (DoS) attacks
---
## What is a DNS DoS Attack

### A DNS DoS attack is a type of cyber-attack that aims to disrupt or overwhelm the DNS servers, making them unavailable to legitimate users and clients. The attack typically involves flooding the DNS servers with a massive amount of bogus requests, consuming all available resources and preventing the server from responding to genuine requests
---
## Types of DNS DoS Attacks

1. **UDP Flood Attack**: This attack involves sending a large number of UDP packets to the DNS server, overwhelming its ability to process legitimate requests.
1. **DNS Query Flood Attack**: In this attack, the attacker sends an excessive number of DNS queries to the server, overwhelming its ability to handle the requests.
1. **Random Subdomain Attack**: The attacker generates and sends a huge number of DNS requests for non-existent subdomains, causing the DNS server to waste resources resolving these invalid queries.
1. **NXDOMAIN Flood Attack**: This attack exploits the caching mechanism of DNS servers by sending numerous requests for non-existent domains, causing the server to cache negative responses and consume resources.

---

## Impacts of DNS DoS Attacks

- **Service Disruption**: A successful DNS DoS attack can render the targeted DNS server unavailable, preventing users from accessing websites and online services that rely on the affected domain names.

- **Network Congestion**: The flood of malicious traffic can congest the network, impacting other services and applications that share the same infrastructure.

- **Revenue Loss**: For businesses that rely on online services, a DNS DoS attack can lead to significant revenue loss due to service disruption and customer dissatisfaction.

- **Reputational Damage**: High-profile DNS DoS attacks can damage the reputation of the targeted organization and erode customer trust.

---

## Mitigating DNS DoS Attacks
1. **Implement Rate Limiting**: Configure DNS servers to limit the number of requests accepted from a single source within a specific time frame.
1. **Use Anycast DNS**: Distribute the DNS service across multiple networks and servers, making it more resilient to localized attacks.
1. **Leverage Cloud-based DNS Services**: Utilize cloud-based DNS services that offer robust DDoS mitigation capabilities and global load balancing.
1. **Implement DNS Response Rate Limiting (RRL)**: Limit the rate at which a DNS server responds to queries from a specific IP address or network.
1. **Keep DNS Software Up-to-Date**: Regularly update the DNS software and apply security patches to mitigate known vulnerabilities
---

## DNS DoS Attack Flow

![dns_dos_attack_flow](svg/courses/security/cyber-attacks-and-vectors/09_dns_denial_of_service/dns_dos_attack_flow.svg)

---

## Random Subdomain Attack (Water Torture)

![random_subdomain_attack_water_torture](svg/courses/security/cyber-attacks-and-vectors/09_dns_denial_of_service/random_subdomain_attack_water_torture.svg)

---

## Detecting DNS DoS Attacks

```bash
# Monitor DNS query rates
# Using tcpdump to count queries per second
tcpdump -i eth0 -n 'udp dst port 53' -c 10000 2>/dev/null | \
    awk '{print $1}' | cut -d. -f1-3 | sort | uniq -c | sort -rn

# Check BIND query statistics
rndc stats
cat /var/named/data/named_stats.txt | grep "queries"

# Monitor NXDOMAIN response rate (high = possible attack)
tcpdump -i eth0 -n 'udp src port 53' | grep "NXDomain" | \
    awk '{print $1}' | cut -d. -f1 | uniq -c

# Using dnstop for real-time DNS monitoring
dnstop eth0

# Check for query patterns (same domain, random subdomains)
tcpdump -i eth0 -n 'udp dst port 53' -c 1000 | \
    grep -oP '[a-z0-9]+\.example\.com' | sort | uniq -c | sort -rn
```

---

## Response Rate Limiting (RRL) Configuration

```bash
# BIND named.conf - RRL configuration
rate-limit {
    responses-per-second 5;    # Max responses per client
    window 15;                  # Tracking window in seconds
    nxdomains-per-second 3;    # NXDOMAIN rate limit
    errors-per-second 5;       # Error response limit
    slip 2;                    # Send every Nth response
    log-only no;               # Actually enforce limits
};

# Unbound configuration
server:
    ratelimit: 1000            # Queries per second limit
    ip-ratelimit: 100          # Per-IP rate limit
    ratelimit-slabs: 4
    ratelimit-size: 4m
```

---

## Real-World DNS DoS Incidents

| Incident          | Year | Impact                                        |
|-------------------|------|-----------------------------------------------|
| Dyn DNS Attack    | 2016 | Twitter, Reddit, Netflix, GitHub down          |
| Spamhaus Attack   | 2013 | 300 Gbps, slowed European internet             |
| NS1 Attack        | 2016 | Major DNS provider targeted                    |
| AWS Route 53      | 2019 | 8-hour DDoS affecting AWS customers            |

The 2016 Dyn attack used the Mirai botnet (IoT devices) to generate massive DNS query floods.

---

## Anycast DNS Architecture

![anycast_dns_architecture](svg/courses/security/cyber-attacks-and-vectors/09_dns_denial_of_service/anycast_dns_architecture.svg)

---

## Exercise: DNS DoS Mitigation Lab

1. Set up a BIND DNS server in a test environment
1. Configure logging to track query rates and types
1. Generate simulated DNS query flood traffic using `dnsperf`
1. Observe server behavior under load (CPU, memory, response time)
1. Implement Rate Limiting (RRL) and repeat the test
1. Compare server performance with and without RRL
1. Set up monitoring dashboards for DNS metrics (Grafana + Prometheus)

```bash
# Using dnsperf for DNS load testing
# (only on YOUR OWN test systems)
dnsperf -s 127.0.0.1 -d queryfile.txt -c 100 -Q 10000
# -s: target server
# -d: file with domain names to query
# -c: concurrent queries
# -Q: queries per second limit
```

## Conclusion

DNS DoS attacks can have severe consequences for businesses and organizations that rely on online services. By understanding the different types of attacks and implementing appropriate mitigation strategies, organizations can enhance the resilience and availability of their DNS infrastructure, ensuring uninterrupted access to their online services.
