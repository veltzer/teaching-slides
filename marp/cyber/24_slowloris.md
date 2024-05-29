# Slowloris Attack and Mitigation

---

## What is Slowloris Attack?

- Slowloris is a type of Denial of Service (DoS) attack that targets web servers
- It works by opening multiple HTTP connections to the target server and keeping them open as long as possible
- This consumes all available connections/threads on the server, making it unable to serve legitimate requests

---

## How Does Slowloris Work?

- The attacker sends partial HTTP requests, sending just a few bytes at a time
- By doing this, the server keeps the connections open, waiting for the request to complete
- The attacker continues sending these partial requests to keep the connections alive
- This causes the server to exhaust its maximum concurrent connection pool

---

## Impact of Slowloris Attack

- Legitimate users are unable to access the web server or web application
- The server becomes unresponsive and may crash or need to be restarted
- Can lead to significant downtime and service disruption
- Can be used as a precursor to other attacks when the server is overwhelmed

---

## Mitigating Slowloris Attacks

- Limit the maximum number of connections per IP address
- Set a timeout for incomplete HTTP requests
- Use load balancing and distribute traffic across multiple servers
- Implement application-level filtering to detect and block malicious requests
- Use a Web Application Firewall (WAF) to monitor and protect against Slowloris attacks

---

## Additional Mitigation Strategies

- Increase the maximum number of concurrent connections the server can handle
- Implement rate-limiting to restrict the number of requests per client
- Monitor server logs for suspicious activity and patterns
- Keep software and systems up-to-date with the latest security patches
- Implement a robust incident response plan to quickly detect and mitigate attacks
