---
tags:
  - data-and-ai:nlp
  - concepts:dialogue-systems
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Dialogue Systems

---

## What This Chapter Covers

- Task-oriented vs open-domain dialogue, and the architectures for each
- The classical four-component pipeline: NLU, DST, policy, NLG
- Dialogue state tracking and how it became a deep learning task
- End-to-end neural dialogue and the rise of `LLM` agents
- Evaluation that captures both task completion and conversational quality
- Production realities: grounding, tool use, and safety

---

## Why Dialogue Is Hard

- Language is incremental — context arrives a turn at a time
- Users rarely state goals cleanly; they refine across turns
- Coreference, ellipsis, and implicit assumptions are everywhere
- The "right" answer depends on what came before in the same session
- Even minor misunderstandings compound into broken interactions

---

## Two Families of Dialogue Systems

![dialogue_taxonomy](svg/courses/ai/natural-language-processing/19_dialogue_systems/dialogue_taxonomy.svg)

---

## Task-Oriented Dialogue

- The user has a goal: book a flight, change a setting, get account info
- The system must execute API calls or database queries to satisfy it
- Success is measurable: did the user complete the task
- Domain is narrow but coverage of intents must be deep
- The setting where most production deployments live

---

## Open-Domain Dialogue

- Conversation for its own sake — companionship, brainstorming, chit-chat
- No clean success metric; engagement and coherence matter
- Trained on massive conversational data from social media or scripts
- The setting where modern `LLMs` shine
- Often combined with task capabilities in real products

---

## The Classical Pipeline

- Natural Language Understanding extracts intent and slot values
- Dialogue State Tracker maintains the running representation of the conversation
- Policy chooses the next system action based on state
- Natural Language Generation realizes the action as text
- A clean factorization that pre-deep-learning systems all shared

---

## Pipeline Architecture

![dialog_pipeline](svg/courses/ai/natural-language-processing/19_dialogue_systems/dialog_pipeline.svg)

---

## Natural Language Understanding

- Two sub-tasks: intent classification and slot filling
- Intent: a discrete label like `book_flight` or `cancel_order`
- Slots: typed entities like `departure_city`, `date`, `passengers`
- Joint models share representations between the two heads
- `BERT`-based intent + slot models are the standard backbone

---

## Slot Filling

- Treat slot filling as `BIO`-style sequence labeling
- A token can be `B-departure_city`, `I-departure_city`, or `O`
- Per-domain ontologies define the slot inventory
- Dialog systems often share an `NLU` model across many domains
- Mixed-domain training improves generalization to new intents

---

## Dialogue State Tracking

- A running summary of what the user has said about each slot
- Belief state is typically a probability distribution over slot values
- Tracks corrections, confirmations, and slot overrides across turns
- The classical `DSTC` benchmark series defined the task
- Modern trackers are sequence-to-sequence over the conversation

---

## Slot Lookup vs Generative Tracking

- Slot lookup: classifier per slot picks among ontology values
- Generative: decoder writes the full state as text
- Generative trackers handle unseen values gracefully
- Slot lookup remains a strong baseline for closed ontologies
- Hybrid systems mix the two depending on slot type

---

## Dialogue Policy

- Given state, decide the next system action
- Actions: `request(slot)`, `confirm(slot)`, `inform(value)`, `book()`
- Reinforcement learning trained policies maximize task completion reward
- Hand-written policies dominate production for predictability
- Modern `LLM` systems collapse policy into the generation step

---

## Reinforcement Learning for Dialogue

- Frame dialogue as a Markov Decision Process over states and actions
- Reward shapes the agent toward task completion and brevity
- User simulators enable training without huge user populations
- Deep `RL` policies plateaued on most narrow-domain benchmarks
- Often used for fine-tuning conversational `LLMs` post-pretraining

---

## Natural Language Generation

- Turn the chosen action into a fluent system utterance
- Templates: simple, predictable, no surprises, but feel rigid
- Neural `NLG`: paraphrases templates, varies surface form, sounds natural
- Hybrid: templated structure with neural realization for free-text slots
- Templates dominate when consistency matters more than naturalness

---

## End-to-End Neural Dialogue

- One model takes conversation history and emits the next system turn
- No explicit state tracker, policy, or generator
- `BlenderBot` and dialogue-tuned `T5` were early examples
- Easy to train on conversation logs at scale
- Hard to debug when the model misbehaves

---

## LLM-Based Dialogue Agents

- Instruction-tuned `LLMs` handle dialogue out of the box
- Persona, tone, and constraints set via system prompt
- Tool calling extends capabilities to API and database access
- Memory across sessions implemented externally with retrieval
- The current default for both task-oriented and open-domain dialogue

---

## LLM Dialogue Stack

![llm_dialog_stack](svg/courses/ai/natural-language-processing/19_dialogue_systems/llm_dialog_stack.svg)

---

## Grounding in Knowledge

- Ungrounded dialogue agents hallucinate confidently
- Retrieve relevant documents at each turn and cite them
- Inject database facts when the user asks for personal data
- Tool calls are the most explicit form of grounding
- Without grounding, even strong `LLMs` produce convincing fabrications

---

## Multi-Turn Coreference

- "Book it for tomorrow" — what is `it`
- The model must resolve references against the dialog history
- Long conversations strain the context window
- Conversation summaries condense old turns into a few sentences
- Retrieval over conversation history fills the gap for very long sessions

---

## Persona and Style

- A consistent persona makes the agent feel coherent
- Trained via instruction tuning or system prompts
- Style transfer techniques adapt tone to formality requirements
- Persona drift across long conversations is a real failure mode
- A short persona statement in every system prompt mitigates drift

---

## Safety Filters

- Pre-filter user input for prompt injection and policy violations
- Post-filter system output for harmful, biased, or off-topic content
- Decline politely on out-of-scope or unsafe requests
- Rate limiting and abuse detection for production deployments
- Layered defense beats any single filter

---

## Evaluation: Task Completion

- Did the user achieve their goal in the conversation
- Measured by API call success or simulated user surveys
- The single most important metric for task-oriented systems
- Easier to score than conversational quality
- Deceptively simple: many calls succeed but feel terrible

---

## Evaluation: Conversational Quality

- Coherence — does the response follow from the prior turns
- Engagingness — does the user want to keep talking
- Specificity — does the response address the user's actual point
- Hallucination — does the response invent facts
- Almost always requires human raters for trustworthy scores

---

## Evaluation: Automatic Metrics

- `BLEU` and `ROUGE` correlate poorly with conversational quality
- Embedding-based metrics like `BERTScore` do better but not great
- `LLM`-as-judge prompted to rate dialogue is increasingly common
- All automatic metrics drift from human preference under distribution shift
- Calibrate against human ratings on a held-out subset

---

## Production Pitfalls

- Treating multi-turn context as if it were a single prompt
- Forgetting to capture conversation state for analytics
- Letting the model commit to actions without confirmation
- Skipping fallback behavior for tool failures
- Underestimating how long users will keep a session open

---

## Anti-Patterns

- Training a chatbot on web scrapes and shipping it to consumers
- Hand-crafting policy for every edge case rather than abstracting state
- Single-turn evaluation for inherently multi-turn systems
- Ignoring abandonment as a signal — users leave when conversations break
- Personas that promise capabilities the system does not have

---

## When to Use Each Architecture

- Narrow domain, high accuracy needed -> classical pipeline with `NLU`
- Open domain, conversational feel -> instruction-tuned `LLM`
- Mixed -> `LLM` with structured tool calls and retrieval
- Hard real-time constraints -> templated `NLG` with hand-written policy
- The right answer is almost always a hybrid

---

## Summary

- Dialogue systems split into task-oriented and open-domain families
- The classical four-stage pipeline still anchors many production systems
- End-to-end `LLM` agents replace the pipeline when flexibility matters more than control
- Evaluation requires both task completion and conversational quality
- Production-grade dialogue blends grounding, tool use, and safety filtering
