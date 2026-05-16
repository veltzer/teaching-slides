---
tags:
  - data-and-ai:deep-learning
level: intermediate
category: machine-learning
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Transfer Learning

---
## What This Chapter Covers

- Pretrained models and feature extraction
- Fine-tuning strategies
- Domain adaptation
- When and how to apply transfer learning

---
## What Is Transfer Learning

- Start from a model trained on something else
- Adapt it to your specific task
- Reuse learned features instead of relearning
- Saves data, time, and compute

---
## Why It Works

- Early features generalize across tasks
- Edges and textures are reusable
- Language structure is reusable
- The hard part is already done

---
## The Pretrain-Finetune Pattern

![pretrain_finetune](svg/courses/machine_learning/deep-learning-fundamentals/06_transfer_learning/pretrain_finetune.svg)

---
## When to Use It

- Small labeled dataset
- Task close to a well-studied one
- Limited compute budget
- Need a strong baseline fast

---
## When It Hurts

- Very different domain (medical scans vs cats)
- Very different label structure
- Pretrained model is much larger than needed
- Sometimes from-scratch is fine

---
## Pretrained Vision Models

- Trained on ImageNet (~1.3M images, 1000 classes)
- Available in Keras Applications and torchvision
- ResNet, EfficientNet, ConvNeXt, ViT
- One line to load

---
## Loading a Pretrained CNN

```python
base = keras.applications.ResNet50(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3),
)
```

- include_top=False drops the classification head
- We add our own head

---
## Pretrained NLP Models

- Trained on huge text corpora
- BERT, RoBERTa, DeBERTa for understanding
- GPT family, T5 for generation
- Hugging Face is the default hub

---
## Feature Extraction

- Freeze the backbone
- Run inputs through it
- Use outputs as feature vectors
- Train a small classifier on top

---
## Feature Extraction Example

```python
base.trainable = False
inputs = keras.Input(shape=(224, 224, 3))
x = base(inputs, training=False)
x = layers.GlobalAveragePooling2D()(x)
outputs = layers.Dense(num_classes, activation="softmax")(x)
model = keras.Model(inputs, outputs)
```

---
## When to Use Feature Extraction

- Very small dataset
- Need fast iteration
- Backbone is well-suited
- Limited GPU memory

---
## Fine-Tuning

- Unfreeze some or all of the backbone
- Train at a lower learning rate
- Updates backbone for your task
- Higher accuracy at higher cost

---
## Feature Extraction vs Fine-Tuning

![fine_tuning](svg/courses/machine_learning/deep-learning-fundamentals/06_transfer_learning/fine_tuning.svg)

---
## Three Freezing Strategies

![freezing strategy](svg/courses/machine_learning/deep-learning-fundamentals/06_transfer_learning/freezing_strategy.svg)

---
## Picking What to Unfreeze

- Last block often: most task-specific
- More layers if you have more data
- Whole model if data is plentiful
- Start small, expand if needed

---
## Learning Rate for Fine-Tuning

- Use a much smaller learning rate
- 10x to 100x smaller than from-scratch
- Prevents wrecking pretrained weights
- Often the single most important setting

---
## Discriminative Learning Rates

- Different learning rates per layer
- Higher for new head, lower for old layers
- Slow updates deep in the network
- ULMFiT popularized this for NLP

---
## A Fine-Tuning Recipe

- Add a new head
- Freeze backbone, train head briefly
- Unfreeze backbone
- Continue training at a low lr

---
## Avoid Catastrophic Forgetting

- Sudden large updates erase pretrained knowledge
- Symptoms: loss spikes, accuracy collapses
- Lower lr, warm up, freeze longer
- Watch validation metrics carefully

---
## Warmup

- Start with very small learning rate
- Ramp up over a few hundred steps
- Stabilizes early training
- Standard in transformer fine-tuning

---
## Parameter-Efficient Fine-Tuning

- Update few parameters, freeze most
- Adapters: small trainable bottleneck layers
- LoRA: low-rank weight updates
- Prefix and prompt tuning

---
## LoRA in One Sentence

- Add low-rank deltas to weight matrices
- Train only the deltas
- 1% of parameters often enough
- Now standard for large model fine-tuning

---
## When PEFT Wins

- Huge base models you cannot fully fine-tune
- Many tasks, one base, many adapters
- Limited GPU memory
- Faster training, smaller checkpoints

---
## Domain Adaptation

- Source and target distributions differ
- Same labels, different inputs
- Photos vs sketches, news vs tweets
- Specialized techniques can help

---
## Domain Adaptation Techniques

- Continued pretraining on target domain
- Domain-adversarial training
- Style transfer to match distributions
- Match label space first, content second

---
## Continued Pretraining

- Take a pretrained model
- Pretrain more on your domain corpus
- No labels needed
- Often the cheapest big win for niche NLP

---
## Few-Shot Transfer

- Adapt with very few labeled examples
- Foundation models do this surprisingly well
- Prompting can replace fine-tuning
- Lower bound: zero-shot

---
## Zero-Shot Classification

- Use a model's prior knowledge directly
- No task-specific training
- Works for many text and vision tasks
- Baseline before you label data

---
## CLIP and Zero-Shot Vision

- Learns image-text alignment
- Classify by similarity to class names
- No task-specific training
- Strong out-of-the-box performance

---
## Multi-Task Learning

- Train one model on several tasks
- Shared backbone, task-specific heads
- Tasks can regularize each other
- Watch for negative transfer

---
## Negative Transfer

- Pretrained features hurt your task
- Sometimes happens with mismatched domains
- Train from scratch as a sanity check
- Don't assume pretrained is always better

---
## Choosing a Base Model

- Pick something close to your task
- Reuse the tokenizer or input pipeline
- Smaller if you can deploy it
- Open weights vs API access

---
## Evaluating Transfer

- Compare to from-scratch baseline
- Use the same data split
- Hold out a true test set
- Beware of pretraining data leakage

---
## Pretraining Data Leakage

- Public benchmarks may overlap pretraining data
- Inflated metrics that won't survive deployment
- Make your own held-out set
- Especially with web-trained LLMs

---
## Practical Tips

- Match input preprocessing exactly
- Use the same normalization as pretraining
- Resize images correctly
- Tokenize text with the model's tokenizer

---
## Common Pitfalls

- Different image normalization than pretraining
- Wrong tokenizer for the model
- Training the head with backbone unfrozen first
- Catastrophic forgetting from high lr

---
## Cost of Transfer Learning

- Downloading large checkpoints
- GPU memory for huge backbones
- Inference cost in production
- License terms on weights

---
## Licensing Matters

- Not all pretrained weights are commercially usable
- Read the license before shipping
- Some require attribution
- Some forbid certain uses

---
## Summary

- Transfer learning reuses pretrained features
- Feature extraction is cheap, fine-tuning is stronger
- Low learning rates protect pretrained weights
- PEFT lets you fine-tune huge models cheaply
