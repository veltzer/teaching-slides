# Socket Programming
## Building Networked Applications

---

## What is a Socket?

- A socket is an endpoint for network communication
- Provides a file-descriptor-like interface for sending/receiving data
- Originated in BSD Unix (1983) -- the "Berkeley Sockets API"
- Available in virtually every programming language
- Two main types: **stream sockets** (TCP) and **datagram sockets** (UDP)

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="290" font-family="sans-serif">
<defs>
  <marker id="arr"  markerWidth="10" markerHeight="7" refX="9"   refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#555"/>
  </marker>
  <marker id="arrl" markerWidth="10" markerHeight="7" refX="1"   refY="3.5" orient="auto">
    <polygon points="10 0,0 3.5,10 7" fill="#555"/>
  </marker>
</defs>
<text x="340" y="22" text-anchor="middle" font-size="14" fill="#222222" font-weight="bold">Socket: Endpoint for Network Communication</text>
<rect x="20" y="40" width="250" height="220" fill="#e3f2fd" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="145" y="64" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">Server Application</text>
<text x="145" y="90" text-anchor="middle" font-size="12" fill="#333">socket()</text>
<text x="145" y="112" text-anchor="middle" font-size="12" fill="#333">bind()</text>
<text x="145" y="134" text-anchor="middle" font-size="12" fill="#333">listen()</text>
<text x="145" y="156" text-anchor="middle" font-size="12" fill="#333">accept()</text>
<rect x="60" y="210" width="170" height="36" fill="#bbdefb" stroke="#1565c0" stroke-width="1.5" rx="4"/>
<text x="145" y="232" text-anchor="middle" font-size="12" fill="#1565c0" font-weight="bold">Socket  fd = 3</text>
<rect x="410" y="40" width="250" height="220" fill="#fff3e0" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="535" y="64" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">Client Application</text>
<text x="535" y="90" text-anchor="middle" font-size="12" fill="#333">socket()</text>
<text x="535" y="112" text-anchor="middle" font-size="12" fill="#333">connect()</text>
<text x="535" y="134" text-anchor="middle" font-size="12" fill="#333">send()</text>
<text x="535" y="156" text-anchor="middle" font-size="12" fill="#333">recv()</text>
<rect x="450" y="210" width="170" height="36" fill="#ffe0b2" stroke="#e65100" stroke-width="1.5" rx="4"/>
<text x="535" y="232" text-anchor="middle" font-size="12" fill="#e65100" font-weight="bold">Socket  fd = 3</text>
<line x1="270" y1="228" x2="410" y2="228" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<line x1="410" y1="218" x2="270" y2="218" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="340" y="210" text-anchor="middle" font-size="11" fill="#555" font-style="italic">Network (TCP/UDP)</text>
</svg>

---

## Socket API: System Call Flow

### TCP Connection Lifecycle

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="410" font-family="sans-serif">
<defs>
  <marker id="arr"  markerWidth="10" markerHeight="7" refX="9"   refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#555"/>
  </marker>
  <marker id="arrl" markerWidth="10" markerHeight="7" refX="1"   refY="3.5" orient="auto">
    <polygon points="10 0,0 3.5,10 7" fill="#555"/>
  </marker>
</defs>
<text x="340" y="22" text-anchor="middle" font-size="14" fill="#222222" font-weight="bold">TCP Socket Lifecycle</text>
<text x="170" y="44" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">Server</text>
<text x="510" y="44" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">Client</text>
<line x1="170" y1="55" x2="170" y2="290" stroke="#aaa" stroke-width="1" stroke-dasharray="4,3"/>
<line x1="510" y1="55" x2="510" y2="290" stroke="#aaa" stroke-width="1" stroke-dasharray="4,3"/>
<text x="170" y="74" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">socket()</text>
<text x="510" y="74" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">socket()</text>
<text x="170" y="99" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">bind()</text>
<text x="170" y="124" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">listen()</text>
<text x="170" y="159" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">accept()</text>
<text x="510" y="159" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">connect()</text>
<line x1="200" y1="165" x2="480" y2="165" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<line x1="480" y1="177" x2="200" y2="177" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="340" y="162" text-anchor="middle" font-size="11" fill="#555" font-style="italic">3-way handshake (SYN→SYN-ACK→ACK)</text>
<text x="170" y="204" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">recv()</text>
<text x="510" y="204" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">send()</text>
<line x1="480" y1="210" x2="200" y2="210" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="340" y="207" text-anchor="middle" font-size="11" fill="#555" font-style="italic">data</text>
<text x="170" y="239" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">send()</text>
<text x="510" y="239" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">recv()</text>
<line x1="200" y1="245" x2="480" y2="245" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="340" y="242" text-anchor="middle" font-size="11" fill="#555" font-style="italic">data</text>
<text x="170" y="274" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">close()</text>
<text x="510" y="274" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">close()</text>
<line x1="200" y1="280" x2="480" y2="280" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<line x1="480" y1="292" x2="200" y2="292" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="340" y="277" text-anchor="middle" font-size="11" fill="#555" font-style="italic">FIN handshake</text>
</svg>

### UDP Communication (no connection)

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="260" font-family="sans-serif">
<defs>
  <marker id="arr"  markerWidth="10" markerHeight="7" refX="9"   refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#555"/>
  </marker>
  <marker id="arrl" markerWidth="10" markerHeight="7" refX="1"   refY="3.5" orient="auto">
    <polygon points="10 0,0 3.5,10 7" fill="#555"/>
  </marker>
</defs>
<text x="340" y="22" text-anchor="middle" font-size="14" fill="#222222" font-weight="bold">UDP Socket Lifecycle</text>
<text x="170" y="44" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">Server</text>
<text x="510" y="44" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">Client</text>
<line x1="170" y1="55" x2="170" y2="240" stroke="#aaa" stroke-width="1" stroke-dasharray="4,3"/>
<line x1="510" y1="55" x2="510" y2="240" stroke="#aaa" stroke-width="1" stroke-dasharray="4,3"/>
<text x="170" y="74" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">socket()</text>
<text x="510" y="74" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">socket()</text>
<text x="170" y="99" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">bind()</text>
<text x="170" y="134" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">recvfrom()</text>
<text x="510" y="134" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">sendto()</text>
<line x1="470" y1="140" x2="210" y2="140" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="340" y="137" text-anchor="middle" font-size="11" fill="#555" font-style="italic">datagram</text>
<text x="170" y="174" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">sendto()</text>
<text x="510" y="174" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">recvfrom()</text>
<line x1="210" y1="180" x2="470" y2="180" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="340" y="177" text-anchor="middle" font-size="11" fill="#555" font-style="italic">datagram</text>
<text x="170" y="214" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">close()</text>
<text x="510" y="214" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">close()</text>
</svg>

---

## TCP Server in Python: Basic

```python
#!/usr/bin/env python3
"""Simple TCP echo server."""

import socket

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow address reuse (avoid "Address already in use" error)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to address and port
server_socket.bind(('0.0.0.0', 8080))

# Start listening (backlog of 5 pending connections)
server_socket.listen(5)
print("Server listening on port 8080...")

while True:
    # Accept a new connection (blocks until client connects)
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    try:
        while True:
            # Receive data (up to 4096 bytes)
            data = client_socket.recv(4096)
            if not data:
                break  # Client disconnected

            print(f"Received: {data.decode()}")

            # Echo the data back
            client_socket.sendall(data)
    except ConnectionResetError:
        print(f"Client {client_address} disconnected abruptly")
    finally:
        client_socket.close()
        print(f"Connection with {client_address} closed")
```

---

## TCP Client in Python: Basic

```python
#!/usr/bin/env python3
"""Simple TCP client."""

import socket

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect(('127.0.0.1', 8080))
print("Connected to server")

try:
    # Send a message
    message = "Hello, Server!"
    client_socket.sendall(message.encode())
    print(f"Sent: {message}")

    # Receive the response
    response = client_socket.recv(4096)
    print(f"Received: {response.decode()}")

finally:
    client_socket.close()
    print("Connection closed")
```

```bash
# Test the echo server
$ python3 tcp_server.py &
Server listening on port 8080...

$ python3 tcp_client.py
Connected to server
Sent: Hello, Server!
Received: Hello, Server!
Connection closed
```

---

## TCP Server: Multi-Client with Threading

The basic server handles only one client at a time. Use threading for concurrency:

```python
#!/usr/bin/env python3
"""Multi-threaded TCP server."""

import socket
import threading

def handle_client(client_socket, client_address):
    """Handle a single client connection."""
    print(f"[+] New connection from {client_address}")
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            print(f"[{client_address}] {data.decode()}")
            client_socket.sendall(data)
    except ConnectionResetError:
        pass
    finally:
        client_socket.close()
        print(f"[-] Connection from {client_address} closed")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 8080))
    server.listen(100)
    print("Server listening on port 8080...")

    while True:
        client_socket, addr = server.accept()
        # Spawn a new thread for each client
        thread = threading.Thread(target=handle_client,
                                  args=(client_socket, addr))
        thread.daemon = True  # Thread dies when main thread dies
        thread.start()

if __name__ == '__main__':
    main()
```

---

## UDP Server and Client in Python

UDP is connectionless -- no handshake, no guaranteed delivery, but lower overhead.

**UDP Server:**

```python
#!/usr/bin/env python3
"""Simple UDP echo server."""

import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('0.0.0.0', 9090))
print("UDP server listening on port 9090...")

while True:
    data, client_address = server_socket.recvfrom(4096)
    print(f"Received from {client_address}: {data.decode()}")

    # Send response back to the client
    server_socket.sendto(data, client_address)
```

**UDP Client:**

```python
#!/usr/bin/env python3
"""Simple UDP client."""

import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# No connect() needed for UDP -- just send directly
message = "Hello, UDP Server!"
client_socket.sendto(message.encode(), ('127.0.0.1', 9090))
print(f"Sent: {message}")

# Receive response (with timeout)
client_socket.settimeout(5.0)
try:
    data, server_address = client_socket.recvfrom(4096)
    print(f"Received from {server_address}: {data.decode()}")
except socket.timeout:
    print("No response received (timeout)")
finally:
    client_socket.close()
```

---

## TCP vs UDP in Code

| Aspect | TCP | UDP |
|--------|-----|-----|
| Socket type | SOCK_STREAM | SOCK_DGRAM |
| Setup | connect() + accept() | No connection |
| Send | send() / sendall() | sendto() |
| Receive | recv() | recvfrom() |
| Reliability | Guaranteed delivery | Best effort |
| Order | Maintained | Not guaranteed |
| Boundaries | Stream (no boundaries) | Message boundaries preserved |

**Message boundary example:**

```python
# TCP: two sends may arrive as one recv
client.send(b"Hello")
client.send(b"World")
# Server recv() might get: b"HelloWorld"

# UDP: each sendto is a separate datagram
client.sendto(b"Hello", addr)
client.sendto(b"World", addr)
# Server recvfrom() gets: b"Hello", then b"World" (separate calls)
```

---

## Important Socket Options

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SO_REUSEADDR: reuse address immediately after server restart
# Without this, you get "Address already in use" for ~60 seconds
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# SO_KEEPALIVE: detect dead connections
sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

# TCP_NODELAY: disable Nagle's algorithm (send immediately)
# Good for interactive/real-time applications, bad for bulk transfers
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

# SO_RCVBUF / SO_SNDBUF: set buffer sizes
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)

# SO_LINGER: control behavior on close()
# linger on, timeout 0 = send RST immediately (abort connection)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,
                 struct.pack('ii', 1, 0))

# Set timeout for blocking operations
sock.settimeout(10.0)  # 10 second timeout
sock.settimeout(0)     # Non-blocking mode
sock.settimeout(None)  # Blocking mode (default)
```

---

## Non-Blocking I/O

By default, socket operations block (wait until complete). Non-blocking mode returns immediately.

```python
#!/usr/bin/env python3
"""Non-blocking socket example."""

import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 8080))
server.listen(5)
server.setblocking(False)  # Non-blocking mode

clients = []
print("Non-blocking server on port 8080...")

while True:
    # Try to accept new connections (non-blocking)
    try:
        client, addr = server.accept()
        client.setblocking(False)
        clients.append(client)
        print(f"New connection from {addr}")
    except BlockingIOError:
        pass  # No pending connections, that's fine

    # Try to read from each connected client
    for client in clients[:]:  # Copy list to allow removal
        try:
            data = client.recv(4096)
            if data:
                print(f"Received: {data.decode()}")
                client.sendall(data)
            else:
                clients.remove(client)
                client.close()
        except BlockingIOError:
            pass  # No data available yet
        except (ConnectionResetError, BrokenPipeError):
            clients.remove(client)
            client.close()

    time.sleep(0.01)  # Small sleep to prevent CPU spinning
```

The busy-loop above is inefficient. That is where select/poll/epoll come in.

---

## select() -- I/O Multiplexing

`select()` monitors multiple sockets and tells you which ones are ready for I/O.

```python
#!/usr/bin/env python3
"""TCP server using select() for I/O multiplexing."""

import socket
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 8080))
server.listen(100)
server.setblocking(False)

# Lists for select()
inputs = [server]   # Sockets to monitor for readability
outputs = []        # Sockets to monitor for writability

print("Select-based server on port 8080...")

while inputs:
    # Wait until at least one socket is ready
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    for sock in readable:
        if sock is server:
            # New incoming connection
            client, addr = sock.accept()
            client.setblocking(False)
            inputs.append(client)
            print(f"New connection from {addr}")
        else:
            # Data from an existing client
            data = sock.recv(4096)
            if data:
                print(f"Received: {data.decode()}")
                sock.sendall(data)  # Echo back
            else:
                # Client disconnected
                print("Client disconnected")
                inputs.remove(sock)
                sock.close()

    for sock in exceptional:
        print("Socket exception")
        inputs.remove(sock)
        sock.close()
```

---

## select vs poll vs epoll

| Feature | select | poll | epoll |
|---------|--------|------|-------|
| Max FDs | 1024 (FD_SETSIZE) | Unlimited | Unlimited |
| Scaling | O(n) per call | O(n) per call | O(1) per event |
| Copies FD set | Every call | Every call | Once (kernel) |
| Platform | All POSIX + Windows | POSIX | Linux only |
| Best for | Small number of FDs | Moderate FDs | Large scale servers |

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="340" font-family="sans-serif">
<defs>
  <marker id="arr"  markerWidth="10" markerHeight="7" refX="9"   refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#555"/>
  </marker>
  <marker id="arrl" markerWidth="10" markerHeight="7" refX="1"   refY="3.5" orient="auto">
    <polygon points="10 0,0 3.5,10 7" fill="#555"/>
  </marker>
</defs>
<text x="340" y="22" text-anchor="middle" font-size="14" fill="#222222" font-weight="bold">I/O Multiplexing: select / poll / epoll</text>
<rect x="10" y="40" width="660" height="76" fill="#fff3e0" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="85" y="62" text-anchor="middle" font-size="13" fill="#1a1a2e" font-weight="bold">select()</text>
<line x1="160" y1="44" x2="160" y2="112" stroke="#aaa" stroke-width="1"/>
<text x="170" y="62" text-anchor="start" font-size="12" fill="#222222">Pass ALL fds every time → kernel scans all → returns ready ones</text>
<text x="170" y="80" text-anchor="start" font-size="11" fill="#555">Works on ~1024 fds max. O(n) scan per call.</text>
<rect x="10" y="120" width="660" height="76" fill="#f3e5f5" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="85" y="142" text-anchor="middle" font-size="13" fill="#1a1a2e" font-weight="bold">poll()</text>
<line x1="160" y1="124" x2="160" y2="192" stroke="#aaa" stroke-width="1"/>
<text x="170" y="142" text-anchor="start" font-size="12" fill="#222222">Similar to select() but no fd limit.</text>
<text x="170" y="160" text-anchor="start" font-size="11" fill="#555">Still O(n) — kernel scans the whole list each call.</text>
<rect x="10" y="200" width="660" height="76" fill="#e8f5e9" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="85" y="222" text-anchor="middle" font-size="13" fill="#1a1a2e" font-weight="bold">epoll()</text>
<line x1="160" y1="204" x2="160" y2="272" stroke="#aaa" stroke-width="1"/>
<text x="170" y="222" text-anchor="start" font-size="12" fill="#222222">Register fds once; kernel notifies only about ready fds.</text>
<text x="170" y="240" text-anchor="start" font-size="11" fill="#555">O(1) for returning events. Scales to millions of connections.</text>
<rect x="80" y="290" width="520" height="70" fill="#c8e6c9" stroke="#388e3c" stroke-width="1.5" rx="4"/>
<text x="340" y="312" text-anchor="middle" font-size="12" fill="#1b5e20" font-weight="bold">Kernel (epoll): monitors registered fds efficiently</text>
<text x="340" y="334" text-anchor="middle" font-size="11" fill="#2e7d32">Notifies userspace only about fds with actual events</text>
</svg>

---

## epoll Example

```python
#!/usr/bin/env python3
"""TCP server using epoll (Linux only)."""

import socket
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 8080))
server.listen(100)
server.setblocking(False)

# Create epoll instance
epoll = select.epoll()

# Register server socket for read events
epoll.register(server.fileno(), select.EPOLLIN)

# Map file descriptors to socket objects
fd_to_socket = {server.fileno(): server}

print("Epoll-based server on port 8080...")

try:
    while True:
        # Wait for events (timeout = 1 second)
        events = epoll.poll(1)

        for fd, event in events:
            sock = fd_to_socket[fd]

            if sock is server:
                # New connection
                client, addr = server.accept()
                client.setblocking(False)
                epoll.register(client.fileno(), select.EPOLLIN)
                fd_to_socket[client.fileno()] = client
                print(f"New connection from {addr}")

            elif event & select.EPOLLIN:
                # Data available to read
                data = sock.recv(4096)
                if data:
                    sock.sendall(data)
                else:
                    # Client disconnected
                    epoll.unregister(fd)
                    del fd_to_socket[fd]
                    sock.close()

            elif event & select.EPOLLHUP:
                # Hang up
                epoll.unregister(fd)
                del fd_to_socket[fd]
                sock.close()
finally:
    epoll.unregister(server.fileno())
    epoll.close()
    server.close()
```

---

## Python asyncio: Modern Async Sockets

Python's `asyncio` wraps epoll/kqueue with a clean async/await interface.

```python
#!/usr/bin/env python3
"""TCP echo server using asyncio."""

import asyncio

async def handle_client(reader, writer):
    """Handle a single client connection."""
    addr = writer.get_extra_info('peername')
    print(f"New connection from {addr}")

    try:
        while True:
            data = await reader.read(4096)
            if not data:
                break

            message = data.decode()
            print(f"[{addr}] {message}")

            writer.write(data)
            await writer.drain()
    except ConnectionResetError:
        pass
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"Connection from {addr} closed")

async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 8080)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
```

This handles thousands of concurrent connections on a single thread using the event loop.

---

## A Simple HTTP Server from Scratch

Understanding sockets by building a minimal HTTP server:

```python
#!/usr/bin/env python3
"""Minimal HTTP server using raw sockets."""

import socket
import datetime

def handle_request(client_socket):
    """Parse HTTP request and send response."""
    request = client_socket.recv(4096).decode()
    if not request:
        return

    # Parse the request line
    lines = request.split('\r\n')
    method, path, version = lines[0].split(' ')
    print(f"{method} {path} {version}")

    # Build response
    if path == '/':
        body = "<html><body><h1>Hello from raw sockets!</h1></body></html>"
        status = "200 OK"
    elif path == '/time':
        body = f"<html><body><p>{datetime.datetime.now()}</p></body></html>"
        status = "200 OK"
    else:
        body = "<html><body><h1>404 Not Found</h1></body></html>"
        status = "404 Not Found"

    response = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: text/html\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
        f"{body}"
    )

    client_socket.sendall(response.encode())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 8080))
server.listen(5)
print("HTTP server on http://localhost:8080")

while True:
    client, addr = server.accept()
    handle_request(client)
    client.close()
```

---

## Practical Tool: netcat (nc)

`netcat` is the "Swiss army knife" of networking -- reads and writes data across network connections.

```bash
# TCP listener (simple server)
$ nc -l -p 8080
# Type messages, they're sent to the connected client

# TCP client
$ nc localhost 8080
# Type messages, they're sent to the server

# Send a file over the network
# Receiver:
$ nc -l -p 9090 > received_file.txt
# Sender:
$ nc localhost 9090 < file_to_send.txt

# Simple HTTP request
$ echo -e "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n" | nc example.com 80

# Port scanning
$ nc -zv localhost 20-100
localhost [127.0.0.1] 80 (http) open
localhost [127.0.0.1] 22 (ssh) open

# UDP mode
$ nc -u -l -p 9090          # UDP listener
$ nc -u localhost 9090       # UDP client

# Chat between two machines
# Machine A:
$ nc -l -p 5000
# Machine B:
$ nc machine-a-ip 5000
# Both can type messages back and forth
```

---

## Practical Tool: telnet

`telnet` is useful for testing text-based protocols interactively.

```bash
# Test HTTP server
$ telnet example.com 80
Trying 93.184.216.34...
Connected to example.com.
GET / HTTP/1.1
Host: example.com

HTTP/1.1 200 OK
Content-Type: text/html
...

# Test SMTP server
$ telnet mail.example.com 25
220 mail.example.com ESMTP
HELO test.com
250 Hello
MAIL FROM:<test@test.com>
250 Ok
QUIT

# Test if a port is open
$ telnet database-server 5432
Trying 10.0.0.50...
Connected to database-server.
# Port is open! (Ctrl+] then quit to exit)

$ telnet database-server 5433
Trying 10.0.0.50...
telnet: Unable to connect to remote host: Connection refused
# Port is closed or service is not running
```

---

## Practical Tool: ss (Socket Statistics)

`ss` is the modern replacement for `netstat` -- faster and more informative.

```bash
# Show all TCP listening sockets
$ ss -tlnp
State    Recv-Q  Send-Q  Local Address:Port   Peer Address:Port  Process
LISTEN   0       128     0.0.0.0:22           0.0.0.0:*          users:(("sshd",pid=1234))
LISTEN   0       511     0.0.0.0:80           0.0.0.0:*          users:(("nginx",pid=5678))
LISTEN   0       100     127.0.0.1:5432       0.0.0.0:*          users:(("postgres",pid=9012))

# Show all established connections
$ ss -tnp
State    Recv-Q  Send-Q  Local Address:Port   Peer Address:Port  Process
ESTAB    0       0       10.0.0.5:22          203.0.113.50:54321  users:(("sshd",pid=2345))

# Show socket summary
$ ss -s
Total: 156
TCP:   12 (estab 4, closed 2, orphaned 0, timewait 2)
UDP:   6

# Filter by state
$ ss -t state established
$ ss -t state time-wait
$ ss -t state close-wait

# Filter by port
$ ss -tn sport = :443
$ ss -tn dport = :8080

# Show timer information
$ ss -tnpo

# Show UDP sockets
$ ss -ulnp

# Show all Unix domain sockets
$ ss -xlnp
```

---

## ss Flags Reference

| Flag | Meaning |
|------|---------|
| -t | TCP sockets |
| -u | UDP sockets |
| -l | Listening sockets only |
| -n | Numeric (don't resolve names) |
| -p | Show process info |
| -a | All sockets (listening + non-listening) |
| -o | Show timer information |
| -e | Show extended info |
| -s | Summary statistics |
| -4 | IPv4 only |
| -6 | IPv6 only |

```bash
# Common combinations
$ ss -tlnp    # What's listening? (TCP)
$ ss -ulnp    # What's listening? (UDP)
$ ss -tnp     # Active TCP connections
$ ss -s       # Quick summary

# Legacy netstat equivalents
$ netstat -tlnp    →    ss -tlnp
$ netstat -an      →    ss -an
$ netstat -s       →    ss -s
```

---

## Socket Address Families

```python
import socket

# IPv4
sock4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock4.bind(('0.0.0.0', 8080))  # (host, port)

# IPv6
sock6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
sock6.bind(('::', 8080))  # (host, port, flowinfo, scopeid)

# Unix domain socket (local IPC, no network)
sock_unix = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock_unix.bind('/tmp/my_socket.sock')

# Dual-stack (IPv4 + IPv6 on same socket)
sock_dual = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
sock_dual.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
sock_dual.bind(('::', 8080))
# This accepts both IPv4 and IPv6 connections
```

| Family | Description | Address Format |
|--------|-------------|---------------|
| AF_INET | IPv4 | ('host', port) |
| AF_INET6 | IPv6 | ('host', port, flowinfo, scopeid) |
| AF_UNIX | Local (Unix socket) | '/path/to/socket' |

---

## Handling Partial Sends and Receives

TCP is a byte stream -- `recv()` may return fewer bytes than requested, and `send()` may not send everything.

```python
def recv_exact(sock, num_bytes):
    """Receive exactly num_bytes from socket."""
    data = b''
    while len(data) < num_bytes:
        chunk = sock.recv(num_bytes - len(data))
        if not chunk:
            raise ConnectionError("Connection closed before all data received")
        data += chunk
    return data

def send_message(sock, message):
    """Send a length-prefixed message."""
    encoded = message.encode()
    # Send 4-byte length header, then the data
    length = len(encoded)
    sock.sendall(length.to_bytes(4, byteorder='big'))
    sock.sendall(encoded)

def recv_message(sock):
    """Receive a length-prefixed message."""
    # Read 4-byte length header
    length_bytes = recv_exact(sock, 4)
    length = int.from_bytes(length_bytes, byteorder='big')

    # Read exactly that many bytes of data
    data = recv_exact(sock, length)
    return data.decode()
```

This "length-prefix" pattern is fundamental to many network protocols.

---

## A Complete Chat Application

```python
#!/usr/bin/env python3
"""Simple TCP chat server."""

import socket
import threading
import sys

clients = {}  # socket -> nickname

def broadcast(message, sender=None):
    """Send message to all connected clients except sender."""
    for client_socket in list(clients.keys()):
        if client_socket != sender:
            try:
                client_socket.sendall(message.encode())
            except (BrokenPipeError, ConnectionResetError):
                remove_client(client_socket)

def remove_client(client_socket):
    """Remove a disconnected client."""
    if client_socket in clients:
        nickname = clients.pop(client_socket)
        client_socket.close()
        broadcast(f"*** {nickname} has left the chat ***\n")

def handle_client(client_socket, addr):
    """Handle messages from a single client."""
    client_socket.sendall(b"Enter your nickname: ")
    nickname = client_socket.recv(1024).decode().strip()
    clients[client_socket] = nickname

    broadcast(f"*** {nickname} has joined the chat ***\n", client_socket)
    client_socket.sendall(f"Welcome, {nickname}!\n".encode())

    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            message = f"[{nickname}] {data.decode()}"
            broadcast(message, client_socket)
    except (ConnectionResetError, BrokenPipeError):
        pass
    finally:
        remove_client(client_socket)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5000))
    server.listen(50)
    print("Chat server running on port 5000")

    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client, addr),
                         daemon=True).start()

if __name__ == '__main__':
    main()
```

```bash
# Connect multiple clients with netcat:
$ nc localhost 5000
Enter your nickname: Alice
Welcome, Alice!
[Bob] Hi everyone!
```

---

## Raw Sockets: ICMP Ping

Raw sockets allow constructing packets at a low level (requires root privileges).

```python
#!/usr/bin/env python3
"""Simple ICMP ping using raw sockets (requires root)."""

import socket
import struct
import time
import os

def checksum(data):
    """Calculate ICMP checksum."""
    if len(data) % 2:
        data += b'\x00'
    s = sum(struct.unpack('!%dH' % (len(data) // 2), data))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    return ~s & 0xffff

def ping(host, count=4):
    """Send ICMP echo requests."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    sock.settimeout(2)

    dest = socket.gethostbyname(host)
    pid = os.getpid() & 0xFFFF
    print(f"PING {host} ({dest})")

    for seq in range(count):
        # Build ICMP echo request
        # Type=8, Code=0, Checksum=0 (placeholder), ID, Sequence
        header = struct.pack('!BBHHH', 8, 0, 0, pid, seq)
        payload = struct.pack('!d', time.time())
        chksum = checksum(header + payload)
        header = struct.pack('!BBHHH', 8, 0, chksum, pid, seq)

        sock.sendto(header + payload, (dest, 0))
        start = time.time()

        try:
            data, addr = sock.recvfrom(1024)
            elapsed = (time.time() - start) * 1000
            print(f"Reply from {addr[0]}: seq={seq} time={elapsed:.1f}ms")
        except socket.timeout:
            print(f"Request timed out: seq={seq}")

        time.sleep(1)

    sock.close()

if __name__ == '__main__':
    import sys
    ping(sys.argv[1] if len(sys.argv) > 1 else '8.8.8.8')
```

---

## Socket Programming: Error Handling

Robust network code must handle many failure modes:

```python
import socket
import errno

def robust_connect(host, port, timeout=10):
    """Connect with proper error handling."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        return sock

    except socket.gaierror as e:
        print(f"DNS resolution failed for {host}: {e}")
    except socket.timeout:
        print(f"Connection to {host}:{port} timed out")
    except ConnectionRefusedError:
        print(f"Connection refused by {host}:{port} (port closed or no listener)")
    except ConnectionResetError:
        print(f"Connection reset by {host}:{port}")
    except PermissionError:
        print(f"Permission denied connecting to {host}:{port}")
    except OSError as e:
        if e.errno == errno.ENETUNREACH:
            print(f"Network unreachable: {host}")
        elif e.errno == errno.EHOSTUNREACH:
            print(f"Host unreachable: {host}")
        else:
            print(f"OS error: {e}")

    return None
```

**Common socket errors:**
| Error | Meaning |
|-------|---------|
| ECONNREFUSED | No process listening on port |
| ETIMEDOUT | Connection attempt timed out |
| ECONNRESET | Connection forcefully closed by peer |
| EPIPE / BrokenPipeError | Write to closed connection |
| EADDRINUSE | Port already in use (missing SO_REUSEADDR) |
| ENETUNREACH | No route to network |

---

## Debugging with strace

Trace system calls to see exactly what your socket program does:

```bash
# Trace all network-related syscalls
$ strace -e trace=network python3 tcp_client.py
socket(AF_INET, SOCK_STREAM, IPPROTO_IP) = 3
connect(3, {sa_family=AF_INET, sin_port=htons(8080),
        sin_addr=inet_addr("127.0.0.1")}, 16) = 0
sendto(3, "Hello, Server!", 14, 0, NULL, 0) = 14
recvfrom(3, "Hello, Server!", 4096, 0, NULL, NULL) = 14
close(3)                                = 0

# Trace with timestamps
$ strace -e trace=network -T python3 tcp_client.py
connect(...) = 0 <0.000234>    # connect took 234 microseconds
sendto(...)  = 14 <0.000045>   # send took 45 microseconds
recvfrom(...) = 14 <0.012345>  # recv took 12ms (waiting for response)

# Trace a running process
$ sudo strace -e trace=network -p $(pgrep nginx)
```

---

## Review: Socket Programming Key Concepts

- Sockets provide the fundamental API for network communication
- **TCP** (SOCK_STREAM): connection-oriented, reliable, ordered byte stream
- **UDP** (SOCK_DGRAM): connectionless, fast, message-oriented
- Key socket calls: `socket()`, `bind()`, `listen()`, `accept()`, `connect()`, `send()`, `recv()`
- **SO_REUSEADDR** and **TCP_NODELAY** are the most important socket options
- I/O multiplexing: `select()` for small scale, `epoll()` for large scale
- **asyncio** provides a modern Python interface over epoll/kqueue
- TCP is a byte stream -- use length-prefix framing for message boundaries
- Tools: `netcat`, `telnet`, `ss` (replaces netstat), `strace`
- Always handle partial reads/writes and connection errors
