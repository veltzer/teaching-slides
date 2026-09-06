---
tags:
  - networking:wifi
  - security:wireless
level: intermediate
category: networking
audience:
  - audiences:developers
  - audiences:embedded-engineers

---

# Wireless Security

---

## What This Chapter Covers

- Why wireless is fundamentally a different security problem
- WEP and what went wrong
- WPA and WPA2: the workhorse era
- The four-way handshake
- WPA3 and what it actually fixes
- Enterprise authentication via 802.1X
- Practical attacker behaviour and defender response

---

## What Makes Wireless Different

- The medium is *broadcast* — anyone in radio range hears your frames
- Physical site security buys you nothing
- Attackers can be in the parking lot, in the next office, or six floors down
- "Encrypted on the wire" is not optional, it's table stakes
- Authentication needs to be mutual — the AP can also be impersonated

---

## The Threats, Concretely

- Eavesdropping: read other clients' traffic
- Impersonation: fake AP captures credentials
- Deauth attacks: knock clients off the network for fun or to force a re-auth
- Brute force: capture a handshake, attack the password offline
- Lateral movement: a compromised IoT device on the same SSID reaches your laptop

---

## WEP (Wired Equivalent Privacy)

- The original 802.11 security, defined in 1997
- 40-bit (later 104-bit) RC4 key
- Shared key — same one for every client and the AP
- IV (initialization vector) only 24 bits long, sent in the clear
- Catastrophically broken — by 2007, real-world attacks recovered keys in minutes

---

## Why WEP Fell

- Short IV space meant IV collisions on busy networks
- Attackers collect enough IV-encrypted frames and recover the key with statistics
- Tools like aircrack-ng made this trivial
- Even with strong passphrases, the protocol itself was the weak link
- Modern advice: do not enable WEP, ever; treat WEP networks as open

---

## WPA (Wi-Fi Protected Access)

- Released in 2003 as a stop-gap on the way to 802.11i / WPA2
- Reused WEP-era hardware: still RC4, but with TKIP key mixing
- Per-frame keys, longer IVs, message integrity check
- Bought time, but TKIP is also now broken
- WPA-only networks should be treated like WEP — upgrade

---

## WPA2

- Standardised in 2004 as IEEE 802.11i
- Replaced RC4 with AES-CCMP (real block cipher, real authenticated encryption)
- Two modes: WPA2-Personal (pre-shared key) and WPA2-Enterprise (802.1X)
- Has been the workhorse of Wi-Fi security for ~20 years
- Vulnerable to KRACK in 2017, patched in clients and APs

---

## WPA Evolution

![wpa_evolution](svg/courses/wifi/wifi-protocols/06_security/wpa_evolution.svg)

---

## The 4-Way Handshake

- After association, AP and client run a 4-frame exchange to derive session keys
- Inputs: PSK (or 802.1X master key), AP MAC, client MAC, two random nonces
- Output: PTK (pairwise transient key) for unicast, GTK for broadcast
- Each new association generates fresh nonces and fresh keys
- The handshake is in the clear — captureable by any monitor in range

---

## 4-Way Handshake Diagram

![handshake](svg/courses/wifi/wifi-protocols/06_security/handshake.svg)

---

## Why the Handshake Matters to Attackers

- Capture the 4 EAPOL frames + the SSID + the MACs &#8594; can attempt offline brute force
- Attacker cycles through candidate passwords, derives PTKs, checks integrity
- A weak passphrase falls in seconds with a GPU
- Strong passphrases (random, &#8805; 14 chars) defeat this
- WPA3 fundamentally changes this game (next slide)

---

## WPA3 Personal: SAE

- Replaces the PSK handshake with SAE (Simultaneous Authentication of Equals)
- Each handshake is its own zero-knowledge proof
- Capturing it tells the attacker *nothing* useful for offline attack
- Forward secrecy: a leaked password does not decrypt past sessions
- Still the same UI: a SSID and a passphrase

---

## WPA3 Enterprise

- 802.1X with stricter modern crypto requirements
- 192-bit security mode for high-assurance environments
- Eliminates the worst legacy EAP methods (no MS-CHAPv2 password leaks)
- Backward-compatible with WPA2 clients via "transition mode"
- Adoption is growing but still mixed; many devices still ship WPA2 only

---

## 802.1X / WPA-Enterprise Flow

- Client &#8594; AP &#8594; RADIUS server
- Client and RADIUS run an EAP method (PEAP, EAP-TLS, EAP-TTLS, etc.)
- On success, RADIUS hands the AP a master key
- AP and client then run the normal 4-way handshake using that master key
- No shared password between users — each user has their own credential

---

## EAP Method Choice

- EAP-TLS: client certificate + server certificate. The gold standard.
- PEAP-MSCHAPv2: server cert + username/password. Common, but MSCHAPv2 has known weaknesses
- EAP-TTLS: similar to PEAP, more flexible inner methods
- LEAP: Cisco-only legacy method, broken — do not use
- New deployments: EAP-TLS if you have a PKI, otherwise PEAP with very strong passwords

---

## Common Configuration Mistakes

- Open guest networks with no isolation — guest devices attack each other
- WPA2-Personal with the same PSK shared by 200 employees — leaked once, leaked forever
- Disabling SSID broadcast for "security" — accomplishes nothing, breaks some clients
- MAC filtering — trivially bypassed (MACs are on the air in the clear)
- Trusting captive portals as authentication — they don't encrypt the link

---

## Rogue AP Detection

- Attackers stand up an AP with the same SSID as yours
- Clients with cached credentials may auto-associate to it
- Many enterprise APs include rogue-AP scanning during off-channel time
- Detection is statistical: you flag SSIDs you didn't authorise on unknown channels
- Shutting down a rogue requires physical pursuit — or just shutting your client off

---

## Deauthentication Attacks

- Management frames in 802.11 were *unauthenticated* originally
- An attacker sends a deauth frame on behalf of the AP
- Client thinks the AP wants it gone, disconnects, then re-associates
- Useful for forcing handshake captures, denial of service, or evil twins
- Protected Management Frames (802.11w) authenticate these — enabled by default in WPA3

---

## Practical Defender Checklist

- WPA3 if every client supports it; WPA2-AES-only otherwise
- WPA-Enterprise with EAP-TLS for staff networks
- Separate IoT VLAN behind its own SSID
- Strong PSK for any personal-mode network: random, &#8805; 16 characters
- Rotate the PSK periodically; rotate immediately on staff turnover
- Enable Protected Management Frames (PMF / 802.11w)

---

## Course Wrap-Up

- The physical layer (OFDM, MIMO, beamforming) is what the engineering depth is in
- Protocol generations layer up: each one adds bandwidth and efficiency
- Real-world performance comes from honest measurement, not advertised specs
- Security has had a clear arc: WEP &#8594; WPA &#8594; WPA2 &#8594; WPA3
- Wireless is a moving target — both standards and threats keep evolving
