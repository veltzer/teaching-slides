---
tags:
  - tools:spark
  - languages:scala
  - data-and-ai:big-data
  - data-and-ai:machine-learning
level: intermediate
category: big-data
audience:
  - audiences:developers

---

# Spark MLlib

---

## Introduction to Machine Learning

1. Supervised Learning
1. Unsupervised Learning
1. Model Training
1. Model Evaluation
1. Feature Engineering

---

## MLlib Architecture

![mllib_architecture](svg/courses/big_data/apache-spark-with-scala/05_spark_mllib/mllib_architecture.svg)

---

## Machine Learning Types

![machine_learning_types](svg/courses/big_data/apache-spark-with-scala/05_spark_mllib/machine_learning_types.svg)

---

## ML Pipeline Components

![ml_pipeline_components](svg/courses/big_data/apache-spark-with-scala/05_spark_mllib/ml_pipeline_components.svg)

---

## Data Preparation

```scala
import org.apache.spark.ml.feature._
val tokenizer = new Tokenizer()
  .setInputCol("text")
  .setOutputCol("words")
val hashingTF = new HashingTF()
  .setInputCol("words")
  .setOutputCol("features")
```

---

## Feature Engineering Flow

![feature_engineering_flow](svg/courses/big_data/apache-spark-with-scala/05_spark_mllib/feature_engineering_flow.svg)

---

## Feature Types

1. Numerical Features
1. Categorical Features
1. Text Features
1. Custom Features
1. Combined Features

---

## Feature Transformations

![feature_transformations](svg/courses/big_data/apache-spark-with-scala/05_spark_mllib/feature_transformations.svg)

---

## Classification Architecture

![classification_architecture](svg/courses/big_data/apache-spark-with-scala/05_spark_mllib/classification_architecture.svg)

---

## Classification Implementation

```scala
import org.apache.spark.ml.classification._
val lr = new LogisticRegression()
  .setMaxIter(10)
  .setRegParam(0.001)
val model = lr.fit(training)
val predictions = model.transform(test)
```

---

## Regression Models

![regression_models](svg/courses/big_data/apache-spark-with-scala/05_spark_mllib/regression_models.svg)

---

## Regression Implementation

```scala
import org.apache.spark.ml.regression._
val lr = new LinearRegression()
  .setMaxIter(10)
  .setRegParam(0.3)
  .setElasticNetParam(0.8)
val lrModel = lr.fit(training)
```

---

## Model Evaluation Flow

![model_evaluation_flow](svg/courses/big_data/apache-spark-with-scala/05_spark_mllib/model_evaluation_flow.svg)

---

## Evaluation Metrics

```scala
import org.apache.spark.ml.evaluation._
val evaluator = new RegressionEvaluator()
  .setLabelCol("label")
  .setPredictionCol("prediction")
  .setMetricName("rmse")
val rmse = evaluator.evaluate(predictions)
```

---

## Cross Validation

![cross_validation](svg/courses/big_data/apache-spark-with-scala/05_spark_mllib/cross_validation.svg)

---

## Pipeline Architecture

![pipeline_architecture](svg/courses/big_data/apache-spark-with-scala/05_spark_mllib/pipeline_architecture.svg)

---

## ML Pipeline Example

```scala
val pipeline = new Pipeline()
  .setStages(Array(
    tokenizer,
    hashingTF,
    lr))
val model = pipeline.fit(training)
```

---

## Hyperparameter Tuning

![hyperparameter_tuning](svg/courses/big_data/apache-spark-with-scala/05_spark_mllib/hyperparameter_tuning.svg)

---

## Cross Validation Setup

```scala
val paramGrid = new ParamGridBuilder()
  .addGrid(lr.regParam, Array(0.1, 0.01))
  .addGrid(lr.maxIter, Array(10, 20))
  .build()
val cv = new CrossValidator()
  .setEstimator(pipeline)
  .setEvaluator(evaluator)
  .setEstimatorParamMaps(paramGrid)
  .setNumFolds(3)
```

---

## Clustering Architecture

![clustering_architecture](svg/courses/big_data/apache-spark-with-scala/05_spark_mllib/clustering_architecture.svg)

---

## Clustering Implementation

```scala
import org.apache.spark.ml.clustering._
val kmeans = new KMeans()
  .setK(2)
  .setSeed(1L)
val model = kmeans.fit(dataset)
```

---

## Model Persistence

![model_persistence](svg/courses/big_data/apache-spark-with-scala/05_spark_mllib/model_persistence.svg)

---

## Model Save and Load

```scala
model.save("model_path")
val loadedModel = PipelineModel.load("model_path")
```

---

## Performance Optimization

![performance_optimization](svg/courses/big_data/apache-spark-with-scala/05_spark_mllib/performance_optimization.svg)

---

## Best Practices

![best_practices](svg/courses/big_data/apache-spark-with-scala/05_spark_mllib/best_practices.svg)

---

## Model Deployment Flow

![model_deployment_flow](svg/courses/big_data/apache-spark-with-scala/05_spark_mllib/model_deployment_flow.svg)

---

## Common Use Cases

1. Text Classification
1. Recommendation Systems
1. Anomaly Detection
1. Customer Segmentation
1. Predictive Maintenance

---

## Advanced Topics

![advanced_topics](svg/courses/big_data/apache-spark-with-scala/05_spark_mllib/advanced_topics.svg)
