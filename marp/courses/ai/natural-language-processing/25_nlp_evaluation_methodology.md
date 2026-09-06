---
tags:
  - data-and-ai:nlp
  - concepts:evaluation
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---

# NLP Evaluation Methodology

---

## What This Chapter Covers

- The metrics zoo and how to pick the right one
- Reference-based, reference-free, and learned metrics
- Statistical significance and the dangers of overfitting to benchmarks
- Human evaluation: protocols, costs, and quality control
- `LLM`-as-judge and its calibration pitfalls
- Holistic evaluation across capability, safety, and cost

---

## Why Evaluation Is the Hard Part

- Models are easy to train; deciding which is better is hard
- A wrong metric ships a worse system with measurable confidence
- Different stakeholders care about different metrics
- Evaluation budgets are usually a tenth of training budgets when they should be more
- The deepest engineering challenges in modern `NLP` live here

---

## Levels of Evaluation

![evaluation_levels](svg/courses/ai/natural-language-processing/25_nlp_evaluation_methodology/evaluation_levels.svg)

---

## Intrinsic vs Extrinsic Evaluation

- Intrinsic: measure the property a model is supposed to have (perplexity, accuracy)
- Extrinsic: measure downstream task performance the model enables
- Intrinsic is cheap but can drift from real value
- Extrinsic is expensive but tells you what users will see
- Healthy programs run both and reconcile divergences

---

## Reference-Based Metrics

- Compare model output to one or more human references
- `BLEU`, `ROUGE`, `chrF`, `METEOR`, `Exact Match`, `F1`
- Cheap, deterministic, easy to log
- Reward lexical overlap, punish paraphrase
- Plateau quickly as model quality improves

---

## BLEU and Its Limits

- N-gram precision against references with brevity penalty
- The default `MT` metric for two decades
- Per-sentence noisy; corpus-level meaningful
- Many configurations of `BLEU` exist; report `sacreBLEU` with signature
- Replaced as the headline metric by `COMET` and `chrF` in modern work

---

## ROUGE for Summarization

- Recall-oriented n-gram overlap, with `ROUGE-1`, `ROUGE-2`, and `ROUGE-L`
- The de facto summarization metric since 2004
- Correlates poorly with faithfulness — fluent wrong summaries score well
- Always pair with a faithfulness or `BERTScore` metric
- Reporting only `ROUGE` is now a red flag in reviews

---

## BERTScore and Embedding Metrics

- Compare contextual embeddings of candidate and reference tokens
- Captures paraphrase that lexical metrics miss
- Slower, but works well even on a CPU for small evaluation sets
- Good correlation with human ratings on most generation tasks
- A reasonable second metric to pair with `BLEU` or `ROUGE`

---

## Learned Metrics

- Train a regressor from human ratings to predict quality
- `COMET`, `BLEURT`, `BARTScore`, `UniEval`
- Best correlation with human judgment available
- Cost: GPU at evaluation time, less interpretable
- Becoming the default for `MT` and increasingly for summarization

---

## Reference-Free Metrics

- Score a generation without a reference
- Useful when references are unavailable or unreliable
- Quality estimation for `MT`, faithfulness scoring for summaries
- Often less reliable than reference-based metrics
- Pair with reference-based when references exist

---

## Perplexity

- The exponentiated cross-entropy of the model on a held-out corpus
- Lower is better; reflects how well the model fits the data
- Common for language model comparison
- Sensitive to tokenizer; cross-model comparisons need care
- Disconnected from generation quality at the high end

---

## Task-Specific Benchmarks

- `GLUE`, `SuperGLUE` for classification and inference
- `SQuAD`, `NaturalQuestions` for QA
- `WMT` for `MT`, `XSum` and `CNN/DM` for summarization
- `MMLU`, `BIG-bench`, `HELM` for `LLM` capability profiling
- Standardize methodology, but they age fast

---

## Benchmark Saturation

- Models hit human parity on a benchmark
- Subsequent gains say less about real progress
- New benchmarks emerge to differentiate frontier models
- Mind the leaderboard treadmill — invest in a benchmark that matches your task
- Saturation is when to switch metrics, not declare victory

---

## Test-Set Contamination

- Training data scraped from the web includes public test sets
- Models score high on benchmarks they have effectively memorized
- A growing risk as `LLMs` train on ever larger crawls
- Decontamination protocols exist but are imperfect
- Healthy benchmarks have private held-out sets that prove generalization

---

## Statistical Significance

- A 0.5 point `BLEU` gap on a 1000-sentence test is rarely significant
- Bootstrap resampling computes confidence intervals
- Paired tests across systems control for variance from input
- `sacreBLEU` includes built-in significance support
- Report the `p` value or interval, not just the point estimate

---

## Significance Testing in Practice

```python
from scipy import stats

bleu_a = [...]  # per-sentence BLEU for system A
bleu_b = [...]  # per-sentence BLEU for system B

stat, p = stats.wilcoxon(bleu_a, bleu_b)
print(f"Wilcoxon p = {p:.4f}")
# p < 0.05 -> the systems differ significantly on this test
```

- Paired non-parametric tests handle skewed metric distributions
- Worth running before publishing a new "state of the art"

---

## Human Evaluation: When and How

- The gold standard for any generation task
- Scales: pairwise preference, Likert ratings, error annotation
- Quality control: inter-annotator agreement, gold questions, training rounds
- Budget for re-evaluation across releases
- Most reliable when the rubric is task-specific and well-piloted

---

## Direct Assessment

- Annotators rate outputs on a 0-100 scale against a reference or source
- Used in `WMT` evaluation campaigns
- Easy to train annotators, but ratings drift over time
- Per-annotator calibration helps comparability
- Pair with pairwise comparisons for robustness

---

## Multidimensional Quality Metrics (MQM)

- Annotators mark errors with categories: accuracy, fluency, locale, style
- Errors weighted by severity (minor, major, critical)
- More expressive than single-number ratings
- The current standard for high-stakes `MT` evaluation
- Closer to how editors actually think about quality

---

## LLM as Judge

- Prompt a strong `LLM` to rate or compare outputs
- Cheap, fast, and surprisingly accurate
- Calibrate against human preference on a small held-out subset
- Watch for biases: position effect, length bias, preference for the judge's own style
- Increasingly common but not yet a replacement for humans

---

## LLM Judge Pitfalls

![llm_judge_pitfalls](svg/courses/ai/natural-language-processing/25_nlp_evaluation_methodology/llm_judge_pitfalls.svg)

---

## Human-LLM Hybrid Evaluation

- Use the `LLM` judge as a first-pass filter
- Send borderline cases to humans
- Reduces total human evaluation cost
- Maintains human quality on the hardest cases
- Standard in production evaluation pipelines for chat systems

---

## Counterfactual and Targeted Evaluation

- Build challenge sets that probe specific behaviors
- Counterfactual examples flip a feature and check the model response
- Adversarial sets surface known failure modes
- Distribution-of-success matters as much as average score
- Catches regressions that aggregate metrics miss

---

## Robustness Evaluation

- Test the model on perturbed inputs: typos, paraphrase, code-switching
- Stress tests for length, domain shift, adversarial prompts
- A model that loses 10 points under typos is not production-ready
- Robustness is rarely on the headline scorecard but always matters
- The cheapest improvement comes from training on more diverse data

---

## Calibration Evaluation

- Does the model's confidence match its accuracy
- Reliability diagrams plot predicted probability vs accuracy buckets
- Expected Calibration Error summarizes the gap
- Critical for systems that abstain or escalate to humans
- Modern `LLMs` are often poorly calibrated until reward modeling is applied

---

## Holistic Evaluation Frameworks

- `HELM` evaluates models across many tasks, metrics, and conditions
- Goes beyond accuracy to robustness, calibration, fairness, efficiency
- Encourages a richer model picture than a single benchmark
- Reproducibility built into the design
- The closest thing the field has to a comprehensive `LLM` scorecard

---

## Benchmark Cards

- Document a benchmark's purpose, composition, limitations, license
- Companion to model cards and data sheets
- Helps downstream users pick benchmarks suited to their use
- Catches mismatches between benchmark intent and actual deployment
- Underused but increasingly expected

---

## Reproducibility

- Pin random seeds, document hardware, log software versions
- Release evaluation scripts alongside results
- Use containerized runs for environment determinism
- Re-running a paper's evaluation should be a single command
- The minimum bar for credible numbers in 2026

---

## Cost-Aware Evaluation

- Latency-to-first-token, total time, throughput at peak load
- Cost per query in dollars or tokens
- Memory footprint and quantization quality
- These belong on the same scorecard as accuracy
- A more accurate model at 10x the cost is not a clear win

---

## Common Production Pitfalls

- Evaluating only on the easy splits and ignoring tail behavior
- Reporting a single average across heterogeneous user groups
- Skipping human evaluation because the metric "looks good"
- Comparing systems with different decoding configurations
- Not measuring drift after deployment

---

## Anti-Patterns

- "We hit `97%` on `XYZ` benchmark, ship it"
- Statistical claims without confidence intervals
- Test sets that overlap with training sets via web scrape
- `LLM`-judge results without calibration to humans
- Adding a metric to the dashboard but never acting on it

---

## Summary

- Pick metrics that match the user-visible behavior, not the easiest to compute
- Combine reference-based, reference-free, and learned metrics for a fuller picture
- Statistical significance and human evaluation are not optional
- `LLM`-as-judge accelerates evaluation but needs calibration
- Holistic evaluation across accuracy, safety, calibration, and cost is the bar
