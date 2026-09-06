---
tags:
  - networking:grpc
  - concepts:rpc
level: intermediate
category: networking
audience:
  - audiences:developers

---

# The Four RPC Types

---

## What This Chapter Covers

- Unary RPC — request/response
- Server streaming
- Client streaming
- Bidirectional streaming
- Use cases and patterns for each

---

## The Four Types

- Unary: one request, one response
- Server streaming: one request, many responses
- Client streaming: many requests, one response
- Bidirectional streaming: many requests, many responses
- Each maps to a method shape in the .proto

---

## .proto Syntax for Each

```protobuf
service Chat {
    // Unary
    rpc SendMessage(MessageRequest) returns (MessageReply);

    // Server streaming
    rpc Subscribe(SubscribeRequest) returns (stream Message);

    // Client streaming
    rpc Upload(stream Chunk) returns (UploadReply);

    // Bidirectional
    rpc Chat(stream Message) returns (stream Message);
}
```

---

## Four Types Visualized

![rpc_types](svg/courses/networking/grpc/03_rpc_types/rpc_types.svg)

---

## Streaming Modes Compared

![streaming_modes](svg/courses/networking/grpc/03_rpc_types/streaming_modes.svg)

---

## Unary RPC

- The simplest pattern — like a function call
- Client sends one message, gets one back
- Synchronous in feel; usually async in code
- Most common type — covers the bulk of RPCs
- Deadlines and cancellation work naturally

---

## When to Use Unary

- CRUD operations
- Lookups (`GetUser`, `GetOrder`)
- Commands with simple acks
- Anything fitting the request/response shape
- Default choice unless streaming adds value

---

## Server Streaming

- Client sends one request
- Server sends a stream of responses
- Stream ends when server closes it
- Client iterates over the stream
- No further input from client during the stream

---

## When to Use Server Streaming

- Real-time feeds: stock prices, sports scores
- Large result sets: pagination's alternative
- Progress updates: long-running operations
- Live tail of logs
- Server pushes data; client just listens

---

## Client Streaming

- Client sends a stream of requests
- Server sends one response when done
- Useful for batch ingestion or upload
- Less common than server streaming
- Server can't reply until client finishes

---

## When to Use Client Streaming

- File upload in chunks
- Telemetry/event ingestion
- Batch processing where order matters
- Aggregating client-side data over time
- Saves on connection overhead vs many unary calls

---

## Bidirectional Streaming

- Both sides send streams independently
- Read and write streams are decoupled
- Each can act asynchronously
- Like a TCP connection but typed
- The most flexible (and complex) pattern

---

## When to Use Bidirectional

- Chat applications
- Live collaboration (cursors, edits)
- Game state synchronization
- Real-time interactive sessions
- When neither side dictates the rhythm

---

## Implementing Unary (Server, Go)

```go
func (s *server) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
    user, err := s.repo.Find(ctx, req.GetId())
    if err != nil {
        return nil, status.Error(codes.NotFound, "user not found")
    }
    return user, nil
}
```

- Simple function shape
- Context for cancellation and deadlines
- Return response or error

---

## Implementing Unary (Client, Go)

```go
ctx, cancel := context.WithTimeout(context.Background(), time.Second)
defer cancel()

resp, err := client.GetUser(ctx, &pb.GetUserRequest{Id: "42"})
if err != nil {
    log.Fatalf("GetUser failed: %v", err)
}
fmt.Println(resp.GetEmail())
```

- Looks like a normal function call
- Pass a context to control deadlines
- Handle errors as values

---

## Implementing Server Streaming

```go
func (s *server) Subscribe(req *pb.SubscribeRequest, stream pb.Chat_SubscribeServer) error {
    for msg := range s.subscribe(req) {
        if err := stream.Send(msg); err != nil {
            return err
        }
    }
    return nil
}
```

- `stream.Send` for each message
- Return when done; gRPC closes the stream
- Errors abort the stream

---

## Implementing Client Streaming

```go
func (s *server) Upload(stream pb.Storage_UploadServer) error {
    var size int64
    for {
        chunk, err := stream.Recv()
        if err == io.EOF {
            return stream.SendAndClose(&pb.UploadReply{Size: size})
        }
        if err != nil { return err }
        size += int64(len(chunk.Data))
    }
}
```

- Loop on `stream.Recv`
- Detect EOF for end-of-stream
- `SendAndClose` sends the final response

---

## Implementing Bidi Streaming

```go
func (s *server) Chat(stream pb.Chat_ChatServer) error {
    for {
        msg, err := stream.Recv()
        if err == io.EOF { return nil }
        if err != nil { return err }
        if err := stream.Send(reply(msg)); err != nil { return err }
    }
}
```

- Reads and writes independently
- No fixed pattern — react as needed
- Most flexible; most care needed

---

## Flow Control and Backpressure

- HTTP/2 manages flow control
- A slow consumer slows the producer naturally
- gRPC libraries expose this implicitly
- Careless server-side code can block
- Honor cancellation and deadlines explicitly

---

## Stream Lifecycle

- Open: client initiates the call
- Active: messages flow as needed
- Half-close: one side stops sending
- Close: both sides done; status emitted
- Status code (OK or error) ends every call

---

## Error Handling in Streams

- Errors abort the stream immediately
- Use status codes for semantic errors
- Network errors look like cancellation in some clients
- Plan for partial completion
- Logging the error per stream is essential

---

## Choosing the Right Type

- Default: unary
- Long-running result set from server: server streaming
- Bulk upload from client: client streaming
- Truly interactive: bidi
- Don't use streaming for simple request/response

---

## Common Pitfalls

- Bidirectional when you needed two unary RPCs
- Server streaming forever without a way to close
- Client streaming with no timeout — leaks resources
- Mixing per-message ack logic into bidirectional streams
- Treating streaming as "free" — it has overhead

---

## Summary

- Four RPC types: unary, server stream, client stream, bidi
- Match the type to the data flow shape
- Unary covers most cases — start there
- Streaming earns its complexity for real-time and bulk data
- Each language provides idiomatic APIs for all four
