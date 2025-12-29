# Spark MLlib

## Introduction to Machine Learning

---
## What is Machine Learning
- Automated pattern recognition
- Learning from data without explicit programming
- Making predictions or decisions based on data
- Types: Supervised, Unsupervised, and Reinforcement Learning

---
## MLlib Overview
<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <!-- Data Sources -->
  <rect x="50" y="50" width="150" height="60" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="125" y="85" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Data Sources</text>

  <!-- Feature Engineering -->
  <rect x="280" y="50" width="180" height="60" rx="5" fill="#d4edda" stroke="#28a745" stroke-width="2"/>
  <text x="370" y="85" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Feature Engineering</text>

  <!-- Algorithm Selection -->
  <rect x="540" y="50" width="180" height="60" rx="5" fill="#fff3cd" stroke="#ffc107" stroke-width="2"/>
  <text x="630" y="85" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Algorithm Selection</text>

  <!-- Model Training -->
  <rect x="540" y="180" width="180" height="60" rx="5" fill="#cce5ff" stroke="#007bff" stroke-width="2"/>
  <text x="630" y="215" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Model Training</text>

  <!-- Model Evaluation -->
  <rect x="540" y="310" width="180" height="60" rx="5" fill="#f8d7da" stroke="#dc3545" stroke-width="2"/>
  <text x="630" y="345" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Model Evaluation</text>

  <!-- Prediction -->
  <rect x="540" y="440" width="180" height="60" rx="5" fill="#e2d5f1" stroke="#6f42c1" stroke-width="2"/>
  <text x="630" y="475" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Prediction</text>

  <!-- Model Tuning -->
  <rect x="280" y="310" width="180" height="60" rx="5" fill="#ffeaa7" stroke="#fdcb6e" stroke-width="2"/>
  <text x="370" y="345" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Model Tuning</text>

  <!-- Arrows -->
  <defs>
    <marker id="arrow9" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>

  <!-- Data Sources to Feature Engineering -->
  <line x1="200" y1="80" x2="280" y2="80" stroke="#666" stroke-width="2" marker-end="url(#arrow9)"/>

  <!-- Feature Engineering to Algorithm Selection -->
  <line x1="460" y1="80" x2="540" y2="80" stroke="#666" stroke-width="2" marker-end="url(#arrow9)"/>

  <!-- Algorithm Selection to Model Training -->
  <line x1="630" y1="110" x2="630" y2="180" stroke="#666" stroke-width="2" marker-end="url(#arrow9)"/>

  <!-- Model Training to Model Evaluation -->
  <line x1="630" y1="240" x2="630" y2="310" stroke="#666" stroke-width="2" marker-end="url(#arrow9)"/>

  <!-- Model Evaluation to Prediction -->
  <line x1="630" y1="370" x2="630" y2="440" stroke="#666" stroke-width="2" marker-end="url(#arrow9)"/>

  <!-- Model Evaluation to Model Tuning -->
  <line x1="540" y1="340" x2="460" y2="340" stroke="#666" stroke-width="2" marker-end="url(#arrow9)"/>

  <!-- Model Tuning back to Model Training (feedback loop) -->
  <path d="M 370 310 Q 370 210 540 210" fill="none" stroke="#666" stroke-width="2" marker-end="url(#arrow9)"/>
</svg>

---
## The MLlib API

## Key Components
1. Transformers
    - Transform one DataFrame to another
    - Implement transform() method
1. Estimators
    - Algorithm that can be fit on data
    - Implement fit() method
1. Pipelines
    - Chain multiple transformers and estimators
1. Parameters
    - Shared interface for all ML components

---

## Basic Pipeline Structure

```python
from pyspark.ml import Pipeline
from pyspark.ml.feature import *
from pyspark.ml.classification import *
from pyspark.ml.evaluation import *

# Create pipeline stages
tokenizer = Tokenizer(inputCol="text", outputCol="words")
hashingTF = HashingTF(inputCol="words", outputCol="features")
lr = LogisticRegression(labelCol="label", featuresCol="features")

# Build pipeline
pipeline = Pipeline(stages=[tokenizer, hashingTF, lr])
```

---
## Feature Engineering

## Data Preprocessing

```python
# Handling missing values
from pyspark.ml.feature import Imputer

imputer = Imputer(
    inputCols=["age", "income"],
    outputCols=["age_imputed", "income_imputed"]
)

# Scaling features
from pyspark.ml.feature import StandardScaler

scaler = StandardScaler(
    inputCol="features",
    outputCol="scaledFeatures",
    withStd=True,
    withMean=True
)
```

---
## Feature Transformations

```python
# One-hot encoding
encoder = OneHotEncoder(
    inputCols=["categoryIndex"],
    outputCols=["categoryVec"]
)

# Text processing
tokenizer = Tokenizer(inputCol="text", outputCol="words")
hashingTF = HashingTF(inputCol="words", outputCol="features")

# Vector assembly
assembler = VectorAssembler(
    inputCols=["age", "income", "categoryVec"],
    outputCol="features"
)
```

---
## Supervised Learning

## Classification

```python
# Logistic Regression
lr = LogisticRegression(
    maxIter=10,
    regParam=0.001,
    elasticNetParam=0.8,
    labelCol="label",
    featuresCol="features"
)

# Random Forest
rf = RandomForestClassifier(
    numTrees=100,
    maxDepth=5,
    labelCol="label",
    featuresCol="features"
)

# Model training
model = pipeline.fit(training_data)
predictions = model.transform(test_data)
```

---
## Regression

```python
# Linear Regression
lr = LinearRegression(
    maxIter=10,
    regParam=0.3,
    elasticNetParam=0.8
)

# Decision Tree Regression
dt = DecisionTreeRegressor(
    maxDepth=5,
    featuresCol="features",
    labelCol="label"
)
```

---
## Unsupervised Learning

## Clustering

```python
# K-means clustering
kmeans = KMeans(k=3, seed=1)
model = kmeans.fit(dataset)

# Gaussian Mixture Model
gmm = GaussianMixture(k=3)
model = gmm.fit(dataset)
```

---
## Dimensionality Reduction

```python
# PCA
pca = PCA(k=3, inputCol="features", outputCol="pcaFeatures")

# Word2Vec
word2Vec = Word2Vec(
    vectorSize=3,
    minCount=0,
    inputCol="words",
    outputCol="result"
)
```

---
## Model Evaluation

## Metrics and Validation

```python
# Binary classification evaluation
evaluator = BinaryClassificationEvaluator(
    labelCol="label",
    rawPredictionCol="rawPrediction",
    metricName="areaUnderROC"
)

# Regression evaluation
evaluator = RegressionEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="rmse"
)
```

---
## Cross Validation

```python
# Create parameter grid
paramGrid = ParamGridBuilder() \
    .addGrid(lr.regParam, [0.1, 0.01]) \
    .addGrid(lr.maxIter, [10, 100]) \
    .build()

# Cross validation
crossval = CrossValidator(
    estimator=pipeline,
    estimatorParamMaps=paramGrid,
    evaluator=evaluator,
    numFolds=3
)

# Train with cross validation
cvModel = crossval.fit(training_data)
```

---
## Real-World Use Cases

## Customer Churn Prediction

```python
# Feature preparation
assembler = VectorAssembler(
    inputCols=["usage_time", "bill_amount", "support_calls"],
    outputCol="features"
)

# Model pipeline
pipeline = Pipeline(stages=[
    assembler,
    StandardScaler(inputCol="features", outputCol="scaled_features"),
    LogisticRegression(
        featuresCol="scaled_features",
        labelCol="churned"
    )
])
```

---
## Recommendation System

```python
# Collaborative filtering
als = ALS(
    maxIter=5,
    regParam=0.01,
    userCol="userId",
    itemCol="movieId",
    ratingCol="rating"
)

# Train model
model = als.fit(ratings)
predictions = model.transform(test_ratings)
```

---
## Text Classification

```python
# Text processing pipeline
pipeline = Pipeline(stages=[
    Tokenizer(inputCol="text", outputCol="words"),
    StopWordsRemover(inputCol="words", outputCol="filtered"),
    HashingTF(inputCol="filtered", outputCol="features"),
    LogisticRegression(labelCol="category")
])
```

---
## Model Deployment

## Saving and Loading Models

```python
# Save model
model.save("path/to/model")

# Load model
from pyspark.ml.model import PipelineModel
loaded_model = PipelineModel.load("path/to/model")
```

---
## Model Serving

```python
# Batch predictions
predictions = model.transform(new_data)

# Streaming predictions
def process_stream(df, epoch_id):
    predictions = model.transform(df)
    predictions.write.save("predictions")

streaming_data.foreachBatch(process_stream)
```

---
## Best Practices

## Performance Optimization

```python
# Cache frequently used DataFrames
training_data.cache()

# Tune parallel processing
spark.conf.set("spark.sql.shuffle.partitions", "100")
```

---
## Model Monitoring

```python
# Track metrics over time
def log_metrics(predictions, timestamp):
    metrics = evaluator.evaluate(predictions)
    log_to_monitoring_system(metrics, timestamp)
```

---
## Pipeline Management

```python
# Custom transformer
class CustomFeatureTransformer(Transformer):
    def __init__(self):
        super(CustomFeatureTransformer, self).__init__()

    def _transform(self, dataset):
        return dataset.withColumn("new_feature", ...)
```

---
## Summary
- MLlib provides scalable ML algorithms
- Pipeline API for end-to-end ML workflows
- Rich set of features for data preprocessing
- Support for model evaluation and tuning
- Easy model deployment and serving
