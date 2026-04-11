---
tags:
  - infrastructure:cloud
  - infrastructure:aws
  - infrastructure:storage
level: beginner
category: cloud
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:managers

---
# Core Storage Services

---

## AWS Storage Options
- Object storage (S3)
- Block storage (EBS)
- File storage (EFS, FSx)
- Archival storage (Glacier)
- Each designed for different use cases

---

## Storage Types Compared
- Object: files accessed by key, web-scale
- Block: low-latency, attached to single instance
- File: shared file system, NFS/SMB
- Archive: infrequent access, low cost
- Choose based on access pattern and performance

---

## Amazon S3 Overview
- Simple Storage Service
- Object storage with unlimited capacity
- 99.999999999% (11 nines) durability
- Accessible via HTTP/HTTPS
- Foundation service for many AWS architectures

---

## S3 Key Concepts
- Buckets: containers for objects
- Objects: files + metadata (up to 5 TB each)
- Keys: unique identifier within a bucket
- Versioning: keep multiple versions of objects
- Globally unique bucket names

---

## S3 Operations
- PUT: upload objects
- GET: retrieve objects
- DELETE: remove objects
- LIST: enumerate objects in a bucket
- Multipart upload for large files (>100 MB)

---

## S3 Storage Classes
- S3 Standard: frequent access, low latency
- S3 Intelligent-Tiering: auto-moves between tiers
- S3 Standard-IA: infrequent access, lower cost
- S3 One Zone-IA: single AZ, even lower cost
- S3 Glacier: archive, minutes to hours retrieval
- S3 Glacier Deep Archive: lowest cost, 12-hour retrieval

---

## S3 Storage Class Selection
- How often is the data accessed?
- How quickly must it be retrieved?
- How critical is multi-AZ redundancy?
- What is the acceptable cost?
- Lifecycle policies automate transitions

---

## S3 Lifecycle Policies
- Automatically transition objects between classes
- Example: Standard -> IA after 30 days -> Glacier after 90 days
- Delete objects after a set period
- Apply to entire bucket or specific prefixes
- Reduce costs without manual effort

---

## S3 Security
- Bucket policies (resource-based, JSON)
- IAM policies (identity-based)
- Block Public Access settings (account or bucket level)
- Server-side encryption (SSE-S3, SSE-KMS, SSE-C)
- Client-side encryption

---

## S3 Versioning
- Keep all versions of an object
- Protect against accidental deletes
- Delete marker instead of permanent removal
- Restore previous versions
- Increases storage costs (all versions stored)

---

## S3 Replication
- Cross-Region Replication (CRR): compliance, latency
- Same-Region Replication (SRR): aggregation, compliance
- Requires versioning on both buckets
- Replicated asynchronously
- Not retroactive (only new objects)

---

## S3 Event Notifications
- Trigger actions on object events
- New object created, deleted, etc.
- Targets: Lambda, SQS, SNS
- Build event-driven architectures
- Example: resize images on upload

---

## S3 Use Cases
- Static website hosting
- Data lake foundation
- Backup and disaster recovery
- Application asset storage
- Log storage and analytics

---

## S3 Performance
- 3,500 PUT and 5,500 GET requests per second per prefix
- Multipart upload for large objects
- S3 Transfer Acceleration: fast long-distance transfers
- Byte-range fetches for partial downloads
- Use prefixes to distribute load

---

## Amazon EBS Overview
- Elastic Block Store
- Persistent block-level storage for EC2
- Like a virtual hard drive
- Automatically replicated within its AZ
- Snapshots for backup to S3

---

## EBS Volume Types
- gp3: General Purpose SSD (baseline 3,000 IOPS)
- gp2: General Purpose SSD (burst to 3,000 IOPS)
- io2: Provisioned IOPS SSD (up to 64,000 IOPS)
- st1: Throughput Optimized HDD (big data)
- sc1: Cold HDD (infrequent access)

---

## Choosing an EBS Volume Type
- gp3: most workloads (default choice)
- io2: databases needing consistent high IOPS
- st1: sequential large reads (data warehousing)
- sc1: infrequent access, lowest cost
- Match IOPS and throughput to workload

---

## EBS Snapshots
- Point-in-time backup of EBS volumes
- Stored incrementally in S3
- Can create new volumes from snapshots
- Copy snapshots across Regions
- Automate with Data Lifecycle Manager

---

## EBS Encryption
- Encrypt volumes and snapshots at rest
- Uses AWS KMS keys
- Encryption at rest, in transit, and snapshots
- Minimal impact on latency
- Snapshots from encrypted volumes are encrypted

---

## Amazon EFS Overview
- Elastic File System
- Fully managed NFS file system
- Shared access across multiple EC2 instances
- Automatically grows and shrinks
- Regional service (multi-AZ by default)

---

## EFS Performance Modes
- General Purpose: low latency (web serving, CMS)
- Max I/O: higher throughput, slightly higher latency
- Elastic throughput: auto-scales with workload
- Provisioned throughput: specify throughput needed
- Choose based on workload characteristics

---

## EFS Storage Classes
- Standard: frequently accessed files
- Infrequent Access (IA): lower cost for rare access
- Lifecycle management moves files automatically
- One Zone variants for cost savings
- Significant savings with IA tiering

---

## Amazon FSx
- Fully managed third-party file systems
- FSx for Windows File Server: SMB protocol, Active Directory
- FSx for Lustre: high-performance computing
- FSx for NetApp ONTAP: multi-protocol
- FSx for OpenZFS: Linux workloads

---

## Amazon S3 Glacier
- Long-term archive storage
- Very low cost per GB
- Expedited retrieval: 1-5 minutes
- Standard retrieval: 3-5 hours
- Bulk retrieval: 5-12 hours

---

## Glacier Deep Archive
- Lowest cost storage in AWS
- 12-hour standard retrieval
- 48-hour bulk retrieval
- Designed for data accessed once or twice a year
- Regulatory and compliance archives

---

## Glacier Vault Lock
- WORM (Write Once Read Many) compliance
- Immutable policy once locked
- Time-based retention rules
- SEC, FINRA, HIPAA compliance
- Cannot be changed after locking

---

## Choosing the Right Storage
- S3: unstructured data, web content, backups
- EBS: databases, boot volumes, low-latency apps
- EFS: shared file access, content management
- FSx: Windows or HPC file systems
- Glacier: compliance archives, long-term backup
