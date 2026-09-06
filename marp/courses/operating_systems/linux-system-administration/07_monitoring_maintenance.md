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

# System Monitoring and Maintenance
## Performance, Logs, Automation, and Disaster Recovery

---

## Performance Monitoring: top and htop

```bash
# top - built-in process monitor
top
# Key shortcuts:
#   P - sort by CPU
#   M - sort by memory
#   k - kill a process
#   1 - show per-CPU stats

# htop - improved interactive monitor
htop
# Features: tree view, mouse support,
# horizontal/vertical scrolling
```

---

## Understanding top Output

```console
top - 14:30:00 up 42 days, load average: 1.50, 1.30, 1.20
Tasks: 200 total,   2 running, 198 sleeping
%Cpu(s): 15.0 us,  3.0 sy,  0.0 ni, 80.0 id, 2.0 wa
MiB Mem:  16384.0 total,  2048.0 free,  8192.0 used
MiB Swap:  4096.0 total,  4000.0 free,    96.0 used
```

Key metrics:
- **load average**: 1/5/15 min (compare to CPU count)
- **us**: user space CPU, **sy**: kernel CPU
- **wa**: I/O wait (high = disk bottleneck)
- **id**: idle time
- Swap usage increasing = memory pressure

---

## Performance Monitoring: vmstat, iostat, sar

```bash
# vmstat - virtual memory statistics
vmstat 1 5          # every 1 sec, 5 times
# Key columns: r(run queue), free, si/so(swap),
# us/sy/id(cpu)

# iostat - I/O statistics
iostat -xz 1        # extended, skip idle devices

# sar - system activity reporter
sar -u 1 5          # CPU usage
sar -r 1 5          # memory usage
sar -d 1 5          # disk I/O
sar -n DEV 1 5      # network stats
sar -q 1 5          # load average
```

---

## sar Historical Data

```bash
# sar stores data in /var/log/sysstat/

# View yesterday's CPU usage
sar -u -f /var/log/sysstat/sa$(date -d yesterday +%d)

# View specific time range
sar -u -s 09:00:00 -e 17:00:00

# Enable sar data collection
apt install sysstat
# Edit /etc/default/sysstat: ENABLED="true"
systemctl enable --now sysstat

# Generate report for specific day
sar -A -f /var/log/sysstat/sa15 > report.txt
```

Historical `sar` data is invaluable for capacity planning and post-incident analysis.

---

## Performance Monitoring: dstat

`dstat` combines `vmstat`, `iostat`, `netstat`, and `ifstat` into one tool.

```bash
# Install
apt install dstat

# Default output (CPU, disk, net, paging, system)
dstat

# Specific resources
dstat -c            # CPU only
dstat -d            # disk only
dstat -n            # network only
dstat -m            # memory only

# Combined view with 2-second interval
dstat -cdnm 2

# Top CPU and memory consumers
dstat --top-cpu --top-mem

# Output to CSV for analysis
dstat -cdnm --output stats.csv 5
```

---

## dstat Plugins and Advanced Usage

```bash
# List available plugins
dstat --list

# Useful plugin combinations
dstat -cdnm --top-io --top-cpu 2

# Disk utilization per device
dstat -d -D sda,sdb 1

# Network per interface
dstat -n -N eth0,eth1 1

# Full system overview
dstat -tclmdnr --top-cpu --top-mem 5
# -t: timestamp, -l: load avg, -r: disk requests

# Compare CPU wait vs disk I/O
dstat -c -d --disk-util 1
```

Note: on newer systems, `dstat` may be replaced by `pcp-dstat` (Performance Co-Pilot).

---

## Memory Analysis in Depth

```bash
# Detailed memory breakdown
free -h

# Per-process memory usage
ps aux --sort=-%mem | head -20

# Shared memory segments
ipcs -m

# View memory maps for a process
pmap -x <PID>

# Check OOM killer log
dmesg | grep -i "out of memory"
journalctl -k | grep -i oom

# View slab cache (kernel memory)
slabtop

# Drop filesystem caches (for testing)
sync; echo 3 > /proc/sys/vm/drop_caches
```

---

## CPU Analysis Tools

```bash
# Per-CPU statistics
mpstat -P ALL 1 5

# Process CPU accounting
pidstat 1 5

# View CPU frequency and governor
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
cpupower frequency-info

# Set CPU governor
cpupower frequency-set -g performance

# View hardware interrupts per CPU
cat /proc/interrupts

# Perf for CPU profiling
perf top                    # live CPU profiling
perf stat -p <PID>          # process stats
perf record -p <PID> -g     # record for analysis
perf report                 # view recorded data
```

---

## Troubleshooting: strace

```bash
# Trace system calls of a command
strace ls /tmp

# Trace a running process
strace -p <PID>

# Trace specific syscalls
strace -e open,read,write ls /tmp

# Count syscalls
strace -c ls /tmp

# Follow child processes
strace -f ./my_program

# Output to file
strace -o trace.log ls /tmp
```

---

## strace Practical Examples

```bash
# Debug "file not found" issues
strace -e openat,access myapp 2>&1 | grep -i "no such"

# Debug network issues
strace -e connect,sendto,recvfrom myapp

# Find config files being read
strace -e openat myapp 2>&1 | grep "/etc/"

# Measure time spent in each syscall
strace -T myapp 2>&1 | tail -20

# Debug DNS resolution
strace -e connect,socket getent hosts example.com

# Time-stamp each syscall
strace -tt -o trace.log myapp
```

---

## Troubleshooting: lsof and dmesg

```bash
# lsof - list open files
lsof -i :80              # who's using port 80
lsof -u alice            # files opened by user
lsof +D /var/log         # files in directory
lsof -p <PID>            # files by process
lsof /dev/sda1           # processes using device
```

```bash
# dmesg - kernel ring buffer
dmesg                    # all kernel messages
dmesg -T                 # human-readable time
dmesg -l err,warn        # errors and warnings
dmesg -w                 # follow (like tail -f)
dmesg | grep -i usb      # filter for USB events
```

---

## Troubleshooting: Additional Tools

```bash
# ltrace - trace library calls
ltrace -p <PID>
ltrace -e malloc+free myapp

# ss - check socket states
ss -tnp state time-wait | wc -l
ss -tnp state established

# ip utility for network troubleshooting
ip -s link show eth0     # interface statistics
ip -s neigh show         # ARP with stats

# systemd-analyze for slow boots
systemd-analyze blame
systemd-analyze critical-chain nginx.service
systemd-analyze plot > boot.svg
```

---

## Log Management: logrotate

```bash
# Main config: /etc/logrotate.conf
# Per-app configs: /etc/logrotate.d/
```

```config
# /etc/logrotate.d/myapp
/var/log/myapp/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data adm
    postrotate
        systemctl reload myapp
    endscript
}
```

```bash
# Test rotation
logrotate -d /etc/logrotate.d/myapp

# Force rotation
logrotate -f /etc/logrotate.d/myapp
```

---

## logrotate Options Reference

| Option | Purpose |
|--------|---------|
| `daily/weekly/monthly` | Rotation frequency |
| `rotate N` | Keep N old files |
| `compress` | gzip old files |
| `delaycompress` | Compress on next rotation |
| `missingok` | Don't error if log missing |
| `notifempty` | Don't rotate if empty |
| `copytruncate` | Copy then truncate (no restart) |
| `sharedscripts` | Run postrotate once for all |
| `maxsize 100M` | Rotate if file exceeds size |
| `minsize 10M` | Don't rotate if below size |
| `dateext` | Use date in rotated filename |

---

## Log Management: rsyslog

```bash
# Main config: /etc/rsyslog.conf
# Additional configs: /etc/rsyslog.d/
```

```config
# /etc/rsyslog.d/50-custom.conf
# Log all auth messages to separate file
auth,authpriv.*   /var/log/auth.log

# Send logs to remote server
*.* @logserver.example.com:514       # UDP
*.* @@logserver.example.com:514      # TCP

# Log specific program
:programname, isequal, "myapp" /var/log/myapp.log
```

---

## Centralized Logging with rsyslog

```config
# rsyslog server config (/etc/rsyslog.d/server.conf)

# Listen on TCP 514
module(load="imtcp")
input(type="imtcp" port="514")

# Template: separate log per host
template(name="RemoteLogs"
  type="string"
  string="/var/log/remote/%HOSTNAME%/%PROGRAMNAME%.log")

# Apply template to remote logs
if $fromhost-ip != '127.0.0.1' then {
    action(type="omfile" dynaFile="RemoteLogs")
    stop
}
```

```bash
# Client: forward all logs
# *.* @@logserver.example.com:514
systemctl restart rsyslog
```

---

## Automated Monitoring: Prometheus and Grafana
![automated_monitoring_prometheus_and_grafana](svg/courses/operating_systems/linux-system-administration/07_monitoring_maintenance/automated_monitoring_prometheus_and_grafana.svg)

---

## Automated Monitoring: Prometheus and Grafana: Details

- `Prometheus` scrapes metrics from targets
- `Grafana` visualizes metrics with dashboards
- `Alertmanager` handles alerts and notifications
- `node_exporter` exposes system metrics

---

## Prometheus Configuration

```yaml
# /etc/prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['localhost:9093']

scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets:
          - 'server1:9100'
          - 'server2:9100'
          - 'server3:9100'
```

---

## Prometheus Alert Rules

```yaml
# /etc/prometheus/alert_rules.yml
groups:
  - name: system
    rules:
      - alert: HighCPU
        expr: 100 - (avg by(instance)
          (irate(node_cpu_seconds_total
          {mode="idle"}[5m])) * 100) > 90
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU on {{ $labels.instance }}"

      - alert: DiskSpaceLow
        expr: node_filesystem_avail_bytes
          / node_filesystem_size_bytes < 0.1
        for: 10m
        labels:
          severity: critical
```

---

## Monitoring with Nagios/Zabbix

- `Nagios` - traditional, plugin-based monitoring
    - Checks: host up/down, service status, custom
    - Notifications via email, SMS, webhooks
- `Zabbix` - enterprise monitoring with auto-discovery
    - Agent-based and agentless monitoring
    - Built-in graphing and alerting
    - Template-based configuration

Both support:
- Custom check scripts
- Escalation policies
- Distributed monitoring

---

## Scheduled Tasks: crontab

```bash
# Edit user crontab
crontab -e

# List current crontab
crontab -l
```

```cron
# Crontab format:
# min hour dom month dow command
# ┌───── minute (0-59)
# │ ┌───── hour (0-23)
# │ │ ┌───── day of month (1-31)
# │ │ │ ┌───── month (1-12)
# │ │ │ │ ┌───── day of week (0-6, Sun=0)
  0 2 * * * /usr/local/bin/backup.sh
 30 * * * * /usr/bin/check-health.sh
  0 0 1 * * /usr/local/bin/monthly-report.sh
```

---

## crontab Advanced Usage

```bash
# System-wide crontab
cat /etc/crontab

# Drop-in directories
ls /etc/cron.daily/
ls /etc/cron.weekly/
ls /etc/cron.monthly/

# Restrict cron access
# /etc/cron.allow - whitelist (if exists, deny all others)
# /etc/cron.deny  - blacklist

# Common patterns
*/5 * * * *     # every 5 minutes
0 */2 * * *     # every 2 hours
0 9-17 * * 1-5  # hourly during business hours
@reboot         # run once at boot
@daily          # same as 0 0 * * *
```

---

## Scheduled Tasks: at and systemd Timers

```bash
# at - one-time scheduled task
at now + 2 hours <<EOF
/usr/local/bin/generate-report.sh
EOF

# List pending at jobs
atq

# Remove an at job
atrm 5
```

`systemd` timers (covered in chapter 1) offer advantages:
- Logged via `journalctl`
- Dependency management
- Calendar expressions (`OnCalendar=Mon..Fri *-*-* 09:00`)
- Persistent: runs missed jobs after reboot

---

## Disaster Recovery Planning

Key components:
- **RPO** (Recovery Point Objective) - max acceptable data loss
- **RTO** (Recovery Time Objective) - max acceptable downtime

Checklist:
1. Documented backup and restore procedures
1. Regular backup verification and restore testing
1. Off-site backup copies
1. System configuration under version control
1. Runbooks for common failure scenarios
1. Contact escalation procedures

---

## Disaster Recovery: Practical Steps

```bash
# 1. Document system state
dpkg --get-selections > packages.txt
crontab -l > crontab.txt
iptables-save > iptables.txt
tar czf /backup/etc-$(date +%F).tar.gz /etc

# 2. Create bootable rescue media
# Keep Ubuntu Live USB ready

# 3. Test restore procedure regularly
# Restore to a test VM, verify services

# 4. Bare-metal recovery script
#!/bin/bash
# Restore packages
dpkg --set-selections < packages.txt
apt-get dselect-upgrade
# Restore configs
tar xzf /backup/etc-latest.tar.gz -C /
# Restore data
borg extract /backup/repo::latest
```

---

## System Updates and Patches

```bash
# Check for updates
apt update
apt list --upgradable

# Apply security updates only
apt upgrade --only-upgrade
unattended-upgrades --dry-run

# Configure automatic security updates
apt install unattended-upgrades
dpkg-reconfigure unattended-upgrades

# View update history
cat /var/log/apt/history.log

# Rollback (if using snapshots)
# Take snapshot before updates, revert if needed
```

---

## Unattended Upgrades Configuration

```config
# /etc/apt/apt.conf.d/50unattended-upgrades
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
};

Unattended-Upgrade::Package-Blacklist {
    "linux-image*";
    "linux-headers*";
};

Unattended-Upgrade::AutoFixInterruptedDpkg "true";
Unattended-Upgrade::Mail "admin@example.com";
Unattended-Upgrade::MailReport "on-change";
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "false";
```

---

## Automation with Ansible

```yaml
# inventory.ini
# [webservers]
# web1.example.com
# web2.example.com

# playbook.yml
- hosts: webservers
  become: yes
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Start nginx
      systemd:
        name: nginx
        state: started
        enabled: yes
```

```bash
ansible-playbook -i inventory.ini playbook.yml
```

---

## Ansible Advanced Usage

```yaml
# roles/webserver/tasks/main.yml
- name: Install packages
  apt:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - certbot
    - python3-certbot-nginx

- name: Deploy nginx config
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/sites-available/default
  notify: Restart nginx

- name: Ensure nginx is running
  systemd:
    name: nginx
    state: started
    enabled: yes
```

```yaml
# handlers
- name: Restart nginx
  systemd:
    name: nginx
    state: restarted
```

---

## Ansible Ad-Hoc Commands

```bash
# Ping all hosts
ansible all -i inventory.ini -m ping

# Run command on all hosts
ansible all -m shell -a "uptime"

# Check disk space
ansible all -m shell -a "df -h /"

# Install package on specific group
ansible webservers -m apt -a "name=nginx state=present" -b

# Copy file to all hosts
ansible all -m copy -a "src=config.txt dest=/etc/myconfig"

# Gather facts
ansible all -m setup -a "filter=ansible_os_family"
```

---

## Best Practices for Production

1. **Change management** - no ad-hoc changes, use IaC
1. **Monitoring** - set up alerts before something breaks
1. **Backups** - test restores regularly
1. **Security** - patch promptly, principle of least privilege
1. **Documentation** - runbooks, architecture diagrams
1. **Logging** - centralized logging with retention policies
1. **Automation** - repeatable deployments
1. **Capacity planning** - trend analysis, proactive scaling

---

## Production Runbook Template

Every critical service should have a runbook:

1. **Service overview** - what it does, who owns it
1. **Architecture** - dependencies, data flow
1. **Health checks** - how to verify it's working
1. **Common alerts** - what they mean, how to resolve
1. **Restart procedure** - safe restart steps
1. **Scaling** - how to add capacity
1. **Disaster recovery** - full rebuild from scratch
1. **Contact list** - who to escalate to

```bash
# Store runbooks in version control
# alongside infrastructure code
git init /opt/runbooks
```

---

## Process Accounting

Track resource usage per process and per user with `psacct`/`acct`.

```bash
# Install process accounting
apt install acct

# Enable accounting
systemctl enable --now acct

# Summary of commands by user
ac -p                  # connect time per user
sa                     # summary of commands
sa -u                  # per-user command summary

# Last commands run by a user
lastcomm alice
lastcomm --command curl

# Daily accounting report
ac -dp                 # daily connect time per user
```

---

## /proc/meminfo Deep Dive

```bash
# Key fields explained
cat /proc/meminfo
```

| Field | Meaning |
|-------|---------|
| `MemTotal` | Total physical RAM |
| `MemFree` | Completely unused RAM |
| `MemAvailable` | Estimated available for new apps |
| `Buffers` | Block device I/O cache |
| `Cached` | Page cache (file contents) |
| `SwapTotal/Free` | Swap space usage |
| `Dirty` | Data waiting to be written to disk |
| `Slab` | Kernel data structure cache |
| `SReclaimable` | Slab memory that can be freed |

```bash
# Available memory = MemFree + Buffers + Cached + SReclaimable
# This is what MemAvailable approximates

# Monitor dirty pages (pending writes)
watch -n 1 'grep -E "Dirty|Writeback" /proc/meminfo'
```

---

## BPF and bpftrace

`BPF` (Berkeley Packet Filter) enables safe kernel-level tracing without recompilation.

```bash
# Install bpftrace
apt install bpftrace

# Count syscalls by process
bpftrace -e 'tracepoint:raw_syscalls:sys_enter {
  @[comm] = count(); }'

# Trace file opens
bpftrace -e 'tracepoint:syscalls:sys_enter_openat {
  printf("%s %s\n", comm, str(args->filename)); }'

# Histogram of read sizes
bpftrace -e 'tracepoint:syscalls:sys_exit_read /args->ret > 0/ {
  @bytes = hist(args->ret); }'

# Trace TCP connections
bpftrace -e 'kprobe:tcp_connect {
  printf("%s connecting\n", comm); }'
```

---

## BPF Tools (bcc)

```bash
# Install BCC tools
apt install bpfcc-tools

# Top processes by disk I/O
biosnoop-bpfcc

# Trace new TCP connections
tcpconnect-bpfcc

# Trace DNS queries
gethostlatency-bpfcc

# Trace file system latency
ext4slower-bpfcc

# CPU scheduler latency
runqlat-bpfcc

# Off-CPU analysis
offcputime-bpfcc -p <PID> 5
```

These tools run in production with minimal overhead due to `BPF` safety guarantees.

---

## Grafana Dashboards

```bash
# Install Grafana
apt install -y grafana
systemctl enable --now grafana-server
# Access at http://localhost:3000 (admin/admin)
```

Key dashboard components:
1. **Data source** - connect to `Prometheus`, `InfluxDB`, etc.
1. **Panels** - graphs, gauges, tables, heatmaps
1. **Variables** - dynamic filters (host, service)
1. **Alerts** - threshold-based notifications

```bash
# Provisioning dashboards as code
# /etc/grafana/provisioning/dashboards/default.yaml
# apiVersion: 1
# providers:
#   - name: 'default'
#     folder: ''
#     type: file
#     options:
#       path: /var/lib/grafana/dashboards
```

---

## Incident Response Checklist

When a production incident occurs:

1. **Detect** - monitoring alerts or user reports
1. **Triage** - assess severity and impact
1. **Communicate** - notify stakeholders, open incident channel
1. **Investigate** - gather data before making changes

```bash
# Capture system state immediately
date > /tmp/incident-$(date +%s).log
uptime >> /tmp/incident-*.log
free -h >> /tmp/incident-*.log
ps auxf >> /tmp/incident-*.log
ss -tlnp >> /tmp/incident-*.log
dmesg -T | tail -50 >> /tmp/incident-*.log
journalctl --since "1 hour ago" >> /tmp/incident-*.log
```

1. **Mitigate** - restore service (restart, failover, rollback)
1. **Resolve** - apply the root cause fix
1. **Postmortem** - blameless review, document lessons learned

---

## Capacity Planning

```bash
# Collect baseline metrics over 30 days
sar -u -f /var/log/sysstat/sa01  # CPU trend
sar -r -f /var/log/sysstat/sa01  # memory trend
sar -d -f /var/log/sysstat/sa01  # disk I/O trend

# Disk growth rate
df -h / | tail -1
# Compare weekly snapshots to project exhaustion date

# Monitor inode usage (often overlooked)
df -i /
```

Key metrics to track for capacity planning:

| Resource | Warning | Critical |
|----------|---------|----------|
| CPU | Sustained > 70% | Sustained > 90% |
| Memory | `MemAvailable` < 20% | `MemAvailable` < 10% |
| Disk | > 80% used | > 90% used |
| Inodes | > 80% used | > 90% used |
| Network | > 70% bandwidth | > 90% bandwidth |

---

## collectd Metrics Collection

`collectd` is a lightweight daemon that collects system metrics and writes them to various backends.

```bash
# Install collectd
apt install collectd

# Key plugins to enable in /etc/collectd/collectd.conf
LoadPlugin cpu
LoadPlugin memory
LoadPlugin disk
LoadPlugin interface
LoadPlugin load
LoadPlugin df
LoadPlugin processes
LoadPlugin write_graphite
```

```bash
# Send metrics to Graphite/InfluxDB
<Plugin write_graphite>
  <Node "graphite">
    Host "graphite.example.com"
    Port "2003"
    Protocol "tcp"
    Prefix "servers."
  </Node>
</Plugin>
```

```bash
systemctl enable --now collectd
# Verify data collection
collectdctl listval
```

---

## /proc/diskstats Explained

`/proc/diskstats` provides raw I/O statistics per block device.

```bash
cat /proc/diskstats
# Major Minor Name  Reads  RMerged RSectors RTime
#   Writes WMerged WSectors WTime IoInProg IoTime WIoTime
```

| Field | Meaning |
|-------|---------|
| Reads completed | Total read operations |
| Reads merged | Adjacent reads combined by scheduler |
| Sectors read | Total sectors read (512 bytes each) |
| Read time (ms) | Total time spent reading |
| Writes completed | Total write operations |
| Writes merged | Adjacent writes combined |
| I/Os in progress | Currently active I/O operations |
| I/O time (ms) | Time with I/O in flight |

```bash
# Calculate IOPS and throughput from diskstats
# Use iostat for a friendlier view
iostat -xz 1
# %util close to 100% = device saturated
# await high = I/O latency issues
```

---

## Network Monitoring with Netdata

`Netdata` provides real-time, per-second monitoring with a built-in web dashboard.

```bash
# Install Netdata
wget -O /tmp/netdata-kickstart.sh \
  https://get.netdata.cloud/kickstart.sh
sh /tmp/netdata-kickstart.sh --stable-channel

# Access dashboard at http://localhost:19999

# Configuration
# /etc/netdata/netdata.conf
# [global]
#   memory mode = dbengine
#   page cache size = 64
#   dbengine multihost disk space = 256
```

Key features:
1. Zero-configuration for most system metrics
1. Per-second granularity by default
1. Built-in health alarms for anomaly detection
1. Low resource footprint (~2% CPU, ~100 MB RAM)

```bash
# Check running alarms
curl -s localhost:19999/api/v1/alarms | python3 -m json.tool
```

---

## systemd Service Watchdogs

`systemd` can automatically restart services that stop responding using the watchdog mechanism.

```bash
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application

[Service]
ExecStart=/usr/local/bin/myapp
Restart=on-failure
RestartSec=5

# Watchdog: service must notify within 30s
WatchdogSec=30
# systemd sends SIGABRT if watchdog times out

# Additional restart controls
StartLimitIntervalSec=300
StartLimitBurst=5
# Max 5 restarts in 300 seconds
```

```bash
# Applications notify the watchdog via sd_notify
# or the systemd-notify command
systemd-notify WATCHDOG=1

# Monitor watchdog status
systemctl show myapp.service | grep Watchdog
journalctl -u myapp.service | grep watchdog
```

---

## Kernel Live Patching

Apply critical kernel patches without rebooting using `livepatch` or `kpatch`.

```bash
# Ubuntu Livepatch (Canonical service)
snap install canonical-livepatch
canonical-livepatch enable <TOKEN>

# Check livepatch status
canonical-livepatch status --verbose
```

```bash
# kpatch (Red Hat / generic approach)
apt install kpatch

# List applied patches
kpatch list

# Apply a patch
kpatch load /path/to/kpatch-module.ko

# Check if system needs a full reboot
# despite live patches
needs-restarting -r    # RHEL/CentOS
cat /var/run/reboot-required  # Ubuntu
```

Benefits:
- Eliminates reboot windows for security patches
- Reduces downtime for production systems
- Patches are verified for safety before application

---

## Configuration Drift Detection

Detect unauthorized or accidental changes to system configuration.

```bash
# Method 1: etckeeper - track /etc in git
apt install etckeeper
# Auto-commits changes to /etc daily and on package install
cd /etc && git log --oneline -10
git diff HEAD~1

# Method 2: debsums - verify installed packages
apt install debsums
debsums --changed       # show modified config files
debsums --silent        # show only errors

# Method 3: Ansible diff mode
ansible all -m shell -a "cat /etc/ssh/sshd_config" \
  --diff --check
```

```bash
# Method 4: custom script for critical files
sha256sum /etc/passwd /etc/shadow /etc/sudoers \
  /etc/ssh/sshd_config > /root/config-checksums.txt
# Compare later
sha256sum -c /root/config-checksums.txt
```

---

## Change Management Workflow
![change_management_workflow](svg/courses/operating_systems/linux-system-administration/07_monitoring_maintenance/change_management_workflow.svg)

---

## Change Management Workflow: Details

Key principles:
1. All changes tracked in version control (IaC)
1. No direct production changes without review
1. Rollback plan documented before deployment
1. Change window agreed upon with stakeholders

---

## Exercise: Set Up Monitoring Stack

Deploy a basic monitoring stack with `Prometheus` and `node_exporter`:

```bash
# 1. Install node_exporter on target hosts
wget https://github.com/prometheus/node_exporter/\
releases/download/v1.7.0/node_exporter-1.7.0.linux-amd64.tar.gz
tar xzf node_exporter-*.tar.gz
cp node_exporter-*/node_exporter /usr/local/bin/

# 2. Create systemd service for node_exporter
# /etc/systemd/system/node_exporter.service
# [Service]
# ExecStart=/usr/local/bin/node_exporter
# User=node_exporter
systemctl enable --now node_exporter

# 3. Configure Prometheus to scrape targets
# /etc/prometheus/prometheus.yml
# scrape_configs:
#   - job_name: 'nodes'
#     static_configs:
#       - targets: ['localhost:9100','server2:9100']

# 4. Add alert rules for disk, CPU, memory
# 5. Install Grafana and import dashboard ID 1860
#    (Node Exporter Full)

# 6. Verify metrics are flowing
curl -s localhost:9100/metrics | head -20
curl -s localhost:9090/api/v1/targets
```

---

## System Monitoring Tools

![system_monitoring_tools](svg/courses/operating_systems/linux-system-administration/07_monitoring_maintenance/system_monitoring_tools.svg)

---

## Log Management

![log_management](svg/courses/operating_systems/linux-system-administration/07_monitoring_maintenance/log_management.svg)

---

## Backup Strategies

![backup_strategies](svg/courses/operating_systems/linux-system-administration/07_monitoring_maintenance/backup_strategies.svg)
