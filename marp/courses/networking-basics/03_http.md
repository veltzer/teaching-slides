# HTTP Protocol: Evolution and Versions

## From 1.0 to 3.0

---

## What is HTTP

- HTTP: Hypertext Transfer Protocol
- Foundation of data exchange on the Web
- Client-server protocol
- Stateless, but not sessionless

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd0_02_http" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="30" width="140" height="130" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="8"/>
  <text x="90" y="55" text-anchor="middle" font-size="12" font-weight="bold">Client (Browser)</text>
  <text x="90" y="80" text-anchor="middle" font-size="10">GET /index.html</text>
  <text x="90" y="95" text-anchor="middle" font-size="10">Host: example.com</text>
  <text x="90" y="110" text-anchor="middle" font-size="10">Accept: text/html</text>
  <text x="90" y="130" text-anchor="middle" font-size="10" fill="#555">Port 80 / 443</text>
  <rect x="430" y="30" width="150" height="130" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="8"/>
  <text x="505" y="55" text-anchor="middle" font-size="12" font-weight="bold">Server</text>
  <text x="505" y="80" text-anchor="middle" font-size="10">HTTP/1.1 200 OK</text>
  <text x="505" y="95" text-anchor="middle" font-size="10">Content-Type: text/html</text>
  <text x="505" y="110" text-anchor="middle" font-size="10">Content-Length: 1234</text>
  <text x="505" y="130" text-anchor="middle" font-size="10" fill="#555">&lt;html&gt;...&lt;/html&gt;</text>
  <line x1="160" y1="70" x2="430" y2="70" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd0_02_http)"/>
  <text x="300" y="63" text-anchor="middle" font-size="11" fill="#1565c0" font-weight="bold">HTTP Request</text>
  <line x1="430" y1="120" x2="160" y2="120" stroke="#2e7d32" stroke-width="2" stroke-dasharray="5,3" marker-end="url(#arrowd0_02_http)"/>
  <text x="300" y="140" text-anchor="middle" font-size="11" fill="#2e7d32" font-weight="bold">HTTP Response</text>
  <text x="300" y="185" text-anchor="middle" font-size="10" fill="#555">Stateless request-response protocol over TCP</text>
</svg>

---

## HTTP/1.0 (1996)

- First standardized version
- One request-response pair per TCP connection
- Headers introduced
- Methods: GET, HEAD, POST

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd1_02_http" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="70" y="5" width="100" height="25" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="120" y="22" text-anchor="middle" font-size="11" font-weight="bold">Client</text>
  <rect x="420" y="5" width="100" height="25" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="470" y="22" text-anchor="middle" font-size="11" font-weight="bold">Server</text>
  <line x1="120" y1="35" x2="120" y2="190" stroke="#333" stroke-width="2"/>
  <line x1="470" y1="35" x2="470" y2="190" stroke="#333" stroke-width="2"/>
  <line x1="120" y1="50" x2="470" y2="60" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd1_02_http)"/>
  <text x="295" y="45" text-anchor="middle" font-size="10" fill="#1565c0">TCP Connect</text>
  <line x1="120" y1="75" x2="470" y2="85" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd1_02_http)"/>
  <text x="295" y="72" text-anchor="middle" font-size="10" fill="#1565c0">GET /page.html</text>
  <line x1="470" y1="95" x2="120" y2="105" stroke="#2e7d32" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd1_02_http)"/>
  <text x="295" y="98" text-anchor="middle" font-size="10" fill="#2e7d32">200 OK + HTML</text>
  <line x1="120" y1="115" x2="470" y2="115" stroke="#c62828" stroke-width="1" stroke-dasharray="2,2"/>
  <text x="295" y="128" text-anchor="middle" font-size="10" fill="#c62828">TCP Close</text>
  <line x1="120" y1="140" x2="470" y2="150" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd1_02_http)"/>
  <text x="295" y="140" text-anchor="middle" font-size="10" fill="#1565c0">New TCP + GET /style.css</text>
  <line x1="470" y1="160" x2="120" y2="170" stroke="#2e7d32" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd1_02_http)"/>
  <text x="295" y="165" text-anchor="middle" font-size="10" fill="#2e7d32">200 OK + CSS</text>
  <line x1="120" y1="180" x2="470" y2="180" stroke="#c62828" stroke-width="1" stroke-dasharray="2,2"/>
  <text x="295" y="195" text-anchor="middle" font-size="10" fill="#c62828">TCP Close (new conn per request)</text>
</svg>

---

## HTTP/1.1 (1997)

- Persistent connections
- Pipelining (multiple requests before responses)
- Host header (virtual hosting)
- New methods: PUT, DELETE, TRACE, OPTIONS
- Chunked transfer encoding

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd2_02_http" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="70" y="5" width="100" height="25" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="120" y="22" text-anchor="middle" font-size="11" font-weight="bold">Client</text>
  <rect x="420" y="5" width="100" height="25" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="470" y="22" text-anchor="middle" font-size="11" font-weight="bold">Server</text>
  <line x1="120" y1="35" x2="120" y2="195" stroke="#333" stroke-width="2"/>
  <line x1="470" y1="35" x2="470" y2="195" stroke="#333" stroke-width="2"/>
  <line x1="120" y1="48" x2="470" y2="55" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd2_02_http)"/>
  <text x="295" y="43" text-anchor="middle" font-size="10" fill="#1565c0">TCP Connect (persistent)</text>
  <line x1="120" y1="70" x2="470" y2="75" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd2_02_http)"/>
  <text x="295" y="67" text-anchor="middle" font-size="10" fill="#1565c0">GET /page.html</text>
  <line x1="470" y1="85" x2="120" y2="90" stroke="#2e7d32" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd2_02_http)"/>
  <text x="295" y="88" text-anchor="middle" font-size="10" fill="#2e7d32">200 OK + HTML</text>
  <line x1="120" y1="105" x2="470" y2="110" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd2_02_http)"/>
  <text x="295" y="103" text-anchor="middle" font-size="10" fill="#1565c0">GET /style.css (same conn)</text>
  <line x1="470" y1="120" x2="120" y2="125" stroke="#2e7d32" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd2_02_http)"/>
  <text x="295" y="122" text-anchor="middle" font-size="10" fill="#2e7d32">200 OK + CSS</text>
  <line x1="120" y1="140" x2="470" y2="145" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd2_02_http)"/>
  <text x="295" y="139" text-anchor="middle" font-size="10" fill="#1565c0">GET /app.js (same conn)</text>
  <line x1="470" y1="155" x2="120" y2="160" stroke="#2e7d32" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd2_02_http)"/>
  <text x="295" y="157" text-anchor="middle" font-size="10" fill="#2e7d32">200 OK + JS</text>
  <rect x="500" y="60" width="90" height="100" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5" opacity="0.7"/>
  <text x="545" y="80" text-anchor="middle" font-size="10" fill="#555">Keep-Alive</text>
  <text x="545" y="95" text-anchor="middle" font-size="10" fill="#555">Pipelining</text>
  <text x="545" y="110" text-anchor="middle" font-size="10" fill="#555">Chunked</text>
  <text x="545" y="125" text-anchor="middle" font-size="10" fill="#555">encoding</text>
  <text x="295" y="190" text-anchor="middle" font-size="10" fill="#555">Single TCP connection reused for multiple requests</text>
</svg>

---

## HTTP/1.1 Improvements

- Reduced latency for multiple requests
- Better bandwidth utilization
- Introduced caching mechanisms
- Added compression (Content-Encoding)

---

## HTTP/2 (2015)

- Binary protocol (not text-based)
- Multiplexing (multiple requests/responses over single connection)
- Header compression (HPACK)
- Server push
- Stream prioritization

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd3_02_http" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="20" width="110" height="160" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="8"/>
  <text x="75" y="42" text-anchor="middle" font-size="12" font-weight="bold">Client</text>
  <text x="75" y="60" text-anchor="middle" font-size="10">Single TCP</text>
  <text x="75" y="75" text-anchor="middle" font-size="10">Connection</text>
  <rect x="460" y="20" width="120" height="160" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="8"/>
  <text x="520" y="42" text-anchor="middle" font-size="12" font-weight="bold">Server</text>
  <rect x="180" y="30" width="230" height="25" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="220" y="47" text-anchor="middle" font-size="10" fill="#1565c0">Stream 1: GET /page</text>
  <line x1="320" y1="42" x2="410" y2="42" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd3_02_http)"/>
  <rect x="180" y="60" width="230" height="25" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="220" y="77" text-anchor="middle" font-size="10" fill="#7b1fa2">Stream 2: GET /style.css</text>
  <line x1="320" y1="72" x2="410" y2="72" stroke="#7b1fa2" stroke-width="2" marker-end="url(#arrowd3_02_http)"/>
  <rect x="180" y="90" width="230" height="25" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="220" y="107" text-anchor="middle" font-size="10" fill="#2e7d32">Stream 3: GET /app.js</text>
  <line x1="320" y1="102" x2="410" y2="102" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrowd3_02_http)"/>
  <rect x="180" y="120" width="230" height="25" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="220" y="137" text-anchor="middle" font-size="10" fill="#c62828">Stream 4: GET /image.png</text>
  <line x1="320" y1="132" x2="410" y2="132" stroke="#c62828" stroke-width="2" marker-end="url(#arrowd3_02_http)"/>
  <text x="295" y="165" text-anchor="middle" font-size="10" fill="#555">All streams multiplexed over single connection</text>
  <text x="295" y="180" text-anchor="middle" font-size="10" fill="#555">Binary framing + HPACK header compression</text>
</svg>

---

## HTTP/2 Server Push

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd4_02_http" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="70" y="5" width="100" height="25" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="120" y="22" text-anchor="middle" font-size="11" font-weight="bold">Client</text>
  <rect x="420" y="5" width="100" height="25" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="470" y="22" text-anchor="middle" font-size="11" font-weight="bold">Server</text>
  <line x1="120" y1="35" x2="120" y2="195" stroke="#333" stroke-width="2"/>
  <line x1="470" y1="35" x2="470" y2="195" stroke="#333" stroke-width="2"/>
  <line x1="120" y1="50" x2="470" y2="58" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd4_02_http)"/>
  <text x="295" y="46" text-anchor="middle" font-size="10" fill="#1565c0">GET /index.html (Stream 1)</text>
  <line x1="470" y1="72" x2="120" y2="80" stroke="#2e7d32" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd4_02_http)"/>
  <text x="295" y="72" text-anchor="middle" font-size="10" fill="#2e7d32">200 OK + HTML (Stream 1)</text>
  <line x1="470" y1="95" x2="120" y2="103" stroke="#7b1fa2" stroke-width="2" marker-end="url(#arrowd4_02_http)"/>
  <text x="295" y="95" text-anchor="middle" font-size="10" fill="#7b1fa2">PUSH_PROMISE: /style.css (Stream 2)</text>
  <line x1="470" y1="118" x2="120" y2="126" stroke="#7b1fa2" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd4_02_http)"/>
  <text x="295" y="118" text-anchor="middle" font-size="10" fill="#7b1fa2">Push: style.css data (Stream 2)</text>
  <line x1="470" y1="141" x2="120" y2="149" stroke="#c62828" stroke-width="2" marker-end="url(#arrowd4_02_http)"/>
  <text x="295" y="141" text-anchor="middle" font-size="10" fill="#c62828">PUSH_PROMISE: /app.js (Stream 4)</text>
  <line x1="470" y1="164" x2="120" y2="172" stroke="#c62828" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd4_02_http)"/>
  <text x="295" y="164" text-anchor="middle" font-size="10" fill="#c62828">Push: app.js data (Stream 4)</text>
  <text x="295" y="192" text-anchor="middle" font-size="10" fill="#555">Server proactively sends resources before client requests them</text>
</svg>

---

## HTTP/3 (2022)

- Based on QUIC protocol (Quick UDP Internet Connections)
- Replaces TCP with UDP
- Improved performance on poor networks
- Reduced connection establishment time
- Better multiplexing without head-of-line blocking

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd5_02_http" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="18" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">HTTP/3 Protocol Stack</text>
  <rect x="150" y="30" width="300" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="52" text-anchor="middle" font-size="12" font-weight="bold">HTTP/3 (Application)</text>
  <rect x="150" y="70" width="300" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="92" text-anchor="middle" font-size="12" font-weight="bold">QPACK (Header Compression)</text>
  <rect x="150" y="110" width="300" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="132" text-anchor="middle" font-size="12" font-weight="bold">QUIC (Transport + TLS 1.3)</text>
  <rect x="150" y="150" width="300" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="172" text-anchor="middle" font-size="12" font-weight="bold">UDP</text>
  <text x="520" y="52" text-anchor="middle" font-size="10" fill="#555">Semantics</text>
  <text x="520" y="92" text-anchor="middle" font-size="10" fill="#555">Compression</text>
  <text x="520" y="132" text-anchor="middle" font-size="10" fill="#555">Reliability + Encryption</text>
  <text x="520" y="172" text-anchor="middle" font-size="10" fill="#555">Datagrams</text>
  <text x="80" y="92" text-anchor="middle" font-size="10" fill="#c62828">No TCP!</text>
  <text x="80" y="112" text-anchor="middle" font-size="10" fill="#c62828">No HOL</text>
  <text x="80" y="127" text-anchor="middle" font-size="10" fill="#c62828">blocking</text>
</svg>

---

## HTTP/3 Connection Establishment

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd6_02_http" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="70" y="5" width="100" height="25" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="120" y="22" text-anchor="middle" font-size="11" font-weight="bold">Client</text>
  <rect x="420" y="5" width="100" height="25" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="470" y="22" text-anchor="middle" font-size="11" font-weight="bold">Server</text>
  <line x1="120" y1="35" x2="120" y2="195" stroke="#333" stroke-width="2"/>
  <line x1="470" y1="35" x2="470" y2="195" stroke="#333" stroke-width="2"/>
  <line x1="120" y1="55" x2="470" y2="65" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd6_02_http)"/>
  <text x="295" y="50" text-anchor="middle" font-size="10" fill="#1565c0">QUIC Initial (ClientHello + TLS 1.3)</text>
  <line x1="470" y1="85" x2="120" y2="95" stroke="#2e7d32" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd6_02_http)"/>
  <text x="295" y="82" text-anchor="middle" font-size="10" fill="#2e7d32">QUIC Handshake (ServerHello + TLS)</text>
  <line x1="120" y1="110" x2="470" y2="120" stroke="#7b1fa2" stroke-width="2" marker-end="url(#arrowd6_02_http)"/>
  <text x="295" y="110" text-anchor="middle" font-size="10" fill="#7b1fa2">QUIC Handshake Done + HTTP/3 Request</text>
  <rect x="490" y="50" width="100" height="40" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3" opacity="0.8"/>
  <text x="540" y="65" text-anchor="middle" font-size="10" fill="#555">0-RTT possible</text>
  <text x="540" y="80" text-anchor="middle" font-size="10" fill="#555">on reconnect!</text>
  <rect x="140" y="135" width="310" height="25" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3" opacity="0.5"/>
  <text x="295" y="152" text-anchor="middle" font-size="10" fill="#333">Transport + TLS handshake combined = 1 RTT (vs 3 RTT in TCP+TLS)</text>
  <text x="295" y="185" text-anchor="middle" font-size="10" fill="#555">QUIC eliminates separate TCP and TLS handshakes</text>
</svg>

---

## Version Comparison
| Feature           | HTTP/1.0 | HTTP/1.1 | HTTP/2   | HTTP/3   |
|-------------------|----------|----------|----------|----------|
| Connections       | One-off  | Persistent | Multiplexed | Multiplexed |
| Compression       | No       | Yes      | HPACK    | QPACK    |
| Multiplexing      | No       | Limited  | Yes      | Yes      |
| Server Push       | No       | No       | Yes      | Yes      |
| HOL Blocking      | Yes      | Yes      | Reduced  | Eliminated |
| Transport Protocol| TCP      | TCP      | TCP      | UDP (QUIC) |
---
## Key Takeaways

1. HTTP has evolved to meet increasing web demands
1. Each version improved performance and capabilities
1. HTTP/2 and HTTP/3 focus on multiplexing and reducing latency
1. Modern websites benefit from using the latest HTTP version
1. Understanding HTTP versions helps in web optimization
---

## Final image of HTTP1.1

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd7_02_http" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="70" y="5" width="100" height="25" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="120" y="22" text-anchor="middle" font-size="11" font-weight="bold">Client</text>
  <rect x="420" y="5" width="100" height="25" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="470" y="22" text-anchor="middle" font-size="11" font-weight="bold">Server</text>
  <line x1="120" y1="35" x2="120" y2="195" stroke="#333" stroke-width="2"/>
  <line x1="470" y1="35" x2="470" y2="195" stroke="#333" stroke-width="2"/>
  <line x1="120" y1="48" x2="470" y2="55" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd7_02_http)"/>
  <text x="295" y="44" text-anchor="middle" font-size="10" fill="#1565c0">TCP Connect (persistent, Keep-Alive)</text>
  <line x1="120" y1="70" x2="470" y2="75" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd7_02_http)"/>
  <text x="295" y="67" text-anchor="middle" font-size="10" fill="#1565c0">GET /index.html HTTP/1.1</text>
  <line x1="470" y1="85" x2="120" y2="90" stroke="#2e7d32" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd7_02_http)"/>
  <text x="295" y="87" text-anchor="middle" font-size="10" fill="#2e7d32">HTTP/1.1 200 OK (chunked)</text>
  <line x1="120" y1="105" x2="470" y2="110" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd7_02_http)"/>
  <text x="295" y="104" text-anchor="middle" font-size="10" fill="#1565c0">GET /style.css HTTP/1.1</text>
  <line x1="470" y1="120" x2="120" y2="125" stroke="#2e7d32" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd7_02_http)"/>
  <text x="295" y="121" text-anchor="middle" font-size="10" fill="#2e7d32">HTTP/1.1 200 OK</text>
  <line x1="120" y1="140" x2="470" y2="145" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd7_02_http)"/>
  <text x="295" y="139" text-anchor="middle" font-size="10" fill="#1565c0">GET /app.js HTTP/1.1</text>
  <line x1="470" y1="155" x2="120" y2="160" stroke="#2e7d32" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrowd7_02_http)"/>
  <text x="295" y="157" text-anchor="middle" font-size="10" fill="#2e7d32">HTTP/1.1 200 OK</text>
  <text x="295" y="185" text-anchor="middle" font-size="10" fill="#555">Persistent connection: sequential requests on same TCP connection</text>
</svg>
