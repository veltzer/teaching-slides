# SQL Injection
---
## What is SQL Injection?
- A technique to exploit web applications by injecting malicious SQL statements
- Attacker can gain unauthorized access to databases
- Can lead to data theft, data manipulation, or even server takeover
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
