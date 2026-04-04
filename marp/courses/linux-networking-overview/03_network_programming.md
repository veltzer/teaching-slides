# Network C Programming Essentials
## Chapter 3: Socket Programming in Linux

---

## Chapter Overview

- Stream Socket Programming
- Socket API Functions
- C Library Utilities
- Datagram Socket Programming
- Socket Options
- Quality of Service
- Out of Band Data

---

## Socket Programming Basics

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd0_02_network_programming" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="16" text-anchor="middle" font-size="12" font-weight="bold">TCP Socket API Flow</text>
  <rect x="30" y="30" width="130" height="160" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="95" y="48" text-anchor="middle" font-size="11" font-weight="bold">Server</text>
  <rect x="45" y="55" width="100" height="22" fill="#fff" stroke="#333" stroke-width="1" rx="2"/>
  <text x="95" y="70" text-anchor="middle" font-size="10">socket()</text>
  <rect x="45" y="80" width="100" height="22" fill="#fff" stroke="#333" stroke-width="1" rx="2"/>
  <text x="95" y="95" text-anchor="middle" font-size="10">bind()</text>
  <rect x="45" y="105" width="100" height="22" fill="#fff" stroke="#333" stroke-width="1" rx="2"/>
  <text x="95" y="120" text-anchor="middle" font-size="10">listen()</text>
  <rect x="45" y="130" width="100" height="22" fill="#fff3e0" stroke="#333" stroke-width="1" rx="2"/>
  <text x="95" y="145" text-anchor="middle" font-size="10">accept()</text>
  <rect x="45" y="155" width="100" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="2"/>
  <text x="95" y="170" text-anchor="middle" font-size="10">recv() / send()</text>
  <rect x="440" y="30" width="130" height="160" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="505" y="48" text-anchor="middle" font-size="11" font-weight="bold">Client</text>
  <rect x="455" y="55" width="100" height="22" fill="#fff" stroke="#333" stroke-width="1" rx="2"/>
  <text x="505" y="70" text-anchor="middle" font-size="10">socket()</text>
  <rect x="455" y="105" width="100" height="22" fill="#fff3e0" stroke="#333" stroke-width="1" rx="2"/>
  <text x="505" y="120" text-anchor="middle" font-size="10">connect()</text>
  <rect x="455" y="155" width="100" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="2"/>
  <text x="505" y="170" text-anchor="middle" font-size="10">send() / recv()</text>
  <line x1="455" y1="116" x2="145" y2="141" stroke="#333" stroke-width="1" stroke-dasharray="4,3" marker-end="url(#arrowd0_02_network_programming)"/>
  <text x="300" y="118" text-anchor="middle" font-size="9" fill="#666">3-way handshake</text>
  <line x1="145" y1="166" x2="455" y2="166" stroke="#2e7d32" stroke-width="1" marker-end="url(#arrowd0_02_network_programming)"/>
  <line x1="455" y1="172" x2="145" y2="172" stroke="#1565c0" stroke-width="1" marker-end="url(#arrowd0_02_network_programming)"/>
  <text x="300" y="163" text-anchor="middle" font-size="9" fill="#2e7d32">data exchange</text>
</svg>

---

## Socket Creation

```c
int socket(int domain, int type, int protocol);

// Example:
int sock = socket(AF_INET, SOCK_STREAM, 0);
if (sock == -1) {
    perror("socket failed");
    exit(EXIT_FAILURE);
}
```

**Domains:**
- AF_INET (IPv4)
- AF_INET6 (IPv6)
- AF_UNIX (Unix domain)

---

## Socket Types

**Stream Sockets (SOCK_STREAM):**
- Connection-oriented
- Reliable delivery
- Used with TCP

**Datagram Sockets (SOCK_DGRAM):**
- Connectionless
- Unreliable delivery
- Used with UDP

---

## Address Structures

```c
// IPv4 address structure
struct sockaddr_in {
    sa_family_t     sin_family;
    in_port_t       sin_port;
    struct in_addr  sin_addr;
};

// IPv6 address structure
struct sockaddr_in6 {
    sa_family_t     sin6_family;
    in_port_t       sin6_port;
    uint32_t        sin6_flowinfo;
    struct in6_addr sin6_addr;
    uint32_t        sin6_scope_id;
};
```

---

## Binding Sockets

```c
int bind(int sockfd, const struct sockaddr *addr,
         socklen_t addrlen);

// Example:
struct sockaddr_in server_addr = {0};
server_addr.sin_family = AF_INET;
server_addr.sin_port = htons(8080);
server_addr.sin_addr.s_addr = INADDR_ANY;

if (bind(sock, (struct sockaddr*)&server_addr,
         sizeof(server_addr)) == -1) {
    perror("bind failed");
    exit(EXIT_FAILURE);
}
```

---

## Listen for Connections

```c
int listen(int sockfd, int backlog);

// Example:
if (listen(sock, SOMAXCONN) == -1) {
    perror("listen failed");
    exit(EXIT_FAILURE);
}
```

**Backlog Values:**
- SOMAXCONN (System maximum)
- Typical values: 5-128
- Configurable via sysctl

---

## Accepting Connections

```c
int accept(int sockfd, struct sockaddr *addr,
           socklen_t *addrlen);

// Example:
struct sockaddr_in client_addr;
socklen_t client_len = sizeof(client_addr);

int client_sock = accept(sock,
    (struct sockaddr*)&client_addr, &client_len);
if (client_sock == -1) {
    perror("accept failed");
    exit(EXIT_FAILURE);
}
```

---

## Complete TCP Server Example

```c
int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in address = {0};
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(8080);

    bind(server_fd, (struct sockaddr*)&address, sizeof(address));
    listen(server_fd, 3);

    while(1) {
        int client_fd = accept(server_fd, NULL, NULL);
        // Handle client connection
    }
}
```

---

## Connecting to Server

```c
int connect(int sockfd, const struct sockaddr *addr,
           socklen_t addrlen);

// Example:
struct sockaddr_in server_addr = {0};
server_addr.sin_family = AF_INET;
server_addr.sin_port = htons(8080);
inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr);

if (connect(sock, (struct sockaddr*)&server_addr,
           sizeof(server_addr)) == -1) {
    perror("connect failed");
    exit(EXIT_FAILURE);
}
```

---

## Data Transfer Functions

```c
ssize_t read(int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);
ssize_t recv(int sockfd, void *buf, size_t len, int flags);
ssize_t send(int sockfd, const void *buf, size_t len, int flags);
```

---

## Send/Recv Flags

| Flag | Description |
|------|-------------|
| MSG_PEEK | Look at data without removing |
| MSG_OOB | Send/receive out-of-band data |
| MSG_WAITALL | Wait for full buffer |
| MSG_DONTWAIT | Non-blocking operation |
| MSG_NOSIGNAL | Don't send SIGPIPE |

---

## Utility Functions: Host Lookup

```c
struct hostent *gethostbyname(const char *name);

// Example:
struct hostent *he = gethostbyname("www.example.com");
if (he == NULL) {
    herror("gethostbyname failed");
    exit(EXIT_FAILURE);
}
```

---

## Utility Functions: Service Lookup

```c
struct servent *getservbyname(const char *name,
                            const char *proto);

// Example:
struct servent *se = getservbyname("http", "tcp");
if (se == NULL) {
    perror("getservbyname failed");
    exit(EXIT_FAILURE);
}
```

---

## UDP Programming

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd1_02_network_programming" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="16" text-anchor="middle" font-size="12" font-weight="bold">UDP Socket API Flow</text>
  <rect x="30" y="30" width="130" height="155" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="95" y="48" text-anchor="middle" font-size="11" font-weight="bold">Server</text>
  <rect x="45" y="55" width="100" height="22" fill="#fff" stroke="#333" stroke-width="1" rx="2"/>
  <text x="95" y="70" text-anchor="middle" font-size="10">socket(DGRAM)</text>
  <rect x="45" y="82" width="100" height="22" fill="#fff" stroke="#333" stroke-width="1" rx="2"/>
  <text x="95" y="97" text-anchor="middle" font-size="10">bind()</text>
  <rect x="45" y="115" width="100" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="2"/>
  <text x="95" y="130" text-anchor="middle" font-size="10">recvfrom()</text>
  <rect x="45" y="145" width="100" height="22" fill="#fff3e0" stroke="#333" stroke-width="1" rx="2"/>
  <text x="95" y="160" text-anchor="middle" font-size="10">sendto()</text>
  <rect x="440" y="30" width="130" height="155" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="505" y="48" text-anchor="middle" font-size="11" font-weight="bold">Client</text>
  <rect x="455" y="55" width="100" height="22" fill="#fff" stroke="#333" stroke-width="1" rx="2"/>
  <text x="505" y="70" text-anchor="middle" font-size="10">socket(DGRAM)</text>
  <rect x="455" y="115" width="100" height="22" fill="#fff3e0" stroke="#333" stroke-width="1" rx="2"/>
  <text x="505" y="130" text-anchor="middle" font-size="10">sendto()</text>
  <rect x="455" y="145" width="100" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="2"/>
  <text x="505" y="160" text-anchor="middle" font-size="10">recvfrom()</text>
  <line x1="455" y1="126" x2="145" y2="126" stroke="#333" stroke-width="1" marker-end="url(#arrowd1_02_network_programming)"/>
  <text x="300" y="122" text-anchor="middle" font-size="9" fill="#666">datagram (no connection)</text>
  <line x1="145" y1="156" x2="455" y2="156" stroke="#333" stroke-width="1" marker-end="url(#arrowd1_02_network_programming)"/>
  <text x="300" y="152" text-anchor="middle" font-size="9" fill="#666">reply datagram</text>
  <text x="300" y="195" text-anchor="middle" font-size="10" fill="#999">No connect/listen/accept needed</text>
</svg>

---

## UDP Server Example

```c
// UDP Server receiving data
struct sockaddr_in client_addr;
socklen_t client_len = sizeof(client_addr);
char buffer[1024];

ssize_t received = recvfrom(sock, buffer, sizeof(buffer), 0,
    (struct sockaddr*)&client_addr, &client_len);
if (received == -1) {
    perror("recvfrom failed");
    exit(EXIT_FAILURE);
}
```

---

## UDP Client Example

```c
// UDP Client sending data
struct sockaddr_in server_addr = {0};
server_addr.sin_family = AF_INET;
server_addr.sin_port = htons(8080);
inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr);

ssize_t sent = sendto(sock, "Hello", 5, 0,
    (struct sockaddr*)&server_addr, sizeof(server_addr));
if (sent == -1) {
    perror("sendto failed");
    exit(EXIT_FAILURE);
}
```

---

## Socket Options

```c
int setsockopt(int sockfd, int level, int optname,
               const void *optval, socklen_t optlen);
int getsockopt(int sockfd, int level, int optname,
               void *optval, socklen_t *optlen);
```

---

## Common Socket Options

| Option | Level | Purpose |
|--------|-------|---------|
| SO_REUSEADDR | SOL_SOCKET | Allow address reuse |
| SO_KEEPALIVE | SOL_SOCKET | Keep connection alive |
| TCP_NODELAY | IPPROTO_TCP | Disable Nagle's algorithm |
| IP_TOS | IPPROTO_IP | Set Type of Service |

---

## Setting IP_TOS (QoS)

```c
int tos = IPTOS_LOWDELAY;  // Priority for low delay
if (setsockopt(sock, IPPROTO_IP, IP_TOS,
               &tos, sizeof(tos)) == -1) {
    perror("setsockopt IP_TOS failed");
    exit(EXIT_FAILURE);
}
```

---

## Traffic Control (tc)

```bash
# Set priority for outgoing traffic
tc qdisc add dev eth0 root handle 1: prio

# Add filter based on TOS
tc filter add dev eth0 parent 1: protocol ip prio 1 \
    u32 match ip tos 0x10 0xff flowid 1:1
```

---

## Out of Band Data

```c
// Sending OOB data
send(sock, "!", 1, MSG_OOB);

// Receiving OOB data
char oob_byte;
recv(sock, &oob_byte, 1, MSG_OOB);

// Check for OOB data
int is_oob;
ioctl(sock, SIOCATMARK, &is_oob);
```

---

## Error Handling

```c
// Get last error
int err = errno;
char *err_str = strerror(err);

// Print error message
perror("Operation failed");

// Get detailed socket error
int error;
socklen_t len = sizeof(error);
getsockopt(sock, SOL_SOCKET, SO_ERROR, &error, &len);
```

---

## Best Practices

1. Always check return values
1. Use appropriate buffer sizes
1. Handle partial sends/receives
1. Clean up resources properly
1. Set appropriate socket options
1. Use error handling consistently
1. Consider non-blocking operations

---

## Summary

- Socket API fundamentals
- TCP/UDP programming
- Address handling
- Data transfer
- Socket options
- QoS configuration
- Error handling
