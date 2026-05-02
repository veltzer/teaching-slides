---
tags:
  - architecture:system-design
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Case Study: News Feed

---
## Feed Design

![feed_design](svg/courses/architecting/system-design/10_case_study_news_feed/feed_design.svg)

---
## What This Chapter Covers

- Requirements
- Push vs pull (fan-out)
- Hybrid model
- Storage
- Ranking
- Caching
- Scale

---
## Requirements

- Users post; followers see in feed
- Real-time-ish (within seconds)
- Personalised ordering
- Infinite scroll
- 1B users

---
## Two Approaches

- **Push (fan-out on write)**: post to feed of every follower at write time
- **Pull (fan-out on read)**: collect from following at read time
- Trade-offs for each

---
## Push Model

- User A posts &#8594; insert into feed table for each follower
- Read: just fetch feed
- Write-heavy; expensive for celebrities (millions of followers)
- Best for: low-celebrity, high-read

---
## Pull Model

- Read time: query "what did all my followings post recently?"
- Light writes; expensive reads (esp. for active users)
- Best for: highly-active accounts, fewer reads

---
## Hybrid

- Default: push
- Celebrity (>10K followers): pull
- Best of both
- Used by Twitter, Instagram

---
## Storage

- Posts: write-once; partition by user
- Feed cache: per-user; sorted by time
- Cassandra / DynamoDB common
- Hot users: in-memory (Redis)

---
## Feed Generation

- Active users: precomputed (Redis)
- Inactive: rebuild on next visit
- TTL: 7-30 days; expire idle users

---
## Ranking

- Chronological: simplest
- Algorithmic: ML model; engagement
- Mixed: chronological + boost for high-engagement
- The hard, valuable part

---
## Ranking Inputs

- Recency
- Engagement (likes, comments)
- Affinity (close friends rank higher)
- Topic match
- Time of day
- Combine: ML model

---
## Caching

- Top-of-feed: in-memory
- Older: paginate from store
- Per-user cache; invalidate on post
- Hit rate critical

---
## Real-Time Updates

- WebSocket / SSE: push new posts to active clients
- Or: client polls every N seconds
- Match to user expectation

---
## Scale

- 1B users * 100 reads/day = 100B feed reads/day
- ~1.2M reads/sec average; peak 5x
- Caching essential
- Fan-out pipeline: massive Kafka deployment

---
## Failure Modes

- Cache miss storm: gradual warm-up
- Hot user: replicas, throttling
- Backend slow: serve stale feed
- Most failures: degrade to "good enough"

---
## Cost Considerations

- Storage: petabytes for posts + feeds
- Compute: ranking is expensive
- Bandwidth: serving images / video
- Can be the biggest spend at scale

---
## Common Discussion Points

- "How do celebrities work?" — pull on read; cache aggressively
- "How does Instagram do it?" — published architecture; hybrid
- "What about ranking?" — feedback loop; A/B testing
- "How do you handle deletes?" — tombstones; eventual consistency
- Demonstrate the trade-off thinking
