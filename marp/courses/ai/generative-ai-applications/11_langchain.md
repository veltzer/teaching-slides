# LangChain

---

## What is LangChain?

A framework for building `LLM`-powered applications:

```diagram
┌──────────────────────────────────────────────────┐
│                  LANGCHAIN                        │
│                                                   │
│  ┌──────────┐ ┌──────────┐ ┌─────────────────┐  │
│  │  Models  │ │ Prompts  │ │  Output Parsers │  │
│  │  (LLMs)  │ │ (Templ.) │ │  (Structured)   │  │
│  └──────────┘ └──────────┘ └─────────────────┘  │
│                                                   │
│  ┌──────────┐ ┌──────────┐ ┌─────────────────┐  │
│  │  Chains  │ │  Memory  │ │    Agents       │  │
│  │  (LCEL)  │ │          │ │    (Tools)      │  │
│  └──────────┘ └──────────┘ └─────────────────┘  │
│                                                   │
│  ┌──────────┐ ┌──────────┐ ┌─────────────────┐  │
│  │ Document │ │  Vector  │ │  Retrievers     │  │
│  │ Loaders  │ │  Stores  │ │                 │  │
│  └──────────┘ └──────────┘ └─────────────────┘  │
└──────────────────────────────────────────────────┘
```

---

## Installing LangChain

```python
# Core package
pip install langchain

# Provider-specific packages
pip install langchain-openai        # OpenAI models
pip install langchain-anthropic     # Claude models
pip install langchain-community     # Community integrations
pip install langchain-chroma        # ChromaDB vector store

# Additional useful packages
pip install langchain-text-splitters  # Document chunking
pip install langgraph                 # Agent orchestration
pip install langsmith                 # Observability/tracing
```

---

## LangChain Basics — Chat Models

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize model
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# Simple invocation
response = llm.invoke([
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is LangChain?"),
])
print(response.content)

# Batch processing
responses = llm.batch([
    [HumanMessage(content="What is Python?")],
    [HumanMessage(content="What is JavaScript?")],
    [HumanMessage(content="What is Rust?")],
])

# Streaming
for chunk in llm.stream([HumanMessage(content="Tell me a joke")]):
    print(chunk.content, end="", flush=True)
```

---

## Prompt Templates

```python
from langchain_core.prompts import ChatPromptTemplate

# Simple template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} expert."),
    ("human", "{question}"),
])

# Use the template
messages = prompt.invoke({
    "role": "Python",
    "question": "How do decorators work?"
})
response = llm.invoke(messages)

# Template with multiple variables
analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a code reviewer. Language: {language}"),
    ("human", "Review this code for {focus_area}:\n\n{code}"),
])

messages = analysis_prompt.invoke({
    "language": "Python",
    "focus_area": "security vulnerabilities",
    "code": "user_input = input(); eval(user_input)",
})
```

---

## LCEL — LangChain Expression Language

Compose components using the pipe `|` operator:

```python
from langchain_core.output_parsers import StrOutputParser

# Chain: prompt → model → parser
chain = prompt | llm | StrOutputParser()

# Invoke the chain
result = chain.invoke({
    "role": "database",
    "question": "Explain indexing in PostgreSQL"
})
print(result)  # Just the string, not a Message object

# More complex chain
from langchain_core.prompts import ChatPromptTemplate

summarize = ChatPromptTemplate.from_messages([
    ("human", "Summarize in 1 sentence: {text}"),
]) | llm | StrOutputParser()

translate = ChatPromptTemplate.from_messages([
    ("human", "Translate to French: {text}"),
]) | llm | StrOutputParser()

# Compose chains
result = summarize.invoke({"text": long_article})
translation = translate.invoke({"text": result})
```

---

## Output Parsers — Structured Output

```python
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

class CodeReview(BaseModel):
    issues: List[str] = Field(description="List of issues found")
    severity: str = Field(description="overall severity: low/medium/high")
    suggestions: List[str] = Field(description="Improvement suggestions")

parser = JsonOutputParser(pydantic_object=CodeReview)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Review the code and respond in this format:\n"
     "{format_instructions}"),
    ("human", "Review: {code}"),
])

chain = prompt | llm | parser

result = chain.invoke({
    "code": "password = 'admin123'",
    "format_instructions": parser.get_format_instructions(),
})
print(result)
# {'issues': ['Hardcoded password'], 'severity': 'high',
#  'suggestions': ['Use environment variables']}
```

---

## Document Loaders

Load data from various sources:

```python
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    WebBaseLoader,
    DirectoryLoader,
)

# Load a text file
loader = TextLoader("data/report.txt")
docs = loader.load()

# Load a PDF
loader = PyPDFLoader("data/paper.pdf")
docs = loader.load()  # One document per page

# Load from a website
loader = WebBaseLoader("https://example.com/article")
docs = loader.load()

# Load all files in a directory
loader = DirectoryLoader(
    "data/",
    glob="**/*.txt",
    loader_cls=TextLoader,
)
docs = loader.load()

# Each document has: .page_content and .metadata
for doc in docs:
    print(f"Source: {doc.metadata['source']}")
    print(f"Content: {doc.page_content[:100]}...")
```

---

## Text Splitters

```python
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    TokenTextSplitter,
)

# Recursive character splitter (most common)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,       # Max characters per chunk
    chunk_overlap=200,     # Overlap between chunks
    separators=["\n\n", "\n", ". ", " ", ""],
    # Tries to split at paragraph, then sentence, etc.
)

chunks = splitter.split_documents(docs)
print(f"Split {len(docs)} docs into {len(chunks)} chunks")

# Token-based splitter (more precise for LLM context)
token_splitter = TokenTextSplitter(
    chunk_size=500,        # Max tokens per chunk
    chunk_overlap=50,
    model_name="gpt-4o",  # Use model's tokenizer
)
chunks = token_splitter.split_documents(docs)
```

---

## Vector Stores

```python
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Create embeddings and vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Index documents
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db",
    collection_name="my_docs",
)

# Similarity search
results = vectorstore.similarity_search(
    "What is the company's revenue?",
    k=3,
)
for doc in results:
    print(doc.page_content[:100])

# Search with score
results = vectorstore.similarity_search_with_score(
    "quarterly earnings",
    k=3,
)
for doc, score in results:
    print(f"Score: {score:.4f} | {doc.page_content[:80]}")
```

---

## Building RAG with LangChain

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Create retriever from vector store
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4},
)

# RAG prompt
rag_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Answer based on the context below. If you can't find "
     "the answer in the context, say 'I don't have that information.'\n\n"
     "Context: {context}"),
    ("human", "{question}"),
])

# Build RAG chain
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# Use it
answer = rag_chain.invoke("What were the Q3 financial results?")
print(answer)
```

---

## LangChain Memory

```python
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Memory setup
memory = ConversationBufferMemory(return_messages=True)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

# Manual memory management with LCEL
from langchain_core.runnables import RunnablePassthrough

chain = prompt | llm | StrOutputParser()

def chat_with_memory(user_input):
    history = memory.load_memory_variables({})["history"]
    response = chain.invoke({
        "input": user_input,
        "history": history,
    })
    memory.save_context(
        {"input": user_input},
        {"output": response},
    )
    return response

print(chat_with_memory("My name is Alice"))
print(chat_with_memory("What's my name?"))  # "Alice!"
```

---

## LangChain Summary Memory

```python
from langchain.memory import ConversationSummaryMemory

summary_memory = ConversationSummaryMemory(
    llm=ChatOpenAI(model="gpt-4o-mini"),
    return_messages=True,
)

# After many messages, old ones get summarized:
# Instead of keeping 50 messages (10K tokens),
# keeps a summary (200 tokens) + recent messages

# Summary example:
# "The user (Alice) is a data scientist interested in
#  NLP. She asked about tokenization, embeddings, and
#  fine-tuning. She prefers PyTorch over TensorFlow."

# Hybrid: Summary + Buffer Window
from langchain.memory import ConversationSummaryBufferMemory

hybrid_memory = ConversationSummaryBufferMemory(
    llm=ChatOpenAI(model="gpt-4o-mini"),
    max_token_limit=2000,  # Summarize when exceeding this
    return_messages=True,
)
```

---

## LangChain Agents

```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    # Simulated search
    return f"Results for '{query}': ..."

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    return str(eval(expression))

# Create agent
tools = [search_web, calculate]

agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant with access to tools."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, agent_prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = executor.invoke({"input": "What is 15% of 847?"})
print(result["output"])
```

---

## LangGraph — Advanced Agent Orchestration

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated

class AgentState(TypedDict):
    messages: list
    next_step: str

def researcher(state: AgentState) -> AgentState:
    """Research step — gather information."""
    # ... research logic ...
    return {"messages": state["messages"] + [research_result],
            "next_step": "analyzer"}

def analyzer(state: AgentState) -> AgentState:
    """Analyze step — process research."""
    # ... analysis logic ...
    return {"messages": state["messages"] + [analysis],
            "next_step": "writer"}

def writer(state: AgentState) -> AgentState:
    """Write step — produce final output."""
    # ... writing logic ...
    return {"messages": state["messages"] + [report],
            "next_step": "end"}

# Build graph
graph = StateGraph(AgentState)
graph.add_node("researcher", researcher)
graph.add_node("analyzer", analyzer)
graph.add_node("writer", writer)
graph.add_edge("researcher", "analyzer")
graph.add_edge("analyzer", "writer")
graph.add_edge("writer", END)
graph.set_entry_point("researcher")

app = graph.compile()
result = app.invoke({"messages": ["Research AI agents"], "next_step": "researcher"})
```

---

## LangSmith — Observability

```python
# Enable tracing (set environment variables)
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__..."
os.environ["LANGCHAIN_PROJECT"] = "my-genai-app"

# All LangChain calls are now automatically traced
# View traces at: smith.langchain.com

# Traces show:
# ┌─────────────────────────────────────────┐
# │ Chain: rag_chain                        │
# │ ├─ Retriever: similarity_search         │
# │ │  └─ Duration: 45ms, 4 docs returned   │
# │ ├─ Prompt: rag_prompt                   │
# │ │  └─ Variables: context=..., q=...     │
# │ ├─ LLM: gpt-4o                         │
# │ │  └─ Tokens: 1200 in, 350 out          │
# │ │  └─ Duration: 2.3s                    │
# │ └─ Parser: StrOutputParser              │
# │    └─ Output: "Based on the data..."    │
# └─────────────────────────────────────────┘
```

---

## Comparing LangChain with Alternatives

| Feature | LangChain | LlamaIndex | Direct API |
|---------|-----------|------------|------------|
| Learning curve | Medium | Medium | Low |
| Flexibility | High | Medium | Highest |
| RAG support | Good | Excellent | Manual |
| Agent support | Excellent | Good | Manual |
| Community | Large | Medium | N/A |
| Abstraction | High | High | None |
| Debugging | LangSmith | Built-in | Custom |
| Best for | Agents, chains | RAG, data | Simple apps |

**Rule of thumb:**
- Simple apps → Direct API calls
- RAG-heavy apps → `LlamaIndex` or `LangChain`
- Agent-heavy apps → `LangChain` / `LangGraph`

---

## Exercise: LangChain RAG Pipeline

```python
"""
Exercise: Build a complete RAG system with LangChain.

Requirements:
1. Load documents from a directory of text files
2. Split into chunks with appropriate overlap
3. Create a ChromaDB vector store
4. Build a RAG chain with conversation memory
5. Add source citation to responses

Steps:
1. Create sample documents (3-5 text files about a topic)
2. Load and split with RecursiveCharacterTextSplitter
3. Index into ChromaDB
4. Build RAG chain with LCEL
5. Add ConversationBufferMemory
6. Test with multi-turn conversation

Bonus:
- Add a "sources" field to responses
- Implement hybrid search (keyword + semantic)
- Add conversation summary memory for long sessions
"""
```

---

## Key Takeaways — LangChain

1. `LangChain` provides building blocks for `LLM` applications
1. **LCEL** (pipe operator) enables composable chains
1. **Document loaders** + **text splitters** prepare data for RAG
1. **Vector stores** enable semantic search over your documents
1. **Memory** classes handle conversation persistence
1. **Agents** combine `LLM` reasoning with tool use
1. **LangGraph** enables complex multi-step agent workflows
1. **LangSmith** provides observability and debugging

---

## Custom LangChain Tools

```python
from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field
from typing import Optional

@tool
def search_products(
    query: str,
    category: Optional[str] = None,
    max_price: Optional[float] = None,
) -> str:
    """Search the product catalog.

    Args:
        query: Search terms for product name or description
        category: Filter by category (electronics, clothing, etc.)
        max_price: Maximum price filter in USD
    """
    # Your search implementation
    results = db.search(query, category=category, max_price=max_price)
    return format_results(results)

# Or use StructuredTool for more control
class SearchInput(BaseModel):
    query: str = Field(description="Search terms")
    category: Optional[str] = Field(None, description="Category filter")

search_tool = StructuredTool.from_function(
    func=search_products,
    name="product_search",
    description="Search the product catalog by name or features",
    args_schema=SearchInput,
)
```

---

## Advanced RAG — Hybrid Search

```python
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

# Semantic search (embedding-based)
vectorstore = Chroma.from_documents(docs, embeddings)
semantic_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

# Keyword search (BM25)
keyword_retriever = BM25Retriever.from_documents(docs)
keyword_retriever.k = 5

# Combine both with Ensemble Retriever
hybrid_retriever = EnsembleRetriever(
    retrievers=[semantic_retriever, keyword_retriever],
    weights=[0.6, 0.4],  # 60% semantic, 40% keyword
)

# Benefits of hybrid search:
# Semantic: finds conceptually similar content
#   "How to fix login issues" → "Authentication troubleshooting"
# Keyword: finds exact terms
#   "error code 403" → documents containing "403"
# Combined: best of both worlds

results = hybrid_retriever.invoke("error code 403 authentication")
```

---

## Advanced RAG — Multi-Query Retriever

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

# Generate multiple search queries from a single question
multi_retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=ChatOpenAI(model="gpt-4o-mini"),
)

# For question: "What are the side effects of aspirin?"
# The retriever generates multiple queries:
# 1. "aspirin adverse reactions"
# 2. "risks of taking aspirin"
# 3. "aspirin safety profile"
# Then combines results from all queries

# This increases recall by searching from multiple angles

# Custom prompt for query generation
from langchain_core.prompts import PromptTemplate

query_prompt = PromptTemplate(
    input_variables=["question"],
    template="""Generate 3 different search queries to find
    information about: {question}
    Queries should approach the topic from different angles.
    Output one query per line, nothing else.""",
)
```

---

## LangChain Callbacks

```python
from langchain_core.callbacks import BaseCallbackHandler
from typing import Any

class CostTracker(BaseCallbackHandler):
    """Track LLM costs across the chain."""

    PRICES = {"gpt-4o": {"input": 2.5, "output": 10.0}}

    def __init__(self):
        self.total_cost = 0
        self.calls = 0

    def on_llm_end(self, response, **kwargs: Any):
        self.calls += 1
        usage = response.llm_output.get("token_usage", {})
        model = kwargs.get("model", "gpt-4o")
        prices = self.PRICES.get(model, {"input": 0, "output": 0})
        cost = (
            usage.get("prompt_tokens", 0) * prices["input"] +
            usage.get("completion_tokens", 0) * prices["output"]
        ) / 1_000_000
        self.total_cost += cost

# Use in any chain
tracker = CostTracker()
chain.invoke({"question": "..."}, config={"callbacks": [tracker]})
print(f"Cost: ${tracker.total_cost:.4f}")
```

---

## LangChain — Routing Chains

```python
from langchain_core.runnables import RunnableLambda, RunnableBranch

# Route to different chains based on the question type
def classify_question(question):
    response = llm.invoke(
        f"Classify this question as one of: "
        f"technical, billing, general\n"
        f"Question: {question}\n"
        f"Category:"
    )
    return response.content.strip().lower()

# Different chains for different question types
technical_chain = tech_prompt | llm | StrOutputParser()
billing_chain = billing_prompt | llm | StrOutputParser()
general_chain = general_prompt | llm | StrOutputParser()

# Build router
router = RunnableBranch(
    (lambda x: classify_question(x["question"]) == "technical",
     technical_chain),
    (lambda x: classify_question(x["question"]) == "billing",
     billing_chain),
    general_chain,  # Default
)

# Each question type gets specialized handling
result = router.invoke({"question": "My API key isn't working"})
```

---

## Parent Document Retriever

Retrieve small chunks but return the full parent document:

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Small chunks for accurate retrieval
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

# Larger chunks for context when answering
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)

store = InMemoryStore()
vectorstore = Chroma(embedding_function=embeddings)

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

# Index documents
retriever.add_documents(docs)

# Search finds small chunks (precise matching)
# But returns the PARENT chunk (more context for the LLM)
results = retriever.invoke("What is the refund policy?")
# Returns ~2000 char chunk containing the matching section
```

---

## Conversational RAG Chain

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Step 1: Contextualize the question using conversation history
contextualize_prompt = ChatPromptTemplate.from_messages([
    ("system", "Given the chat history and latest question, "
               "reformulate the question to be standalone."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_prompt
)

# Step 2: Answer based on retrieved documents
answer_prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer based on this context:\n\n{context}"),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

doc_chain = create_stuff_documents_chain(llm, answer_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, doc_chain)

# Use with conversation history
result = rag_chain.invoke({
    "input": "What about their pricing?",
    "chat_history": [
        HumanMessage("Tell me about LangChain"),
        AIMessage("LangChain is a framework for..."),
    ],
})
```

---

## LangChain Output Validation

```python
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from typing import List

class ProductRecommendation(BaseModel):
    products: List[str] = Field(
        description="List of recommended product names",
        min_length=1, max_length=5,
    )
    reasoning: str = Field(
        description="Why these products were chosen",
        min_length=20,
    )
    confidence: float = Field(
        description="Confidence score 0-1",
        ge=0.0, le=1.0,
    )

    @validator("products")
    def products_not_empty(cls, v):
        if not v:
            raise ValueError("Must recommend at least 1 product")
        return v

parser = PydanticOutputParser(pydantic_object=ProductRecommendation)

# If the model output doesn't match, parser raises an error
# You can then retry with error feedback
chain_with_retry = prompt | llm | parser.with_retry(
    retry_if_exception_type=(ValueError,),
    max_retries=3,
)
```

---

## Caching in LangChain

```python
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache, InMemoryCache

# In-memory cache (fastest, lost on restart)
set_llm_cache(InMemoryCache())

# SQLite cache (persists across restarts)
set_llm_cache(SQLiteCache(database_path=".langchain_cache.db"))

# Now identical LLM calls are cached automatically
llm = ChatOpenAI(model="gpt-4o")

# First call: hits the API
response1 = llm.invoke("What is Python?")

# Second identical call: returns cached result instantly
response2 = llm.invoke("What is Python?")

# Semantic cache (cache similar, not just identical queries)
from langchain_community.cache import RedisSemanticCache

set_llm_cache(RedisSemanticCache(
    redis_url="redis://localhost:6379",
    embedding=OpenAIEmbeddings(),
    score_threshold=0.95,  # How similar must queries be
))
```

---

## LangChain Document Transformers

```python
from langchain_community.document_transformers import (
    EmbeddingsRedundantFilter,
    LongContextReorder,
)

# Remove redundant documents (near-duplicates)
redundant_filter = EmbeddingsRedundantFilter(embeddings=embeddings)
unique_docs = redundant_filter.transform_documents(docs)

# Reorder documents for better LLM comprehension
# LLMs struggle with the "lost in the middle" problem:
# they attend better to the start and end of context
reorder = LongContextReorder()
reordered = reorder.transform_documents(docs)
# Places most relevant docs at START and END
# Less relevant in the MIDDLE

# Combine in a pipeline
from langchain.retrievers.document_compressors import DocumentCompressorPipeline

pipeline = DocumentCompressorPipeline(
    transformers=[
        redundant_filter,
        reorder,
    ]
)
```

---

## Building Production LangChain Applications

```python
# Production patterns for LangChain

from langchain_core.runnables import RunnableConfig
import asyncio

class ProductionRAG:
    """Production-ready RAG application."""

    def __init__(self, retriever, llm):
        self.chain = (
            {"context": retriever | self._format, "question": RunnablePassthrough()}
            | rag_prompt | llm | StrOutputParser()
        )

    async def query_async(self, question):
        """Async query for web applications."""
        return await self.chain.ainvoke(question)

    def query_with_sources(self, question):
        """Return answer with source citations."""
        docs = self.retriever.invoke(question)
        context = self._format(docs)

        answer = self.chain.invoke(question)

        sources = [
            {"content": d.page_content[:100],
             "source": d.metadata.get("source", "unknown")}
            for d in docs
        ]
        return {"answer": answer, "sources": sources}

    def _format(self, docs):
        return "\n\n".join(d.page_content for d in docs)
```
