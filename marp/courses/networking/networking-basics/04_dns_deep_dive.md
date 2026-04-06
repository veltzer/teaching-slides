# DNS Deep Dive
## Understanding the Domain Name System

---

## What is DNS?

- Domain Name System: the "phonebook" of the internet
- Translates human-readable domain names to IP addresses
- Distributed, hierarchical database system
- Critical infrastructure -- without DNS, the internet is nearly unusable
- Defined in RFC 1034 and RFC 1035 (1987), with many subsequent updates

```misc
User types:    www.example.com
DNS resolves:  www.example.com → 93.184.216.34
Browser uses:  93.184.216.34 to establish TCP connection
```

---

## The DNS Hierarchy

DNS is organized as an inverted tree structure with the root at the top.

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="310" font-family="sans-serif">
  <!-- DNS Hierarchy Tree -->
  <!-- Root -->
  <text x="330" y="26" font-size="14" fill="#222" text-anchor="middle" font-weight="bold">. (Root)</text>
  <!-- Root → TLDs -->
  <line x1="330" y1="30" x2="95"  y2="85" stroke="#555" stroke-width="1.5"/>
  <line x1="330" y1="30" x2="195" y2="85" stroke="#555" stroke-width="1.5"/>
  <line x1="330" y1="30" x2="295" y2="85" stroke="#555" stroke-width="1.5"/>
  <line x1="330" y1="30" x2="430" y2="85" stroke="#555" stroke-width="1.5"/>
  <line x1="330" y1="30" x2="520" y2="85" stroke="#555" stroke-width="1.5"/>
  <line x1="330" y1="30" x2="605" y2="85" stroke="#555" stroke-width="1.5"/>
  <!-- TLD labels -->
  <text x="95"  y="98" font-size="13" fill="#222" text-anchor="middle">.com</text>
  <text x="195" y="98" font-size="13" fill="#222" text-anchor="middle">.org</text>
  <text x="295" y="98" font-size="13" fill="#222" text-anchor="middle">.net</text>
  <text x="430" y="98" font-size="13" fill="#222" text-anchor="middle">.uk</text>
  <text x="520" y="98" font-size="13" fill="#222" text-anchor="middle">.de</text>
  <text x="605" y="98" font-size="13" fill="#222" text-anchor="middle">...</text>
  <!-- .com → second level -->
  <line x1="95" y1="102" x2="45"  y2="175" stroke="#555" stroke-width="1.5"/>
  <line x1="95" y1="102" x2="130" y2="175" stroke="#555" stroke-width="1.5"/>
  <line x1="95" y1="102" x2="215" y2="175" stroke="#555" stroke-width="1.5"/>
  <!-- .uk → bbc -->
  <line x1="430" y1="102" x2="430" y2="175" stroke="#555" stroke-width="1.5"/>
  <!-- Second level labels -->
  <text x="45"  y="188" font-size="13" fill="#222" text-anchor="middle">google</text>
  <text x="130" y="188" font-size="13" fill="#222" text-anchor="middle">amazon</text>
  <text x="215" y="188" font-size="13" fill="#222" text-anchor="middle">example</text>
  <text x="430" y="188" font-size="13" fill="#222" text-anchor="middle">bbc</text>
  <!-- google → www, mail -->
  <line x1="45" y1="192" x2="22"  y2="262" stroke="#555" stroke-width="1.5"/>
  <line x1="45" y1="192" x2="80"  y2="262" stroke="#555" stroke-width="1.5"/>
  <!-- amazon → www -->
  <line x1="130" y1="192" x2="138" y2="262" stroke="#555" stroke-width="1.5"/>
  <!-- bbc → www -->
  <line x1="430" y1="192" x2="430" y2="262" stroke="#555" stroke-width="1.5"/>
  <!-- Third level labels -->
  <text x="22"  y="276" font-size="13" fill="#222" text-anchor="middle">www</text>
  <text x="80"  y="276" font-size="13" fill="#222" text-anchor="middle">mail</text>
  <text x="138" y="276" font-size="13" fill="#222" text-anchor="middle">www</text>
  <text x="430" y="276" font-size="13" fill="#222" text-anchor="middle">www</text>
</svg>

Each level is called a "zone" and is managed by different organizations:
- **Root zone**: managed by ICANN, served by 13 root server clusters (a.root-servers.net through m.root-servers.net)
- **TLD zone**: managed by registries (.com by Verisign, .org by PIR, ccTLDs by country organizations)
- **Second-level domains**: managed by domain owners (you!)

---

## DNS Root Servers

There are 13 logical root server addresses (A through M), but hundreds of physical servers worldwide using anycast routing.

| Letter | Operator | Locations |
|--------|----------|-----------|
| A | Verisign | Distributed |
| B | USC-ISI | Los Angeles |
| C | Cogent | Distributed |
| D | University of Maryland | College Park |
| E | NASA Ames | Mountain View |
| F | ISC | Distributed (100+) |
| J | Verisign | Distributed (100+) |
| K | RIPE NCC | Distributed |
| L | ICANN | Distributed |
| M | WIDE Project | Distributed |

```bash
# Query a root server directly
dig @a.root-servers.net . NS

# See all root server IPs
dig . NS +short
```

---

## DNS Record Types Overview

DNS stores various types of records, each serving a different purpose.

| Record Type | Purpose | Example |
|-------------|---------|---------|
| A | IPv4 address | example.com → 93.184.216.34 |
| AAAA | IPv6 address | example.com → 2606:2800:220:1:... |
| CNAME | Canonical name (alias) | www.example.com → example.com |
| MX | Mail exchange | example.com → mail.example.com |
| TXT | Text data | SPF, DKIM, domain verification |
| NS | Name server | example.com → ns1.example.com |
| SOA | Start of authority | Zone metadata |
| PTR | Reverse DNS | IP → domain name |
| SRV | Service locator | _sip._tcp.example.com |

---

## A and AAAA Records

The most fundamental DNS records -- they map domain names to IP addresses.

**A Record** (IPv4):
```bash
$ dig example.com A +short
93.184.216.34

$ dig example.com A

;; ANSWER SECTION:
example.com.        3600    IN    A    93.184.216.34
```

**AAAA Record** (IPv6):
```bash
$ dig example.com AAAA +short
2606:2800:220:1:248:1893:25c8:1946

$ dig example.com AAAA

;; ANSWER SECTION:
example.com.        3600    IN    AAAA    2606:2800:220:1:248:1893:25c8:1946
```

A domain can have multiple A records for load balancing (round-robin DNS):
```bash
$ dig google.com A +short
142.250.80.46
142.250.80.78
142.250.80.110
```

---

## CNAME Records

CNAME (Canonical Name) creates an alias from one domain name to another.

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="130" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#555"/>
    </marker>
  </defs>
  <!-- Box 1 -->
  <rect x="10" y="30" width="170" height="60" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="95" y="56" font-size="13" fill="#222" text-anchor="middle">www.example.com</text>
  <text x="95" y="74" font-size="12" fill="#555" text-anchor="middle">(alias)</text>
  <!-- Arrow 1 with label -->
  <line x1="180" y1="60" x2="228" y2="60" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="204" y="52" font-size="11" fill="#555" text-anchor="middle">CNAME</text>
  <!-- Box 2 -->
  <rect x="230" y="30" width="170" height="60" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="315" y="56" font-size="13" fill="#222" text-anchor="middle">example.com</text>
  <text x="315" y="74" font-size="12" fill="#555" text-anchor="middle">(canonical)</text>
  <!-- Arrow 2 with label -->
  <line x1="400" y1="60" x2="448" y2="60" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="424" y="52" font-size="11" fill="#555" text-anchor="middle">A</text>
  <!-- Box 3 -->
  <rect x="450" y="30" width="170" height="60" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="535" y="56" font-size="13" fill="#222" text-anchor="middle">93.184.216.34</text>
  <text x="535" y="74" font-size="12" fill="#555" text-anchor="middle">(IP address)</text>
</svg>

```bash
$ dig www.example.com

;; ANSWER SECTION:
www.example.com.    3600    IN    CNAME   example.com.
example.com.        3600    IN    A       93.184.216.34
```

**Important CNAME rules:**
- A CNAME cannot coexist with other record types for the same name
- A CNAME cannot be at the zone apex (e.g., example.com itself)
- Some providers offer "ALIAS" or "ANAME" as a workaround for apex CNAMEs

---

## MX Records

MX (Mail Exchange) records direct email for a domain to the correct mail servers.

```bash
$ dig example.com MX

;; ANSWER SECTION:
example.com.    3600    IN    MX    10 mail1.example.com.
example.com.    3600    IN    MX    20 mail2.example.com.
example.com.    3600    IN    MX    30 mail3.example.com.
```

The number before the server name is the **priority** (lower = higher priority).

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="200" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#555"/>
    </marker>
  </defs>
  <!-- Sending MTA box -->
  <rect x="10" y="10" width="140" height="44" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="80" y="37" font-size="13" fill="#222" text-anchor="middle">Sending MTA</text>
  <!-- Arrow down -->
  <line x1="80" y1="54" x2="80" y2="108" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="95" y="86" font-size="12" fill="#555">Query MX for example.com</text>
  <!-- DNS Server box -->
  <rect x="10" y="110" width="140" height="44" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="80" y="137" font-size="13" fill="#222" text-anchor="middle">DNS Server</text>
  <!-- Arrow right -->
  <line x1="150" y1="132" x2="198" y2="132" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Priority list -->
  <text x="205" y="118" font-size="13" fill="#222">Priority 10 → mail1.example.com  (try first)</text>
  <text x="205" y="137" font-size="13" fill="#222">Priority 20 → mail2.example.com  (fallback)</text>
  <text x="205" y="156" font-size="13" fill="#222">Priority 30 → mail3.example.com  (last resort)</text>
</svg>

If mail1 is unreachable, the sender automatically tries mail2, then mail3.

---

## TXT Records

TXT records hold arbitrary text data. Widely used for domain verification and email security.

**Common uses:**

1. **SPF** (Sender Policy Framework) -- specifies which servers can send email for your domain:
```bash
$ dig example.com TXT +short
"v=spf1 include:_spf.google.com ~all"
```

1. **DKIM** (DomainKeys Identified Mail) -- email authentication via cryptographic signatures:
```bash
$ dig google._domainkey.example.com TXT +short
"v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA..."
```

1. **DMARC** -- policy for handling email that fails SPF/DKIM:
```bash
$ dig _dmarc.example.com TXT +short
"v=DMARC1; p=reject; rua=mailto:dmarc@example.com"
```

1. **Domain verification** (Google, Microsoft, Let's Encrypt):
```bash
$ dig example.com TXT +short
"google-site-verification=abc123..."
```

---

## NS Records

NS (Name Server) records delegate a DNS zone to specific authoritative name servers.

```bash
$ dig example.com NS

;; ANSWER SECTION:
example.com.    86400    IN    NS    a.iana-servers.net.
example.com.    86400    IN    NS    b.iana-servers.net.
```

NS records form the delegation chain from root to your domain:

<svg xmlns="http://www.w3.org/2000/svg" width="560" height="360" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#555"/>
    </marker>
  </defs>
  <!-- Node 1: Root -->
  <rect x="10" y="10" width="120" height="40" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="70" y="35" font-size="13" fill="#222" text-anchor="middle">Root (.)</text>
  <text x="150" y="35" font-size="12" fill="#555">"Who handles .com?"</text>
  <!-- Arrow -->
  <line x1="70" y1="50" x2="70" y2="98" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Node 2: .com NS servers -->
  <rect x="10" y="100" width="120" height="40" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="70" y="125" font-size="13" fill="#222" text-anchor="middle">.com NS servers</text>
  <text x="150" y="125" font-size="12" fill="#555">"Who handles example.com?"</text>
  <!-- Arrow -->
  <line x1="70" y1="140" x2="70" y2="188" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Node 3: example.com NS -->
  <rect x="10" y="190" width="120" height="40" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="70" y="215" font-size="13" fill="#222" text-anchor="middle">example.com NS</text>
  <text x="150" y="208" font-size="12" fill="#555">"I am authoritative for example.com"</text>
  <text x="150" y="225" font-size="12" fill="#555">Here are the records you requested.</text>
  <!-- Arrow -->
  <line x1="70" y1="230" x2="70" y2="278" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Node 4: iana servers -->
  <rect x="10" y="280" width="120" height="60" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="70" y="306" font-size="12" fill="#222" text-anchor="middle">a.iana-servers.net</text>
  <text x="70" y="326" font-size="12" fill="#222" text-anchor="middle">b.iana-servers.net</text>
</svg>

---

## SOA Record

SOA (Start of Authority) contains administrative information about a DNS zone.

```bash
$ dig example.com SOA

;; ANSWER SECTION:
example.com.  3600  IN  SOA  ns1.example.com. admin.example.com. (
                            2024010101  ; Serial number
                            7200        ; Refresh (2 hours)
                            3600        ; Retry (1 hour)
                            1209600     ; Expire (14 days)
                            86400       ; Minimum TTL (1 day)
                            )
```

| Field | Meaning |
|-------|---------|
| ns1.example.com. | Primary name server |
| admin.example.com. | Admin email (@ replaced with .) |
| Serial | Zone version (often YYYYMMDDNN format) |
| Refresh | How often secondaries check for updates |
| Retry | Retry interval if refresh fails |
| Expire | When secondaries stop serving if primary unreachable |
| Minimum TTL | Default TTL for negative caching |

---

## PTR Records (Reverse DNS)

PTR records map IP addresses back to domain names. Used for reverse DNS lookups.

IPv4 reverse lookups use the special domain `in-addr.arpa` with octets reversed:

```bash
# Forward lookup
$ dig example.com A +short
93.184.216.34

# Reverse lookup (note reversed octets)
$ dig -x 93.184.216.34
;; ANSWER SECTION:
34.216.184.93.in-addr.arpa. 3600 IN PTR example.com.

# Shorthand using -x flag
$ dig -x 8.8.8.8 +short
dns.google.
```

**Why reverse DNS matters:**
- Email servers check PTR records to verify sending servers (anti-spam)
- Logging and monitoring tools resolve IPs to names for readability
- Some services reject connections from IPs without valid PTR records

---

## SRV Records

SRV (Service) records specify the location of services, including port numbers.

Format: `_service._protocol.name TTL IN SRV priority weight port target`

```bash
$ dig _sip._tcp.example.com SRV

;; ANSWER SECTION:
_sip._tcp.example.com. 3600 IN SRV 10 60 5060 sip1.example.com.
_sip._tcp.example.com. 3600 IN SRV 10 40 5060 sip2.example.com.
_sip._tcp.example.com. 3600 IN SRV 20 0  5060 sip3.example.com.
```

| Field | Meaning |
|-------|---------|
| Priority | Lower = preferred (like MX) |
| Weight | Load balancing among same-priority targets |
| Port | TCP/UDP port for the service |
| Target | Hostname providing the service |

**Common SRV uses:**
- SIP (VoIP): `_sip._tcp`
- XMPP (chat): `_xmpp-client._tcp`
- LDAP: `_ldap._tcp`
- Kubernetes service discovery

---

## Recursive vs Iterative Resolution

DNS resolution can happen in two modes:

**Recursive Resolution** -- the resolver does all the work:

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="220" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="8" markerHeight="6" refX="0" refY="3" orient="auto">
      <polygon points="8 0, 0 3, 8 6" fill="#555"/>
    </marker>
  </defs>
  <!-- Box 1: Client -->
  <rect x="5" y="20" width="80" height="60" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="45" y="47" font-size="12" fill="#222" text-anchor="middle">Client</text>
  <!-- Box 2: Recursive Resolver -->
  <rect x="110" y="20" width="130" height="60" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="175" y="44" font-size="12" fill="#222" text-anchor="middle">Recursive</text>
  <text x="175" y="60" font-size="12" fill="#222" text-anchor="middle">Resolver</text>
  <text x="175" y="76" font-size="10" fill="#555" text-anchor="middle">(ISP/8.8.8.8)</text>
  <!-- Box 3: Root -->
  <rect x="270" y="20" width="70" height="60" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="305" y="54" font-size="12" fill="#222" text-anchor="middle">Root</text>
  <!-- Box 4: .com NS -->
  <rect x="365" y="20" width="70" height="60" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="400" y="47" font-size="12" fill="#222" text-anchor="middle">.com</text>
  <text x="400" y="63" font-size="12" fill="#222" text-anchor="middle">NS</text>
  <!-- Box 5: Authoritative NS -->
  <rect x="460" y="20" width="110" height="60" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="515" y="44" font-size="12" fill="#222" text-anchor="middle">Authoritative</text>
  <text x="515" y="60" font-size="12" fill="#222" text-anchor="middle">NS</text>
  <!-- Forward arrows (top) -->
  <line x1="85"  y1="38" x2="108" y2="38" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="240" y1="38" x2="268" y2="38" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="340" y1="38" x2="363" y2="38" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="435" y1="38" x2="458" y2="38" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Return arrows (bottom) -->
  <line x1="108" y1="62" x2="85"  y2="62" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="268" y1="62" x2="240" y2="62" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="363" y1="62" x2="340" y2="62" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="458" y1="62" x2="435" y2="62" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Labels below -->
  <text x="45"  y="110" font-size="11" fill="#555" text-anchor="middle">Single</text>
  <text x="45"  y="124" font-size="11" fill="#555" text-anchor="middle">query</text>
  <text x="175" y="110" font-size="11" fill="#555" text-anchor="middle">Does all</text>
  <text x="175" y="124" font-size="11" fill="#555" text-anchor="middle">the work</text>
  <text x="430" y="110" font-size="11" fill="#555" text-anchor="middle">Iterative queries to each level</text>
</svg>

**Iterative Resolution** -- each server returns the next server to ask:

```misc
Client asks Root:    "Where is www.example.com?"
Root responds:       "I don't know, but ask .com NS at 192.5.6.30"

Client asks .com:    "Where is www.example.com?"
.com responds:       "I don't know, but ask example.com NS at 93.184.216.34"

Client asks example.com NS: "Where is www.example.com?"
example.com responds:       "Here: 93.184.216.34"
```

In practice, your computer uses recursive resolution (asking your configured DNS resolver), and the resolver uses iterative resolution to walk the hierarchy.

---

## DNS Resolution: Step by Step

What happens when you type `www.example.com` in your browser:

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="350" font-family="sans-serif">
  <rect x="5" y="5" width="630" height="340" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="20" y="32" font-size="13" fill="#222">Step 1:  Browser checks its own DNS cache</text>
  <text x="20" y="56" font-size="13" fill="#222">Step 2:  OS checks /etc/hosts file</text>
  <text x="20" y="80" font-size="13" fill="#222">Step 3:  OS checks its DNS cache (systemd-resolved, nscd)</text>
  <text x="20" y="104" font-size="13" fill="#222">Step 4:  Query sent to configured recursive resolver</text>
  <text x="20" y="128" font-size="13" fill="#222">Step 5:  Resolver checks its cache</text>
  <text x="20" y="152" font-size="13" fill="#222">Step 6:  If not cached, resolver walks the DNS hierarchy:</text>
  <text x="44" y="174" font-size="13" fill="#555">6a:  Query root server → get .com NS</text>
  <text x="44" y="196" font-size="13" fill="#555">6b:  Query .com NS → get example.com NS</text>
  <text x="44" y="218" font-size="13" fill="#555">6c:  Query example.com NS → get A record</text>
  <text x="20" y="242" font-size="13" fill="#222">Step 7:  Resolver caches the result and returns it</text>
  <text x="20" y="266" font-size="13" fill="#222">Step 8:  OS caches the result</text>
  <text x="20" y="290" font-size="13" fill="#222">Step 9:  Browser caches the result</text>
  <text x="20" y="314" font-size="13" fill="#222">Step 10: Browser uses IP to establish TCP connection</text>
</svg>

```bash
# Trace the full resolution path
$ dig +trace www.example.com

; <<>> DiG 9.18.1 <<>> +trace www.example.com
;; global options: +cmd
.                       518400  IN      NS      a.root-servers.net.
com.                    172800  IN      NS      a.gtld-servers.net.
example.com.            172800  IN      NS      a.iana-servers.net.
www.example.com.        86400   IN      A       93.184.216.34
```

---

## DNS Caching and TTL

Every DNS record has a TTL (Time To Live) that controls how long it can be cached.

```bash
$ dig example.com A

;; ANSWER SECTION:
example.com.        3600    IN    A    93.184.216.34
                    ^^^^
                    TTL = 3600 seconds (1 hour)
```

**TTL trade-offs:**

| Short TTL (60-300s) | Long TTL (3600-86400s) |
|---------------------|------------------------|
| Quick DNS changes propagate fast | Reduced DNS query load |
| Higher DNS query volume | Faster resolution (cached) |
| Good for failover scenarios | Changes take longer to propagate |
| Useful before migrations | Better for stable services |

**Caching layers:**
1. Browser cache (Chrome: `chrome://net-internals/#dns`)
2. OS cache (`systemd-resolved`, `nscd`, Windows DNS Client)
3. Recursive resolver cache (ISP, 8.8.8.8, 1.1.1.1)

```bash
# View systemd-resolved cache statistics
$ resolvectl statistics

# Flush DNS cache on Linux (systemd)
$ sudo resolvectl flush-caches

# Flush DNS cache on macOS
$ sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder

# Flush DNS cache on Windows
> ipconfig /flushdns
```

---

## Negative Caching

DNS also caches negative results -- when a domain does not exist.

```bash
$ dig nonexistent.example.com A

;; AUTHORITY SECTION:
example.com.  86400  IN  SOA  ns1.example.com. admin.example.com. (
                            ...
                            86400  ; Minimum TTL ← used for negative caching
                            )

;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN
```

The SOA minimum TTL field determines how long the "does not exist" (NXDOMAIN) response is cached. This prevents repeated queries for non-existent domains.

---

## Configuring DNS on Linux

### /etc/resolv.conf

The primary DNS configuration file on Linux:

```bash
$ cat /etc/resolv.conf

# DNS resolver configuration
nameserver 8.8.8.8          # Primary DNS server (Google)
nameserver 8.8.4.4          # Secondary DNS server
nameserver 1.1.1.1          # Tertiary DNS server (Cloudflare)
search example.com corp.example.com  # Search domains
options timeout:2 attempts:3 rotate  # Options
```

| Directive | Purpose |
|-----------|---------|
| nameserver | IP of DNS resolver (max 3) |
| search | Domains appended to short hostnames |
| domain | Default search domain (alternative to search) |
| options timeout:N | Query timeout in seconds |
| options attempts:N | Number of retries |
| options rotate | Round-robin among nameservers |

### /etc/nsswitch.conf

Controls the order of name resolution:
```bash
$ grep hosts /etc/nsswitch.conf
hosts: files dns mymachines myhostname
#      ^     ^
#      |     └── Use DNS (/etc/resolv.conf)
#      └── Check /etc/hosts first
```

---

## systemd-resolved

Modern Linux distributions often use systemd-resolved as a local DNS stub resolver.

```bash
# Check resolved status
$ resolvectl status
Global
       Protocols: +LLMNR +mDNS -DNSOverTLS DNSSEC=no/unsupported
resolv.conf mode: stub

Link 2 (eth0)
    Current Scopes: DNS LLMNR/IPv4 LLMNR/IPv6
         Protocols: +DefaultRoute +LLMNR -mDNS -DNSOverTLS
Current DNS Server: 8.8.8.8
       DNS Servers: 8.8.8.8 8.8.4.4

# Query using resolvectl
$ resolvectl query example.com
example.com: 93.184.216.34
             2606:2800:220:1:248:1893:25c8:1946

# View cache statistics
$ resolvectl statistics
DNSSEC supported by current servers: no
Transactions
  Current:        0
  Total:       1234
Cache
  Current Size: 89
  Hits:        567
  Misses:      667
```

When systemd-resolved is active, `/etc/resolv.conf` typically points to `127.0.0.53`.

---

## Practical DNS Tools: dig

`dig` (Domain Information Groper) is the most powerful DNS query tool.

```bash
# Basic query
$ dig example.com

# Query specific record type
$ dig example.com MX
$ dig example.com AAAA
$ dig example.com TXT

# Short output
$ dig example.com +short
93.184.216.34

# Query a specific DNS server
$ dig @8.8.8.8 example.com
$ dig @1.1.1.1 example.com

# Trace full resolution path
$ dig +trace example.com

# Show only answer section
$ dig example.com +noall +answer

# Reverse DNS lookup
$ dig -x 8.8.8.8

# Query with TCP instead of UDP
$ dig +tcp example.com

# Check DNSSEC
$ dig example.com +dnssec

# Batch queries from file
$ dig -f domains.txt +short
```

---

## Practical DNS Tools: nslookup and host

### nslookup (older, interactive tool)

```bash
# Simple lookup
$ nslookup example.com
Server:    8.8.8.8
Address:   8.8.8.8#53

Non-authoritative answer:
Name:    example.com
Address: 93.184.216.34

# Query specific record type
$ nslookup -type=MX example.com

# Use a specific DNS server
$ nslookup example.com 1.1.1.1

# Interactive mode
$ nslookup
> set type=AAAA
> example.com
> exit
```

### host (simple, scriptable)

```bash
# Simple lookup
$ host example.com
example.com has address 93.184.216.34
example.com has IPv6 address 2606:2800:220:1:248:1893:25c8:1946
example.com mail is handled by 0 .

# Reverse lookup
$ host 8.8.8.8
8.8.8.8.in-addr.arpa domain name pointer dns.google.

# Specific record type
$ host -t MX example.com
$ host -t NS example.com
```

---

## DNSSEC: Securing DNS

DNSSEC (DNS Security Extensions) adds cryptographic signatures to DNS records to prevent tampering.

**The problem DNSSEC solves:**

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="420" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#555"/>
    </marker>
  </defs>
  <!-- ── Without DNSSEC ── -->
  <text x="10" y="22" font-size="14" fill="#c62828" font-weight="bold">Without DNSSEC:</text>
  <!-- Client -->
  <rect x="10" y="34" width="90" height="50" rx="4" fill="#ffebee" stroke="#333" stroke-width="1.5"/>
  <text x="55" y="64" font-size="13" fill="#222" text-anchor="middle">Client</text>
  <!-- Resolver -->
  <rect x="220" y="34" width="100" height="50" rx="4" fill="#ffebee" stroke="#333" stroke-width="1.5"/>
  <text x="270" y="64" font-size="13" fill="#222" text-anchor="middle">Resolver</text>
  <!-- NS -->
  <rect x="440" y="34" width="90" height="50" rx="4" fill="#ffebee" stroke="#333" stroke-width="1.5"/>
  <text x="485" y="64" font-size="13" fill="#222" text-anchor="middle">NS</text>
  <!-- Client→Resolver (query) -->
  <line x1="100" y1="50" x2="218" y2="50" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="160" y="45" font-size="11" fill="#555" text-anchor="middle">Query</text>
  <!-- NS→Resolver (response) -->
  <line x1="440" y1="50" x2="322" y2="50" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="380" y="45" font-size="11" fill="#555" text-anchor="middle">Response</text>
  <!-- Resolver→Client (response) -->
  <line x1="220" y1="74" x2="102" y2="74" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="162" y="90" font-size="11" fill="#555" text-anchor="middle">Response</text>
  <!-- Warning note -->
  <rect x="190" y="105" width="200" height="44" rx="4" fill="#fff9c4" stroke="#f9a825" stroke-width="1.5"/>
  <text x="290" y="124" font-size="12" fill="#b71c1c" text-anchor="middle">⚠ Attacker can forge</text>
  <text x="290" y="140" font-size="12" fill="#b71c1c" text-anchor="middle">responses (DNS spoofing)</text>
  <line x1="270" y1="84" x2="270" y2="104" stroke="#f9a825" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- ── With DNSSEC ── -->
  <text x="10" y="186" font-size="14" fill="#1b5e20" font-weight="bold">With DNSSEC:</text>
  <!-- Client -->
  <rect x="10" y="198" width="90" height="50" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="55" y="228" font-size="13" fill="#222" text-anchor="middle">Client</text>
  <!-- Resolver -->
  <rect x="200" y="198" width="130" height="60" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="265" y="222" font-size="13" fill="#222" text-anchor="middle">Resolver</text>
  <text x="265" y="240" font-size="11" fill="#1b5e20" text-anchor="middle">Validates signature</text>
  <!-- NS -->
  <rect x="450" y="198" width="100" height="60" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="500" y="222" font-size="13" fill="#222" text-anchor="middle">NS</text>
  <text x="500" y="240" font-size="11" fill="#1b5e20" text-anchor="middle">Signs records</text>
  <!-- Client→Resolver (query) -->
  <line x1="100" y1="214" x2="198" y2="214" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="149" y="209" font-size="11" fill="#555" text-anchor="middle">Query</text>
  <!-- NS→Resolver (signed response) -->
  <line x1="450" y1="214" x2="332" y2="214" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="390" y="209" font-size="11" fill="#555" text-anchor="middle">Signed Response</text>
  <!-- Resolver→Client -->
  <line x1="200" y1="244" x2="102" y2="244" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="151" y="262" font-size="11" fill="#1b5e20" text-anchor="middle">Verified Response</text>
</svg>

**DNSSEC record types:**
- **RRSIG**: Contains the signature for a record set
- **DNSKEY**: Contains the public key used to verify signatures
- **DS**: Delegation Signer -- links parent zone to child zone keys
- **NSEC/NSEC3**: Proves a record does not exist (authenticated denial)

```bash
# Check if a domain uses DNSSEC
$ dig example.com +dnssec +short
93.184.216.34
A 13 2 86400 20240201000000 20240115000000 12345 example.com. <signature>

# Validate DNSSEC chain
$ dig +sigchase +trusted-key=/etc/trusted-key.key example.com
```

---

## DNS over HTTPS (DoH) and DNS over TLS (DoT)

Traditional DNS queries are sent in plaintext over UDP port 53, allowing eavesdropping. DoH and DoT encrypt DNS queries.

| Feature | Traditional DNS | DNS over TLS (DoT) | DNS over HTTPS (DoH) |
|---------|----------------|--------------------|-----------------------|
| Port | 53 (UDP/TCP) | 853 (TCP) | 443 (TCP) |
| Encryption | None | TLS | HTTPS (TLS) |
| Privacy | Low | High | High |
| Blockable | Easily | Moderate | Hard (same as HTTPS) |
| Standard | RFC 1035 | RFC 7858 | RFC 8484 |

**Popular DoH/DoT providers:**

| Provider | DoH URL | DoT Server |
|----------|---------|------------|
| Google | https://dns.google/dns-query | dns.google |
| Cloudflare | https://cloudflare-dns.com/dns-query | 1dot1dot1dot1.cloudflare-dns.com |
| Quad9 | https://dns.quad9.net/dns-query | dns.quad9.net |

```bash
# Test DoH with curl
$ curl -s -H 'Accept: application/dns-json' \
    'https://cloudflare-dns.com/dns-query?name=example.com&type=A' | python3 -m json.tool

# Configure systemd-resolved for DoT
# Edit /etc/systemd/resolved.conf:
[Resolve]
DNS=1.1.1.1#cloudflare-dns.com
DNSOverTLS=yes
```

---

## Common DNS Issues and Debugging

### Problem 1: DNS resolution failure

```bash
# Symptom: "Could not resolve host"
$ curl https://example.com
curl: (6) Could not resolve host: example.com

# Step 1: Check /etc/resolv.conf
$ cat /etc/resolv.conf

# Step 2: Test with a known-good resolver
$ dig @8.8.8.8 example.com

# Step 3: Check if it's a specific record issue
$ dig example.com A
$ dig example.com AAAA

# Step 4: Check if it's a local cache issue
$ sudo resolvectl flush-caches
$ dig example.com
```

---

## Common DNS Issues (continued)

### Problem 2: Slow DNS resolution

```bash
# Measure DNS lookup time
$ time dig example.com +short
93.184.216.34
real    0m0.045s

# If slow, check each resolver
$ dig @8.8.8.8 example.com | grep "Query time"
;; Query time: 12 msec

$ dig @1.1.1.1 example.com | grep "Query time"
;; Query time: 5 msec

# Check for packet loss to DNS server
$ ping -c 10 8.8.8.8
```

### Problem 3: DNS propagation delay

After changing DNS records, different resolvers may return old values due to caching.

```bash
# Check current TTL to know when caches will expire
$ dig example.com A | grep -A1 "ANSWER SECTION"
example.com.    1800    IN    A    93.184.216.34

# Query multiple public resolvers to check propagation
$ dig @8.8.8.8 example.com +short
$ dig @1.1.1.1 example.com +short
$ dig @9.9.9.9 example.com +short
$ dig @208.67.222.222 example.com +short
```

---

## DNS Zones and Zone Files

A zone file is the actual data file on an authoritative DNS server.

```misc
; Zone file for example.com
$TTL 86400
@   IN  SOA   ns1.example.com. admin.example.com. (
              2024010101  ; Serial
              7200        ; Refresh
              3600        ; Retry
              1209600     ; Expire
              86400 )     ; Minimum TTL

; Name servers
@       IN  NS    ns1.example.com.
@       IN  NS    ns2.example.com.

; A records
@       IN  A     93.184.216.34
www     IN  A     93.184.216.34
mail    IN  A     93.184.216.50

; AAAA records
@       IN  AAAA  2606:2800:220:1:248:1893:25c8:1946

; CNAME records
blog    IN  CNAME www.example.com.
ftp     IN  CNAME www.example.com.

; MX records
@       IN  MX    10 mail.example.com.
@       IN  MX    20 mail2.example.com.

; TXT records
@       IN  TXT   "v=spf1 mx -all"

; SRV records
_sip._tcp  IN  SRV  10 60 5060 sip.example.com.
```

---

## DNS Load Balancing Techniques

### Round-Robin DNS

Multiple A records for the same name -- clients get different IPs in rotation:

```bash
$ dig loadbalanced.example.com A
;; ANSWER SECTION:
loadbalanced.example.com. 300 IN A 10.0.0.1
loadbalanced.example.com. 300 IN A 10.0.0.2
loadbalanced.example.com. 300 IN A 10.0.0.3
```

### GeoDNS

Returns different IP addresses based on the client's geographic location:

<svg xmlns="http://www.w3.org/2000/svg" width="480" height="180" font-family="sans-serif">
  <rect x="5" y="5" width="470" height="168" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="240" y="32" font-size="14" fill="#222" text-anchor="middle" font-weight="bold">GeoDNS Server</text>
  <line x1="20" y1="42" x2="460" y2="42" stroke="#333" stroke-width="1"/>
  <text x="30" y="66"  font-size="13" fill="#222">US client  →  1.2.3.4</text>
  <text x="320" y="66"  font-size="12" fill="#555">(US data center)</text>
  <text x="30" y="96"  font-size="13" fill="#222">EU client  →  5.6.7.8</text>
  <text x="320" y="96"  font-size="12" fill="#555">(EU data center)</text>
  <text x="30" y="126" font-size="13" fill="#222">AS client  →  9.0.1.2</text>
  <text x="320" y="126" font-size="12" fill="#555">(Asia data center)</text>
</svg>

Used by CDNs (Cloudflare, AWS Route53, Akamai) for latency-based routing.

---

## DNS Security Threats

| Attack | Description | Mitigation |
|--------|-------------|------------|
| DNS Spoofing | Forged responses redirect users | DNSSEC |
| DNS Cache Poisoning | Corrupt resolver cache | DNSSEC, source port randomization |
| DNS Amplification DDoS | Abuse open resolvers for DDoS | Rate limiting, response rate limiting |
| DNS Tunneling | Exfiltrate data over DNS queries | Monitor unusual query patterns |
| Domain Hijacking | Unauthorized domain transfer | Registrar lock, 2FA |
| Typosquatting | Register similar domain names | Monitor similar domains |

```bash
# Check for open resolver (should NOT respond to external queries)
$ dig @your-server example.com

# Test if DNS responses are being modified (MITM detection)
$ dig +dnssec example.com @8.8.8.8
$ dig +dnssec example.com @1.1.1.1
# Compare RRSIG values -- they should match
```

---

## Python DNS Example

```python
#!/usr/bin/env python3
"""Simple DNS resolver using the socket library and dnspython."""

import socket

# Basic resolution using socket
def resolve_basic(hostname):
    """Resolve hostname using OS resolver."""
    try:
        ip = socket.gethostbyname(hostname)
        print(f"{hostname} -> {ip}")

        # Get all addresses (IPv4)
        ips = socket.gethostbyname_ex(hostname)
        print(f"  Hostname: {ips[0]}")
        print(f"  Aliases:  {ips[1]}")
        print(f"  IPs:      {ips[2]}")

        # Get address info (IPv4 + IPv6)
        results = socket.getaddrinfo(hostname, 80)
        for family, socktype, proto, canonname, sockaddr in results:
            print(f"  {socket.AddressFamily(family).name}: {sockaddr[0]}")
    except socket.gaierror as e:
        print(f"DNS resolution failed: {e}")

resolve_basic("example.com")
```

```bash
$ python3 dns_resolver.py
example.com -> 93.184.216.34
  Hostname: example.com
  Aliases:  []
  IPs:      ['93.184.216.34']
  AF_INET: 93.184.216.34
  AF_INET6: 2606:2800:220:1:248:1893:25c8:1946
```

---

## Advanced DNS with dnspython

```python
#!/usr/bin/env python3
"""Advanced DNS queries using dnspython library."""

import dns.resolver
import dns.reversename
import dns.zone

def query_all_records(domain):
    """Query multiple record types for a domain."""
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']

    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            print(f"\n{rtype} records for {domain}:")
            for rdata in answers:
                print(f"  {rdata}")
                if rtype == 'A' or rtype == 'AAAA':
                    print(f"    TTL: {answers.rrset.ttl}s")
        except dns.resolver.NoAnswer:
            print(f"\n{rtype}: No records found")
        except dns.resolver.NXDOMAIN:
            print(f"\nDomain {domain} does not exist")
            return

def reverse_lookup(ip_address):
    """Perform reverse DNS lookup."""
    rev_name = dns.reversename.from_address(ip_address)
    try:
        answers = dns.resolver.resolve(rev_name, 'PTR')
        for rdata in answers:
            print(f"{ip_address} -> {rdata}")
    except dns.resolver.NXDOMAIN:
        print(f"No PTR record for {ip_address}")

query_all_records("google.com")
reverse_lookup("8.8.8.8")
```

---

## /etc/hosts File

The `/etc/hosts` file provides local static name resolution, checked before DNS.

```bash
$ cat /etc/hosts

# Standard entries
127.0.0.1       localhost
127.0.1.1       myhostname
::1             localhost ip6-localhost ip6-loopback

# Custom entries (useful for development)
192.168.1.100   myserver.local myserver
10.0.0.50       database.dev db
127.0.0.1       myapp.test

# Block unwanted domains (ad blocking)
0.0.0.0         ads.example.com
0.0.0.0         tracking.example.com
```

**Use cases:**
- Local development (map custom domains to localhost)
- Testing before DNS changes go live
- Simple ad/tracker blocking
- Override DNS for specific hosts

---

## DNS Best Practices

1. **Use at least two authoritative name servers** on different networks for redundancy
2. **Set appropriate TTLs**: lower before changes, raise after stability confirmed
3. **Implement DNSSEC** for zones you control
4. **Monitor DNS health**: check resolution times, error rates
5. **Use DNS over HTTPS/TLS** for privacy on client devices
6. **Keep SOA serial numbers** updated when changing zone files
7. **Avoid CNAME at zone apex** -- use A/AAAA records instead
8. **Document your DNS records** -- maintain a record of what each entry is for
9. **Use separate DNS providers** for redundancy (multi-provider DNS)
10. **Test changes** with `dig` before and after applying them

```bash
# Quick DNS health check script
#!/bin/bash
DOMAIN="example.com"
RESOLVERS="8.8.8.8 1.1.1.1 9.9.9.9"

echo "DNS Health Check for $DOMAIN"
echo "=============================="
for resolver in $RESOLVERS; do
    result=$(dig @$resolver $DOMAIN +short +time=2)
    time=$(dig @$resolver $DOMAIN +stats | grep "Query time" | awk '{print $4}')
    echo "Resolver $resolver: $result (${time}ms)"
done
```

---

## Review: DNS Key Concepts

- DNS is a distributed hierarchical naming system
- Multiple record types serve different purposes (A, AAAA, CNAME, MX, TXT, NS, SOA, PTR, SRV)
- Resolution involves recursive resolvers and iterative queries through the hierarchy
- TTL controls caching duration -- balance between freshness and performance
- DNSSEC adds cryptographic authentication to prevent spoofing
- DoH and DoT encrypt DNS queries for privacy
- Tools: `dig`, `nslookup`, `host`, `resolvectl` for querying and debugging
- `/etc/resolv.conf` and `/etc/hosts` are key configuration files on Linux
