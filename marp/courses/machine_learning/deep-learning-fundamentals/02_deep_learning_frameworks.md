---
tags:
  - data-and-ai:deep-learning
  - tools:pytorch
  - tools:tensorflow
level: intermediate
category: machine-learning
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Deep Learning Frameworks

---
## What This Chapter Covers

- TensorFlow and Keras
- PyTorch
- Tensor operations and automatic differentiation
- Building models with Sequential and functional APIs
- Training loops and callbacks
- GPU acceleration

---
## Why Use a Framework

- Hand-coding backprop is painful
- Frameworks give us autodiff for free
- GPU kernels are tuned for you
- Huge ecosystem of pretrained models

---
## The Landscape

- TensorFlow: Google, production-heavy
- PyTorch: Meta, research-heavy
- JAX: composable transforms, growing
- Keras: high-level API, now multi-backend

---
## Frameworks Compared

![frameworks_overview](svg/courses/machine_learning/deep-learning-fundamentals/02_deep_learning_frameworks/frameworks_overview.svg)

---
## Convergence

- APIs increasingly similar
- Both support eager execution
- Both support graph compilation
- Choice often comes down to ecosystem

---
## The Framework Stack

![framework stack](svg/courses/machine_learning/deep-learning-fundamentals/02_deep_learning_frameworks/framework_stack.svg)

---
## TensorFlow

- Released 2015 by Google
- Originally static computation graph
- TF 2.x defaults to eager mode
- Strong production tooling

---
## Keras

- High-level neural network API
- Now backend-agnostic
- Three styles: Sequential, functional, subclassing
- Beginner-friendly and concise

---
## A Keras Sequential Model

```python
import keras
from keras import layers

model = keras.Sequential([
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.2),
    layers.Dense(10, activation="softmax"),
])
```

---
## Compile and Fit

```python
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)
model.fit(x_train, y_train, epochs=5, batch_size=32)
```

---
## The Functional API

- Build a graph of layers as functions
- Supports multiple inputs and outputs
- Shared layers across branches
- More flexible than Sequential

---
## Functional API Example

```python
inputs = keras.Input(shape=(784,))
x = layers.Dense(128, activation="relu")(inputs)
x = layers.Dropout(0.2)(x)
outputs = layers.Dense(10, activation="softmax")(x)
model = keras.Model(inputs, outputs)
```

---
## Model Subclassing

- Inherit from keras.Model
- Define call(self, inputs)
- Full control over forward pass
- Pythonic and flexible

---
## PyTorch

- Released 2016 by Meta
- Eager by default from day one
- Pythonic feel
- Dominant in research

---
## Tensors

- N-dimensional arrays
- Live on CPU or GPU
- Track gradients automatically
- Foundation of every framework

---
## Creating Tensors

```python
import torch

a = torch.zeros(3, 4)
b = torch.randn(3, 4)
c = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
d = torch.arange(10).reshape(2, 5)
```

---
## Tensor Operations

```python
x = torch.randn(3, 4)
y = torch.randn(4, 5)
z = x @ y              # matmul
s = x.sum(dim=0)       # reduction
r = x.relu()           # elementwise
```

---
## Broadcasting

- Operate on tensors of different shapes
- Smaller tensor stretched to match
- Same rules as numpy
- Avoids explicit loops

---
## Automatic Differentiation

- Frameworks record operations on tensors
- Build a computation graph behind the scenes
- Call backward and get all gradients
- No manual chain rule

---
## Autograd in PyTorch

```python
x = torch.tensor(2.0, requires_grad=True)
y = x ** 3 + 2 * x
y.backward()
print(x.grad)   # 3*x^2 + 2 = 14
```

---
## Computation Graph

![computation_graph](svg/courses/machine_learning/deep-learning-fundamentals/02_deep_learning_frameworks/computation_graph.svg)

---
## Building a Module in PyTorch

```python
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(784, 128),
            nn.ReLU(),
            nn.Linear(128, 10),
        )
    def forward(self, x):
        return self.net(x)
```

---
## A PyTorch Training Loop

```python
model = MLP().to(device)
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.CrossEntropyLoss()

for x, y in loader:
    x, y = x.to(device), y.to(device)
    opt.zero_grad()
    out = model(x)
    loss = loss_fn(out, y)
    loss.backward()
    opt.step()
```

---
## Training Loop Anatomy

![training_loop](svg/courses/machine_learning/deep-learning-fundamentals/02_deep_learning_frameworks/training_loop.svg)

---
## Why Zero the Gradients

- PyTorch accumulates gradients by default
- Forgetting zero_grad gives stale updates
- Common bug for beginners
- Keras hides this in fit

---
## Eval Mode

- Disable dropout and batchnorm updates
- PyTorch: model.eval()
- Disable autograd: torch.no_grad()
- Saves memory and speeds inference

---
## Datasets and Loaders

- Dataset: knows how to fetch one sample
- DataLoader: batching, shuffling, parallel workers
- Same pattern in both frameworks
- Backbone of any training pipeline

---
## A PyTorch Dataset

```python
from torch.utils.data import Dataset, DataLoader

class MyData(Dataset):
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __len__(self):
        return len(self.x)
    def __getitem__(self, i):
        return self.x[i], self.y[i]

loader = DataLoader(MyData(x, y), batch_size=64, shuffle=True)
```

---
## Callbacks in Keras

- Hook into training events
- EarlyStopping, ModelCheckpoint
- ReduceLROnPlateau, TensorBoard
- Pass via callbacks argument to fit

---
## Callback Example

```python
callbacks = [
    keras.callbacks.EarlyStopping(patience=5),
    keras.callbacks.ModelCheckpoint("best.keras"),
    keras.callbacks.TensorBoard(log_dir="logs"),
]
model.fit(..., callbacks=callbacks)
```

---
## PyTorch Lightning

- High-level wrapper for PyTorch
- Hides boilerplate training loops
- Built-in checkpoints, logging, multi-GPU
- Closer to the Keras experience

---
## GPU Acceleration

- Neural networks are mostly matmuls
- GPUs do thousands in parallel
- One-line code change in both frameworks
- Speedups of 10x to 100x

---
## CPU vs GPU

![cpu_vs_gpu](svg/courses/machine_learning/deep-learning-fundamentals/02_deep_learning_frameworks/cpu_vs_gpu.svg)

---
## Moving to GPU

```python
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
x = x.to(device)
```

- Inputs and model must be on the same device
- Forgetting this gives a confusing error

---
## Mixed Precision

- Use float16 for forward and backward
- Use float32 for accumulation
- Faster, less memory
- torch.cuda.amp, tf.keras mixed_precision

---
## Multi-GPU Training

- Data parallel: split the batch
- Model parallel: split the model
- DistributedDataParallel in PyTorch
- MirroredStrategy in TensorFlow

---
## Saving and Loading Models

- Save weights, not just code
- PyTorch: torch.save(model.state_dict())
- Keras: model.save("model.keras")
- Version your checkpoints

---
## Reproducibility

- Seed Python, NumPy, framework
- Set deterministic flags
- Pin library versions
- GPU nondeterminism is hard to fully kill

---
## TensorBoard

- Visualize loss, metrics, weights
- Inspect computation graphs
- See sample inputs and outputs
- Works with both frameworks

---
## Debugging Tips

- Print shapes at every layer
- Overfit a tiny batch first
- Check loss on a known easy example
- Watch the gradient norms

---
## Common Pitfalls

- Forgetting model.eval at inference
- Mixing devices CPU and GPU
- Wrong loss for the task
- Targets in the wrong shape

---
## Picking a Framework

- PyTorch: research, custom models
- TensorFlow: production, mobile, TFLite
- Keras: fastest to a first model
- Many teams use both

---
## Summary

- Frameworks handle tensors, autograd, and GPUs
- Keras is highest-level, PyTorch is most flexible
- The training loop is short and repetitive
- Master one, the others come quickly
