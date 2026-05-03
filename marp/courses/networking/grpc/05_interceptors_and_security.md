---
tags:
  - networking:grpc
  - concepts:middleware
  - security:tls
level: intermediate
category: networking
audience:
  - audiences:developers

---
# Interceptors and Security

---
## What This Chapter Covers

- Interceptors: client and server, unary and streaming
- Common uses: logging, metrics, auth
- Chaining and ordering
- TLS for transport security
- mTLS, JWT, OAuth2 integration

---
## What Is an Interceptor?

- Middleware for gRPC calls
- Wraps the actual handler
- Sees request, response, errors, metadata
- Can short-circuit, transform, or just observe
- Equivalent to HTTP middleware in REST frameworks

---
## Common Interceptor Chain

![interceptor_chain](svg/courses/networking/grpc/05_interceptors_and_security/interceptor_chain.svg)

---
## Interceptor Use Cases

![interceptor_uses](svg/courses/networking/grpc/05_interceptors_and_security/interceptor_uses.svg)

---
## Authentication Layers

![auth_layers](svg/courses/networking/grpc/05_interceptors_and_security/auth_layers.svg)

---
## Why Interceptors?

- Cross-cutting concerns: logging, tracing, auth
- Implement once; apply to all RPCs
- Composable — chain multiple
- Both client side and server side
- The standard way to extend gRPC behavior

---
## Server Interceptor (Unary, Go)

```go
func loggingInterceptor(
    ctx context.Context,
    req interface{},
    info *grpc.UnaryServerInfo,
    handler grpc.UnaryHandler,
) (interface{}, error) {
    log.Printf("--> %s", info.FullMethod)
    resp, err := handler(ctx, req)
    log.Printf("<-- %s err=%v", info.FullMethod, err)
    return resp, err
}
```

- Wraps the handler
- Pre and post hooks
- Returns or transforms the response

---
## Server Streaming Interceptor

- Similar shape, but wraps a stream
- Need to wrap the stream object too — for in-flight observation
- Common pattern: `WrappedServerStream`
- More involved than unary
- Same purpose: cross-cutting logic

---
## Client Interceptor

- Wraps outgoing calls
- Same opportunities: logging, retries, metrics
- Used in client SDKs to bake in patterns
- Symmetric to server interceptors
- Both unary and streaming variants

---
## Common Server Interceptors

- Logging — request/response, latency
- Metrics — Prometheus counters and histograms
- Tracing — OpenTelemetry spans
- Authentication — verify tokens
- Rate limiting — protect endpoints
- Recovery — convert panics to gRPC errors

---
## Common Client Interceptors

- Auth token attachment
- Retry with backoff
- Circuit breaker
- Tracing context propagation
- Request ID generation

---
## Chaining Interceptors

```go
server := grpc.NewServer(
    grpc.ChainUnaryInterceptor(
        loggingInterceptor,
        metricsInterceptor,
        authInterceptor,
    ),
)
```

- Order matters
- Logging on the outside catches everything
- Auth before business logic
- Each library has a chain helper

---
## Auth Interceptor Example

```go
func authInterceptor(ctx context.Context, req interface{},
    info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {

    md, _ := metadata.FromIncomingContext(ctx)
    tokens := md.Get("authorization")
    if len(tokens) == 0 {
        return nil, status.Error(codes.Unauthenticated, "missing token")
    }
    if !valid(tokens[0]) {
        return nil, status.Error(codes.Unauthenticated, "bad token")
    }
    return handler(ctx, req)
}
```

---
## Why TLS for gRPC?

- gRPC defaults to plaintext only on localhost
- Production should always use TLS
- HTTP/2 expects TLS in most ecosystems
- Encrypts transport, authenticates server
- Without TLS, anyone can read or modify traffic

---
## TLS Setup (Server)

```go
creds, err := credentials.NewServerTLSFromFile("server.crt", "server.key")
if err != nil { log.Fatal(err) }

server := grpc.NewServer(grpc.Creds(creds))
```

- Load cert and key
- Pass as server option
- Clients must trust the cert (or use mTLS)

---
## TLS Setup (Client)

```go
creds, err := credentials.NewClientTLSFromFile("ca.crt", "")
if err != nil { log.Fatal(err) }

conn, err := grpc.Dial(addr, grpc.WithTransportCredentials(creds))
```

- Trust the server's CA
- Dial with credentials
- Public CAs work for hosted services

---
## Mutual TLS (mTLS)

- Both client and server present certs
- Server verifies client identity, not just vice versa
- Strong service-to-service authentication
- Each service has its own cert
- Common in service meshes

---
## mTLS Setup

```go
cert, _ := tls.LoadX509KeyPair("client.crt", "client.key")
caCert, _ := os.ReadFile("ca.crt")
caPool := x509.NewCertPool()
caPool.AppendCertsFromPEM(caCert)

creds := credentials.NewTLS(&tls.Config{
    Certificates: []tls.Certificate{cert},
    RootCAs:      caPool,
})
```

---
## Token-Based Authentication

- JWT tokens in `authorization` metadata
- Server validates signature and claims
- Combine with TLS for transport security
- Mature pattern; lots of library support
- Per-call rather than per-connection

---
## Per-RPC Credentials

- Library construct: attach creds per call
- Useful when one connection serves many users
- Token scoped to the user, not the connection
- Combine with mTLS at the connection layer
- Layered security model

---
## OAuth2 Integration

- Tokens minted by an OAuth2 IdP
- Refreshed by a client library
- Attached automatically via interceptor
- Validated by an interceptor or shared library
- Standard for user-facing systems

---
## Channel Credentials vs Call Credentials

- Channel: per-connection (TLS, mTLS)
- Call: per-RPC (tokens)
- Combine both for layered security
- Channel credentials are typically static
- Call credentials are typically per-user

---
## Authorization vs Authentication

- Authentication: "who are you?"
- Authorization: "what can you do?"
- gRPC interceptors handle the first naturally
- Authorization usually goes in business logic or its own interceptor
- Don't conflate the two

---
## Security Anti-Patterns

- Plaintext gRPC in production
- Tokens in proto fields instead of metadata
- One mTLS cert shared across all services
- Forever-tokens with no expiration
- Auth interceptor that ignores some methods

---
## Defense in Depth

- TLS everywhere
- mTLS for service-to-service
- Token-based for user identity
- Authorization at multiple layers
- Audit logs for everything

---
## Summary

- Interceptors are the gRPC middleware mechanism
- Logging, metrics, tracing, auth all fit naturally
- TLS in production is non-negotiable
- mTLS for strong service identity
- Combine channel and call credentials for layered security
