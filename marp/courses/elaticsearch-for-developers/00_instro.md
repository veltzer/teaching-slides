# Elasticsearch for Developers

## Welcome to the Course

---

## Course Overview

1. **Duration**: 40 hours / 5 days
1. **Focus**: Developer perspective
1. **Approach**: Hands-on exercises
1. **Goal**: Integrate search into applications

---

## What We'll Build

1. Full-text search features
1. Analytics capabilities
1. Real-time data processing
1. Scalable search solutions

---

## Prerequisites Check

1. Programming experience (Java, Python, JavaScript)
1. Understanding of JSON format
1. RESTful API knowledge
1. Basic database concepts

---

## What is Elasticsearch?

A distributed, RESTful search and analytics engine capable of:
1. Storing petabytes of data
1. Searching in near real-time
1. Scaling horizontally
1. Analyzing complex data

---

## Why Elasticsearch?

<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="100" height="60" fill="#4CAF50" rx="5"/>
  <text x="100" y="85" text-anchor="middle" fill="white">Fast Search</text>
  <rect x="250" y="50" width="100" height="60" fill="#2196F3" rx="5"/>
  <text x="300" y="85" text-anchor="middle" fill="white">Scalable</text>
  <rect x="50" y="150" width="100" height="60" fill="#FF9800" rx="5"/>
  <text x="100" y="185" text-anchor="middle" fill="white">Real-time</text>
  <rect x="250" y="150" width="100" height="60" fill="#9C27B0" rx="5"/>
  <text x="300" y="185" text-anchor="middle" fill="white">Analytics</text>
</svg>

---

## Use Cases for Developers

1. **E-commerce**: Product search, recommendations
1. **Logging**: Application logs, metrics
1. **Content Management**: Document search
1. **Geospatial**: Location-based services

---

## Real-World Examples

1. **Wikipedia**: Full-text search
1. **GitHub**: Code search
1. **Stack Overflow**: Question search
1. **Uber**: Geospatial queries

---

## Elasticsearch vs Traditional Databases

| **Aspect** | **Elasticsearch** | **RDBMS** |
|------------|------------------|-----------|
| Schema | Flexible | Rigid |
| Search | Full-text | Basic |
| Speed | Milliseconds | Variable |
| Scaling | Horizontal | Vertical |

---

## Elasticsearch vs Other Search Engines

| **Feature** | **Elasticsearch** | **Solr** | **Algolia** |
|-------------|------------------|----------|-------------|
| Self-hosted | Yes | Yes | No |
| Real-time | Yes | Limited | Yes |
| Analytics | Excellent | Good | Basic |
| Cost | Open Source | Open Source | SaaS |

---

## Basic Architecture Concepts

<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
  <rect x="150" y="20" width="100" height="40" fill="#2196F3" rx="5"/>
  <text x="200" y="45" text-anchor="middle" fill="white">Cluster</text>
  <rect x="50" y="100" width="80" height="40" fill="#4CAF50" rx="5"/>
  <text x="90" y="125" text-anchor="middle" fill="white">Node 1</text>
  <rect x="160" y="100" width="80" height="40" fill="#4CAF50" rx="5"/>
  <text x="200" y="125" text-anchor="middle" fill="white">Node 2</text>
  <rect x="270" y="100" width="80" height="40" fill="#4CAF50" rx="5"/>
  <text x="310" y="125" text-anchor="middle" fill="white">Node 3</text>
  <rect x="50" y="180" width="60" height="30" fill="#FF9800" rx="3"/>
  <text x="80" y="200" text-anchor="middle" fill="white" font-size="12">Shard</text>
  <rect x="120" y="180" width="60" height="30" fill="#FF9800" rx="3"/>
  <text x="150" y="200" text-anchor="middle" fill="white" font-size="12">Shard</text>
  <rect x="190" y="180" width="60" height="30" fill="#FF9800" rx="3"/>
  <text x="220" y="200" text-anchor="middle" fill="white" font-size="12">Shard</text>
</svg>

---

## Cluster

1. Collection of one or more nodes
1. Identified by unique name
1. Holds all your data
1. Provides federated indexing and search

---

## Nodes

1. Single server instance
1. Part of a cluster
1. Stores data
1. Participates in cluster's indexing and search

---

## Indices

1. Collection of documents
1. Similar to database in RDBMS
1. Identified by name (lowercase)
1. Can have multiple types (deprecated)

---

## Shards

1. Subdivision of an index
1. Horizontal scaling unit
1. Each shard is a Lucene index
1. Primary and replica shards

---

## Documents

```json
{
  "_index": "products",
  "_id": "1",
  "_source": {
    "name": "Laptop",
    "price": 999.99,
    "category": "Electronics",
    "in_stock": true
  }
}
```

---

## Document Structure

1. **_index**: Where document lives
1. **_id**: Unique identifier
1. **_source**: Actual JSON data
1. **_version**: Version number

---

## Development Environment Setup

Choose your preferred setup:
1. Local installation
1. Docker container
1. Elasticsearch Cloud trial
1. Development tools

---

## Local Installation

```bash
# Download and extract
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.x.x.tar.gz
tar -xzf elasticsearch-8.x.x.tar.gz
cd elasticsearch-8.x.x/

# Start Elasticsearch
./bin/elasticsearch
```

---

## Docker Setup

```bash
# Pull image
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.x.x

# Run container
docker run -p 9200:9200 -p 9300:9300 \
  -e "discovery.type=single-node" \
  docker.elastic.co/elasticsearch/elasticsearch:8.x.x
```

---

## Verify Installation

```bash
curl -X GET "localhost:9200/"
```

Response:
```json
{
  "name" : "node-1",
  "cluster_name" : "elasticsearch",
  "version" : {
    "number" : "8.x.x"
  }
}
```

---

## Elasticsearch Cloud

1. Visit cloud.elastic.co
1. Start free trial (14 days)
1. Create deployment
1. Note credentials and endpoint

---

## Development Tools

1. **Kibana Dev Tools**: Interactive console
1. **Postman**: API testing
1. **cURL**: Command line
1. **Client libraries**: Language-specific

---

## Kibana Dev Tools

Most convenient for development:

```txt
GET /_cluster/health

POST /products/_doc
{
  "name": "Mouse",
  "price": 29.99
}
```

---

## RESTful API

All operations via HTTP:
1. `GET`: Retrieve data
1. `POST`: Create/Update
1. `PUT`: Create/Update with ID
1. `DELETE`: Remove data

---

## JSON Format

All data in JSON:
```json
{
  "field": "value",
  "number": 42,
  "boolean": true,
  "array": [1, 2, 3],
  "nested": {
    "key": "value"
  }
}
```

---

## Your First Index

```bash
PUT /my_first_index
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  }
}
```

---

## Index a Document

```bash
POST /my_first_index/_doc
{
  "title": "Hello Elasticsearch",
  "content": "This is my first document",
  "timestamp": "2024-01-01T10:00:00"
}
```

---

## Search for Documents

```bash
GET /my_first_index/_search
{
  "query": {
    "match": {
      "content": "document"
    }
  }
}
```

---

## Response Structure

```json
{
  "hits": {
    "total": { "value": 1 },
    "hits": [{
      "_index": "my_first_index",
      "_source": {
        "title": "Hello Elasticsearch",
        "content": "This is my first document"
      }
    }]
  }
}
```

---

## Course Structure

1. **Day 1**: Fundamentals & Data Modeling
1. **Day 2**: Search & Aggregations
1. **Day 3**: Advanced Features & `ES|QL`
1. **Day 4**: Performance & Integration
1. **Day 5**: Modern Features & Best Practices

---

## Learning Approach

1. Concept introduction
1. Live demonstrations
1. Hands-on exercises
1. Real-world scenarios

---

## Lab Environment

1. Each participant gets a cluster
1. Sample datasets provided
1. Exercise workbooks
1. Solution guides available

---

## Sample Datasets

1. **E-commerce**: Products, orders, reviews
1. **Logs**: Application logs, metrics
1. **Geo**: Store locations, routes
1. **Text**: Articles, documents

---

## Success Tips

1. **Practice**: Hands-on is key
1. **Experiment**: Try variations
1. **Ask Questions**: No question is too small
1. **Take Notes**: Document your learning

---

## Common Challenges

1. Understanding distributed nature
1. Query DSL syntax
1. Performance tuning
1. Data modeling decisions

---

## Resources

1. **Official Docs**: elastic.co/guide
1. **Forums**: discuss.elastic.co
1. **GitHub**: github.com/elastic
1. **Stack Overflow**: Tagged questions
