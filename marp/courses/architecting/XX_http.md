---
marp: true
theme: default
paginate: true
---

# HTTP Protocol: Evolution and Versions
## From 1.0 to 3.0

---

# What is HTTP?

- HTTP: Hypertext Transfer Protocol
- Foundation of data exchange on the Web
- Client-server protocol
- Stateless, but not sessionless

```mermaid
graph LR
    A[Client] -->|Request| B[Server]
    B -->|Response| A
```

---

# HTTP/1.0 (1996)

- First standardized version
- One request-response pair per TCP connection
- Headers introduced
- Methods: GET, HEAD, POST

```mermaid
sequenceDiagram
    participant Client
    participant Server
    Client->>Server: TCP Connection
    Client->>Server: HTTP Request
    Server->>Client: HTTP Response
    Client->>Server: TCP Close
```

---

# HTTP/1.1 (1997)

- Persistent connections
- Pipelining (multiple requests before responses)
- Host header (virtual hosting)
- New methods: PUT, DELETE, TRACE, OPTIONS
- Chunked transfer encoding

```mermaid
sequenceDiagram
    participant Client
    participant Server
    Client->>Server: TCP Connection
    Client->>Server: Request 1
    Client->>Server: Request 2
    Server->>Client: Response 1
    Server->>Client: Response 2
    Note over Client,Server: Connection remains open
```

---

# HTTP/1.1 Improvements

- Reduced latency for multiple requests
- Better bandwidth utilization
- Introduced caching mechanisms
- Added compression (Content-Encoding)

---

# HTTP/2 (2015)

- Binary protocol (not text-based)
- Multiplexing (multiple requests/responses over single connection)
- Header compression (HPACK)
- Server push
- Stream prioritization

```mermaid
graph TD
    A[Single TCP Connection] --> B[Stream 1]
    A --> C[Stream 2]
    A --> D[Stream 3]
    B --> E[Request/Response 1]
    C --> F[Request/Response 2]
    D --> G[Request/Response 3]
```

---

# HTTP/2 Server Push

```mermaid
sequenceDiagram
    participant Client
    participant Server
    Client->>Server: Request HTML
    Server->>Client: HTML
    Server->>Client: CSS (pushed)
    Server->>Client: JavaScript (pushed)
    Note over Client,Server: Server anticipates client needs
```

---

# HTTP/3 (2022)

- Based on QUIC protocol (Quick UDP Internet Connections)
- Replaces TCP with UDP
- Improved performance on poor networks
- Reduced connection establishment time
- Better multiplexing without head-of-line blocking

```mermaid
graph LR
    A[HTTP/3] --> B[QUIC]
    B --> C[UDP]
    C --> D[IP]
```

---

# HTTP/3 Connection Establishment

```mermaid
sequenceDiagram
    participant Client
    participant Server
    Client->>Server: QUIC Handshake (includes TLS)
    Note over Client,Server: 0-RTT if resuming
    Client->>Server: HTTP Request
    Server->>Client: HTTP Response
```

---

# Version Comparison

| Feature           | HTTP/1.0 | HTTP/1.1 | HTTP/2   | HTTP/3   |
|-------------------|----------|----------|----------|----------|
| Connections       | One-off  | Persistent | Multiplexed | Multiplexed |
| Compression       | No       | Yes      | HPACK    | QPACK    |
| Multiplexing      | No       | Limited  | Yes      | Yes      |
| Server Push       | No       | No       | Yes      | Yes      |
| HOL Blocking      | Yes      | Yes      | Reduced  | Eliminated |
| Transport Protocol| TCP      | TCP      | TCP      | UDP (QUIC) |

---

# Key Takeaways

1. HTTP has evolved to meet increasing web demands
2. Each version improved performance and capabilities
3. HTTP/2 and HTTP/3 focus on multiplexing and reducing latency
4. Modern websites benefit from using the latest HTTP version
5. Understanding HTTP versions helps in web optimization

---

# Questions?

Thank you for your attention!

Feel free to ask any questions about HTTP and its evolution.

