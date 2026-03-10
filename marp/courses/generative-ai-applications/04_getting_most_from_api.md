# Getting the Most from an API

---

## Day 2: APIs of Generative Models

```text
Today's Roadmap:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 ┌──────────────────────────────────────┐
 │ 1. API fundamentals and best         │
 │    practices                         │
 │ 2. Prompt engineering techniques     │
 │ 3. Few-shot and zero-shot learning   │
 │ 4. Chain-of-thought reasoning        │
 │ 5. Fine-tuning for custom tasks      │
 └──────────────────────────────────────┘
```

---

## The OpenAI API — Architecture

```text
Your Application
      │
      │ HTTPS (REST API)
      ▼
┌─────────────────┐
│  API Gateway     │
│  (rate limiting, │
│   auth, routing) │
└────────┬────────┘
         │
┌────────┴────────┐
│  Load Balancer   │
└────────┬────────┘
         │
   ┌─────┴─────┐
   ▼           ▼
┌──────┐  ┌──────┐
│GPU   │  │GPU   │
│Cluster│  │Cluster│
│(model│  │(model│
│ srvr)│  │ srvr)│
└──────┘  └──────┘
```

---

## Setting Up the `OpenAI` Client

```python
import os
from openai import OpenAI

# Method 1: Environment variable (recommended)
# export OPENAI_API_KEY="sk-..."
client = OpenAI()  # Automatically reads OPENAI_API_KEY

# Method 2: Explicit key (for development only)
client = OpenAI(api_key="sk-...")

# Method 3: Azure OpenAI
from openai import AzureOpenAI
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-01",
    azure_endpoint="https://your-resource.openai.azure.com"
)

# Method 4: Custom endpoint (local models, proxies)
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"  # For local models
)
```

---

## The Chat Completions API

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a data scientist."},
        {"role": "user", "content": "Explain p-values simply."},
    ],
    temperature=0.7,
    max_tokens=300,
)

# Response structure
print(response.model)                          # "gpt-4o-2024-08-06"
print(response.choices[0].message.content)     # The response text
print(response.choices[0].finish_reason)       # "stop" or "length"
print(response.usage.prompt_tokens)            # Input token count
print(response.usage.completion_tokens)        # Output token count
print(response.usage.total_tokens)             # Total tokens used

# Finish reasons:
# "stop"         — model finished naturally
# "length"       — hit max_tokens limit
# "content_filter" — flagged by safety filter
# "tool_calls"   — model wants to call a function
```

---

## Streaming Responses

For real-time output in user-facing applications:

```python
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Write a short story about AI."}
    ],
    stream=True,  # Enable streaming
)

full_response = ""
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        token = chunk.choices[0].delta.content
        print(token, end="", flush=True)  # Print token by token
        full_response += token

# Streaming benefits:
# - User sees output immediately (lower perceived latency)
# - Time-to-first-token: ~200ms vs ~2-5s for full response
# - Better UX for long responses
# - Can abort early if response is going off-track
```

---

## Handling Multi-Turn Conversations

```python
class Conversation:
    def __init__(self, system_prompt, model="gpt-4o"):
        self.model = model
        self.messages = [
            {"role": "system", "content": system_prompt}
        ]

    def chat(self, user_message):
        self.messages.append(
            {"role": "user", "content": user_message}
        )

        response = client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0.7,
        )

        assistant_msg = response.choices[0].message.content
        self.messages.append(
            {"role": "assistant", "content": assistant_msg}
        )
        return assistant_msg

# Usage
conv = Conversation("You are a Python tutor.")
print(conv.chat("What are list comprehensions?"))
print(conv.chat("Show me a complex example."))
# The model remembers the context of the conversation
```

---

## Function Calling (Tool Use)

Let the model call your functions:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    },
                    "units": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature units"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Weather in Paris?"}],
    tools=tools,
    tool_choice="auto",
)
```

---

## Function Calling — Handling the Response

```python
import json

def get_weather(city, units="celsius"):
    """Your actual weather API call."""
    # ... call weather service ...
    return {"temp": 22, "condition": "sunny", "city": city}

# Check if model wants to call a function
message = response.choices[0].message

if message.tool_calls:
    for tool_call in message.tool_calls:
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)

        # Execute the function
        if func_name == "get_weather":
            result = get_weather(**func_args)

        # Send result back to the model
        messages.append(message)  # Include the tool call
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result),
        })

    # Get final response with function results
    final = client.chat.completions.create(
        model="gpt-4o", messages=messages
    )
    print(final.choices[0].message.content)
    # "The weather in Paris is 22°C and sunny."
```

---

## Structured Output with JSON Mode

Force the model to return valid `JSON`:

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "Extract entities as JSON with keys: "
                       "persons, locations, organizations"
        },
        {
            "role": "user",
            "content": "Tim Cook announced that Apple will "
                       "open a new office in Berlin next year."
        }
    ],
    response_format={"type": "json_object"},
)

import json
data = json.loads(response.choices[0].message.content)
print(data)
# {
#   "persons": ["Tim Cook"],
#   "locations": ["Berlin"],
#   "organizations": ["Apple"]
# }
```

---

## Structured Output with Pydantic Models

Even more robust structured outputs:

```python
from pydantic import BaseModel
from typing import List, Optional

class Entity(BaseModel):
    name: str
    type: str  # "person", "location", "organization"
    confidence: float

class ExtractionResult(BaseModel):
    entities: List[Entity]
    summary: str

response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Extract named entities."},
        {"role": "user", "content": "Elon Musk visited Tesla's "
                                     "factory in Austin, Texas."},
    ],
    response_format=ExtractionResult,
)

result = response.choices[0].message.parsed
for entity in result.entities:
    print(f"{entity.name}: {entity.type} ({entity.confidence})")
```

---

## Embeddings API

Convert text to dense vectors for semantic search:

```python
def get_embedding(text, model="text-embedding-3-small"):
    response = client.embeddings.create(
        input=text,
        model=model,
    )
    return response.data[0].embedding

# Compare similarity between texts
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

e1 = get_embedding("How do I reset my password?")
e2 = get_embedding("I forgot my login credentials")
e3 = get_embedding("What is the weather today?")

print(cosine_similarity(e1, e2))  # ~0.89 (very similar)
print(cosine_similarity(e1, e3))  # ~0.42 (unrelated)
```

| Model | Dimensions | Price/1M tokens |
|-------|-----------|-----------------|
| `text-embedding-3-small` | 1536 | $0.02 |
| `text-embedding-3-large` | 3072 | $0.13 |

---

## Rate Limiting and Retries

```python
from openai import OpenAI, RateLimitError
from tenacity import retry, wait_exponential, stop_after_attempt

client = OpenAI()

@retry(
    wait=wait_exponential(multiplier=1, min=1, max=60),
    stop=stop_after_attempt(6),
    retry=lambda e: isinstance(e, RateLimitError),
)
def robust_completion(messages, **kwargs):
    return client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        **kwargs,
    )

# Rate limits by tier:
# Tier 1: 500 RPM,  30,000 TPM
# Tier 2: 5,000 RPM, 450,000 TPM
# Tier 3: 5,000 RPM, 800,000 TPM
# Tier 5: 10,000 RPM, 10,000,000 TPM
```

---

## Batch Processing for Cost Savings

Process large volumes at 50% discount:

```python
import jsonl

# 1. Create batch file
requests = []
for i, text in enumerate(documents):
    requests.append({
        "custom_id": f"doc-{i}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Summarize."},
                {"role": "user", "content": text},
            ],
            "max_tokens": 200,
        }
    })

# 2. Upload and create batch
batch_file = client.files.create(
    file=open("batch_requests.jsonl", "rb"),
    purpose="batch",
)
batch = client.batches.create(
    input_file_id=batch_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
)
# 3. Results available within 24 hours at 50% cost
```

---

## Vision API — Multimodal Input

Send images alongside text:

```python
import base64

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this diagram."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,"
                               f"{encode_image('diagram.png')}",
                        "detail": "high",  # or "low" for cheaper
                    },
                },
            ],
        }
    ],
    max_tokens=500,
)
# Model can analyze charts, diagrams, screenshots, photos
```

---

## Error Handling Best Practices

```python
from openai import (
    OpenAI, APIError, RateLimitError,
    APIConnectionError, AuthenticationError
)

def safe_completion(messages, model="gpt-4o"):
    try:
        response = client.chat.completions.create(
            model=model, messages=messages
        )
        return response.choices[0].message.content

    except AuthenticationError:
        raise ValueError("Invalid API key. Check OPENAI_API_KEY.")

    except RateLimitError as e:
        print(f"Rate limited. Retry after: {e.retry_after}s")
        time.sleep(e.retry_after or 60)
        return safe_completion(messages, model)  # retry

    except APIConnectionError:
        print("Network error. Check your connection.")
        return None

    except APIError as e:
        print(f"API error {e.status_code}: {e.message}")
        if e.status_code >= 500:  # Server error, retry
            time.sleep(5)
            return safe_completion(messages, model)
        return None
```

---

## Cost Optimization Strategies

```text
┌───────────────────────────────────────────────────────┐
│           COST OPTIMIZATION PLAYBOOK                   │
├───────────────────────────────────────────────────────┤
│                                                        │
│ 1. MODEL SELECTION                                     │
│    Use gpt-4o-mini for simple tasks (20× cheaper)     │
│    Reserve gpt-4o for complex reasoning                │
│                                                        │
│ 2. PROMPT OPTIMIZATION                                 │
│    Shorter prompts = fewer input tokens                │
│    Cache system prompts when possible                  │
│                                                        │
│ 3. MAX_TOKENS                                          │
│    Set appropriate limits (don't default to 4096)      │
│                                                        │
│ 4. CACHING                                             │
│    Cache identical requests (deterministic temp=0)     │
│                                                        │
│ 5. BATCHING                                            │
│    Use batch API for non-urgent requests (50% off)     │
│                                                        │
│ 6. PROMPT CACHING                                      │
│    Reuse system prompts across requests (50% off)      │
│                                                        │
└───────────────────────────────────────────────────────┘
```

---

## Implementing a Response Cache

```python
import hashlib
import json
from functools import lru_cache

class LLMCache:
    def __init__(self):
        self.cache = {}

    def _key(self, messages, model, temperature):
        content = json.dumps({
            "messages": messages,
            "model": model,
            "temp": temperature,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()

    def get_completion(self, messages, model="gpt-4o",
                       temperature=0):
        key = self._key(messages, model, temperature)

        if key in self.cache:
            print("Cache hit!")
            return self.cache[key]

        response = client.chat.completions.create(
            model=model, messages=messages,
            temperature=temperature,
        )
        result = response.choices[0].message.content
        self.cache[key] = result
        return result

cache = LLMCache()
```

---

## Monitoring API Usage

```python
class UsageTracker:
    """Track API usage and costs."""

    PRICING = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    }

    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.call_count = 0

    def track(self, response):
        self.call_count += 1
        usage = response.usage
        model = response.model.split("-2024")[0]  # normalize
        prices = self.PRICING.get(model, {"input": 0, "output": 0})

        cost = (usage.prompt_tokens * prices["input"] +
                usage.completion_tokens * prices["output"]) / 1_000_000

        self.total_input_tokens += usage.prompt_tokens
        self.total_output_tokens += usage.completion_tokens
        self.total_cost += cost

    def report(self):
        print(f"Calls: {self.call_count}")
        print(f"Input tokens:  {self.total_input_tokens:,}")
        print(f"Output tokens: {self.total_output_tokens:,}")
        print(f"Total cost:    ${self.total_cost:.4f}")
```

---

## Exercise: Building a Multi-Function Assistant

```python
"""
Exercise: Build an assistant that can:
1. Answer questions using the LLM
2. Call a calculator function for math
3. Look up information in a local database
4. Return structured JSON responses

Steps:
- Define tool schemas for calculator and database lookup
- Implement the tool functions
- Handle the tool_calls response loop
- Test with various user queries
"""

# Starter code:
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform arithmetic calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression, e.g. '2+2'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    # Add more tools...
]
```

---

## Key Takeaways — Getting the Most from an API

1. Use **streaming** for real-time user-facing applications
1. **Function calling** extends `LLM` capabilities with external tools
1. **Structured outputs** (JSON mode, Pydantic) ensure parseable responses
1. **Batch API** saves 50% on non-urgent processing
1. Implement **retries with exponential backoff** for reliability
1. **Cache** deterministic requests to reduce cost
1. **Monitor usage** to avoid budget surprises
1. Choose the **right model** for each task (mini vs. full)

---

## Audio API — Speech to Text

```python
# Transcribe audio with Whisper
audio_file = open("meeting.mp3", "rb")

transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="verbose_json",
    timestamp_granularities=["segment"],
)

for segment in transcript.segments:
    print(f"[{segment.start:.1f}s - {segment.end:.1f}s] "
          f"{segment.text}")

# Translation (any language → English)
translation = client.audio.translations.create(
    model="whisper-1",
    file=open("french_audio.mp3", "rb"),
)
print(translation.text)  # English translation

# Text to Speech
speech = client.audio.speech.create(
    model="tts-1-hd",
    voice="nova",   # alloy, echo, fable, onyx, nova, shimmer
    input="Hello, welcome to the generative AI course!",
)
speech.stream_to_file("welcome.mp3")
```

---

## Moderation API

```python
# Check content for safety before/after generation
moderation = client.moderations.create(
    model="omni-moderation-latest",
    input="I want to build a helpful chatbot for customer service",
)

result = moderation.results[0]
print(f"Flagged: {result.flagged}")

# Category scores
for category, score in result.category_scores.__dict__.items():
    if score > 0.01:
        print(f"  {category}: {score:.4f}")

# Categories checked:
# sexual, hate, harassment, self-harm, violence
# sexual/minors, hate/threatening, harassment/threatening
# self-harm/intent, self-harm/instructions, violence/graphic

# Use in your pipeline:
def safe_generate(user_input):
    mod = client.moderations.create(input=user_input)
    if mod.results[0].flagged:
        return "Sorry, I can't help with that request."
    return generate_response(user_input)
```

---

## Parallel Function Calling

Handle multiple tool calls in a single response:

```python
# The model can request multiple function calls at once
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content":
            "What's the weather in Paris, London, and Tokyo?"}
    ],
    tools=tools,
)

message = response.choices[0].message

# message.tool_calls might contain 3 calls:
# [get_weather("Paris"), get_weather("London"), get_weather("Tokyo")]

if message.tool_calls:
    # Execute all calls (can be done in parallel!)
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(
                available_functions[tc.function.name],
                **json.loads(tc.function.arguments)
            ): tc
            for tc in message.tool_calls
        }
        for future in concurrent.futures.as_completed(futures):
            tc = futures[future]
            result = future.result()
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result),
            })
```

---

## Prompt Caching

Reduce costs for repeated system prompts:

```python
# Prompt caching is automatic for identical prefixes
# When your messages start the same way across requests,
# the API caches the prefix computation

# Request 1: Full computation
messages_1 = [
    {"role": "system", "content": LONG_SYSTEM_PROMPT},  # 2000 tokens
    {"role": "user", "content": "Question 1"},
]

# Request 2: System prompt is cached!
messages_2 = [
    {"role": "system", "content": LONG_SYSTEM_PROMPT},  # CACHED
    {"role": "user", "content": "Question 2"},
]

# Cached tokens are 50% cheaper
# System prompt: 2000 tokens × $2.50/1M = $0.005 (full price)
# With caching:  2000 tokens × $1.25/1M = $0.0025 (50% off)

# To maximize caching:
# 1. Keep system prompts identical across requests
# 2. Place static content at the START of messages
# 3. Put variable content at the END
```

---

## Assistants API (Threads & Runs)

```python
# The Assistants API manages state server-side

# Create an assistant
assistant = client.beta.assistants.create(
    name="Data Analyst",
    instructions="You are a data analyst. Use code interpreter "
                 "to analyze data and create visualizations.",
    model="gpt-4o",
    tools=[
        {"type": "code_interpreter"},
        {"type": "file_search"},
    ],
)

# Create a thread (conversation)
thread = client.beta.threads.create()

# Add a message
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Analyze the sales trends in the attached CSV",
)

# Run the assistant
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
)

# Get the response
messages = client.beta.threads.messages.list(thread_id=thread.id)
print(messages.data[0].content[0].text.value)
```

---

## API Best Practices Summary

```text
┌──────────────────────────────────────────────────────┐
│          API BEST PRACTICES CHECKLIST                 │
├──────────────────────────────────────────────────────┤
│                                                       │
│  RELIABILITY                                          │
│  ☐ Implement exponential backoff for retries         │
│  ☐ Set appropriate timeouts                          │
│  ☐ Handle all error types gracefully                 │
│  ☐ Use idempotency keys for critical operations      │
│                                                       │
│  COST                                                 │
│  ☐ Choose the right model for each task              │
│  ☐ Set max_tokens to reasonable limits               │
│  ☐ Cache deterministic responses                     │
│  ☐ Use batch API for non-urgent processing           │
│  ☐ Monitor usage with tracking middleware            │
│                                                       │
│  SECURITY                                             │
│  ☐ Never expose API keys in client code              │
│  ☐ Validate and sanitize all user inputs             │
│  ☐ Use moderation API for user-facing apps           │
│  ☐ Implement rate limiting per user                  │
│                                                       │
│  QUALITY                                              │
│  ☐ Use structured outputs for data extraction        │
│  ☐ Validate model outputs before using               │
│  ☐ Log inputs/outputs for debugging                  │
│  ☐ A/B test prompt changes                           │
└──────────────────────────────────────────────────────┘
```
