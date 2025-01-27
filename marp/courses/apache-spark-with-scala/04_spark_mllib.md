# Spark MLlib

## Introduction to Machine Learning

1. Supervised Learning
1. Unsupervised Learning
1. Model Training
1. Model Evaluation
1. Feature Engineering

## MLlib Components

![0](../../../out/mermaid/marp/courses/apache-spark-with-scala/04_spark_mllib.md/0.png)

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

## Feature Engineering

1. Tokenization
1. TF-IDF
1. Word2Vec
1. OneHotEncoding
1. StandardScaler

## Classification Algorithms

```scala
import org.apache.spark.ml.classification._
val lr = new LogisticRegression()
  .setMaxIter(10)
  .setRegParam(0.001)
val model = lr.fit(training)
val predictions = model.transform(test)
```

## Regression Models

```scala
import org.apache.spark.ml.regression._
val lr = new LinearRegression()
  .setMaxIter(10)
  .setRegParam(0.3)
  .setElasticNetParam(0.8)
val lrModel = lr.fit(training)
```

## Model Evaluation

```scala
import org.apache.spark.ml.evaluation._
val evaluator = new RegressionEvaluator()
  .setLabelCol("label")
  .setPredictionCol("prediction")
  .setMetricName("rmse")
val rmse = evaluator.evaluate(predictions)
```

## Pipeline Architecture

![1](../../../out/mermaid/marp/courses/apache-spark-with-scala/04_spark_mllib.md/1.png)

## ML Pipeline Example

```scala
val pipeline = new Pipeline()
  .setStages(Array(
    tokenizer,
    hashingTF,
    lr))
val model = pipeline.fit(training)
```

## Cross Validation

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

## Clustering

```scala
import org.apache.spark.ml.clustering._
val kmeans = new KMeans()
  .setK(2)
  .setSeed(1L)
val model = kmeans.fit(dataset)
```

## Model Save and Load

```scala
model.save("model_path")
val loadedModel = PipelineModel.load("model_path")
```

## Performance Optimization

1. Feature scaling
1. Parameter tuning
1. Cross-validation
1. Model selection
1. Performance metrics

## Best Practices

![2](../../../out/mermaid/marp/courses/apache-spark-with-scala/04_spark_mllib.md/2.png)

## Common Use Cases

1. Text Classification
1. Recommendation Systems
1. Anomaly Detection
1. Customer Segmentation
1. Predictive Maintenance
