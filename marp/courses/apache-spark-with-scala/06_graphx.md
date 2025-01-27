# Graph Processing with GraphX

## Introduction to Graph Computation

1. Vertices and Edges
1. Graph Properties
1. Graph Algorithms
1. Graph Analytics
1. Graph Visualization

---

## Graph Basics

![0](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/0.png)

---

## Graph Components

![1](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/1.png)

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

![2](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/2.png)

---

## Edge Operations

![3](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/3.png)

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

![4](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/4.png)

---

## Graph Transformations

![5](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/5.png)

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

![6](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/6.png)

---

## Message Passing

![7](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/7.png)

---

## Pregel API

![8](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/8.png)

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

![9](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/9.png)

---

## PageRank Flow

![10](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/10.png)

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

![11](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/11.png)

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

![12](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/12.png)

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

![13](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/13.png)

---

## Performance Optimization

![14](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/14.png)

---

## Best Practices

![15](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/15.png)

---

## Graph Building

![16](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/16.png)

---

## Graph Analytics

![17](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/17.png)

---

## Use Cases

1. Social Network Analysis
1. Recommendation Systems
1. Fraud Detection
1. Network Optimization
1. Knowledge Graphs

---

## Advanced Features

![18](../../../out/mermaid/marp/courses/apache-spark-with-scala/06_graphx.md/18.png)
