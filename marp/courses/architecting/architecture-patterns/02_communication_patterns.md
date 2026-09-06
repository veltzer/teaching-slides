---
tags:
  - concepts:architecture
  - concepts:design-patterns
  - concepts:communication-patterns
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---

# Communication Patterns

---

## Client-Server Overview

- Separates the system into two applications:
    - Client: Requests services, can be "thin" or "thick"
    - Server: Provides services, often manages resources
- Client and server have different lifecycles but communicate via requests/responses

---

## Client-Server Component Roles

- Client
    - Initiates requests to the server
    - Waits for and receives server responses
    - Usually interacts directly with end users
- Server
    - Listens for client requests
    - Processes requests and sends responses back
    - May validate requests and authorize access
    - Often manages shared resources

---

## Client-Server Diagram

![communication_diagram](svg/courses/architecting/architecture-patterns/02_communication_patterns/communication_diagram.svg)

---

## Client-Server Pros and Cons

Pros:
- Centralized control and management of resources
- Supports many clients with different capabilities
- Easy to add new clients without changing the server
- Clients and servers can evolve independently

Cons:
- Server can be a single point of failure
- Potential performance bottlenecks at the server
- Limited offline capability for thin clients
- Security and scalability can be challenging

---

## Client-Server When to Use

- Resources need to be centrally managed
- Many clients need to access the same data or services
- Clients may have different capabilities or technical stacks
- System must support changing client-side platforms
- Processing can be offloaded from clients to server

---

## Broker Overview

- A broker component coordinates communication between clients and servers
- Clients request services from the broker, not directly from servers
- Servers register their services with the broker and wait for requests
- Broker decouples clients from servers and provides additional services

---

## Broker Component Roles

- Broker
    - Maintains a registry of available services and their locations
    - Receives client requests and forwards them to appropriate servers
    - May provide additional services like logging, security, or transaction management
- Client
    - Requests services from the broker using a common interface
    - Does not need to know the location or implementation details of servers
- Server
    - Registers its services with the broker
    - Receives requests from the broker and sends responses back
    - Does not interact directly with clients

---

## Broker Interaction Diagram

![broker_interaction_diagram](svg/courses/architecting/architecture-patterns/02_communication_patterns/broker_interaction_diagram.svg)

---

## Broker Pros and Cons

Pros:
- Decouples clients from servers
- Enables location transparency and platform independence
- Supports dynamic registration and discovery of services
- Can provide additional services and optimizations

Cons:
- Broker can become a performance bottleneck or single point of failure
- Added complexity from the broker component and interactions
- Potential latency overhead from indirection through broker
- Clients and servers must agree on a common broker interface

---

## Broker When to Use

- Clients need to access multiple services in a uniform way
- Services need to be decoupled from clients for flexibility
- Dynamic registration and discovery of services is required
- Additional services like logging or security need to be centralized
- Platform and language independence between clients and servers is desired

---

## P2P Overview

- Distributes tasks or workloads between equally privileged participants (peers)
- Peers are both consumers and suppliers of resources
- Peers can act as clients, servers, or both
- Decentralized model without the need for central coordination

---

## Peer-to-Peer Roles

- Peer
    - Participates in the network both as a consumer and supplier of resources
    - Can act as a client by requesting services from other peers
    - Can act as a server by providing services to other peers
    - May have different capabilities or responsibilities
- Connection
    - Logical link between two peers that enables communication
    - Can be direct or indirect (e.g., through other peers)
    - Can be persistent or created on-demand

---

## Peer-to-Peer Diagram

![peer_to_peer_diagram](svg/courses/architecting/architecture-patterns/02_communication_patterns/peer_to_peer_diagram.svg)

---

## Peer-to-Peer Pros and Cons

Pros:
- Eliminates the need for central servers or authorities
- Can increase robustness and availability through redundancy
- Enables collaborative resource sharing and aggregation
- Supports scalability by distributing load among peers

Cons:
- Complexity of peer discovery and communication
- Potential security and trust issues between peers
- Performance can be unpredictable and depends on peer capabilities
- Harder to ensure data consistency and integrity across peers

---

## Peer-to-Peer When to Use

- Resources are distributed among multiple participants
- Centralized control or single points of failure need to be avoided
- Collaborative resource sharing or aggregation is desired
- Scalability and load balancing can be achieved through peer distribution
- Participants are willing to contribute resources as well as consume them

---

## Event Bus Overview

- An in-process dispatcher that wires components together inside a single application
- Publishers raise events; the bus invokes registered handlers in the same process
- Routing is by event type (the class or name of the event), not by network topic
- Typically synchronous and in-memory — no broker, no network hop, no durability
- Examples: Guava EventBus, Spring ApplicationEventPublisher, .NET MediatR, browser EventTarget

---

## Event Bus Roles

- Event Bus
    - A library object living inside the application process
    - Maintains an in-memory map from event type to handler list
    - Dispatches each event by calling its handlers directly (often on the publisher's thread)
- Publisher
    - Code that constructs an event object and hands it to the bus
    - Does not know which handlers exist, or whether any do
- Subscriber
    - Code in the same process that registers a handler for an event type
    - Runs as a callback when an event of that type is dispatched

---

## Event Bus Interaction Diagram

![event_bus_interaction_diagram](svg/courses/architecting/architecture-patterns/02_communication_patterns/event_bus_interaction_diagram.svg)

---

## Event Bus Pros and Cons

Pros:
- Decouples modules within one process without inventing interfaces between them
- Trivial to set up — just a library, no infrastructure to deploy or operate
- Cheap and fast — direct method calls, no serialization, no network
- Easy to add a new reaction to an existing event without touching the publisher

Cons:
- Bounded to one process — does not span services or machines
- Synchronous dispatch means a slow handler blocks the publisher
- A throwing handler can break the publisher unless the bus isolates errors
- No durability or replay — if no one is subscribed when the event fires, it is lost
- Implicit wiring makes the call graph hard to read in an IDE

---

## Event Bus When to Use

- Inside a single application that wants internal modules to react to domain events
- When you want to break a direct call dependency between two modules in the same process
- For UI frameworks where widgets react to user actions
- For lightweight in-process domain events in a modular monolith
- Not appropriate when publisher and subscriber live in different services — use pub-sub for that

---

## Pub-Sub Overview

- A messaging pattern that runs over a message broker shared by many processes or services
- Publishers send messages to a topic on the broker; they do not call subscribers
- Subscribers connect to the broker and ask to receive messages from specific topics
- Communication is asynchronous and crosses process, machine, and network boundaries
- The broker can buffer, persist, replay, fan-out, and filter messages
- Examples: Kafka, RabbitMQ, NATS, MQTT, AWS SNS/SQS, Google Pub/Sub, Redis Pub/Sub

---

## Publish-Subscribe Key Concepts

- Publisher
    - A separate process or service that sends messages to the broker over the network
    - Does not know who, or how many, subscribers exist
- Subscriber
    - A separate process or service that connects to the broker and consumes from topics
    - Multiple independent subscribers can each receive their own copy of the same message
- Message Broker
    - A dedicated piece of infrastructure (Kafka, RabbitMQ, NATS, etc.) that you deploy and operate
    - Buffers messages so publisher and subscriber do not need to be online at the same time
    - May persist messages on disk and allow replay from an offset
    - Performs routing, filtering, and fan-out based on topic and subscription
- Topic or Channel
    - A named stream on the broker that publishers write to and subscribers read from
    - The unit of routing — there is no event-type dispatch, just topic membership
    - Often supports hierarchies or wildcards (e.g. `orders.*`, `sensors/+/temp`)

---

## Publish-Subscribe Diagram

![publish_subscribe_diagram](svg/courses/architecting/architecture-patterns/02_communication_patterns/publish_subscribe_diagram.svg)

---

## Publish-Subscribe Pros and Cons

Pros:
- Decouples services across process and machine boundaries — publisher and subscriber can be written in different languages and deployed independently
- Asynchronous: a slow or down subscriber does not block the publisher
- Buffering and persistence let producers and consumers run at different rates and survive restarts
- Replay from a stored offset enables new subscribers to catch up on history (Kafka-style brokers)
- Fan-out: a single message reaches many independent subscriber groups

Cons:
- You must deploy, secure, monitor, and upgrade the broker — real operational cost
- Network and serialization add latency a function call would not
- At-least-once delivery is the norm — subscribers must be idempotent
- Global ordering across topics or partitions is usually not guaranteed
- Tracing a request across many topics and consumers is harder than reading a stack trace

---

## Publish-Subscribe When to Use

- One service needs to inform many other services that something happened, without knowing them
- Producers and consumers need to scale, deploy, and fail independently
- A burst of work needs to be absorbed by the broker and drained at the consumers' pace
- New consumers must be able to join later and replay historical events
- Cross-language, cross-platform, or cross-team integration where shared code is not an option

---

## Event Bus vs Publish-Subscribe

| | Event Bus | Publish-Subscribe |
|---|---|---|
| Scope | Inside one process | Across processes / services / machines |
| Transport | In-memory method calls | Network protocol over a broker |
| Routing key | Event type (class) | Topic / channel name |
| Default timing | Synchronous | Asynchronous |
| Infrastructure | A library | A broker you must operate |
| Durability / replay | None | Available (Kafka-style) |
| If no subscriber | Event is dropped | Broker buffers (and may persist) |
| Failure isolation | Handler exception can hit publisher | Broker isolates publisher from subscribers |

---

## Summary

- Client-Server centralizes resources behind one server contract
- Broker adds an intermediary that decouples clients from concrete servers
- Peer-to-Peer removes the central coordinator entirely
- Event Bus is an *in-process* dispatcher routed by event type — a library, synchronous, no durability
- Publish-Subscribe is a *cross-process* messaging pattern routed by topic over a broker — asynchronous, buffered, often durable
- Pick by where the boundary is: same process → event bus; different services → pub-sub
