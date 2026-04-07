# Graph Processing with GraphX

## Introduction to Graph Computation

1. Vertices and Edges
1. Graph Properties
1. Graph Algorithms
1. Graph Analytics
1. Graph Visualization

---

## Graph Basics

![graph_basics](svg/courses/big_data/apache-spark-with-scala/07_graphx/graph_basics.svg)

---

## Graph Components

![graph_components](svg/courses/big_data/apache-spark-with-scala/07_graphx/graph_components.svg)

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

![vertex_operations](svg/courses/big_data/apache-spark-with-scala/07_graphx/vertex_operations.svg)

---

## Edge Operations

![edge_operations](svg/courses/big_data/apache-spark-with-scala/07_graphx/edge_operations.svg)

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

![property_graphs](svg/courses/big_data/apache-spark-with-scala/07_graphx/property_graphs.svg)

---

## Graph Transformations

![graph_transformations](svg/courses/big_data/apache-spark-with-scala/07_graphx/graph_transformations.svg)

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

![aggregation_operations](svg/courses/big_data/apache-spark-with-scala/07_graphx/aggregation_operations.svg)

---

## Message Passing

![message_passing](svg/courses/big_data/apache-spark-with-scala/07_graphx/message_passing.svg)

---

## Pregel API

![pregel_api](svg/courses/big_data/apache-spark-with-scala/07_graphx/pregel_api.svg)

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

![graph_algorithms](svg/courses/big_data/apache-spark-with-scala/07_graphx/graph_algorithms.svg)

---

## PageRank Flow

![pagerank_flow](svg/courses/big_data/apache-spark-with-scala/07_graphx/pagerank_flow.svg)

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

![connected_components](svg/courses/big_data/apache-spark-with-scala/07_graphx/connected_components.svg)

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

![triangle_counting](svg/courses/big_data/apache-spark-with-scala/07_graphx/triangle_counting.svg)

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

![graph_partitioning](svg/courses/big_data/apache-spark-with-scala/07_graphx/graph_partitioning.svg)

---

## Performance Optimization

![performance_optimization](svg/courses/big_data/apache-spark-with-scala/07_graphx/performance_optimization.svg)

---

## Best Practices

![best_practices](svg/courses/big_data/apache-spark-with-scala/07_graphx/best_practices.svg)

---

## Graph Building

![graph_building](svg/courses/big_data/apache-spark-with-scala/07_graphx/graph_building.svg)

---

## Graph Analytics

![graph_analytics](svg/courses/big_data/apache-spark-with-scala/07_graphx/graph_analytics.svg)

---

## Use Cases

1. Social Network Analysis
1. Recommendation Systems
1. Fraud Detection
1. Network Optimization
1. Knowledge Graphs

---

## Advanced Features

![advanced_features](svg/courses/big_data/apache-spark-with-scala/07_graphx/advanced_features.svg)
