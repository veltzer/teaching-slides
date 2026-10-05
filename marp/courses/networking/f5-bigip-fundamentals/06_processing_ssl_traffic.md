---
tags:
  - security:tls
  - networking:http
  - networking:troubleshooting
  - networking:performance
level: beginner
category: networking
audience:
  - audiences:network-engineers
  - audiences:sysadmins
  - audiences:devops

---

# Processing SSL Traffic

---

## What This Chapter Covers

- `SSL/TLS` on a full proxy: offload, re-encryption and pass through
- Managing certificates and keys on `BIG-IP`
- Importing certificates, keys and chains; creating `CSR`s
- Client `SSL` profiles: certificate, key, chain, protocols, ciphers
- Server `SSL` profiles and re-encrypting traffic to the servers
- `SNI`: several certificates on one virtual server
- `SSL` statistics and handshake troubleshooting

---

## Why BIG-IP Terminates TLS

- Almost all client traffic today arrives encrypted
- Encrypted traffic is opaque: no `HTTP` profile, no cookie persistence, no policies
- Terminating `TLS` on `BIG-IP` turns the bytes back into requests
- One place to manage certificates instead of every web server
- Hardware or `AES-NI` crypto acceleration takes the load off the servers
- One place to enforce protocol versions and cipher policy

---

## SSL Deployment Modes

![ssl_deployment_modes](svg/courses/networking/f5-bigip-fundamentals/06_processing_ssl_traffic/ssl_deployment_modes.svg)

---

## Comparing the Deployment Modes

| Mode | Client side | Server side | Profiles on the virtual | `L7` visibility |
| --- | --- | --- | --- | --- |
| Offload | `HTTPS` | `HTTP` | client `SSL` | Full |
| Re-encryption | `HTTPS` | `HTTPS` | client `SSL` + server `SSL` | Full |
| Pass through | `HTTPS` | `HTTPS` | none (`TCP` only) | None |

- Offload: cheapest for the servers, cleartext on the internal network
- Re-encryption: compliance (`PCI`, zero trust) with full visibility
- Pass through: the servers own the keys; `BIG-IP` is a `L4` load balancer

---

## SSL Offload

- Client `SSL` profile on the virtual server, no server `SSL` profile
- Pool members listen on port `80`
- Servers see plain `HTTP`, often need to know the original scheme
- Insert `X-Forwarded-Proto: https` with a policy or `HTTP` profile header insert
- The internal segment between `BIG-IP` and servers must be trusted

```bash
tmsh create ltm virtual vs_app_https destination 10.1.10.100:443 \
    ip-protocol tcp pool app_http_pool \
    profiles add { tcp http clientssl_app { context clientside } } \
    source-address-translation { type automap }
```

---

## SSL Re-encryption

- Client `SSL` profile decrypts; server `SSL` profile encrypts again
- Pool members listen on `443`
- `BIG-IP` sees cleartext in between: profiles, persistence, policies all work
- Server certificates can be internal or self-signed; `BIG-IP` may not verify them
- Costs two handshakes per connection; `OneConnect` and session reuse help

```bash
tmsh create ltm virtual vs_app_reencrypt destination 10.1.10.101:443 \
    ip-protocol tcp pool app_https_pool \
    profiles add { tcp http clientssl_app { context clientside } \
                   serverssl { context serverside } } \
    source-address-translation { type automap }
```

---

## SSL Pass Through

- No `SSL` profiles; the virtual server sees only encrypted `TCP`
- No `HTTP` profile possible, no cookie persistence, no header insertion
- Persistence options: source address, or `SSL` session ID persistence
- Useful when the keys must stay on the servers (`HSM`, legal, mutual `TLS` at the app)
- A `Performance (Layer 4)` or standard virtual with only a `TCP` profile

```bash
tmsh create ltm virtual vs_app_passthru destination 10.1.10.102:443 \
    ip-protocol tcp pool app_https_pool profiles add { fastL4 } \
    persist replace-all-with { source_addr }
```

---

## The Client Side Handshake

![client_handshake](svg/courses/networking/f5-bigip-fundamentals/06_processing_ssl_traffic/client_handshake.svg)

---

## What BIG-IP Does in the Handshake

- Acts as the `TLS` server towards the client
- Chooses the protocol version from the intersection of both sides
- Chooses the cipher by the order in the profile cipher string
- Sends the certificate plus the configured chain
- Performs the private key operation (`RSA` or `ECDSA`) in `TMM`
- `TLS 1.3` shortens this to one round trip; the logic is the same

---

## Where Certificates Live

- GUI: System > Certificate Management > Traffic Certificate Management > SSL Certificate List
- A certificate and its key share one name (for example `app.example.com`)
- Stored by `mcpd` as file objects, backed by files under `/config/filestore`
- Included in the `UCS` archive; not included in `SCF` exports
- Device certificate for the management `GUI` is separate (Device Certificates)

```bash
tmsh list sys file ssl-cert app.example.com
tmsh list sys file ssl-key app.example.com
tmsh list sys crypto cert app.example.com
```

---

## Text Certificate and Key Files

| Format | Extension | Content | `BIG-IP` import |
| --- | --- | --- | --- |
| `PEM` | `.crt`, `.pem` | Base64 certificate, `BEGIN CERTIFICATE` | Certificate |
| `PEM` key | `.key` | Base64 private key, maybe encrypted | Key |
| Bundle | `.crt` | Several `PEM` certificates concatenated | Certificate (chain) |

---

## Binary Certificate and Key Files

| Format | Extension | Content | `BIG-IP` import |
| --- | --- | --- | --- |
| `DER` | `.cer`, `.der` | Binary certificate | Convert to `PEM` first |
| `PKCS#12` | `.pfx`, `.p12` | Certificate + key (+ chain), password protected | `PKCS 12 (IIS)` |

---

## Converting Certificate Formats

```bash
openssl x509 -inform der -in app.cer -out app.crt
openssl pkcs12 -in app.pfx -nokeys -out app_with_chain.crt
```

---

## The Certificate Chain of Trust

![certificate_chain](svg/courses/networking/f5-bigip-fundamentals/06_processing_ssl_traffic/certificate_chain.svg)

---

## Importing Certificates and Keys

1. Copy the files to the `BIG-IP` (`scp` to `/var/tmp`) or use the `GUI` Import button
1. Import the key, then the certificate, with the same object name
1. Import the intermediate bundle as its own certificate object
1. Verify the key matches the certificate before using them

```bash
tmsh install sys crypto key app.example.com from-local-file /var/tmp/app.key
tmsh install sys crypto cert app.example.com from-local-file /var/tmp/app.crt
tmsh install sys crypto cert digicert_chain from-local-file /var/tmp/chain.crt
```

---

## Verifying a Key Matches a Certificate

- A mismatched pair makes the profile fail to save or the handshake fail
- Compare the modulus (`RSA`) or public key hash of both files

```bash
cd /config/filestore/files_d/Common_d
openssl x509 -noout -modulus -in certificate_d/:Common:app.example.com.crt_* | md5sum
openssl rsa  -noout -modulus -in certificate_key_d/:Common:app.example.com.key_* | md5sum
```

- The two hashes must be identical
- Also check dates: `openssl x509 -noout -dates -subject -issuer -in ...`

---

## Encrypted Private Keys

- Keys can be stored with a passphrase (`Security Type: Password`)
- The profile then needs the passphrase to load the key
- Keys can also live in a `FIPS` card, `NetHSM` or cloud `HSM`
- Whoever has `UCS` archives has the keys: protect them like the keys themselves
- Set `encryption` on `UCS` saves: `tmsh save sys ucs backup.ucs passphrase <secret>`

---

## Certificate Signing Requests

![csr_workflow](svg/courses/networking/f5-bigip-fundamentals/06_processing_ssl_traffic/csr_workflow.svg)

---

## Creating a CSR in tmsh

```bash
tmsh create sys crypto key app.example.com key-size 2048 gen-csr \
    country US state CA city "San Jose" organization "Example Inc" \
    common-name app.example.com \
    subject-alternative-name "DNS:app.example.com, DNS:www.example.com"
tmsh list sys crypto csr app.example.com
```

- The key is generated on `BIG-IP` and never leaves it
- Modern browsers ignore the common name: the `SAN` list must be complete
- Paste the `CSR` into the `CA` portal; import the returned certificate under the same name

---

## Self-Signed and Default Certificates

- `default.crt` / `default.key`: self-signed, created at install time
- The built in `clientssl` profile uses them
- Good for a lab, never for production: every browser will warn
- Create a self-signed certificate for internal testing:

```bash
tmsh create sys crypto key lab.example.com key-size 2048 \
    gen-certificate common-name lab.example.com lifetime 365
```

---

## Watching Certificate Expiry

- Expired certificates are the most common `SSL` outage
- `BIG-IP` logs warnings to `/var/log/ltm` as expiry approaches
- The certificate list shows a status icon per certificate
- Check from the command line and feed it to your monitoring

```bash
tmsh run sys crypto check-cert
tmsh list sys crypto cert all-properties | grep -E '^sys|expiration'
```

---

## Profile Placement

![profile_placement](svg/courses/networking/f5-bigip-fundamentals/06_processing_ssl_traffic/profile_placement.svg)

---

## The Client SSL Profile

- Local Traffic > Profiles > SSL > Client
- Parent: `clientssl`; always create a child, never edit the parent
- Applies on the client side (`context clientside`)
- Key settings: certificate key chain, ciphers, options, renegotiation, `SNI`
- One virtual server can carry several client `SSL` profiles (for `SNI`)

---

## Certificate, Key and Chain

```bash
tmsh create ltm profile client-ssl clientssl_app \
    defaults-from clientssl \
    cert-key-chain replace-all-with { app_chain { \
        cert app.example.com key app.example.com chain digicert_chain } }
tmsh modify ltm virtual vs_app_https profiles add { clientssl_app }
```

- `cert-key-chain` can hold one `RSA` and one `ECDSA` pair
- `BIG-IP` sends the `ECDSA` certificate to clients that support it
- Forgetting the chain works in some browsers and fails in others

---

## Testing the Chain From the Client

```bash
openssl s_client -connect 10.1.10.100:443 -servername app.example.com \
    -showcerts </dev/null | grep -E 's:|i:'
```

```output
 0 s:CN = app.example.com
   i:C = US, O = DigiCert Inc, CN = DigiCert TLS RSA SHA256 2020 CA1
 1 s:C = US, O = DigiCert Inc, CN = DigiCert TLS RSA SHA256 2020 CA1
   i:C = US, O = DigiCert Inc, OU = www.digicert.com, CN = DigiCert Global Root CA
```

- Certificate `0` is the leaf; each `i:` must match the next `s:`
- The root is not sent: the client already has it

---

## Retired Protocol Versions

| Version | Status | Recent `BIG-IP` default | Recommendation |
| --- | --- | --- | --- |
| `SSLv3` | Broken (`POODLE`) | Disabled | Never |
| `TLS 1.0` | Deprecated (`RFC 8996`) | Disabled in new profiles | Disable |
| `TLS 1.1` | Deprecated (`RFC 8996`) | Disabled in new profiles | Disable |

---

## Current Protocol Versions

| Version | Status | Recent `BIG-IP` default | Recommendation |
| --- | --- | --- | --- |
| `TLS 1.2` | Current | Enabled | Enable |
| `TLS 1.3` | Current | Off until enabled | Enable |

---

## Switching Versions On and Off

- Versions are switched off with `options`: `no-tlsv1`, `no-tlsv1.1`
- `TLS 1.3` is enabled by removing `no-tlsv1.3` from the options

---

## Disabling Old Protocols

```bash
tmsh modify ltm profile client-ssl clientssl_app \
    options { dont-insert-empty-fragments no-tlsv1 no-tlsv1.1 }
tmsh list ltm profile client-ssl clientssl_app options
```

- Check who still connects with old versions before disabling them
- `tmsh show ltm profile client-ssl clientssl_app` lists per-version counts
- Disabling a version the client needs causes a handshake failure, not a fallback

---

## Cipher Strings

| Cipher string | Meaning |
| --- | --- |
| `DEFAULT` | `F5` curated default list for the version |
| `ECDHE` | Only suites with forward secret `ECDHE` key exchange |
| `ECDHE:!SHA1:!3DES` | `ECDHE`, minus `SHA-1` and `3DES` suites |
| `ECDHE+AES-GCM` | `ECDHE` key exchange with `AES-GCM` encryption |
| `@SPEED` | Sort the list by performance |
| `!RC4:!EXPORT:!NULL` | Remove broken suites |

- Same syntax as `OpenSSL`: `:` separates, `!` removes, `+` combines
- Order matters: `BIG-IP` picks the first suite in its list that the client offers

---

## Testing a Cipher String

```bash
tmm --clientciphers 'ECDHE:!SHA1:!3DES'
```

```output
       ID  SUITE                          BITS PROT    CIPHER  MAC     KEYX
 0: 49199  ECDHE-RSA-AES128-GCM-SHA256    128  TLS1.2  AES-GCM SHA256  ECDHE_RSA
 1: 49200  ECDHE-RSA-AES256-GCM-SHA384    256  TLS1.2  AES-GCM SHA384  ECDHE_RSA
 2: 49191  ECDHE-RSA-AES128-SHA256        128  TLS1.2  AES     SHA256  ECDHE_RSA
```

- Run `tmm --clientciphers` before putting a string in a profile
- An empty result means no client could ever connect

---

## Cipher Rules and Groups

- Since `BIG-IP` `13.0` ciphers can also be built from objects
- Cipher rule: a cipher string plus `DH` groups and signature algorithms
- Cipher group: allow and exclude lists of rules, plus ordering
- Profile setting `cipher-group` replaces the `ciphers` string
- `F5` ships rules such as `f5-default`, `f5-secure`, `f5-ecc`

```bash
tmsh create ltm cipher rule rule_strong cipher 'ECDHE+AES-GCM'
tmsh create ltm cipher group group_strong allow add { rule_strong }
tmsh modify ltm profile client-ssl clientssl_app ciphers none cipher-group group_strong
```

---

## Session Resumption Options

| Setting | Default | Purpose |
| --- | --- | --- |
| `cache-size` / `cache-timeout` | `262144` / `3600` | Session ID cache for resumption |
| `session-ticket` | disabled | Stateless resumption with tickets |
| `strict-resume` | disabled | Refuse resumption after an unclean shutdown |

---

## Renegotiation, Client Certificates and Alerts

| Setting | Default | Purpose |
| --- | --- | --- |
| `renegotiation` | enabled | Allow mid-session renegotiation; usually disable |
| `peer-cert-mode` | ignore | Request or require client certificates (mutual `TLS`) |
| `alert-timeout` | indefinite | How long to wait for a close alert |

---

## The Server SSL Profile

- Local Traffic > Profiles > SSL > Server; parent `serverssl`
- Applies on the server side (`context serverside`); `BIG-IP` is the `TLS` client
- Default: no server certificate validation (`peer-cert-mode ignore`)
- Server side ciphers and versions can differ from the client side
- Turn on validation when the network to the servers is not trusted

```bash
tmsh create ltm profile server-ssl serverssl_app defaults-from serverssl \
    peer-cert-mode require ca-file ca-bundle.crt \
    authenticate-name app.internal.example.com server-name app.internal.example.com
```

---

## Re-encryption Settings That Matter

- `server-name`: the `SNI` value sent to the server (needed by most `HTTPS` servers)
- `authenticate-name`: the name expected in the server certificate
- `ca-file`: which `CA`s `BIG-IP` trusts for the server certificates
- `cert` / `key`: a client certificate if the server requires mutual `TLS`
- Server side session reuse keeps the extra handshake cheap

---

## Several Sites on One Virtual Server

- Without `SNI` a virtual server can serve only one certificate
- With `SNI` the client sends the host name in the `ClientHello`
- `BIG-IP` picks the client `SSL` profile whose `server-name` matches
- One profile must be marked `sni-default true` for clients without `SNI`
- A wildcard or multi-`SAN` certificate is the alternative

---

## SNI Profile Selection

![sni_selection](svg/courses/networking/f5-bigip-fundamentals/06_processing_ssl_traffic/sni_selection.svg)

---

## Configuring SNI

```bash
tmsh create ltm profile client-ssl clientssl_shop defaults-from clientssl \
    cert-key-chain replace-all-with { shop { cert shop.example.com key shop.example.com } } \
    server-name shop.example.com
tmsh create ltm profile client-ssl clientssl_api defaults-from clientssl \
    cert-key-chain replace-all-with { api { cert api.example.com key api.example.com } } \
    server-name api.example.com
tmsh create ltm profile client-ssl clientssl_default defaults-from clientssl \
    cert-key-chain replace-all-with { def { cert shop.example.com key shop.example.com } } \
    sni-default true
tmsh modify ltm virtual vs_https profiles add { clientssl_shop clientssl_api clientssl_default }
```

---

## Viewing SSL Statistics

```bash
tmsh show ltm profile client-ssl clientssl_app
tmsh show ltm profile client-ssl clientssl_app field-fmt | grep -iE 'handshake|fail|tlsv'
tmsh reset-stats ltm profile client-ssl clientssl_app
```

- Current and total connections per profile
- Handshake failures, fatal alerts, bad records
- Counts per protocol version and per cipher: the evidence for retiring old ones
- GUI: Statistics > Module Statistics > Local Traffic > Profiles Summary

---

## Testing With openssl s_client

```bash
openssl s_client -connect 10.1.10.100:443 -servername app.example.com -tls1_2
openssl s_client -connect 10.1.10.100:443 -servername app.example.com -tls1_1
openssl s_client -connect 10.1.10.100:443 -cipher 'AES128-SHA' -tls1_2
```

- Force one version or one cipher at a time and watch for success or an alert
- `Verify return code: 0 (ok)` means the chain is valid from the client view
- `-servername` sets `SNI`: leave it out to see the default profile
- `curl -vk https://...` gives a quick summary of version, cipher and certificate

---

## Capturing Handshakes With tcpdump

```bash
tcpdump -ni 0.0:nnn -s0 -w /var/tmp/ssl.pcap host 10.1.10.50 and port 443
```

- `0.0` captures on all `TMM` interfaces; `:nnn` adds `TMM` metadata
- Open the file in `Wireshark`; filter `tls.handshake`
- The `ClientHello` shows offered versions, ciphers and `SNI`
- A `TLS` alert right after `ClientHello` points to version or cipher mismatch
- Captures contain encrypted payload only; that is usually enough for handshakes

---

## Logs for SSL Problems

```bash
grep -i ssl /var/log/ltm | tail -20
tmsh modify sys db log.ssl.level value Debug
tmsh modify sys db log.ssl.level value Warning
```

- Typical messages: `SSL Handshake failed`, `no shared cipher`, `alert(40)`
- `Debug` level is verbose: turn it on briefly, then back to `Warning`
- Server side failures appear with the pool member address

---

## Troubleshooting Certificate Problems

| Symptom | Likely cause | Check |
| --- | --- | --- |
| Browser warns, name mismatch | Wrong certificate or missing `SAN` | `s_client` subject, `SNI` profile |
| Works in one browser, fails in another | Chain not configured | `-showcerts` depth |
| Sudden outage for everyone | Expired certificate | `check-cert`, expiry dates |

---

## Troubleshooting Handshake Problems

| Symptom | Likely cause | Check |
| --- | --- | --- |
| `handshake failure` alert | No shared version or cipher | `tmm --clientciphers`, profile options |
| Old clients cannot connect | `TLS 1.0/1.1` disabled | Version counters in stats |
| `502`/reset on re-encrypt only | Server side handshake fails | Server `SSL` stats, `server-name` |

---

## Lab: Offload a Web Application

1. Generate a key and self-signed certificate `lab.example.com` on `bigip1`
1. Create `clientssl_lab` with that certificate and key
1. Build `vs_lab_https` on `10.1.10.100:443` with `http`, `clientssl_lab`, `SNAT` `automap`
1. Point it at the existing `HTTP` pool (`10.1.20.11-13:80`)
1. Test from the client: `curl -vk https://10.1.10.100/`
1. Check `tmsh show ltm profile client-ssl clientssl_lab`

---

## Lab: Re-encrypt and Restrict

1. Create a second pool of the same servers on port `443`
1. Add a server `SSL` profile and attach the new pool
1. Disable `TLS 1.0` and `TLS 1.1` in `clientssl_lab`
1. Prove it with `openssl s_client -tls1_1` (fails) and `-tls1_2` (works)
1. Restrict the ciphers to `ECDHE+AES-GCM` and verify with `tmm --clientciphers`
1. Capture one handshake with `tcpdump` and open it in `Wireshark`

---

## Lab: SNI

1. Create certificates for `shop.example.com` and `api.example.com`
1. Create two client `SSL` profiles with matching `server-name` values
1. Mark one profile as `sni-default`
1. Attach all to one virtual server
1. Test with `openssl s_client -servername shop.example.com` and `api.example.com`
1. Test without `-servername` and see which certificate comes back

---

## Key Takeaways

- Terminating `TLS` gives `BIG-IP` the visibility every other feature depends on
- Offload, re-encrypt or pass through: choose per application
- Certificate and key share a name; always configure the chain
- Client `SSL` faces the client, server `SSL` faces the pool
- Control versions with `options` and suites with cipher strings or groups
- `SNI` serves many certificates from one address
- `s_client`, `tcpdump` and profile statistics find most handshake problems
