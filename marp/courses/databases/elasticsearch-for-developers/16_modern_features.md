# Modern Search Features

## Vector Search, Machine Learning, and Beyond

---

## Modern Search Evolution

![modern_search_evolution](svg/courses/databases/elasticsearch-for-developers/16_modern_features/modern_search_evolution.svg)

---

## Vector Search Overview

Vector search enables:
1. Semantic similarity search
1. Image and audio search
1. Recommendation systems
1. Natural language queries
1. Cross-lingual search

---

## Dense Vectors

```json
PUT /products
{
  "mappings": {
    "properties": {
      "name": {"type": "text"},
      "description_vector": {
        "type": "dense_vector",
        "dims": 768,
        "index": true,
        "similarity": "cosine"
      }
    }
  }
}
```

---

## Vector Similarity Metrics

```json
{
  "mappings": {
    "properties": {
      "embedding": {
        "type": "dense_vector",
        "dims": 512,
        "index": true,
        "similarity": "dot_product"  // or "l2_norm", "cosine"
      }
    }
  }
}
```

Options:
1. **cosine**: Angle between vectors
1. **dot_product**: Magnitude and direction
1. **l2_norm**: Euclidean distance

---

## Indexing Vectors

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def index_with_vectors(doc):
    # Generate embedding
    text = f"{doc['name']} {doc['description']}"
    vector = model.encode(text).tolist()

    # Index document with vector
    es.index(
        index="products",
        document={
            **doc,
            "description_vector": vector
        }
    )
```

---

## kNN Search

```json
GET /products/_search
{
  "knn": {
    "field": "description_vector",
    "query_vector": [0.1, 0.2, ..., 0.9],
    "k": 10,
    "num_candidates": 100
  }
}
```

---

## Approximate kNN

```json
{
  "mappings": {
    "properties": {
      "embedding": {
        "type": "dense_vector",
        "dims": 768,
        "index": true,
        "similarity": "cosine",
        "index_options": {
          "type": "hnsw",
          "m": 16,
          "ef_construction": 100
        }
      }
    }
  }
}
```

HNSW = Hierarchical Navigable Small World

---

## Hybrid Search

```json
{
  "query": {
    "bool": {
      "should": [
        {
          "match": {
            "title": {
              "query": "laptop computer",
              "boost": 1
            }
          }
        }
      ]
    }
  },
  "knn": {
    "field": "title_vector",
    "query_vector": [0.1, 0.2, ...],
    "k": 20,
    "boost": 0.5
  }
}
```

Combines keyword and vector search

---

## Reciprocal Rank Fusion

```python
def reciprocal_rank_fusion(results_lists, k=60):
    """Combine multiple result sets using RRF"""
    scores = {}

    for results in results_lists:
        for rank, doc in enumerate(results, 1):
            doc_id = doc['_id']
            if doc_id not in scores:
                scores[doc_id] = 0
            scores[doc_id] += 1 / (k + rank)

    # Sort by combined score
    return sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )
```

---

## Sparse Vectors

```json
PUT /documents
{
  "mappings": {
    "properties": {
      "content": {"type": "text"},
      "content_sparse": {
        "type": "sparse_vector"
      }
    }
  }
}

POST /documents/_doc
{
  "content": "machine learning algorithms",
  "content_sparse": {
    "1234": 0.8,  // term ID: weight
    "5678": 0.6,
    "9012": 0.4
  }
}
```

---

## Text Expansion

```json
{
  "query": {
    "text_expansion": {
      "ml.tokens": {
        "model_id": "elser_model",
        "model_text": "How to implement search?"
      }
    }
  }
}
```

Uses ELSER (Elastic Learned Sparse EncodeR)

---

## Machine Learning Features

```json
PUT _ml/trained_models/my-model
{
  "model_type": "pytorch",
  "inference_config": {
    "text_embedding": {
      "tokenization": {
        "bert": {
          "truncate": "first",
          "max_sequence_length": 512
        }
      },
      "embedding_size": 768
    }
  }
}
```

---

## Inference Processor

```json
PUT _ingest/pipeline/ml_pipeline
{
  "processors": [
    {
      "inference": {
        "model_id": "sentence-transformers__all-minilm-l6-v2",
        "target_field": "text_embedding",
        "field_map": {
          "text": "text_field"
        }
      }
    }
  ]
}
```

---

## Language Identification

```json
{
  "processors": [
    {
      "inference": {
        "model_id": "lang_ident_model_1",
        "inference_config": {
          "classification": {
            "num_top_classes": 3
          }
        },
        "field_map": {
          "text": "content"
        },
        "target_field": "language"
      }
    }
  ]
}
```

---

## Named Entity Recognition

```json
{
  "processors": [
    {
      "inference": {
        "model_id": "ner_model",
        "field_map": {
          "text": "content"
        },
        "target_field": "entities"
      }
    }
  ]
}

// Result:
{
  "entities": {
    "persons": ["John Doe", "Jane Smith"],
    "organizations": ["Elastic"],
    "locations": ["San Francisco"]
  }
}
```

---

## Sentiment Analysis

```python
def analyze_sentiment(text):
    response = es.ml.infer_trained_model(
        model_id="sentiment_model",
        docs=[{"text_field": text}]
    )

    return {
        "sentiment": response["inference_results"][0]["predicted_value"],
        "confidence": response["inference_results"][0]["prediction_probability"]
    }

# Result: {"sentiment": "positive", "confidence": 0.92}
```

---

## Text Classification

```json
PUT _ml/trained_models/category_classifier/_infer
{
  "docs": [
    {
      "text_field": "New laptop with 16GB RAM and SSD"
    }
  ]
}

// Response:
{
  "inference_results": [{
    "predicted_value": "electronics",
    "prediction_probability": 0.87,
    "top_classes": [
      {"class_name": "electronics", "probability": 0.87},
      {"class_name": "computers", "probability": 0.65}
    ]
  }]
}
```

---

## Question Answering

```python
def answer_question(question, context):
    response = es.ml.infer_trained_model(
        model_id="qa_model",
        docs=[{
            "question": question,
            "context": context
        }]
    )

    return {
        "answer": response["inference_results"][0]["predicted_value"],
        "start_pos": response["inference_results"][0]["start_offset"],
        "end_pos": response["inference_results"][0]["end_offset"],
        "confidence": response["inference_results"][0]["prediction_score"]
    }
```

---

## Semantic Search Implementation

```python
class SemanticSearch:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.es = Elasticsearch()

    def search(self, query, size=10):
        # Generate query vector
        query_vector = self.model.encode(query).tolist()

        # Hybrid search
        response = self.es.search(
            index="products",
            body={
                "query": {
                    "bool": {
                        "should": [
                            {
                                "match": {
                                    "title": {
                                        "query": query,
                                        "boost": 0.3
                                    }
                                }
                            }
                        ]
                    }
                },
                "knn": {
                    "field": "title_vector",
                    "query_vector": query_vector,
                    "k": size * 2,
                    "num_candidates": 100,
                    "boost": 0.7
                }
            }
        )

        return response
```

---

## Image Search

```python
from transformers import CLIPModel, CLIPProcessor

class ImageSearch:
    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    def index_image(self, image_path, doc_id):
        image = Image.open(image_path)
        inputs = self.processor(images=image, return_tensors="pt")

        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
            vector = image_features.numpy().flatten().tolist()

        self.es.index(
            index="images",
            id=doc_id,
            document={
                "image_path": image_path,
                "image_vector": vector
            }
        )

    def search_by_text(self, text_query):
        inputs = self.processor(text=text_query, return_tensors="pt")

        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)
            query_vector = text_features.numpy().flatten().tolist()

        return self.es.search(
            index="images",
            body={
                "knn": {
                    "field": "image_vector",
                    "query_vector": query_vector,
                    "k": 10
                }
            }
        )
```

---

## Cross-lingual Search

```python
class CrossLingualSearch:
    def __init__(self):
        # Multilingual model
        self.model = SentenceTransformer('distiluse-base-multilingual-cased-v2')

    def search_multilingual(self, query, source_lang='en'):
        # Encode query in any language
        query_vector = self.model.encode(query).tolist()

        # Search across all languages
        return self.es.search(
            index="multilingual_docs",
            body={
                "knn": {
                    "field": "content_vector",
                    "query_vector": query_vector,
                    "k": 20
                },
                "_source": ["title", "content", "language"]
            }
        )
```

---

## Personalized Search

```python
class PersonalizedSearch:
    def __init__(self):
        self.user_embeddings = {}

    def update_user_embedding(self, user_id, clicked_items):
        # Average embeddings of clicked items
        vectors = []
        for item_id in clicked_items:
            doc = self.es.get(index="products", id=item_id)
            vectors.append(doc["_source"]["embedding"])

        self.user_embeddings[user_id] = np.mean(vectors, axis=0)

    def personalized_search(self, user_id, query):
        user_vector = self.user_embeddings.get(user_id)

        if user_vector:
            # Blend query and user preference
            query_vector = self.encode_query(query)
            combined_vector = 0.7 * query_vector + 0.3 * user_vector
        else:
            combined_vector = self.encode_query(query)

        return self.search_with_vector(combined_vector)
```

---

## Learning to Rank

```json
{
  "query": {
    "match": {"title": "laptop"}
  },
  "rescore": {
    "window_size": 100,
    "query": {
      "rescore_query": {
        "sltr": {
          "model": "laptop_ranking_model",
          "active_features": [
            "title_match",
            "description_match",
            "popularity",
            "price_score"
          ]
        }
      }
    }
  }
}
```

---

## Feature Store for LTR

```python
class FeatureStore:
    def extract_features(self, query, document):
        features = {
            "title_match": self.calculate_bm25(query, document["title"]),
            "desc_match": self.calculate_bm25(query, document["description"]),
            "popularity": document.get("view_count", 0),
            "recency": self.calculate_recency(document["created_at"]),
            "price_band": self.categorize_price(document["price"]),
            "rating": document.get("avg_rating", 0),
            "in_stock": 1 if document["in_stock"] else 0,
            "query_length": len(query.split()),
            "title_length": len(document["title"].split())
        }
        return features

    def prepare_training_data(self, queries_with_clicks):
        X, y = [], []
        for query, clicked, not_clicked in queries_with_clicks:
            # Positive examples
            for doc in clicked:
                X.append(self.extract_features(query, doc))
                y.append(1)

            # Negative examples
            for doc in not_clicked[:5]:  # Sample negatives
                X.append(self.extract_features(query, doc))
                y.append(0)

        return np.array(X), np.array(y)
```

---

## Async Search

```json
POST /products/_async_search
{
  "size": 0,
  "aggs": {
    "expensive_analytics": {
      "terms": {
        "field": "category",
        "size": 1000
      },
      "aggs": {
        "stats": {
          "extended_stats": {"field": "price"}
        }
      }
    }
  }
}

// Check status
GET /_async_search/FmRldE8zRElCcVdrRmdKSUhGQ0wifQ==

// Get results when ready
GET /_async_search/FmRldE8zRElCcVdrRmdKSUhGQ0wifQ==?wait_for_completion_timeout=10s
```

---

## SQL Interface

```sql
POST /_sql?format=json
{
  "query": """
    SELECT category,
           COUNT(*) as product_count,
           AVG(price) as avg_price,
           MAX(price) as max_price
    FROM products
    WHERE in_stock = true
    GROUP BY category
    HAVING COUNT(*) > 10
    ORDER BY avg_price DESC
    LIMIT 10
  """
}
```

---

## JDBC/ODBC Drivers

```java
// Java JDBC example
String url = "jdbc:es://localhost:9200";
Properties props = new Properties();
props.put("user", "elastic");
props.put("password", "password");

Connection conn = DriverManager.getConnection(url, props);
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(
    "SELECT * FROM products WHERE price > 100"
);

while (rs.next()) {
    System.out.println(rs.getString("name"));
}
```

---

## GraphQL Integration

```javascript
const { GraphQLSchema, GraphQLObjectType } = require('graphql');

const ProductType = new GraphQLObjectType({
  name: 'Product',
  fields: {
    id: { type: GraphQLString },
    name: { type: GraphQLString },
    price: { type: GraphQLFloat },
    similar: {
      type: new GraphQLList(ProductType),
      resolve: async (parent) => {
        // Vector similarity search
        const response = await es.search({
          index: 'products',
          body: {
            knn: {
              field: 'embedding',
              query_vector: parent.embedding,
              k: 5
            }
          }
        });
        return response.hits.hits.map(hit => hit._source);
      }
    }
  }
});
```

---

## Recommendation Engine

```python
class RecommendationEngine:
    def collaborative_filtering(self, user_id):
        # Find similar users
        similar_users = self.find_similar_users(user_id)

        # Get their interactions
        recommendations = self.es.search(
            index="user_interactions",
            body={
                "query": {
                    "terms": {"user_id": similar_users}
                },
                "aggs": {
                    "popular_items": {
                        "terms": {
                            "field": "product_id",
                            "size": 20
                        }
                    }
                }
            }
        )

        return recommendations

    def content_based(self, product_id):
        # Get product vector
        product = self.es.get(index="products", id=product_id)
        vector = product["_source"]["embedding"]

        # Find similar products
        return self.es.search(
            index="products",
            body={
                "knn": {
                    "field": "embedding",
                    "query_vector": vector,
                    "k": 10,
                    "filter": {
                        "bool": {
                            "must_not": {"term": {"_id": product_id}}
                        }
                    }
                }
            }
        )
```

---

## Real-time Personalization

```python
class RealTimePersonalization:
    def __init__(self):
        self.session_embeddings = {}

    def update_session_context(self, session_id, action):
        if session_id not in self.session_embeddings:
            self.session_embeddings[session_id] = []

        # Add action embedding
        if action["type"] == "view":
            doc = self.get_document(action["product_id"])
            self.session_embeddings[session_id].append(
                doc["embedding"]
            )

        # Keep last 10 actions
        self.session_embeddings[session_id] = \
            self.session_embeddings[session_id][-10:]

    def get_personalized_results(self, session_id, query):
        # Combine query with session context
        query_vector = self.encode(query)

        if session_id in self.session_embeddings:
            context_vector = np.mean(
                self.session_embeddings[session_id],
                axis=0
            )
            final_vector = 0.6 * query_vector + 0.4 * context_vector
        else:
            final_vector = query_vector

        return self.vector_search(final_vector)
```

---

## Conversational Search

```python
class ConversationalSearch:
    def __init__(self):
        self.conversation_history = {}

    def process_query(self, user_id, query):
        # Get conversation context
        history = self.conversation_history.get(user_id, [])

        # Expand query with context
        expanded_query = self.expand_with_context(query, history)

        # Search
        results = self.semantic_search(expanded_query)

        # Update history
        history.append({"query": query, "expanded": expanded_query})
        self.conversation_history[user_id] = history[-5:]  # Keep last 5

        return results

    def expand_with_context(self, query, history):
        if not history:
            return query

        # Use NLP to resolve references
        context = " ".join([h["query"] for h in history[-3:]])

        # Resolve pronouns and references
        resolved = self.resolve_references(query, context)

        return resolved
```

---

## Voice Search

```python
import speech_recognition as sr

class VoiceSearch:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.search_engine = SemanticSearch()

    def search_by_voice(self, audio_file):
        # Convert speech to text
        with sr.AudioFile(audio_file) as source:
            audio = self.recognizer.record(source)
            text = self.recognizer.recognize_google(audio)

        # Handle voice-specific patterns
        text = self.normalize_spoken_query(text)

        # Semantic search
        return self.search_engine.search(text)

    def normalize_spoken_query(self, text):
        # Handle spoken patterns
        replacements = {
            "comma": ",",
            "period": ".",
            "dash": "-",
            "at sign": "@"
        }

        for spoken, symbol in replacements.items():
            text = text.replace(spoken, symbol)

        return text
```

---

## Performance Optimization

```python
class VectorSearchOptimizer:
    def optimize_index_settings(self):
        return {
            "index": {
                "knn": True,
                "knn.algo_param.ef_search": 100,
                "knn.algo_param.ef_construction": 200,
                "knn.algo_param.m": 16,
                "number_of_shards": 3,
                "number_of_replicas": 1
            }
        }

    def batch_vector_search(self, queries):
        # Batch multiple vector searches
        msearch_body = []

        for query_vector in queries:
            msearch_body.extend([
                {"index": "products"},
                {
                    "knn": {
                        "field": "embedding",
                        "query_vector": query_vector,
                        "k": 10
                    }
                }
            ])

        return self.es.msearch(body=msearch_body)
```

---

## Monitoring ML Models

```python
class ModelMonitor:
    def track_model_performance(self, model_id, predictions, actuals):
        metrics = {
            "model_id": model_id,
            "timestamp": datetime.now(),
            "accuracy": accuracy_score(actuals, predictions),
            "precision": precision_score(actuals, predictions),
            "recall": recall_score(actuals, predictions),
            "f1": f1_score(actuals, predictions),
            "drift_score": self.calculate_drift(predictions)
        }

        self.es.index(
            index="model_metrics",
            document=metrics
        )

        # Alert on performance degradation
        if metrics["accuracy"] < 0.8:
            self.send_alert(f"Model {model_id} accuracy below threshold")

    def calculate_drift(self, predictions):
        # Compare with baseline distribution
        baseline = self.get_baseline_distribution()
        current = np.histogram(predictions)[0]

        return wasserstein_distance(baseline, current)
```

---

## Future Trends

1. **Generative AI Integration**: LLMs for query understanding
1. **Multi-modal Search**: Text + Image + Audio
1. **Neural Search**: End-to-end learned retrieval
1. **Federated Learning**: Privacy-preserving ML
1. **Quantum Computing**: Future search algorithms

---

## Best Practices

1. Start with hybrid search (keyword + vector)
1. Choose appropriate vector dimensions
1. Monitor model performance continuously
1. Version your models and embeddings
1. Consider computational costs

---

## Common Challenges

1. Vector dimension selection
1. Model drift over time
1. Computational resource requirements
1. Cold start problems
1. Interpretability of results

---

## Next Steps

1. Best Practices and Common Pitfalls
1. Development workflow
1. Production considerations
1. Course wrap-up
