---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---

# Backup and Recovery

---

## What This Chapter Covers

- The snapshot and restore model and its `_snapshot` APIs
- Repository configuration for fs, S3, GCS, and Azure
- Snapshot lifecycle management with SLM policies
- How Elasticsearch snapshots are incremental
- Searchable snapshots for cold and frozen tiers
- Disaster recovery planning and cross-cluster restore
- Point-in-time recovery considerations

---

## Why Snapshots, Not File Copies

- Copying data directories of a live cluster corrupts backups
- Snapshots are the only supported backup mechanism
- They are consistent, incremental, and restorable per index
- Snapshots live in a registered repository, not on data nodes
- Restore can target the same or a different cluster

---

## Snapshot Repositories

- A repository is the storage backend for snapshots
- Must be registered before any snapshot can be taken
- A shared repository must be reachable by all data + master nodes
- Supported types: `fs`, `s3`, `gcs`, `azure`, `url` (read-only)
- Object-store repos need the matching repository plugin/credentials

```bash
GET _snapshot
GET _snapshot/my_repo/_verify
```

---

## Registering a Shared Filesystem Repository

- The `fs` type uses a network share mounted on every node
- The mount path must be listed in `path.repo` on all nodes
- All nodes must see the identical path for it to work

```yaml
path.repo: ["/mnt/es_backups"]
```

```bash
PUT _snapshot/my_repo
{
  "type": "fs",
  "settings": { "location": "/mnt/es_backups", "compress": true }
}
```

---

## Registering an S3 Repository

- The `repository-s3` integration stores snapshots in a bucket
- Credentials go in the secure keystore, not the config file
- Supports server-side encryption and storage classes

```bash
bin/elasticsearch-keystore add s3.client.default.access_key
bin/elasticsearch-keystore add s3.client.default.secret_key
```

```bash
PUT _snapshot/s3_repo
{
  "type": "s3",
  "settings": { "bucket": "es-snapshots", "region": "us-east-1" }
}
```

---

## GCS and Azure Repositories

- GCS uses the `gcs` type with a service-account credential
- Azure uses the `azure` type with a storage account key/SAS
- Both store credentials in the keystore like S3
- Choose the repo matching your cloud provider for locality/cost

```bash
PUT _snapshot/gcs_repo
{
  "type": "gcs",
  "settings": { "bucket": "es-snapshots", "client": "default" }
}
```

---

## Creating a Snapshot

- Snapshots can cover the whole cluster or selected indices
- Include global state to capture templates and settings
- `wait_for_completion=true` blocks until done (use for scripts)

```bash
PUT _snapshot/my_repo/snap_2026_06_14?wait_for_completion=true
{
  "indices": "logs-*,metrics-*",
  "include_global_state": true,
  "metadata": { "taken_by": "ops", "reason": "nightly" }
}
```

---

## Monitoring Snapshot Progress

- List snapshots and inspect their state in the repository
- `_status` shows per-shard progress for in-flight snapshots
- States: `IN_PROGRESS`, `SUCCESS`, `PARTIAL`, `FAILED`

```bash
GET _snapshot/my_repo/snap_2026_06_14
GET _snapshot/my_repo/_current
GET _snapshot/my_repo/snap_2026_06_14/_status
```

---

## How Snapshots Are Incremental

- Snapshots operate at the Lucene segment level
- A new snapshot only copies segments not already in the repo
- Unchanged segments are referenced, not re-uploaded
- This makes frequent snapshots cheap in space and time
- Deleting a snapshot only removes segments no other snapshot needs
- Never manually delete files in the repository — use the API

---

## Restoring a Snapshot

- Close or delete the target index first, or rename on restore
- Use `rename_pattern`/`rename_replacement` to restore side-by-side
- You can restore a subset of indices from a snapshot

```bash
POST _snapshot/my_repo/snap_2026_06_14/_restore
{
  "indices": "logs-2026.06.13",
  "rename_pattern": "logs-(.+)",
  "rename_replacement": "restored-logs-$1",
  "include_global_state": false
}
```

---

## Snapshot Lifecycle Management (SLM)

- SLM automates taking and retaining snapshots on a schedule
- A policy defines schedule, repo, name pattern, and config
- Retention prunes old snapshots by age and count
- Manage and monitor SLM through dedicated APIs

```bash
PUT _slm/policy/nightly-snapshots
{
  "schedule": "0 30 1 * * ?",
  "name": "<nightly-{now/d}>",
  "repository": "my_repo",
  "config": { "indices": "*", "include_global_state": true },
  "retention": { "expire_after": "30d", "min_count": 5, "max_count": 50 }
}
```

---

## Managing SLM Policies

- Trigger a policy manually to test it end to end
- Inspect execution history and the next scheduled run
- The retention task runs separately and can be forced

```bash
POST _slm/policy/nightly-snapshots/_execute
GET _slm/policy/nightly-snapshots
POST _slm/_execute_retention
GET _slm/stats
```

---

## Searchable Snapshots

- Mount a snapshot as a searchable index without full restore
- Data stays in the repository; nodes cache what is queried
- Powers the cold and frozen data tiers cheaply
- Cold tier: full copy on local disk for resilience
- Frozen tier: shared cache, minimal local storage

```bash
POST _snapshot/my_repo/snap_2026_06_14/_mount?storage=shared_cache
{
  "index": "logs-2026.05",
  "renamed_index": "frozen-logs-2026.05"
}
```

---

## Disaster Recovery Planning

- Define RPO (data loss tolerance) and RTO (recovery time)
- Store snapshots in a region/provider separate from the cluster
- Test restores regularly — an untested backup is not a backup
- Snapshot cluster settings/templates via `include_global_state`
- Document the full recovery runbook and access credentials
- Keep the repository immutable/versioned to resist tampering

---

## Cross-Cluster Restore

- Register the same repository (read-only) on a second cluster
- Restore snapshots taken by the primary into the DR cluster
- Target version must be compatible (one major version back)
- Use renaming to avoid clashes with existing indices
- Combine with CCR for near-real-time replication if needed

```bash
PUT _snapshot/my_repo
{ "type": "s3", "settings": { "bucket": "es-snapshots", "readonly": true } }
```

---

## Point-in-Time Recovery Considerations

- ES has no continuous WAL-style PITR like an RDBMS
- The translog provides durability between refresh/flush, not history
- Recovery granularity equals your snapshot frequency
- Tighten RPO by increasing SLM frequency (incremental keeps it cheap)
- For low RPO, pair snapshots with cross-cluster replication

---

## Backup Operations Best Practices

- Automate everything with SLM; alert on policy failures
- Verify the repository periodically with `_verify`
- Keep snapshots off the production storage and region
- Monitor repository size growth and prune via retention
- Rehearse full and partial restores into a staging cluster
- Capture global state so templates and ILM policies are restorable

---

## Chapter Summary

- Snapshots are the only supported, consistent backup method
- Register fs/S3/GCS/Azure repositories before snapshotting
- Snapshots are incremental at the segment level — cheap and fast
- SLM automates scheduling and retention of snapshots
- Searchable snapshots back the cold and frozen tiers
- DR planning needs off-site repos, cross-cluster restore, and tested runbooks
