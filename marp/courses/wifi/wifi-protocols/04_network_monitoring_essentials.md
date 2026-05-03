---
tags:
  - networking:wifi
  - networking:monitoring
level: intermediate
category: networking
audience:
  - audiences:developers
  - audiences:embedded-engineers

---
# Network Monitoring Essentials

---
## What This Chapter Covers

- Monitor mode and why it matters
- The four metrics every Wi-Fi engineer reads first
- Common Linux tools and what they tell you
- Where to put your capture tap
- Decoding protected traffic, when you have the keys

---
## Monitor Mode vs Managed Mode

- *Managed* mode: the radio talks to one AP, ignores everything else
- *Monitor* mode: the radio observes every frame on a channel, attached to none
- Monitor mode is what gives a packet capture its full visibility
- Not all chips and drivers expose monitor mode — check before buying
- Monitor mode is per-channel; you only see what's on the tuned channel

---
## The First Four Metrics

- **RSSI** of each client at the AP — coverage
- **Retry rate** per client — link quality
- **Average data rate** per client — rate-adaptation health
- **Channel utilisation** — how full is the air
- Get these four, in that order, before changing anything

---
## RSSI in Practice

- Reported in dBm; numbers are negative
- &gt; -65 dBm: strong, will sustain top rates
- -65 to -75 dBm: usable, fall-backs likely
- &lt; -75 dBm: marginal, expect retries and slow rates
- &lt; -85 dBm: hardly usable for most modern apps

---
## Retry Rate

- The fraction of frames that needed at least one retransmission
- Healthy networks sit under 5% retry rate
- &gt; 15% means the link is hurting — coverage, interference, or hidden node
- Retries multiply airtime use; a 30% retry rate roughly halves throughput
- Available in the AP dashboard *and* per-frame in a Wireshark capture

---
## Channel Utilisation

- Percent of airtime the channel is busy
- Includes your own traffic, neighbours' traffic, and non-Wi-Fi noise
- Above ~60% the channel is saturated; latency climbs sharply
- Watch for utilisation spikes — they correlate with user complaints
- Many APs split utilisation into self / others / noise — read all three

---
## iw: The Linux Swiss Army Knife

- `iw dev` — list interfaces
- `iw dev wlan0 link` — current AP, signal, rate, frequency
- `iw dev wlan0 scan` — list APs the radio can hear (briefly leaves managed mode)
- `iw dev wlan0 station dump` — per-client stats on an AP
- `iw phy phy0 info` — what the radio supports

---
## Spectrum and Capture Tools

![spectrum_view](svg/courses/wifi/wifi-protocols/04_network_monitoring_essentials/spectrum_view.svg)

---
## Putting wlan0 in Monitor Mode

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo iw dev wlan0 set channel 36
```

- After this Wireshark on `wlan0` sees raw 802.11 frames
- Use `iw dev wlan0 set channel <n>` to hop bands
- Many cards drop other functionality while in monitor mode — your laptop loses Wi-Fi

---
## tcpdump on Monitor Mode

```bash
sudo tcpdump -i wlan0 -s 0 -w cap.pcap \
  '(type mgt or type ctl)'
```

- `-s 0` captures full frame length
- The filter limits to management and control frames — useful for handshake debugging
- Open `cap.pcap` in Wireshark for analysis
- For data frames, drop the filter (file fills up fast on a busy channel)

---
## Wireshark Display Filters

- `wlan.fc.type == 0` — management frames
- `wlan.fc.type == 1` — control frames
- `wlan.fc.type == 2` — data frames
- `wlan.fc.retry == 1` — retransmissions only
- `wlan.addr == aa:bb:cc:dd:ee:ff` — frames involving one MAC

---
## Where to Tap

- On a laptop in the same room as the user — sees what they see
- Next to the AP — sees the AP side, but misses client-side hidden nodes
- A dedicated capture box on a USB radio — best for sustained monitoring
- AP-integrated packet capture (vendor-specific) — convenient, sometimes lossy
- Capture *both ends* for the worst problems

---
## Decoding WPA2 Captures

- 802.11 traffic is encrypted per-association via the 4-way handshake
- Wireshark needs the PSK *and* the full handshake to decrypt
- Configure under Preferences &#8594; IEEE 802.11 &#8594; Decryption Keys
- WPA3 uses SAE — different handshake, different decoding story
- Without keys you still see *headers* (addresses, types, sizes) but not payload

---
## Beacon Frames

- The AP advertises itself ~10 times per second by default
- Beacon contents: SSID, supported rates, capabilities, vendor IEs
- A capture full of beacons is normal; filter them out with `!(wlan.fc.type_subtype == 0x08)`
- Missing beacons at the client = roaming or coverage hole
- Vendor IEs leak product info — useful for fingerprinting

---
## Probe Requests and Responses

- Clients shout "any AP for SSID X?" via probe requests
- Some clients leak a *list* of remembered SSIDs in probes — privacy issue
- Modern phones randomise their MAC during probing
- Probe responses are basically targeted beacons
- Watch probes to discover which devices are around without associating

---
## Capture Hygiene

- Capture sessions get big fast — start with rotation: `tcpdump -W 10 -G 60`
- Keep timestamps accurate; sync your capture box to NTP
- Note the channel, AP MAC, and any test you ran in a separate text file
- Captures contain client MACs and PSK-encrypted payloads — handle as sensitive
- Anonymise before sharing if needed

---
## Tooling Map

![tooling_map](svg/courses/wifi/wifi-protocols/04_network_monitoring_essentials/tooling_map.svg)
