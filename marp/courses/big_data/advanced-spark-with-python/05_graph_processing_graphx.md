---
tags:
  - tools:spark
  - languages:python
  - data-and-ai:big-data
  - concepts:graph-processing
level: advanced
category: big-data
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Graph Processing with GraphX

---

## Introduction to GraphX
* Graph computation model
* Vertices and edges
* Property graphs
* Graph operators

---

## Graph Abstractions
![graph_abstractions](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/graph_abstractions.svg)

---

## Basic Components
1. Vertex RDD
1. Edge RDD
1. Property graph
1. Triplets

---

## Creating Graphs
```python
# Create vertices and edges as DataFrames
from graphframes import GraphFrame
v = spark.createDataFrame(
    [("1", "A"), ("2", "B"), ("3", "C")], ["id", "name"])
e = spark.createDataFrame(
    [("1", "2", "connects"), ("2", "3", "connects")],
    ["src", "dst", "relationship"])
graph = GraphFrame(v, e)
```

---

## Graph Construction
![graph_construction](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/graph_construction.svg)

---

## Property Graphs
1. Vertex properties
1. Edge properties
1. Graph metadata
1. Property operations

---

## Graph Properties
```python
# Add properties to vertices
def add_property(v):
    return (v[0], {"name": v[1], "degree": 0})
vertices_with_props = vertices.map(add_property)
```

---

## Basic Operations
![basic_operations](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/basic_operations.svg)

---

## Graph Transformations
1. Map vertices
1. Map edges
1. Map triplets
1. Filter operations

---

## Vertex Programs
```python
# Vertex-centric computation
def update_vertex(id, attr, message):
    return min(attr, message)
```

---

## Edge Operations
![edge_operations](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/edge_operations.svg)

---

## Triplet Views
```python
# Process triplets
def process_triplet(triplet):
    return (triplet.src, triplet.dst, triplet.attr)
```

---

## Graph Algorithms
1. PageRank
1. Connected components
1. Shortest paths
1. Triangle counting

---

## PageRank Implementation
```python
# Run PageRank
results = g.pageRank(
    resetProbability=0.15,
    tol=0.01
)
```

---

## Connected Components
![connected_components](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/connected_components.svg)

---

## Shortest Paths
```python
# Compute shortest paths
paths = g.shortestPaths(
    landmarks=["A", "B"]
)
```

---

## Triangle Counting
![triangle_counting](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/triangle_counting.svg)

---

## Graph Algorithms API
1. Built-in algorithms
1. Custom algorithms
1. Algorithm composition
1. Result handling

---

## Custom Algorithms
```python
def custom_graph_algo(graph):
    # Algorithm implementation
    return processed_graph
```

---

## Pregel API
![pregel_api](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/pregel_api.svg)

---

## Message Passing
1. Send messages
1. Receive messages
1. Update state
1. Converge

---

## Iterative Computation
```python
# Iterative process
for i in range(max_iterations):
    messages = send_messages(graph)
    graph = update_vertices(graph, messages)
```

---

## Graph Partitioning
![graph_partitioning](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/graph_partitioning.svg)

---

## Partition Strategies
1. Random partitioning
1. Edge partitioning
1. Vertex partitioning
1. Custom strategies

---

## Performance Tuning
```python
# Configure partitioning
graph = graph.partitionBy(
    "EdgePartition2D",
    numPartitions=100
)
```

---

## Memory Management
![memory_management](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/memory_management.svg)

---

## Caching Strategies
1. Cache vertices
1. Cache edges
1. Cache graphs
1. Persistence levels

---

## Graph Views
```python
# Create subgraph
subgraph = graph.filter(
    vertex_pred=lambda v: v.age > 30
)
```

---

## Graph Metrics
![graph_metrics](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/graph_metrics.svg)

---

## Graph Analytics
1. Degree distribution
1. Centrality measures
1. Clustering coefficient
1. Path analysis

---

## Visualization
```python
# Export for visualization
def export_graph(graph, path):
    graph.write.format("graphml").save(path)
```

---

## Graph Formats
![graph_formats](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/graph_formats.svg)

---

## Data Integration
1. Load from files
1. Database integration
1. Streaming graphs
1. External sources

---

## Graph ETL
```python
# Transform graph data
def transform_graph(data):
    vertices = extract_vertices(data)
    edges = extract_edges(data)
    return create_graph(vertices, edges)
```

---

## Security Considerations
![security_considerations](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/security_considerations.svg)

---

## Production Deployment
1. Resource allocation
1. Monitoring setup
1. Error handling
1. Recovery strategies

---

## Monitoring
```python
# Monitor metrics
def track_metrics(graph):
    vertices = graph.vertices.count()
    edges = graph.edges.count()
    log_metrics(vertices, edges)
```

---

## Error Handling
![error_handling](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/error_handling.svg)

---

## Best Practices
1. Efficient partitioning
1. Memory management
1. Algorithm selection
1. Data structure choice

---

## Common Patterns
```python
# Common graph pattern
def process_graph_pattern(graph):
    components = graph.connectedComponents()
    return analyze_components(components)
```

---

## Advanced Features
![advanced_features](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/advanced_features.svg)

---

## Integration Patterns
1. ML pipelines
1. Streaming systems
1. Storage systems
1. Analysis tools

---

## Performance Analysis
```python
# Analyze performance
def analyze_performance(graph):
    metrics = compute_metrics(graph)
    return optimize_graph(graph, metrics)
```

---

## Optimization Techniques
![optimization_techniques](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/optimization_techniques.svg)

---

## Future Developments
1. Enhanced algorithms
1. Better performance
1. New features
1. Tool integration

---

## Case Studies
```python
# Real-world example
def social_network_analysis(graph):
    communities = detect_communities(graph)
    influence = compute_influence(graph)
    return analyze_results(communities, influence)
```

---

## Production Checklist
![production_checklist](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/production_checklist.svg)

---

## Additional Resources
* Official documentation
* Research papers
* Community guides
* Example projects

---

## Full Program: Social Network Analysis with GraphFrames

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from graphframes import GraphFrame

spark = SparkSession.builder \
    .appName("SocialNetworkAnalysis") \
    .config("spark.jars.packages",
            "graphframes:graphframes:0.8.3-spark3.5-s_2.12") \
    .getOrCreate()

# Create vertices (users)
vertices = spark.createDataFrame([
    ("1", "Alice", 28, "Engineering"),
    ("2", "Bob", 35, "Marketing"),
    ("3", "Charlie", 42, "Engineering"),
    ("4", "Diana", 31, "Sales"),
    ("5", "Eve", 26, "Engineering"),
    ("6", "Frank", 38, "Marketing"),
    ("7", "Grace", 29, "Sales"),
    ("8", "Hank", 45, "Management"),
    ("9", "Ivy", 33, "Engineering"),
    ("10", "Jack", 27, "Marketing"),
], ["id", "name", "age", "department"])
```

---

## Social Network: Edges and Graph Stats

```python
# Create edges (relationships)
edges = spark.createDataFrame([
    ("1", "2", "friend"), ("1", "3", "colleague"),
    ("1", "5", "colleague"), ("2", "4", "friend"),
    ("2", "6", "colleague"), ("3", "5", "colleague"),
    ("3", "8", "reports_to"), ("4", "7", "friend"),
    ("5", "9", "colleague"), ("6", "10", "colleague"),
    ("7", "8", "reports_to"), ("8", "3", "manages"),
    ("9", "1", "colleague"), ("10", "2", "colleague"),
    ("3", "9", "colleague"), ("5", "3", "colleague"),
], ["src", "dst", "relationship"])

# Create graph
g = GraphFrame(vertices, edges)

# Basic graph stats
print(f"Vertices: {g.vertices.count()}")
print(f"Edges: {g.edges.count()}")

# Degree analysis
in_degrees = g.inDegrees.orderBy("inDegree", ascending=False)
out_degrees = g.outDegrees.orderBy("outDegree", ascending=False)
degrees = g.degrees.orderBy("degree", ascending=False)

print("\nMost connected users:")
degrees.join(vertices, "id").select(
    "name", "department", "degree"
).show()
```

---

## Graph Structure Visualization

![graph_structure_visualization](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/graph_structure_visualization.svg)

---

## Full Program: PageRank with GraphFrames

```python
# Run PageRank algorithm
pr_results = g.pageRank(
    resetProbability=0.15,
    maxIter=20
)

# Show PageRank scores
print("PageRank Results:")
pr_results.vertices.select(
    "id", "name", "department", "pagerank"
).orderBy("pagerank", ascending=False).show()

# Connected components
cc = g.connectedComponents()
print("\nConnected Components:")
cc.select("id", "name", "component").show()

# Strongly connected components
scc = g.stronglyConnectedComponents(maxIter=10)
print("\nStrongly Connected Components:")
scc.select("id", "name", "component").show()
```

---

## PageRank: Triangles and Communities

```python
# Triangle counting
triangles = g.triangleCount()
print("\nTriangle Count per vertex:")
triangles.select("id", "name", "count") \
    .orderBy("count", ascending=False).show()

# Label propagation (community detection)
communities = g.labelPropagation(maxIter=5)
print("\nCommunities (Label Propagation):")
communities.select("id", "name", "department", "label") \
    .orderBy("label").show()
```

---

## PageRank Algorithm Explanation

![pagerank_algorithm_explanation](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/pagerank_algorithm_explanation.svg)

---

## Full Program: Motif Finding (Pattern Matching)

```python
# Find specific patterns in the graph

# Pattern: Find friend-of-friend relationships
fof = g.find("(a)-[e1]->(b); (b)-[e2]->(c)")

# Filter to only "friend" relationships
friend_of_friend = (
    fof
    .filter("e1.relationship = 'friend'")
    .filter("e2.relationship = 'friend'")
    .filter("a.id != c.id")  # Exclude self-loops
    .select(
        F.col("a.name").alias("person"),
        F.col("b.name").alias("mutual_friend"),
        F.col("c.name").alias("suggested_friend"),
    )
)

print("Friend-of-Friend Suggestions:")
friend_of_friend.distinct().show()
```

---

## Motif Finding: Reporting Chains and Triangles

```python
# Pattern: Find reporting chains (A manages B reports_to C)
chains = g.find("(mgr)-[e1]->(emp); (emp)-[e2]->(boss)")
reporting_chains = (
    chains
    .filter("e1.relationship = 'manages'")
    .filter("e2.relationship = 'reports_to'")
    .select(
        F.col("mgr.name").alias("manager"),
        F.col("emp.name").alias("employee"),
        F.col("boss.name").alias("boss"),
    )
)
print("Reporting Chains:")
reporting_chains.show()

# Pattern: Find triangles (mutual connections)
triangles_motif = g.find("(a)-[]->(b); (b)-[]->(c); (c)-[]->(a)")
print(f"Number of triangle patterns: {triangles_motif.count()}")
```

---

## Graph Algorithms Comparison

| Algorithm | Complexity | Use Case | Distributed? |
|---|---|---|---|
| PageRank | O(V + E) per iter | Node importance | Yes |
| Connected Components | O(V + E) | Cluster detection | Yes |
| Shortest Paths | O(V * E) | Route finding | Yes |
| Triangle Count | O(E^1.5) | Network density | Yes |
| Label Propagation | O(E) per iter | Community detection | Yes |
| BFS | O(V + E) | Reachability | Yes |

---

## Full Program: Shortest Paths

```python
# Compute shortest paths from all vertices to landmarks
landmarks = ["1", "8"]  # Alice and Hank
sp = g.shortestPaths(landmarks=landmarks)

print("Shortest Paths to Alice(1) and Hank(8):")
sp.select("id", "name", "distances").show(truncate=False)

# Custom BFS: Find all users within N hops
bfs_result = g.bfs(
    fromExpr="id = '1'",  # Start from Alice
    toExpr="department = 'Management'",  # Find managers
    maxPathLength=3
)

print("\nPath from Alice to Management:")
bfs_result.show(truncate=False)

# Find paths between specific vertices
paths = g.bfs(
    fromExpr="name = 'Alice'",
    toExpr="name = 'Hank'",
    edgeFilter="relationship != 'friend'",
    maxPathLength=4
)
print("\nAlice to Hank (non-friend paths):")
paths.show(truncate=False)
```

---

## Full Program: Fraud Detection with Graph Analysis

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from graphframes import GraphFrame

spark = SparkSession.builder \
    .appName("FraudDetectionGraph") \
    .getOrCreate()

# Vertices: accounts
accounts = spark.createDataFrame([
    ("A001", "personal", "US", 50000.0),
    ("A002", "personal", "US", 12000.0),
    ("A003", "business", "UK", 500000.0),
    ("A004", "personal", "RU", 8000.0),
    ("A005", "shell", "CY", 1000000.0),
    ("A006", "personal", "US", 25000.0),
    ("A007", "business", "DE", 200000.0),
    ("A008", "personal", "CN", 15000.0),
], ["id", "account_type", "country", "balance"])

# Edges: transactions
transactions = spark.createDataFrame([
    ("A001", "A002", 5000.0, "2024-01-15"),
    ("A002", "A005", 4500.0, "2024-01-15"),  # Suspicious
    ("A005", "A004", 4000.0, "2024-01-16"),  # Suspicious
    ("A004", "A008", 3500.0, "2024-01-16"),  # Suspicious
    ("A003", "A007", 50000.0, "2024-01-17"),
    ("A006", "A001", 2000.0, "2024-01-18"),
    ("A001", "A003", 10000.0, "2024-01-19"),
    ("A005", "A008", 100000.0, "2024-01-20"),  # Suspicious
], ["src", "dst", "amount", "date"]).toDF(
    "src", "dst", "amount", "date"
)

g = GraphFrame(accounts, transactions)
```

---

## Fraud Detection: Circular Money Flows

```python
# 1. Detect circular money flows (layering)
circular = g.find("(a)-[e1]->(b); (b)-[e2]->(c); (c)-[e3]->(a)")
print("Circular flows (potential layering):")
circular.select(
    F.col("a.id").alias("start"),
    F.col("b.id").alias("middle"),
    F.col("c.id").alias("end"),
    F.col("e1.amount").alias("amount_1"),
    F.col("e2.amount").alias("amount_2"),
    F.col("e3.amount").alias("amount_3"),
).show()

# 2. Find rapid pass-through accounts
# (receive and send similar amounts quickly)
pass_through = g.find("(a)-[e1]->(b); (b)-[e2]->(c)")
suspicious_passthrough = (
    pass_through
    .filter("e2.amount > e1.amount * 0.8")
    .filter("e2.amount < e1.amount * 1.0")
    .filter("datediff(e2.date, e1.date) <= 1")
    .select(
        F.col("a.id").alias("source"),
        F.col("b.id").alias("pass_through_account"),
        F.col("c.id").alias("destination"),
        F.col("e1.amount").alias("in_amount"),
        F.col("e2.amount").alias("out_amount"),
    )
)
print("Suspicious pass-through accounts:")
suspicious_passthrough.show()
```

---

## Fraud Detection: Risk Scoring with PageRank

```python
# 3. Risk scoring using PageRank
# Higher PageRank = more money flowing through
pr = g.pageRank(resetProbability=0.15, maxIter=10)
risk_scores = (
    pr.vertices
    .withColumn("risk_score",
        F.when(F.col("account_type") == "shell", F.col("pagerank") * 3)
        .when(F.col("country").isin("CY", "PA", "VG"),
              F.col("pagerank") * 2)
        .otherwise(F.col("pagerank"))
    )
    .orderBy("risk_score", ascending=False)
)
print("Account Risk Scores:")
risk_scores.select("id", "account_type", "country",
    "pagerank", "risk_score").show()
```

---

## Graph Partitioning Strategies

| Strategy | How it Works | Best For |
|---|---|---|
| Random | Hash vertex IDs | General purpose |
| EdgePartition1D | Partition by source | High out-degree graphs |
| EdgePartition2D | 2D grid on (src,dst) | Balanced edge distribution |
| Canonical Random | Consistent edge placement | Undirected graphs |
| Range | By vertex ID range | Ordered ID graphs |

---

## Performance Tuning for Graph Processing

```python
# Memory configuration for graph workloads
spark.conf.set("spark.executor.memory", "16g")
spark.conf.set("spark.executor.memoryOverhead", "4g")
spark.conf.set("spark.memory.fraction", "0.8")

# Graph-specific tuning
spark.conf.set("spark.graphx.pregel.checkpointInterval", "10")

# Checkpoint for iterative algorithms
spark.sparkContext.setCheckpointDir("/tmp/graph_checkpoints/")

# Cache graph for multiple operations
g.vertices.cache()
g.edges.cache()

# Partition graph for better parallelism
vertices_partitioned = vertices.repartition(100, "id")
edges_partitioned = edges.repartition(100, "src")

g_optimized = GraphFrame(vertices_partitioned, edges_partitioned)

# For very large graphs, persist intermediate results
pr_results = g_optimized.pageRank(resetProbability=0.15, maxIter=5)
pr_results.vertices.persist()
pr_results.vertices.count()  # Trigger caching
```

---

## Real-World Graph Applications

![real_world_graph_applications](svg/courses/big_data/advanced-spark-with-python/05_graph_processing_graphx/real_world_graph_applications.svg)
