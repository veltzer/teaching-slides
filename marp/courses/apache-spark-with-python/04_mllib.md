# Spark MLlib

---
## Introduction to Machine Learning

### What is Machine Learning?
- Automated pattern recognition
- Learning from data without explicit programming
- Making predictions or decisions based on data
- Types: Supervised, Unsupervised, and Reinforcement Learning

---
### MLlib Overview
![0](../../../out/mermaid/marp/courses/apache-spark-with-python/04_mllib.md/0.png)

---
## The MLlib API

### Key Components
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

### Basic Pipeline Structure
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

### Data Preprocessing
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
### Feature Transformations
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

### Classification
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
### Regression
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

### Clustering
```python
# K-means clustering
kmeans = KMeans(k=3, seed=1)
model = kmeans.fit(dataset)

# Gaussian Mixture Model
gmm = GaussianMixture(k=3)
model = gmm.fit(dataset)
```

---
### Dimensionality Reduction
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

### Metrics and Validation
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
### Cross Validation
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

### Customer Churn Prediction
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
### Recommendation System
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
### Text Classification
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

### Saving and Loading Models
```python
# Save model
model.save("path/to/model")

# Load model
from pyspark.ml.model import PipelineModel
loaded_model = PipelineModel.load("path/to/model")
```

---
### Model Serving
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

### Performance Optimization
```python
# Cache frequently used DataFrames
training_data.cache()

# Tune parallel processing
spark.conf.set("spark.sql.shuffle.partitions", "100")
```

---
### Model Monitoring
```python
# Track metrics over time
def log_metrics(predictions, timestamp):
    metrics = evaluator.evaluate(predictions)
    log_to_monitoring_system(metrics, timestamp)
```

---
### Pipeline Management
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
