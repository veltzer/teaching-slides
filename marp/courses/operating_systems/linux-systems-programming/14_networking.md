# Networking in Linux

---

## Chapter Overview

1. **Socket Basics**
1. **TCP Programming**
1. **UDP Programming**
1. **Socket Domains**
1. **Advanced Networking**
1. **Network Namespaces & VRFs**
1. **Debugging & Performance**

---

## What are Sockets?

## Definition:
- **Endpoints** for communication
- **File descriptors** in Unix
- **Bidirectional** data flow
- **Network** or local communication
- **Multiple protocols** support

"Everything is a file" - Including network connections!

---

## Socket Architecture

![socket_architecture](svg/courses/operating_systems/linux-systems-programming/14_networking/socket_architecture.svg)

---

## Socket Types and Protocols

```c
// Socket domains (address families)
AF_UNIX, AF_LOCAL  // Local communication
AF_INET           // IPv4
AF_INET6          // IPv6
AF_PACKET         // Raw packet
AF_NETLINK        // Kernel communication

// Socket types
SOCK_STREAM       // TCP - reliable, ordered
SOCK_DGRAM        // UDP - unreliable datagrams
SOCK_RAW          // Raw network protocol
SOCK_SEQPACKET    // Reliable datagrams

// Common protocols
IPPROTO_TCP       // TCP
IPPROTO_UDP       // UDP
IPPROTO_ICMP      // ICMP (ping)
IPPROTO_RAW       // Raw IP
```

---

## TCP Server - Basic Flow

```c
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int create_tcp_server(int port) {
    // 1. Create socket
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);

    // 2. Set socket options
    int opt = 1;
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR,
               &opt, sizeof(opt));

    // 3. Bind to address
    struct sockaddr_in addr = {
        .sin_family = AF_INET,
        .sin_port = htons(port),
        .sin_addr.s_addr = INADDR_ANY
    };
    bind(sockfd, (struct sockaddr*)&addr, sizeof(addr));

    // 4. Listen for connections
    listen(sockfd, SOMAXCONN);

    // 5. Accept connections
    struct sockaddr_in client_addr;
    socklen_t len = sizeof(client_addr);
    int client = accept(sockfd, (struct sockaddr*)&client_addr, &len);

    return client;
}
```

---

## TCP Client - Basic Flow

```c
int connect_tcp_client(const char *server, int port) {
    // 1. Create socket
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        perror("socket");
        return -1;
    }

    // 2. Setup server address
    struct sockaddr_in addr = {
        .sin_family = AF_INET,
        .sin_port = htons(port)
    };

    // Convert IP address
    if (inet_pton(AF_INET, server, &addr.sin_addr) <= 0) {
        perror("inet_pton");
        return -1;
    }

    // 3. Connect to server
    if (connect(sockfd, (struct sockaddr*)&addr,
                sizeof(addr)) < 0) {
        perror("connect");
        return -1;
    }

    return sockfd;
}
```

---

## Socket State Diagram - TCP

![socket_state_diagram_tcp](svg/courses/operating_systems/linux-systems-programming/14_networking/socket_state_diagram_tcp.svg)

---

## Complete TCP Server

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 8080
#define BACKLOG 10

int main() {
    int server_fd, client_fd;
    struct sockaddr_in address;
    int addrlen = sizeof(address);

    // Create socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);

    // Allow port reuse
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR,
               &opt, sizeof(opt));

    // Bind
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);
    bind(server_fd, (struct sockaddr*)&address, sizeof(address));

    // Listen
    listen(server_fd, BACKLOG);
    printf("Server listening on port %d\n", PORT);

    // Accept loop
    while (1) {
        client_fd = accept(server_fd,
                          (struct sockaddr*)&address,
                          (socklen_t*)&addrlen);

        // Handle client
        char buffer[1024] = {0};
        read(client_fd, buffer, 1024);
        printf("Received: %s\n", buffer);

        send(client_fd, "Hello from server", 17, 0);
        close(client_fd);
    }
}
```

---

## Socket Options

```c
// Common socket options
int sockfd = socket(AF_INET, SOCK_STREAM, 0);

// SO_REUSEADDR - Reuse local address
int reuse = 1;
setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR,
           &reuse, sizeof(reuse));

// SO_REUSEPORT - Multiple binds to same port
setsockopt(sockfd, SOL_SOCKET, SO_REUSEPORT,
           &reuse, sizeof(reuse));

// SO_KEEPALIVE - Enable keep-alive
int keepalive = 1;
setsockopt(sockfd, SOL_SOCKET, SO_KEEPALIVE,
           &keepalive, sizeof(keepalive));

// SO_RCVTIMEO - Receive timeout
struct timeval tv = {.tv_sec = 5, .tv_usec = 0};
setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO,
           &tv, sizeof(tv));

// TCP_NODELAY - Disable Nagle's algorithm
int nodelay = 1;
setsockopt(sockfd, IPPROTO_TCP, TCP_NODELAY,
           &nodelay, sizeof(nodelay));

// SO_LINGER - Linger on close
struct linger lng = {.l_onoff = 1, .l_linger = 5};
setsockopt(sockfd, SOL_SOCKET, SO_LINGER,
           &lng, sizeof(lng));
```

---

## Non-blocking Sockets

```c
#include <fcntl.h>

// Make socket non-blocking
int make_nonblocking(int sockfd) {
    int flags = fcntl(sockfd, F_GETFL, 0);
    if (flags == -1) return -1;

    flags |= O_NONBLOCK;
    return fcntl(sockfd, F_SETFL, flags);
}

// Non-blocking accept
int client_fd = accept(server_fd, NULL, NULL);
if (client_fd == -1) {
    if (errno == EAGAIN || errno == EWOULDBLOCK) {
        // No connections pending
    } else {
        perror("accept");
    }
}

// Non-blocking read
ssize_t n = recv(sockfd, buffer, sizeof(buffer), 0);
if (n == -1) {
    if (errno == EAGAIN || errno == EWOULDBLOCK) {
        // No data available
    } else {
        perror("recv");
    }
} else if (n == 0) {
    // Connection closed
}
```

---

## UDP Server

```c
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>

#define PORT 8080
#define MAXLINE 1024

int main() {
    int sockfd;
    char buffer[MAXLINE];
    struct sockaddr_in servaddr, cliaddr;

    // Create UDP socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    memset(&servaddr, 0, sizeof(servaddr));
    memset(&cliaddr, 0, sizeof(cliaddr));

    // Server information
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(PORT);

    // Bind socket
    bind(sockfd, (struct sockaddr*)&servaddr,
         sizeof(servaddr));

    socklen_t len = sizeof(cliaddr);

    while (1) {
        // Receive datagram
        int n = recvfrom(sockfd, buffer, MAXLINE, 0,
                        (struct sockaddr*)&cliaddr, &len);
        buffer[n] = '\0';
        printf("Client: %s\n", buffer);

        // Send response
        sendto(sockfd, "ACK", 3, 0,
               (struct sockaddr*)&cliaddr, len);
    }
}
```

---

## UDP Client

```c
int main() {
    int sockfd;
    char buffer[MAXLINE];
    struct sockaddr_in servaddr;

    // Create socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    memset(&servaddr, 0, sizeof(servaddr));

    // Server information
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(PORT);
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");

    // Send message
    const char *message = "Hello UDP Server";
    sendto(sockfd, message, strlen(message), 0,
           (struct sockaddr*)&servaddr, sizeof(servaddr));

    // Receive response
    int n = recvfrom(sockfd, buffer, MAXLINE, 0,
                     NULL, NULL);
    buffer[n] = '\0';
    printf("Server: %s\n", buffer);

    close(sockfd);
}
```

---

## TCP vs UDP Comparison

| Feature | TCP | UDP |
|---------|-----|-----|
| **Connection** | Connection-oriented | Connectionless |
| **Reliability** | Guaranteed delivery | Best effort |
| **Ordering** | In-order delivery | No ordering |
| **Speed** | Slower | Faster |
| **Header Size** | 20 bytes | 8 bytes |
| **Use Cases** | HTTP, SSH, FTP | DNS, VoIP, Gaming |
| **Flow Control** | Yes | No |
| **Congestion Control** | Yes | No |

---

## Unix Domain Sockets

```c
#include <sys/un.h>

// Server
int create_unix_server(const char *path) {
    int sockfd = socket(AF_UNIX, SOCK_STREAM, 0);

    struct sockaddr_un addr;
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, path, sizeof(addr.sun_path)-1);

    unlink(path);  // Remove if exists

    bind(sockfd, (struct sockaddr*)&addr, sizeof(addr));
    listen(sockfd, 5);

    return sockfd;
}

// Client
int connect_unix_client(const char *path) {
    int sockfd = socket(AF_UNIX, SOCK_STREAM, 0);

    struct sockaddr_un addr;
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, path, sizeof(addr.sun_path)-1);

    connect(sockfd, (struct sockaddr*)&addr, sizeof(addr));

    return sockfd;
}
```

---

## AF_UNIX vs AF_INET Performance

![afunix_vs_afinet_performance](svg/courses/operating_systems/linux-systems-programming/14_networking/afunix_vs_afinet_performance.svg)

---

## select() - I/O Multiplexing

```c
#include <sys/select.h>

void handle_multiple_clients(int server_fd) {
    fd_set master_set, read_fds;
    int max_fd = server_fd;

    FD_ZERO(&master_set);
    FD_SET(server_fd, &master_set);

    while (1) {
        read_fds = master_set;

        // Wait for activity
        if (select(max_fd + 1, &read_fds, NULL, NULL, NULL) == -1) {
            perror("select");
            exit(1);
        }

        for (int fd = 0; fd <= max_fd; fd++) {
            if (FD_ISSET(fd, &read_fds)) {
                if (fd == server_fd) {
                    // New connection
                    int client = accept(server_fd, NULL, NULL);
                    FD_SET(client, &master_set);
                    if (client > max_fd) max_fd = client;
                } else {
                    // Data from client
                    char buf[256];
                    int n = recv(fd, buf, sizeof(buf), 0);
                    if (n <= 0) {
                        // Connection closed
                        close(fd);
                        FD_CLR(fd, &master_set);
                    } else {
                        // Process data
                        send(fd, buf, n, 0);  // Echo
                    }
                }
            }
        }
    }
}
```

---

## poll() - Better than select()

```c
#include <poll.h>

#define MAX_CLIENTS 1000

void poll_server(int server_fd) {
    struct pollfd fds[MAX_CLIENTS];
    int nfds = 1;

    // Add server socket
    fds[0].fd = server_fd;
    fds[0].events = POLLIN;

    while (1) {
        int ret = poll(fds, nfds, -1);  // -1 = wait forever

        if (ret < 0) {
            perror("poll");
            exit(1);
        }

        // Check server socket
        if (fds[0].revents & POLLIN) {
            int client = accept(server_fd, NULL, NULL);
            fds[nfds].fd = client;
            fds[nfds].events = POLLIN;
            nfds++;
        }

        // Check client sockets
        for (int i = 1; i < nfds; i++) {
            if (fds[i].revents & POLLIN) {
                char buf[256];
                int n = recv(fds[i].fd, buf, sizeof(buf), 0);
                if (n <= 0) {
                    close(fds[i].fd);
                    fds[i] = fds[--nfds];  // Remove
                    i--;
                } else {
                    send(fds[i].fd, buf, n, 0);
                }
            }
        }
    }
}
```

---

## epoll() - Linux High Performance

```c
#include <sys/epoll.h>

#define MAX_EVENTS 10

void epoll_server(int server_fd) {
    struct epoll_event ev, events[MAX_EVENTS];
    int epollfd = epoll_create1(0);

    // Add server socket
    ev.events = EPOLLIN;
    ev.data.fd = server_fd;
    epoll_ctl(epollfd, EPOLL_CTL_ADD, server_fd, &ev);

    while (1) {
        int nfds = epoll_wait(epollfd, events, MAX_EVENTS, -1);

        for (int i = 0; i < nfds; i++) {
            if (events[i].data.fd == server_fd) {
                // New connection
                int client = accept(server_fd, NULL, NULL);

                // Make non-blocking
                make_nonblocking(client);

                // Add to epoll
                ev.events = EPOLLIN | EPOLLET;  // Edge-triggered
                ev.data.fd = client;
                epoll_ctl(epollfd, EPOLL_CTL_ADD, client, &ev);
            } else {
                // Handle client data
                handle_client(events[i].data.fd);
            }
        }
    }
}
```

---

## I/O Multiplexing Comparison

| Feature | select() | poll() | epoll() |
|---------|----------|--------|---------|
| **Max FDs** | 1024 (typical) | No limit | No limit |
| **Performance** | O(n) | O(n) | O(1) |
| **Portability** | POSIX | POSIX | Linux only |
| **Interface** | fd_set | pollfd array | epoll_event |
| **Edge-trigger** | No | No | Yes |
| **Modify set** | Rebuild | Rebuild | Add/remove |

---

## Raw Sockets

```c
#include <netinet/ip.h>
#include <netinet/tcp.h>

// Create raw socket (requires root)
int create_raw_socket() {
    int sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
    if (sockfd < 0) {
        perror("socket");
        exit(1);
    }

    // Enable IP header inclusion
    int on = 1;
    setsockopt(sockfd, IPPROTO_IP, IP_HDRINCL, &on, sizeof(on));

    return sockfd;
}

// Receive raw packets
void receive_raw_packets(int sockfd) {
    unsigned char buffer[65536];

    while (1) {
        int data_size = recv(sockfd, buffer, sizeof(buffer), 0);

        // Parse IP header
        struct iphdr *iph = (struct iphdr*)buffer;

        // Parse TCP header
        struct tcphdr *tcph = (struct tcphdr*)
            (buffer + iph->ihl * 4);

        printf("Source IP: %s\n",
               inet_ntoa(*(struct in_addr*)&iph->saddr));
        printf("Source Port: %d\n", ntohs(tcph->source));
    }
}
```

---

## Netlink Sockets

```c
#include <linux/netlink.h>
#include <linux/rtnetlink.h>

// Monitor network events
int create_netlink_socket() {
    int sockfd = socket(AF_NETLINK, SOCK_RAW, NETLINK_ROUTE);

    struct sockaddr_nl addr = {
        .nl_family = AF_NETLINK,
        .nl_groups = RTMGRP_LINK | RTMGRP_IPV4_IFADDR
    };

    bind(sockfd, (struct sockaddr*)&addr, sizeof(addr));

    return sockfd;
}

// Read network events
void monitor_network_events(int sockfd) {
    char buffer[4096];

    while (1) {
        int len = recv(sockfd, buffer, sizeof(buffer), 0);
        struct nlmsghdr *nlh = (struct nlmsghdr*)buffer;

        while (NLMSG_OK(nlh, len)) {
            if (nlh->nlmsg_type == RTM_NEWLINK) {
                printf("Network interface added/changed\n");
            } else if (nlh->nlmsg_type == RTM_DELLINK) {
                printf("Network interface removed\n");
            }

            nlh = NLMSG_NEXT(nlh, len);
        }
    }
}
```

---

## Network Namespaces

```c
#define _GNU_SOURCE
#include <sched.h>

// Create network namespace
void create_network_namespace() {
    // Requires CAP_SYS_ADMIN
    if (unshare(CLONE_NEWNET) == -1) {
        perror("unshare");
        exit(1);
    }

    // Now in new network namespace
    // Only loopback interface exists
    system("ip link");  // Shows only 'lo'

    // Create veth pair to connect namespaces
    system("ip link add veth0 type veth peer name veth1");
}

// Enter existing namespace
void enter_network_namespace(const char *name) {
    char path[256];
    snprintf(path, sizeof(path), "/var/run/netns/%s", name);

    int fd = open(path, O_RDONLY);
    if (setns(fd, CLONE_NEWNET) == -1) {
        perror("setns");
    }
    close(fd);
}
```

---

## VRF (Virtual Routing and Forwarding)

```bash
# Create VRF device
ip link add dev vrf-blue type vrf table 10
ip link set dev vrf-blue up

# Assign interface to VRF
ip link set dev eth1 master vrf-blue

# Add route to VRF table
ip route add 10.0.0.0/24 dev eth1 table 10

# Run command in VRF context
ip vrf exec vrf-blue ping 10.0.0.1
```

```c
// Bind socket to VRF
int bind_to_vrf(int sockfd, const char *vrf_name) {
    if (setsockopt(sockfd, SOL_SOCKET, SO_BINDTODEVICE,
                   vrf_name, strlen(vrf_name)) < 0) {
        perror("setsockopt SO_BINDTODEVICE");
        return -1;
    }
    return 0;
}
```

---

## Network Namespaces vs VRF

| Feature | Network Namespaces | VRF |
|---------|-------------------|-----|
| **Isolation** | Complete | Routing only |
| **Resource Usage** | Higher | Lower |
| **Management** | Complex | Simple |
| **Use Case** | Containers | Multi-tenant routing |
| **Performance** | More overhead | Less overhead |
| **Compatibility** | Requires namespace support | Works with regular tools |
