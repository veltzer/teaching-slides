---
tags:
  - data-and-ai:ai
  - data-and-ai:generative-ai
  - languages:python
  - data-and-ai:prompt-engineering
  - concepts:ethics
level: intermediate
category: ai
audience:
  - audiences:data-scientists

---

# Image Generation — Overview and Approaches

---

## Day 5: Image Generation & AI Safety

![day_5_image_generation_ai_safety](svg/courses/ai/generative-ai-applications/16_image_generation/day_5_image_generation_ai_safety.svg)

---

## Image Generation — A Brief History

![image_generation_a_brief_history](svg/courses/ai/generative-ai-applications/16_image_generation/image_generation_a_brief_history.svg)

---

## Generative Approaches Compared

![generative_approaches_compared](svg/courses/ai/generative-ai-applications/16_image_generation/generative_approaches_compared.svg)

---

## How Diffusion Models Work

![how_diffusion_models_work](svg/courses/ai/generative-ai-applications/16_image_generation/how_diffusion_models_work.svg)

---

## Diffusion — The Math

```misc
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

![stable_diffusion_architecture](svg/courses/ai/generative-ai-applications/16_image_generation/stable_diffusion_architecture.svg)

---

## Latent Diffusion — Why It's Efficient

![latent_diffusion_why_it_s_efficient](svg/courses/ai/generative-ai-applications/16_image_generation/latent_diffusion_why_it_s_efficient.svg)

---

## CLIP — Connecting Text and Images

![clip_connecting_text_and_images](svg/courses/ai/generative-ai-applications/16_image_generation/clip_connecting_text_and_images.svg)

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

![controlnet_fine_grained_control](svg/courses/ai/generative-ai-applications/16_image_generation/controlnet_fine_grained_control.svg)

---

## ControlNet — Fine-Grained Control: Example

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
1. **Latent diffusion** operates in compressed space for efficiency
1. **CLIP** connects text and images, enabling text-to-image generation
1. **Guidance scale** controls text adherence vs. image quality
1. **ControlNet** adds spatial control (edges, depth, pose)
1. **Inpainting** enables selective editing of image regions
1. Both **API-based** (DALL-E 3) and **local** (Stable Diffusion) options exist
1. The field is rapidly evolving toward video generation

---

## Noise Schedulers Compared

![noise_schedulers_compared](svg/courses/ai/generative-ai-applications/16_image_generation/noise_schedulers_compared.svg)

---

## Noise Schedulers Compared: Example

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

```template
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

![text_to_3d_generation_emerging](svg/courses/ai/generative-ai-applications/16_image_generation/text_to_3d_generation_emerging.svg)

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

![comparing_image_generation_models](svg/courses/ai/generative-ai-applications/16_image_generation/comparing_image_generation_models.svg)
