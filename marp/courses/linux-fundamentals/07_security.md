# Security in Practice
## Understanding UNIX Security Mechanisms
---
## UNIX Accounts

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">UNIX Account Model</text>
  <defs>
    <marker id="arrowacct" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="200" y="35" width="200" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="60" text-anchor="middle" font-size="12" font-weight="bold">root (UID 0)</text>
  <line x1="300" y1="75" x2="150" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrowacct)"/>
  <line x1="300" y1="75" x2="450" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrowacct)"/>
  <rect x="50" y="100" width="200" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="150" y="118" text-anchor="middle" font-size="11" font-weight="bold">Regular Users (UID 1000+)</text>
  <rect x="350" y="100" width="200" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="450" y="118" text-anchor="middle" font-size="11" font-weight="bold">System Users (UID 1-999)</text>
  <rect x="50" y="155" width="130" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="4"/>
  <text x="115" y="174" text-anchor="middle" font-size="10">john (1000)</text>
  <rect x="195" y="155" width="130" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="4"/>
  <text x="260" y="174" text-anchor="middle" font-size="10">alice (1001)</text>
  <rect x="350" y="155" width="130" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" rx="4"/>
  <text x="415" y="174" text-anchor="middle" font-size="10">nginx (998)</text>
  <rect x="495" y="155" width="80" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" rx="4"/>
  <text x="535" y="174" text-anchor="middle" font-size="10">mysql (27)</text>
</svg>

Key components:
- Username (human readable)
- UID (system identifier)
- Group memberships
- Home directory
- Default shell

---
## The /etc/passwd File

Structure:

```txt
username:x:UID:GID:comment:home:shell
```

Example entries:

```bash
root:x:0:0:root:/root:/bin/bash
john:x:1000:1000:John Doe:/home/john:/bin/bash
nginx:x:998:998:Nginx web server:/var/www:/sbin/nologin
```

View entries:

```bash
# View all entries
cat /etc/passwd

# Get specific user
grep "^john:" /etc/passwd

# Count users
wc -l /etc/passwd
```

---
## The `/etc/shadow` File

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">/etc/shadow: Password Storage</text>
  <rect x="30" y="40" width="540" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="57" text-anchor="middle" font-size="10" font-family="monospace">john:$6$salt$hash...:18900:0:99999:7:::</text>
  <text x="300" y="72" text-anchor="middle" font-size="9" fill="#666">username : hashed_password : last_change : min : max : warn : inactive : expire</text>
  <rect x="30" y="95" width="120" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="90" y="112" text-anchor="middle" font-size="10" font-weight="bold">$1$</text>
  <text x="90" y="127" text-anchor="middle" font-size="9">MD5 (weak)</text>
  <rect x="170" y="95" width="120" height="40" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="230" y="112" text-anchor="middle" font-size="10" font-weight="bold">$5$</text>
  <text x="230" y="127" text-anchor="middle" font-size="9">SHA-256</text>
  <rect x="310" y="95" width="120" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="370" y="112" text-anchor="middle" font-size="10" font-weight="bold">$6$</text>
  <text x="370" y="127" text-anchor="middle" font-size="9">SHA-512 (best)</text>
  <rect x="450" y="95" width="120" height="40" fill="#ffebee" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="510" y="112" text-anchor="middle" font-size="10" font-weight="bold">$y$</text>
  <text x="510" y="127" text-anchor="middle" font-size="9">yescrypt (new)</text>
  <rect x="30" y="150" width="540" height="35" fill="#ffebee" stroke="#333" stroke-width="1" rx="4" opacity="0.5"/>
  <text x="300" y="172" text-anchor="middle" font-size="10">Only root can read /etc/shadow (permissions: 640, owner root:shadow)</text>
</svg>

Structure:

```txt
username:password:lastchg:min:max:warn:inactive:expire:
```

Example:

```bash
john:$6$xyz...:18900:0:99999:7:::
```

---
## File Ownership

```bash
# View file ownership
ls -l file.txt

# Change owner
chown john file.txt

# Change group
chgrp developers file.txt

# Change both
chown john:developers file.txt

# Recursive change
chown -R john:developers directory/
```

Output example:

```txt
-rw-r--r-- 1 john developers 4096 Nov 19 10:00 file.txt
```

---
## Directory and File Access Modes

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Permission Bits: Owner / Group / Others</text>
  <rect x="50" y="35" width="500" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="57" text-anchor="middle" font-size="13" font-family="monospace" font-weight="bold">r w x   r w x   r w x</text>
  <text x="300" y="78" text-anchor="middle" font-size="11" font-family="monospace" fill="#666">owner   group   others</text>
  <rect x="50" y="105" width="160" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="130" y="122" text-anchor="middle" font-size="11" font-weight="bold">r = 4 (read)</text>
  <text x="130" y="137" text-anchor="middle" font-size="10">view contents</text>
  <rect x="220" y="105" width="160" height="40" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="300" y="122" text-anchor="middle" font-size="11" font-weight="bold">w = 2 (write)</text>
  <text x="300" y="137" text-anchor="middle" font-size="10">modify contents</text>
  <rect x="390" y="105" width="160" height="40" fill="#ffebee" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="470" y="122" text-anchor="middle" font-size="11" font-weight="bold">x = 1 (execute)</text>
  <text x="470" y="137" text-anchor="middle" font-size="10">run / traverse</text>
  <rect x="50" y="160" width="500" height="30" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="4" opacity="0.7"/>
  <text x="300" y="180" text-anchor="middle" font-size="11" font-family="monospace">chmod 754 = rwxr-xr-- (7=rwx, 5=r-x, 4=r--)</text>
</svg>

Symbolic notation:

```txt
rwxr-xr--
│││││││││
││││││││└─ Others: no execute
│││││││└── Others: no write
││││││└─── Others: read
│││││└──── Group: no execute
││││└───── Group: no write
│││└────── Group: read
││└─────── User: execute
│└──────── User: write
└───────── User: read
```

---
## Understanding Permission Bits

Permission calculation:

```txt
r = 4 (100 binary)
w = 2 (010 binary)
x = 1 (001 binary)
```

Examples:

```txt
rwx = 7 (4+2+1)
rw- = 6 (4+2+0)
r-x = 5 (4+0+1)
r-- = 4 (4+0+0)
```

Full permission string:

```txt
chmod 754 file.txt
# rwxr-xr--
# 7   5   4
```

---
## How File Access is Determined

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">File Access Decision Flow</text>
  <defs>
    <marker id="arrowaccess" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="40" width="130" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="63" text-anchor="middle" font-size="11" font-weight="bold">Process (UID)</text>
  <line x1="160" y1="57" x2="190" y2="57" stroke="#333" stroke-width="2" marker-end="url(#arrowaccess)"/>
  <rect x="190" y="40" width="130" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="15"/>
  <text x="255" y="62" text-anchor="middle" font-size="10">Is owner?</text>
  <line x1="255" y1="75" x2="255" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrowaccess)"/>
  <text x="243" y="92" font-size="9" fill="#c00">No</text>
  <rect x="190" y="100" width="130" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="15"/>
  <text x="255" y="122" text-anchor="middle" font-size="10">In group?</text>
  <line x1="255" y1="135" x2="255" y2="160" stroke="#333" stroke-width="1.5" marker-end="url(#arrowaccess)"/>
  <text x="243" y="152" font-size="9" fill="#c00">No</text>
  <rect x="190" y="160" width="130" height="30" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="255" y="180" text-anchor="middle" font-size="10">Use "other" perms</text>
  <line x1="320" y1="57" x2="390" y2="57" stroke="#333" stroke-width="1.5" marker-end="url(#arrowaccess)"/>
  <text x="350" y="50" font-size="9" fill="#090">Yes</text>
  <rect x="390" y="40" width="170" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="475" y="62" text-anchor="middle" font-size="10">Use "owner" perms</text>
  <line x1="320" y1="117" x2="390" y2="117" stroke="#333" stroke-width="1.5" marker-end="url(#arrowaccess)"/>
  <text x="350" y="110" font-size="9" fill="#090">Yes</text>
  <rect x="390" y="100" width="170" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="475" y="122" text-anchor="middle" font-size="10">Use "group" perms</text>
</svg>

Access check order:
1. Is user the owner?
1. Is user in the group?
1. What are "other" permissions?
---
## Changing Modes and Ownership

Symbolic mode:

```bash
# Add execute for user
chmod u+x file.txt

# Remove write for group
chmod g-w file.txt

# Set read-write for all
chmod a=rw file.txt

# Add execute for user and group
chmod ug+x file.txt
```

Octal mode:

```bash
# rwxr-xr--
chmod 754 file.txt

# rwxrwxrwx
chmod 777 file.txt

# r--------
chmod 400 file.txt
```

---
## Special Permissions

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Special Permission Bits</text>
  <rect x="20" y="40" width="180" height="90" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="62" text-anchor="middle" font-size="11" font-weight="bold">SUID (4xxx)</text>
  <text x="110" y="78" text-anchor="middle" font-size="10">Run as file owner</text>
  <text x="110" y="95" text-anchor="middle" font-size="9" font-family="monospace">-rwsr-xr-x</text>
  <text x="110" y="118" text-anchor="middle" font-size="9" fill="#666">e.g. /usr/bin/passwd</text>
  <rect x="210" y="40" width="180" height="90" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="62" text-anchor="middle" font-size="11" font-weight="bold">SGID (2xxx)</text>
  <text x="300" y="78" text-anchor="middle" font-size="10">Run as file group</text>
  <text x="300" y="95" text-anchor="middle" font-size="9" font-family="monospace">-rwxr-sr-x</text>
  <text x="300" y="118" text-anchor="middle" font-size="9" fill="#666">Dir: inherit group</text>
  <rect x="400" y="40" width="180" height="90" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="490" y="62" text-anchor="middle" font-size="11" font-weight="bold">Sticky (1xxx)</text>
  <text x="490" y="78" text-anchor="middle" font-size="10">Only owner deletes</text>
  <text x="490" y="95" text-anchor="middle" font-size="9" font-family="monospace">drwxrwxrwt</text>
  <text x="490" y="118" text-anchor="middle" font-size="9" fill="#666">e.g. /tmp</text>
  <rect x="20" y="150" width="560" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="4" opacity="0.6"/>
  <text x="300" y="168" text-anchor="middle" font-size="10" font-family="monospace">chmod 4755 file  |  chmod 2755 dir  |  chmod 1777 /tmp</text>
</svg>

Examples:

```bash
# Set SUID
chmod u+s file.txt
chmod 4755 file.txt

# Set SGID
chmod g+s directory
chmod 2755 directory

# Set sticky bit
chmod +t directory
chmod 1755 directory
```

---
## The umask Command

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">umask: Default Permission Mask</text>
  <defs>
    <marker id="arrowumask" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="40" width="160" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="65" text-anchor="middle" font-size="11" font-weight="bold">Default: 0666/0777</text>
  <line x1="190" y1="60" x2="230" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowumask)"/>
  <text x="210" y="52" text-anchor="middle" font-size="9">minus</text>
  <rect x="230" y="40" width="140" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="65" text-anchor="middle" font-size="11" font-weight="bold">umask: 022</text>
  <line x1="370" y1="60" x2="410" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowumask)"/>
  <text x="390" y="52" text-anchor="middle" font-size="9">equals</text>
  <rect x="410" y="40" width="160" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="490" y="65" text-anchor="middle" font-size="11" font-weight="bold">Result: 0644/0755</text>
  <rect x="30" y="100" width="260" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="4"/>
  <text x="160" y="115" text-anchor="middle" font-size="10" font-weight="bold">umask 022 (common)</text>
  <text x="160" y="128" text-anchor="middle" font-size="10">files: rw-r--r-- dirs: rwxr-xr-x</text>
  <rect x="310" y="100" width="260" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="4"/>
  <text x="440" y="115" text-anchor="middle" font-size="10" font-weight="bold">umask 077 (strict)</text>
  <text x="440" y="128" text-anchor="middle" font-size="10">files: rw------- dirs: rwx------</text>
  <rect x="30" y="155" width="540" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="4" opacity="0.5"/>
  <text x="300" y="175" text-anchor="middle" font-size="10">umask bits are removed from default permissions when creating new files/dirs</text>
</svg>

Common umask values:

```bash
# View current umask
umask

# Set stricter permissions
umask 027  # rwxr-x---

# Set common permissions
umask 022  # rwxr-xr-x
```

---
## Practical Security Examples

1. Setting up a shared directory:

```bash
# Create directory
mkdir /shared
# Set ownership
chown root:developers /shared
# Set permissions
chmod 2775 /shared  # SGID + rwxrwxr-x
```

1. Securing sensitive files:

```bash
# Create private directory
mkdir ~/.private
# Set restrictive permissions
chmod 700 ~/.private
# Set secure umask
umask 077
```

---
## Security Best Practices

1. File Permissions:

```bash
# Secure configuration files
chmod 600 ~/.ssh/config
chmod 644 ~/.bashrc

# Secure directories
chmod 755 ~/public_html
chmod 700 ~/.ssh
```

1. Group Management:

```bash
# Create group
sudo groupadd developers

# Add user to group
sudo usermod -aG developers john

# Check group membership
groups john
```

---
## Advanced Security Topics

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Advanced Security: ACLs and Beyond</text>
  <defs>
    <marker id="arrowadv" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="40" width="160" height="65" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="60" text-anchor="middle" font-size="11" font-weight="bold">Traditional</text>
  <text x="110" y="76" text-anchor="middle" font-size="10">owner/group/other</text>
  <text x="110" y="92" text-anchor="middle" font-size="10">rwx bits only</text>
  <line x1="190" y1="72" x2="220" y2="72" stroke="#333" stroke-width="2" marker-end="url(#arrowadv)"/>
  <rect x="220" y="40" width="160" height="65" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="60" text-anchor="middle" font-size="11" font-weight="bold">POSIX ACLs</text>
  <text x="300" y="76" text-anchor="middle" font-size="10">setfacl / getfacl</text>
  <text x="300" y="92" text-anchor="middle" font-size="10">per-user/group rules</text>
  <line x1="380" y1="72" x2="410" y2="72" stroke="#333" stroke-width="2" marker-end="url(#arrowadv)"/>
  <rect x="410" y="40" width="165" height="65" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="492" y="60" text-anchor="middle" font-size="11" font-weight="bold">SELinux/AppArmor</text>
  <text x="492" y="76" text-anchor="middle" font-size="10">Mandatory Access</text>
  <text x="492" y="92" text-anchor="middle" font-size="10">Control (MAC)</text>
  <rect x="30" y="125" width="545" height="55" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5" opacity="0.7"/>
  <text x="300" y="145" text-anchor="middle" font-size="10" font-family="monospace">setfacl -m u:john:rx file.txt    # grant john read+execute</text>
  <text x="300" y="162" text-anchor="middle" font-size="10" font-family="monospace">getfacl file.txt                 # view all ACL entries</text>
</svg>

Example with ACLs:

```bash
# Set ACL
setfacl -m u:john:rx file.txt

# View ACLs
getfacl file.txt

# Remove ACL
setfacl -x u:john file.txt
```
