# Spark Internals: From Query to Execution

## Slide 1: The Journey of a Spark Query

When you submit a query (SQL or RDD), Spark follows these key steps:
1. Query parsing and optimization
1. DAG creation
1. Stage division
1. Task scheduling and execution
1. Data shuffling and aggregation

---

## Slide 2: Logical Planning

### Query Analysis
* SQL queries are parsed into an Abstract Syntax Tree (AST)
* RDD transformations create a lineage graph
* Both are converted into a logical plan
* Catalyst Optimizer applies optimization rules:
    * Predicate pushdown
    * Column pruning
    * Constant folding
    * Join reordering

---

## Slide 3: Physical Planning

### Converting Logic to Action
* Logical plan transforms into physical execution plan
* Multiple strategies evaluated for each operation
* Cost-based optimizer selects best implementation
* Examples of physical strategies:
    * Broadcast Hash Join vs. Shuffle Hash Join
    * Sort-Merge Join
    * Range Partitioning

---

## Slide 4: DAG and Stage Creation

### Breaking Down the Work
* Physical plan becomes a Directed Acyclic Graph (DAG)
* Stages are created at shuffle boundaries
* Each stage contains multiple tasks
* Example stage divisions:

  ```text
  Stage 1: Read + Filter + Project
  Shuffle
  Stage 2: Aggregate
  Shuffle
  Stage 3: Final Results
  ```

---

## Slide 5: Task Execution

### Parallel Processing in Action
* Each stage divided into tasks based on partitions
* Tasks are fundamental unit of parallelism
* Executor nodes:
    * Run tasks in parallel
    * Cache data in memory
    * Spill to disk if needed
* Task scheduling considers data locality

---

## Slide 6: Data Movement and Shuffling

### The Critical Path
* Shuffle operations move data between executors
* Types of data movement:
    * Narrow dependencies (no shuffle)
    * Wide dependencies (requires shuffle)
* Performance implications:
    * Network bandwidth usage
    * Disk I/O for spilling
    * Memory pressure

---

## Slide 7: Memory Management

### Keeping Data Close
* Memory hierarchy:
    * On-heap storage
    * Off-heap storage
    * Disk storage
* Memory regions:
    * Execution memory (shuffles, joins, sorts)
    * Storage memory (caching)
* Dynamic allocation between regions
* Eviction policies for cached data

---

## Slide 8: Why This Architecture Works

### Key Design Principles
* Lazy evaluation enables optimization
* Immutable RDDs provide fault tolerance
* In-memory processing reduces I/O
* Data locality optimizations
* Flexible execution plans
* Balance between memory and disk usage

---

## Slide 9: Performance Considerations

### Optimizing Your Queries
* Partition tuning affects parallelism
* Broadcast joins reduce shuffling
* Caching strategies matter
* Column pruning reduces I/O
* Predicate pushdown minimizes data movement
* Proper memory configuration crucial
