# Agents and Memory

---

## Day 3: Agents, Memory & LangChain

<svg xmlns="http://www.w3.org/2000/svg" width="580" height="260" font-family="sans-serif">
  <text x="20" y="28" font-size="16" fill="#1565c0" font-weight="bold">Today's Roadmap</text>
  <line x1="20" y1="36" x2="560" y2="36" stroke="#1565c0" stroke-width="2"/>
  <rect x="10" y="46" width="560" height="140" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="30" y="74"  font-size="13" fill="#222">1.  What are AI agents?</text>
  <text x="30" y="98"  font-size="13" fill="#222">2.  Memory systems for LLMs</text>
  <text x="30" y="122" font-size="13" fill="#222">3.  LangChain framework</text>
  <text x="30" y="146" font-size="13" fill="#222">4.  Building a custom database interface</text>
  <text x="20" y="216" font-size="13" fill="#222" font-weight="bold">Goal:</text>
  <text x="70" y="216" font-size="13" fill="#222">Build systems where LLMs can remember</text>
  <text x="20" y="238" font-size="13" fill="#222">context, use tools, and take autonomous actions.</text>
</svg>

---

## What is an AI Agent?

An `LLM` that can **observe**, **reason**, and **act** in a loop:

<svg xmlns="http://www.w3.org/2000/svg" width="500" height="400" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#555"/>
    </marker>
  </defs>
  <!-- Outer container -->
  <rect x="5" y="5" width="490" height="388" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="250" y="32" font-size="14" fill="#222" text-anchor="middle" font-weight="bold">AGENT LOOP</text>
  <!-- Observe box -->
  <rect x="150" y="52" width="110" height="44" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="205" y="79" font-size="13" fill="#222" text-anchor="middle">Observe</text>
  <!-- Observe ← Environment label -->
  <line x1="270" y1="74" x2="390" y2="74" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="405" y="78" font-size="12" fill="#555">Environment / Tools</text>
  <!-- Arrow: Observe → Think -->
  <line x1="205" y1="96" x2="205" y2="158" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Think box -->
  <rect x="150" y="160" width="110" height="44" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="205" y="187" font-size="13" fill="#222" text-anchor="middle">Think</text>
  <!-- Think ← LLM label -->
  <line x1="270" y1="182" x2="350" y2="182" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="365" y="186" font-size="12" fill="#555">LLM Reasoning</text>
  <!-- Arrow: Think → Act -->
  <line x1="205" y1="204" x2="205" y2="266" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Act box -->
  <rect x="150" y="268" width="110" height="44" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="205" y="295" font-size="13" fill="#222" text-anchor="middle">Act</text>
  <!-- Act → Call tool label -->
  <line x1="270" y1="290" x2="350" y2="290" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="360" y="294" font-size="12" fill="#555">Call tool / Respond</text>
  <!-- Loop back arrow -->
  <path d="M 150 290 Q 80 290 80 74 Q 80 52 148 52"
        fill="none" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="15" y="175" font-size="11" fill="#555" transform="rotate(-90,15,175)">Loop until task complete</text>
</svg>

**Key difference from simple chatbots:** Agents can take **multiple steps** and use **external tools** to accomplish tasks.

---

## Simple Agent vs. Complex Agent

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="310" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#555"/>
    </marker>
  </defs>
  <!-- SIMPLE CHATBOT section -->
  <text x="10" y="24" font-size="14" fill="#222" font-weight="bold">SIMPLE CHATBOT:</text>
  <rect x="10" y="34" width="60" height="30" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="40" y="54" font-size="12" fill="#222" text-anchor="middle">User</text>
  <line x1="70" y1="49" x2="108" y2="49" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="110" y="34" width="50" height="30" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="135" y="54" font-size="12" fill="#222" text-anchor="middle">LLM</text>
  <line x1="160" y1="49" x2="198" y2="49" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="200" y="34" width="80" height="30" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="240" y="54" font-size="12" fill="#222" text-anchor="middle">Response</text>
  <text x="10" y="84" font-size="12" fill="#555">(single turn, no tools, no memory)</text>

  <!-- AGENT section -->
  <text x="10" y="116" font-size="14" fill="#222" font-weight="bold">AGENT:</text>
  <rect x="10" y="124" width="60" height="30" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="40" y="144" font-size="12" fill="#222" text-anchor="middle">User</text>
  <line x1="70" y1="139" x2="108" y2="139" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="110" y="124" width="50" height="30" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="135" y="144" font-size="12" fill="#222" text-anchor="middle">LLM</text>
  <!-- Steps -->
  <text x="175" y="134" font-size="12" fill="#555">→ "I need to search the database"</text>
  <text x="175" y="154" font-size="12" fill="#555">→ [calls search tool]</text>
  <text x="175" y="174" font-size="12" fill="#555">→ "Found 3 results, let me analyze..."</text>
  <text x="175" y="194" font-size="12" fill="#555">→ "I also need to check the API"</text>
  <text x="175" y="214" font-size="12" fill="#555">→ [calls API tool]</text>
  <text x="175" y="234" font-size="12" fill="#555">→ "Based on my research, here's the answer..."</text>
  <text x="175" y="254" font-size="12" fill="#555">→ Response to User</text>
  <text x="10" y="286" font-size="12" fill="#555">(multi-step, tools, memory, autonomous)</text>
</svg>

---

## Agent Architecture

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="460" font-family="sans-serif">
  <!-- Outer AGENT box -->
  <rect x="5" y="5" width="650" height="450" rx="6" fill="#f0f4f8" stroke="#333" stroke-width="2"/>
  <text x="330" y="30" font-size="14" fill="#222" text-anchor="middle" font-weight="bold">AGENT</text>

  <!-- LLM box -->
  <rect x="20" y="45" width="620" height="110" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="68" font-size="13" fill="#222" text-anchor="middle" font-weight="bold">LLM (Brain)</text>
  <text x="40" y="92"  font-size="12" fill="#555">• Understands instructions</text>
  <text x="40" y="110" font-size="12" fill="#555">• Plans actions</text>
  <text x="40" y="128" font-size="12" fill="#555">• Interprets tool outputs</text>

  <!-- TOOLS box -->
  <rect x="20" y="175" width="620" height="140" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="198" font-size="13" fill="#222" text-anchor="middle" font-weight="bold">TOOLS</text>
  <!-- 4 tool sub-boxes -->
  <rect x="36"  y="210" width="120" height="80" rx="4" fill="#ffe0b2" stroke="#e65100" stroke-width="1.5"/>
  <text x="96"  y="247" font-size="12" fill="#222" text-anchor="middle">Search</text>
  <text x="96"  y="265" font-size="12" fill="#222" text-anchor="middle">Engine</text>

  <rect x="176" y="210" width="120" height="80" rx="4" fill="#ffe0b2" stroke="#e65100" stroke-width="1.5"/>
  <text x="236" y="247" font-size="12" fill="#222" text-anchor="middle">Code</text>
  <text x="236" y="265" font-size="12" fill="#222" text-anchor="middle">Exec</text>

  <rect x="316" y="210" width="120" height="80" rx="4" fill="#ffe0b2" stroke="#e65100" stroke-width="1.5"/>
  <text x="376" y="247" font-size="12" fill="#222" text-anchor="middle">Database</text>
  <text x="376" y="265" font-size="12" fill="#222" text-anchor="middle">Query</text>

  <rect x="456" y="210" width="120" height="80" rx="4" fill="#ffe0b2" stroke="#e65100" stroke-width="1.5"/>
  <text x="516" y="247" font-size="12" fill="#222" text-anchor="middle">API</text>
  <text x="516" y="265" font-size="12" fill="#222" text-anchor="middle">Call</text>

  <!-- MEMORY box -->
  <rect x="20" y="335" width="620" height="100" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="358" font-size="13" fill="#222" text-anchor="middle" font-weight="bold">MEMORY</text>
  <text x="40" y="382" font-size="12" fill="#555">Short-term:  conversation history</text>
  <text x="40" y="402" font-size="12" fill="#555">Long-term:   vector database</text>
</svg>

---

## Building a Simple Agent from Scratch

```python
import json
from openai import OpenAI

client = OpenAI()

def calculator(expression: str) -> str:
    """Safely evaluate a math expression."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def search_database(query: str) -> str:
    """Simulate a database search."""
    db = {
        "revenue_2024": "$4.2M",
        "employees": "127",
        "top_product": "CloudSync Pro",
    }
    for key, value in db.items():
        if query.lower() in key.lower():
            return f"{key}: {value}"
    return "No results found"

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate math expressions",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_database",
            "description": "Search company database",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
]
```

---

## The Agent Loop

```python
def run_agent(user_message, max_iterations=10):
    available_functions = {
        "calculator": calculator,
        "search_database": search_database,
    }

    messages = [
        {"role": "system", "content":
            "You are a helpful assistant with access to tools. "
            "Use them when needed to answer questions accurately."},
        {"role": "user", "content": user_message},
    ]

    for i in range(max_iterations):
        response = client.chat.completions.create(
            model="gpt-4o", messages=messages, tools=tools,
        )
        msg = response.choices[0].message

        if msg.tool_calls:
            messages.append(msg)
            for tool_call in msg.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)
                result = available_functions[fn_name](**fn_args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })
        else:
            return msg.content

    return "Max iterations reached."
```

---

## Agent Planning Strategies

<svg xmlns="http://www.w3.org/2000/svg" width="620" height="336" font-family="sans-serif">
  <rect x="5" y="5" width="610" height="326" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="310" y="30" font-size="14" fill="#222" text-anchor="middle" font-weight="bold">PLANNING STRATEGIES</text>
  <line x1="5" y1="38" x2="615" y2="38" stroke="#333" stroke-width="1"/>
  <line x1="155" y1="5" x2="155" y2="331" stroke="#333" stroke-width="1"/>
  <rect x="6" y="39" width="148" height="71" fill="#e3f2fd" stroke="none"/>
  <rect x="156" y="39" width="458" height="71" fill="#e3f2fd" stroke="none"/>
  <line x1="5" y1="110" x2="615" y2="110" stroke="#bbb" stroke-width="1"/>
  <text x="14" y="80" font-size="13" fill="#222" font-weight="bold">ReAct</text>
  <text x="166" y="64" font-size="12" fill="#555">Interleave reasoning and actions</text>
  <text x="166" y="80" font-size="12" fill="#555">Thought → Action → Observation</text>
  <text x="166" y="96" font-size="12" fill="#555">Simple, effective for most tasks</text>
  <rect x="6" y="111" width="148" height="71" fill="#fff3e0" stroke="none"/>
  <rect x="156" y="111" width="458" height="71" fill="#fff3e0" stroke="none"/>
  <line x1="5" y1="182" x2="615" y2="182" stroke="#bbb" stroke-width="1"/>
  <text x="14" y="144" font-size="13" fill="#222" font-weight="bold">Plan-and-</text>
  <text x="14" y="160" font-size="13" fill="#222" font-weight="bold">Execute</text>
  <text x="166" y="136" font-size="12" fill="#555">Create full plan first, then execute</text>
  <text x="166" y="152" font-size="12" fill="#555">Better for complex multi-step tasks</text>
  <text x="166" y="168" font-size="12" fill="#555">Can revise plan based on results</text>
  <rect x="6" y="183" width="148" height="71" fill="#e3f2fd" stroke="none"/>
  <rect x="156" y="183" width="458" height="71" fill="#e3f2fd" stroke="none"/>
  <line x1="5" y1="254" x2="615" y2="254" stroke="#bbb" stroke-width="1"/>
  <text x="14" y="224" font-size="13" fill="#222" font-weight="bold">Reflexion</text>
  <text x="166" y="208" font-size="12" fill="#555">Agent reflects on past attempts</text>
  <text x="166" y="224" font-size="12" fill="#555">Learns from mistakes in-context</text>
  <text x="166" y="240" font-size="12" fill="#555">Good for trial-and-error tasks</text>
  <rect x="6" y="255" width="148" height="71" fill="#fff3e0" stroke="none"/>
  <rect x="156" y="255" width="458" height="71" fill="#fff3e0" stroke="none"/>
  <line x1="5" y1="326" x2="615" y2="326" stroke="#bbb" stroke-width="1"/>
  <text x="14" y="272" font-size="13" fill="#222" font-weight="bold">LATS</text>
  <text x="14" y="288" font-size="13" fill="#222" font-weight="bold">(Language</text>
  <text x="14" y="304" font-size="13" fill="#222" font-weight="bold">Agent Tree</text>
  <text x="14" y="320" font-size="13" fill="#222" font-weight="bold">Search)</text>
  <text x="166" y="280" font-size="12" fill="#555">Tree search over action space</text>
  <text x="166" y="296" font-size="12" fill="#555">Evaluate multiple paths</text>
  <text x="166" y="312" font-size="12" fill="#555">Best for complex reasoning</text>
</svg>

---

## Plan-and-Execute Agent

```python
def plan_and_execute(task):
    # Step 1: Create a plan
    plan_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content":
                "Create a numbered step-by-step plan to complete "
                "this task. Each step should be one concrete action."},
            {"role": "user", "content": task},
        ],
    )
    plan = plan_response.choices[0].message.content

    # Step 2: Execute each step
    results = []
    steps = parse_plan(plan)

    for i, step in enumerate(steps):
        print(f"Executing step {i+1}: {step}")
        result = run_agent(
            f"Execute this step: {step}\n"
            f"Previous results: {results}"
        )
        results.append({"step": step, "result": result})

    # Step 3: Synthesize final answer
    synthesis = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content":
                f"Task: {task}\nResults: {json.dumps(results)}\n"
                f"Provide the final answer."},
        ],
    )
    return synthesis.choices[0].message.content
```

---

## The Memory Problem

`LLM`s have no persistent memory — each API call starts fresh:

```misc
Call 1: User: "My name is Alice"
        AI:   "Nice to meet you, Alice!"

Call 2: User: "What's my name?"
        AI:   "I don't know your name."  ← No memory!
```

**Solutions:**

<svg xmlns="http://www.w3.org/2000/svg" width="530" height="328" font-family="sans-serif">
  <rect x="5" y="5" width="520" height="318" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="265" y="30" font-size="14" fill="#222" text-anchor="middle" font-weight="bold">MEMORY STRATEGIES</text>
  <line x1="5" y1="38" x2="525" y2="38" stroke="#333" stroke-width="1"/>
  <line x1="155" y1="5" x2="155" y2="323" stroke="#333" stroke-width="1"/>
  <rect x="6" y="39" width="148" height="55" fill="#e3f2fd" stroke="none"/>
  <rect x="156" y="39" width="368" height="55" fill="#e3f2fd" stroke="none"/>
  <line x1="5" y1="94" x2="525" y2="94" stroke="#bbb" stroke-width="1"/>
  <text x="14" y="64" font-size="13" fill="#222" font-weight="bold">Conversation</text>
  <text x="14" y="80" font-size="13" fill="#222" font-weight="bold">Buffer</text>
  <text x="166" y="64" font-size="12" fill="#555">Pass full history in context</text>
  <text x="166" y="80" font-size="12" fill="#555">Simple but limited by context window</text>
  <rect x="6" y="95" width="148" height="55" fill="#e8f5e9" stroke="none"/>
  <rect x="156" y="95" width="368" height="55" fill="#e8f5e9" stroke="none"/>
  <line x1="5" y1="150" x2="525" y2="150" stroke="#bbb" stroke-width="1"/>
  <text x="14" y="120" font-size="13" fill="#222" font-weight="bold">Summary</text>
  <text x="14" y="136" font-size="13" fill="#222" font-weight="bold">Memory</text>
  <text x="166" y="120" font-size="12" fill="#555">Summarize old messages</text>
  <text x="166" y="136" font-size="12" fill="#555">Saves tokens, loses some detail</text>
  <rect x="6" y="151" width="148" height="55" fill="#e3f2fd" stroke="none"/>
  <rect x="156" y="151" width="368" height="55" fill="#e3f2fd" stroke="none"/>
  <line x1="5" y1="206" x2="525" y2="206" stroke="#bbb" stroke-width="1"/>
  <text x="14" y="176" font-size="13" fill="#222" font-weight="bold">Window</text>
  <text x="14" y="192" font-size="13" fill="#222" font-weight="bold">Memory</text>
  <text x="166" y="176" font-size="12" fill="#555">Keep last N messages</text>
  <text x="166" y="192" font-size="12" fill="#555">Fixed token budget</text>
  <rect x="6" y="207" width="148" height="55" fill="#e8f5e9" stroke="none"/>
  <rect x="156" y="207" width="368" height="55" fill="#e8f5e9" stroke="none"/>
  <line x1="5" y1="262" x2="525" y2="262" stroke="#bbb" stroke-width="1"/>
  <text x="14" y="232" font-size="13" fill="#222" font-weight="bold">Vector Store</text>
  <text x="14" y="248" font-size="13" fill="#222" font-weight="bold">Memory</text>
  <text x="166" y="232" font-size="12" fill="#555">Embed and retrieve relevant memories</text>
  <text x="166" y="248" font-size="12" fill="#555">Semantic retrieval</text>
  <rect x="6" y="263" width="148" height="55" fill="#e3f2fd" stroke="none"/>
  <rect x="156" y="263" width="368" height="55" fill="#e3f2fd" stroke="none"/>
  <line x1="5" y1="318" x2="525" y2="318" stroke="#bbb" stroke-width="1"/>
  <text x="14" y="288" font-size="13" fill="#222" font-weight="bold">Entity</text>
  <text x="14" y="304" font-size="13" fill="#222" font-weight="bold">Memory</text>
  <text x="166" y="288" font-size="12" fill="#555">Track key entities and facts</text>
  <text x="166" y="304" font-size="12" fill="#555">Structured knowledge</text>
</svg>

---

## Conversation Buffer Memory

The simplest approach — keep everything:

```python
class BufferMemory:
    def __init__(self, max_tokens=4000):
        self.messages = []
        self.max_tokens = max_tokens

    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})

    def add_ai_message(self, content):
        self.messages.append({"role": "assistant", "content": content})

    def get_messages(self):
        return self.messages.copy()

    def token_count(self):
        # Rough estimate: 4 chars ≈ 1 token
        return sum(len(m["content"]) // 4 for m in self.messages)

# Problem: Eventually exceeds context window
# After 50 messages of ~200 tokens each = 10,000 tokens
# With GPT-4o (128K): works for ~640 messages
# With GPT-3.5 (16K): works for ~80 messages
```

---

## Summary Memory

Periodically summarize old conversation to save tokens:

```python
class SummaryMemory:
    def __init__(self, summary_threshold=20):
        self.messages = []
        self.summary = ""
        self.summary_threshold = summary_threshold

    def add_exchange(self, user_msg, ai_msg):
        self.messages.append({"role": "user", "content": user_msg})
        self.messages.append({"role": "assistant", "content": ai_msg})

        if len(self.messages) > self.summary_threshold:
            self._summarize()

    def _summarize(self):
        old_messages = self.messages[:-6]  # Keep last 3 exchanges
        summary_prompt = (
            f"Previous summary: {self.summary}\n\n"
            f"New messages to incorporate:\n"
            + "\n".join(f"{m['role']}: {m['content']}" for m in old_messages)
            + "\n\nProvide an updated summary of key information."
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": summary_prompt}],
        )
        self.summary = response.choices[0].message.content
        self.messages = self.messages[-6:]  # Keep recent messages
```

---

## Vector Store Memory

Embed conversations and retrieve relevant ones:

```python
import chromadb
import numpy as np

class VectorMemory:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("memory")
        self.counter = 0

    def store(self, text, metadata=None):
        self.counter += 1
        self.collection.add(
            documents=[text],
            ids=[f"mem_{self.counter}"],
            metadatas=[metadata or {}],
        )

    def retrieve(self, query, k=5):
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
        )
        return results["documents"][0]

# Usage in agent
memory = VectorMemory()
memory.store("User's name is Alice, she's a data scientist")
memory.store("Alice prefers Python over R")
memory.store("User asked about pandas performance")

relevant = memory.retrieve("What does Alice do for work?")
# Returns: ["User's name is Alice, she's a data scientist"]
```

---

## RAG — Retrieval-Augmented Generation

Combine vector memory with generation for knowledge-grounded responses:

<svg xmlns="http://www.w3.org/2000/svg" width="580" height="560" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#555"/>
    </marker>
  </defs>
  <!-- Query label at top -->
  <text x="20" y="22" font-size="13" fill="#222" font-weight="bold">User Query:</text>
  <text x="130" y="22" font-size="13" fill="#555">"What were Q3 results?"</text>
  <line x1="56" y1="28" x2="56" y2="52" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Step 1: EMBED -->
  <rect x="10" y="55" width="200" height="50" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="110" y="78" font-size="13" fill="#222" text-anchor="middle" font-weight="bold">1. EMBED query</text>
  <line x1="210" y1="80" x2="228" y2="80" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="235" y="84" font-size="12" fill="#555">[0.12, -0.34, ...]</text>
  <!-- Arrow down -->
  <line x1="110" y1="105" x2="110" y2="138" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Step 2: SEARCH -->
  <rect x="10" y="142" width="200" height="60" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="110" y="165" font-size="13" fill="#222" text-anchor="middle" font-weight="bold">2. SEARCH vector</text>
  <text x="110" y="183" font-size="13" fill="#222" text-anchor="middle">database</text>
  <line x1="210" y1="172" x2="228" y2="172" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="235" y="176" font-size="12" fill="#555">Find similar docs</text>
  <line x1="110" y1="202" x2="110" y2="236" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Step 3: RETRIEVE -->
  <rect x="10" y="240" width="200" height="60" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="110" y="263" font-size="13" fill="#222" text-anchor="middle" font-weight="bold">3. RETRIEVE top</text>
  <text x="110" y="281" font-size="13" fill="#222" text-anchor="middle">k documents</text>
  <line x1="210" y1="260" x2="228" y2="260" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="235" y="256" font-size="12" fill="#555">"Q3 revenue was $4.2M..."</text>
  <text x="235" y="272" font-size="12" fill="#555">"Operating costs were..."</text>
  <line x1="110" y1="300" x2="110" y2="334" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Step 4: GENERATE -->
  <rect x="10" y="338" width="200" height="60" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="110" y="361" font-size="13" fill="#222" text-anchor="middle" font-weight="bold">4. GENERATE</text>
  <text x="110" y="379" font-size="13" fill="#222" text-anchor="middle">response</text>
  <line x1="210" y1="368" x2="228" y2="368" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="235" y="364" font-size="12" fill="#555">Context + Query → LLM → Response</text>
  <line x1="110" y1="398" x2="110" y2="432" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Final answer -->
  <rect x="10" y="436" width="550" height="60" rx="4" fill="#fff3e0" stroke="#e65100" stroke-width="1.5"/>
  <text x="30" y="462" font-size="12" fill="#222">"Based on Q3 reports, revenue was $4.2M,</text>
  <text x="30" y="480" font-size="12" fill="#222">up 15% from Q2..."</text>
</svg>

---

## Building a RAG Pipeline

```python
from openai import OpenAI
import chromadb

client = OpenAI()
chroma = chromadb.Client()
collection = chroma.create_collection("documents")

def index_documents(documents):
    """Index documents into vector store."""
    for i, doc in enumerate(documents):
        collection.add(
            documents=[doc["text"]],
            ids=[f"doc_{i}"],
            metadatas=[{"source": doc.get("source", "unknown")}],
        )

def rag_query(question, k=3):
    """Answer a question using RAG."""
    # Retrieve relevant documents
    results = collection.query(
        query_texts=[question], n_results=k
    )
    context = "\n\n".join(results["documents"][0])

    # Generate answer grounded in context
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content":
                "Answer based ONLY on the provided context. "
                "If the context doesn't contain the answer, say so."},
            {"role": "user", "content":
                f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
    return response.choices[0].message.content
```

---

## Chunking Strategies for RAG

```python
def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# Different chunking strategies:
# 1. Fixed-size chunks (simple but may split sentences)
# 2. Sentence-based (respects sentence boundaries)
# 3. Paragraph-based (respects topic boundaries)
# 4. Semantic chunking (split at topic changes)
# 5. Recursive (try large chunks, split if too big)

# Recommended chunk sizes:
# Small chunks (200-500 tokens): Better retrieval precision
# Large chunks (500-1500 tokens): More context per retrieval
# Sweet spot: 500-800 tokens with 10-20% overlap
```

---

## Entity Memory

Track specific entities across conversations:

```python
class EntityMemory:
    def __init__(self):
        self.entities = {}

    def update(self, conversation_text):
        """Extract and update entities from conversation."""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content":
                    "Extract entities and facts from this conversation. "
                    "Return JSON: {entity_name: {fact_key: fact_value}}"},
                {"role": "user", "content": conversation_text},
            ],
            response_format={"type": "json_object"},
        )
        import json
        new_entities = json.loads(response.choices[0].message.content)
        for entity, facts in new_entities.items():
            if entity not in self.entities:
                self.entities[entity] = {}
            self.entities[entity].update(facts)

    def get_context(self, query):
        """Return relevant entity information."""
        relevant = []
        for entity, facts in self.entities.items():
            if entity.lower() in query.lower():
                relevant.append(f"{entity}: {json.dumps(facts)}")
        return "\n".join(relevant)
```

---

## Multi-Agent Systems

Multiple specialized agents collaborating:

<svg xmlns="http://www.w3.org/2000/svg" width="600" height="310" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#555"/>
    </marker>
  </defs>
  <!-- Orchestrator -->
  <rect x="80" y="10" width="440" height="64" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="300" y="36" font-size="14" fill="#222" text-anchor="middle" font-weight="bold">ORCHESTRATOR AGENT</text>
  <text x="300" y="58" font-size="12" fill="#555" text-anchor="middle">(routes tasks to specialized agents)</text>

  <!-- Lines from orchestrator to agents -->
  <line x1="170" y1="74" x2="150" y2="138" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="300" y1="74" x2="300" y2="138" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="430" y1="74" x2="450" y2="138" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Research Agent -->
  <rect x="50" y="140" width="150" height="130" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="125" y="164" font-size="13" fill="#222" text-anchor="middle" font-weight="bold">Research Agent</text>
  <line x1="60" y1="174" x2="190" y2="174" stroke="#bbb" stroke-width="1"/>
  <text x="125" y="194" font-size="12" fill="#555" text-anchor="middle">Search</text>
  <text x="125" y="212" font-size="12" fill="#555" text-anchor="middle">Summarize</text>
  <text x="125" y="230" font-size="12" fill="#555" text-anchor="middle">Cite</text>

  <!-- Code Agent -->
  <rect x="225" y="140" width="150" height="130" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="300" y="164" font-size="13" fill="#222" text-anchor="middle" font-weight="bold">Code Agent</text>
  <line x1="235" y1="174" x2="365" y2="174" stroke="#bbb" stroke-width="1"/>
  <text x="300" y="194" font-size="12" fill="#555" text-anchor="middle">Execute</text>
  <text x="300" y="212" font-size="12" fill="#555" text-anchor="middle">Debug</text>
  <text x="300" y="230" font-size="12" fill="#555" text-anchor="middle">Test</text>

  <!-- Review Agent -->
  <rect x="400" y="140" width="150" height="130" rx="4" fill="#fce4ec" stroke="#333" stroke-width="1.5"/>
  <text x="475" y="164" font-size="13" fill="#222" text-anchor="middle" font-weight="bold">Review Agent</text>
  <line x1="410" y1="174" x2="540" y2="174" stroke="#bbb" stroke-width="1"/>
  <text x="475" y="194" font-size="12" fill="#555" text-anchor="middle">Analyze</text>
  <text x="475" y="212" font-size="12" fill="#555" text-anchor="middle">Critique</text>
  <text x="475" y="230" font-size="12" fill="#555" text-anchor="middle">Suggest</text>
</svg>

```python
def orchestrator(task):
    plan = create_plan(task)
    for step in plan:
        if step.type == "research":
            result = research_agent.run(step)
        elif step.type == "code":
            result = code_agent.run(step)
        elif step.type == "review":
            result = review_agent.run(step)
    return synthesize(results)
```

---

## Agent Safety and Guardrails

```python
class SafeAgent:
    """Agent with safety guardrails."""

    ALLOWED_TOOLS = {"search", "calculator", "read_file"}
    MAX_ITERATIONS = 10
    MAX_TOKENS_PER_STEP = 1000

    def __init__(self):
        self.iteration_count = 0
        self.total_tokens = 0

    def validate_action(self, action):
        """Check if action is allowed."""
        if action["tool"] not in self.ALLOWED_TOOLS:
            raise ValueError(f"Tool {action['tool']} not allowed")
        if self.iteration_count >= self.MAX_ITERATIONS:
            raise RuntimeError("Max iterations exceeded")
        if "rm " in str(action.get("args", "")):
            raise ValueError("Destructive operations not allowed")
        return True

    def run(self, task):
        while self.iteration_count < self.MAX_ITERATIONS:
            self.iteration_count += 1
            action = self.think(task)
            self.validate_action(action)
            result = self.execute(action)
            if self.is_complete(result):
                return result
```

---

## Exercise: Building a Research Agent

```python
"""
Exercise: Build a research agent that can:

1. Accept a research question
2. Break it down into sub-questions
3. Search for relevant information (simulated)
4. Synthesize findings into a report
5. Maintain memory of findings across steps

Requirements:
- Use the agent loop pattern
- Implement at least 2 tools (search + note_taking)
- Add conversation buffer memory
- Include safety guardrails (max iterations, allowed tools)

Test with:
- "Compare the performance of GPT-4 and Claude 3.5 Sonnet"
- "What are the best practices for fine-tuning LLMs?"

Bonus:
- Add a "verify" tool that fact-checks claims
- Implement entity memory to track key findings
"""
```

---

## Key Takeaways — Agents and Memory

1. **Agents** = `LLM` + tools + loop (observe → think → act)
1. **Planning strategies** (ReAct, Plan-and-Execute) guide agent behavior
1. **Memory** is essential for multi-turn interactions
1. **Buffer memory** is simplest but limited by context window
1. **Summary memory** compresses old conversations
1. **Vector memory** enables semantic retrieval of relevant history
1. **RAG** grounds responses in your specific documents
1. **Safety guardrails** prevent runaway agents and harmful actions

---

## Hybrid Memory — Combining Approaches

```python
class HybridMemory:
    """Combine short-term buffer with long-term vector store."""

    def __init__(self, buffer_size=10, llm_client=None):
        self.buffer = []          # Recent messages
        self.buffer_size = buffer_size
        self.summary = ""         # Running summary
        self.vector_store = VectorMemory()  # Long-term
        self.client = llm_client

    def add(self, role, content):
        self.buffer.append({"role": role, "content": content})
        # Store in vector memory for retrieval
        self.vector_store.store(f"{role}: {content}")

        # Summarize when buffer is full
        if len(self.buffer) > self.buffer_size:
            self._compress()

    def _compress(self):
        old = self.buffer[:self.buffer_size // 2]
        new_summary = self._summarize(old)
        self.summary = f"{self.summary}\n{new_summary}"
        self.buffer = self.buffer[self.buffer_size // 2:]

    def get_context(self, query):
        # Combine: summary + relevant memories + recent buffer
        relevant = self.vector_store.retrieve(query, k=3)
        return {
            "summary": self.summary,
            "relevant_memories": relevant,
            "recent": self.buffer[-6:],
        }
```

---

## Tool Design Best Practices

```python
# Good tool design for agents

# BAD: Vague description, no constraints
bad_tool = {
    "name": "search",
    "description": "Search for stuff",
    "parameters": {"query": {"type": "string"}},
}

# GOOD: Clear description, constraints, examples
good_tool = {
    "name": "search_knowledge_base",
    "description": (
        "Search the company knowledge base for technical "
        "documentation. Returns top 3 matching articles. "
        "Use for questions about product features, API docs, "
        "or internal processes. Do NOT use for general knowledge."
    ),
    "parameters": {
        "query": {
            "type": "string",
            "description": "Search query, 3-10 words, specific terms",
        },
        "category": {
            "type": "string",
            "enum": ["api", "product", "process", "troubleshooting"],
            "description": "Category to filter results",
        },
    },
}
```

---

## Agent Error Handling Patterns

```python
class ResilientAgent:
    """Agent with comprehensive error handling."""

    def run(self, task, max_retries=3):
        for attempt in range(max_retries):
            try:
                result = self._execute(task)
                if self._validate_result(result):
                    return result
                else:
                    task = self._refine_task(task, result)

            except ToolExecutionError as e:
                # Tool failed — try alternative approach
                self.messages.append({
                    "role": "user",
                    "content": f"The tool failed with: {e}. "
                               f"Try a different approach."
                })

            except RateLimitError:
                time.sleep(2 ** attempt)  # Exponential backoff

            except ContextLengthError:
                # Context too long — summarize history
                self._compress_history()

        return "Could not complete task after retries."

    def _validate_result(self, result):
        """Check if the result actually answers the task."""
        validation = self.llm.invoke(
            f"Does this answer the original question? "
            f"Answer YES or NO: {result}"
        )
        return "YES" in validation.upper()
```

---

## Agentic RAG — Agents That Know When to Search

```python
def agentic_rag(question, retriever, llm):
    """Agent decides whether to search or answer directly."""

    # Step 1: Does the agent need to search?
    decision = llm.invoke(
        f"Can you answer this confidently without searching?\n"
        f"Question: {question}\n"
        f"Respond: SEARCH or ANSWER_DIRECTLY"
    )

    if "SEARCH" in decision:
        # Step 2: Generate search query (might differ from question)
        search_query = llm.invoke(
            f"Generate an optimal search query for:\n{question}"
        )

        # Step 3: Retrieve documents
        docs = retriever.get_relevant_documents(search_query)

        # Step 4: Grade documents — are they relevant?
        relevant_docs = []
        for doc in docs:
            grade = llm.invoke(
                f"Is this document relevant to '{question}'?\n"
                f"Doc: {doc.page_content[:200]}\n"
                f"Respond: RELEVANT or NOT_RELEVANT"
            )
            if "RELEVANT" in grade:
                relevant_docs.append(doc)

        if not relevant_docs:
            # No relevant docs — try web search or say "I don't know"
            return "I don't have enough information to answer that."

        # Step 5: Generate answer from relevant documents
        context = "\n".join(d.page_content for d in relevant_docs)
        return llm.invoke(f"Context: {context}\nQuestion: {question}")

    return llm.invoke(question)
```

---

## Observability for Agents

```python
import logging
from datetime import datetime

class AgentObserver:
    """Track and log agent behavior for debugging."""

    def __init__(self):
        self.trace = []
        self.start_time = None

    def start_run(self, task):
        self.start_time = datetime.now()
        self.trace = [{"event": "start", "task": task,
                       "time": self.start_time.isoformat()}]

    def log_thought(self, thought):
        self.trace.append({
            "event": "thought",
            "content": thought,
            "time": datetime.now().isoformat(),
        })

    def log_tool_call(self, tool, args, result, duration_ms):
        self.trace.append({
            "event": "tool_call",
            "tool": tool, "args": args,
            "result": str(result)[:200],
            "duration_ms": duration_ms,
        })

    def summary(self):
        duration = (datetime.now() - self.start_time).total_seconds()
        tool_calls = [t for t in self.trace if t["event"] == "tool_call"]
        return {
            "total_duration_s": duration,
            "total_steps": len(self.trace),
            "tool_calls": len(tool_calls),
            "trace": self.trace,
        }
```

---

## Token-Aware Memory Management

```python
import tiktoken

class TokenAwareMemory:
    """Memory that respects token budgets."""

    def __init__(self, max_tokens=8000, model="gpt-4o"):
        self.max_tokens = max_tokens
        self.enc = tiktoken.encoding_for_model(model)
        self.messages = []

    def _count_tokens(self, messages):
        total = 0
        for msg in messages:
            total += len(self.enc.encode(msg["content"])) + 4
        return total

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})
        self._trim()

    def _trim(self):
        """Remove oldest messages to stay under token limit."""
        while (self._count_tokens(self.messages) > self.max_tokens
               and len(self.messages) > 2):
            # Always keep the first message (system) and last
            self.messages.pop(1)  # Remove second-oldest

    def get_messages(self, system_prompt=""):
        result = [{"role": "system", "content": system_prompt}]
        result.extend(self.messages)
        tokens_used = self._count_tokens(result)
        tokens_remaining = self.max_tokens - tokens_used
        return result, tokens_remaining
```

---

## Designing Agent Personas

```python
# Well-designed agent personas improve consistency

research_agent_persona = """You are a thorough research assistant.

PERSONALITY:
- Systematic and methodical in your approach
- Always verify claims with multiple sources
- Clearly distinguish facts from opinions
- Acknowledge uncertainty when appropriate

WORKFLOW:
1. Understand the research question fully
2. Break it into sub-questions
3. Search for information on each sub-question
4. Synthesize findings
5. Identify gaps and contradictions
6. Present conclusions with confidence levels

COMMUNICATION STYLE:
- Use clear, academic language
- Cite sources when possible
- Structure responses with headers
- Include "Confidence: High/Medium/Low" for key claims

CONSTRAINTS:
- Never fabricate sources or data
- If you can't find information, say so
- Maximum 3 tool calls per sub-question
- Always provide a summary at the end
"""
```

---

## Building a Customer Support Agent

```python
class CustomerSupportAgent:
    """Production-ready customer support agent."""

    def __init__(self, knowledge_base, ticket_system):
        self.kb = knowledge_base  # RAG retriever
        self.tickets = ticket_system
        self.memory = TokenAwareMemory(max_tokens=4000)

    def handle_query(self, user_message, user_id):
        # 1. Classify intent
        intent = self._classify_intent(user_message)

        # 2. Route based on intent
        if intent == "faq":
            return self._answer_faq(user_message)
        elif intent == "technical_issue":
            return self._troubleshoot(user_message, user_id)
        elif intent == "billing":
            return self._handle_billing(user_message, user_id)
        elif intent == "escalate":
            return self._escalate_to_human(user_message, user_id)
        else:
            return self._general_response(user_message)

    def _answer_faq(self, question):
        docs = self.kb.retrieve(question, k=3)
        if docs and docs[0].score > 0.85:
            return self._generate_response(question, docs)
        return "Let me connect you with a specialist for that."

    def _escalate_to_human(self, message, user_id):
        ticket = self.tickets.create(user_id, message)
        return (f"I've created ticket #{ticket.id}. "
                f"A human agent will follow up within 2 hours.")
```

---

## Evaluating Agent Performance

```python
class AgentEvaluator:
    """Measure agent effectiveness across dimensions."""

    def evaluate(self, agent, test_tasks):
        results = []
        for task in test_tasks:
            import time
            start = time.time()

            try:
                result = agent.run(task["input"])
                duration = time.time() - start

                results.append({
                    "task": task["description"],
                    "success": self._check_success(result, task["expected"]),
                    "steps": agent.step_count,
                    "tool_calls": agent.tool_call_count,
                    "duration_s": duration,
                    "tokens_used": agent.total_tokens,
                })
            except Exception as e:
                results.append({
                    "task": task["description"],
                    "success": False,
                    "error": str(e),
                })

        # Summary
        successes = sum(1 for r in results if r.get("success"))
        avg_steps = sum(r.get("steps", 0) for r in results) / len(results)
        print(f"Success rate: {successes}/{len(results)}")
        print(f"Avg steps per task: {avg_steps:.1f}")
        return results
```

---

## Common Agent Failure Modes

<svg xmlns="http://www.w3.org/2000/svg" width="600" height="372" font-family="sans-serif">
  <rect x="5" y="5" width="590" height="362" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="300" y="30" font-size="14" fill="#222" text-anchor="middle" font-weight="bold">AGENT FAILURE MODES</text>
  <line x1="5" y1="38" x2="595" y2="38" stroke="#333" stroke-width="1"/>
  <line x1="165" y1="5" x2="165" y2="367" stroke="#333" stroke-width="1"/>
  <rect x="6" y="39" width="158" height="53" fill="#ffebee" stroke="none"/>
  <rect x="166" y="39" width="428" height="53" fill="#ffebee" stroke="none"/>
  <line x1="5" y1="92" x2="595" y2="92" stroke="#bbb" stroke-width="1"/>
  <text x="14" y="71" font-size="12" fill="#c62828" font-weight="bold">LOOPING</text>
  <text x="176" y="63" font-size="12" fill="#222">Agent repeats the same action</text>
  <text x="176" y="79" font-size="12" fill="#222">Fix: Track action history, detect loops</text>
  <rect x="6" y="93" width="158" height="53" fill="#fce4ec" stroke="none"/>
  <rect x="166" y="93" width="428" height="53" fill="#fce4ec" stroke="none"/>
  <line x1="5" y1="146" x2="595" y2="146" stroke="#bbb" stroke-width="1"/>
  <text x="14" y="117" font-size="12" fill="#c62828" font-weight="bold">HALLUCINATED</text>
  <text x="14" y="133" font-size="12" fill="#c62828" font-weight="bold">TOOLS</text>
  <text x="176" y="117" font-size="12" fill="#222">Agent "uses" tools that don't exist</text>
  <text x="176" y="133" font-size="12" fill="#222">Fix: Strict tool validation</text>
  <rect x="6" y="147" width="158" height="53" fill="#fff3e0" stroke="none"/>
  <rect x="166" y="147" width="428" height="53" fill="#fff3e0" stroke="none"/>
  <line x1="5" y1="200" x2="595" y2="200" stroke="#bbb" stroke-width="1"/>
  <text x="14" y="171" font-size="12" fill="#c62828" font-weight="bold">WRONG TOOL</text>
  <text x="14" y="187" font-size="12" fill="#c62828" font-weight="bold">SELECTION</text>
  <text x="176" y="171" font-size="12" fill="#222">Uses search when calculator needed</text>
  <text x="176" y="187" font-size="12" fill="#222">Fix: Better tool descriptions</text>
  <rect x="6" y="201" width="158" height="53" fill="#ffebee" stroke="none"/>
  <rect x="166" y="201" width="428" height="53" fill="#ffebee" stroke="none"/>
  <line x1="5" y1="254" x2="595" y2="254" stroke="#bbb" stroke-width="1"/>
  <text x="14" y="233" font-size="12" fill="#c62828" font-weight="bold">OVER-PLANNING</text>
  <text x="176" y="225" font-size="12" fill="#222">Plans forever, never executes</text>
  <text x="176" y="241" font-size="12" fill="#222">Fix: Force action after N think steps</text>
  <rect x="6" y="255" width="158" height="53" fill="#fce4ec" stroke="none"/>
  <rect x="166" y="255" width="428" height="53" fill="#fce4ec" stroke="none"/>
  <line x1="5" y1="308" x2="595" y2="308" stroke="#bbb" stroke-width="1"/>
  <text x="14" y="279" font-size="12" fill="#c62828" font-weight="bold">PREMATURE</text>
  <text x="14" y="295" font-size="12" fill="#c62828" font-weight="bold">TERMINATION</text>
  <text x="176" y="279" font-size="12" fill="#222">Answers before gathering enough info</text>
  <text x="176" y="295" font-size="12" fill="#222">Fix: Require minimum evidence</text>
  <rect x="6" y="309" width="158" height="53" fill="#fff3e0" stroke="none"/>
  <rect x="166" y="309" width="428" height="53" fill="#fff3e0" stroke="none"/>
  <line x1="5" y1="362" x2="595" y2="362" stroke="#bbb" stroke-width="1"/>
  <text x="14" y="333" font-size="12" fill="#c62828" font-weight="bold">CONTEXT</text>
  <text x="14" y="349" font-size="12" fill="#c62828" font-weight="bold">OVERFLOW</text>
  <text x="176" y="333" font-size="12" fill="#222">Forgets earlier findings in long runs</text>
  <text x="176" y="349" font-size="12" fill="#222">Fix: Summarize + working memory</text>
</svg>
