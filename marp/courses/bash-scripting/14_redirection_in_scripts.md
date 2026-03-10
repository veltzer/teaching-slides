# Redirection in Scripts
---
## Redirecting Entire Scripts
```bash
#!/bin/bash

# Redirect all output of the entire script
exec > /var/log/myscript.log 2>&1

echo "This goes to the log file"
echo "So does this"
date
ls -la
# Everything goes to the log file
# Nothing appears on the terminal
```
---
## Redirecting to Both Log and Terminal
```bash
#!/bin/bash

# Send all output to both log file and terminal
exec > >(tee /var/log/myscript.log) 2>&1

echo "This appears on terminal AND in the log"
echo "Errors too" >&2
```
---
## Saving and Restoring File Descriptors
```bash
#!/bin/bash

# Save stdout (fd 1) as fd 3
exec 3>&1

# Redirect stdout to a file
exec > output.txt

echo "This goes to the file"

# Restore stdout from fd 3
exec 1>&3

# Close fd 3 (no longer needed)
exec 3>&-

echo "This goes to the terminal again"
```
---
## Saving and Restoring: Full Pattern
```bash
#!/bin/bash

# Save both stdout and stderr
exec 3>&1 4>&2

# Redirect both to log
exec > /tmp/script.log 2>&1

echo "logged output"
ls /nonexistent   # logged error

# Restore both
exec 1>&3 2>&4
exec 3>&- 4>&-

echo "back to terminal"
```
---
## Redirect a Block of Commands
```bash
#!/bin/bash

# Redirect just a section
{
    echo "=== System Report ==="
    date
    uname -a
    df -h
    free -m
} > /tmp/report.txt

echo "Report saved (this prints to terminal)"

# Redirect with error handling
{
    echo "Starting backup..."
    tar czf /tmp/backup.tar.gz /home/user/data
    echo "Backup complete"
} > /tmp/backup.log 2>&1
```
---
## Logging Functions
```bash
#!/bin/bash

# Create a proper logging system
readonly LOG_FILE="/tmp/app.log"

exec 3>> "$LOG_FILE"    # open log file on fd 3

log_info()  { echo "[INFO]  $(date '+%H:%M:%S') $*" >&3; }
log_warn()  { echo "[WARN]  $(date '+%H:%M:%S') $*" >&3; }
log_error() { echo "[ERROR] $(date '+%H:%M:%S') $*" | tee /dev/fd/2 >&3; }

log_info "Script started"
log_info "Processing data"
log_warn "Disk space is low"
log_error "Cannot connect to database"

exec 3>&-    # close log file
```
---
## Input Redirection in Scripts
```bash
#!/bin/bash

# Read configuration from a file
exec 3< /etc/myapp.conf

while IFS='=' read -r key value <&3; do
    case "$key" in
        host)   HOST="$value" ;;
        port)   PORT="$value" ;;
        debug)  DEBUG="$value" ;;
    esac
done

exec 3<&-    # close input fd

echo "Config: $HOST:$PORT (debug=$DEBUG)"
```
---
## Here Document Tricks
```bash
#!/bin/bash

# Generate a config file
cat > /tmp/nginx.conf << EOF
server {
    listen ${PORT:-80};
    server_name ${HOSTNAME};
    root ${WEBROOT:-/var/www/html};
}
EOF

# SSH with multiple commands
ssh user@server << 'REMOTE'
    cd /var/log
    grep "error" syslog | tail -20
    df -h
REMOTE
# Note: 'REMOTE' (quoted) prevents local expansion
```
---
## Practical: Script that Logs Everything
```bash
#!/bin/bash
set -euo pipefail

# Log everything: stdout, stderr, and a copy to terminal
LOG="/var/log/deploy-$(date +%Y%m%d-%H%M%S).log"

# Duplicate all output
exec &> >(tee "$LOG")

echo "=== Deployment started at $(date) ==="
echo "Log file: $LOG"

echo "Step 1: Pulling latest code..."
git pull origin main

echo "Step 2: Building..."
make clean && make

echo "Step 3: Running tests..."
make test

echo "=== Deployment completed at $(date) ==="
```
