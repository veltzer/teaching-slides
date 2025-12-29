# Spark Optimization and Tuning

## Performance Overview

1. Memory Management
1. CPU Utilization
1. I/O Operations
1. Network Usage
1. Resource Allocation

---

## Performance Factors

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Performance</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Memory Architecture

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">JVM Heap</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Memory Distribution

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Total Memory</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Memory Configuration

```scala
spark.conf.set("spark.memory.fraction", 0.75)
spark.conf.set("spark.memory.storageFraction", 0.5)
spark.conf.set("spark.driver.memory", "4g")
spark.conf.set("spark.executor.memory", "4g")
```

---

## Executor Configuration

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Executor</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Resource Planning

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Resources</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Data Serialization

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Serialization</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Serialization Setup

```scala
// Configure Kryo serialization
spark.conf.set("spark.serializer",
  "org.apache.spark.serializer.KryoSerializer")
// Register classes
spark.conf.set("spark.kryo.registrator",
  "MyRegistrator")
```

---

## Data Partitioning

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Data</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Partition Sizing

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Sizing Factors</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Shuffle Operations

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Map</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Shuffle Configuration

```scala
// Configure shuffle
spark.conf.set("spark.shuffle.file.buffer", "32k")
spark.conf.set("spark.reducer.maxSizeInFlight", "48m")
spark.conf.set("spark.shuffle.io.maxRetries", "3")
```

---

## Caching Strategy

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Cache Levels</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Cache Implementation

```scala
// Memory only
df.cache()
// Memory and disk
df.persist(StorageLevel.MEMORY_AND_DISK)
// Memory and disk serialized
df.persist(StorageLevel.MEMORY_AND_DISK_SER)
```

---

## SQL Optimization

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">SQL</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Join Optimization

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Joins</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Broadcast Implementation

```scala
import org.apache.spark.sql.functions.broadcast
val joinedDF = largeDF.join(
  broadcast(smallDF),
  Seq("key")
)
```

---

## Data Skew

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Skew</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Skew Handling

```scala
// Add random prefix
val saltedDF = df.withColumn(
  "salt",
  rand() * numPartitions
)
// Join with salt
val joinedDF = saltedDF.join(
  otherDF,
  Seq("key", "salt")
)
```

---

## Performance Monitoring

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Monitoring</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Spark UI Components

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Spark UI</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Metrics Collection

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Metrics</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Resource Utilization

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Resources</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Memory Tuning

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Memory Tuning</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## GC Optimization

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">GC</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Network Configuration

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Network</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Storage Optimization

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Storage</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Best Practices

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Best Practices</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Performance Checklist

1. Memory Configuration
1. Partition Sizing
1. Shuffle Management
1. Cache Strategy
1. Resource Allocation

---

## Troubleshooting

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Issues</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Production Deployment

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Deploy</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>
