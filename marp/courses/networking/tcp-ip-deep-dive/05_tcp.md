---
tags:
  - networking:tcp-ip
  - concepts:tcp
level: intermediate
category: networking
audience:
  - audiences:developers

---
# TCP Deep Dive

---
## What This Chapter Covers

- TCP design goals
- Three-way handshake
- Sequence numbers and acknowledgments
- Flow control and congestion control
- Connection close and TIME-WAIT

---
## TCP Design Goals

- Reliable: data arrives or you know it didn't
- Ordered: bytes arrive in order
- Connection-oriented: handshake before data
- Stream-based: not message-based
- Flow-controlled: receiver can slow sender
- Congestion-controlled: respects network capacity

---
## TCP Feature Map

![tcp_features](svg/courses/networking/tcp-ip-deep-dive/05_tcp/tcp_features.svg)

---
## When to Use TCP

- Web (HTTP)
- File transfer (FTP, SCP)
- Email (SMTP, IMAP)
- Database connections
- Anything where lost bytes matter

---
## TCP Header

```output
+----------------+----------------+
| Source Port    | Dest Port      |
+----------------+----------------+
|   Sequence Number               |
+----------------+----------------+
|   Ack Number                    |
+----------------+----------------+
| HL | Flags | Window             |
+----------------+----------------+
| Checksum       | Urgent Pointer |
+----------------+----------------+
| Options                         |
+----------------+----------------+
```

---
## Three-Way Handshake

- SYN: client sends sequence number
- SYN-ACK: server replies with its sequence number, acks client's
- ACK: client acks server's sequence number
- Connection established
- One round-trip-time (RTT) of delay before data

---
## Handshake Visualized

![tcp_handshake](svg/courses/networking/tcp-ip-deep-dive/05_tcp/tcp_handshake.svg)

---
## Sequence Numbers

- 32-bit; counts bytes, not packets
- Initial Sequence Number (ISN) randomized for security
- Each byte gets its own number
- ACK acknowledges the next expected byte
- Wraps around at 2^32

---
## Acknowledgment

- "I have received everything up to and including byte N"
- Cumulative — implicitly acks lower-numbered bytes
- Selective ACK (SACK) for non-contiguous receipt
- Receiver sends ACK on receipt
- Sender retransmits if ACK doesn't arrive

---
## Window Size

- "I can accept this many more bytes before you must wait"
- Receiver advertises window
- Sender doesn't exceed it
- Window scaling option for high-bandwidth networks
- Foundation of flow control

---
## Flow Control

- Receiver-side rate limiting
- Receiver shrinks window when full
- Sender pauses
- Receiver enlarges window when consuming
- Sender resumes

---
## Congestion Control

- Network-side rate limiting
- Different algorithms: classic, modern Cubic, modern BBR
- Slow start, congestion avoidance, fast retransmit, fast recovery
- Detects loss; backs off
- Critical to internet stability

---
## Slow Start

- Begins with a small congestion window
- Doubles the congestion window each RTT until a threshold
- Then linear growth (congestion avoidance)
- Quickly probes available bandwidth
- Backs off on loss

---
## Congestion Avoidance Visualized

![congestion-window](svg/courses/networking/tcp-ip-deep-dive/05_tcp/cwnd.svg)

---
## Fast Retransmit

- Three duplicate ACKs trigger retransmission
- Don't wait for timeout
- Used by all modern TCP stacks
- Reduces recovery time
- Built into the standard

---
## Classic Recovery

- Classic algorithm
- Halves the congestion window on loss
- Linear growth in congestion avoidance
- Fair across many flows
- Default for decades; still common

---
## TCP Cubic

- Default in Linux (and most modern OS)
- Cubic-shaped growth of the window
- Better in high-bandwidth scenarios
- Less RTT-dependent
- The most common modern algorithm

---
## TCP BBR

- Google's congestion control
- Based on bottleneck bandwidth and RTT
- Doesn't react primarily to packet loss
- Better in modern networks (cloud, mobile)
- Increasing adoption

---
## Algorithm Trade-Offs

![congestion_algorithms](svg/courses/networking/tcp-ip-deep-dive/05_tcp/congestion_algorithms.svg)

---
## Connection Close

- FIN: "I'm done sending"
- Each side sends its own FIN
- Four-way close: FIN, ACK, FIN, ACK
- Half-close possible
- Connection state: ESTABLISHED → FIN-WAIT → TIME-WAIT → CLOSED

---
## Close Sequence Visualized

![tcp_close](svg/courses/networking/tcp-ip-deep-dive/05_tcp/tcp_close.svg)

---
## TIME-WAIT State

- Sender holds the connection for 2*MSL (~60s) after close
- Catches stragglers
- Prevents reuse with stale segments
- Can pile up on busy servers
- socket reuse options mitigate

---
## RST: Reset

- Abrupt connection termination
- Sent on unexpected packets
- Common: connecting to a closed port
- Bypasses graceful FIN handshake
- Useful for forced shutdown

---
## Keepalive

- Optional periodic probes
- Detect dead peers without active traffic
- Default intervals are long (hours on Linux)
- Tune for your application
- Not a substitute for app-level health checks

---
## Nagle's Algorithm

- Buffer small writes; send when window or RTT
- Reduces per-packet overhead
- Bad for interactive apps
- Disable with TCP_NODELAY
- Most network apps disable it

---
## Selective Acknowledgments

- ACK ranges, not just cumulative
- "I got 100-200 and 300-400 but not 200-300"
- Sender retransmits exact gap
- Faster recovery from multiple losses
- Modern networks negotiate it

---
## TCP Options

- MSS: Maximum Segment Size
- SACK Permitted
- Window Scale
- Timestamps (RTT measurement)
- Negotiated in SYN/SYN-ACK

---
## Common TCP Issues

- TCP retransmissions hurt latency
- Buffer bloat: too much queueing
- Long-lived connections accumulate state
- Head-of-line blocking
- HTTP/2 mitigates some via multiplexing on one TCP

---
## Tuning TCP

- Increase send/receive buffer sizes
- Use BBR for high-bandwidth links
- Tune TIME-WAIT for high-traffic servers
- Adjust keepalive for connection longevity
- Most defaults are good for typical traffic

---
## Common Pitfalls

- Forgetting graceful close — RST in production
- TCP buffer too small for high-RTT links
- TIME-WAIT exhaustion under high churn
- Treating TCP as message-oriented
- Not understanding that delivery doesn't mean read

---
## Summary

- TCP: reliable, ordered, connection-oriented byte stream
- Three-way handshake establishes; four-way close
- Sequence + ACK numbers handle reliability
- Window for flow control; congestion window for congestion control
- Modern algorithms: Cubic and BBR; the classic algorithm is the textbook one
