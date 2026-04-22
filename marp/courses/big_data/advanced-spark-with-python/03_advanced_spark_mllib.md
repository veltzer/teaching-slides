---
tags:
  - tools:spark
  - languages:python
  - data-and-ai:big-data
  - data-and-ai:machine-learning
level: advanced
category: big-data
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Advanced Spark MLlib

---
## Chapter Overview
* Scalable ML pipelines
* Advanced model training
* Hyperparameter tuning
* Model deployment
* Production considerations

---
## MLlib Architecture
![mllib_architecture](svg/courses/big_data/advanced-spark-with-python/03_advanced_spark_mllib/mllib_architecture.svg)

---
## Pipeline Components
1. Feature transformers
1. Estimators
1. Evaluators
1. Model persistence

---
## Data Preparation

```python
from pyspark.ml.feature import VectorAssembler

assembler = VectorAssembler(
    inputCols=["feature1", "feature2"],
    outputCol="features"
)
```

---
## Feature Engineering
![feature_engineering](svg/courses/big_data/advanced-spark-with-python/03_advanced_spark_mllib/feature_engineering.svg)

---
## Feature Transformers
1. StringIndexer
1. OneHotEncoder
1. VectorAssembler
1. StandardScaler

---
## Advanced Feature Processing
```python
from pyspark.ml.feature import StandardScaler, PCA

scaler = StandardScaler(
    inputCol="features",
    outputCol="scaledFeatures"
)
```

---
## Pipeline Construction
```python
from pyspark.ml import Pipeline

pipeline = Pipeline(stages=[
    assembler,
    scaler,
    estimator
])
```

---
## Custom Transformers
```python
from pyspark.ml import Transformer
from pyspark.ml.param.shared import HasInputCol, HasOutputCol

class CustomTransformer(Transformer, HasInputCol, HasOutputCol):
    def _transform(self, dataset):
        return dataset
```

---
## Model Training
![model_training](svg/courses/big_data/advanced-spark-with-python/03_advanced_spark_mllib/model_training.svg)

---
## Hyperparameter Tuning
```python
from pyspark.ml.tuning import ParamGridBuilder

paramGrid = ParamGridBuilder()\
    .addGrid(classifier.maxDepth, [2, 5, 10])\
    .addGrid(classifier.maxBins, [10, 20, 40])\
    .build()
```

---
## Cross Validation
```python
from pyspark.ml.tuning import CrossValidator

cv = CrossValidator(
    estimator=pipeline,
    evaluator=evaluator,
    estimatorParamMaps=paramGrid
)
```

---
## Model Evaluation
1. Binary classification metrics
1. Multiclass metrics
1. Regression metrics
1. Custom metrics

---
## Evaluation Metrics
![evaluation_metrics](svg/courses/big_data/advanced-spark-with-python/03_advanced_spark_mllib/evaluation_metrics.svg)

---
## Custom Evaluator
```python
from pyspark.ml.evaluation import Evaluator

class CustomEvaluator(Evaluator):
    def _evaluate(self, dataset):
        return computed_metric
```

---
## Model Selection
```python
# Get best model from cross validation
bestModel = cvModel.bestModel
bestPipeline = bestModel.stages[-1]
```

---
## Distributed Training
![distributed_training](svg/courses/big_data/advanced-spark-with-python/03_advanced_spark_mllib/distributed_training.svg)

---
## Model Persistence

```python
# Save pipeline model
pipeline_model.save("hdfs://model/path")

# Load saved model
loaded_model = PipelineModel.load("hdfs://model/path")
```

---
## Advanced Algorithms
1. Gradient Boosted Trees
1. Neural Networks
1. Random Forests
1. Custom Algorithms

---
## Ensemble Methods
```python
from pyspark.ml.classification import RandomForestClassifier

rf = RandomForestClassifier(
    numTrees=100,
    maxDepth=5
)
```

---
## Neural Networks
![neural_networks](svg/courses/big_data/advanced-spark-with-python/03_advanced_spark_mllib/neural_networks.svg)

---
## Custom Algorithms
```python
from pyspark.ml.classification import Classifier

class CustomClassifier(Classifier):
    def _fit(self, dataset):
        return self._fit_internal(dataset)
```

---
## Online Learning
```python
# Streaming model updates
for batch in streaming_data:
    model = model.fit(batch)
```

---
## Model Serving
![model_serving](svg/courses/big_data/advanced-spark-with-python/03_advanced_spark_mllib/model_serving.svg)

---
## Production Pipeline
1. Data validation
1. Feature computation
1. Model prediction
1. Result logging

---
## Monitoring ML Pipelines
```python
# Log metrics
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
evaluator = MulticlassClassificationEvaluator()
accuracy = evaluator.evaluate(predictions)
```

---
## Performance Optimization
![performance_optimization](svg/courses/big_data/advanced-spark-with-python/03_advanced_spark_mllib/performance_optimization.svg)

---

## Resource Management
1. Memory configuration
1. CPU allocation
1. GPU utilization
1. Cluster sizing

---
## Pipeline Optimization
```python
# Cache frequently used datasets
transformed_data = pipeline.fit(train_data)\
    .transform(train_data).cache()
```

---
## Distributed Processing
![distributed_processing](svg/courses/big_data/advanced-spark-with-python/03_advanced_spark_mllib/distributed_processing.svg)

---
## Feature Store Integration
1. Feature versioning
1. Feature sharing
1. Computation reuse
1. Metadata management

---
## Model Registry
```python
# Register model in MLflow
mlflow.spark.log_model(spark_model, "model")
```

---
## A/B Testing
![a_b_testing](svg/courses/big_data/advanced-spark-with-python/03_advanced_spark_mllib/a_b_testing.svg)

---
## Model Versioning
1. Version control
1. Model lineage
1. Experiment tracking
1. Deployment history

---
## Deployment Strategies
```python
# Rolling deployment
def deploy_model(new_model, old_model):
    # Gradual traffic shift
    pass
```

---
## Error Handling
```python
try:
    predictions = model.transform(dataset)
except Exception as e:
    logging.error(f"Prediction failed: {e}")
```

---
## Data Validation
![data_validation](svg/courses/big_data/advanced-spark-with-python/03_advanced_spark_mllib/data_validation.svg)

---
## Model Explainability
1. Feature importance
1. SHAP values
1. Partial dependence
1. LIME explanations

---
## Automated ML
```python
# AutoML example
from pyspark.ml.tuning import TrainValidationSplit
automl = TrainValidationSplit(
    estimator=pipeline,
    evaluator=evaluator
)
```

---
## Transfer Learning
![transfer_learning](svg/courses/big_data/advanced-spark-with-python/03_advanced_spark_mllib/transfer_learning.svg)

---
## Model Compression
1. Pruning
1. Quantization
1. Knowledge distillation
1. Architecture optimization

---
## Streaming Predictions
```python
# Streaming prediction pipeline
def process_stream(batch_df, epoch_id):
    predictions = model.transform(batch_df)
    return predictions
```

---
## Security Considerations
![security_considerations](svg/courses/big_data/advanced-spark-with-python/03_advanced_spark_mllib/security_considerations.svg)

---
## Testing ML Pipelines
1. Unit tests
1. Integration tests
1. Performance tests
1. Validation tests

---
## Debugging Techniques
```python
# Debug transformation
debug_df = transformer.transform(input_df)
debug_df.show()
```

---
## Best Practices
![best_practices](svg/courses/big_data/advanced-spark-with-python/03_advanced_spark_mllib/best_practices.svg)

---
## Production Checklist
1. Model validation
1. Performance metrics
1. Monitoring setup
1. Fallback strategy

---
## Future Developments
1. AutoML improvements
1. Distributed deep learning
1. Edge deployment
1. Federated learning

---
## MLOps Integration
![mlops_integration](svg/courses/big_data/advanced-spark-with-python/03_advanced_spark_mllib/mlops_integration.svg)

---
## Additional Resources
* Official documentation
* Research papers
* Community guides
* MLOps tools

---

## Full Program: End-to-End ML Pipeline

```python
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import (
    StringIndexer, OneHotEncoder, VectorAssembler,
    StandardScaler, Imputer
)
from pyspark.ml.classification import (
    RandomForestClassifier, GBTClassifier,
    LogisticRegression
)
from pyspark.ml.evaluation import (
    BinaryClassificationEvaluator,
    MulticlassClassificationEvaluator
)
from pyspark.ml.tuning import (
    CrossValidator, ParamGridBuilder
)
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("EndToEndMLPipeline") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()
```

---

## ML Pipeline: Data Loading and Split

```python
# Load and prepare data
raw_data = spark.read.csv(
    "/data/customer_churn.csv",
    header=True,
    inferSchema=True
)

# Data exploration
print(f"Total records: {raw_data.count()}")
print(f"Columns: {raw_data.columns}")
raw_data.describe().show()
raw_data.groupBy("churn").count().show()

# Split data
train_data, test_data = raw_data.randomSplit(
    [0.8, 0.2], seed=42
)
```

---

## Feature Engineering Pipeline

```python
# Identify column types
categorical_cols = ["contract_type", "payment_method", "region"]
numeric_cols = ["tenure", "monthly_charges", "total_charges",
                "num_support_tickets", "num_products"]

# Step 1: Handle missing values in numeric columns
imputer = Imputer(
    inputCols=numeric_cols,
    outputCols=[f"{c}_imputed" for c in numeric_cols],
    strategy="median"
)

# Step 2: Index categorical columns
indexers = [
    StringIndexer(
        inputCol=col,
        outputCol=f"{col}_indexed",
        handleInvalid="keep"
    )
    for col in categorical_cols
]

# Step 3: One-hot encode indexed columns
encoders = [
    OneHotEncoder(
        inputCol=f"{col}_indexed",
        outputCol=f"{col}_encoded"
    )
    for col in categorical_cols
]
```

---

## Feature Engineering: Assembly and Scaling

```python
# Step 4: Assemble all features into a single vector
assembler_inputs = (
    [f"{c}_imputed" for c in numeric_cols] +
    [f"{c}_encoded" for c in categorical_cols]
)
assembler = VectorAssembler(
    inputCols=assembler_inputs,
    outputCol="raw_features",
    handleInvalid="keep"
)

# Step 5: Scale features
scaler = StandardScaler(
    inputCol="raw_features",
    outputCol="features",
    withStd=True,
    withMean=True
)

# Step 6: Index label column
label_indexer = StringIndexer(
    inputCol="churn",
    outputCol="label"
)
```

---

## ML Pipeline Data Flow

![ml_pipeline_data_flow](svg/courses/big_data/advanced-spark-with-python/03_advanced_spark_mllib/ml_pipeline_data_flow.svg)

---

## Model Comparison with CrossValidation

```python
from pyspark.ml.classification import (
    RandomForestClassifier, GBTClassifier,
    LogisticRegression
)

# Define multiple models to compare
models = {
    "RandomForest": RandomForestClassifier(
        labelCol="label",
        featuresCol="features",
        seed=42
    ),
    "GBT": GBTClassifier(
        labelCol="label",
        featuresCol="features",
        seed=42
    ),
    "LogisticRegression": LogisticRegression(
        labelCol="label",
        featuresCol="features",
    ),
}
```

---

## Model Comparison: Parameter Grids

```python
# Define parameter grids for each model
param_grids = {
    "RandomForest": ParamGridBuilder()
        .addGrid(models["RandomForest"].numTrees, [50, 100, 200])
        .addGrid(models["RandomForest"].maxDepth, [5, 10, 15])
        .addGrid(models["RandomForest"].minInstancesPerNode, [1, 5])
        .build(),
    "GBT": ParamGridBuilder()
        .addGrid(models["GBT"].maxDepth, [3, 5, 8])
        .addGrid(models["GBT"].maxIter, [20, 50, 100])
        .addGrid(models["GBT"].stepSize, [0.05, 0.1, 0.2])
        .build(),
    "LogisticRegression": ParamGridBuilder()
        .addGrid(models["LogisticRegression"].regParam,
                 [0.01, 0.1, 1.0])
        .addGrid(models["LogisticRegression"].elasticNetParam,
                 [0.0, 0.5, 1.0])
        .build(),
}

evaluator = BinaryClassificationEvaluator(
    labelCol="label",
    metricName="areaUnderROC"
)
```

---

## Model Comparison: Cross-Validation Loop

```python
# Build and evaluate pipelines
feature_stages = [imputer] + indexers + encoders + \
    [assembler, scaler, label_indexer]

results = {}
for name, model in models.items():
    pipeline = Pipeline(stages=feature_stages + [model])
    cv = CrossValidator(
        estimator=pipeline,
        estimatorParamMaps=param_grids[name],
        evaluator=evaluator,
        numFolds=5,
        parallelism=4,
        seed=42
    )
    cv_model = cv.fit(train_data)
    predictions = cv_model.transform(test_data)
    auc = evaluator.evaluate(predictions)
    results[name] = {
        "auc": auc,
        "best_model": cv_model.bestModel,
    }
    print(f"{name}: AUC = {auc:.4f}")
```

---

## Model Comparison Results Table

| Model | AUC-ROC | Training Time | Interpretable | Handles Nulls |
|---|---|---|---|---|
| Logistic Regression | ~0.82 | Fast | Yes (coefficients) | No |
| Random Forest | ~0.87 | Medium | Partial (importance) | Yes |
| GBT | ~0.89 | Slow | Partial (importance) | Yes |
| MLP Neural Network | ~0.88 | Slowest | No | No |

---

## Feature Importance Analysis

```python
from pyspark.ml.classification import RandomForestClassificationModel

# Extract the best Random Forest model
best_rf = results["RandomForest"]["best_model"]
rf_model = best_rf.stages[-1]  # Last stage is the classifier

# Get feature importances
importances = rf_model.featureImportances.toArray()

# Map to feature names
feature_names = assembler_inputs
feature_importance_df = spark.createDataFrame(
    [(name, float(imp))
     for name, imp in zip(feature_names, importances)],
    ["feature", "importance"]
).orderBy("importance", ascending=False)

feature_importance_df.show(truncate=False)

# Top 5 most important features
print("\nTop 5 Features:")
for row in feature_importance_df.take(5):
    bar = "#" * int(row["importance"] * 50)
    print(f"  {row['feature']:30s} {row['importance']:.4f} {bar}")
```

---

## Full Program: Custom Transformer

```python
from pyspark.ml import Transformer
from pyspark.ml.param.shared import (
    HasInputCol, HasOutputCol, Param, Params
)
from pyspark.ml.util import DefaultParamsReadable, DefaultParamsWritable
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType

class OutlierClipper(
    Transformer,
    HasInputCol,
    HasOutputCol,
    DefaultParamsReadable,
    DefaultParamsWritable
):
    """Custom transformer that clips outliers using IQR method."""

    lower_quantile = Param(
        Params._dummy(), "lower_quantile",
        "Lower quantile for clipping", typeConverter=float
    )
    upper_quantile = Param(
        Params._dummy(), "upper_quantile",
        "Upper quantile for clipping", typeConverter=float
    )
```

---

## Custom Transformer: Init and setParams

```python
    def __init__(self, inputCol=None, outputCol=None,
                 lower_quantile=0.01, upper_quantile=0.99):
        super().__init__()
        self._setDefault(
            lower_quantile=0.01,
            upper_quantile=0.99
        )
        kwargs = self._input_kwargs
        self.setParams(**kwargs)

    def setParams(self, inputCol=None, outputCol=None,
                  lower_quantile=0.01, upper_quantile=0.99):
        kwargs = self._input_kwargs
        return self._set(**kwargs)
```

---

## Custom Transformer: _transform and Usage

```python
    def _transform(self, dataset):
        input_col = self.getInputCol()
        output_col = self.getOutputCol()
        lower_q = self.getOrDefault(self.lower_quantile)
        upper_q = self.getOrDefault(self.upper_quantile)

        quantiles = dataset.approxQuantile(
            input_col, [lower_q, upper_q], 0.01
        )
        lower_bound, upper_bound = quantiles[0], quantiles[1]

        return dataset.withColumn(
            output_col,
            F.when(F.col(input_col) < lower_bound, lower_bound)
            .when(F.col(input_col) > upper_bound, upper_bound)
            .otherwise(F.col(input_col))
        )

# Usage in a pipeline
clipper = OutlierClipper(
    inputCol="monthly_charges",
    outputCol="monthly_charges_clipped",
    lower_quantile=0.01,
    upper_quantile=0.99
)
```

---

## Full Program: Streaming ML Predictions

```python
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel

spark = SparkSession.builder \
    .appName("StreamingPredictions") \
    .getOrCreate()

# Load pre-trained model
model = PipelineModel.load("/models/churn_predictor_v2/")

# Define streaming source (Kafka)
streaming_input = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "customer_events")
    .option("startingOffsets", "latest")
    .load()
)
```

---

## Streaming ML: Event Schema

```python
# Parse JSON messages
from pyspark.sql.types import *
from pyspark.sql import functions as F

event_schema = StructType([
    StructField("customer_id", IntegerType()),
    StructField("contract_type", StringType()),
    StructField("tenure", IntegerType()),
    StructField("monthly_charges", DoubleType()),
    StructField("total_charges", DoubleType()),
    StructField("num_support_tickets", IntegerType()),
    StructField("num_products", IntegerType()),
    StructField("payment_method", StringType()),
    StructField("region", StringType()),
])

parsed_events = (
    streaming_input
    .select(
        F.from_json(
            F.col("value").cast("string"),
            event_schema
        ).alias("data")
    )
    .select("data.*")
)
```

---

## Streaming ML: Scoring and Query

```python
# Apply model to streaming data
def score_batch(batch_df, batch_id):
    if batch_df.count() == 0:
        return
    predictions = model.transform(batch_df)
    high_risk = predictions.filter(F.col("prediction") == 1.0)
    high_risk.select(
        "customer_id", "prediction", "probability"
    ).write.mode("append").parquet("/output/churn_alerts/")

# Start streaming query
query = (
    parsed_events.writeStream
    .foreachBatch(score_batch)
    .option("checkpointLocation", "/checkpoints/churn_scoring/")
    .trigger(processingTime="30 seconds")
    .start()
)

query.awaitTermination()
```

---

## MLflow Integration: Full Experiment Tracking

```python
import mlflow
import mlflow.spark
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import BinaryClassificationEvaluator

mlflow.set_tracking_uri("http://mlflow-server:5000")
mlflow.set_experiment("customer_churn_prediction")

with mlflow.start_run(run_name="rf_v3_tuned") as run:
    # Log parameters
    mlflow.log_param("model_type", "RandomForest")
    mlflow.log_param("num_trees", 200)
    mlflow.log_param("max_depth", 10)
    mlflow.log_param("train_size", train_data.count())
    mlflow.log_param("test_size", test_data.count())

    # Train model
    pipeline = Pipeline(stages=feature_stages + [
        RandomForestClassifier(
            numTrees=200, maxDepth=10, seed=42,
            labelCol="label", featuresCol="features"
        )
    ])
    model = pipeline.fit(train_data)
    predictions = model.transform(test_data)
```

---

## MLflow: Metrics and Model Logging

```python
with mlflow.start_run(run_name="rf_v3_tuned") as run:
    # Evaluate and log metrics
    evaluator_auc = BinaryClassificationEvaluator(
        labelCol="label", metricName="areaUnderROC")
    evaluator_pr = BinaryClassificationEvaluator(
        labelCol="label", metricName="areaUnderPR")
    multi_eval = MulticlassClassificationEvaluator(
        labelCol="label")

    mlflow.log_metric("auc_roc", evaluator_auc.evaluate(predictions))
    mlflow.log_metric("auc_pr", evaluator_pr.evaluate(predictions))
    mlflow.log_metric("accuracy",
        multi_eval.evaluate(predictions, {multi_eval.metricName: "accuracy"}))
    mlflow.log_metric("f1",
        multi_eval.evaluate(predictions, {multi_eval.metricName: "f1"}))

    # Log model
    mlflow.spark.log_model(model, "model",
        registered_model_name="churn_predictor")

    # Log feature importance as artifact
    importance_pdf = feature_importance_df.toPandas()
    importance_pdf.to_csv("/tmp/feature_importance.csv", index=False)
    mlflow.log_artifact("/tmp/feature_importance.csv")

    print(f"Run ID: {run.info.run_id}")
```

---

## Handling Class Imbalance

```python
from pyspark.sql import functions as F

# Check class distribution
train_data.groupBy("churn").count().show()
# +-----+------+
# |churn| count|
# +-----+------+
# |   No|  5174|
# |  Yes|  1869|
# +-----+------+

# Method 1: Class weights
total = train_data.count()
pos_count = train_data.filter(F.col("churn") == "Yes").count()
neg_count = total - pos_count

weight_pos = total / (2.0 * pos_count)
weight_neg = total / (2.0 * neg_count)

weighted_train = train_data.withColumn(
    "weight",
    F.when(F.col("churn") == "Yes", weight_pos)
    .otherwise(weight_neg)
)

# Use with LogisticRegression
lr = LogisticRegression(
    labelCol="label",
    featuresCol="features",
    weightCol="weight"
)
```

---

## Class Imbalance: Oversampling

```python
# Method 2: SMOTE-like oversampling
minority = train_data.filter(F.col("churn") == "Yes")
oversample_ratio = int(neg_count / pos_count)
oversampled_minority = minority
for _ in range(oversample_ratio - 1):
    oversampled_minority = oversampled_minority.union(minority)

balanced_train = train_data.filter(
    F.col("churn") == "No"
).union(oversampled_minority)

print(f"Balanced distribution:")
balanced_train.groupBy("churn").count().show()
```

---

## Model Serving Architecture

![model_serving_architecture](svg/courses/big_data/advanced-spark-with-python/03_advanced_spark_mllib/model_serving_architecture.svg)

---

## Production ML Pipeline Checklist

![production_ml_pipeline_checklist](svg/courses/big_data/advanced-spark-with-python/03_advanced_spark_mllib/production_ml_pipeline_checklist.svg)
