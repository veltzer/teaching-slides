# SQL Injection
---
## What is SQL Injection?
- A technique to exploit web applications by injecting malicious SQL statements
- Attacker can gain unauthorized access to databases
- Can lead to data theft, data manipulation, or even server takeover
---
## How Does SQL Injection Work?

![0](../../../out/mermaid/marp/courses/cyber-attacks-and-vectors/05_sql_injection.md/0.png)

---
## How Does SQL Injection Work?
1. User input is not properly sanitized
1. Malicious SQL code is injected into application queries
1. Injected code is executed by the database
1. Attacker can retrieve, modify, or delete data
---
## Examples of SQL Injection
- Login bypass: `' OR '1'='1`
- Retrieving data: `UNION SELECT password FROM users`
- Adding data: `'; INSERT INTO users VALUES ('admin', 'password')`
- Deleting data: `'; DROP TABLE users; --`
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
## Sanitizing User Input
- Remove or escape special characters (', ", `, etc.)
- Use allowlists (whitelisting) instead of denylists (blacklisting)
- Apply strong input validation rules
- Avoid interpreting input as executable code
---
## Best Practices
- Follow the principle of "least privilege" for database accounts
- Implement secure authentication and access control mechanisms
- Keep software up-to-date with security patches and updates
- Regularly audit and test your applications for SQL Injection vulnerabilities
- Educate developers on secure coding practices and SQL Injection prevention
