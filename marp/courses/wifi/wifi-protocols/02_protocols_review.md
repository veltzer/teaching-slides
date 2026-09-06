---
tags:
  - networking:wifi
  - networking:802.11
level: intermediate
category: networking
audience:
  - audiences:developers
  - audiences:embedded-engineers

---

# Protocols Review

---

## What This Chapter Covers

- The shape of the IEEE 802.11 standard
- Frequency bands the standard lives in
- Each amendment from 802.11 (legacy) through 802.11ax
- What changed at the physical layer in each generation
- The Wi-Fi Alliance's marketing names (Wi-Fi 4, 5, 6, 6E, 7)

---

## The 802.11 Family

- IEEE 802.11 is a *base standard* with periodic *amendments*
- Each amendment is a single letter or two: 802.11a, 802.11b, 802.11ac
- Amendments add new modulations, more bandwidth, new features
- Older devices keep working — the standard mandates backward compatibility
- Wi-Fi Alliance certifies products against the IEEE specs

---

## Bands We Operate In

- 2.4 GHz: ISM band, 11-14 channels (region-dependent), 20 MHz wide
- 5 GHz: many more channels, less crowded, weaker wall penetration
- 6 GHz: opened recently for Wi-Fi 6E and Wi-Fi 7, even more spectrum
- Channel widths: 20, 40, 80, 160 MHz (and 320 MHz in Wi-Fi 7)
- Lower frequency = better range; higher frequency = more capacity

---

## Frequency Bands at a Glance

![frequency_bands](svg/courses/wifi/wifi-protocols/02_protocols_review/frequency_bands.svg)

---

## Channels and Overlap (2.4 GHz)

- 2.4 GHz channels are 5 MHz apart but 20 MHz wide — adjacent channels overlap
- Only channels 1, 6, 11 are non-overlapping in most regions
- Pick a non-overlapping triple to plan a multi-AP deployment
- Bonded 40 MHz channels in 2.4 GHz are usually a bad idea (no room)
- 5 GHz has plenty of non-overlapping wide channels — much easier

---

## Legacy 802.11 (1997)

- The original standard: up to 2 Mbps in 2.4 GHz
- Modulations: DSSS, FHSS
- Almost no devices in the wild today
- Mainly important because frame formats inherit from it
- A modern Wi-Fi 6 AP must still send legacy preambles for compatibility

---

## 802.11b (1999)

- Pushed throughput to 11 Mbps in 2.4 GHz
- Used HR/DSSS modulation
- Cheap chips drove rapid adoption — this is what "Wi-Fi" first meant
- Range good enough for home and small office
- Vulnerable to interference from microwaves and Bluetooth

---

## 802.11a (1999)

- Released alongside 802.11b but used 5 GHz
- 54 Mbps using OFDM (a brand-new technique at the time)
- Less interference, more capacity, but shorter range and pricier chips
- Saw little adoption initially because 2.4 GHz had a head start
- Its OFDM techniques were the foundation for everything that followed

---

## 802.11g (2003)

- Brought OFDM and 54 Mbps to the 2.4 GHz band
- Backward-compatible with 802.11b clients on the same network
- Mixed-mode networks paid a throughput penalty: protection mechanisms were required
- Default Wi-Fi for the mid-2000s
- Effective real-world throughput: ~25 Mbps

---

## 802.11n (2009) — Wi-Fi 4

- First MIMO-capable amendment: up to 4 spatial streams
- 40 MHz channel bonding doubled per-channel capacity
- Top advertised rate: 600 Mbps (4 streams, 40 MHz, short guard interval)
- Operated in both 2.4 GHz and 5 GHz
- Introduced frame aggregation (A-MPDU, A-MSDU) for efficiency

---

## 802.11ac (2013) — Wi-Fi 5

- 5 GHz only; legacy bands stay on 802.11n
- 80 MHz default, optional 160 MHz; up to 8 spatial streams (rarely seen)
- 256-QAM modulation packs 8 bits per subcarrier per symbol
- Wave 1 and Wave 2 — Wave 2 added MU-MIMO and 160 MHz
- Top advertised rate (Wave 2, 4 streams, 160 MHz): ~3.5 Gbps

---

## 802.11ax (2019) — Wi-Fi 6 and Wi-Fi 6E

- Targets *efficiency* in dense environments, not just peak speed
- OFDMA brings per-user time-frequency tiles
- 1024-QAM modulation (10 bits per symbol)
- TWT (Target Wake Time) lets battery devices sleep on a schedule
- Wi-Fi 6E extends Wi-Fi 6 into the 6 GHz band

---

## Generation Comparison

![generation_comparison](svg/courses/wifi/wifi-protocols/02_protocols_review/generation_comparison.svg)

---

## Backward Compatibility, In Practice

- Every modern AP can still talk to a 1999-era 802.11b client
- The cost is real: legacy preambles slow the air down for everyone
- Many enterprise APs let you disable old rates (1, 2, 5.5, 11 Mbps)
- Disabling slow rates kicks off ancient devices but speeds up the channel
- Plan migrations: profile what's actually attached before turning rates off

---

## Channel Width Tradeoffs

- Wider channels: more peak throughput, fewer non-overlapping channels
- 80 MHz in a dense apartment building means everyone overlaps
- Narrower channels: less peak speed but more parallel APs in the same area
- Site survey first, channel-width decisions second
- Auto-channel features in modern APs help but are not magic

---

## Marketing Names vs IEEE Names

- IEEE name: 802.11n &#8594; Wi-Fi 4
- IEEE name: 802.11ac &#8594; Wi-Fi 5
- IEEE name: 802.11ax &#8594; Wi-Fi 6 (and Wi-Fi 6E for 6 GHz support)
- IEEE name: 802.11be &#8594; Wi-Fi 7
- Wi-Fi Alliance simplified the labels because customers couldn't tell which 802.11* was newer

---

## Wi-Fi 7 (802.11be) Preview

- Up to 320 MHz channels in the 6 GHz band
- 4096-QAM modulation (12 bits per symbol)
- Multi-Link Operation (MLO) — one client uses multiple bands at once
- Targets low-latency applications: AR/VR, cloud gaming, real-time control
- Standard ratified late, but products are shipping

---

## Choosing a Generation Today

- New deployment: Wi-Fi 6 minimum, Wi-Fi 6E if you need 6 GHz capacity
- Mixed-vendor environment: stick with widely supported features
- Embedded device: pick the generation your radio chip supports — usually n or ac
- Legacy device support: keep one band on older rates if needed
- Don't pay Wi-Fi 7 prices for clients that can only do Wi-Fi 5
