# Graph Processing with GraphX

## Introduction to Graph Computation

1. Vertices and Edges
1. Graph Properties
1. Graph Algorithms
1. Graph Analytics
1. Graph Visualization

---

## Graph Basics

```mermaid
graph LR
    A((V1)) --> B((V2))
    B --> C((V3))
    C --> A
    style A fill:#f96
    style B fill:#f96
    style C fill:#f96
```

---

## Graph Components

```mermaid
graph TB
    A[Graph] --> B[Vertices]
    A --> C[Edges]
    B --> D[Properties]
    C --> E[Attributes]
    style A fill:#f96
```

---

## Graph Creation

```scala
import org.apache.spark.graphx._
val vertices = sc.parallelize(Array(
  (1L, ("Alice", 28)),
  (2L, ("Bob", 27)),
  (3L, ("Charlie", 65))
))
val edges = sc.parallelize(Array(
  Edge(1L, 2L, "coworker"),
  Edge(2L, 3L, "parent"),
  Edge(3L, 1L, "friend")
))
val graph = Graph(vertices, edges)
```

---

## Vertex Operations

```mermaid
graph TB
    A[Vertex] --> B[Properties]
    A --> C[Degree]
    A --> D[Neighbors]
    B --> E[Updates]
    style A fill:#f96
```

---

## Edge Operations

```mermaid
graph LR
    A[Edge] --> B[Source]
    A --> C[Target]
    A --> D[Properties]
    style A fill:#f96
```

---

## Basic Operations

```scala
// Count vertices and edges
println(s"Vertices: ${graph.vertices.count()}")
println(s"Edges: ${graph.edges.count()}")
// Get vertex degrees
val degrees = graph.degrees
```

---

## Property Graphs

```mermaid
graph LR
    A((A:User<br/>age:28)) -->|knows| B((B:User<br/>age:27))
    B -->|follows| C((C:User<br/>age:65))
    style A fill:#f96
    style B fill:#f96
    style C fill:#f96
```

---

## Graph Transformations

```mermaid
graph TB
    A[Transform] --> B[Map Vertices]
    A --> C[Map Edges]
    B --> D[New Graph]
    C --> D
    style A fill:#f96
```

---

## Transformation Code

```scala
// Map vertices
val newGraph = graph.mapVertices((id, attr) =>
  attr._2 * 2)
// Map edges
val weightedGraph = graph.mapEdges(e =>
  e.attr.length.toDouble)
```

---

## Aggregation Operations

```mermaid
graph LR
    A[Graph] --> B[Aggregate Messages]
    B --> C[Combine Messages]
    C --> D[Update Graph]
    style B fill:#f96
```

---

## Message Passing

```mermaid
graph TB
    A((V1)) -->|msg| B((V2))
    B -->|msg| C((V3))
    C -->|msg| A
    style B fill:#f96
```

---

## Pregel API

```mermaid
graph LR
    A[Initial] --> B[Send Messages]
    B --> C[Combine Messages]
    C --> D[Update Vertices]
    D --> B
    style C fill:#f96
```

---

## Pregel Implementation

```scala
val initialGraph = graph.mapVertices((id, _) =>
  if (id == sourceId) 0.0 else Double.PositiveInfinity)
val sssp = initialGraph.pregel(Double.PositiveInfinity)(
  (id, dist, newDist) => math.min(dist, newDist),
  triplet => {
    if (triplet.srcAttr + triplet.attr < triplet.dstAttr) {
      Iterator((triplet.dstId, triplet.srcAttr + triplet.attr))
    } else {
      Iterator.empty
    }
  },
  (a, b) => math.min(a, b)
)
```

---

## Graph Algorithms

```mermaid
graph TB
    A[Algorithms] --> B[PageRank]
    A --> C[Connected Components]
    A --> D[Triangle Counting]
    A --> E[Shortest Paths]
    style A fill:#f96
```

---

## PageRank Flow

```mermaid
graph LR
    A[Initial Rank] --> B[Distribute]
    B --> C[Calculate]
    C --> D[Update]
    D --> B
    style C fill:#f96
```

---

## PageRank Implementation

```scala
val ranks = graph.pageRank(0.0001).vertices
val users = vertices.map { case (id, (name, age)) =>
  (id, name) }
val ranksByUsername = users.join(ranks).map {
  case (id, (name, rank)) => (name, rank)
}
```

---

## Connected Components

```mermaid
graph TB
    subgraph Component 1
    A((1)) --- B((2))
    end
    subgraph Component 2
    C((3)) --- D((4))
    end
```

---

## Component Analysis

```scala
val cc = graph.connectedComponents()
val componentCounts = cc.vertices
  .map(_._2)
  .countByValue()
```

---

## Triangle Counting

```mermaid
graph LR
    A((1)) --> B((2))
    B --> C((3))
    C --> A
    style A fill:#f96
    style B fill:#f96
    style C fill:#f96
```

---

## Triangle Implementation

```scala
val triCounts = graph.triangleCount()
val maxTris = triCounts.vertices
  .map(_._2)
  .max()
```

---

## Graph Partitioning

```mermaid
graph TB
    A[Graph] --> B[Partition 1]
    A --> C[Partition 2]
    A --> D[Partition 3]
    style A fill:#f96
```

---

## Performance Optimization

```mermaid
graph LR
    A[Optimization] --> B[Partitioning]
    A --> C[Caching]
    A --> D[Join Strategy]
    style A fill:#f96
```

---

## Best Practices

```mermaid
graph TB
    A[Best Practices] --> B[Data Structure]
    A --> C[Algorithm Choice]
    A --> D[Memory Usage]
    A --> E[Partitioning]
    style A fill:#f96
```

---

## Graph Building

```mermaid
graph LR
    A[Raw Data] --> B[Vertices]
    A --> C[Edges]
    B --> D[Graph]
    C --> D
    style D fill:#f96
```

---

## Graph Analytics

```mermaid
graph TB
    A[Analytics] --> B[Centrality]
    A --> C[Community]
    A --> D[Path Analysis]
    style A fill:#f96
```

---

## Use Cases

1. Social Network Analysis
1. Recommendation Systems
1. Fraud Detection
1. Network Optimization
1. Knowledge Graphs

---

## Advanced Features

```mermaid
graph TB
    A[Advanced] --> B[Custom Algorithms]
    A --> C[Graph Builders]
    A --> D[Optimizers]
    style A fill:#f96
```
