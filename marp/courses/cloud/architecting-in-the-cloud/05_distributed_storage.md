---
tags:
  - infrastructure:cloud
  - infrastructure:storage
  - concepts:architecture
level: intermediate
category: cloud
audience:
  - audiences:developers
  - audiences:architects
  - audiences:devops

---
# Distributed Storage

---

## Cloud Storage Overview
- Storage as a service, not a disk to manage
- Object storage: the cloud-native default
- Virtually unlimited capacity
- Built-in redundancy and durability
- Accessible via HTTP APIs

---

## What Do You Get?
- Object storage: S3, Blob Storage, Cloud Storage
- 11 nines of durability (99.999999999%)
- Data replicated across multiple facilities
- Versioning and lifecycle management
- Global accessibility via HTTP/HTTPS

---

## How is it Different from a Disk?
- Not a file system (no directories, no POSIX)
- Objects accessed by key, not path
- No in-place updates (write full object)
- Higher latency than local disk
- Massively parallel access

---

## Object Storage Architecture
- Flat namespace with key-based access
- Metadata attached to each object
- Eventual consistency for some operations (mostly consistent now)
- Partitioned across many storage nodes
- Designed for massive scale

---

## How Costly Is It?
- Storage: $0.02-0.03/GB/month (standard tier)
- Requests: $0.005 per 1000 GET, $0.05 per 1000 PUT
- Data transfer out: $0.09/GB (first 10 TB)
- Inbound data: free
- Much cheaper than block storage or file storage

---

## Cost Optimization for Storage
- Use lifecycle policies to move data to cheaper tiers
- Standard -> Infrequent Access -> Glacier
- Delete old versions and expired objects
- Analyze access patterns before choosing tier
- S3 Intelligent-Tiering automates tier selection

---

## Storage Tiers
- Hot: frequently accessed, highest cost
- Warm: infrequent access, lower cost
- Cold: archive, very low cost, retrieval time
- Deep archive: lowest cost, hours to retrieve
- Match tier to access pattern

---

## Durability vs Availability
- Durability: probability data won't be lost (11 nines)
- Availability: probability you can access data (99.99%)
- High durability doesn't mean always accessible
- Outages are temporary; data loss is permanent
- Design for both

---

## Types of Durability
- Single-AZ: data in one data center (risk of facility failure)
- Multi-AZ: data replicated across AZs (standard)
- Cross-Region: data replicated across Regions (highest)
- Choose based on criticality and cost tolerance
- Most workloads: multi-AZ is sufficient

---

## Object Storage Use Cases
- Static website hosting
- Data lake and analytics
- Application assets (images, videos, documents)
- Backup and disaster recovery
- Log storage and archival

---

## Object Storage Patterns
- Direct upload: client uploads directly to storage (signed URLs)
- CDN origin: serve content globally via edge caching
- Event-driven: trigger processing on upload (Lambda, Functions)
- Data lake: store raw data, query with SQL (Athena, BigQuery)
- Backup target: automated backups from databases and VMs

---

## Cross-Region Replication
- Replicate objects to another Region
- Compliance, latency, and DR use cases
- Asynchronous replication
- Requires versioning enabled
- Adds storage and transfer costs

---

## Data Lakes on Object Storage
- Store raw data in any format
- Schema on read (not schema on write)
- Query with Athena, BigQuery, Presto
- Separate storage from compute
- Cheapest storage for massive datasets

---

## Lifecycle Policies
- Automatically transition objects between tiers
- Delete expired objects
- Example: Standard -> IA after 30 days -> Glacier after 90
- Reduce costs without manual intervention
- Apply per bucket or per prefix

---

## Multi-Part Upload
- Required for objects > 5 GB
- Recommended for objects > 100 MB
- Upload parts in parallel
- Resume after failure (only re-upload failed parts)
- Better throughput for large files

---

## Transfer Acceleration
- Use CloudFront edge locations for uploads
- Faster long-distance transfers
- Especially useful for global users
- Additional per-GB cost
- Enable per bucket when needed

---

## Security for Object Storage
- Bucket policies and IAM policies
- Block Public Access (enable by default)
- Server-side encryption (SSE)
- Access logging
- Object Lock for compliance (WORM)

---

## Object Storage Best Practices
- Enable versioning for critical data
- Use lifecycle policies from day one
- Block public access unless explicitly needed
- Encrypt everything
- Monitor access patterns and costs
- Use multi-part upload for large files

---

## S3 Select and Glacier Select
- Query data in S3 without downloading entire object
- SQL-like expressions on CSV, JSON, Parquet
- Reduce data transfer costs
- Faster than downloading and processing locally
- Works even on Glacier (with retrieval delay)

---

## Object Storage Consistency
- S3 provides strong read-after-write consistency
- PUT -> immediately readable with latest data
- DELETE -> immediately reflected
- LIST -> immediately consistent
- No more eventual consistency concerns (since Dec 2020)

---

## Comparing Storage Costs
- S3 Standard: ~$0.023/GB/month
- S3 IA: ~$0.0125/GB/month
- S3 Glacier: ~$0.004/GB/month
- EBS gp3: ~$0.08/GB/month
- EFS: ~$0.30/GB/month
- Choose based on access pattern, not just price

---

## Block Storage in Detail
- EBS: network-attached, persistent, per-instance
- Instance Store: local NVMe, ephemeral, highest performance
- EBS snapshots for backup and migration
- Encryption at rest with KMS
- Choose volume type based on IOPS requirements

---

## File Storage in the Cloud
- EFS: managed NFS, multi-instance shared access
- FSx for Windows: SMB protocol, Active Directory
- FSx for Lustre: HPC, high throughput
- Shared file access for legacy applications
- More expensive than S3, necessary for specific workloads

---

## When Object Storage Is Not Enough
- Need POSIX file system semantics: use EFS/FSx
- Need low-latency block access: use EBS
- Need shared file access: use managed file systems
- Need database-like queries: use a database
- Object storage is the default, not the only option
