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
# Chain-of-Thought Reasoning

---

## What is Chain-of-Thought (CoT)?

Prompting the model to show its reasoning step by step:

```misc
Without CoT:
  Q: "Roger has 5 tennis balls. He buys 2 cans of 3 balls each.
      How many does he have now?"
  A: "11" ← Just the answer (often correct, but fragile)

With CoT:
  Q: Same question + "Think step by step."
  A: "Roger starts with 5 balls.
      He buys 2 cans, each with 3 balls.
      2 cans × 3 balls = 6 new balls.
      Total: 5 + 6 = 11 balls." ← Reasoning visible

Why it matters:
  - Enables VERIFICATION of reasoning
  - Improves accuracy on complex problems
  - Reduces certain types of errors
```

---

## CoT — The Key Insight

![cot_the_key_insight](svg/courses/ai/generative-ai-applications/08_chain_of_thought/cot_the_key_insight.svg)

---

## Standard Prompting vs Chain-of-Thought

![chain_of_thought](svg/courses/ai/generative-ai-applications/08_chain_of_thought/chain_of_thought.svg)

---

## Zero-Shot CoT — "Let's Think Step by Step"

The simplest CoT technique — just add a magic phrase:

```python
# Without CoT
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content":
        "A train travels 120km in 2 hours, then 180km in 3 hours. "
        "What is the average speed for the entire journey?"}],
    temperature=0,
)
# Might say "60 km/h" (wrong — averaged the speeds, not the journey)

# With zero-shot CoT
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content":
        "A train travels 120km in 2 hours, then 180km in 3 hours. "
        "What is the average speed for the entire journey? "
        "Let's think step by step."}],
    temperature=0,
)
# "Total distance: 120 + 180 = 300 km
#  Total time: 2 + 3 = 5 hours
#  Average speed: 300/5 = 60 km/h" ← Correct!
```

---

## Few-Shot CoT — Providing Reasoning Examples

```python
messages = [
    {"role": "system", "content":
        "Solve math problems step by step."},

    # Example with reasoning
    {"role": "user", "content":
        "A store has 45 apples. They sell 1/3 on Monday "
        "and 1/2 of the remainder on Tuesday. How many are left?"},
    {"role": "assistant", "content":
        "Step 1: Monday sales = 45 × 1/3 = 15 apples\n"
        "Step 2: After Monday = 45 - 15 = 30 apples\n"
        "Step 3: Tuesday sales = 30 × 1/2 = 15 apples\n"
        "Step 4: After Tuesday = 30 - 15 = 15 apples\n"
        "Answer: 15 apples"},

    # Actual problem
    {"role": "user", "content":
        "A tank is 2/5 full. After adding 30 liters, it becomes "
        "3/4 full. What is the tank's total capacity?"},
]
# Model follows the step-by-step pattern from the example
```

---

## Self-Consistency — Multiple CoT Paths

Generate multiple reasoning chains and take the majority vote:

```python
def self_consistency(prompt, n_samples=5):
    """Generate multiple reasoning paths and vote."""
    answers = []

    for _ in range(n_samples):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content":
                    prompt + "\nThink step by step."}
            ],
            temperature=0.7,  # Need randomness for diversity
            max_tokens=500,
        )
        text = response.choices[0].message.content

        # Extract final answer (last line or number)
        answer = extract_answer(text)
        answers.append(answer)

    # Majority vote
    from collections import Counter
    most_common = Counter(answers).most_common(1)[0]
    return most_common[0], most_common[1] / len(answers)

answer, confidence = self_consistency("What is 17 × 23?", n_samples=5)
print(f"Answer: {answer}, Confidence: {confidence:.0%}")
```

---

## Self-Consistency Visualized

![self_consistency_visualized](svg/courses/ai/generative-ai-applications/08_chain_of_thought/self_consistency_visualized.svg)

---

## Tree of Thoughts (ToT)

Explore multiple reasoning branches, evaluate, and prune:

```misc
                    Problem
                   /   |   \
                  /    |    \
            Thought1 Thought2 Thought3
            /    \      |       ✗ (prune)
           /      \     |
         T1a     T1b   T2a
          |       ✗     |
          |     (prune)  |
        T1a1           T2a1
          |              |
       Answer1        Answer2
                        ↑
                   (best answer)
```

```python
def tree_of_thoughts(problem, breadth=3, depth=3):
    thoughts = generate_initial_thoughts(problem, n=breadth)

    for step in range(depth):
        scored = [(evaluate_thought(t), t) for t in thoughts]
        scored.sort(reverse=True)
        best = [t for _, t in scored[:breadth]]  # Keep top-k
        thoughts = []
        for t in best:
            thoughts.extend(extend_thought(t, n=breadth))

    return select_best(thoughts)
```

---

## ReAct — Reasoning + Acting

Combine CoT with tool use in an interleaved pattern:

```misc
Question: "What is the population of the country where
           the Eiffel Tower is located?"

Thought 1: I need to find which country the Eiffel Tower
            is in, then look up its population.

Action 1: search("Eiffel Tower location")
Observation 1: The Eiffel Tower is in Paris, France.

Thought 2: The Eiffel Tower is in France. Now I need
            the population of France.

Action 2: search("France population 2024")
Observation 2: France population is approximately 68.4M.

Thought 3: I have the answer.

Answer: The population of France (where the Eiffel Tower
        is located) is approximately 68.4 million.
```

---

## Implementing ReAct in `Python`

```python
def react_agent(question, tools, max_steps=5):
    messages = [
        {"role": "system", "content":
            "You are an agent that reasons step by step. "
            "Available actions: search(query), calculate(expr). "
            "Format: Thought: ...\nAction: tool(args)\n"
            "After observations, continue reasoning. "
            "When done, respond with: Answer: ..."},
        {"role": "user", "content": question},
    ]

    for step in range(max_steps):
        response = client.chat.completions.create(
            model="gpt-4o", messages=messages, temperature=0
        )
        text = response.choices[0].message.content
        messages.append({"role": "assistant", "content": text})

        if "Answer:" in text:
            return text.split("Answer:")[-1].strip()

        # Parse and execute action
        if "Action:" in text:
            action = parse_action(text)
            result = execute_action(action, tools)
            messages.append(
                {"role": "user", "content": f"Observation: {result}"}
            )

    return "Could not determine answer within step limit."
```

---

## Structured CoT Prompting

```python
structured_cot_prompt = """Solve this problem using the following structure:

PROBLEM: {problem}

UNDERSTAND:
- What information is given?
- What is being asked?
- What are the constraints?

PLAN:
- What steps are needed?
- What formulas or methods apply?
- What order should steps be executed?

EXECUTE:
- Carry out each step with calculations
- Show intermediate results

VERIFY:
- Does the answer make sense?
- Check with estimation or alternative method

ANSWER:
- State the final answer clearly
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content":
        structured_cot_prompt.format(
            problem="A rectangular garden is 3x longer than wide. "
                    "If the perimeter is 64m, find the area."
        )}],
)
```

---

## CoT for Code Debugging

```python
debug_prompt = """Debug this Python code step by step.

def merge_sorted(a, b):
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
    return result

TRACE through with a=[1,3,5] and b=[2,4,6]:
1. What happens at each iteration?
2. Where does the bug occur?
3. What is missing?
4. Provide the corrected code.
"""

# The model will trace execution and find:
# Bug: j is never incremented in the else branch
# Missing: remaining elements aren't appended after loop
```

---

## CoT for Complex Decision Making

```python
decision_prompt = """You are evaluating cloud providers for a startup.

REQUIREMENTS:
- Budget: $5000/month
- Need: GPU compute for ML training
- Team size: 5 developers
- Region: Europe (GDPR compliance)
- Scale: 10x growth expected in 12 months

EVALUATE each option using chain-of-thought:

For each provider (AWS, GCP, Azure):
1. Available GPU instances in EU regions
2. Cost estimate for typical ML workload
3. GDPR compliance features
4. Scaling capabilities
5. Developer experience (SDKs, docs)

Score each criterion 1-5, then calculate weighted total.
Finally, provide a recommendation with justification.
"""
```

---

## When CoT Doesn't Help

![when_cot_does_not_help](svg/courses/ai/generative-ai-applications/08_chain_of_thought/when_cot_does_not_help.svg)

---

## Comparing CoT Techniques

| Technique | Accuracy Boost | Cost | Latency | Best For |
|-----------|---------------|------|---------|----------|
| Zero-shot CoT | +10-15% | 1× | ~1× | Quick improvement |
| Few-shot CoT | +15-25% | 1× | ~1× | Consistent format |
| Self-consistency | +5-10% over CoT | 5× | 5× | High-stakes decisions |
| Tree of Thoughts | +10-20% over CoT | 10× | 10× | Complex planning |
| ReAct | Task-dependent | 3-5× | 3-5× | Tasks needing tools |

---

## Exercise: CoT Reasoning Challenges

```python
"""
Exercise: Apply CoT techniques to these problems.

Problem 1 (Math):
  "A farmer has 3 fields. The first yields 400kg/hectare,
   the second 350kg/hectare, and the third 500kg/hectare.
   If the fields are 2.5, 3, and 1.5 hectares respectively,
   what is the average yield per hectare across all fields?"

Problem 2 (Logic):
  "In a room of 30 people, everyone shakes hands with
   everyone else exactly once. How many handshakes occur?"

Problem 3 (Code debugging with trace):
  Apply CoT to trace through a buggy binary search
  implementation and find the error.

For each:
1. Solve without CoT (direct answer)
2. Solve with zero-shot CoT
3. Solve with structured CoT (UNDERSTAND/PLAN/EXECUTE/VERIFY)
4. Compare accuracy across approaches
"""
```

---

## Key Takeaways — Chain-of-Thought Reasoning

1. **CoT** improves accuracy by making reasoning explicit
1. **"Let's think step by step"** is the simplest zero-shot CoT
1. **Few-shot CoT** provides reasoning patterns via examples
1. **Self-consistency** boosts reliability through majority voting
1. **Tree of Thoughts** enables exploration of multiple paths
1. **ReAct** combines reasoning with tool use
1. CoT helps most with **multi-step reasoning** tasks
1. The cost is increased **token usage** and **latency**

---

## Chain-of-Thought for Classification

```python
# CoT isn't just for math — it helps classification too

prompt_without_cot = """Classify this email as spam or not_spam:

"Dear valued customer, your account has been selected for a
special reward. Click here to claim your $500 gift card.
This offer expires in 24 hours!"

Classification:"""
# Model might just guess

prompt_with_cot = """Classify this email as spam or not_spam.
Think through the indicators:

"Dear valued customer, your account has been selected for a
special reward. Click here to claim your $500 gift card.
This offer expires in 24 hours!"

Analysis:
1. Does it use urgency tactics? (expires in 24 hours — yes)
2. Does it promise free money? ($500 gift card — yes)
3. Is it from a known sender? (generic "valued customer" — no)
4. Does it have suspicious links? ("click here" — yes)
5. Score: 4/4 spam indicators present

Classification: spam"""
```

---

## Plan-and-Solve Prompting

An improvement over basic CoT:

```python
plan_and_solve_prompt = """Let's first understand the problem
and devise a plan to solve it. Then, let's carry out the plan
and solve the problem step by step.

Problem: A library has 4,500 books. They receive donations of
120 books per month and remove 45 damaged books per month.
How many books will they have after 8 months?

Plan:
1. Calculate net monthly change in books
2. Calculate total change over 8 months
3. Add to starting amount

Solution:
Step 1: Net monthly change = 120 received - 45 removed = 75 books/month
Step 2: Total change over 8 months = 75 × 8 = 600 books
Step 3: Final count = 4,500 + 600 = 5,100 books

Answer: 5,100 books

Let me verify: 4,500 + (120 × 8) - (45 × 8)
= 4,500 + 960 - 360 = 5,100 ✓"""
```

**Key addition:** The plan step before execution improves accuracy on multi-step problems by 5-10% over basic CoT.

---

## Least-to-Most Prompting

Decompose a complex problem into simpler sub-problems:

```python
least_to_most_prompt = """Solve this by breaking it into simpler
sub-problems, solving each one, then combining.

Problem: "Last year, Amy was 3 times as old as Ben. In 5 years,
Amy will be twice as old as Ben. How old is Amy now?"

Sub-problem 1: Set up the equations
  Let Ben's age last year = x
  Amy's age last year = 3x
  In 5 years: Amy = 3x + 6, Ben = x + 6 (add 1 year + 5 years)
  Equation: 3x + 6 = 2(x + 6)

Sub-problem 2: Solve the equation
  3x + 6 = 2x + 12
  3x - 2x = 12 - 6
  x = 6 (Ben's age last year)

Sub-problem 3: Find Amy's current age
  Amy last year = 3 × 6 = 18
  Amy now = 18 + 1 = 19

Verification:
  Amy now: 19, Ben now: 7
  Last year: Amy 18, Ben 6 → 18 = 3 × 6 ✓
  In 5 years: Amy 24, Ben 12 → 24 = 2 × 12 ✓

Answer: Amy is 19 years old."""
```

---

## Skeleton-of-Thought (SoT)

Generate an outline first, then fill in details in parallel:

```python
def skeleton_of_thought(question, model="gpt-4o"):
    # Step 1: Generate skeleton (fast)
    skeleton = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content":
            f"Create a brief outline to answer: {question}\n"
            f"List 3-5 key points, one per line. Just headers."}],
        temperature=0,
        max_tokens=200,
    ).choices[0].message.content

    points = skeleton.strip().split("\n")

    # Step 2: Expand each point IN PARALLEL
    import concurrent.futures
    expanded = {}

    def expand_point(point):
        return client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content":
                f"Expand this point in 2-3 sentences:\n{point}"}],
            max_tokens=150,
        ).choices[0].message.content

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(expand_point, p): i
                   for i, p in enumerate(points)}
        for future in concurrent.futures.as_completed(futures):
            idx = futures[future]
            expanded[idx] = future.result()

    # Combine
    return "\n\n".join(
        f"{points[i]}\n{expanded[i]}" for i in sorted(expanded)
    )
# 2-3× faster than sequential generation!
```
