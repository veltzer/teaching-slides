---
tags:
  - databases:neo4j
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:dba

---
# Operations and Algorithms

---
## What This Chapter Covers

- Causal Cluster
- Backups
- Monitoring
- Graph Data Science
- Use cases

---
## Causal Cluster

- Core servers handle writes
- Read replicas scale reads
- Raft for consensus on cores
- Survives core minority loss

---
## Topology

- Three or five core servers
- Many read replicas
- Multi-region possible
- Plan for region survival

---
## Backups

- Online backup against replicas
- Off-host storage
- Test restores
- Daily for production

---
## Restore

- Stop a node
- Restore from backup
- Bring back into cluster
- Or restore to a fresh cluster

---
## Monitoring Metrics

- Page cache hit ratio
- Transactions per second
- Heap usage
- Query latency

---
## Alerts

- Cluster member down
- Replica lag
- Disk near full
- Query timeouts

---
## Graph Data Science

- Built-in algorithms library
- Path finding, centrality, community
- Embeddings and link prediction
- Run as procedures

---
## Centrality

- Page-rank, between-ness, closeness
- Identify important nodes
- Good for fraud and influence
- Tune precision and runtime

---
## Community Detection

- Modularity-based clustering, label propagation
- Group similar nodes
- Useful for clustering customers
- Watch for memory cost

---
## Path Algorithms

- Shortest path
- All shortest paths
- A* with heuristics
- Useful for routing

---
## Link Prediction

- Train on existing relationships
- Predict missing edges
- Useful for recommendations
- Validate against held-out data

---
## Embeddings

- node2vec and similar
- Vector representation
- Plug into ML pipelines
- Bridge graph and ML worlds

---
## Use Cases

- Recommendations
- Fraud rings
- Knowledge graphs
- Identity resolution

---
## Common Operational Mistakes

- One node in production
- No backup verification
- Wrong page cache size
- Algorithms run on hot transactional cluster
- No GDS pipeline checkpoints
