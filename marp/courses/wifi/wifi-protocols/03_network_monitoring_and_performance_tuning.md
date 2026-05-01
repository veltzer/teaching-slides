---
tags:
  - networking:wifi
  - networking:performance
level: intermediate
category: networking
audience:
  - audiences:developers
  - audiences:embedded-engineers

---
# Network Monitoring and Performance Tuning

---
## What This Chapter Covers

- Why a "fast" Wi-Fi network can still feel slow
- Throughput vs goodput vs application latency
- Where time disappears: airtime, retries, and contention
- Tuning levers that actually matter
- A short tour of useful tools

---
## Throughput Is Not Speed

- Advertised "1 Gbps" is the link rate of a single client to the AP
- Goodput is what an application actually sees end-to-end
- The gap is real: typically 50-70% of the link rate at best
- Many factors eat the difference: protocol overhead, retries, contention
- Treat manufacturer numbers as upper bounds, not promises

---
## Where Airtime Goes

- Every packet costs *time on the medium*
- Preamble + headers eat fixed overhead per frame
- Acknowledgements add another whole frame round-trip
- Retransmissions multiply both
- Many small frames waste airtime even at high link rates

---
## Contention and Collisions

- Wi-Fi is half-duplex: the AP and clients take turns
- The protocol uses CSMA/CA: listen before sending, back off if busy
- Many active clients means more time spent backing off
- Hidden node problem: two clients can't hear each other but both hit the AP
- RTS/CTS reduces collisions at the cost of more overhead

---
## Rate Adaptation

- The radio picks a modulation per packet based on recent success rates
- Strong link &#8594; high QAM, more bits per symbol
- Weak link &#8594; fall back to BPSK, fewer bits per symbol
- Algorithms are vendor-specific (Minstrel, Iwlwifi rate control, etc.)
- One slow client running at 1 Mbps can drag down the whole BSS

---
## RSSI, SNR, and What They Mean

- RSSI: received signal strength, measured in dBm (more negative = weaker)
- SNR: signal-to-noise ratio, in dB (bigger = cleaner)
- Useful rule of thumb: SNR > 25 dB for stable high-rate links
- RSSI alone is not enough — a strong signal in a noisy environment is still bad
- Modern APs report SNR per client; check that, not just bars

---
## Where Latency Hides

- Airtime contention adds variable delay
- Power-save: a sleeping client must be woken before it can receive
- AP buffer bloat: queues filled with bulk traffic delay tiny VOIP packets
- Roaming events: brief gaps as the client switches APs
- DNS, NAT, and the wider internet are always on top of all of this

---
## Tuning Lever 1: Channel Choice

- Pick non-overlapping channels: 1/6/11 in 2.4 GHz, the wide DFS range in 5 GHz
- Use a survey tool, not just the APs auto-channel
- Account for neighbours — your neighbour's AP is your noise floor
- Re-scan periodically; the radio environment drifts
- One bad channel often explains 90% of complaints

---
## Tuning Lever 2: Channel Width

- Wider channels &#8594; higher peak speed, fewer non-overlapping channels
- 80 MHz in a dense building usually backfires
- 40 MHz in 5 GHz is a sane default for most offices
- 20 MHz in 2.4 GHz is the only sane choice
- Match width to client mix — old clients can't use bonded channels anyway

---
## Tuning Lever 3: Disabling Slow Rates

- A 1 Mbps client transmits 100x slower than a 100 Mbps client per byte
- Each slow frame burns airtime everyone else has to wait for
- Many APs let you set a minimum basic rate (e.g., 12 Mbps)
- Devices that can't reach the floor get kicked off — usually a feature
- Audit your fleet first; a thermostat needs Wi-Fi too

---
## Tuning Lever 4: Roaming Behaviour

- Sticky clients hold onto a far AP even after walking near a closer one
- 802.11k/v/r help: clients learn neighbours, are nudged to roam, and roam fast
- Most APs implement these but clients have to support them too
- Old IoT devices ignore the standard; nothing helps them
- Plan AP density assuming clients are dumber than you'd like

---
## Tuning Lever 5: QoS / WMM

- WMM (Wi-Fi Multimedia) maps DSCP into 4 access categories: voice, video, best-effort, background
- High-priority categories get shorter back-off — cut the line for airtime
- Useless if upstream switches strip DSCP markings
- Pair WMM with the wired QoS policy or it does nothing
- Voice on Wi-Fi without WMM sounds bad in any congested cell

---
## Useful Tools

- `iw` (Linux): low-level radio info, scan, station stats
- `wpa_cli`: status of the supplicant, signal/noise of the current AP
- Wireshark with a monitor-mode interface: capture frames, watch retries
- Vendor dashboards: airtime utilisation, retries, top talkers
- Spectrum analyser hardware: see *non-Wi-Fi* interferers (microwaves, baby monitors)

---
## Reading a Capture

- Look at retry rate per client: > 10% means the link is hurting
- Watch the actual data rate column — clients should sit near max, not the floor
- Beacon misses indicate roaming or coverage holes
- Block ACKs (BA) are normal — every aggregated chunk is acknowledged at once
- Excessive RTS/CTS may mean a hidden node is active

---
## Performance Tuning Workflow

![tuning_workflow](svg/courses/wifi/wifi-protocols/03_network_monitoring_and_performance_tuning/tuning_workflow.svg)

---
## Pitfalls

- Believing the auto-channel feature is set-and-forget
- Trusting a single test from one location
- Ignoring the wired side: a misconfigured switch port hurts wireless too
- Tuning per-AP without thinking about the whole BSS
- Forgetting that throughput and latency are different problems

---
## A Short Checklist

- Confirm channel plan is sane for the building
- Check that fast clients see SNR > 25 dB at all times
- Audit retry rates and slow rates per client
- Confirm WMM end-to-end if voice/video matter
- Re-survey after significant changes (new walls, more clients, more APs)
