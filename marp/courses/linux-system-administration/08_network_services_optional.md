# Network Services (Optional)
## nginx, Apache, HAProxy, and Postfix

---
## Web Server: nginx

```bash
# Install
apt install nginx

# Main config
# /etc/nginx/nginx.conf
# Site configs: /etc/nginx/sites-available/
# Enabled sites: /etc/nginx/sites-enabled/
```

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;

    location / {
        try_files $uri $uri/ =404;
    }

    location /api {
        proxy_pass http://localhost:3000;
    }
}
```

---
## nginx Configuration Structure

```txt
/etc/nginx/
├── nginx.conf              # Main config
├── conf.d/                 # Additional configs
├── sites-available/        # Available virtual hosts
├── sites-enabled/          # Enabled virtual hosts (symlinks)
├── snippets/               # Reusable config snippets
└── modules-enabled/        # Loaded modules
```

```bash
# Enable/disable site
ln -s /etc/nginx/sites-available/mysite \
  /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/mysite

# Test and reload
nginx -t
systemctl reload nginx
```

---
## nginx: Reverse Proxy Configuration

```nginx
upstream backend {
    server 127.0.0.1:3000 weight=3;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002 backup;
    keepalive 32;
}

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

---
## nginx: SSL and Performance

```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/ssl/certs/server.crt;
    ssl_certificate_key /etc/ssl/private/server.key;
    ssl_protocols TLSv1.2 TLSv1.3;

    gzip on;
    gzip_types text/plain text/css application/json;

    location /static {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Test config and reload
nginx -t
systemctl reload nginx
```

---
## nginx: Security Headers and Rate Limiting

```nginx
server {
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security
      "max-age=31536000; includeSubDomains" always;

    # Rate limiting
    limit_req_zone $binary_remote_addr
      zone=api:10m rate=10r/s;

    location /api {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://backend;
    }

    # Block bad bots
    if ($http_user_agent ~* (bot|crawler|spider)) {
        return 403;
    }
}
```

---
## Web Server: Apache

```bash
# Install
apt install apache2

# Enable/disable modules
a2enmod rewrite ssl proxy
a2dismod autoindex

# Enable/disable sites
a2ensite mysite.conf
a2dissite 000-default.conf
```

```apache
# /etc/apache2/sites-available/mysite.conf
<VirtualHost *:80>
    ServerName example.com
    DocumentRoot /var/www/html
    <Directory /var/www/html>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

---
## Apache: SSL and Reverse Proxy

```apache
<VirtualHost *:443>
    ServerName example.com
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/server.crt
    SSLCertificateKeyFile /etc/ssl/private/server.key

    ProxyPreserveHost On
    ProxyPass / http://localhost:3000/
    ProxyPassReverse / http://localhost:3000/

    <Location />
        Require all granted
    </Location>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

```bash
a2enmod ssl proxy proxy_http
systemctl restart apache2
```

---
## Load Balancer: HAProxy

```bash
apt install haproxy
```

```txt
# /etc/haproxy/haproxy.cfg
frontend http_front
    bind *:80
    default_backend http_back

backend http_back
    balance roundrobin
    option httpchk GET /health
    server web1 192.168.1.10:80 check
    server web2 192.168.1.11:80 check
    server web3 192.168.1.12:80 check backup

listen stats
    bind *:8404
    stats enable
    stats uri /stats
```

```bash
haproxy -c -f /etc/haproxy/haproxy.cfg
systemctl restart haproxy
```

---
## HAProxy: SSL Termination and Algorithms

```txt
# /etc/haproxy/haproxy.cfg
frontend https_front
    bind *:443 ssl crt /etc/ssl/haproxy.pem
    http-request set-header X-Forwarded-Proto https
    default_backend http_back

backend http_back
    # Load balancing algorithms:
    # roundrobin - equal distribution
    # leastconn  - fewest connections
    # source     - sticky by client IP
    balance leastconn
    option httpchk GET /health
    http-check expect status 200
    server web1 192.168.1.10:80 check inter 5s fall 3
    server web2 192.168.1.11:80 check inter 5s fall 3
```

```bash
# Combine cert + key into single PEM
cat server.crt server.key > /etc/ssl/haproxy.pem
```

---
## Email Server: Postfix Basics

```bash
# Install
apt install postfix

# Main config: /etc/postfix/main.cf
```

```txt
# Key settings in /etc/postfix/main.cf
myhostname = mail.example.com
mydomain = example.com
myorigin = $mydomain
mydestination = $myhostname, localhost, $mydomain
inet_interfaces = all
relay_domains =
smtpd_tls_cert_file = /etc/ssl/certs/mail.crt
smtpd_tls_key_file = /etc/ssl/private/mail.key
```

```bash
# Test mail delivery
echo "Test" | mail -s "Test Subject" user@example.com

# Check mail queue
mailq
postqueue -f    # flush queue
```

---
## Postfix: Relay and Security

```txt
# /etc/postfix/main.cf

# Relay through external SMTP
relayhost = [smtp.example.com]:587
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options = noanonymous
smtp_tls_security_level = encrypt

# Restrict relay (prevent open relay)
smtpd_relay_restrictions =
    permit_mynetworks,
    permit_sasl_authenticated,
    reject_unauth_destination

# SPF/DKIM setup requires additional packages
# apt install opendkim opendkim-tools
```

```bash
# Create password file
echo "[smtp.example.com]:587 user:pass" > /etc/postfix/sasl_passwd
postmap /etc/postfix/sasl_passwd
chmod 600 /etc/postfix/sasl_passwd*
```

---
## nginx: Logging and Debugging

```nginx
# Custom log format
log_format detailed '$remote_addr - $remote_user '
  '[$time_local] "$request" $status '
  '$body_bytes_sent "$http_referer" '
  'rt=$request_time uct=$upstream_connect_time';

server {
    access_log /var/log/nginx/app.log detailed;
    error_log /var/log/nginx/app_error.log warn;

    # Per-location logging
    location /api {
        access_log /var/log/nginx/api.log detailed;
        proxy_pass http://backend;
    }
}
```

```bash
# Enable debug logging (recompile with --with-debug)
error_log /var/log/nginx/debug.log debug;

# Real-time log monitoring
tail -f /var/log/nginx/access.log | awk '{print $9}'
```

---
## Apache MPM Models

```bash
# Check active MPM
apachectl -V | grep MPM

# Switch MPM module
a2dismod mpm_prefork
a2enmod mpm_event
systemctl restart apache2
```

| MPM | Model | Best For |
|-----|-------|----------|
| `prefork` | Process per connection | Legacy `mod_php` |
| `worker` | Thread pool per process | General purpose |
| `event` | Async event-driven | High concurrency |

```apache
# /etc/apache2/mods-available/mpm_event.conf
<IfModule mpm_event_module>
    StartServers          2
    MinSpareThreads       25
    MaxSpareThreads       75
    ThreadLimit           64
    ThreadsPerChild       25
    MaxRequestWorkers     150
    MaxConnectionsPerChild 0
</IfModule>
```

---
## HAProxy: ACLs and Routing

```txt
# /etc/haproxy/haproxy.cfg
frontend http_front
    bind *:80

    # Define ACLs
    acl is_api path_beg /api
    acl is_static path_end .css .js .png .jpg
    acl is_admin hdr(host) -i admin.example.com
    acl is_blocked src 10.0.0.0/8

    # Route based on ACLs
    use_backend api_back if is_api
    use_backend static_back if is_static
    use_backend admin_back if is_admin
    http-request deny if is_blocked
    default_backend web_back
```

---
## HAProxy: Health Checks

```txt
backend api_back
    balance roundrobin
    option httpchk GET /health
    http-check expect status 200

    # Advanced health check settings
    server api1 10.0.1.1:3000 check inter 3s \
      fall 3 rise 2 weight 100
    server api2 10.0.1.2:3000 check inter 3s \
      fall 3 rise 2 weight 100

    # Slow start (ramp up traffic gradually)
    server api3 10.0.1.3:3000 check slowstart 30s

backend db_back
    option tcp-check
    tcp-check connect port 3306
    server db1 10.0.2.1:3306 check inter 5s
```

- `inter` - check interval
- `fall` - failures before marking down
- `rise` - successes before marking up

---
## Let's Encrypt with Web Servers

```bash
# Install certbot
apt install certbot

# For nginx
apt install python3-certbot-nginx
certbot --nginx -d example.com -d www.example.com

# For Apache
apt install python3-certbot-apache
certbot --apache -d example.com -d www.example.com

# Auto-renewal (installed by default)
systemctl status certbot.timer
certbot renew --dry-run
```

```bash
# Manual certificate for other services
certbot certonly --standalone -d example.com

# Certificates stored at:
# /etc/letsencrypt/live/example.com/fullchain.pem
# /etc/letsencrypt/live/example.com/privkey.pem
```

---
## nginx: Reverse Proxy for WebSocket

```nginx
# WebSocket requires HTTP/1.1 upgrade headers
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

upstream ws_backend {
    server 127.0.0.1:8080;
}

server {
    listen 80;
    server_name ws.example.com;

    location /ws {
        proxy_pass http://ws_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection
          $connection_upgrade;
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }
}
```

---
## Load Testing Web Services

```bash
# Apache Bench (simple)
apt install apache2-utils
ab -n 10000 -c 100 http://localhost/

# wrk (modern HTTP benchmarking)
wrk -t4 -c100 -d30s http://localhost/

# vegeta (constant rate testing)
echo "GET http://localhost/" | \
  vegeta attack -rate=100 -duration=30s | \
  vegeta report
```

Key metrics to watch:
- Requests per second (throughput)
- Latency percentiles (p50, p95, p99)
- Error rate under load
- Connection timeouts

```bash
# Monitor nginx during load test
watch -n 1 'curl -s localhost/nginx_status'
# Requires stub_status module enabled
```

---
## nginx: Worker Process Tuning

```nginx
# /etc/nginx/nginx.conf
# Set workers to number of CPU cores
worker_processes auto;

# Max open files per worker
worker_rlimit_nofile 65535;

events {
    # Connections per worker
    worker_connections 4096;
    # Accept multiple connections at once
    multi_accept on;
    # Use epoll on Linux
    use epoll;
}
```

```bash
# Check current worker count
ps aux | grep "nginx: worker"

# Determine optimal worker_connections
ulimit -n
# worker_connections should not exceed this value

# Monitor active connections
curl -s http://localhost/nginx_status
# Active connections: 291
# server accepts handled requests
```

---
## Apache: `.htaccess` Configuration

`.htaccess` provides per-directory configuration without restarting Apache:

```apache
# /var/www/html/.htaccess
# Requires AllowOverride All in VirtualHost

# Enable URL rewriting
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]

# Deny access to sensitive files
<FilesMatch "\.(env|git|htpasswd)$">
    Require all denied
</FilesMatch>

# Set security headers
Header set X-Content-Type-Options "nosniff"

# Password protect a directory
AuthType Basic
AuthName "Restricted"
AuthUserFile /etc/apache2/.htpasswd
Require valid-user
```

```bash
# Create password file
htpasswd -c /etc/apache2/.htpasswd admin
```

---
## HAProxy: Stick Tables

Stick tables track client state for rate limiting and session persistence:

```txt
# /etc/haproxy/haproxy.cfg
frontend http_front
    bind *:80

    # Define stick table: track request rates per IP
    stick-table type ip size 100k expire 30s \
      store http_req_rate(10s),conn_cur

    # Track client IP in the table
    http-request track-sc0 src

    # Deny if request rate > 100 per 10 seconds
    http-request deny deny_status 429 \
      if { sc_http_req_rate(0) gt 100 }

    # Deny if more than 20 concurrent connections
    http-request deny deny_status 429 \
      if { sc_conn_cur(0) gt 20 }

    default_backend web_back
```

```bash
# View stick table contents at runtime
echo "show table http_front" | \
  socat stdio /run/haproxy/admin.sock
```

---
## Postfix: Virtual Domains and Aliases

Serve multiple domains from a single `Postfix` instance:

```txt
# /etc/postfix/main.cf
virtual_mailbox_domains = domain1.com, domain2.com
virtual_mailbox_base = /var/mail/vhosts
virtual_mailbox_maps = hash:/etc/postfix/vmailbox
virtual_alias_maps = hash:/etc/postfix/virtual
virtual_minimum_uid = 1000
virtual_uid_maps = static:5000
virtual_gid_maps = static:5000
```

```txt
# /etc/postfix/vmailbox
user@domain1.com    domain1.com/user/
admin@domain2.com   domain2.com/admin/
```

```txt
# /etc/postfix/virtual
postmaster@domain1.com  admin@domain1.com
info@domain2.com        admin@domain2.com
```

```bash
postmap /etc/postfix/vmailbox
postmap /etc/postfix/virtual
systemctl reload postfix
```

---
## Exercise: Deploy a Reverse Proxy Stack

Build a load-balanced web setup with SSL termination:

1. Install `nginx` and configure two upstream `Python` HTTP servers:

```bash
# Start two simple backends
python3 -m http.server 8001 &
python3 -m http.server 8002 &
```

1. Create an `nginx` reverse proxy with:
    - `upstream` block balancing between ports `8001` and `8002`
    - Custom `log_format` including `upstream_response_time`
    - Rate limiting at 5 requests/second with burst of 10
    - Security headers (`X-Frame-Options`, `X-Content-Type-Options`)

1. Test with `ab` or `wrk`:

```bash
ab -n 1000 -c 50 http://localhost/
```

1. Verify rate limiting triggers `503` errors under load
1. Check the access log to confirm requests are distributed across backends
