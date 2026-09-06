---
tags:
  - data-and-ai:deep-learning
level: intermediate
category: machine-learning
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Convolutional Neural Networks

---

## What This Chapter Covers

- Convolution and pooling operations
- Classic CNN architectures
- Image classification
- Object detection overview
- Data augmentation techniques

---

## Why CNNs

- Images have spatial structure
- Pixels nearby are related
- Dense layers ignore that
- CNNs bake locality into the architecture

---

## What a CNN Sees

- Pixels as a 2D grid
- Same pattern can appear anywhere
- Translation invariance is built-in
- Shared filters across the image

---

## The Convolution Operation

- Slide a small filter over the image
- Multiply element-wise and sum
- One output value per position
- Output is a feature map

---

## Convolution Visualized

![convolution](svg/courses/machine_learning/deep-learning-fundamentals/03_cnns/convolution.svg)

---

## Filters Learn Features

- First layer: edges, colors
- Middle layers: textures, parts
- Late layers: objects
- Learned, not hand-coded

---

## Filter, Kernel, Feature Map

- Filter and kernel: same thing
- A filter has weights to learn
- Feature map: output of applying the filter
- Many filters per layer

---

## Stride

- Step size of the filter
- Stride 1: dense output
- Stride 2: halves resolution
- Trade resolution for speed

---

## Padding

- Add zeros around the image
- Keeps output size the same
- "same" padding: output matches input
- "valid" padding: no padding, output shrinks

---

## Receptive Field

- The input region that affects one output
- Grows with depth
- Late layers see most of the image
- Key concept for what a layer can learn

---

## Receptive Field Grows With Depth

![receptive field](svg/courses/machine_learning/deep-learning-fundamentals/03_cnns/receptive_field.svg)

---

## Pooling

- Downsample feature maps
- Max pool: take the maximum
- Average pool: take the mean
- Reduces compute and gives translation tolerance

---

## Pooling Visualized

![pooling](svg/courses/machine_learning/deep-learning-fundamentals/03_cnns/pooling.svg)

---

## Channels

- Color images: 3 channels (RGB)
- Hidden layers: many channels
- One filter spans all input channels
- Number of output channels = number of filters

---

## A Convolutional Block

- Conv layer
- Activation (usually ReLU)
- Optional batch norm
- Optional pooling

---

## Building a CNN

- Stack convolutional blocks
- Reduce spatial size, grow channels
- Flatten or global pool at the end
- Add a small dense head

---

## CNN Architecture Diagram

![cnn_architecture](svg/courses/machine_learning/deep-learning-fundamentals/03_cnns/cnn_architecture.svg)

---

## A Tiny CNN in Keras

```python
model = keras.Sequential([
    layers.Conv2D(32, 3, activation="relu", padding="same"),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation="relu", padding="same"),
    layers.MaxPooling2D(),
    layers.GlobalAveragePooling2D(),
    layers.Dense(10, activation="softmax"),
])
```

---

## The Same in PyTorch

```python
class TinyCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.head = nn.Linear(64, 10)
    def forward(self, x):
        x = self.pool(self.conv1(x).relu())
        x = self.pool(self.conv2(x).relu())
        x = x.mean(dim=(2, 3))
        return self.head(x)
```

---

## LeNet

- LeCun, 1998
- Trained for digit recognition
- Two conv layers, two pool layers
- Ran on a CPU on small images

---

## AlexNet

- Krizhevsky et al, 2012
- Won ImageNet by a large margin
- Used ReLU, dropout, two GPUs
- Kicked off the deep learning era

---

## VGG

- Simonyan and Zisserman, 2014
- All 3x3 convolutions
- 16 or 19 layers deep
- Heavy on parameters, easy to understand

---

## GoogLeNet and Inception

- Inception modules: parallel filter sizes
- Bottleneck 1x1 convolutions
- Much smaller than VGG
- Won ImageNet 2014

---

## ResNet

- He et al, 2015
- Residual connections: y = F(x) + x
- Made 100+ layer networks trainable
- Backbone of countless modern models

---

## Why Residual Connections

- Gradient has a direct path back
- Identity shortcut is easy to learn
- Lets deep nets at least not get worse
- Now standard everywhere

---

## ResNet Block

![resnet_block](svg/courses/machine_learning/deep-learning-fundamentals/03_cnns/resnet_block.svg)

---

## Modern Architectures

- EfficientNet: scaled depth, width, resolution
- MobileNet: depthwise separable convs
- ConvNeXt: convs catching up to transformers
- Vision Transformers: convs replaced by attention

---

## Image Classification

- One label per image
- Softmax over classes
- Cross-entropy loss
- Top-1 and top-5 accuracy

---

## ImageNet

- 1000 classes, ~1.3M training images
- The proving ground for vision models
- Pretrained weights freely available
- Most CV transfer learning starts here

---

## Object Detection

- Find and classify objects in an image
- Output: bounding boxes plus labels
- Harder than classification
- Two main families: two-stage and one-stage

---

## Two-Stage Detectors

- R-CNN, Fast R-CNN, Faster R-CNN
- Stage 1: propose regions
- Stage 2: classify and refine
- Accurate, slower

---

## One-Stage Detectors

- YOLO, SSD, RetinaNet
- Predict boxes and classes in one pass
- Faster, often slightly less accurate
- Good for real-time use

---

## Object Detection Output

![object_detection](svg/courses/machine_learning/deep-learning-fundamentals/03_cnns/object_detection.svg)

---

## Anchor Boxes

- Predefined box shapes
- Network predicts offsets and class
- Spread across the image grid
- Modern: anchor-free designs gaining ground

---

## Non-Maximum Suppression

- Many overlapping boxes per object
- Keep the highest-scoring one
- Suppress others with high overlap
- Post-processing step, not learned

---

## Semantic Segmentation

- Label every pixel
- U-Net is the classic architecture
- Encoder-decoder with skip connections
- Used in medical imaging, satellite, autonomous driving

---

## Instance Segmentation

- Segment each object separately
- Mask R-CNN adds a mask head
- Combines detection and segmentation
- Heavier and slower

---

## Data Augmentation

- Generate variants from training data
- Flip, crop, rotate, color jitter
- Random erasing, mixup, cutmix
- Effectively grows the dataset

---

## Augmentation Examples

![augmentation](svg/courses/machine_learning/deep-learning-fundamentals/03_cnns/augmentation.svg)

---

## Augmentation in Keras

```python
augment = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])
```

---

## Augmentation Best Practices

- Pick transforms that preserve labels
- Don't flip digits, do flip cats
- Apply only during training
- Stronger augmentation, larger nets

---

## Common CNN Pitfalls

- Forgetting to normalize inputs
- Wrong channel order (NHWC vs NCHW)
- Mismatched image sizes
- Augmenting validation data by accident

---

## Practical Tips

- Start with a known architecture
- Use pretrained weights when possible
- Watch GPU memory for batch size
- Try one architecture deeply before swapping

---

## Summary

- CNNs exploit spatial structure with shared filters
- Stack conv and pool to grow receptive fields
- Classic to modern: LeNet, ResNet, EfficientNet
- Augmentation is the cheapest accuracy boost
