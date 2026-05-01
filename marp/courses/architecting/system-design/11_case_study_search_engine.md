---
tags:
  - architecture:system-design
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Case Study: Search Engine

---
## What This Chapter Covers

- Requirements
- Crawler
- Indexer
- Query processing
- Ranking
- Storage and scale
- Real-time updates

---
## Requirements

- Crawl the web (or a subset)
- Index it
- Answer queries fast
- Rank results
- Billions of pages

---
## Crawler

- Fetcher: HTTP requests to URLs
- URL frontier: which URL to fetch next
- Robots.txt: respect
- Politeness: rate-limit per domain
- Distributed: many machines crawl in parallel

---
## URL Frontier

- Priority queue
- Domain-aware: avoid hammering one site
- Re-crawl high-change pages frequently
- New URLs from extracted links
- Distributed via consistent hashing

---
## Parsing And Extraction

- HTML &#8594; text
- Extract: title, body, links, metadata
- Strip ads, navigation
- Tokenisation, stemming, stopword removal

---
## Inverted Index

- Term &#8594; list of (doc id, position, frequency)
- The core search data structure
- Sharded across machines (per-term hashing)
- Compressed (delta encoding, varint)

---
## Building The Index

- MapReduce / Spark over crawled docs
- Output: term postings
- Merge across batches
- Rebuild periodically; incremental updates

---
## Query Processing

- Parse query
- Look up each term in inverted index
- Intersect / union postings
- Score and rank
- Return top-k

---
## Ranking

- TF-IDF: classic baseline
- BM25: improved
- PageRank: importance from link graph
- Modern: ML model (RankNet, LambdaMART)
- Combine many signals

---
## PageRank

- Random walk model
- High score: pages many other high-score pages link to
- Link graph: massive; iterative algorithm
- Updated periodically

---
## Storage

- Crawled HTML: object storage (S3)
- Inverted index: distributed key-value (custom)
- Document metadata: another store
- Petabytes typical

---
## Scale

- Billions of documents
- Trillions of postings
- Thousands of machines
- ~100ms query latency
- Hard problem; specialised systems

---
## Real-Time Updates

- News, social media: minutes-fresh
- Approach: separate "live" index for new docs
- Merge into main periodically
- Trade-off: complexity vs freshness

---
## Caching

- Popular queries: cache the result
- Top 1000 queries account for ~10% of volume
- Cache the postings of frequent terms
- Reduces tail latency

---
## Quality Signals

- Click-through rate
- Dwell time
- Spam classifiers
- Domain authority
- All folded into ranking

---
## Common Discussion Points

- "How do you handle freshness?" — split index, real-time updates
- "How does Google handle billions of queries?" — caching, sharding, custom hardware
- "How do you fight spam?" — classifiers + manual review
- "What about images / video?" — separate verticals; specialised indexes
- Design discussion shows depth

---
## Course Wrap-Up

- System design is asking the right questions, then making trade-offs
- Numbers matter: estimate before designing
- The same techniques recur: caching, replication, sharding, queues
- Case studies practice the synthesis
- Practice; few systems are unique; most reuse patterns
