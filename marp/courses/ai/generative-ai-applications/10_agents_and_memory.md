# Agents and Memory

---

## Day 3: Agents, Memory & LangChain

![day_3_agents_memory_langchain](/svg/courses/ai/generative-ai-applications/10_agents_and_memory/day_3_agents_memory_langchain.svg)

---

## What is an AI Agent?

An `LLM` that can **observe**, **reason**, and **act** in a loop:

![what_is_an_ai_agent](/svg/courses/ai/generative-ai-applications/10_agents_and_memory/what_is_an_ai_agent.svg)

**Key difference from simple chatbots:** Agents can take **multiple steps** and use **external tools** to accomplish tasks.

---

## Simple Agent vs. Complex Agent

![simple_agent_vs_complex_agent](/svg/courses/ai/generative-ai-applications/10_agents_and_memory/simple_agent_vs_complex_agent.svg)

---

## Agent Architecture

![agent_architecture](/svg/courses/ai/generative-ai-applications/10_agents_and_memory/agent_architecture.svg)

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

![agent_planning_strategies](/svg/courses/ai/generative-ai-applications/10_agents_and_memory/agent_planning_strategies.svg)

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

![the_memory_problem](/svg/courses/ai/generative-ai-applications/10_agents_and_memory/the_memory_problem.svg)

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

![rag_retrieval_augmented_generation](/svg/courses/ai/generative-ai-applications/10_agents_and_memory/rag_retrieval_augmented_generation.svg)

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

![multi_agent_systems](/svg/courses/ai/generative-ai-applications/10_agents_and_memory/multi_agent_systems.svg)

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

![common_agent_failure_modes](/svg/courses/ai/generative-ai-applications/10_agents_and_memory/common_agent_failure_modes.svg)
