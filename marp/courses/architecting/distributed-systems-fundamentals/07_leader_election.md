---
tags:
  - concepts:leader-election
level: intermediate
category: architecture
audience:
  - audiences:developers

---

# Leader Election

---

## What This Chapter Covers

- Why leaders
- Election algorithms
- Bully algorithm
- Ring algorithm
- Raft leader election
- Detection and re-election
- Practical considerations

---

## Why Leaders

- Centralised decisions: simpler than fully distributed
- One node coordinates; others follow
- Used for: writes-must-be-ordered, replication, locks
- Scales worse than peer-to-peer; simpler to reason about
- Most distributed systems have a leader somewhere

---

## Election Approaches

![election_methods](svg/courses/architecting/distributed-systems-fundamentals/07_leader_election/election_methods.svg)

---

## Handling Leader Failure

![leader_failure](svg/courses/architecting/distributed-systems-fundamentals/07_leader_election/leader_failure.svg)

---

## When You Need One

- Replication: leader takes writes; followers copy
- Locks / mutual exclusion: leader grants
- Aggregation: leader collates results
- Coordination: leader assigns work
- Consensus algorithms: usually need a leader

---

## When You Don't

- Symmetric peer-to-peer (BitTorrent, Cassandra reads)
- CRDT-based systems: no coordination needed
- Stateless services
- "Leader for everything" is overkill

---

## Bully Algorithm

- Each node has an ID
- Highest ID becomes leader
- When a node thinks the leader is dead: starts election
- Sends "election" to higher-ID nodes
- If none respond: declares itself leader
- Garcia-Molina, 1982

---

## Ring Algorithm

- Nodes arranged in a logical ring
- Election message passes around the ring
- Each node adds its ID
- Highest ID becomes leader
- Slower than bully but less network chatter

---

## Raft Leader Election

- Each follower has a random election timeout
- On timeout: become candidate; request votes
- Win majority &#8594; leader
- Heartbeats from leader suppress new elections
- Modern, used in etcd, Consul, CockroachDB

---

## Why Random Timeouts

- Without randomness: tied elections
- With randomness: one candidate wins each round
- Range: 150-300ms typical
- Tunable based on network conditions
- Critical for liveness

---

## Failure Detection

- How do you know the leader is dead?
- Heartbeats: leader sends "I'm alive"
- Followers expect them within a timeout
- Tune timeout: short = false positives; long = slow detection
- 1-3 seconds typical for cross-DC

---

## False Positives

- Slow leader looks dead
- New election starts
- Old leader comes back to find a new leader exists
- Old leader steps down
- Disruption; mitigate with longer timeouts and proper heartbeats

---

## Split Brain

- Network partition
- Two leaders elected (one per side)
- Both accept writes
- Reconcile when partition heals: data conflicts
- Quorum requirement prevents this in proper consensus

---

## Quorum For Leader Election

- Leader requires majority votes
- Minority can't elect a leader
- Even with split brain, only one side has a leader
- The other side's writes blocked
- The CP choice in CAP

---

## Lease-Based Leadership

- Leader holds a "lease" for N seconds
- Lease auto-expires unless renewed
- If leader crashes, lease expires; new leader can take over
- Avoids: dual-leader after partition heals
- Used in Chubby, etcd

---

## Re-Election Cost

- All operations pause during election
- Hundreds of milliseconds typical
- Application: brief unavailability
- Tune timeouts to balance: detect-quickly vs avoid-flapping
- Test under realistic network conditions

---

## Stateful Leaders

- Leader has state followers don't
- New leader must catch up before serving
- Catch-up time: log replay from followers
- Bigger logs &#8594; longer catch-up &#8594; longer unavailability
- Trim logs / snapshot regularly

---

## Common Leader Election Mistakes

- No randomness in timeouts &#8594; election livelock
- Tight timeouts &#8594; constant re-elections
- Loose timeouts &#8594; slow failure detection
- Even number of nodes &#8594; possible tie
- Not testing failover under load
