# Web Scraping: Extracting Data from the Web

---
## What is Web Scraping

- Web scraping is the process of extracting data from websites, typically by parsing the HTML content and extracting specific data points
- Automated by using scripts or programs to crawl and fetch data at scale
- Common uses include:
    - Price monitoring and comparison
    - Market research and competitive intelligence
    - Content aggregation and data journalism
    - Lead generation and contact harvesting
    - Academic research and data analysis
    - Search engine indexing (legitimate scraping)

---
## How Web Scraping Works

```python
┌──────────────────────────────────────────────────────────┐
│          Web Scraping Pipeline                            │
│                                                          │
│  ┌──────────┐    HTTP     ┌───────────┐                  │
│  │  Scraper  │───────────>│  Website  │                  │
│  │  Script   │  Request   │  Server   │                  │
│  │           │<───────────│           │                  │
│  └────┬──────┘  HTML/JSON └───────────┘                  │
│       │                                                  │
│       v                                                  │
│  ┌──────────┐                                            │
│  │  Parser   │  Extract data from HTML/JSON              │
│  │  (BS4,    │  using CSS selectors, XPath,              │
│  │  lxml)    │  or regex patterns                        │
│  └────┬──────┘                                           │
│       │                                                  │
│       v                                                  │
│  ┌──────────┐                                            │
│  │  Storage  │  CSV, JSON, database, API                 │
│  └──────────┘                                            │
└──────────────────────────────────────────────────────────┘
```

---
## Scraping Tools Overview

| Tool/Library    | Language   | Type              | Best For                        |
|-----------------|------------|-------------------|---------------------------------|
| BeautifulSoup   | Python     | HTML parser       | Simple static page scraping     |
| Scrapy          | Python     | Full framework    | Large-scale crawling projects   |
| Selenium        | Multi      | Browser automation| JavaScript-heavy sites          |
| Puppeteer       | Node.js    | Browser automation| Headless Chrome automation      |
| Playwright      | Multi      | Browser automation| Cross-browser testing/scraping  |
| requests-html   | Python     | HTTP + render     | Simple JS rendering needs       |
| curl / wget     | CLI        | HTTP client       | Simple page downloads           |
| Cheerio         | Node.js    | HTML parser       | Server-side jQuery-like parsing |

---
## Scraping with Python: requests + BeautifulSoup

```python
import requests
from bs4 import BeautifulSoup

# Basic scraping example
url = "https://example.com/products"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 Chrome/120.0.0.0"
}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

# Extract product data
products = []
for item in soup.select('.product-card'):
    product = {
        'name': item.select_one('.product-name').text.strip(),
        'price': item.select_one('.price').text.strip(),
        'url': item.select_one('a')['href'],
    }
    products.append(product)

print(f"Found {len(products)} products")
```

---
## Scraping with Scrapy

```python
# Scrapy: Full-featured scraping framework
# Install: pip install scrapy

import scrapy

class ProductSpider(scrapy.Spider):
    name = 'products'
    start_urls = ['https://example.com/products']

    # Configure politeness settings
    custom_settings = {
        'DOWNLOAD_DELAY': 2,         # 2 seconds between requests
        'CONCURRENT_REQUESTS': 1,     # One request at a time
        'ROBOTSTXT_OBEY': True,       # Respect robots.txt
        'USER_AGENT': 'MyBot/1.0 (research@example.com)',
    }

    def parse(self, response):
        # Extract items from current page
        for product in response.css('.product-card'):
            yield {
                'name': product.css('.product-name::text').get(),
                'price': product.css('.price::text').get(),
                'url': response.urljoin(
                    product.css('a::attr(href)').get()
                ),
            }

        # Follow pagination
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

```bash
# Run the spider
scrapy crawl products -o products.json
scrapy crawl products -o products.csv
```

---
## Scraping JavaScript-Heavy Sites

```python
# Selenium: Automates real browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('--headless')           # No visible browser
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

try:
    driver.get('https://example.com/spa-page')

    # Wait for dynamic content to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.data-loaded'))
    )

    # Now extract from the rendered DOM
    items = driver.find_elements(By.CSS_SELECTOR, '.product-card')
    for item in items:
        name = item.find_element(By.CSS_SELECTOR, '.name').text
        price = item.find_element(By.CSS_SELECTOR, '.price').text
        print(f"{name}: {price}")
finally:
    driver.quit()
```

```javascript
// Puppeteer (Node.js): Headless Chrome
const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto('https://example.com/products');
    await page.waitForSelector('.product-card');

    const products = await page.evaluate(() => {
        return [...document.querySelectorAll('.product-card')].map(el => ({
            name: el.querySelector('.name').textContent,
            price: el.querySelector('.price').textContent,
        }));
    });

    console.log(products);
    await browser.close();
})();
```

---
## Anti-Scraping Techniques

```python
┌──────────────────────────────────────────────────────────┐
│  Anti-Scraping Defense Layers                            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Layer 1: Access Control                                 │
│  ├── robots.txt directives                               │
│  ├── Rate limiting (per IP, per session)                 │
│  ├── IP blocking and reputation lists                    │
│  └── Geo-blocking suspicious regions                     │
│                                                          │
│  Layer 2: Detection                                      │
│  ├── User-Agent analysis                                 │
│  ├── Browser fingerprinting (TLS, JS, Canvas)            │
│  ├── Behavioral analysis (mouse, scroll, timing)         │
│  └── Honeypot traps (hidden links/fields)                │
│                                                          │
│  Layer 3: Challenge                                      │
│  ├── CAPTCHAs (reCAPTCHA, hCaptcha, Turnstile)         │
│  ├── JavaScript challenges                               │
│  ├── Cookie-based verification                           │
│  └── Proof-of-work challenges                            │
│                                                          │
│  Layer 4: Obfuscation                                    │
│  ├── Dynamic CSS class names                             │
│  ├── Shadow DOM                                          │
│  ├── Image-based rendering of text                       │
│  └── Data delivered via encrypted API calls              │
└──────────────────────────────────────────────────────────┘
```

---
## robots.txt

```python
# Example robots.txt
# https://example.com/robots.txt

# Block all bots from admin areas
User-agent: *
Disallow: /admin/
Disallow: /api/internal/
Disallow: /search?*

# Allow Google to index everything
User-agent: Googlebot
Allow: /

# Block specific scraper bots
User-agent: Scrapy
Disallow: /

# Specify sitemap location
Sitemap: https://example.com/sitemap.xml

# Crawl delay (non-standard but widely respected)
User-agent: *
Crawl-delay: 10
```

- robots.txt is a voluntary standard -- scrapers can ignore it
- Legal consideration: ignoring robots.txt may weaken legal defenses
- Does not prevent access -- it is an advisory, not a technical control
- Should be combined with actual rate limiting and access controls

---
## CAPTCHA Systems

| CAPTCHA Type    | Mechanism                              | Bypass Difficulty |
|-----------------|----------------------------------------|-------------------|
| Text CAPTCHA    | Distorted text recognition             | Easy (OCR)        |
| Image CAPTCHA   | Select images with specific objects    | Medium            |
| reCAPTCHA v2    | "I'm not a robot" checkbox + risk      | Medium            |
| reCAPTCHA v3    | Invisible, risk scoring (0.0 - 1.0)   | Hard              |
| hCaptcha        | Image labeling tasks                   | Medium            |
| Cloudflare Turnstile | Invisible challenge               | Hard              |

```bash
┌──────────────────────────────────────────────────────────┐
│  CAPTCHA Bypass Methods (for awareness)                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  1. CAPTCHA solving services ($1-3 per 1000 solves)      │
│     - 2Captcha, Anti-Captcha, DeathByCaptcha             │
│     - Human workers solve CAPTCHAs in real time          │
│                                                          │
│  2. Machine learning / OCR                               │
│     - Trained models for specific CAPTCHA types           │
│     - Tesseract OCR for simple text CAPTCHAs             │
│                                                          │
│  3. Browser automation with stealth                      │
│     - undetected-chromedriver                             │
│     - puppeteer-extra-plugin-stealth                     │
│     - Real browser fingerprints                          │
│                                                          │
│  4. Token harvesting                                     │
│     - Solve CAPTCHA once, reuse token for multiple reqs  │
└──────────────────────────────────────────────────────────┘
```

---
## Rate Limiting Implementation

```python
# Server-side rate limiting (Flask example)
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour", "10 per minute"],
    storage_uri="redis://localhost:6379",
)

@app.route('/api/products')
@limiter.limit("30 per minute")
def get_products():
    return jsonify(products)

@app.route('/api/search')
@limiter.limit("10 per minute")
def search():
    return jsonify(results)
```

```nginx
# Nginx rate limiting configuration
http {
    # Define rate limit zones
    limit_req_zone $binary_remote_addr
        zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr
        zone=page_limit:10m rate=2r/s;

    server {
        # Apply to API endpoints
        location /api/ {
            limit_req zone=api_limit burst=20 nodelay;
            proxy_pass http://backend;
        }

        # Apply to scrape-sensitive pages
        location /products {
            limit_req zone=page_limit burst=5;
            proxy_pass http://backend;
        }
    }
}
```

---
## Browser Fingerprinting as Anti-Scraping

```javascript
// Server-side detection of headless browsers
// These checks distinguish real browsers from automated ones

function detectHeadless() {
    const checks = {
        // Chrome headless detection
        webdriver: navigator.webdriver,  // true in automated
        languages: navigator.languages,  // empty in headless
        plugins: navigator.plugins.length,  // 0 in headless
        chrome: window.chrome,          // undefined in headless

        // Canvas fingerprint (renders differently in headless)
        canvas: getCanvasFingerprint(),

        // WebGL renderer (reveals "SwiftShader" in headless)
        webgl: getWebGLRenderer(),

        // Permissions API (different in headless)
        permissions: await testPermissions(),
    };

    return checks;
}

// TLS fingerprinting (server-side)
// JA3 hash of TLS handshake identifies the client library
// Python requests, Go net/http, and browsers have different
// TLS fingerprints
```

---
## Scraping Defenses: Honeypot Traps

```html
<!-- Hidden link that only bots will follow -->
<a href="/trap" style="display:none; visibility:hidden;">
    More products
</a>

<!-- Hidden form field that only bots will fill -->
<form>
    <input type="text" name="name" placeholder="Your name">
    <!-- Honeypot: invisible to users, bots fill it in -->
    <input type="text" name="email_confirm"
           style="position:absolute; left:-9999px;"
           tabindex="-1" autocomplete="off">
    <button type="submit">Submit</button>
</form>
```

```python
# Server-side honeypot handler
@app.route('/trap')
def honeypot():
    # Any request to this endpoint is a bot
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    log_bot_activity(ip, user_agent)
    block_ip(ip, duration_hours=24)
    return "Page not found", 404
```

---
## Legal Considerations

```bash
┌──────────────────────────────────────────────────────────┐
│  Legal Landscape of Web Scraping                         │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  United States:                                          │
│  - CFAA (Computer Fraud and Abuse Act)                   │
│    hiQ v. LinkedIn (2022): Scraping PUBLIC data is       │
│    generally not a CFAA violation                        │
│  - Terms of Service violations (breach of contract)      │
│  - Copyright: scraping copyrighted content may violate   │
│                                                          │
│  European Union:                                         │
│  - GDPR: Scraping personal data requires legal basis     │
│  - Database Directive: Protects database contents        │
│  - Must comply with data subject rights                  │
│                                                          │
│  General Principles:                                     │
│  - Public data != free data                              │
│  - Respect robots.txt and ToS                            │
│  - Do not bypass technical protection measures           │
│  - Do not overload servers (DoS risk)                    │
│  - Be cautious with personal data                        │
│  - Consider whether an API is available instead          │
└──────────────────────────────────────────────────────────┘
```

---
## Ethical Scraping Guidelines

```python
# Ethical scraping implementation example

import requests
import time
import robotsparser

class EthicalScraper:
    def __init__(self, base_url, user_agent, contact_email):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': f'{user_agent} ({contact_email})',
        })
        self.delay = 2  # seconds between requests

        # Check robots.txt
        self.robots = robotsparser.RobotFileParser()
        self.robots.set_url(f'{base_url}/robots.txt')
        self.robots.read()

    def can_fetch(self, url):
        """Check if robots.txt allows scraping this URL."""
        return self.robots.can_fetch(
            self.session.headers['User-Agent'], url
        )

    def fetch(self, url):
        """Fetch a URL with politeness delays."""
        if not self.can_fetch(url):
            print(f"Blocked by robots.txt: {url}")
            return None

        time.sleep(self.delay)  # Be polite
        response = self.session.get(url, timeout=10)

        # Respect rate limit headers
        if response.status_code == 429:
            retry_after = int(
                response.headers.get('Retry-After', 60)
            )
            print(f"Rate limited. Waiting {retry_after}s")
            time.sleep(retry_after)
            return self.fetch(url)

        return response
```

---
## Scraping Detection and Monitoring

```bash
# Server-side monitoring for scraping activity

# Analyze access logs for scraping patterns
# High request rate from single IP
awk '{print $1}' /var/log/nginx/access.log | \
    sort | uniq -c | sort -rn | head -20

# Requests without common browser headers
grep -v "Mozilla\|Chrome\|Safari" \
    /var/log/nginx/access.log | head -20

# Sequential page access patterns
awk '{print $1, $7}' /var/log/nginx/access.log | \
    sort | head -50

# Monitor for scraping tools in User-Agent
grep -Ei "scrapy|python-requests|wget|curl|bot|spider" \
    /var/log/nginx/access.log | \
    awk '{print $1}' | sort | uniq -c | sort -rn
```

---
## Defense Strategy for Website Owners

```bash
┌──────────────────────────────────────────────────────────┐
│  Anti-Scraping Defense Strategy                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  1. Define what you want to protect                      │
│     - Pricing data? User content? Search results?        │
│     - Not all scraping needs to be blocked               │
│                                                          │
│  2. Implement proportional defenses                      │
│     - robots.txt for well-behaved bots                   │
│     - Rate limiting for volume control                   │
│     - CAPTCHAs for sensitive pages                       │
│     - Authentication for premium data                    │
│                                                          │
│  3. Offer alternatives                                   │
│     - Public API with rate limits and API keys           │
│     - Data feeds or partnerships                         │
│     - Terms of Service with clear data use policies      │
│                                                          │
│  4. Monitor and respond                                  │
│     - Log analysis for scraping patterns                 │
│     - Automated blocking of abusive IPs                  │
│     - Regular review of anti-bot effectiveness           │
│                                                          │
│  5. Legal backup                                         │
│     - Clear Terms of Service                             │
│     - DMCA notices for copyrighted content               │
│     - Cease and desist for repeat offenders              │
└──────────────────────────────────────────────────────────┘
```

---
## Key Takeaways

- Web scraping is a powerful technique with both legitimate and malicious uses
- Tools range from simple (requests + BeautifulSoup) to full frameworks (Scrapy) to browser automation (Selenium, Puppeteer)
- Anti-scraping defenses operate in layers: access control, detection, challenges, and obfuscation
- CAPTCHAs raise the cost of scraping but can be bypassed with solving services
- Rate limiting is essential to prevent scraping from becoming a denial of service
- Legal landscape varies by jurisdiction -- public data does not mean free data
- Ethical scraping means respecting robots.txt, rate limits, and terms of service
- Website owners should offer APIs as an alternative to scraping when feasible
