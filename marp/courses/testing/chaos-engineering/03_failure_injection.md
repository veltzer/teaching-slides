---
tags:
  - testing:chaos
  - practices:reliability
level: advanced
category: testing
audience:
  - audiences:devops
  - audiences:developers

---
# Failure Injection

---
## What This Chapter Covers

- Categories of failures
- Network issues
- Resource pressure
- Application failures
- Dependency failures

---
## Failure Categories

- Network
- Resource
- Application
- Dependency
- Operational

---
## Killing Instances

- Stop a node
- Verify replacement
- Verify load redistribution
- Foundational experiment

---
## Latency Injection

- Add delay to network calls
- Reveals timeout settings
- Reveals retry behavior
- Often where bugs hide

---
## Packet Loss

- Drop a percentage of packets
- Tests TCP and timeouts
- Stresses retries
- Realistic edge case

---
## Network Partition

- Split nodes from each other
- Tests consistency choices
- Tests leader election
- Hardest to recover from

---
## CPU Pressure

- Pin cores at 100%
- Tests autoscaling
- Tests latency under load
- Tests timeout sensitivity

---
## Memory Pressure

- Allocate large blocks
- Triggers swapping or OOM
- Tests memory-aware scheduling
- Reveals leaks

---
## Disk Pressure

- Fill the disk
- Tests log rotation
- Tests fail-safe alerts
- Often surprising failures

---
## Application Failures

- Kill a process
- Throw exceptions on schedule
- Slow handlers
- Reject random requests

---
## Dependency Failures

- DB unavailable
- Cache unavailable
- Downstream API errors
- Test fallbacks

---
## Clock Skew

- Move clocks forward or back
- Catches assumptions about time
- Common cause of subtle bugs
- Especially in distributed systems

---
## Region Outage

- Drop traffic to a region
- Tests multi-region failover
- Big-blast-radius experiment
- Run rarely, prepare thoroughly

---
## Tools

- Open source platforms
- Cloud-provider chaos services
- Custom scripts
- Pick by environment

---
## Common Injection Mistakes

- Killing without observing
- One-shot, no repeat
- No partial outages
- No clock-related tests
- No dependency mocks for safe runs
