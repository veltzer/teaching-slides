---
tags:
  - networking:grpc
  - concepts:rpc
level: intermediate
category: networking
audience:
  - audiences:developers

---
# gRPC Fundamentals

---
## What This Chapter Covers

- What gRPC is and what problem it solves
- The role of HTTP/2 and Protocol Buffers
- Architecture and communication model
- gRPC vs REST vs GraphQL
- Supported languages and the ecosystem

---
## What Is gRPC?

- A high-performance, open-source RPC framework
- Originally built at Google; donated to CNCF
- Built on HTTP/2 for transport
- Uses Protocol Buffers as the default serialization format
- Cross-language: clients and servers in different languages interoperate

---
## Why gRPC?

- Type-safe contracts via .proto files
- Compact binary serialization
- HTTP/2 multiplexing — many calls share one connection
- Native streaming support
- First-class support for many languages

---
## HTTP/2: The Transport

- Binary framing instead of plain-text HTTP/1
- Header compression (HPACK)
- Multiplexing — multiple streams per connection
- Server push (rarely used by gRPC)
- Long-lived connections — better latency

---
## Why HTTP/2 Matters Here

- Multiplexing eliminates head-of-line blocking
- One TCP connection serves many concurrent calls
- Header compression cuts overhead for repeated calls
- Streaming requests/responses are first-class
- The basis of gRPC's performance claims

---
## Protocol Buffers: The Schema

- Strongly-typed schema language
- Compact binary on the wire
- Backward and forward compatibility built in
- Codegen for many languages
- Schema is the contract, shared between client and server

---
## Architecture Overview

![grpc_architecture](svg/courses/networking/grpc/01_grpc_fundamentals/grpc_architecture.svg)

---
## Communication Model

- Client invokes a method on a stub (generated)
- Stub serializes args, sends over HTTP/2
- Server deserializes, calls the implementation
- Server serializes response, sends back
- Client receives, deserializes, returns

---
## Stubs and Generated Code

- The .proto file defines the service
- `protoc` generates client stubs and server interfaces
- Client code calls methods like local functions
- Server code implements an interface
- Wire details are abstracted

---
## gRPC vs REST

- REST: HTTP/1, JSON, resource-oriented
- gRPC: HTTP/2, binary, action-oriented
- REST: easy to debug with curl
- gRPC: faster, smaller, type-safe
- REST: better for public APIs
- gRPC: better for internal microservices

---
## gRPC vs GraphQL

- GraphQL: query language, flexible response shape
- gRPC: predefined RPCs, strict shape
- GraphQL: one endpoint, many shapes
- gRPC: many endpoints, one shape per RPC
- Different tools for different problems

---
## When to Use gRPC

- Microservices communicating internally
- High-throughput, low-latency requirements
- Polyglot environments needing strong contracts
- Streaming use cases (chat, telemetry, file transfer)
- Mobile clients where bandwidth matters

---
## When Not to Use gRPC

- Browser-direct calls (need gRPC-Web proxy)
- Quick prototyping where REST is faster to set up
- Public APIs where third parties prefer REST
- Teams without protobuf tooling experience
- Cases where text-readable wire format matters for debugging

---
## Language Support

- First-class: Go, Java, Python, C++, C#, Node, Ruby, Dart
- Strong community: Rust, Kotlin, Swift, PHP
- Each has its own client and server implementation
- Code-generation patterns vary slightly per language
- Not all languages have all features

---
## Ecosystem and Tooling

- `grpcurl` — like curl for gRPC
- Evans — interactive REPL
- BloomRPC — desktop GUI
- Buf — modern protobuf toolchain
- Connect — gRPC-compatible alternative with browser support

---
## Performance Claims

- 5-10x faster than equivalent JSON over HTTP/1 in many benchmarks
- Smaller payload — protobuf is binary
- Lower CPU for serialization than JSON
- HTTP/2 reduces connection overhead
- Real numbers vary by use case — always benchmark

---
## Course Roadmap

- Chapter 2: Protocol Buffers syntax
- Chapter 3: The four RPC types
- Chapter 4: Streaming patterns
- Chapter 5: Metadata, errors, deadlines
- Chapter 6: Interceptors
- Chapter 7: Authentication and security
- Chapter 8: Load balancing and health
- Chapter 9: gRPC-Web and Gateway
- Chapter 10: Testing and performance

---
## Setting Up: A Simple Workflow

- Define service in .proto
- Run `protoc` to generate client and server code
- Implement the server interface
- Wire client code to call methods
- Run, test, iterate

---
## Example: Hello World

```protobuf
service Greeter {
    rpc SayHello (HelloRequest) returns (HelloReply);
}
message HelloRequest {
    string name = 1;
}
message HelloReply {
    string message = 1;
}
```

- One service, one RPC, two messages
- Numbered fields for serialization
- Generated code in client and server languages

---
## Common Misconceptions

- "gRPC is just RPC over HTTP" — it's tightly tied to HTTP/2 and protobuf
- "gRPC replaces REST entirely" — they coexist; pick per use case
- "Protobuf is just JSON's binary cousin" — much stricter, schema-driven
- "gRPC is always faster" — protocol overhead is small; bottleneck often elsewhere
- "Streaming means async" — gRPC streaming is its own thing

---
## Summary

- gRPC: HTTP/2 + Protocol Buffers + cross-language codegen
- Strong typing, streaming, multiplexing, performance
- Better for internal microservices than for public APIs
- Ecosystem mature; tooling improves yearly
- The rest of the course goes deep on each piece
