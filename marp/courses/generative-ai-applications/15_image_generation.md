# Image Generation — Overview and Approaches

---

## Day 5: Image Generation & AI Safety

```text
Today's Roadmap:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 ┌──────────────────────────────────────────┐
 │ 1. Image generation approaches           │
 │ 2. PEFT for image models (DreamBooth,    │
 │    Textual Inversion)                    │
 │ 3. Measuring text generation quality     │
 │ 4. Bias in generative models             │
 │ 5. AI Safety and Deep Fakes              │
 └──────────────────────────────────────────┘
```

---

## Image Generation — A Brief History

```text
Timeline:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2014 │ GANs (Goodfellow)
     │ Generator vs. Discriminator adversarial training
     │
2015 │ DCGAN — Deep Convolutional GANs
     │ First realistic image generation
     │
2019 │ StyleGAN (NVIDIA) — photorealistic faces
     │
2020 │ DDPM — Denoising Diffusion Probabilistic Models
     │ Foundation of modern image generation
     │
2021 │ DALL-E (OpenAI) — text-to-image with transformers
     │ CLIP — connecting text and images
     │
2022 │ Stable Diffusion — open source diffusion model
     │ Midjourney — artistic image generation
     │
2023 │ SDXL, DALL-E 3, Midjourney v5
     │
2024 │ Flux, Stable Diffusion 3, DALL-E 3 + ChatGPT
     │
2025 │ Video generation (Sora, Runway Gen-3)
```

---

## Generative Approaches Compared

```text
┌──────────────┬───────────────────────────────────────┐
│ Approach     │ How It Works                          │
├──────────────┼───────────────────────────────────────┤
│ GANs         │ Two networks compete:                 │
│              │ Generator creates, Discriminator       │
│              │ judges. Adversarial training.           │
│              │ Fast inference, hard to train.          │
├──────────────┼───────────────────────────────────────┤
│ VAEs         │ Encode to latent space, decode back.   │
│              │ Probabilistic, smooth latent space.    │
│              │ Often blurry outputs.                  │
├──────────────┼───────────────────────────────────────┤
│ Diffusion    │ Gradually add noise, learn to reverse. │
│              │ High quality, slow inference.          │
│              │ Dominates current SOTA.                │
├──────────────┼───────────────────────────────────────┤
│ Autoregressive│ Generate pixels/tokens sequentially.  │
│              │ Very slow but high quality.            │
│              │ Used in DALL-E 1.                      │
├──────────────┼───────────────────────────────────────┤
│ Flow-based   │ Invertible transformations.            │
│              │ Exact likelihood, good for editing.    │
│              │ Used in Flux, Stable Diffusion 3.     │
└──────────────┴───────────────────────────────────────┘
```

---

## How Diffusion Models Work

```text
FORWARD PROCESS (adding noise):
  Image → slightly noisy → more noisy → ... → pure noise
  x₀ ──────────────────────────────────────────> xₜ

  Step 0     Step 100    Step 500    Step 1000
  ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐
  │ 🐱   │   │ 🐱~  │   │ ~~?  │   │ ████ │
  │clear │   │faint │   │barely│   │noise │
  └──────┘   └──────┘   └──────┘   └──────┘

REVERSE PROCESS (removing noise — learned by model):
  Pure noise → slightly less noisy → ... → clear image
  xₜ ──────────────────────────────────────────> x₀

  The model learns: given noisy image at step t,
  predict what the noise looks like, then subtract it.
```

---

## Diffusion — The Math

```text
Forward process (fixed):
  q(xₜ | xₜ₋₁) = N(xₜ; √(1-βₜ) xₜ₋₁, βₜ I)

  At step t, add a small amount of Gaussian noise.
  βₜ is the noise schedule (increases over time).

Reverse process (learned):
  pθ(xₜ₋₁ | xₜ) = N(xₜ₋₁; μθ(xₜ, t), σₜ² I)

  A neural network predicts the noise to subtract.

Training objective:
  L = E[‖ε - εθ(xₜ, t)‖²]

  "Predict the noise that was added at step t"
```

```python
# Simplified training step
def diffusion_training_step(model, images, noise_scheduler):
    noise = torch.randn_like(images)
    timesteps = torch.randint(0, 1000, (images.shape[0],))
    noisy_images = noise_scheduler.add_noise(images, noise, timesteps)
    noise_pred = model(noisy_images, timesteps)
    loss = F.mse_loss(noise_pred, noise)
    return loss
```

---

## Stable Diffusion Architecture

```text
┌─────────────────────────────────────────────────────┐
│              STABLE DIFFUSION                        │
│                                                      │
│  Text: "A cat wearing a top hat, oil painting"       │
│         │                                            │
│         ▼                                            │
│  ┌──────────────┐                                    │
│  │ CLIP Text     │  Text → embedding vector           │
│  │ Encoder       │                                    │
│  └──────┬───────┘                                    │
│         │ text embedding                              │
│         ▼                                            │
│  ┌──────────────┐     ┌──────────────┐               │
│  │   U-Net      │     │   Noise      │               │
│  │  (denoiser)  │◄────│  Scheduler   │               │
│  │              │     │  (50 steps)  │               │
│  └──────┬───────┘     └──────────────┘               │
│         │ latent representation                       │
│         ▼                                            │
│  ┌──────────────┐                                    │
│  │   VAE        │  Latent → pixel space               │
│  │   Decoder    │                                    │
│  └──────┬───────┘                                    │
│         │                                            │
│         ▼                                            │
│     Generated Image (512×512 or 1024×1024)           │
└─────────────────────────────────────────────────────┘
```

---

## Latent Diffusion — Why It's Efficient

```text
Pixel-space diffusion:
  512 × 512 × 3 = 786,432 values
  Very expensive to process!

Latent-space diffusion:
  VAE encoder: 512×512×3 → 64×64×4 = 16,384 values
  48× less data to process!

┌────────────────┐     ┌──────────┐     ┌────────────────┐
│ Original Image │     │ Latent   │     │ Reconstructed  │
│ 512 × 512 × 3 │────>│ 64×64×4  │────>│ 512 × 512 × 3 │
│                │ VAE │          │ VAE │                │
│                │ Enc │ Diffusion│ Dec │                │
│                │     │ happens  │     │                │
│                │     │  HERE    │     │                │
└────────────────┘     └──────────┘     └────────────────┘

The diffusion process operates entirely in latent space.
This is why it's called "Latent Diffusion Model" (LDM).
```

---

## CLIP — Connecting Text and Images

```text
CLIP (Contrastive Language-Image Pre-training):

Training:
  Match text descriptions with their corresponding images
  in a shared embedding space.

  ┌──────────┐        ┌──────────┐
  │ "A dog"  │        │ [photo]  │
  │ Text     │        │ Image    │
  │ Encoder  │        │ Encoder  │
  └────┬─────┘        └────┬─────┘
       │                    │
       ▼                    ▼
  [0.3, -0.1, ...]   [0.3, -0.1, ...]
       │                    │
       └────────┬───────────┘
                │
           cosine similarity
           (maximize for matching pairs)

Uses in Stable Diffusion:
  - Text encoder: converts prompt to embedding
  - Guides the diffusion process toward the text description
  - Enables text-to-image generation
```

---

## Using Stable Diffusion with `Diffusers`

```python
from diffusers import StableDiffusionPipeline
import torch

# Load model
pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16",
)
pipe = pipe.to("cuda")

# Generate image
image = pipe(
    prompt="A serene Japanese garden with cherry blossoms, "
           "watercolor painting style, golden hour lighting",
    negative_prompt="blurry, low quality, distorted",
    num_inference_steps=30,    # More steps = higher quality
    guidance_scale=7.5,        # How closely to follow prompt
    width=1024,
    height=1024,
).images[0]

image.save("japanese_garden.png")

# Guidance scale:
# 1.0 = ignore text (random image)
# 7-8 = balanced (recommended)
# 15+ = strongly follows text (may reduce quality)
```

---

## Image-to-Image Generation

```python
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
)
pipe = pipe.to("cuda")

# Load an existing image
init_image = Image.open("sketch.png").resize((1024, 1024))

# Transform it
image = pipe(
    prompt="A detailed oil painting of a medieval castle",
    image=init_image,
    strength=0.75,     # 0=keep original, 1=fully regenerate
    guidance_scale=7.5,
    num_inference_steps=30,
).images[0]

image.save("castle_painting.png")

# Use cases:
# - Style transfer (sketch → painting)
# - Image enhancement
# - Concept variation
# - Color palette changes
```

---

## Inpainting — Editing Parts of an Image

```python
from diffusers import StableDiffusionInpaintPipeline
from PIL import Image

pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
)
pipe = pipe.to("cuda")

# Load image and mask
image = Image.open("photo.png").resize((1024, 1024))
mask = Image.open("mask.png").resize((1024, 1024))
# Mask: white areas will be regenerated

result = pipe(
    prompt="A golden retriever sitting on the grass",
    image=image,
    mask_image=mask,
    guidance_scale=7.5,
    num_inference_steps=30,
).images[0]

# The model regenerates ONLY the masked area
# while keeping the rest of the image intact
```

---

## ControlNet — Fine-Grained Control

```text
ControlNet adds spatial control to diffusion:

Input: Text prompt + Control signal

Control types:
┌──────────────┬────────────────────────────────┐
│ Canny Edge   │ Generate from edge map          │
│ Depth Map    │ Generate matching depth          │
│ Pose         │ Generate matching human pose     │
│ Segmentation │ Generate from semantic map       │
│ Scribble     │ Generate from rough sketch       │
│ Normal Map   │ Generate matching surface normal │
└──────────────┴────────────────────────────────┘
```

```python
from diffusers import ControlNetModel, StableDiffusionControlNetPipeline

controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/control_v11p_sd15_canny",
    torch_dtype=torch.float16,
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float16,
)

# edge_image = detected edges from input photo
result = pipe("a beautiful house", image=edge_image).images[0]
```

---

## Image Generation APIs

```python
# OpenAI DALL-E 3
from openai import OpenAI
client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="A futuristic city at sunset, cyberpunk style",
    size="1024x1024",
    quality="hd",
    n=1,
)
image_url = response.data[0].url

# Stability AI API
import requests

response = requests.post(
    "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "text_prompts": [{"text": "A serene mountain landscape"}],
        "cfg_scale": 7,
        "steps": 30,
        "width": 1024,
        "height": 1024,
    },
)
```

---

## Key Takeaways — Image Generation

1. **Diffusion models** dominate current image generation (replacing GANs)
2. **Latent diffusion** operates in compressed space for efficiency
3. **CLIP** connects text and images, enabling text-to-image generation
4. **Guidance scale** controls text adherence vs. image quality
5. **ControlNet** adds spatial control (edges, depth, pose)
6. **Inpainting** enables selective editing of image regions
7. Both **API-based** (DALL-E 3) and **local** (Stable Diffusion) options exist
8. The field is rapidly evolving toward video generation

---

## Noise Schedulers Compared

```text
Different schedulers control how noise is added/removed:

Scheduler      Steps    Quality    Speed
─────────────────────────────────────────────
DDPM           1000     ★★★★★    Slowest
DDIM           50       ★★★★     Medium
PNDM           50       ★★★★     Medium
Euler          30       ★★★★     Fast
Euler Ancestral 30      ★★★★½    Fast
DPM++ 2M       20       ★★★★½    Very fast
DPM++ SDE      20       ★★★★★    Fast
LCM            4-8      ★★★½     Fastest
```

```python
from diffusers import (
    DDPMScheduler, DDIMScheduler,
    EulerDiscreteScheduler, DPMSolverMultistepScheduler
)

# Switch scheduler on an existing pipeline
pipe.scheduler = DPMSolverMultistepScheduler.from_config(
    pipe.scheduler.config
)
# Now generates in 20 steps instead of 50!
```

---

## Latent Consistency Models (LCM) — Ultra-Fast Generation

```python
from diffusers import LatentConsistencyModelPipeline

pipe = LatentConsistencyModelPipeline.from_pretrained(
    "SimianLuo/LCM_Dreamshaper_v7",
    torch_dtype=torch.float16,
)
pipe = pipe.to("cuda")

# Generate in just 4 steps! (~0.5 seconds)
image = pipe(
    prompt="A beautiful mountain landscape at sunset",
    num_inference_steps=4,    # vs. 30-50 for standard SD
    guidance_scale=1.0,       # LCM works best with low guidance
).images[0]

# Comparison:
# Standard SD (30 steps):  ~3 seconds on A100
# LCM (4 steps):           ~0.5 seconds on A100
# That's 6× faster — enables real-time generation!
```

---

## Prompt Engineering for Image Generation

```text
EFFECTIVE IMAGE PROMPTS:

Structure:
  [Subject] + [Style] + [Details] + [Lighting] + [Quality]

Example:
  "A majestic lion sitting on a throne,
   digital art style,
   intricate golden details, jeweled crown,
   dramatic rim lighting, dark background,
   highly detailed, 8k resolution, artstation"

NEGATIVE PROMPTS (what to avoid):
  "blurry, low quality, distorted, deformed,
   bad anatomy, bad proportions, extra limbs,
   duplicate, watermark, text, signature"

STYLE KEYWORDS:
  Photorealistic: "photo, 35mm, f/1.8, bokeh, RAW"
  Digital art:    "digital painting, concept art, artstation"
  Anime:          "anime style, cel shading, vibrant"
  Oil painting:   "oil on canvas, impasto, gallery quality"
  Watercolor:     "watercolor, soft edges, paper texture"
```

---

## SDXL Turbo and Real-Time Generation

```python
from diffusers import AutoPipelineForText2Image

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo",
    torch_dtype=torch.float16,
)
pipe = pipe.to("cuda")

# Real-time generation (1 step!)
image = pipe(
    prompt="A cat wearing sunglasses",
    num_inference_steps=1,
    guidance_scale=0.0,  # Turbo doesn't need guidance
).images[0]

# This enables:
# - Interactive image editing
# - Live image generation from text input
# - Real-time style transfer
# - Video frame generation

# Performance on A100:
# 1 step:  ~50ms (20 FPS)
# 4 steps: ~200ms (5 FPS)
```

---

## Image-to-Video with Stable Video Diffusion

```python
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import load_image, export_to_video

pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt",
    torch_dtype=torch.float16,
)
pipe = pipe.to("cuda")

# Animate a static image
image = load_image("landscape.png").resize((1024, 576))

frames = pipe(
    image,
    decode_chunk_size=4,
    num_frames=25,           # 25 frames = ~1 second
    motion_bucket_id=127,    # Controls amount of motion
).frames[0]

export_to_video(frames, "animated_landscape.mp4", fps=7)

# Current limitations:
# - Short clips only (1-4 seconds)
# - Limited control over motion
# - High VRAM requirements (~40GB)
# - Quality varies significantly
```

---

## Text-to-3D Generation (Emerging)

```text
Emerging approaches to 3D generation:

1. Score Distillation Sampling (DreamFusion)
   Text → optimize 3D representation using 2D diffusion
   Slow but produces real 3D models

2. Multi-view Generation (Zero123++)
   Text → multiple views → 3D reconstruction
   Faster, good for simple objects

3. Direct 3D Generation (Point-E, Shap-E)
   Text → 3D point cloud or mesh directly
   Fastest, lower quality

4. Gaussian Splatting
   Multiple images → 3D Gaussian representation
   Very fast rendering, high quality

Applications:
  - Game asset generation
  - Product prototyping
  - Architecture visualization
  - AR/VR content creation
  - E-commerce product views
```

---

## Flux — Next-Generation Image Model

```python
# Flux: Flow-based model from Black Forest Labs
from diffusers import FluxPipeline

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.bfloat16,
)
pipe = pipe.to("cuda")

image = pipe(
    prompt="A photorealistic portrait of a woman reading "
           "a book in a cozy library, warm lighting, "
           "depth of field, 35mm film",
    num_inference_steps=30,
    guidance_scale=3.5,     # Lower than SD (Flux works differently)
    height=1024,
    width=1024,
).images[0]

# Flux advantages over Stable Diffusion:
# - Better text rendering in images
# - More photorealistic outputs
# - Better understanding of spatial relationships
# - Improved hands and faces
# - Flow-matching (not diffusion) — different math
```

---

## Comparing Image Generation Models

```text
┌──────────────┬────────────┬───────────┬───────────┬──────────┐
│ Model        │ Quality    │ Speed     │ Open?     │ Cost     │
├──────────────┼────────────┼───────────┼───────────┼──────────┤
│ DALL-E 3     │ ★★★★★     │ ~10s      │ No        │ $0.04-   │
│              │            │           │           │ $0.12/img│
├──────────────┼────────────┼───────────┼───────────┼──────────┤
│ Midjourney   │ ★★★★★     │ ~30s      │ No        │ $10-60/  │
│ v6           │            │           │           │ month    │
├──────────────┼────────────┼───────────┼───────────┼──────────┤
│ Flux.1 Dev   │ ★★★★½     │ ~8s       │ Yes*      │ Self-host│
├──────────────┼────────────┼───────────┼───────────┼──────────┤
│ SDXL         │ ★★★★      │ ~5s       │ Yes       │ Self-host│
├──────────────┼────────────┼───────────┼───────────┼──────────┤
│ SD 3.5       │ ★★★★½     │ ~6s       │ Yes       │ Self-host│
├──────────────┼────────────┼───────────┼───────────┼──────────┤
│ SDXL Turbo   │ ★★★½      │ ~0.5s     │ Yes       │ Self-host│
└──────────────┴────────────┴───────────┴───────────┴──────────┘
* Flux.1 Dev: open weights but non-commercial license
  Flux.1 Schnell: Apache 2.0 (fully open)
```
