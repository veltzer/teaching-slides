# Spark MLlib

## Introduction to Machine Learning

1. Supervised Learning
1. Unsupervised Learning
1. Model Training
1. Model Evaluation
1. Feature Engineering

---

## MLlib Architecture

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">MLlib</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">G</text>
  <rect x="625" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">H</text>
  <rect x="25" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">I</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="100" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Machine Learning Types

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">ML Types</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">G</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## ML Pipeline Components

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
  <line x1="300" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Raw Data</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="150" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Feature Types

1. Numerical Features
1. Categorical Features
1. Text Features
1. Custom Features
1. Combined Features

---

## Feature Transformations

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Features</text>
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

## Classification Architecture

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Classification</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">G</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Regression</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">G</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Model</text>
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
  <line x1="300" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
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
  <line x1="100" y1="150" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Pipeline Architecture

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Raw Data</text>
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
  <line x1="300" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Parameters</text>
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
  <line x1="500" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Clustering</text>
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

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Model</text>
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

## Model Save and Load

```scala
model.save("model_path")
val loadedModel = PipelineModel.load("model_path")
```

---

## Performance Optimization

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Optimization</text>
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
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Model Deployment Flow

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Development</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="150" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Common Use Cases

1. Text Classification
1. Recommendation Systems
1. Anomaly Detection
1. Customer Segmentation
1. Predictive Maintenance

---

## Advanced Topics

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Advanced ML</text>
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
