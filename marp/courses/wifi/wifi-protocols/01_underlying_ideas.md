---
tags:
  - networking:wifi
  - networking:physical-layer
level: intermediate
category: networking
audience:
  - audiences:developers
  - audiences:embedded-engineers

---
# Underlying Ideas

---
## What This Chapter Covers

- Why a wireless link is physically harder than a wire
- OFDM: turning one fast carrier into many slow ones
- MIMO: making the air carry more than one signal at a time
- Beamforming: aiming energy where the receiver actually is
- Spatial multiplexing: independent streams in the same channel

---
## The Wireless Channel Is Hostile

- The radio channel is shared, not switched
- Other devices, microwaves, and walls all radiate or absorb energy
- Signals reflect off walls and arrive multiple times (multipath)
- Strength varies with distance, orientation, and time
- A single carrier collapses under all of this; we need clever modulation

---
## Symbols, Bits, and Bandwidth

- A modem maps bits onto a continuous waveform
- One transmitted unit is a *symbol*; symbols carry one or more bits
- Higher modulation order packs more bits per symbol but needs cleaner signal
- Channel bandwidth (in Hz) sets the upper limit on symbol rate
- Wi-Fi keeps both knobs adjustable; rate adapts to channel quality

---
## Single Carrier vs Multi Carrier

- Single carrier: one big channel, one fast symbol stream
- Fast symbols are short in time, so multipath echoes overlap them
- Multi carrier: split bandwidth into many narrow subcarriers
- Each subcarrier carries a slow stream — long symbols, immune to echoes
- This is the core idea behind OFDM

---
## OFDM Overview

- OFDM = Orthogonal Frequency Division Multiplexing
- Bandwidth is divided into many evenly spaced subcarriers
- Subcarriers are *orthogonal*: their peaks land on each other's nulls
- Orthogonality lets them overlap in frequency without interfering
- Result: high spectral efficiency in a multipath environment

---
## OFDM Symbol Structure

![ofdm_symbol](svg/courses/wifi/wifi-protocols/01_underlying_ideas/ofdm_symbol.svg)

---
## OFDM in Numbers

- 802.11a/g: 64 subcarriers in 20 MHz (52 carry data)
- 802.11n/ac: up to 80 MHz channels, hundreds of subcarriers
- 802.11ax (Wi-Fi 6): 4x more subcarriers per Hz, supports OFDMA
- Each subcarrier independently picks a modulation: BPSK, QPSK, 16-QAM, 64-QAM, 256-QAM, 1024-QAM
- The strongest subcarriers carry the most bits; weak ones drop back

---
## The Cyclic Prefix

- Echoes from the previous symbol leak into the next
- OFDM prepends a short copy of the symbol's tail at its start (the cyclic prefix)
- The prefix is the "guard time" — receiver discards it
- Long enough prefix swallows all echoes and restores orthogonality
- Costs throughput in exchange for robustness

---
## OFDMA: Sharing the Subcarriers

- OFDM gives one device the whole channel for one symbol time
- OFDMA splits subcarriers across users *within* one symbol
- Tiny packets can ride a small slice of the channel without monopolizing it
- Introduced in Wi-Fi 6 (802.11ax) — borrowed from LTE
- Drastically improves efficiency in dense, low-traffic-per-client deployments

---
## What MIMO Solves

- One antenna, one symbol, one bit stream — that is SISO
- Multipath used to be the enemy
- MIMO turns multipath into an *asset* by using multiple antennas
- More antennas at both ends means more independent paths
- Each path is its own channel; we can stuff more data through them in parallel

---
## MIMO Configurations

- SISO: 1x1 — single antenna each side
- SIMO: 1xN — receiver diversity, helps reception
- MISO: Nx1 — transmitter diversity, helps reach
- MIMO: NxN — multiple antennas at both ends, multiple streams
- Notation: 4x4:2 means 4 TX, 4 RX, 2 spatial streams

---
## Spatial Multiplexing

- The transmitter splits one bit stream into N parallel streams
- Each stream goes out on its own antenna
- The receiver sees a *mixture* of the streams at every antenna
- It solves a system of equations to recover the originals
- Aggregate throughput scales roughly with the number of streams

---
## MIMO Diagram

![mimo_streams](svg/courses/wifi/wifi-protocols/01_underlying_ideas/mimo_streams.svg)

---
## Channel Estimation

- The receiver only knows what came out, not what went in
- Each frame includes known training symbols
- The receiver compares received vs known to estimate the channel matrix
- Without an accurate channel matrix, MIMO degenerates to noise
- Channel changes with motion, so estimation runs constantly

---
## Beamforming Idea

- Multiple antennas, all transmitting the same signal with deliberate phase shifts
- At the target receiver, the phases line up — signal adds constructively
- Off-axis, phases cancel — signal weakens
- Effectively *aims* a beam at one client without moving any hardware
- Improves range, throughput, and reduces interference at other devices

---
## Explicit vs Implicit Beamforming

- Explicit: the AP asks the client for channel feedback, then computes weights
- Implicit: the AP infers the channel from uplink traffic and assumes reciprocity
- 802.11ac standardized explicit beamforming and made it interoperable
- Pre-802.11ac vendor-specific beamforming was rarely used cross-vendor
- Wi-Fi 6 retains explicit beamforming

---
## Multi-User MIMO (MU-MIMO)

- Single-user MIMO: many streams to one client at a time
- MU-MIMO: streams to multiple clients *simultaneously*
- AP forms separate beams for each client, all in the same channel
- Requires lots of antennas at the AP and accurate channel knowledge
- Wi-Fi 5 added downlink MU-MIMO; Wi-Fi 6 added uplink MU-MIMO

---
## Putting It All Together

- OFDM splits the channel in *frequency* — tames multipath
- MIMO uses extra antennas in *space* — multiplies throughput
- Beamforming *steers* MIMO energy at specific clients
- OFDMA shares the channel *across users* in time-frequency tiles
- Every Wi-Fi generation since 802.11n stacks more of these on top of each other

---
## Why This Matters Up the Stack

- Throughput numbers on the box assume good radio conditions
- Real environments fall back to slower modulations and fewer streams
- Higher-layer protocols see this as variable bandwidth and latency
- Knowing the physical layer explains why TCP behaves oddly on Wi-Fi
- Embedded engineers tuning chips need this vocabulary to read datasheets
