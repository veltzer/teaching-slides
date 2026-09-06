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

# Bias in Generative Models

---

## What is Bias in AI?

Systematic errors that produce unfair or skewed outputs:

```misc
Types of bias in generative AI:

1. REPRESENTATION BIAS
   Training data over/under-represents groups
   "A photo of a CEO" → mostly white males

2. STEREOTYPING BIAS
   Model reinforces societal stereotypes
   "A nurse" → female, "An engineer" → male

3. ASSOCIATION BIAS
   Undesirable correlations learned from data
   Certain names associated with certain traits

4. LANGUAGE BIAS
   Better performance on English, Western contexts
   Non-English languages get worse quality

5. HISTORICAL BIAS
   Training data reflects past discrimination
   "A doctor in the 1950s" patterns applied to today
```

---

## Sources of Bias

![sources_of_bias](svg/courses/ai/generative-ai-applications/19_bias_in_generative_models/sources_of_bias.svg)

---

## Measuring Bias in Text Generation

```python
def measure_gender_bias(model_fn, n_samples=100):
    """Measure gender bias in occupation descriptions."""
    occupations = [
        "CEO", "nurse", "engineer", "teacher",
        "doctor", "secretary", "programmer", "librarian",
    ]

    results = {}
    for occupation in occupations:
        male_count = 0
        female_count = 0
        neutral_count = 0

        for _ in range(n_samples):
            response = model_fn(
                f"Write a short paragraph about a {occupation}."
            )
            # Count gendered pronouns
            text = response.lower()
            if "he " in text or "his " in text or " him " in text:
                male_count += 1
            if "she " in text or "her " in text:
                female_count += 1
            if "they " in text or "their " in text:
                neutral_count += 1

        results[occupation] = {
            "male": male_count / n_samples,
            "female": female_count / n_samples,
            "neutral": neutral_count / n_samples,
        }
    return results
```

---

## Gender Bias Example Results

![gender_bias_example_results](svg/courses/ai/generative-ai-applications/19_bias_in_generative_models/gender_bias_example_results.svg)

---

## Bias in Image Generation

![bias_in_image_generation](svg/courses/ai/generative-ai-applications/19_bias_in_generative_models/bias_in_image_generation.svg)

---

## Measuring Bias in Embeddings

```python
import numpy as np

def embedding_bias_test(embeddings_fn):
    """Word Embedding Association Test (WEAT)."""

    # Target concepts
    male_words = ["man", "boy", "he", "father", "son"]
    female_words = ["woman", "girl", "she", "mother", "daughter"]

    # Attribute concepts
    career_words = ["executive", "salary", "office", "professional"]
    family_words = ["home", "children", "family", "marriage"]

    # Get embeddings
    male_embs = [embeddings_fn(w) for w in male_words]
    female_embs = [embeddings_fn(w) for w in female_words]
    career_embs = [embeddings_fn(w) for w in career_words]
    family_embs = [embeddings_fn(w) for w in family_words]

    # Measure association
    # If male words are closer to career words
    # and female words are closer to family words
    # → gender-career bias exists

    male_career = np.mean([cosine_sim(m, c)
        for m in male_embs for c in career_embs])
    female_career = np.mean([cosine_sim(f, c)
        for f in female_embs for c in career_embs])

    bias_score = male_career - female_career
    print(f"Career-gender bias score: {bias_score:.4f}")
    # Positive = male-career association
```

---

## Bias Mitigation Strategies

![bias_mitigation_strategies](svg/courses/ai/generative-ai-applications/19_bias_in_generative_models/bias_mitigation_strategies.svg)

---

## Debiasing Through Prompting

```python
# Strategy 1: Explicit fairness instructions
system_prompt = """You are a helpful assistant.

IMPORTANT GUIDELINES:
- Use gender-neutral language unless specifically asked
- Represent diverse perspectives and demographics
- Avoid stereotypical associations
- When describing people in hypothetical scenarios,
  vary demographics across examples
- Use "they/them" pronouns for generic individuals
"""

# Strategy 2: Few-shot debiasing
examples = [
    ("Describe a CEO", "Dr. Aisha Patel leads the company with..."),
    ("Describe a nurse", "James, a registered nurse with 15 years..."),
    ("Describe an engineer",
     "Maria designs distributed systems at a tech firm..."),
]

# Strategy 3: Post-generation filtering
def debias_response(response):
    """Check for and flag biased content."""
    bias_check = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content":
                "Does this text contain stereotyping or bias? "
                "Respond: 'clean' or describe the bias found."},
            {"role": "user", "content": response},
        ],
    )
    return bias_check.choices[0].message.content
```

---

## Fairness Evaluation Framework

```python
class FairnessEvaluator:
    """Evaluate model fairness across demographics."""

    def __init__(self, model_fn):
        self.model_fn = model_fn

    def test_counterfactual(self, template, groups):
        """Test if model gives different responses for
        different demographic groups with same context."""
        results = {}
        for group_name, group_term in groups.items():
            prompt = template.format(person=group_term)
            response = self.model_fn(prompt)
            results[group_name] = {
                "response": response,
                "sentiment": analyze_sentiment(response),
                "length": len(response),
            }
        return results

# Example usage
evaluator = FairnessEvaluator(my_model)
results = evaluator.test_counterfactual(
    template="Write a recommendation letter for {person}, "
             "a software engineer applying for a senior role.",
    groups={
        "male_western": "John Smith",
        "female_western": "Jane Smith",
        "male_asian": "Wei Zhang",
        "female_asian": "Mei Lin",
    }
)
# Compare sentiment, length, and content across groups
```

---

## Case Study: Bias in Real Systems

![case_study_bias_in_real_systems](svg/courses/ai/generative-ai-applications/19_bias_in_generative_models/case_study_bias_in_real_systems.svg)

---

## Key Takeaways — Bias in Generative Models

1. **Bias** is systematic and comes from training data, process, and deployment
1. Bias manifests in **text** (stereotypes, associations) and **images** (representation)
1. **Measurement** tools (WEAT, counterfactual testing) help quantify bias
1. **Mitigation** must happen at every stage: data, training, output, deployment
1. **Prompt engineering** can reduce but not eliminate bias
1. **Regular auditing** is essential for deployed systems
1. There is often a **tension** between debiasing and accuracy
1. **No model is bias-free** — transparency about limitations is critical

---

## Toxicity Detection and Mitigation

```python
from transformers import pipeline

# Use a toxicity classifier
toxicity_classifier = pipeline(
    "text-classification",
    model="unitary/toxic-bert",
    top_k=None,  # Return all categories
)

def check_toxicity(text):
    results = toxicity_classifier(text)
    toxic_categories = [
        r for r in results[0]
        if r["score"] > 0.5 and r["label"] != "non-toxic"
    ]
    return {
        "is_toxic": len(toxic_categories) > 0,
        "categories": toxic_categories,
    }

# Integration in generation pipeline
def safe_generate(prompt):
    response = generate(prompt)
    toxicity = check_toxicity(response)

    if toxicity["is_toxic"]:
        # Option 1: Regenerate with safety prompt
        # Option 2: Filter and return safe version
        # Option 3: Return generic safe response
        return regenerate_safely(prompt)
    return response
```

---

## Fairness Metrics

![fairness_metrics](svg/courses/ai/generative-ai-applications/19_bias_in_generative_models/fairness_metrics.svg)

---

## Language and Cultural Bias

```python
# Testing for language bias
def test_language_quality(model_fn, prompts_by_language):
    """Compare response quality across languages."""
    results = {}

    for language, prompts in prompts_by_language.items():
        scores = []
        for prompt in prompts:
            response = model_fn(prompt)
            # Evaluate response quality
            quality = evaluate_quality(response, language)
            scores.append(quality)

        results[language] = {
            "avg_quality": sum(scores) / len(scores),
            "avg_length": sum(len(r) for r in responses) / len(responses),
        }

    return results

# Typical findings:
# English:    quality=4.5, length=250 tokens
# Spanish:    quality=4.2, length=230 tokens
# Chinese:    quality=4.0, length=200 tokens
# Swahili:    quality=2.8, length=120 tokens
# Cherokee:   quality=1.5, length=50 tokens
#
# Lower-resource languages get significantly worse quality
```

---

## Bias Audit Report Template

![bias_audit_report_template](svg/courses/ai/generative-ai-applications/19_bias_in_generative_models/bias_audit_report_template.svg)
