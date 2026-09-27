---
tags:
  - infrastructure:linux
  - security:forensics
  - security:security
level: advanced
category: security
audience:
  - audiences:security-professionals

---

# Anti-Forensics and Countermeasures

## Course: Linux Forensics - Day 4 (continued)
- Attackers actively try to destroy, hide, or falsify evidence
- Recognizing anti-forensics is what separates a thorough investigation
- This module covers detecting tampering and where hidden data lives
- Every technique leaves traces; the investigator's job is to find them

---

## The Anti-Forensics Mindset

- Destruction: wiping files, logs, and history
- Hiding: concealing data in places tools overlook
- Falsification: forging timestamps and log entries to mislead
- Counter-strategy: verify with independent sources, never one artifact

```output
Single artifact:   .bash_history shows a clean, ordinary session
Cross-checked:     auth.log, audit.log, and utmp disagree with it
Conclusion:        the history was edited; trust the harder-to-forge sources
```

- The most forgeable artifacts are the ones the attacker controls directly

---

## Timestamp Manipulation (Timestomping)

- `touch` and `debugfs` can backdate a file's MAC times to blend in
- ext4 inodes hold four timestamps: mtime, atime, ctime, and crtime
- `ctime` (inode change time) is not settable by `touch`: a key tell

```bash
# All four ext4 timestamps for an inode
debugfs -R "stat <12345>" /dev/sdb1

# stat shows the user-facing three
stat suspicious_binary
```

- When mtime is older than ctime, the file was touched after creation
- crtime older than the filesystem, or in the future, signals tampering
- Compare a file's times against neighbors installed in the same package

---

## Detecting Timestomping at Scale

```bash
# Files whose modify time predates their change time (classic stomp)
find /mnt/evidence -type f -printf '%T@ %C@ %p\n' \
  | awk '$1 < $2 - 60 { print }'

# Binaries in system paths newer than the package that owns them
find /mnt/evidence/usr/bin -type f -newermt "2026-01-01" -ls

# Cross-check package files against recorded metadata
dpkg --verify 2>/dev/null | grep -v '^..5'
```

- Package databases record the expected size and hash of every system file
- A binary whose hash differs from its package is tampered, whatever its date
- Timeline analysis exposes stomping as a break in otherwise ordered activity

---

## Log Tampering

- Attackers truncate, edit, or selectively delete log lines
- Gaps, resets, and out-of-order timestamps betray edited text logs
- `journald` binary logs carry a checksum chain that detects edits

```bash
# journald verifies its own sealed log integrity
journalctl --verify

# Hunt for suspicious gaps in auth.log timestamps
awk '{print $1, $2, $3}' /mnt/evidence/var/log/auth.log | uniq -c

# Wtmp/utmp login records that text logs may contradict
last -f /mnt/evidence/var/log/wtmp
```

- A `journalctl --verify` failure is direct evidence of log tampering
- Correlate text logs against binary `wtmp` and `audit.log` for the truth

---

## Hidden Storage Locations

- `/dev/shm` and `tmpfs` mounts hold data in RAM, gone on reboot
- Deleted-but-open files live on until the holding process exits
- Slack space and unallocated blocks retain fragments of old data

```bash
# In-memory filesystems attackers favor for staging
mount | grep -E "tmpfs|/dev/shm"
ls -la /dev/shm /run

# Recover a deleted file still held open by a running process
ls -l /proc/*/fd/ 2>/dev/null | grep deleted

# File slack and unallocated space with Sleuth Kit
blkls -s /evidence/disk.dd > /evidence/slack.raw
strings /evidence/slack.raw | less
```

---

## Secure Deletion and Its Traces

- Tools like `shred` and `wipe` overwrite file content to defeat recovery
- Overwriting hides content but leaves metadata and side effects behind
- Journaling, backups, and SSD wear-leveling often keep stale copies

```bash
# Directory entries and inodes may survive a content wipe
debugfs -R "ls -d /home/suspect" /dev/sdb1

# The ext4 journal can hold pre-wipe versions of blocks
debugfs -R "logdump" /dev/sdb1 | less
```

- Absence of expected files is itself evidence worth documenting
- On SSDs, TRIM and remapping mean a wipe rarely reaches every copy

---

## Detecting a Rootkit-Modified Image

- Compare the seized kernel and modules against known-good vendor hashes
- A tainted kernel log or unsigned module points to on-disk tampering
- Pair on-disk checks with the memory-side hook detection from earlier

```bash
# Hash on-disk modules against a trusted reference set
find /mnt/evidence/lib/modules -name '*.ko' -exec sha256sum {} \; \
  > /evidence/module_hashes.txt

# Persistence points a kernel implant loads from
cat /mnt/evidence/etc/modules-load.d/*.conf
cat /mnt/evidence/etc/modprobe.d/*.conf
```

- A module present on disk but absent from the vendor set is suspect
- Follow the persistence entry to prove how the implant survives reboot

---

## Exercise: Anti-Forensics Detection

Investigate the provided image for signs of tampering.

Deliverables:
1. 1. Files with inconsistent timestamps, with the evidence for each
1. 1. The result of log-integrity verification and any gaps found
1. 1. Any data recovered from hidden or in-memory storage locations
1. 1. A short note on which artifacts you trusted, and why
