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
# PEFT for Image Generating Models — DreamBooth & Textual Inversion

---

## Customizing Image Models: Overview

Why customize? To generate images of **your specific** concepts:

---

## Customizing Image Models

![customizing_image_models_1](svg/courses/ai/generative-ai-applications/17_peft_image_models/customizing_image_models_1.svg)

---

## Customizing Image Models (2)

![customizing_image_models_2](svg/courses/ai/generative-ai-applications/17_peft_image_models/customizing_image_models_2.svg)

---

## DreamBooth — How It Works

![dreambooth_how_it_works](svg/courses/ai/generative-ai-applications/17_peft_image_models/dreambooth_how_it_works.svg)

---

## DreamBooth Implementation

```python
from diffusers import StableDiffusionPipeline, DDPMScheduler
from diffusers.training_utils import dreambooth_training
import torch

# Step 1: Prepare training data
# Place 3-5 images of your subject in a directory:
# instance_data_dir/
# ├── photo1.jpg
# ├── photo2.jpg
# ├── photo3.jpg
# ├── photo4.jpg
# └── photo5.jpg

# Step 2: Use the diffusers training script
# Command line:
# accelerate launch train_dreambooth.py \
#   --pretrained_model_name_or_path="stabilityai/stable-diffusion-xl-base-1.0" \
#   --instance_data_dir="./my_dog_photos" \
#   --output_dir="./dreambooth_model" \
#   --instance_prompt="a photo of sks dog" \
#   --class_prompt="a photo of a dog" \
#   --resolution=1024 \
#   --train_batch_size=1 \
#   --gradient_accumulation_steps=1 \
#   --learning_rate=5e-6 \
#   --max_train_steps=800 \
#   --with_prior_preservation \
#   --prior_loss_weight=1.0 \
#   --num_class_images=200
```

---

## DreamBooth with LoRA

```python
# DreamBooth + LoRA: Much smaller fine-tuned model
# Standard DreamBooth: ~5GB model copy
# DreamBooth + LoRA: ~50MB adapter

# accelerate launch train_dreambooth_lora.py \
#   --pretrained_model_name_or_path="stabilityai/stable-diffusion-xl-base-1.0" \
#   --instance_data_dir="./my_dog_photos" \
#   --output_dir="./dreambooth_lora" \
#   --instance_prompt="a photo of sks dog" \
#   --resolution=1024 \
#   --train_batch_size=1 \
#   --learning_rate=1e-4 \
#   --max_train_steps=500 \
#   --rank=32

# Load and use
from diffusers import StableDiffusionXLPipeline

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
)
pipe.load_lora_weights("./dreambooth_lora")
pipe = pipe.to("cuda")

image = pipe("a photo of sks dog riding a skateboard").images[0]
```

---

## Prior Preservation Loss: Overview

Prevents the model from forgetting how to draw the class in general:

---

## Prior Preservation Loss

![prior_preservation_loss](svg/courses/ai/generative-ai-applications/17_peft_image_models/prior_preservation_loss.svg)

---

## Textual Inversion: Overview

Instead of fine-tuning model weights, learn a **new word** in the text encoder:

---
## Textual Inversion

![textual_inversion](svg/courses/ai/generative-ai-applications/17_peft_image_models/textual_inversion.svg)

---
## Textual Inversion: Example

```misc
Model weights:  FROZEN (no changes)
Text encoder:   FROZEN (no changes)
New embedding:  TRAINABLE (768-dimensional vector)
Storage: Just the embedding vector (~3 KB!)
vs. DreamBooth: Full model copy (~5 GB)
vs. DreamBooth + LoRA: Adapter weights (~50 MB)
```

---

## Textual Inversion Implementation

```python
from diffusers import StableDiffusionPipeline
from diffusers.training_utils import textual_inversion_training

# Training command:
# accelerate launch textual_inversion.py \
#   --pretrained_model_name_or_path="runwayml/stable-diffusion-v1-5" \
#   --train_data_dir="./my_style_images" \
#   --learnable_property="style" \
#   --placeholder_token="<my-art-style>" \
#   --initializer_token="painting" \
#   --resolution=512 \
#   --train_batch_size=1 \
#   --learning_rate=5e-04 \
#   --max_train_steps=3000

# Use the learned concept
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
)
pipe.load_textual_inversion("./learned_embeds.safetensors")

image = pipe("A mountain landscape in <my-art-style>").images[0]
```

---

## Comparing Personalization Methods

| Method | Trainable | Storage | Quality | Training | Compose? |
|--------|-----------|---------|---------|----------|----------|
| DreamBooth | Full model | ~5 GB | ★★★★★ | 30-60 min | No |
| DB + LoRA | LoRA adapters | ~50 MB | ★★★★☆ | 15-30 min | Yes |
| Textual Inv. | 1 embedding | ~3 KB | ★★★☆☆ | 30-60 min | Yes |

**Composability:**
```misc
Textual Inversion allows combining concepts:
  "<my-dog> sitting in <my-room> painted by <my-style>"
  All three learned embeddings work together!

DreamBooth + LoRA:
  Can load multiple LoRA adapters with different weights
  pipe.load_lora_weights("dog_lora", weight=0.8)
  pipe.load_lora_weights("style_lora", weight=0.5)
```

---

## LoRA for Stable Diffusion — Training Details

```python
# Training LoRA for Stable Diffusion style transfer
# Using the diffusers training script

# Prepare style dataset: 20-50 images in your desired style

config = {
    "pretrained_model": "stabilityai/stable-diffusion-xl-base-1.0",
    "train_data_dir": "./style_images/",
    "output_dir": "./style_lora/",

    # LoRA configuration
    "lora_rank": 32,           # Rank of LoRA matrices
    "lora_alpha": 32,          # Scaling factor

    # Training
    "resolution": 1024,
    "train_batch_size": 1,
    "gradient_accumulation_steps": 4,
    "learning_rate": 1e-4,
    "lr_scheduler": "cosine",
    "max_train_steps": 1000,

    # Memory optimization
    "mixed_precision": "fp16",
    "gradient_checkpointing": True,
    "use_8bit_adam": True,      # Saves ~30% memory

    # Caption prefix for all training images
    "instance_prompt": "artwork in <lora_style> style",
}
```

---

## Generating with Multiple LoRA Adapters

```python
from diffusers import StableDiffusionXLPipeline

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
).to("cuda")

# Load and combine multiple LoRA adapters
pipe.load_lora_weights(
    "my_subject_lora/",
    adapter_name="subject",
)
pipe.load_lora_weights(
    "my_style_lora/",
    adapter_name="style",
)

# Set weights for each adapter
pipe.set_adapters(
    ["subject", "style"],
    adapter_weights=[0.8, 0.6],
)

# Generate with combined effect
image = pipe(
    "A portrait of sks person in watercolor style, "
    "golden hour lighting, detailed background",
    num_inference_steps=30,
    guidance_scale=7.5,
).images[0]
```

---

## Exercise: Personalize an Image Model

```python
"""
Exercise: Create a personalized image generation model.

Option A — DreamBooth with LoRA:
1. Collect 5-10 images of a subject (your pet, a product, etc.)
2. Fine-tune SDXL with DreamBooth + LoRA
3. Generate the subject in 5 different scenarios
4. Experiment with different guidance scales

Option B — Textual Inversion:
1. Collect 5-10 images representing an art style
2. Train a textual inversion embedding
3. Apply the learned style to different subjects
4. Compare quality with the original style

For both:
- Monitor training loss
- Compare outputs at different training steps (200, 500, 1000)
- Experiment with the prompt to test generalization
"""
```

---

## Key Takeaways — PEFT for Image Models

1. **DreamBooth** fine-tunes the full model for subject fidelity
1. **DreamBooth + LoRA** achieves similar quality with ~50MB adapters
1. **Textual Inversion** learns a new word embedding (~3KB)
1. **Prior preservation** prevents catastrophic forgetting
1. **Multiple LoRA adapters** can be composed at runtime
1. Only **3-5 images** are needed for personalization
1. **ControlNet** adds spatial control complementary to personalization
1. Choose the method based on quality needs vs. storage constraints

---

## IP-Adapter — Image Prompt Adapter

Use reference images as prompts alongside text:

```python
from diffusers import StableDiffusionXLPipeline
from diffusers.utils import load_image

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
)
pipe.load_ip_adapter(
    "h94/IP-Adapter",
    subfolder="sdxl_models",
    weight_name="ip-adapter_sdxl.safetensors",
)

# Use a reference image to guide style
reference = load_image("style_reference.png")

image = pipe(
    prompt="A landscape with mountains",
    ip_adapter_image=reference,     # Style reference
    scale=0.6,                       # Reference influence
    num_inference_steps=30,
).images[0]

# Combines: text prompt (content) + image prompt (style)
# No training required — works out of the box!
```

---

## T2I-Adapter — Lightweight ControlNet Alternative

![t2i_adapter_lightweight_controlnet_alternative](svg/courses/ai/generative-ai-applications/17_peft_image_models/t2i_adapter_lightweight_controlnet_alternative.svg)

---

## Training a Style LoRA — Step by Step

```misc
Complete workflow for creating a style LoRA:

1. COLLECT IMAGES (15-30 images)
   - Consistent art style
   - Various subjects (don't let subject dominate)
   - Good quality, high resolution
   - Diverse compositions

2. CAPTION IMAGES
   - Use BLIP-2 or CogVLM for auto-captioning
   - Add style trigger word: "in xyz_style style"
   - Review and correct captions manually

3. CONFIGURE TRAINING
   - Rank: 32-64 for style (higher = more style detail)
   - LR: 1e-4 to 5e-4
   - Steps: 1000-3000 (depends on dataset size)
   - Resolution: match model's native (1024 for SDXL)

4. TRAIN
   - Monitor loss curve
   - Generate test images every 200 steps
   - Watch for overfitting (test images look like training)

5. TEST AND SHARE
   - Test with diverse prompts
   - Adjust LoRA weight (0.5-1.0) for best results
   - Upload to CivitAI or HuggingFace Hub
```

---

## Auto-Captioning for Training Data

```python
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import os

# Load captioning model
processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-large"
)
caption_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-large",
    torch_dtype=torch.float16,
).to("cuda")

def caption_images(image_dir, trigger_word="sks_style"):
    """Generate captions for all images in a directory."""
    for filename in os.listdir(image_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image = Image.open(os.path.join(image_dir, filename))
            inputs = processor(image, return_tensors="pt").to("cuda")

            with torch.no_grad():
                ids = caption_model.generate(**inputs, max_new_tokens=50)
            caption = processor.decode(ids[0], skip_special_tokens=True)

            # Add trigger word
            caption = f"{caption}, in {trigger_word} style"

            # Save caption file (same name, .txt extension)
            txt_path = os.path.splitext(
                os.path.join(image_dir, filename)
            )[0] + ".txt"
            with open(txt_path, "w") as f:
                f.write(caption)
            print(f"{filename}: {caption}")
```

---

## Evaluating Personalized Image Models

```python
def evaluate_personalization(pipe, trigger_word, test_prompts,
                              reference_images):
    """Evaluate how well the model learned a concept."""
    results = []

    for prompt in test_prompts:
        # Generate image
        image = pipe(
            prompt.format(trigger=trigger_word),
            num_inference_steps=30,
            guidance_scale=7.5,
        ).images[0]

        # Evaluate with CLIP
        # 1. Text-image alignment (does it match the prompt?)
        clip_score = compute_clip_score(image, prompt)

        # 2. Identity preservation (does it look like the subject?)
        identity_score = compute_identity_similarity(
            image, reference_images
        )

        results.append({
            "prompt": prompt,
            "clip_score": clip_score,
            "identity_score": identity_score,
        })

    avg_clip = sum(r["clip_score"] for r in results) / len(results)
    avg_identity = sum(r["identity_score"] for r in results) / len(results)
    print(f"Avg CLIP score: {avg_clip:.4f} (text alignment)")
    print(f"Avg Identity: {avg_identity:.4f} (subject fidelity)")
    return results
```

---

## Common Pitfalls in Image Model Fine-Tuning

```misc
1. OVERFITTING (most common)
   Symptoms: Generated images look exactly like training images
   Fix: Reduce training steps, lower learning rate, add regularization

2. CONCEPT BLEEDING
   Symptoms: Trigger word affects ALL generations,
   even without the trigger
   Fix: Use prior preservation, reduce training steps

3. STYLE COLLAPSE
   Symptoms: Model can only generate one style/pose
   Fix: More diverse training images, reduce epochs

4. POOR GENERALIZATION
   Symptoms: Subject only works in poses seen during training
   Fix: More diverse training angles, increase rank

5. QUALITY DEGRADATION
   Symptoms: Overall image quality drops after training
   Fix: Lower learning rate, fewer steps, use LoRA (not full FT)

DEBUGGING CHECKLIST:
☐ Generate test images every 200 steps during training
☐ Compare base model output before/after
☐ Test with and without the trigger word
☐ Try varied prompts (different styles, settings)
```
