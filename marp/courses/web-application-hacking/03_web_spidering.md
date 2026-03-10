---
marp: true
theme: default
paginate: true
---

# Web Spidering & Content Discovery

## Finding What They Don't Want You to Find

---

## What is Web Spidering?

- Automated crawling of web applications
- Follows links to discover pages and resources
- Maps the application structure
- Identifies entry points for testing
- Also called **web crawling** or **web scraping**

```
          Start URL
              |
     +--------+--------+
     |        |        |
   /page1   /page2   /page3
     |        |
  /page1/a  /page2/b
```

---

## Spidering vs Content Discovery

| Spidering | Content Discovery |
|-----------|-------------------|
| Follows existing links | Brute-forces paths |
| Discovers linked content | Finds unlinked content |
| Respects `robots.txt` | Ignores `robots.txt` |
| Fast, less thorough | Slow, more thorough |
| May miss hidden pages | Finds backup files, admin panels |

**Best approach**: Use both techniques together

---

## robots.txt - A Treasure Map

```
# robots.txt - tells search engines what NOT to index
# For pentesters, it tells you what to look AT

User-agent: *
Disallow: /admin/
Disallow: /backup/
Disallow: /api/internal/
Disallow: /config/
Disallow: /tmp/uploads/
Disallow: /.git/
Sitemap: https://target.com/sitemap.xml

# These "disallowed" paths are often the most interesting!
```

---

## sitemap.xml - Application Blueprint

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://target.com/products</loc>
    <lastmod>2024-01-15</lastmod>
  </url>
  <url>
    <loc>https://target.com/api/v2/products</loc>
    <lastmod>2024-01-10</lastmod>
  </url>
  <url>
    <loc>https://target.com/admin/dashboard</loc>
    <lastmod>2024-01-12</lastmod>
  </url>
</urlset>
```

- Reveals URL structure and API endpoints
- Shows last modification dates
- May expose internal/admin paths

---

## Burp Suite Spider

```
Steps to spider with Burp:
1. Set target scope: Target -> Scope -> Add
2. Browse the application manually first
3. Right-click target in Site Map -> "Scan" or "Spider"
4. Review discovered content in Site Map

Key settings:
- Maximum link depth: 5-10
- Form submission: Enable with test values
- Scope: Limit to target domain
- Robots.txt: Check but don't obey
```

---

## Burp Site Map Analysis

```
Target Site Map Tree:
target.com
├── /                     (200)
├── /login                (200)
├── /register             (200)
├── /dashboard            (302 -> /login)
├── /api/
│   ├── /v1/
│   │   ├── /users        (401)
│   │   ├── /products     (200)
│   │   └── /orders       (401)
│   └── /v2/
│       ├── /users        (401)
│       └── /products     (200)
├── /admin/               (403)
└── /static/
    ├── /js/
    └── /css/
```

---

## ZAP Spider

```bash
# ZAP traditional spider
zap-cli spider http://target.com

# ZAP AJAX spider (for JavaScript-heavy apps)
zap-cli ajax-spider http://target.com

# ZAP API usage
# Start spider
curl "http://localhost:8080/JSON/spider/action/scan/\
?url=http://target.com"

# Check spider status
curl "http://localhost:8080/JSON/spider/view/status/"

# Get results
curl "http://localhost:8080/JSON/spider/view/results/"
```

---

## Content Discovery - gobuster

```bash
# Directory discovery
gobuster dir -u http://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -t 50 -o gobuster-results.txt

# With file extensions
gobuster dir -u http://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -x php,asp,aspx,jsp,html,js,txt,bak,old,zip \
  -t 50

# Recursive discovery
gobuster dir -u http://target.com \
  -w common.txt --no-error \
  -t 50 -r  # Follow redirects

# DNS subdomain brute-force
gobuster dns -d target.com \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

---

## Content Discovery - ffuf

```bash
# Basic directory fuzzing
ffuf -u http://target.com/FUZZ \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt

# Filter by status code
ffuf -u http://target.com/FUZZ \
  -w common.txt -mc 200,301,302

# Filter by response size (remove false positives)
ffuf -u http://target.com/FUZZ \
  -w common.txt -fs 4242

# Recursive fuzzing
ffuf -u http://target.com/FUZZ \
  -w common.txt -recursion -recursion-depth 3

# Multiple wordlists
ffuf -u http://target.com/FUZZ1/FUZZ2 \
  -w dirs.txt:FUZZ1 -w files.txt:FUZZ2
```

---

## Finding Backup Files

```bash
# Common backup file patterns
/index.php.bak
/index.php~
/index.php.old
/index.php.swp      # Vim swap file
/.index.php.swp     # Hidden Vim swap
/index.php.save
/config.php.bak
/web.config.bak
/application.yml.bak
/database.sql
/backup.zip
/backup.tar.gz
/www.zip
/site.tar.gz
/.env               # Environment variables
/.env.bak
```

```bash
# Scan for backup files
ffuf -u http://target.com/FUZZ \
  -w /usr/share/seclists/Discovery/Web-Content/raft-large-files.txt
```

---

## Version Control Exposure

```bash
# Git repository exposure
curl -s http://target.com/.git/HEAD
# Returns: ref: refs/heads/master

# If accessible, dump the entire repo:
git-dumper http://target.com/.git/ ./dumped-repo

# SVN exposure
curl -s http://target.com/.svn/entries

# Other version control
curl -s http://target.com/.hg/store/00manifest.i  # Mercurial
curl -s http://target.com/.bzr/README              # Bazaar
curl -s http://target.com/CVS/Root                 # CVS
```

---

## Finding Hidden API Endpoints

```bash
# Check common API paths
/api/
/api/v1/
/api/v2/
/api/swagger.json
/api/swagger-ui/
/api/docs
/api/openapi.json
/graphql
/graphiql
/api-docs
/_api/
/rest/
/services/

# GraphQL introspection
curl -X POST http://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{__schema{types{name,fields{name}}}}"}'
```

---

## JavaScript File Analysis

```bash
# Extract URLs from JavaScript files
# Step 1: Find JS files in Burp/ZAP site map
# Step 2: Download and analyze

# Using grep to find endpoints
curl -s http://target.com/static/js/app.js | \
  grep -oP '["'"'"']/[a-zA-Z0-9_/.-]+' | sort -u

# Using LinkFinder (specialized tool)
python3 linkfinder.py -i http://target.com/static/js/app.js -o cli

# Find API keys and secrets in JS
curl -s http://target.com/static/js/app.js | \
  grep -iE "(api[_-]?key|secret|token|password|auth)" 

# Check for source maps
curl -s http://target.com/static/js/app.js.map
```

---

## Subdomain Enumeration

```bash
# DNS brute-force
gobuster dns -d target.com -w subdomains-top1million.txt

# Certificate transparency logs
curl -s "https://crt.sh/?q=%.target.com&output=json" | \
  jq -r '.[].name_value' | sort -u

# Online services
# - Shodan
# - Censys
# - SecurityTrails
# - VirusTotal

# Subdomain takeover check
subjack -w subdomains.txt -t 50 -ssl -v
```

---

## Virtual Host Discovery

```bash
# Many web servers host multiple sites on one IP
# Different Host headers return different content

ffuf -u http://TARGET_IP \
  -H "Host: FUZZ.target.com" \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
  -fs 4242  # Filter default page size

# Manual test
curl -H "Host: admin.target.com" http://TARGET_IP
curl -H "Host: dev.target.com" http://TARGET_IP
curl -H "Host: staging.target.com" http://TARGET_IP
curl -H "Host: internal.target.com" http://TARGET_IP
```

---

## Discovering Hidden Parameters

```bash
# Burp Extension: Param Miner
# Automatically discovers hidden parameters

# Manual parameter discovery
ffuf -u "http://target.com/page?FUZZ=test" \
  -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -fs 4242

# Common hidden parameters
?debug=true
?test=1
?admin=1
?source=1
?_debug=1
?verbose=1
?format=json
?callback=test
?redirect=http://evil.com
```

---

## Google Dorking for Recon

```
# Find login pages
site:target.com inurl:login OR inurl:signin

# Find exposed files
site:target.com filetype:pdf OR filetype:doc OR filetype:xls

# Find configuration files
site:target.com filetype:xml OR filetype:conf OR filetype:env

# Find error messages
site:target.com "Warning:" OR "Error:" OR "Fatal:"

# Find admin panels
site:target.com inurl:admin OR inurl:dashboard

# Find exposed directories
site:target.com intitle:"Index of"

# Find backup files
site:target.com filetype:bak OR filetype:sql OR filetype:old
```

---

## Wayback Machine Recon

```bash
# The Wayback Machine archives old versions of websites
# Old pages may contain removed but still functional endpoints

# Using waybackurls tool
echo target.com | waybackurls > wayback_urls.txt

# Filter for interesting paths
cat wayback_urls.txt | grep -iE "\.(php|asp|aspx|jsp|do|action)"
cat wayback_urls.txt | grep -iE "(admin|config|backup|test|api)"
cat wayback_urls.txt | grep -iE "(\.zip|\.tar|\.gz|\.bak|\.sql)"

# Check if old endpoints still exist
while read url; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  echo "$code $url"
done < wayback_urls.txt
```

---

## GitHub and Cloud Storage Recon

```bash
# Search GitHub for leaked credentials
# (Use GitHub's search or specialized tools)

# Trufflehog - Find secrets in Git repos
trufflehog git https://github.com/target-org/repo

# GitLeaks - Audit Git repos for secrets
gitleaks detect --source=/path/to/repo

# Common GitHub searches:
# org:targetcompany password
# org:targetcompany aws_access_key
# org:targetcompany api_key
# org:targetcompany jdbc:mysql://
# org:targetcompany BEGIN RSA PRIVATE KEY

# Cloud storage enumeration
# AWS S3
aws s3 ls s3://target-bucket --no-sign-request

# GrayhatWarfare - Search open S3 buckets
# https://grayhatwarfare.com

# Azure blob storage
curl https://targetaccount.blob.core.windows.net/container?restype=container&comp=list

# GCP Storage
curl https://storage.googleapis.com/target-bucket
```

---

## AJAX Spider for Modern Web Apps

```bash
# Traditional spiders miss JavaScript-rendered content
# Use AJAX spiders for Single Page Applications (SPAs)

# ZAP AJAX Spider
zap-cli ajax-spider http://target.com
# Uses a real browser engine to render JavaScript
# Discovers dynamically generated content

# Burp Suite Crawler (Pro)
# Embedded browser navigates the application
# Handles JavaScript frameworks (React, Angular, Vue)
# Submits forms with test values

# Headless browser scripting
# Playwright/Puppeteer for custom crawling
const { chromium } = require('playwright');
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('http://target.com');
// Click buttons, fill forms, navigate
const links = await page.$$eval('a', as => as.map(a => a.href));

# Katana - Fast web crawler with headless support
katana -u https://target.com -headless -d 5 -o results.txt
```

---

## Putting It All Together

```
Comprehensive Discovery Workflow:
================================

1. robots.txt & sitemap.xml          (manual)
2. Burp Suite passive spidering      (browse app)
3. Burp Suite active spidering       (automated)
4. Directory brute-force (gobuster)  (common.txt)
5. File extension fuzzing (ffuf)     (.bak,.old,.zip)
6. Version control checks            (.git,.svn)
7. JavaScript analysis               (linkfinder)
8. Subdomain enumeration             (DNS + CT)
9. Virtual host discovery            (ffuf)
10. Parameter discovery              (Param Miner)
11. Google dorking                   (site: queries)
12. Wayback Machine                  (waybackurls)
```

---

## Lab Exercise: Content Discovery

**Target**: DVWA at `http://localhost:8080`

1. Check `robots.txt` and `sitemap.xml`
2. Spider with Burp Suite
3. Run `gobuster` with `common.txt`
4. Fuzz for backup files with `ffuf`
5. Check for `.git` exposure
6. Analyze any JavaScript files
7. Document all discovered paths

```bash
gobuster dir -u http://localhost:8080 \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -x php,txt,bak -t 20
```

---

## Summary

- Spidering and content discovery are complementary
- `robots.txt` and `sitemap.xml` are recon goldmines
- Backup files and version control exposure are critical findings
- JavaScript files contain hidden API endpoints and secrets
- Subdomain and virtual host discovery expand the attack surface
- Always use multiple discovery techniques
- Document everything you find

> Next: Identifying Entry Points
