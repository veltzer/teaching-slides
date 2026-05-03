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

# Computer Hardware Fundamentals for Forensics

## Course: Linux Forensics - Day 1
- Understanding hardware is the foundation of digital forensics
- Investigators must know how data is physically stored
- Hardware knowledge helps with evidence acquisition and preservation
- This module covers drives, storage media, and data representation

---

## Why Hardware Matters in Forensics

- Data persists on physical media even after "deletion"
- Understanding hardware helps recover evidence
- Different storage technologies have different forensic implications
- Physical access to hardware may be required during investigations
- Chain of custody begins with physical devices

---

## Computer Architecture Overview

![computer_architecture_overview](svg/courses/security/linux-forensics/01_hardware/computer_architecture_overview.svg)

---

## Data Size Units

| Unit     | Abbreviation | Size                    |
|----------|-------------|-------------------------|
| Bit      | b           | 0 or 1                  |
| Byte     | B           | 8 bits                  |
| Kilobyte | KB          | 1,024 bytes             |
| Megabyte | MB          | 1,048,576 bytes         |
| Gigabyte | GB          | 1,073,741,824 bytes     |
| Terabyte | TB          | 1,099,511,627,776 bytes |

- Forensic tools often report sizes in bytes for precision
- Be aware of the difference between KB (1024) and kB (1000)

---

## Binary and Hexadecimal Representation

- Computers store everything as binary (base 2)
- Hexadecimal (base 16) is used for compact representation
- Each hex digit represents 4 bits (a nibble)

```bash
# Convert decimal to hex
printf '%x\n' 255
# Output: ff

# Convert hex to decimal
printf '%d\n' 0xff
# Output: 255

# View raw bytes of a file in hex
xxd /bin/ls | head -5
```

---

## Hexadecimal in Forensics

```misc
Decimal:  0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
Hex:      0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F
Binary: 0000 0001 0010 0011 0100 0101 0110 0111 ...
```

- File signatures (magic numbers) are expressed in hex
- Memory addresses use hexadecimal notation
- Hex editors are essential forensic tools
- Example: `PDF` files start with `%PDF` = `25 50 44 46` in hex

---

## Endianness

- **Little-endian**: least significant byte stored first (x86, x86_64)
- **Big-endian**: most significant byte stored first (network byte order)

```bash
# Check system endianness
lscpu | grep "Byte Order"
# Output: Byte Order: Little Endian

# The value 0x01020304 is stored as:
# Little-endian: 04 03 02 01
# Big-endian:    01 02 03 04
```

- Endianness matters when parsing binary data in forensic analysis
- `ext4` filesystem uses little-endian format
- Network captures use big-endian (network byte order)

---

## Hard Disk Drive (HDD) Anatomy

![hard_disk_drive_hdd_anatomy](svg/courses/security/linux-forensics/01_hardware/hard_disk_drive_hdd_anatomy.svg)

---

## Hard Disk Drive (HDD) Anatomy: Details

- Platters spin at 5400-15000 RPM
- Read/write heads float nanometers above surface
- Data is stored magnetically on platter surfaces
- Each platter has two surfaces (top and bottom)

---

## HDD Geometry: CHS Addressing: Details

- **Cylinder**: concentric tracks at same position on all platters
- **Head**: which platter surface (top/bottom)
- **Sector**: subdivision of a track (traditionally 512 bytes)

---

## HDD Geometry: CHS Addressing

![hdd_geometry_chs_addressing](svg/courses/security/linux-forensics/01_hardware/hdd_geometry_chs_addressing.svg)

---

## HDD Geometry: CHS Addressing: Details (2)

- Modern drives use LBA (Logical Block Addressing) instead of CHS
- LBA numbers sectors sequentially from 0

---

## Logical Block Addressing (LBA)

```bash
# View disk geometry and LBA information
sudo fdisk -l /dev/sda

# Example output:
# Disk /dev/sda: 500 GB
# Sector size (logical/physical): 512 bytes / 4096 bytes
# Disklabel type: gpt
# Sectors: 976773168
```

- LBA maps physical locations to sequential numbers
- Sector 0 = first sector on disk
- Modern drives: 4096-byte physical sectors (Advanced Format)
- Logical sector size may still be reported as 512 bytes

---

## Solid State Drives (SSD): Details

- No moving parts - uses NAND flash memory
- Data stored in cells as electrical charges
- Organized into pages (4-16 KB) and blocks (256-512 pages)

---

## Solid State Drives (SSD)

![solid_state_drives_ssd](svg/courses/security/linux-forensics/01_hardware/solid_state_drives_ssd.svg)

---

## SSD Forensic Implications

- **TRIM command**: tells SSD which blocks are no longer in use
    - Data may be permanently erased automatically
    - Reduces chances of recovering deleted files
- **Wear leveling**: data moves between cells automatically
    - Makes traditional data carving less predictable
- **Over-provisioning**: hidden reserve space
    - May contain remnant data not accessible via standard interfaces

```bash
# Check if TRIM is enabled
sudo fstrim -v /
# Or check mount options
mount | grep discard

# Check SSD TRIM support
sudo hdparm -I /dev/sda | grep TRIM
```

---

## SSD vs HDD: Forensic Comparison

| Feature          | HDD                      | SSD                      |
|-----------------|--------------------------|--------------------------|
| Deleted data    | Often recoverable        | May be wiped by TRIM     |
| Write patterns  | Sequential preferred     | Random access efficient  |
| Wear leveling   | Not applicable           | Active, moves data       |
| Data remnants   | Magnetic residue exists  | Electrical charges fade  |
| Imaging speed   | Slower                   | Faster                   |
| Physical damage | Head crash, platter damage| Controller failure       |
| Hidden areas    | HPA, DCO                 | Over-provisioned space   |

---

## Host Protected Area (HPA) and Device Configuration Overlay (DCO)

- **HPA**: hidden area at end of drive, not visible to OS
- **DCO**: can hide entire drive features and capacity
- Both can be used to hide data from forensic tools

```bash
# Detect HPA using hdparm
sudo hdparm -N /dev/sda
# Output: max sectors = 976773168/976773168, HPA is disabled

# Check for DCO
sudo hdparm --dco-identify /dev/sda

# Remove HPA (CAUTION: may alter evidence)
# sudo hdparm -N p976773168 /dev/sda
```

- Always document HPA/DCO status before acquisition

---

## Disk Interfaces

| Interface | Speed         | Use Case              |
|-----------|--------------|----------------------|
| SATA III  | 6 Gbps      | Consumer HDDs/SSDs   |
| SAS       | 12 Gbps     | Enterprise servers   |
| NVMe      | 32 Gbps+    | Modern SSDs (PCIe)   |
| USB 3.0   | 5 Gbps      | External drives      |
| USB 3.1   | 10 Gbps     | External SSDs        |
| USB 3.2   | 20 Gbps     | Fast external storage|

```bash
# Identify disk interfaces
lsblk -d -o NAME,TRAN,SIZE,MODEL
# Example output:
# sda  sata  500G  Samsung_SSD_860
# nvme0n1  nvme  1T  Samsung_970_EVO
```

---

## Write Blockers

- **Critical** for forensic integrity
- Prevents any write operations to evidence drive
- Hardware write blockers: physical devices inline between drive and examiner system
- Software write blockers: OS-level protection

```bash
# Software write blocking using blockdev
sudo blockdev --setro /dev/sdb

# Verify read-only status
sudo blockdev --getro /dev/sdb
# Output: 1 (read-only)

# Using udev rules for automatic write blocking
# /etc/udev/rules.d/99-forensic-readonly.rules
# SUBSYSTEM=="block", ACTION=="add", RUN+="/sbin/blockdev --setro %N"
```

---

## Identifying Connected Drives

```bash
# List all block devices
lsblk
# NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
# sda      8:0    0   500G  0 disk
# ├─sda1   8:1    0   512M  0 part /boot/efi
# ├─sda2   8:2    0   488G  0 part /
# └─sda3   8:3    0    12G  0 part [SWAP]
# sdb      8:16   0     1T  0 disk

# Detailed disk information
sudo fdisk -l /dev/sdb

# SMART data (drive health)
sudo smartctl -a /dev/sda
```

---

## Drive Serial Numbers and Identification

```bash
# Get drive serial number (essential for chain of custody)
sudo hdparm -I /dev/sda | grep "Serial Number"

# Using udevadm
udevadm info --query=all --name=/dev/sda | grep SERIAL

# Using lshw
sudo lshw -class disk -short

# All connected USB devices
lsusb -v 2>/dev/null | grep -E "idVendor|idProduct|iSerial"
```

- Always record serial numbers in forensic documentation
- Serial numbers link physical evidence to digital images

---

## Partitioning: MBR vs GPT

### MBR (Master Boot Record)
- Legacy partitioning scheme (since 1983)
- Located in first 512 bytes (LBA 0)
- Maximum 4 primary partitions
- Maximum disk size: 2 TB
- Boot code: 446 bytes, partition table: 64 bytes, signature: 2 bytes

### GPT (GUID Partition Table)
- Modern partitioning scheme (UEFI standard)
- Supports up to 128 partitions
- Maximum disk size: 9.4 ZB
- Includes backup partition table at end of disk
- Uses CRC32 checksums for integrity

---

## MBR Structure

```misc
Offset  Size   Description
0x000   446    Bootstrap code
0x1BE   16     Partition entry 1
0x1CE   16     Partition entry 2
0x1DE   16     Partition entry 3
0x1EE   16     Partition entry 4
0x1FE   2      Boot signature (0x55AA)
```

```bash
# Read MBR
sudo dd if=/dev/sda bs=512 count=1 | xxd | head -20

# Check partition table type
sudo fdisk -l /dev/sda | grep "Disklabel type"
# Output: Disklabel type: gpt  (or dos for MBR)
```

---

## GPT Structure

![gpt_structure](svg/courses/security/linux-forensics/01_hardware/gpt_structure.svg)

---

## GPT Structure: Details

- Each partition has a unique GUID
- Backup header allows recovery if primary is corrupted

---

## Examining Partition Tables

```bash
# Using gdisk for GPT disks
sudo gdisk -l /dev/sda

# Using parted
sudo parted /dev/sda print

# Using sfdisk (scriptable, good for backup)
sudo sfdisk -d /dev/sda

# Backup partition table
sudo sfdisk -d /dev/sda > partition_backup.txt

# Using blkid for filesystem identification
sudo blkid
# /dev/sda1: UUID="ABCD-1234" TYPE="vfat" PARTLABEL="EFI"
# /dev/sda2: UUID="abcdef12-..." TYPE="ext4"
```

---

## Common Partition Types

| Type Code | Filesystem | Description           |
|-----------|------------|----------------------|
| 0x83      | ext4       | Linux filesystem     |
| 0x82      | swap       | Linux swap           |
| 0x07      | NTFS       | Windows NTFS         |
| 0x0B      | FAT32      | FAT32 (older)        |
| 0x0C      | FAT32      | FAT32 LBA            |
| 0xEF      | FAT32      | EFI System Partition |
| 0xFD      | -          | Linux RAID           |
| 0x8E      | -          | Linux LVM            |

```bash
# List known partition types
sudo sfdisk -T
```

---

## Logical Volume Manager (LVM)

![logical_volume_manager_lvm](svg/courses/security/linux-forensics/01_hardware/logical_volume_manager_lvm.svg)

---

## Logical Volume Manager (LVM): Example

```bash
# List physical volumes, volume groups, logical volumes
sudo pvs
sudo vgs
sudo lvs
sudo lvdisplay
```

---

## LVM Forensic Considerations

```bash
# Scan for LVM volumes on a forensic image
sudo losetup -fP forensic_image.dd
sudo pvscan
sudo vgscan
sudo lvscan

# Activate volume groups (read-only)
sudo vgchange -ay --readonly

# Mount LVM logical volume read-only
sudo mount -o ro,noexec /dev/vg_name/lv_name /mnt/evidence

# Deactivate when done
sudo vgchange -an vg_name
```

- LVM adds complexity to forensic imaging
- Must capture entire physical volumes
- Snapshots may contain forensic artifacts

---

## RAID Configurations

| Level  | Description         | Min Disks | Forensic Note                |
|--------|--------------------|-----------|-----------------------------|
| RAID 0 | Striping           | 2         | All disks needed            |
| RAID 1 | Mirroring          | 2         | Either disk has full copy   |
| RAID 5 | Striping + Parity  | 3         | Can rebuild with N-1 disks  |
| RAID 6 | Striping + 2 Parity| 4         | Can rebuild with N-2 disks  |
| RAID 10| Mirror + Stripe    | 4         | Need one from each mirror   |

```bash
# Check for software RAID
cat /proc/mdstat
sudo mdadm --detail /dev/md0
```

---

## Disk Imaging Basics

```bash
# Basic disk image with dd
sudo dd if=/dev/sdb of=/evidence/disk_image.dd bs=4M \
  status=progress conv=sync,noerror

# Using dcfldd (forensic version of dd with hashing)
sudo dcfldd if=/dev/sdb of=/evidence/disk_image.dd \
  bs=4M hash=md5,sha256 hashwindow=1G \
  hashlog=/evidence/hash_log.txt

# Using dc3dd (another forensic dd variant)
sudo dc3dd if=/dev/sdb of=/evidence/disk_image.dd \
  hof=/evidence/disk_image.dd.md5 hash=md5 log=imaging.log
```

- Always use a write blocker on the source drive
- Calculate and verify hashes before and after imaging
- Document the entire process

---

## Verifying Disk Images

```bash
# Calculate hash of source drive
sudo md5sum /dev/sdb
sudo sha256sum /dev/sdb

# Calculate hash of image
md5sum /evidence/disk_image.dd
sha256sum /evidence/disk_image.dd

# Both hashes MUST match
# If they don't, the image is not a faithful copy

# Verify image integrity later
sha256sum -c /evidence/checksums.sha256
```

---

## Working with Disk Images

```bash
# Mount a disk image read-only
sudo mount -o ro,loop,noexec /evidence/disk_image.dd /mnt/evidence

# Mount specific partition from image
# First find partition offsets
fdisk -l /evidence/disk_image.dd
# Note the Start sector and multiply by sector size (usually 512)

# Mount partition starting at sector 2048
sudo mount -o ro,loop,offset=$((2048 * 512)),noexec \
  /evidence/disk_image.dd /mnt/evidence

# Using losetup for partition access
sudo losetup -fP /evidence/disk_image.dd
# Creates /dev/loop0, /dev/loop0p1, /dev/loop0p2, etc.
```

---

## Storage Media: Other Types

### USB Flash Drives
- Use NAND flash similar to SSDs
- Often FAT32 or NTFS formatted
- May have hidden partitions
- Wear leveling less aggressive than SSDs

### SD Cards / microSD
- Common in phones, cameras, IoT devices
- Usually FAT32 or exFAT
- Relatively easy to image

### Optical Media (CD/DVD/Blu-ray)
- Write-once media preserves original data
- ISO 9660 / UDF filesystems
- `dd if=/dev/sr0 of=disc_image.iso`

---

## Disk Health and SMART Data

```bash
# Install smartmontools
sudo apt install smartmontools

# View SMART data
sudo smartctl -a /dev/sda

# Key forensic indicators:
# - Power_On_Hours: total usage time
# - Power_Cycle_Count: number of power on/off cycles
# - Reallocated_Sector_Ct: bad sectors replaced
# - Temperature_Celsius: operating temperature

# Start a short self-test
sudo smartctl -t short /dev/sda

# View test results
sudo smartctl -l selftest /dev/sda
```

- SMART data can establish drive usage timeline

---

## Secure Erase and Anti-Forensics Awareness

- Attackers may attempt to destroy evidence
- Understanding erasure methods helps assess data recoverability

```bash
# Standard delete - data remains on disk
rm secret_file.txt

# Overwrite with zeros (single pass)
sudo dd if=/dev/zero of=/dev/sdb bs=4M status=progress

# Secure erase via ATA command (SSD)
sudo hdparm --security-set-pass forensics /dev/sdb
sudo hdparm --security-erase forensics /dev/sdb

# shred - multiple overwrites
shred -vfz -n 3 sensitive_file.txt
```

- Single-pass overwrite is sufficient for modern drives
- SSD secure erase may leave data in over-provisioned areas

---

## Exercise: Hardware Identification Lab

### Tasks:
1. List all block devices and their properties
1. Identify the partition table type for each disk
1. Record serial numbers of all connected drives
1. Check for HPA/DCO on available drives
1. Check SMART health status

```bash
# Complete identification script
echo "=== Block Devices ==="
lsblk -o NAME,SIZE,TYPE,FSTYPE,TRAN,SERIAL,MODEL
echo "=== Partition Tables ==="
sudo fdisk -l
echo "=== Drive Serials ==="
for dev in /dev/sd?; do
  echo "$dev: $(sudo hdparm -I $dev 2>/dev/null | grep Serial)"
done
```

---

## Summary: Hardware Fundamentals

- Digital forensics requires deep hardware knowledge
- HDDs and SSDs have fundamentally different forensic properties
- TRIM and wear leveling on SSDs complicate data recovery
- Always use write blockers during evidence acquisition
- Document drive serial numbers, model, and capacity
- MBR and GPT partition tables structure disk layout
- LVM and RAID add layers of complexity
- Disk imaging with hash verification preserves evidence integrity
- HPA and DCO can hide data from the operating system

---

## NVMe Drive Forensics

- NVMe drives connect directly to PCIe bus
- Faster than SATA, different forensic tools needed
- NVMe namespaces can hide data

```bash
# List NVMe devices
sudo nvme list
# Node       SN          Model                Namespace
# /dev/nvme0n1  S4EVNF0M...  Samsung 970 EVO Plus  1

# NVMe device information
sudo nvme id-ctrl /dev/nvme0n1

# NVMe namespaces (potential hidden storage)
sudo nvme list-ns /dev/nvme0n1
# [   0]:0x1

# NVMe SMART log
sudo nvme smart-log /dev/nvme0n1
# temperature         : 35 C
# available_spare     : 100%
# data_units_read     : 12345678
# data_units_written  : 9876543
# power_on_hours      : 2500
# unsafe_shutdowns    : 3
```

---

## USB Device History

```bash
# USB devices leave traces in multiple locations

# Kernel messages (current boot)
dmesg | grep -i usb | grep -iE "product|serial|new"

# udev database
udevadm info --export-db | grep -B5 -A10 "ID_BUS=usb"

# Syslog history (past events)
grep -i "usb" /var/log/syslog*

# USB device authorization log
cat /var/log/auth.log | grep -i "usb"

# List of USB device rules
ls /etc/udev/rules.d/*usb* 2>/dev/null

# USB device IDs
lsusb -v 2>/dev/null | grep -E "idVendor|idProduct|iSerial|iManufacturer|iProduct"

# journalctl USB events
journalctl | grep -i "usb" | grep -iE "new|product|serial"
```

---

## Disk Error Handling During Imaging

```bash
# When drives have bad sectors, special handling is needed

# Check for bad blocks
sudo badblocks -v /dev/sdb

# Image with dd and error handling
sudo dd if=/dev/sdb of=/evidence/disk.dd bs=512 \
  conv=noerror,sync status=progress
# noerror: don't stop on read errors
# sync: pad error blocks with zeros

# Count errors during imaging
sudo dd if=/dev/sdb of=/evidence/disk.dd bs=512 \
  conv=noerror,sync status=progress 2>&1 | tee imaging.log
grep -c "error" imaging.log

# Better: use ddrescue for damaged media
sudo ddrescue -n -b 512 /dev/sdb /evidence/disk.dd rescue.map
sudo ddrescue -d -r 3 -b 512 /dev/sdb /evidence/disk.dd rescue.map

# View ddrescue map
ddrescuelog -t rescue.map
# rescued: 499 GB, non-tried: 0 B, bad-sector: 12 KB
```

---

## Filesystem Recovery

```bash
# When filesystem is corrupted, recovery tools help

# Check and repair ext4 (on image, not original!)
sudo e2fsck -n /forensics/images/disk.dd
# -n = no changes (read-only check)

# Recover superblock
sudo dumpe2fs /forensics/images/disk.dd | grep superblock
# Backup superblock at 32768, 98304, 163840...

sudo e2fsck -b 32768 /forensics/images/disk.dd

# TestDisk - recover lost partitions
sudo apt install testdisk
testdisk /forensics/images/disk.dd
# Interactive: Analyse -> Quick Search -> List Files

# Recover deleted partitions
testdisk /forensics/images/disk.dd
# Select disk -> Analyse -> Deeper Search
```

---

## eMMC and Flash Storage Forensics

```bash
# eMMC is common in phones, tablets, IoT devices
# Similar to SSD but simpler interface

# Identify eMMC devices
ls /dev/mmcblk*
lsblk | grep mmcblk

# Read eMMC info
cat /sys/class/mmc_host/mmc0/mmc0:*/cid  # Card ID
cat /sys/class/mmc_host/mmc0/mmc0:*/name  # Name
cat /sys/class/mmc_host/mmc0/mmc0:*/serial  # Serial

# Image eMMC
sudo dd if=/dev/mmcblk0 of=/evidence/emmc.dd bs=4M status=progress

# eMMC forensic considerations:
# - TRIM support varies
# - Wear leveling less aggressive than SSDs
# - Boot partitions may contain additional data
# - RPMB (Replay Protected Memory Block) region
sudo mmc extcsd read /dev/mmcblk0  # Extended CSD register
```

---

## Virtual Machine Disk Forensics

```bash
# VM disk formats:
# VMDK (VMware), VDI (VirtualBox), QCOW2 (QEMU/KVM), VHD/VHDX (Hyper-V)

# Convert VMDK to raw for analysis
qemu-img convert -f vmdk -O raw vm_disk.vmdk /evidence/vm_disk.dd

# Convert QCOW2 to raw
qemu-img convert -f qcow2 -O raw vm_disk.qcow2 /evidence/vm_disk.dd

# Convert VDI to raw
qemu-img convert -f vdi -O raw vm_disk.vdi /evidence/vm_disk.dd

# QCOW2 snapshots may contain previous states
qemu-img info vm_disk.qcow2
# Snapshots:
# ID  TAG    VM SIZE    DATE
# 1   snap1  256M       2025-01-10

# Mount QCOW2 directly (with qemu-nbd)
sudo modprobe nbd
sudo qemu-nbd -c /dev/nbd0 vm_disk.qcow2
sudo mount -o ro /dev/nbd0p1 /mnt/evidence
```

---

## Cloud Storage Forensics

```bash
# Cloud instances use virtual block devices
# Forensic imaging depends on cloud provider

# AWS: Create EBS snapshot
# aws ec2 create-snapshot --volume-id vol-xxxx --description "Forensic"

# Convert snapshot to image
# aws ec2 create-image --instance-id i-xxxx --name "forensic-image"

# Download snapshot data
# Use aws ec2 get-ebs-snapshot or mount as volume

# Azure: Managed disk snapshot
# az snapshot create --resource-group RG --name forensic-snap \
#   --source /subscriptions/.../disks/disk1

# GCP: Create disk snapshot
# gcloud compute disks snapshot disk-name --snapshot-names forensic-snap

# General considerations:
# - Volatile data (RAM) often not accessible
# - Network logs from cloud provider
# - API audit logs (CloudTrail, Activity Log)
# - Object storage versioning may preserve deleted files
```

---

## Disk Encryption Detection

```bash
# Detect encrypted volumes before imaging

# LUKS detection
sudo cryptsetup isLuks /dev/sdb1 && echo "LUKS detected" || echo "Not LUKS"
sudo cryptsetup luksDump /dev/sdb1

# Check for LUKS header signature
xxd -l 6 /dev/sdb1
# 4c55 4b53 = LUKS signature

# BitLocker detection
xxd -l 3 /dev/sdb1
# If -FVE-FS- at offset 3, it's BitLocker

# VeraCrypt detection
# No header signature - appears random
# High entropy suggests encryption
ent /dev/sdb1  # If close to 8.0, likely encrypted

# eCryptfs markers
ls /home/.ecryptfs/
file /home/.ecryptfs/*/\.Private/*

# FileVault (macOS)
# Core Storage or APFS encrypted volume headers
```

---

## Exercise: Advanced Hardware Lab

### Tasks:
1. Identify all storage devices including NVMe and USB
1. Check for HPA/DCO on available drives
1. Review USB connection history from system logs
1. Image a USB device with hash verification
1. Detect any encrypted volumes

```bash
#!/bin/bash
echo "=== All Block Devices ==="
lsblk -o NAME,SIZE,TYPE,FSTYPE,TRAN,SERIAL,MODEL,RO
echo ""
echo "=== NVMe Devices ==="
sudo nvme list 2>/dev/null || echo "No NVMe"
echo ""
echo "=== USB History ==="
journalctl | grep -i "usb" | grep -i "product" | tail -10
echo ""
echo "=== Encrypted Volumes ==="
for dev in /dev/sd?? /dev/nvme?n?p?; do
  [ -e "$dev" ] && sudo cryptsetup isLuks "$dev" 2>/dev/null && \
    echo "LUKS: $dev"
done
```

---

## Storage Device Types

![storage_device_types](svg/courses/security/linux-forensics/01_hardware/storage_device_types.svg)

---

## RAID Levels Overview

![raid_levels_overview](svg/courses/security/linux-forensics/01_hardware/raid_levels_overview.svg)

---

## System Buses Overview

![system_buses_overview](svg/courses/security/linux-forensics/01_hardware/system_buses_overview.svg)
