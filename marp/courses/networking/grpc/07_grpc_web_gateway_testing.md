---
tags:
  - networking:grpc
  - concepts:web
  - concepts:testing
level: intermediate
category: networking
audience:
  - audiences:developers

---
# gRPC-Web, Gateway, Testing, Performance

---
## What This Chapter Covers

- gRPC-Web: bringing gRPC to browsers
- gRPC-Gateway: REST/JSON in front of gRPC
- Testing: unit, integration, mocking
- Performance: benchmarking and tuning
- Optimizing protobuf and connections

---
## The Browser Problem

- Browsers don't expose HTTP/2 frames directly
- Trailers and other gRPC features unsupported
- A direct gRPC call from JavaScript fails
- Solution: gRPC-Web, a related but distinct protocol
- Requires a proxy in the middle

---
## gRPC-Web Architecture

![grpc_web](svg/courses/networking/grpc/07_grpc_web_gateway_testing/grpc_web.svg)

---
## gRPC-Web Protocol

- HTTP/1.1 or HTTP/2 between browser and proxy
- Different framing — headers as metadata in body
- Translates to native gRPC behind the proxy
- Standard fetch API on the client side
- Slightly different feature set

---
## gRPC-Web Limitations

- No client-side streaming (yet, in some impls)
- No bidirectional streaming
- Server-streaming works
- Unary works perfectly
- Most apps fit within these limits

---
## Setting Up gRPC-Web

- Run Envoy or a similar proxy
- Configure it to translate gRPC-Web to gRPC
- Generate JS or TS clients via `protoc-gen-grpc-web`
- Same .proto, different codegen
- Browser code looks like normal JS

---
## What Is gRPC-Gateway?

- Generates a REST/JSON proxy from .proto files
- Annotate methods with HTTP bindings
- The proxy translates HTTP+JSON to gRPC
- Best of both: REST for browsers, gRPC for services
- One backend serves both

---
## Annotating .proto for Gateway

```protobuf
import "google/api/annotations.proto";

service Greeter {
    rpc SayHello(HelloRequest) returns (HelloReply) {
        option (google.api.http) = {
            get: "/v1/hello/{name}"
        };
    }
}
```

- HTTP method, path, and field mapping
- Path variables come from message fields
- POST/PUT use body mapping

---
## Generating the Gateway

- `protoc-gen-grpc-gateway` plugin
- Produces a reverse-proxy in Go
- Run alongside the gRPC server
- One backend, two protocols
- OpenAPI specs can also be generated

---
## When to Use Gateway

- You need REST for browsers and gRPC for services
- Single source of truth for the API surface
- Public API that should look REST-y
- Backwards compatibility for HTTP/JSON clients
- Lightweight overhead per call

---
## Connect: An Alternative

- Connect protocol (Buf) is gRPC-compatible
- Works in browsers without a proxy
- Simpler than gRPC-Web
- Servers speak gRPC, gRPC-Web, and Connect
- Worth evaluating for new projects

---
## Testing: Unit Tests

- Unit-test handlers as pure functions
- Mock the dependencies (DB, downstream)
- Use the generated request/response types
- Same approach as any service test
- Fast feedback for developers

---
## Testing: Integration Tests

- Use `grpc.NewServer` in-process
- Spin up real services on bufconn
- Real serialization, real interceptors
- No network — just memory bufconn
- Catches wiring bugs unit tests miss

---
## Bufconn Pattern (Go)

```go
listener := bufconn.Listen(1024 * 1024)
server := grpc.NewServer()
pb.RegisterGreeterServer(server, &myServer{})
go server.Serve(listener)

conn, _ := grpc.Dial("",
    grpc.WithContextDialer(func(_ context.Context, _ string) (net.Conn, error) {
        return listener.Dial()
    }))
client := pb.NewGreeterClient(conn)
```

---
## Mocking Clients

- Generate mock client code
- Most languages have helper libraries (mockgen)
- Stub specific responses for specific calls
- Useful when testing one service without a dependency
- Don't over-mock — integration tests catch what mocks don't

---
## Contract Testing

- Producer and consumer share the .proto
- Compatibility checks in CI
- Buf's `buf breaking` detects breaking changes
- Pact and similar for behavior contracts
- Catches schema regressions before merge

---
## Performance: Where Time Goes

- Serialization (proto encode/decode)
- Network (TCP, TLS)
- HTTP/2 framing
- Application logic
- Profile to find the bottleneck

---
## Benchmarking gRPC

- `ghz` is the standard load tester
- Configurable concurrency, duration, payload
- Outputs latency percentiles, throughput
- Compare changes across deploys
- Run benchmarks before optimizing

---
## Optimizing Payload Size

- Use scalar types matching actual range
- Avoid string-encoded numbers
- Use `bytes` for binary data
- Skip optional fields when default
- Compress at the gRPC layer if needed

---
## Connection Pooling

- One gRPC connection multiplexes many calls
- Don't open a new connection per call
- Connection pools usually unnecessary
- One channel per service is the default
- Profile if in doubt

---
## Streaming Performance

- Server streaming amortizes connection overhead
- Bidi streaming for high-throughput chat-style flows
- Avoid creating one stream per message
- Window size affects throughput
- Profile under realistic load

---
## Compression

- gzip support built in
- Trade CPU for bandwidth
- Useful on slow links
- Diminishing returns for small messages
- Configurable per-call

---
## Memory Considerations

- Large messages allocate per call
- Avoid sending huge messages — chunk via streaming
- Pool buffers in performance-critical code
- Watch GC pressure (Go) or allocator (C++)
- Profile before micro-optimizing

---
## CPU Considerations

- Protobuf encode/decode dominates for small calls
- TLS handshake dominates for short-lived calls
- Reuse connections to amortize TLS
- Pin to fewer threads for cache-friendliness
- Standard concurrency tuning applies

---
## Common Pitfalls

- One connection per call — defeats HTTP/2
- Huge messages instead of streams
- No keepalive — dead connections appear alive
- Skipping benchmarks; trusting intuition
- Premature optimization at the protobuf level

---
## Course Recap

- Fundamentals of gRPC and HTTP/2
- Protocol Buffers
- The four RPC types
- Metadata, errors, deadlines
- Interceptors and security
- Load balancing and health
- gRPC-Web, Gateway, testing, performance

---
## Final Thoughts

- gRPC shines in internal microservices
- Pair with REST for public surfaces via Gateway
- Schema discipline pays off long-term
- Streaming earns its complexity for real workloads
- Profile, then optimize — not the other way around

---
## Summary

- gRPC-Web brings gRPC to browsers via a proxy
- Gateway gives you REST/JSON for free from your .proto
- Test at multiple levels: unit, integration, contract
- Benchmark with realistic loads; optimize what matters
- The ecosystem is mature — pick the right pieces
