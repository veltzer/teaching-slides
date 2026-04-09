# Storage Management and File Systems
## Devices, Partitions, Quotas, and Backups

---
## Storage Device Management

```bash
# List all block devices
lsblk

# Detailed disk info
fdisk -l

# View disk UUIDs
blkid

# Check disk health with SMART
smartctl -a /dev/sda

# View disk I/O statistics
iostat -x 1
```

---
## Understanding Block Devices

```bash
# lsblk with full details
lsblk -f       # show filesystem type and UUID
lsblk -t       # show topology (alignment)
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT,UUID
```

Device naming:
- `/dev/sda`, `/dev/sdb` - SCSI/SATA disks
- `/dev/nvme0n1` - NVMe drives
- `/dev/vda` - VirtIO disks (VMs)
- `/dev/sda1`, `/dev/sda2` - partitions
- `/dev/md0` - RAID arrays
- `/dev/dm-0` - device mapper (LVM)

---
## SMART Disk Monitoring

```bash
# Install smartmontools
apt install smartmontools

# Check if SMART is supported
smartctl -i /dev/sda

# Enable SMART
smartctl -s on /dev/sda

# Full health check
smartctl -H /dev/sda

# Run short self-test
smartctl -t short /dev/sda

# Run long self-test
smartctl -t long /dev/sda

# View test results
smartctl -l selftest /dev/sda

# Key attributes to watch:
# Reallocated_Sector_Ct, Current_Pending_Sector
# Offline_Uncorrectable, UDMA_CRC_Error_Count
```

---
## Partitioning with fdisk and parted

```bash
# Interactive partitioning (MBR)
fdisk /dev/sdb

# GPT partitioning with parted
parted /dev/sdb
  mklabel gpt
  mkpart primary ext4 0% 50%
  mkpart primary xfs 50% 100%

# Non-interactive partitioning
parted -s /dev/sdb mklabel gpt
parted -s /dev/sdb mkpart primary ext4 0% 100%
```

- MBR: up to 4 primary partitions, 2TB max
- GPT: up to 128 partitions, 9.4ZB max

---
## Partition Alignment and Best Practices

```bash
# Check partition alignment
parted /dev/sdb align-check optimal 1

# Optimal alignment for SSDs (1MiB boundary)
parted -s /dev/sdb mkpart primary ext4 1MiB 50%

# View partition table
parted /dev/sdb print

# Backup partition table
sfdisk -d /dev/sdb > sdb-partitions.bak

# Restore partition table
sfdisk /dev/sdb < sdb-partitions.bak
```

Best practices:
- Always use GPT for new systems
- Align partitions to 1MiB boundaries
- Keep partition table backups

---
## Filesystem Types Comparison

| Filesystem | Max Size | Journal | Features |
|------------|----------|---------|----------|
| `ext4` | 1 EiB | Yes | Mature, widely supported |
| `XFS` | 8 EiB | Yes | Great for large files |
| `Btrfs` | 16 EiB | CoW | Snapshots, compression |
| `ZFS` | 256 ZiB | CoW | Enterprise features |
| `tmpfs` | RAM | No | RAM-based, volatile |
| `swap` | - | No | Virtual memory |

---
## Filesystem Creation

```bash
# Create ext4 filesystem
mkfs.ext4 /dev/sdb1

# Create XFS filesystem
mkfs.xfs /dev/sdb2

# Create filesystem with options
mkfs.ext4 -L mydata -b 4096 /dev/sdb1

# View filesystem info
tune2fs -l /dev/sdb1    # ext4
xfs_info /dev/sdb2      # xfs
```

---
## ext4 Tuning Options

```bash
# Set reserved blocks (default 5%, reduce for data)
tune2fs -m 1 /dev/sdb1

# Set filesystem label
tune2fs -L "mydata" /dev/sdb1

# Enable/disable features
tune2fs -O ^has_journal /dev/sdb1  # disable journal
tune2fs -O has_journal /dev/sdb1   # enable journal

# Set mount count before fsck
tune2fs -c 30 /dev/sdb1

# Set time between checks
tune2fs -i 180d /dev/sdb1

# View superblock info
dumpe2fs /dev/sdb1 | head -40
```

---
## Mounting Filesystems

```bash
# Mount manually
mount /dev/sdb1 /mnt/data

# Mount with options
mount -o noexec,nosuid /dev/sdb1 /mnt/data

# Persistent mount in /etc/fstab
```

```config
# /etc/fstab
# <device>       <mount>     <type>  <options>         <dump> <fsck>
UUID=abc-123     /mnt/data   ext4    defaults,noatime  0      2
/dev/sdb2        /mnt/xfs    xfs     defaults          0      0
tmpfs            /tmp        tmpfs   size=2G,noexec    0      0
```

```bash
# Mount all entries in fstab
mount -a
```

---
## Advanced Mount Options

| Option | Purpose |
|--------|---------|
| `noexec` | Prevent execution of binaries |
| `nosuid` | Ignore setuid/setgid bits |
| `nodev` | Ignore device files |
| `noatime` | Do not update access times |
| `ro` | Mount read-only |
| `quota` | Enable filesystem quotas |
| `bind` | Bind mount a directory |

```bash
# Bind mount example
mount --bind /var/www /home/chroot/www
```

---
## Mount Troubleshooting

```bash
# Find what's preventing unmount
fuser -mv /mnt/data
lsof +D /mnt/data

# Lazy unmount (detach, cleanup when idle)
umount -l /mnt/data

# Force unmount (use with caution)
umount -f /mnt/nfs

# Remount with different options
mount -o remount,ro /mnt/data

# Check mount options of mounted filesystem
findmnt /mnt/data
mount | grep /mnt/data

# systemd mount units (auto-generated from fstab)
systemctl list-units --type=mount
```

---
## Swap Space Management

```bash
# View current swap
swapon --show
free -h

# Create swap file
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# Add to fstab
# /swapfile  none  swap  sw  0  0

# Create swap partition
mkswap /dev/sdb3
swapon /dev/sdb3

# Adjust swappiness
sysctl vm.swappiness=10
```

---
## Filesystem Quotas

```bash
# Install quota tools
apt install quota

# Enable quotas in /etc/fstab (add usrquota,grpquota)
# UUID=xxx /home ext4 defaults,usrquota,grpquota 0 2

# Remount and initialize
mount -o remount /home
quotacheck -cugm /home
quotaon /home

# Set quota for a user (soft, hard, grace)
edquota -u alice

# View quota usage
repquota -a
quota -u alice
```

---
## Quota Configuration Details

```bash
# Set quota non-interactively
setquota -u alice 500M 600M 0 0 /home
# Format: softlimit hardlimit softfiles hardfiles

# Set grace period
edquota -t
# Default: 7 days for soft limit violations

# Set default quota for new users
edquota -p alice newuser

# Group quotas
setquota -g developers 5G 6G 0 0 /home

# XFS quotas (different tools)
xfs_quota -x -c 'limit bsoft=500m bhard=600m alice' /home
xfs_quota -x -c 'report' /home
```

---
## Disk Monitoring and Maintenance

```bash
# Check filesystem integrity
fsck /dev/sdb1          # must be unmounted
fsck -n /dev/sdb1       # dry run

# Check ext4 filesystem
e2fsck -f /dev/sdb1

# Monitor disk space
df -h                   # filesystem usage
du -sh /var/log/*       # directory sizes

# Monitor disk I/O
iotop                   # per-process I/O
iostat -xz 1            # device I/O stats
```

---
## Finding Disk Space Hogs

```bash
# Top 20 largest files
find / -xdev -type f -size +100M \
  -exec ls -lh {} \; 2>/dev/null | sort -k5 -rh | head -20

# Largest directories
du -xh --max-depth=2 / 2>/dev/null | sort -rh | head -20

# ncdu - interactive disk usage analyzer
apt install ncdu
ncdu /

# Check for deleted but open files (still using space)
lsof +L1

# Find old log files
find /var/log -name "*.gz" -mtime +30

# Filesystem-specific tools
xfs_bmap -v /path/to/file   # XFS file mapping
filefrag /path/to/file       # ext4 fragmentation
```

---

## Backup Strategies

![backup_strategies](svg/courses/operating_systems/linux-system-administration/04_storage_management/backup_strategies.svg)

---

## Backup Strategies

- **Full**: complete copy, slow but simple to restore
- **Differential**: changes since last full, moderate speed
- **Incremental**: changes since last backup, fast but complex restore
- **Snapshot**: filesystem-level point-in-time copy

---
## Backup with rsync

```bash
# Basic local backup
rsync -av /data/ /backup/data/

# Remote backup over SSH
rsync -avz -e ssh /data/ user@backup:/backup/data/

# Incremental backup with hard links
rsync -av --link-dest=/backup/yesterday \
  /data/ /backup/today/

# Exclude patterns
rsync -av --exclude='*.log' \
  --exclude='.cache' /home/ /backup/home/
```

---
## rsync Advanced Options

```bash
# Bandwidth limit (KBytes/sec)
rsync -avz --bwlimit=5000 /data/ remote:/backup/

# Delete files on dest that don't exist on source
rsync -av --delete /data/ /backup/data/

# Dry run (show what would be transferred)
rsync -avn /data/ /backup/data/

# Preserve hard links
rsync -avH /data/ /backup/data/

# Resume interrupted transfer
rsync -avP /data/ remote:/backup/

# Checksum-based comparison (slower but reliable)
rsync -avc /data/ /backup/data/
```

---
## Backup with tar

```bash
# Create compressed archive
tar czf /backup/data-$(date +%F).tar.gz /data/

# Create with exclusions
tar czf backup.tar.gz --exclude='*.log' /data/

# List archive contents
tar tzf backup.tar.gz

# Extract to specific directory
tar xzf backup.tar.gz -C /restore/

# Incremental backup with tar
tar czf /backup/full.tar.gz -g /backup/snapshot /data/
tar czf /backup/incr.tar.gz -g /backup/snapshot /data/
```

---
## Backup with borgbackup

```bash
# Initialize repository
borg init --encryption=repokey /backup/borg-repo

# Create a backup
borg create /backup/borg-repo::daily-{now} /data

# List backups
borg list /backup/borg-repo

# Restore a backup
borg extract /backup/borg-repo::daily-2024-01-15

# Prune old backups
borg prune --keep-daily=7 --keep-weekly=4 \
  --keep-monthly=6 /backup/borg-repo
```

Key features: deduplication, compression, encryption.

---
## borgbackup Advanced Usage

```bash
# Remote backup
borg create ssh://backup@server/repo::daily-{now} \
  /data /etc --exclude '*.cache'

# Mount backup as filesystem (browse files)
borg mount /backup/borg-repo::daily-2024-01-15 /mnt/borg
ls /mnt/borg/data/
borg umount /mnt/borg

# Show backup info and stats
borg info /backup/borg-repo::daily-2024-01-15

# Verify backup integrity
borg check /backup/borg-repo

# Export/import repo key (for disaster recovery)
borg key export /backup/borg-repo keyfile.txt
```

---
## Automated Backup Script

```bash
#!/bin/bash
# /usr/local/bin/backup.sh
REPO="/backup/borg-repo"
BACKUP_NAME="daily-$(date +%F_%H%M)"

# Create backup
borg create --stats --compression lz4 \
  "${REPO}::${BACKUP_NAME}" \
  /etc /home /var/www \
  --exclude '/home/*/.cache'

# Prune old backups
borg prune --keep-daily=7 --keep-weekly=4 \
  --keep-monthly=12 "$REPO"

# Verify
borg check "$REPO" --last 3
```

Trigger via `systemd` timer or `cron`.

---
## NFS Shared Filesystems

```bash
# Server: install and export
apt install nfs-kernel-server

# /etc/exports
# /shared  192.168.1.0/24(rw,sync,no_subtree_check)

exportfs -a
systemctl restart nfs-kernel-server
```

```bash
# Client: mount NFS share
apt install nfs-common
mount -t nfs server:/shared /mnt/nfs

# Persistent mount in /etc/fstab
# server:/shared  /mnt/nfs  nfs  defaults,_netdev  0  0
```

---
## NFS Advanced Configuration

```bash
# Export options explained
# /data  10.0.0.0/8(rw,sync,no_root_squash,no_subtree_check)
```

| Option | Purpose |
|--------|---------|
| `rw` / `ro` | Read-write or read-only |
| `sync` | Write to disk before responding |
| `no_root_squash` | Allow root on client to be root on NFS |
| `root_squash` | Map client root to `nobody` (default) |
| `all_squash` | Map all users to `nobody` |
| `no_subtree_check` | Disable subtree checking (faster) |

```bash
# Check active exports
exportfs -v

# NFS statistics
nfsstat -s    # server stats
nfsstat -c    # client stats
```

---
## Samba Shared Filesystems

```bash
# Install Samba
apt install samba

# Add share to /etc/samba/smb.conf
```

```ini
[shared]
    path = /srv/samba/shared
    browseable = yes
    read only = no
    valid users = @smbgroup
```

```bash
# Set Samba password for user
smbpasswd -a alice

# Restart and test
systemctl restart smbd
testparm
```

---
## Samba Client and Advanced Options

```bash
# Access from Linux client
smbclient //server/shared -U alice

# Mount Samba share
mount -t cifs //server/shared /mnt/samba \
  -o username=alice,password=secret

# Persistent mount in fstab (use credentials file)
# //server/shared  /mnt/samba  cifs  credentials=/root/.smbcred,_netdev  0  0

# Credentials file (/root/.smbcred, mode 600)
# username=alice
# password=secret
# domain=WORKGROUP
```

---
## Filesystem Integrity and Recovery

```bash
# Check for filesystem corruption
dumpe2fs /dev/sdb1 | grep -i error

# Force fsck on next boot
touch /forcefsck

# Recover deleted files (ext4)
extundelete /dev/sdb1 --restore-all

# XFS repair
xfs_repair /dev/sdb2

# Monitor filesystem events
inotifywait -m -r /data/
```

---
## Filesystem Recovery Deep Dive

```bash
# Backup superblock locations (ext4)
dumpe2fs /dev/sdb1 | grep -i superblock

# Recover using backup superblock
e2fsck -b 32768 /dev/sdb1

# XFS metadata dump for analysis
xfs_metadump /dev/sdb2 metadump.img
xfs_mdrestore metadump.img /dev/sdb2

# testdisk - partition and file recovery
apt install testdisk
testdisk /dev/sdb

# photorec - recover files by signature
photorec /dev/sdb1

# ddrescue - recover data from failing disk
apt install gddrescue
ddrescue /dev/sda /dev/sdc rescue.log
```

---
## `Btrfs` Filesystem

`Btrfs` is a copy-on-write filesystem with built-in snapshots, compression, and subvolumes.

```bash
# Create a Btrfs filesystem
mkfs.btrfs /dev/sdb1

# Mount with compression
mount -o compress=zstd /dev/sdb1 /mnt/data

# Create subvolumes
btrfs subvolume create /mnt/data/@home
btrfs subvolume create /mnt/data/@var

# List subvolumes
btrfs subvolume list /mnt/data

# Mount a specific subvolume
mount -o subvol=@home /dev/sdb1 /home
```

---
## `Btrfs` Snapshots and Maintenance

```bash
# Create a read-only snapshot
btrfs subvolume snapshot -r /mnt/data/@home \
  /mnt/data/@home-snap-$(date +%F)

# Create a writable snapshot (for testing)
btrfs subvolume snapshot /mnt/data/@home \
  /mnt/data/@home-writable

# Delete a snapshot
btrfs subvolume delete /mnt/data/@home-writable

# Show filesystem usage
btrfs filesystem usage /mnt/data

# Scrub for data integrity
btrfs scrub start /mnt/data
btrfs scrub status /mnt/data

# Balance data across devices
btrfs balance start /mnt/data
```

---
## Disk Encryption with `LUKS`

`LUKS` provides full-disk encryption using `dm-crypt`.

```bash
# Install cryptsetup
apt install cryptsetup

# Format partition with LUKS
cryptsetup luksFormat /dev/sdb1

# Open the encrypted partition
cryptsetup luksOpen /dev/sdb1 secure_data

# Create filesystem on the mapped device
mkfs.ext4 /dev/mapper/secure_data

# Mount
mount /dev/mapper/secure_data /mnt/secure

# Close when done
umount /mnt/secure
cryptsetup luksClose secure_data
```

---
## `LUKS` Persistent Configuration

```bash
# Add a key file for automated unlock
dd if=/dev/urandom of=/root/luks-keyfile bs=4096 count=1
chmod 600 /root/luks-keyfile
cryptsetup luksAddKey /dev/sdb1 /root/luks-keyfile
```

```config
# /etc/crypttab
# name      device          key file            options
secure_data /dev/sdb1       /root/luks-keyfile  luks
```

```config
# /etc/fstab
/dev/mapper/secure_data  /mnt/secure  ext4  defaults  0  2
```

```bash
# Manage LUKS key slots
cryptsetup luksDump /dev/sdb1      # show key slots
cryptsetup luksAddKey /dev/sdb1    # add a passphrase
cryptsetup luksRemoveKey /dev/sdb1 # remove a passphrase

# Backup LUKS header (critical for recovery)
cryptsetup luksHeaderBackup /dev/sdb1 \
  --header-backup-file /root/sdb1-luks-header.bak
```

---
## Automounting with `autofs`

`autofs` mounts filesystems on demand and unmounts after idle timeout.

```bash
# Install autofs
apt install autofs
```

```bash
# /etc/auto.master
/mnt/auto  /etc/auto.nfs  --timeout=300
```

```bash
# /etc/auto.nfs
# key     options          source
data      -rw,soft         server:/export/data
home      -rw,soft         server:/export/home
```

```bash
# Restart autofs
systemctl enable --now autofs

# Access triggers the mount automatically
ls /mnt/auto/data    # mounts server:/export/data
# After 300s of inactivity, it unmounts automatically

# Debug autofs issues
automount -f -v -d
journalctl -u autofs
```

---
## Loop Devices

Loop devices allow you to mount regular files as block devices.

```bash
# Create a file-backed block device
dd if=/dev/zero of=/tmp/disk.img bs=1M count=500
losetup /dev/loop0 /tmp/disk.img

# Create a filesystem on it
mkfs.ext4 /dev/loop0
mount /dev/loop0 /mnt/loop

# Auto-assign the next free loop device
losetup -f --show /tmp/disk.img

# List active loop devices
losetup -a

# Mount an ISO image directly
mount -o loop,ro /path/to/image.iso /mnt/iso
```

```bash
# Detach a loop device
umount /mnt/loop
losetup -d /dev/loop0

# Create a partitioned disk image
parted /tmp/disk.img mklabel gpt
losetup -P /dev/loop0 /tmp/disk.img
ls /dev/loop0p*    # partitions appear automatically
```

---
## Disk I/O Scheduling Deep Dive

The I/O scheduler determines how read/write requests are ordered and merged.

| Scheduler | Best For | Algorithm |
|-----------|----------|-----------|
| `none` | NVMe, fast SSDs | No reordering (FIFO) |
| `mq-deadline` | SSDs, databases | Deadline-based, fair |
| `bfq` | Desktop, latency-sensitive | Budget Fair Queuing |
| `kyber` | Fast SSDs, servers | Token-based, low latency |

```bash
# Check current scheduler
cat /sys/block/sda/queue/scheduler

# Change scheduler at runtime
echo "mq-deadline" > /sys/block/sda/queue/scheduler

# Make persistent via udev rule
# /etc/udev/rules.d/60-ioscheduler.rules
# ACTION=="add|change", KERNEL=="sd*", \
#   ATTR{queue/scheduler}="mq-deadline"
# ACTION=="add|change", KERNEL=="nvme*", \
#   ATTR{queue/scheduler}="none"
```

```bash
# Tune scheduler parameters
cat /sys/block/sda/queue/iosched/read_expire
echo 100 > /sys/block/sda/queue/iosched/read_expire
```

---
## `fstrim` for SSD Maintenance

SSDs need periodic `TRIM` commands to maintain write performance and longevity.

```bash
# Manual TRIM on a mounted filesystem
fstrim -v /
fstrim -v /home

# TRIM all mounted filesystems
fstrim -av
```

```bash
# Enable the weekly fstrim timer (recommended)
systemctl enable --now fstrim.timer
systemctl list-timers | grep fstrim

# Verify TRIM support
lsblk --discard
# DISC-GRAN and DISC-MAX should be non-zero
```

```bash
# Alternative: continuous TRIM via mount option
# /etc/fstab
# UUID=xxx  /  ext4  defaults,discard  0  1
# Note: periodic fstrim.timer is preferred over
# the "discard" mount option for performance reasons
```

---

## Multipath I/O

Multipath I/O (`dm-multipath`) provides redundant paths to SAN storage for high availability.

---

## Multipath I/O

![multipath_i_o](svg/courses/operating_systems/linux-system-administration/04_storage_management/multipath_i_o.svg)

---

## Multipath I/O

```bash
# Install multipath tools
apt install multipath-tools
# Discover multipath devices
multipath -ll
# Configuration: /etc/multipath.conf
# defaults {
#     user_friendly_names yes
#     path_grouping_policy multibus
#     failback immediate
# }
# Restart and check
systemctl restart multipathd
multipath -v2
```

---
## Storage Planning for Production

Key considerations when planning storage for production servers:

| Mount Point | Sizing Guidance | Options |
|-------------|----------------|---------|
| `/` | 20-50 GB | `noatime` |
| `/boot` | 1-2 GB | `nodev,nosuid` |
| `/home` | Per-user quotas | `nodev,nosuid,usrquota` |
| `/var` | 20-100 GB (logs grow) | `nodev,nosuid` |
| `/var/log` | 10-50 GB separate | `nodev,nosuid,noexec` |
| `/tmp` | 5-10 GB or `tmpfs` | `nodev,nosuid,noexec` |
| `/opt` | As needed | `nodev` |
| Swap | 1-2x RAM (up to 8 GB) | `sw` |

```bash
# Monitor growth trends
df -h | grep -E '(Filesystem|/var|/home)'
du -sh /var/log/ /var/cache/ /var/lib/

# Set up alerts for >80% usage
# Use cron + df or monitoring tools (Prometheus, Zabbix)
```

---
## `iSCSI` Overview

`iSCSI` provides block-level storage over TCP/IP networks, acting as a cheaper SAN alternative.

```bash
# Initiator (client) setup
apt install open-iscsi

# Discover targets
iscsiadm -m discovery -t sendtargets -p 192.168.1.50

# Login to a target
iscsiadm -m node \
  -T iqn.2024-01.com.example:storage \
  -p 192.168.1.50 --login

# The LUN appears as a local block device
lsblk    # new /dev/sdX appears
```

```bash
# Set automatic login at boot
iscsiadm -m node \
  -T iqn.2024-01.com.example:storage \
  -p 192.168.1.50 --op update \
  -n node.startup -v automatic

# Logout and cleanup
iscsiadm -m node --logoutall=all

# Check session status
iscsiadm -m session -P 3
```

---
## Disk Cloning with `dd`

`dd` performs low-level byte-for-byte copies of block devices.

```bash
# Clone entire disk to another disk
dd if=/dev/sda of=/dev/sdb bs=64K \
  conv=noerror,sync status=progress

# Create a disk image
dd if=/dev/sda of=/backup/sda.img bs=64K \
  status=progress

# Restore from image
dd if=/backup/sda.img of=/dev/sda bs=64K \
  status=progress

# Wipe a disk securely
dd if=/dev/urandom of=/dev/sdb bs=1M \
  status=progress
```

```bash
# Faster alternative: use ddrescue for failing disks
ddrescue /dev/sda /dev/sdb rescue.log

# Compress while cloning
dd if=/dev/sda bs=64K status=progress | \
  gzip > /backup/sda.img.gz

# Restore compressed image
gunzip -c /backup/sda.img.gz | \
  dd of=/dev/sda bs=64K status=progress
```

---
## Exercise: Storage Management Tasks

1. Create a 500 MB file-backed loop device, format it with `ext4`, and mount it to `/mnt/exercise`
1. Check the current I/O scheduler for your primary disk and change it to `mq-deadline`
1. Verify whether your system supports `TRIM` and enable the `fstrim.timer`
1. Set up filesystem quotas on the loop device:
    - Soft limit: 100 MB per user
    - Hard limit: 150 MB per user
1. Create a full backup of `/etc` using `tar`, then create an incremental backup
1. Use `dd` to clone the loop device to a second image file and verify with `diff`

```bash
# Setup hints
dd if=/dev/zero of=/tmp/exercise.img bs=1M count=500
losetup -f --show /tmp/exercise.img
mkfs.ext4 /dev/loop0
mount /dev/loop0 /mnt/exercise

# Verify your work
lsblk | grep loop
findmnt /mnt/exercise
cat /sys/block/sda/queue/scheduler
```

---
## Disk Performance Benchmarking

```bash
# fio - flexible I/O tester (industry standard)
apt install fio

# Sequential read test
fio --name=seqread --rw=read --bs=1M \
  --size=1G --numjobs=1 --runtime=30

# Random read/write (simulates database workload)
fio --name=randmix --rw=randrw --bs=4k \
  --size=512M --numjobs=4 --iodepth=32 --runtime=30

# Quick dd benchmark (simple but less accurate)
dd if=/dev/zero of=/tmp/bench bs=1M count=1024 \
  conv=fdatasync status=progress
```

```bash
# hdparm - test cached and buffered reads
hdparm -Tt /dev/sda
# Timing cached reads:   ~8000 MB/sec (RAM speed)
# Timing buffered reads: ~500 MB/sec (disk speed)
```

Interpreting results: compare IOPS for random workloads, throughput (MB/s) for sequential. Always test with a workload that matches your production use case.

---
## ZFS on Linux Overview

`ZFS` combines volume management and filesystem into one, with built-in integrity checking.

```bash
# Install ZFS
apt install zfsutils-linux

# Create a pool (mirror = RAID1)
zpool create tank mirror /dev/sdb /dev/sdc

# Create a dataset with compression
zfs create tank/data
zfs set compression=lz4 tank/data

# Check pool status
zpool status
zpool list
```

```bash
# Snapshots (instant, copy-on-write)
zfs snapshot tank/data@backup-$(date +%F)
zfs list -t snapshot

# Rollback to a snapshot
zfs rollback tank/data@backup-2025-03-01

# Send/receive for replication
zfs send tank/data@snap1 | \
  ssh backup-server zfs receive backup/data

# Incremental send
zfs send -i @snap1 tank/data@snap2 | \
  ssh backup-server zfs receive backup/data
```

---
## Storage Monitoring Scripts

```bash
#!/bin/bash
# Disk space alert script
THRESHOLD=80
df -h --output=pcent,target | tail -n +2 | \
  while read usage mount; do
    pct=${usage%\%}
    if [ "$pct" -gt "$THRESHOLD" ]; then
      echo "WARNING: $mount is ${usage} full"
    fi
  done
```

```bash
# Inode usage monitoring
df -i --output=ipcent,target | tail -n +2 | \
  while read usage mount; do
    pct=${usage%\%}
    if [ "$pct" -gt 80 ]; then
      echo "INODE WARNING: $mount at ${usage}"
    fi
  done

# SMART health check script
for disk in /dev/sd?; do
  status=$(smartctl -H "$disk" | grep "PASSED\|FAILED")
  echo "$disk: $status"
done
```

Integrate these scripts with `cron` or `systemd` timers and send alerts via email or monitoring systems.

---
## Logical vs Physical Sector Size

Modern disks may have different logical and physical sector sizes.

| Type | Logical | Physical | Common On |
|------|---------|----------|-----------|
| 512n | 512 B | 512 B | Older HDDs |
| 512e | 512 B | 4096 B | Most modern HDDs |
| 4Kn | 4096 B | 4096 B | Enterprise SSDs, new HDDs |

```bash
# Check sector sizes
fdisk -l /dev/sda | grep "Sector size"
cat /sys/block/sda/queue/logical_block_size
cat /sys/block/sda/queue/physical_block_size

# Check partition alignment
parted /dev/sda align-check optimal 1
```

Misaligned partitions on `512e` or `4Kn` drives cause write amplification and poor performance. Always start partitions on 1 MiB boundaries.

```bash
# parted aligns automatically with modern defaults
parted -s /dev/sdb mkpart primary ext4 1MiB 100%

# fdisk may not align properly on older versions
# Use parted or gdisk for reliable alignment
```
