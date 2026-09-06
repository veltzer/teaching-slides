---
tags:
  - networking:grpc
  - tools:protobuf
level: intermediate
category: networking
audience:
  - audiences:developers

---

# Protocol Buffers

---

## What This Chapter Covers

- proto3 syntax overview
- Messages: scalar types, nested, repeated, maps
- Enums, oneof, well-known types
- Importing and packaging
- Reserved fields and backward compatibility

---

## Why Protocol Buffers?

- Compact binary on the wire
- Strict schema — type errors caught at compile time
- Multi-language code generation
- Versioning rules built in
- Independent of gRPC — usable on its own too

---

## End-to-End Workflow

![proto_workflow](svg/courses/networking/grpc/02_protocol_buffers/proto_workflow.svg)

---

## proto3 vs proto2

- proto3 is the current default
- All fields are optional in proto3 (no required keyword)
- Default values handled simply
- Cleaner syntax than proto2
- Use proto3 unless legacy reasons demand proto2

---

## Basic File Structure

```protobuf
syntax = "proto3";

package example.greeter;

option go_package = "github.com/example/greeter";

message HelloRequest {
    string name = 1;
}
```

- `syntax` declaration first
- `package` for namespace
- Optional language-specific options
- Messages and services follow

---

## Scalar Types

- `int32`, `int64`, `uint32`, `uint64`
- `float`, `double`
- `bool`
- `string` — UTF-8
- `bytes` — arbitrary binary
- Choose width based on actual range

---

## Field Numbers

- Each field has a unique number, used on the wire
- Numbers 1-15 use one byte for the tag (faster)
- Reserve low numbers for frequent fields
- Once assigned, never reuse — deserialization breaks
- Numbers go up to 2^29-1, plenty of room

---

## Messages and Nesting

```protobuf
message Address {
    string street = 1;
    string city = 2;
    string country = 3;
}

message User {
    string id = 1;
    Address shipping = 2;
    Address billing = 3;
}
```

- Messages can contain other messages
- Nesting models real domain hierarchies
- Common pattern for composite data

---

## Repeated Fields

- `repeated string emails = 1;` — a list
- Equivalent to `[]string`, `List<String>`, etc
- Default empty when not provided
- Order is preserved in the wire format
- The standard way to model lists

---

## Maps

```protobuf
message Config {
    map<string, string> labels = 1;
    map<string, int32> counts = 2;
}
```

- Key/value pairs
- Keys: integer or string types
- Values: any non-map message or scalar
- Implemented as a list of entries on the wire

---

## Enums

```protobuf
enum Status {
    STATUS_UNSPECIFIED = 0;
    STATUS_ACTIVE = 1;
    STATUS_SUSPENDED = 2;
    STATUS_DELETED = 3;
}
```

- Always include 0 with UNSPECIFIED
- Helps catch missed initialization
- Integer-backed; no string surprise
- Add values at the end; don't reorder

---

## oneof

```protobuf
message Notification {
    oneof channel {
        string email = 1;
        string sms = 2;
        string webhook_url = 3;
    }
}
```

- Exactly one of the listed fields is set
- Saves space; expresses union types cleanly
- Switch on the discriminator in code
- Cannot mix `repeated` inside oneof

---

## Field Visualization

![protobuf_anatomy](svg/courses/networking/grpc/02_protocol_buffers/protobuf_anatomy.svg)

---

## Wire Format

![wire_format](svg/courses/networking/grpc/02_protocol_buffers/wire_format.svg)

---

## Schema Evolution Rules

![proto_evolution](svg/courses/networking/grpc/02_protocol_buffers/proto_evolution.svg)

---

## Well-Known Types

- `google.protobuf.Timestamp` — UTC time, second + nanos
- `google.protobuf.Duration` — time span
- `google.protobuf.Any` — arbitrary nested message
- `google.protobuf.Struct` — JSON-like dynamic data
- `google.protobuf.FieldMask` — partial updates

---

## Timestamps Done Right

- Always use UTC
- Resolution to nanoseconds
- Library converters to/from native time types
- Don't reinvent — use the well-known type
- Date-only? Use `google.type.Date` from google/type

---

## Importing Files

```protobuf
import "google/protobuf/timestamp.proto";
import "common/types.proto";

message Event {
    google.protobuf.Timestamp occurred_at = 1;
    common.UserID user = 2;
}
```

- Standard library and your own packages
- Build system manages include paths
- Buf and bazel have their own setups
- Avoid circular imports

---

## Packages and Names

- Package becomes the namespace in generated code
- `package my.service;` → `my/service` directory hint
- Avoid generic names — collide easily
- Use reverse-DNS conventions (`com.example.x`)
- Each language has its own mapping rules

---

## Reserved Fields

```protobuf
message User {
    reserved 3, 5, 9 to 12;
    reserved "old_name", "removed_field";

    string id = 1;
    string email = 2;
}
```

- Mark removed field numbers as reserved
- Prevents accidental reuse
- Compile-time error if you try to assign 3
- Critical for long-term schema stability

---

## Compatibility Rules: Adding Fields

- New optional field — safe both directions
- New repeated field — safe (defaults to empty)
- Don't change existing field types
- Don't reuse a number you removed
- These rules echo Avro and JSON Schema

---

## Compatibility Rules: Removing

- Mark the field reserved
- Old code reading new wire format ignores absent fields
- New code reading old wire format gets defaults
- Never reuse the number — reserve it forever
- Reservation costs nothing; reuse is dangerous

---

## Default Values

- proto3 fields have implicit defaults
- Strings: empty string
- Numbers: zero
- Bools: false
- Messages: not set (nullable in some languages)
- Cannot distinguish "set to default" from "unset" in proto3 (without wrappers)

---

## Wrapper Types for Nullable

- `google.protobuf.StringValue` — nullable string
- `google.protobuf.Int32Value` — nullable int
- Use when you need to distinguish "set" from "default"
- More boilerplate than scalars
- Useful in patch/update payloads

---

## proto3 Optional (Recent)

- Newer proto3 supports `optional` keyword
- Restores presence-tracking like proto2
- Now: `optional string name = 1;`
- Better for partial updates and patches
- Available in protoc 3.15+

---

## Schema Files in Practice

- One service per .proto when possible
- Common types in `common/` or `types/`
- Generated code committed or built per CI
- Buf BSR or similar for distributing schemas
- Treat .proto changes like API changes — review carefully

---

## Tooling: protoc

- The official compiler
- Generates code for many languages with plugins
- `protoc --go_out=. --go-grpc_out=. file.proto`
- Clunky CLI but the foundation of everything
- Most projects wrap it in build scripts

---

## Tooling: Buf

- Modern UX for protobuf
- Linting (style, breaking-change detection)
- BSR — schema registry like npm for protos
- `buf generate` replaces ad-hoc protoc invocations
- Recommended for serious projects

---

## Common Pitfalls

- Reusing field numbers after removal
- Forgetting `reserved` when removing
- Putting all messages in one giant file
- Making field 1 optional and 100 required (numbers don't reflect priority)
- Wrong scalar width — `int32` for a Unix timestamp overflows in 2038

---

## Summary

- Protocol Buffers — the schema language for gRPC
- Strict types, compact wire format, multi-language codegen
- Field numbers are forever; use `reserved` to retire them
- Well-known types cover timestamps, durations, dynamic data
- Buf and modern tooling make working with protobuf pleasant
