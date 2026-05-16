---
tags:
  - data-and-ai:deep-learning
level: intermediate
category: machine-learning
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Neural Network Foundations

---
## What This Chapter Covers

- Biological inspiration and the perceptron
- Activation functions
- Feedforward networks
- Loss functions and optimization
- Backpropagation and gradient descent
- Regularization techniques

---
## Why Neural Networks

- Universal function approximators
- Learn features automatically
- Scale with data and compute
- State of the art in vision, speech, language

---
## Biological Inspiration

- Brain has billions of neurons
- Each neuron fires on weighted inputs
- Connections strengthen with experience
- Loose metaphor, not a literal model

---
## The Biological Neuron

- Dendrites: receive signals
- Cell body: integrates input
- Axon: transmits output
- Synapse: weight on a connection

---
## The Artificial Neuron

- Inputs x1, x2, ..., xn
- Weights w1, w2, ..., wn
- Bias b
- Output: f(w.x + b)

---
## The Perceptron

- Rosenblatt, 1958
- Single-layer linear classifier
- Step activation
- Learns by adjusting weights on errors

---
## Perceptron Update Rule

- Predict y_hat
- Error: y - y_hat
- `w := w + lr * error * x`
- Converges if data is linearly separable

---
## Limits of a Single Perceptron

- Cannot solve XOR
- Only linear decision boundaries
- Famously highlighted by Minsky and Papert
- Sparked the first AI winter

---
## Multi-Layer Networks Fix This

- Stack neurons in layers
- Hidden layers add non-linearity
- Can approximate any continuous function
- Backed by the universal approximation theorem

---
## Activation Functions

- Inject non-linearity
- Without them, the whole net is linear
- Choice affects training dynamics
- Modern default: ReLU and variants

---
## Sigmoid

- Squashes to (0, 1)
- Smooth and differentiable
- Saturates: gradients vanish at extremes
- Used in output layers for probabilities

---
## Tanh

- Squashes to (-1, 1)
- Zero-centered, easier optimization than sigmoid
- Still saturates at extremes
- Common in older RNNs

---
## ReLU

- f(x) = max(0, x)
- Cheap to compute
- No saturation on positive side
- Default choice for hidden layers

---
## ReLU Pitfalls

- Dying ReLU: neuron stuck at zero
- Not differentiable at zero
- Unbounded output can explode
- Fix with variants

---
## Leaky ReLU and Friends

- Leaky ReLU: small slope for negatives
- PReLU: learnable negative slope
- ELU: smooth negative side
- GELU: Gaussian-weighted, used in transformers

---
## Softmax

- Turns logits into probabilities
- Output sums to 1
- Used for multi-class classification
- Pairs with cross-entropy loss

---
## Feedforward Network

- Input layer
- One or more hidden layers
- Output layer
- Information flows forward only

---
## Feedforward Network Diagram

![feedforward_network](svg/courses/machine_learning/deep-learning-fundamentals/01_neural_network_foundations/feedforward_network.svg)

---
## Depth vs Width

- Depth: number of layers
- Width: neurons per layer
- Deeper nets learn hierarchical features
- Wider nets memorize more

---
## What Hidden Layers Learn

- Early layers: simple patterns
- Middle layers: parts and motifs
- Late layers: full concepts
- Hierarchy emerges from the data

---
## Loss Functions

- Measure prediction error
- Differentiable so we can optimize
- Match the task type
- Same network, different loss, different behavior

---
## Mean Squared Error

- For regression
- Average of squared differences
- Penalizes large errors heavily
- Sensitive to outliers

---
## Mean Absolute Error

- Average of absolute differences
- More robust to outliers than MSE
- Less smooth at zero
- Slower convergence sometimes

---
## Cross-Entropy

- For classification
- Measures distance between distributions
- Pairs with softmax output
- Heavy penalty for confident wrong answers

---
## Binary Cross-Entropy

- For two-class problems
- Pairs with sigmoid output
- Same idea as cross-entropy
- Special case for one logit

---
## Gradient Descent

- Compute loss
- Compute gradient of loss with respect to weights
- Step opposite the gradient
- Repeat until loss stops dropping

---
## Gradient Descent Visualized

![gradient_descent](svg/courses/machine_learning/deep-learning-fundamentals/01_neural_network_foundations/gradient_descent.svg)

---
## Learning Rate

- Step size for each update
- Too high: oscillates or diverges
- Too low: training crawls
- One of the most important hyperparameters

---
## Batch, Mini-Batch, Stochastic

- Batch: full dataset per step
- Stochastic: one sample per step
- Mini-batch: small group, the default
- Mini-batch balances speed and stability

---
## Backpropagation

- Chain rule applied layer by layer
- Forward pass: compute outputs
- Backward pass: compute gradients
- Update weights with gradients

---
## Backpropagation Diagram

![backpropagation](svg/courses/machine_learning/deep-learning-fundamentals/01_neural_network_foundations/backpropagation.svg)

---
## Computing Gradients

- For each weight, partial derivative of loss
- Reuse intermediate values from forward pass
- Linear in network size
- Made deep learning practical

---
## Vanishing Gradients

- Gradients shrink through many layers
- Early layers learn very slowly
- Worse with sigmoid and tanh
- ReLU and residuals help

---
## Exploding Gradients

- Gradients grow without bound
- Weights blow up
- Common in RNNs
- Fix with clipping

---
## Optimizers

- Plain SGD: simple, often enough
- Momentum: smooths the path
- Adam: adapts per-parameter learning rates
- AdamW: Adam with proper weight decay

---
## Momentum

- Adds a running average of past gradients
- Speeds up in consistent directions
- Damps oscillations
- Typical value: 0.9

---
## Adam

- Per-parameter adaptive learning rates
- Combines momentum and RMSProp
- Robust default for many tasks
- Beware: may generalize worse than SGD

---
## Weight Initialization

- Random, not zero
- Variance matters
- Xavier/Glorot: for tanh and sigmoid
- He: for ReLU

---
## Overfitting

- Train loss drops, test loss climbs
- Network memorizes noise
- Common with large nets, small data
- Fight with regularization

---
## Regularization Goals

- Reduce gap between train and test
- Encourage simpler functions
- Improve generalization
- Often costs a bit of train accuracy

---
## L1 and L2 Regularization

- Add a weight penalty to the loss
- L1: encourages sparsity
- L2: encourages small weights
- Tuned by a coefficient

---
## Dropout

- Randomly zero out activations during training
- Forces redundant representations
- Acts like training many sub-networks
- Disabled at inference

---
## Dropout Visualized

![dropout](svg/courses/machine_learning/deep-learning-fundamentals/01_neural_network_foundations/dropout.svg)

---
## Batch Normalization

- Normalize activations per batch
- Smoother loss surface
- Allows higher learning rates
- Acts as a mild regularizer

---
## Layer Normalization

- Normalize across features, not batch
- Independent of batch size
- Used in transformers and RNNs
- Common in modern architectures

---
## Early Stopping

- Track validation loss
- Stop when it stops improving
- Cheap and effective
- Save the best checkpoint

---
## Data Augmentation

- Generate variants of training samples
- Flip, crop, rotate, jitter
- Effectively grows the dataset
- A regularizer in disguise

---
## Bias and Variance

- High bias: underfits
- High variance: overfits
- Balance via capacity and regularization
- Deep nets favor high capacity plus regularization

---
## The Training Loop

![training loop](svg/courses/machine_learning/deep-learning-fundamentals/01_neural_network_foundations/training_loop.svg)

---
## A Training Recipe

- Start with a known architecture
- Use a small subset to overfit on purpose
- Add data and regularization
- Tune learning rate first

---
## Diagnosing Training

- Loss not decreasing: check learning rate
- Train loss low, val loss high: overfit
- Both losses high: underfit
- Loss diverging: clip or lower lr

---
## Summary

- Neurons combine inputs with weights and an activation
- Multi-layer nets learn hierarchical features
- Backprop and gradient descent train them
- Regularization keeps them honest on new data
