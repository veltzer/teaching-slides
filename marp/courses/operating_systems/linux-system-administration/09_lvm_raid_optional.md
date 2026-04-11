---
tags:
  - infrastructure:linux
  - audiences:sysadmin
level: intermediate
category: operating-systems
audience:
  - audiences:sysadmins
  - audiences:devops

---
# LVM and RAID (Optional)
## Logical Volume Management and RAID Configuration

---

## LVM Architecture

![lvm_architecture](svg/courses/operating_systems/linux-system-administration/09_lvm_raid_optional/lvm_architecture.svg)

---

## LVM Architecture

Three layers:
- **PV** (Physical Volumes) - actual disks/partitions
- **VG** (Volume Groups) - pool of PVs
- **LV** (Logical Volumes) - usable volumes from VG

---
## Why Use LVM?

Advantages over raw partitions:
- Resize volumes without downtime
- Span volumes across multiple disks
- Create point-in-time snapshots
- Move data between disks online
- Thin provisioning (over-commit storage)
- Striping for performance
- Mirroring for redundancy

When NOT to use LVM:
- Simple single-disk systems
- When raw performance is critical (minimal overhead)
- Boot partitions (use regular partitions)

---
## Creating LVM Volumes

```bash
# Create physical volumes
pvcreate /dev/sdb1 /dev/sdc1

# Create volume group
vgcreate data-vg /dev/sdb1 /dev/sdc1

# Create logical volumes
lvcreate -L 50G -n home-lv data-vg
lvcreate -l 100%FREE -n data-lv data-vg

# Create filesystem and mount
mkfs.ext4 /dev/data-vg/home-lv
mount /dev/data-vg/home-lv /home

# View status
pvdisplay
vgdisplay
lvdisplay
```

---
## LVM Display Commands

```bash
# Compact status views
pvs              # physical volumes summary
vgs              # volume groups summary
lvs              # logical volumes summary

# Detailed views
pvdisplay /dev/sdb1
vgdisplay data-vg
lvdisplay /dev/data-vg/home-lv

# Custom output columns
lvs -o +devices,seg_size
pvs -o +pv_used,pv_free

# Show LV path mapping
lvdisplay --maps /dev/data-vg/home-lv

# Show physical extent allocation
pvdisplay --maps /dev/sdb1
```

---
## Extending and Reducing LVM

```bash
# Add new disk to VG
pvcreate /dev/sdd1
vgextend data-vg /dev/sdd1

# Extend LV
lvextend -L +20G /dev/data-vg/home-lv
# Resize filesystem
resize2fs /dev/data-vg/home-lv      # ext4
xfs_growfs /home                      # xfs

# Or extend + resize in one step
lvextend -L +20G -r /dev/data-vg/home-lv

# Reduce LV (ext4 only, NOT xfs)
umount /home
e2fsck -f /dev/data-vg/home-lv
resize2fs /dev/data-vg/home-lv 30G
lvreduce -L 30G /dev/data-vg/home-lv
mount /home
```

---
## LVM: Moving Data Between Disks

```bash
# Move all data off a physical volume
pvmove /dev/sdb1

# Move to a specific PV
pvmove /dev/sdb1 /dev/sdd1

# Remove PV from VG (after pvmove)
vgreduce data-vg /dev/sdb1
pvremove /dev/sdb1

# Rename volume group
vgrename data-vg storage-vg

# Rename logical volume
lvrename data-vg home-lv home-data-lv
```

This allows online disk replacement without downtime.

---
## LVM Snapshots

```bash
# Create snapshot
lvcreate -L 5G -s -n home-snap \
  /dev/data-vg/home-lv

# Mount snapshot (read-only)
mount -o ro /dev/data-vg/home-snap /mnt/snap

# Restore from snapshot
lvconvert --merge /dev/data-vg/home-snap

# Remove snapshot
lvremove /dev/data-vg/home-snap
```

Use cases:
- Pre-upgrade backups
- Consistent backup of running system
- Testing changes safely

---
## LVM Thin Provisioning

```bash
# Create thin pool
lvcreate -L 100G --thinpool thin-pool data-vg

# Create thin volumes (can over-commit)
lvcreate -V 50G --thin -n vm1 data-vg/thin-pool
lvcreate -V 50G --thin -n vm2 data-vg/thin-pool
lvcreate -V 50G --thin -n vm3 data-vg/thin-pool
# Total: 150G allocated from 100G pool

# Monitor thin pool usage
lvs -o +data_percent,metadata_percent data-vg/thin-pool

# Extend thin pool when needed
lvextend -L +50G data-vg/thin-pool
```

Thin provisioning is ideal for VM storage and test environments.

---
## LVM Striping and Mirroring

```bash
# Create striped LV (performance)
lvcreate -L 100G -n fast-lv -i 3 -I 64k data-vg
# -i 3: stripe across 3 PVs
# -I 64k: stripe size

# Create mirrored LV (redundancy)
lvcreate -L 50G -n mirror-lv -m 1 data-vg
# -m 1: one mirror copy

# Convert existing LV to mirror
lvconvert -m 1 /dev/data-vg/data-lv

# Check mirror status
lvs -a -o +devices /dev/data-vg/mirror-lv
```

---
## RAID Levels Overview

| Level | Min Disks | Redundancy | Performance | Capacity |
|-------|-----------|------------|-------------|----------|
| RAID 0 | 2 | None | Best read/write | 100% |
| RAID 1 | 2 | Mirror | Good read | 50% |
| RAID 5 | 3 | 1 disk | Good read | (N-1)/N |
| RAID 6 | 4 | 2 disks | Good read | (N-2)/N |
| RAID 10 | 4 | Mirror+Stripe | Best | 50% |

---
## RAID Level Selection Guide

![raid_level_selection_guide](svg/courses/operating_systems/linux-system-administration/09_lvm_raid_optional/raid_level_selection_guide.svg)

---
## Creating RAID Arrays with mdadm

```bash
# Install
apt install mdadm

# Create RAID 1 (mirror)
mdadm --create /dev/md0 --level=1 \
  --raid-devices=2 /dev/sdb1 /dev/sdc1

# Create RAID 5
mdadm --create /dev/md1 --level=5 \
  --raid-devices=3 /dev/sdb1 /dev/sdc1 /dev/sdd1

# Save config
mdadm --detail --scan >> /etc/mdadm/mdadm.conf

# Create filesystem on array
mkfs.ext4 /dev/md0
```

---
## RAID with Spare Disks

```bash
# Create RAID 5 with hot spare
mdadm --create /dev/md0 --level=5 \
  --raid-devices=3 --spare-devices=1 \
  /dev/sdb1 /dev/sdc1 /dev/sdd1 /dev/sde1

# Add spare to existing array
mdadm --add /dev/md0 /dev/sdf1

# Grow array (add disk to RAID 5)
mdadm --grow /dev/md0 --raid-devices=4 --add /dev/sdf1

# Convert RAID level (RAID 1 -> RAID 5)
mdadm --grow /dev/md0 --level=5 --raid-devices=3 \
  --add /dev/sdd1
```

---
## Monitoring and Recovering RAID

```bash
# Check array status
cat /proc/mdstat
mdadm --detail /dev/md0

# Monitor for failures
mdadm --monitor --mail=admin@example.com /dev/md0

# Simulate disk failure
mdadm --fail /dev/md0 /dev/sdc1

# Remove failed disk
mdadm --remove /dev/md0 /dev/sdc1

# Add replacement disk
mdadm --add /dev/md0 /dev/sde1

# Watch rebuild progress
watch cat /proc/mdstat
```

---
## LVM Cache (dm-cache)

```bash
# Use a fast SSD to cache a slow HDD volume
# Create the cache data LV on the SSD
lvcreate -L 50G -n cache-data data-vg /dev/ssd1

# Create cache metadata LV (1/1000 of cache size)
lvcreate -L 100M -n cache-meta data-vg /dev/ssd1

# Create the cache pool
lvconvert --type cache-pool \
  --poolmetadata data-vg/cache-meta \
  data-vg/cache-data

# Attach cache to an existing LV
lvconvert --type cache \
  --cachepool data-vg/cache-data \
  data-vg/data-lv

# Check cache stats
lvs -o +cache_read_hits,cache_read_misses
```

Cache modes: `writethrough` (safe) or `writeback` (fast).

---

## LVM on Top of RAID

![lvm_on_top_of_raid](svg/courses/operating_systems/linux-system-administration/09_lvm_raid_optional/lvm_on_top_of_raid.svg)

---

## LVM on Top of RAID

```bash
# Create RAID arrays first
mdadm --create /dev/md0 --level=1 \
  --raid-devices=2 /dev/sdb /dev/sdc
mdadm --create /dev/md1 --level=5 \
  --raid-devices=3 /dev/sdd /dev/sde /dev/sdf
# Then use RAID arrays as LVM physical volumes
pvcreate /dev/md0 /dev/md1
vgcreate hybrid-vg /dev/md0 /dev/md1
lvcreate -L 50G -n home-lv hybrid-vg
```

---
## RAID Performance Tuning

```bash
# Set stripe cache size (RAID 5/6)
echo 8192 > /sys/block/md0/md/stripe_cache_size

# Set read-ahead for sequential workloads
blockdev --setrahead 4096 /dev/md0

# Check current settings
blockdev --getrahead /dev/md0
cat /sys/block/md0/md/stripe_cache_size

# Set rebuild speed limits
echo 200000 > /proc/sys/dev/raid/speed_limit_min
echo 500000 > /proc/sys/dev/raid/speed_limit_max

# Choose optimal chunk size at creation
# Small chunks (64K): better for small random I/O
# Large chunks (512K): better for sequential I/O
mdadm --create /dev/md0 --level=5 \
  --chunk=256 --raid-devices=4 \
  /dev/sd[b-e]1
```

---
## RAID Disk Replacement Walkthrough

```bash
# 1. Identify the failed disk
cat /proc/mdstat
mdadm --detail /dev/md0
# Look for "faulty" or "removed" state

# 2. Mark disk as failed (if not auto-detected)
mdadm --fail /dev/md0 /dev/sdc1

# 3. Remove the failed disk
mdadm --remove /dev/md0 /dev/sdc1

# 4. Physically replace the disk
# (power down if not hot-swappable)

# 5. Partition new disk to match original
sfdisk -d /dev/sdb | sfdisk /dev/sdc

# 6. Add new disk to array
mdadm --add /dev/md0 /dev/sdc1

# 7. Monitor rebuild
watch cat /proc/mdstat
mdadm --detail /dev/md0

# 8. Update mdadm config
mdadm --detail --scan > /etc/mdadm/mdadm.conf
update-initramfs -u
```

---
## LVM Troubleshooting

```bash
# LV not activating after reboot
vgchange -ay data-vg
lvchange -ay /dev/data-vg/data-lv

# VG missing after disk swap
vgscan
vgimport data-vg
vgchange -ay data-vg

# Recover from missing PV
vgreduce --removemissing data-vg

# Fix corrupted LVM metadata
vgcfgrestore data-vg
# List available backups
ls /etc/lvm/backup/
ls /etc/lvm/archive/

# Scan for orphaned PVs
pvscan --cache
pvs -a

# Debug LVM issues
lvmdump -d /tmp/lvmdump
lvm dumpconfig
```

Common issues:
- **VG inactive**: run `vgchange -ay`
- **Duplicate PVs**: caused by cloned disks, use `vgimportclone`
- **Thin pool full**: extend with `lvextend`

---
## LVM Best Practices for Virtual Machines

```bash
# Use thin provisioning for VM disk images
lvcreate -V 100G --thin -n vm-web01 \
  data-vg/thin-pool

# Take instant snapshot before VM changes
lvcreate -s -n vm-web01-snap data-vg/vm-web01

# Align LV to VM block size (4K)
lvcreate -L 50G -n vm-data data-vg \
  --config 'allocation/physical_extent_size=4096'
```

Best practices for VM storage:
- Use thin provisioning to overcommit safely
- Monitor thin pool usage with automated alerts
- Snapshot VMs before upgrades (merge to rollback)
- Use `virtio-blk` or `virtio-scsi` in the guest
- Avoid snapshots in production long-term (performance degrades)
- Set `issue_discards = 1` in `/etc/lvm/lvm.conf` for SSD backing

---
## RAID Monitoring with Email Alerts

```bash
# Configure mdadm to send email on failure
# /etc/mdadm/mdadm.conf
MAILADDR admin@example.com
MAILFROM raid-monitor@hostname

# Start the monitoring daemon
systemctl enable mdmonitor
systemctl start mdmonitor

# Test the alert (sends a test email)
mdadm --monitor --scan --test --oneshot

# Alternative: use a cron-based check script
```

```bash
#!/bin/bash
# /usr/local/bin/raid-check.sh
STATUS=$(cat /proc/mdstat)
if echo "$STATUS" | grep -q '_'; then
    echo "$STATUS" | mail -s \
      "RAID DEGRADED on $(hostname)" \
      admin@example.com
fi
```

```bash
chmod +x /usr/local/bin/raid-check.sh
# Run every 5 minutes via cron
# */5 * * * * /usr/local/bin/raid-check.sh
```

---
## Understanding `mdadm.conf`

```bash
# /etc/mdadm/mdadm.conf
# Auto-assembled arrays at boot

# Email for monitoring alerts
MAILADDR admin@example.com

# Device scan scope (default: all partitions)
DEVICE partitions

# Array definitions (generated by mdadm --detail --scan)
ARRAY /dev/md0 metadata=1.2 \
  UUID=12345678:abcdef01:23456789:fedcba98 \
  name=server:0

ARRAY /dev/md1 metadata=1.2 \
  UUID=87654321:10fedcba:98765432:89abcdef \
  name=server:1
```

```bash
# Regenerate mdadm.conf from running arrays
mdadm --detail --scan > /etc/mdadm/mdadm.conf

# Update initramfs so arrays assemble at boot
update-initramfs -u

# Verify arrays will assemble correctly
mdadm --assemble --scan --verbose
```

Key fields: `UUID` uniquely identifies each array regardless of device names.

---
## Exercise: LVM Snapshot and RAID Recovery

Practice LVM and RAID operations in a test environment:

1. Create a RAID 1 array from two loop devices:

```bash
dd if=/dev/zero of=/tmp/disk1 bs=1M count=200
dd if=/dev/zero of=/tmp/disk2 bs=1M count=200
losetup /dev/loop10 /tmp/disk1
losetup /dev/loop11 /tmp/disk2
mdadm --create /dev/md99 --level=1 \
  --raid-devices=2 /dev/loop10 /dev/loop11
```

1. Create LVM on top of the RAID array:
    - Create PV, VG, and a 100M LV
    - Format with `ext4` and mount
    - Write test data to the filesystem

1. Take an LVM snapshot, modify data, then merge to restore
1. Simulate a disk failure with `mdadm --fail` and observe rebuild after adding a replacement
1. Verify data integrity after each operation
