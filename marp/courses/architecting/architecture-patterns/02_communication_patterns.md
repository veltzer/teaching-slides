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

- Components communicate through a central event dispatcher (bus)
- Publishers send events to the bus without knowing the subscribers
- Subscribers register interest in specific events and are notified by the bus
- Decouples publishers from subscribers and enables event-driven architecture

---
## Event Bus Roles

- Event Bus
    - Central communication channel for events
    - Receives events from publishers and dispatches them to subscribers
    - Can provide additional services like event filtering, transformation, or persistence
- Publisher
    - Sends events to the event bus
    - Does not need to know or depend on the subscribers
    - Can publish different types of events
- Subscriber
    - Registers interest in specific events with the event bus
    - Receives and handles events dispatched by the bus
    - Can subscribe to different types of events

---

## Event Bus Interaction Diagram

![event_bus_interaction_diagram](svg/courses/architecting/architecture-patterns/02_communication_patterns/event_bus_interaction_diagram.svg)

---

## Event Bus Pros and Cons

Pros:
- Decouples publishers from subscribers
- Enables event-driven and reactive architectures
- Supports dynamic and flexible event routing
- Can scale publishers and subscribers independently

Cons:
- Introduces additional complexity and potential performance overhead
- Event bus can become a bottleneck or single point of failure
- Subscribers need to carefully handle event ordering and duplicates
- Debugging and tracing event flows can be challenging

---

## Event Bus When to Use

- Publishers need to broadcast events without knowing the subscribers
- Subscribers need to dynamically register interest in specific events
- Event-driven communication and reactive processing are required
- Flexibility and extensibility in event routing and handling are desired
- Loose coupling and independent scalability of components are important

---
## Pub-Sub Overview

- Defines a messaging pattern for communication between publishers and subscribers
- Publishers send messages to a message broker or event bus
- Subscribers register their interest in specific topics or message types
- The message broker delivers the messages to all interested subscribers
- Enables loose coupling and asynchronous communication between components

---

## Publish-Subscribe Key Concepts

- Publisher
    - A component that sends messages to the message broker
    - Publishes messages without knowledge of the subscribers
    - Can publish messages to multiple topics or channels
- Subscriber
    - A component that registers interest in specific topics or message types
    - Receives messages from the message broker based on its subscriptions
    - Can subscribe to multiple topics or channels
- Message Broker
    - A central component that receives messages from publishers and delivers them to subscribers
    - Maintains a registry of subscriptions and their associated subscribers
    - Can perform message filtering, transformation, and routing based on topic or message type
- Topic or Channel
    - A logical grouping or category of messages
    - Used by publishers to organize and categorize messages
    - Used by subscribers to express their interest in specific types of messages

---

## Publish-Subscribe Diagram

![publish_subscribe_diagram](svg/courses/architecting/architecture-patterns/02_communication_patterns/publish_subscribe_diagram.svg)

---

## Publish-Subscribe Pros and Cons

Pros:
- Enables loose coupling between publishers and subscribers
- Supports asynchronous communication and independent scalability of components
- Allows for dynamic registration and deregistration of subscribers
- Facilitates event-driven architectures and reactive systems
- Provides flexibility in message routing and filtering based on topics or message types

Cons:
- Introduces additional complexity and potential performance overhead due to the message broker
- Requires careful design and management of topics and subscriptions to avoid message flooding
- Can lead to increased latency due to the indirection through the message broker
- Requires reliable message delivery and handling of failures in the message broker
- May not be suitable for scenarios requiring strict message ordering or real-time processing

---

## Publish-Subscribe When to Use

- When loose coupling and asynchronous communication between components are desired
- When the system needs to support dynamic registration and deregistration of subscribers
- When the system benefits from event-driven architectures and reactive processing
- When the scalability and independent evolution of publishers and subscribers are important
- When the system needs to handle a high volume of messages and perform message routing and filtering
- When the system can tolerate some level of latency and eventual consistency in message delivery

---
## Summary

- Client-Server centralizes resources behind one server contract
- Broker adds an intermediary that decouples clients from concrete servers
- Peer-to-Peer removes the central coordinator entirely
- Event Bus and Publish-Subscribe both decouple sender from receiver, with topic-based filtering
- Choose synchronous (client-server, broker) for request-response, asynchronous (event bus, pub-sub) for fire-and-forget
