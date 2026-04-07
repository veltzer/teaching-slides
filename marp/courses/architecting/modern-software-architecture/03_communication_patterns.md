# Communication Patterns


---
## Why Communication Patterns Matter

- Microservices must communicate across process and network boundaries
- The choice of communication pattern affects coupling, performance, and resilience
- Wrong patterns lead to brittle, slow, or hard-to-debug systems
- Architects must select patterns that match each interaction's requirements

---
## Synchronous Communication

- The caller sends a request and waits for a response
- Simple request-response model familiar to most developers
- Examples: `HTTP REST`, `gRPC`, `GraphQL`
- Creates temporal coupling between caller and callee

---
## Synchronous Communication Diagram

![synchronous_communication_diagram](/mermaid/courses/architecting/modern-software-architecture/03_communication_patterns/synchronous_communication_diagram.mmd)

---
## Asynchronous Communication

- The caller sends a message and does not wait for an immediate response
- Decouples the sender from the receiver in time
- Examples: message queues, event streams, pub/sub
- Enables better resilience and scalability

---
## Asynchronous Communication Diagram

![asynchronous_communication_diagram](/mermaid/courses/architecting/modern-software-architecture/03_communication_patterns/asynchronous_communication_diagram.mmd)

---
## Sync vs Async Comparison

| Aspect | Synchronous | Asynchronous |
|--------|------------|--------------|
| Coupling | Temporal | Decoupled |
| Latency | Caller waits | Fire and forget |
| Complexity | Simpler to reason about | Requires message infrastructure |
| Error handling | Immediate feedback | Delayed, needs dead-letter queues |
| Scalability | Limited by slowest service | Buffer absorbs spikes |

---
## When to Use Synchronous

- User-facing requests that need immediate responses
- Simple query operations with low latency requirements
- Interactions where the caller needs the result to proceed
- Scenarios where failure should be immediately visible

---
## When to Use Asynchronous

- Long-running operations that should not block the caller
- Event notifications where the producer does not need a response
- Workloads with high throughput and variable processing times
- Cross-service communication where resilience matters most

---
## RESTful API Design

- `REST` stands for `Representational State Transfer`
- An architectural style for designing networked applications
- Uses `HTTP` as the transport protocol
- Resources are the core abstraction, identified by `URIs`

---
## REST Principles

- Client-server separation
- Statelessness: each request contains all information needed
- Cacheability: responses should indicate if they can be cached
- Uniform interface: consistent resource identifiers and methods
- Layered system: intermediaries like proxies and gateways allowed

---
## HTTP Methods for REST

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| `GET` | Read a resource | Yes | Yes |
| `POST` | Create a resource | No | No |
| `PUT` | Replace a resource | Yes | No |
| `PATCH` | Partially update | No | No |
| `DELETE` | Remove a resource | Yes | No |

---
## Resource Naming Best Practices

- Use nouns, not verbs: `/orders` not `/getOrders`
- Use plural names: `/users` not `/user`
- Nest related resources: `/users/123/orders`
- Use query parameters for filtering: `/orders?status=pending`
- Keep URIs lowercase and use hyphens for readability

---
## REST Response Status Codes

- `2xx` Success: `200 OK`, `201 Created`, `204 No Content`
- `3xx` Redirection: `301 Moved`, `304 Not Modified`
- `4xx` Client Error: `400 Bad Request`, `401 Unauthorized`, `404 Not Found`
- `5xx` Server Error: `500 Internal Server Error`, `503 Service Unavailable`
- Use the most specific code that applies

---
## API Versioning Strategies

- URI path versioning: `/api/v1/users`
- Query parameter versioning: `/api/users?version=1`
- Header versioning: `Accept: application/vnd.myapi.v1+json`
- Each approach has trade-offs in discoverability and caching

---
## REST Pagination

- Offset-based: `?offset=20&limit=10`
    - Simple but can skip or duplicate items if data changes
- Cursor-based: `?cursor=abc123&limit=10`
    - More reliable for streaming data
- Include pagination metadata in the response body or `Link` headers

---
## REST Best Practices Summary

- Use proper `HTTP` methods and status codes
- Version your APIs from the start
- Support pagination for list endpoints
- Use `HATEOAS` links for discoverability when appropriate
- Document APIs with `OpenAPI` / `Swagger` specifications

---
## Introduction to gRPC

- A high-performance, open-source `RPC` framework by Google
- Uses `HTTP/2` for transport and `Protocol Buffers` for serialization
- Supports streaming, bidirectional communication, and deadlines
- Generates client and server code from `.proto` definitions

---
## gRPC vs REST

| Aspect | gRPC | REST |
|--------|------|------|
| Protocol | `HTTP/2` | `HTTP/1.1` or `HTTP/2` |
| Serialization | `Protocol Buffers` (binary) | `JSON` (text) |
| Code generation | Built-in | External tools |
| Streaming | Native support | Limited (SSE, WebSocket) |
| Browser support | Requires proxy | Native |

---
## Protocol Buffers Definition

```protobuf
syntax = "proto3";

service OrderService {
  rpc GetOrder (OrderRequest)
    returns (OrderResponse);
  rpc StreamOrders (OrderFilter)
    returns (stream OrderResponse);
}

message OrderRequest {
  string order_id = 1;
}

message OrderResponse {
  string order_id = 1;
  string status = 2;
  double total = 3;
}
```

---
## gRPC Communication Patterns

![grpc_communication_patterns](/mermaid/courses/architecting/modern-software-architecture/03_communication_patterns/grpc_communication_patterns.mmd)

---
## When to Use gRPC

- Internal service-to-service communication
- High-throughput, low-latency requirements
- Strongly typed contracts are desired
- Streaming data in real time
- Polyglot environments with multiple programming languages

---
## Message Brokers

- Middleware that receives, stores, and delivers messages
- Decouple producers from consumers
- Provide guaranteed delivery, ordering, and replay
- Examples: `RabbitMQ`, `Apache Kafka`, `Amazon SQS`, `NATS`

---
## Message Broker Architecture

![message_broker_architecture](/mermaid/courses/architecting/modern-software-architecture/03_communication_patterns/message_broker_architecture.mmd)

---
## Point-to-Point Messaging

- A message is delivered to exactly one consumer from a queue
- Used for task distribution and work queues
- Consumers compete for messages (competing consumers pattern)
- Guarantees each message is processed once

---
## Publish-Subscribe Messaging

- A message is delivered to all subscribers of a topic
- Used for event broadcasting and notifications
- Each subscriber receives its own copy of the message
- Subscribers can be added without changing the publisher

---
## Pub-Sub Diagram

![pub_sub_diagram](/mermaid/courses/architecting/modern-software-architecture/03_communication_patterns/pub_sub_diagram.mmd)

---
## Kafka vs RabbitMQ

| Aspect | `Apache Kafka` | `RabbitMQ` |
|--------|-------------|------------|
| Model | Distributed log | Message queue |
| Ordering | Per partition | Per queue |
| Retention | Time or size based | Until consumed |
| Throughput | Very high | Moderate |
| Use case | Event streaming | Task queues |

---
## Event-Driven Architecture (EDA)

- A design pattern where the flow is determined by events
- Events represent significant changes in state
- Components react to events rather than being called directly
- Promotes loose coupling and high scalability

---
## EDA Core Concepts

- Event: a record of something that happened (immutable fact)
- Event Producer: generates events when state changes
- Event Consumer: reacts to events and takes action
- Event Channel: the medium that transports events (broker, stream)

---
## Event-Driven Flow

![event_driven_flow](/mermaid/courses/architecting/modern-software-architecture/03_communication_patterns/event_driven_flow.mmd)

---
## Event Types

- Domain Events: represent business-relevant occurrences
    - Example: `OrderPlaced`, `PaymentReceived`
- Integration Events: cross service boundaries
    - Example: published to a broker for other services to consume
- Notification Events: carry minimal data, signal that something happened
- Event-Carried State Transfer: carry full state snapshot in the event payload

---
## Event Schema Design

```json
{
  "eventId": "evt-abc-123",
  "eventType": "OrderPlaced",
  "timestamp": "2026-02-17T10:30:00Z",
  "source": "order-service",
  "data": {
    "orderId": "ord-456",
    "customerId": "cust-789",
    "totalAmount": 99.99
  }
}
```

---
## Guaranteed Delivery Patterns

- At-most-once: message may be lost but never duplicated
- At-least-once: message is never lost but may be duplicated
- Exactly-once: message is delivered exactly one time (hardest to achieve)
- Most systems use at-least-once with idempotent consumers

---
## Dead Letter Queues

- A special queue for messages that cannot be processed
- Messages moved here after exceeding a retry limit
- Enables debugging and manual intervention
- Critical for operational visibility in async systems

---
## Dead Letter Queue Flow

![dead_letter_queue_flow](/mermaid/courses/architecting/modern-software-architecture/03_communication_patterns/dead_letter_queue_flow.mmd)

---
## Choosing a Communication Pattern

![choosing_a_communication_pattern](/mermaid/courses/architecting/modern-software-architecture/03_communication_patterns/choosing_a_communication_pattern.mmd)

---
## Summary

- Synchronous communication is simpler but creates tight coupling
- Asynchronous communication improves resilience and scalability
- `REST` is the standard for external and browser-facing APIs
- `gRPC` excels at internal, high-performance service communication
- Message brokers enable decoupled, reliable async messaging
- Event-Driven Architecture promotes loosely coupled reactive systems
- Choose the pattern based on coupling, latency, and resilience needs
