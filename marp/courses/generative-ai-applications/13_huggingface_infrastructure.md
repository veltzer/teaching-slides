# Using HuggingFace Infrastructure and LangChain

---

## The HuggingFace Ecosystem

```
┌──────────────────────────────────────────────────────┐
│                HUGGINGFACE ECOSYSTEM                  │
│                                                       │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │    Hub      │  │ Transformers │  │  Datasets   │ │
│  │ 500K+ models│  │ Load & run   │  │ 100K+       │ │
│  │ Model cards │  │ any model    │  │ datasets    │ │
│  └─────────────┘  └──────────────┘  └─────────────┘ │
│                                                       │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │ Tokenizers  │  │  Accelerate  │  │    PEFT     │ │
│  │ Fast        │  │ Distributed  │  │ LoRA, QLoRA │ │
│  │ tokenization│  │ training     │  │ Adapters    │ │
│  └─────────────┘  └──────────────┘  └─────────────┘ │
│                                                       │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │   Spaces    │  │    TRL      │  │   Evaluate  │ │
│  │ Deploy apps │  │ RLHF/DPO    │  │ Benchmarks  │ │
│  └─────────────┘  └──────────────┘  └─────────────┘ │
└──────────────────────────────────────────────────────┘
```

---

## HuggingFace Hub — Finding Models

```python
from huggingface_hub import HfApi, list_models

api = HfApi()

# Search for models
models = api.list_models(
    task="text-generation",
    sort="downloads",
    direction=-1,
    limit=10,
)

for model in models:
    print(f"{model.id:40s} Downloads: {model.downloads:>10,}")

# Filter by specific criteria
models = api.list_models(
    search="llama instruct",
    library="transformers",
    sort="likes",
)

# Download a specific model
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    local_dir="./models/llama-3.1-8b",
    token="hf_...",  # For gated models
)
```

---

## HuggingFace Datasets

```python
from datasets import load_dataset

# Load a dataset
dataset = load_dataset("squad")
print(dataset)
# DatasetDict({
#     train: Dataset({num_rows: 87599, features: [...]})
#     validation: Dataset({num_rows: 10570, features: [...]})
# })

# Access data
print(dataset["train"][0])
# {'question': 'What is...', 'context': '...', 'answers': {...}}

# Filter and transform
filtered = dataset["train"].filter(
    lambda x: len(x["question"]) > 50
)

# Create your own dataset
from datasets import Dataset
my_data = Dataset.from_dict({
    "text": ["Hello world", "Goodbye world"],
    "label": [1, 0],
})

# Push to Hub
my_data.push_to_hub("my-username/my-dataset")
```

---

## Transformers Pipeline API

The simplest way to use models:

```python
from transformers import pipeline

# Text generation
generator = pipeline("text-generation",
    model="meta-llama/Llama-3.1-8B-Instruct",
    device_map="auto",
    torch_dtype="float16",
)

result = generator(
    "Explain machine learning in one paragraph.",
    max_new_tokens=200,
    temperature=0.7,
)
print(result[0]["generated_text"])

# Sentiment analysis
classifier = pipeline("sentiment-analysis")
result = classifier("I love this product!")
# [{'label': 'POSITIVE', 'score': 0.9998}]

# Summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
result = summarizer(long_text, max_length=100, min_length=30)

# Named Entity Recognition
ner = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)
result = ner("Elon Musk founded SpaceX in California")
```

---

## Text Embeddings with HuggingFace

```python
from transformers import AutoTokenizer, AutoModel
import torch

model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def get_embeddings(texts):
    """Generate embeddings for a list of texts."""
    inputs = tokenizer(
        texts, padding=True, truncation=True,
        max_length=512, return_tensors="pt"
    )

    with torch.no_grad():
        outputs = model(**inputs)

    # Mean pooling over token embeddings
    attention_mask = inputs["attention_mask"]
    embeddings = outputs.last_hidden_state
    mask_expanded = attention_mask.unsqueeze(-1).expand(embeddings.size())
    sum_embeddings = (embeddings * mask_expanded).sum(1)
    sum_mask = mask_expanded.sum(1).clamp(min=1e-9)
    return (sum_embeddings / sum_mask).numpy()

embeddings = get_embeddings([
    "How do I reset my password?",
    "I forgot my login credentials",
    "What is the weather today?"
])
# embeddings.shape = (3, 384)
```

---

## Using HuggingFace with LangChain

```python
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from langchain_chroma import Chroma

# Local embeddings (no API needed!)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cuda"},
)

# Create vector store with local embeddings
vectorstore = Chroma.from_texts(
    texts=["Document 1 content...", "Document 2 content..."],
    embedding=embeddings,
    persist_directory="./local_chroma",
)

# Local LLM via HuggingFace
from transformers import pipeline as hf_pipeline

pipe = hf_pipeline(
    "text-generation",
    model="mistralai/Mistral-7B-Instruct-v0.3",
    torch_dtype=torch.float16,
    device_map="auto",
)
local_llm = HuggingFacePipeline(pipeline=pipe)

# Full local RAG — no API calls at all!
chain = (
    {"context": vectorstore.as_retriever(), "question": RunnablePassthrough()}
    | rag_prompt | local_llm | StrOutputParser()
)
```

---

## HuggingFace Inference API

Use models without downloading them:

```python
from huggingface_hub import InferenceClient

client = InferenceClient(
    model="meta-llama/Llama-3.1-70B-Instruct",
    token="hf_...",
)

# Text generation
response = client.text_generation(
    "Explain quantum computing",
    max_new_tokens=200,
    temperature=0.7,
)
print(response)

# Chat completion (OpenAI-compatible format!)
response = client.chat_completion(
    messages=[
        {"role": "user", "content": "What is transformers?"}
    ],
    max_tokens=200,
)
print(response.choices[0].message.content)

# Embeddings
embeddings = client.feature_extraction(
    "Hello world", model="sentence-transformers/all-MiniLM-L6-v2"
)

# Image classification, object detection, etc.
result = client.image_classification("photo.jpg")
```

---

## HuggingFace Spaces — Deploying Demos

```python
# Create a Gradio app for your model
import gradio as gr
from transformers import pipeline

# Load model
generator = pipeline("text-generation",
    model="mistralai/Mistral-7B-Instruct-v0.3",
    device_map="auto",
    torch_dtype="float16",
)

def chat(message, history):
    """Chat function for Gradio interface."""
    messages = [{"role": "user", "content": msg}
                for msg, _ in history]
    messages.append({"role": "user", "content": message})

    response = generator(
        messages,
        max_new_tokens=256,
        temperature=0.7,
    )
    return response[0]["generated_text"][-1]["content"]

# Create and launch
demo = gr.ChatInterface(
    fn=chat,
    title="My Local LLM Chat",
    description="Chat with Mistral 7B locally",
)

demo.launch(share=True)  # Creates public URL
# Deploy to HuggingFace Spaces with: gradio deploy
```

---

## Model Evaluation with HuggingFace

```python
import evaluate

# Load metrics
bleu = evaluate.load("bleu")
rouge = evaluate.load("rouge")
accuracy = evaluate.load("accuracy")

# Evaluate text generation
predictions = ["The cat sat on the mat"]
references = [["The cat is sitting on the mat"]]

bleu_result = bleu.compute(
    predictions=predictions,
    references=references,
)
print(f"BLEU: {bleu_result['bleu']:.4f}")

rouge_result = rouge.compute(
    predictions=predictions,
    references=[r[0] for r in references],
)
print(f"ROUGE-L: {rouge_result['rougeL']:.4f}")

# Evaluate classification
accuracy_result = accuracy.compute(
    predictions=[0, 1, 1, 0, 1],
    references=[0, 1, 0, 0, 1],
)
print(f"Accuracy: {accuracy_result['accuracy']:.2%}")
```

---

## Exercise: Local RAG Pipeline

```python
"""
Exercise: Build a fully local RAG system.

Requirements:
- No API calls (everything runs locally)
- Use HuggingFace models for both embeddings and generation
- Index a set of documents
- Answer questions based on the documents

Steps:
1. Download and load a small model (Phi-3 3.8B or Mistral 7B)
2. Load local embeddings (all-MiniLM-L6-v2)
3. Create sample documents about a topic
4. Build ChromaDB index with local embeddings
5. Create RAG chain with LangChain
6. Test with 5 questions

Compare:
- Local model RAG vs. OpenAI API RAG
- Response quality
- Response time
- Cost (compute vs API)
"""
```

---

## Key Takeaways — HuggingFace & LangChain

1. `HuggingFace` Hub hosts 500K+ models and 100K+ datasets
2. **Transformers** library provides a unified API for all models
3. **Pipeline API** makes it simple to run models for common tasks
4. **Local embeddings** eliminate API costs for semantic search
5. `HuggingFace` **Inference API** runs models without local GPU
6. **Spaces** enables quick demo deployment with Gradio
7. `LangChain` integrates seamlessly with `HuggingFace` models
8. **Fully local** RAG pipelines are now practical and performant

---

## HuggingFace Model Cards

Understanding model documentation:

```
MODEL CARD SECTIONS:
━━━━━━━━━━━━━━━━━━━━

1. Model Description
   - Architecture, size, training data
   - Intended use cases

2. Training Details
   - Hardware used
   - Training duration
   - Hyperparameters
   - Data preprocessing

3. Evaluation Results
   - Benchmark scores (MMLU, HumanEval, etc.)
   - Comparison with similar models

4. Limitations
   - Known failure modes
   - Bias disclosures
   - Not suitable for...

5. License & Usage
   - Commercial vs. research use
   - Attribution requirements
```

```python
from huggingface_hub import ModelCard
card = ModelCard.load("meta-llama/Llama-3.1-8B-Instruct")
print(card.content[:500])
```

---

## Fine-Tuning with HuggingFace Trainer

```python
from transformers import (
    AutoModelForCausalLM, AutoTokenizer,
    TrainingArguments, Trainer, DataCollatorForLanguageModeling
)
from datasets import load_dataset

# Load model and tokenizer
model_name = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_name, torch_dtype=torch.float16, device_map="auto"
)

# Load and tokenize dataset
dataset = load_dataset("json", data_files="train.jsonl")

def tokenize(example):
    return tokenizer(
        example["text"], truncation=True, max_length=2048,
        padding="max_length",
    )

tokenized = dataset.map(tokenize, batched=True)

# Training
args = TrainingArguments(
    output_dir="./finetuned",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    num_train_epochs=3,
    learning_rate=2e-5,
    fp16=True,
    save_strategy="epoch",
)

trainer = Trainer(
    model=model, args=args,
    train_dataset=tokenized["train"],
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)
trainer.train()
```

---

## Accelerate — Distributed Training Made Simple

```python
from accelerate import Accelerator

accelerator = Accelerator(mixed_precision="fp16")

# Wrap everything with accelerate
model, optimizer, dataloader = accelerator.prepare(
    model, optimizer, dataloader
)

# Training loop — works on 1 GPU or 100 GPUs!
for batch in dataloader:
    outputs = model(**batch)
    loss = outputs.loss
    accelerator.backward(loss)
    optimizer.step()
    optimizer.zero_grad()

# Launch distributed training:
# accelerate launch --num_processes 4 train.py
# accelerate launch --multi_gpu --num_processes 8 train.py

# Accelerate config — generated interactively:
# accelerate config
# Then just: accelerate launch train.py
```

---

## Pushing Models to Hub

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# After training, push your model
model.push_to_hub(
    "my-username/my-fine-tuned-model",
    commit_message="Fine-tuned Mistral 7B on customer support data",
    private=True,  # Set to False for public models
)

tokenizer.push_to_hub("my-username/my-fine-tuned-model")

# Create a model card
from huggingface_hub import ModelCard, ModelCardData

card_data = ModelCardData(
    language="en",
    license="mit",
    model_name="My Fine-Tuned Model",
    base_model="mistralai/Mistral-7B-Instruct-v0.3",
)

card = ModelCard.from_template(
    card_data,
    model_description="Fine-tuned for customer support classification.",
    training_details="Trained on 5000 examples, 3 epochs, lr=2e-5",
    eval_results="Accuracy: 94.5% on test set",
)

card.push_to_hub("my-username/my-fine-tuned-model")
```

---

## AutoTrain — No-Code Fine-Tuning

```python
# HuggingFace AutoTrain: fine-tune without writing code

# CLI approach:
# autotrain llm --train \
#   --model meta-llama/Llama-3.1-8B-Instruct \
#   --data-path ./my_data \
#   --text-column text \
#   --lr 2e-4 \
#   --batch-size 2 \
#   --epochs 3 \
#   --trainer sft \
#   --peft \
#   --quantization int4

# Or use the web interface at:
# huggingface.co/autotrain

# AutoTrain handles:
# - Data formatting and validation
# - Training configuration
# - LoRA/QLoRA setup
# - Evaluation
# - Model upload to Hub
# - Cost: ~$5-50 depending on model size and data

# Best for: Quick experiments when you don't need
# full control over the training process
```

---

## HuggingFace Tokenizers — Fast Tokenization

```python
from tokenizers import Tokenizer, models, trainers, pre_tokenizers

# Train a custom BPE tokenizer from scratch
tokenizer = Tokenizer(models.BPE())
tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel()

trainer = trainers.BpeTrainer(
    vocab_size=32000,
    min_frequency=2,
    special_tokens=["<s>", "</s>", "<pad>", "<unk>", "<mask>"],
)

# Train on your domain-specific corpus
files = ["domain_text_1.txt", "domain_text_2.txt"]
tokenizer.train(files, trainer)

# Use for tokenization
output = tokenizer.encode("Your domain-specific text here")
print(f"Tokens: {output.tokens}")
print(f"IDs: {output.ids}")

# Speed comparison:
# Python tokenizer: ~1,000 tokens/second
# HuggingFace Tokenizers (Rust): ~1,000,000 tokens/second
# That's 1000× faster!

# Save and reuse
tokenizer.save("my_tokenizer.json")
```

---

## HuggingFace TRL — Complete RLHF Pipeline

```python
from trl import AutoModelForCausalLMWithValueHead, PPOConfig, PPOTrainer

# 1. Load model with value head (for PPO)
model = AutoModelForCausalLMWithValueHead.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct"
)

# 2. Define reward function
def reward_fn(responses):
    """Score responses (e.g., using a reward model)."""
    scores = []
    for response in responses:
        # Could be: sentiment, helpfulness, safety score
        score = reward_model.score(response)
        scores.append(score)
    return scores

# 3. PPO training
ppo_config = PPOConfig(
    batch_size=4,
    learning_rate=1e-5,
    ppo_epochs=4,
    mini_batch_size=1,
)

trainer = PPOTrainer(
    config=ppo_config,
    model=model,
    tokenizer=tokenizer,
)

# 4. Training loop
for batch in dataloader:
    queries = batch["query"]
    responses = trainer.generate(queries)
    rewards = reward_fn(responses)
    trainer.step(queries, responses, rewards)
```

---

## HuggingFace PEFT Integration

```python
# Seamless PEFT support in transformers

from transformers import AutoModelForCausalLM
from peft import PeftModel

# Load a PEFT model directly from the Hub
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    torch_dtype=torch.float16,
    device_map="auto",
)

# Load community LoRA adapter
model = PeftModel.from_pretrained(
    model,
    "some-user/llama-3.1-8b-coding-lora",  # Hub adapter
)

# Or use the auto class for even simpler loading
from peft import AutoPeftModelForCausalLM

model = AutoPeftModelForCausalLM.from_pretrained(
    "some-user/llama-3.1-8b-coding-lora",
    torch_dtype=torch.float16,
    device_map="auto",
)

# The Hub hosts thousands of community LoRA adapters
# for various tasks, styles, and domains
# Search: huggingface.co/models?library=peft
```

---

## Datasets — Advanced Features

```python
from datasets import load_dataset, DatasetDict, concatenate_datasets

# Stream large datasets (don't download everything)
dataset = load_dataset("HuggingFaceFW/fineweb", streaming=True)
for example in dataset["train"].take(10):
    print(example["text"][:100])

# Dataset operations
dataset = load_dataset("my_dataset")

# Map with multiple workers
def process(example):
    example["text_length"] = len(example["text"])
    return example

dataset = dataset.map(process, num_proc=4)

# Filter efficiently
long_texts = dataset.filter(lambda x: x["text_length"] > 1000)

# Interleave multiple datasets
ds1 = load_dataset("dataset_a", split="train")
ds2 = load_dataset("dataset_b", split="train")
mixed = concatenate_datasets([ds1, ds2]).shuffle(seed=42)

# Create train/test split
split = dataset["train"].train_test_split(test_size=0.2, seed=42)
# split["train"], split["test"]
```
