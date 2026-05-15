---
tags:
  - data-and-ai:deep-learning
level: intermediate
category: machine-learning
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Generative Adversarial Networks

---
## What This Chapter Covers

- Generator and discriminator architecture
- Training dynamics and stability
- DCGAN and StyleGAN overview
- Applications of generative models
- Introduction to diffusion models

---
## Generative vs Discriminative

- Discriminative: predict labels given inputs
- Generative: produce new samples from a distribution
- GANs learn to mimic real data
- A different ML goal entirely

---
## The GAN Idea

- Two networks playing a game
- Generator: makes fake samples
- Discriminator: tells real from fake
- Both improve as they compete

---
## GAN Architecture

![gan_architecture](svg/courses/machine_learning/deep-learning-fundamentals/07_gans/gan_architecture.svg)

---
## The Generator

- Input: random noise vector
- Output: a sample (image, audio, ...)
- Usually a deep network with upsampling
- Goal: fool the discriminator

---
## The Discriminator

- Input: a sample, real or fake
- Output: probability of being real
- Usually a classifier network
- Goal: tell them apart

---
## The Minimax Game

- Generator minimizes discriminator success
- Discriminator maximizes its accuracy
- They share a single value function
- Equilibrium: discriminator at 50/50

---
## Training Loop

- Sample real images from data
- Sample noise, generate fakes
- Update discriminator on both
- Update generator to fool discriminator

---
## GAN Training Loop

![gan_training](svg/courses/machine_learning/deep-learning-fundamentals/07_gans/gan_training.svg)

---
## Loss Functions

- Original: log loss for both networks
- Practical: non-saturating generator loss
- Wasserstein: Earth Mover's distance
- LSGAN, hinge loss, and others

---
## Why Original Loss Saturates

- Early generator outputs look obviously fake
- Discriminator wins easily
- Generator gradient vanishes
- Non-saturating loss fixes this

---
## Training Is Hard

- Two networks must improve together
- Hyperparameters sensitive
- Loss curves are not informative
- Visual inspection is essential

---
## Mode Collapse

- Generator produces only a few outputs
- All inputs map to the same fake
- Discriminator is fooled but diversity is lost
- A signature GAN failure mode

---
## Fixing Mode Collapse

- Different loss (Wasserstein, hinge)
- Mini-batch discrimination
- Spectral normalization
- Two-timescale updates

---
## Training Stability Tricks

- Balanced learning rates per network
- Spectral norm on discriminator
- Gradient penalty
- Exponential moving average of generator weights

---
## DCGAN

- Deep Convolutional GAN
- Radford et al, 2015
- All-convolutional architecture
- Set practical training conventions

---
## DCGAN Guidelines

- Strided conv instead of pooling
- Batch norm in both networks
- ReLU in generator, LeakyReLU in discriminator
- Tanh output, normalize inputs to [-1, 1]

---
## Conditional GANs

- Condition on a label or input
- Generator: noise plus condition
- Discriminator: sees the condition too
- Controllable generation

---
## Pix2Pix

- Image-to-image translation
- Paired training data
- Generator is U-Net shaped
- Discriminator is a PatchGAN

---
## CycleGAN

- Image translation without pairs
- Two generators, two discriminators
- Cycle consistency loss
- Horses to zebras, summer to winter

---
## StyleGAN

- Karras et al, 2018 and beyond
- Disentangled latent space
- Style mixing across layers
- State of the art face generation for years

---
## StyleGAN Tricks

- Mapping network from noise to W space
- AdaIN style injection per layer
- Progressive growing of resolution
- Path length regularization

---
## Progressive Growing

- Start at low resolution
- Add layers gradually during training
- More stable than training huge nets from scratch
- Used in early StyleGAN and ProGAN

---
## Evaluating GANs

- No single perfect metric
- Inception Score: quality and diversity
- FID: distance between feature distributions
- Human evaluation still important

---
## FID

- Frechet Inception Distance
- Compare feature distributions of real and fake
- Lower is better
- The de facto standard for image GANs

---
## GAN Applications

- Face generation and editing
- Super-resolution
- Image inpainting
- Domain transfer

---
## Beyond Images

- Music generation
- Voice cloning
- Tabular data synthesis
- Privacy-preserving synthetic data

---
## Other Generative Models

- VAEs: variational autoencoders
- Autoregressive: PixelRNN, PixelCNN, language models
- Normalizing flows: exact likelihood
- Diffusion: noise then denoise

---
## VAE in One Slide

- Encode to a distribution, not a point
- Sample from the distribution
- Decode back to a sample
- Smooth, structured latent space

---
## Autoregressive Generation

- Generate one pixel or token at a time
- Each step conditions on previous
- Sharp samples, slow inference
- Foundation of large language models

---
## Diffusion Models

- New dominant approach since ~2020
- Outperform GANs in image quality
- Powers Stable Diffusion, DALL-E, Imagen
- Different training dynamic

---
## Diffusion Idea

- Add noise to data step by step
- Train a network to reverse the noise
- Generate by sampling noise and denoising
- Easier to train than GANs

---
## Diffusion Diagram

![diffusion](svg/courses/machine_learning/deep-learning-fundamentals/07_gans/diffusion.svg)

---
## Forward Process

- Start with a real sample
- Add Gaussian noise at each timestep
- After enough steps: pure noise
- Fixed, no learning here

---
## Reverse Process

- Learn to predict the noise added
- Subtract predicted noise step by step
- Many steps from noise to image
- This is the model we train

---
## Latent Diffusion

- Run diffusion in a compressed latent space
- Much cheaper than pixel-space diffusion
- Stable Diffusion's key idea
- Pair with a VAE for encoding and decoding

---
## Conditioning Diffusion

- Text conditioning via cross-attention
- Use a text encoder like CLIP or T5
- Classifier-free guidance for strength
- The "prompt" knob in image generators

---
## Classifier-Free Guidance

- Train with and without conditioning
- At inference, mix the two predictions
- Higher weight: more prompt-faithful
- Standard trick in modern text-to-image

---
## Speeding Up Diffusion

- Original: hundreds of steps
- DDIM, DPM-Solver: tens of steps
- Distillation to single-digit steps
- Consistency models: one step possible

---
## GANs vs Diffusion

- GANs: fast inference, hard to train
- Diffusion: easy to train, slow inference
- Diffusion currently leads on quality
- GANs still strong for specialized fast use cases

---
## Ethical Considerations

- Deepfakes and misinformation
- Copyright of training data
- Consent and likeness rights
- Watermarking and provenance

---
## Safety in Generative Models

- Content filters at input and output
- Guardrails on prompts and outputs
- Provenance signals like C2PA
- Continuous review and red-teaming

---
## When to Reach for a GAN

- Speed-critical inference
- Specific style transfer pipelines
- Mature codebases like StyleGAN
- When diffusion is overkill

---
## When to Use Diffusion

- High quality, controllable images
- Text-to-image generation
- Inpainting and editing
- When latency budget allows

---
## Practical Tips

- Start small and reproduce a known result
- Sample images during training, log them often
- Track FID periodically
- Save checkpoints generously

---
## Common Pitfalls

- Tuning learning rates blindly
- Ignoring mode collapse signs
- Training too long without checkpoints
- Mismatched normalization between train and inference

---
## Summary

- GANs pit a generator against a discriminator
- Training is delicate but capable of stunning results
- DCGAN and StyleGAN are key architectures
- Diffusion has largely taken the lead in 2020s generative modeling
