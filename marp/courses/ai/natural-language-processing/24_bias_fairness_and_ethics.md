---
tags:
  - data-and-ai:nlp
  - concepts:ethics
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Bias, Fairness, and Ethics

---

## What This Chapter Covers

- Where bias enters `NLP` systems and what it costs
- The difference between statistical bias and harmful bias
- Measurement frameworks for evaluating model fairness
- Mitigation techniques and their trade-offs
- Privacy, consent, and the data behind models
- The professional responsibility that comes with deploying language technology

---

## Why This Chapter Exists

- `NLP` systems make decisions about people at scale
- Errors are not evenly distributed across users
- "Statistically biased" outputs cause real-world harm
- Engineers carry responsibility for the systems they ship
- This is engineering practice, not philosophy

---

## Sources of Bias

![bias_sources](svg/courses/ai/natural-language-processing/24_bias_fairness_and_ethics/bias_sources.svg)

---

## Data Bias

- Training data reflects who wrote it, who got recorded, and who got labeled
- Web text overrepresents certain demographics, viewpoints, and topics
- Annotation crowds skew toward specific countries and education levels
- Historical data encodes historical inequities
- Anything not in the data effectively does not exist for the model

---

## Representational Harm

- Models that misrepresent or stereotype groups in their outputs
- Word embeddings that associate occupations with genders
- Translation systems that mistranslate gender across language boundaries
- Generated text that reinforces caricatures
- Damaging even when no decision is being made

---

## Allocative Harm

- Models that distribute resources unevenly across groups
- Resume screeners, credit scoring, content moderation thresholds
- Disparate accuracy or false-positive rates by demographic
- The kind of harm regulators actually punish
- Often discovered only after deployment

---

## Two Kinds of Harm

![harm_taxonomy](svg/courses/ai/natural-language-processing/24_bias_fairness_and_ethics/harm_taxonomy.svg)

---

## Measuring Embedding Bias

- `WEAT` (Word Embedding Association Test) measures stereotypical associations
- Compares the average similarity of target words to attribute words
- Originally adapted from psychological implicit association tests
- Strong stereotypes show up clearly in `Word2Vec` and `GloVe`
- Imperfect but reproducible — a starting point, not the whole story

---

## Bias in Contextual Models

- `BERT` and `GPT` show stereotypical completions of fill-in-the-blank tests
- `StereoSet` and `CrowS-Pairs` benchmark stereotype propagation
- Bias varies by language, religion, ability, age, and class
- Pretraining data shapes most of it; fine-tuning amplifies or dampens it
- Measuring is the easy part; deciding what to do about it is hard

---

## Bias in Downstream Tasks

- Sentiment analyzers rate identity-mentioning sentences differently
- Hate speech classifiers disproportionately flag dialect-marked text
- `MT` systems produce gendered output even when input is neutral
- Coreference resolvers fail more on certain names and pronouns
- Each downstream task has its own measurement methodology

---

## Fairness Metrics

- Demographic parity: equal positive rates across groups
- Equal opportunity: equal true positive rates across groups
- Equalized odds: equal TPR and FPR across groups
- Calibration: predicted probabilities match actual outcomes per group
- Different metrics conflict — you cannot satisfy all of them at once

---

## The Impossibility Result

- `Chouldechova` and `Kleinberg` showed core fairness criteria are mutually incompatible
- When base rates differ across groups, you must choose which fairness to satisfy
- This is mathematics, not engineering laziness
- The choice involves stakeholder values, not just optimization
- Document the choice; be explicit about what was traded off

---

## Bias Mitigation: Pre-processing

- Rebalance training data by group
- Remove or rewrite biased text
- Generate counterfactual examples to balance representations
- Cheap to apply but limited in effect
- Often the first lever an engineer reaches for

---

## Bias Mitigation: In-processing

- Add a fairness regularizer to the training loss
- Adversarial debiasing: predict labels while a discriminator cannot predict groups
- Constrained optimization on fairness metrics
- More effective than pre-processing but harder to tune
- Can degrade overall accuracy

---

## Bias Mitigation: Post-processing

- Calibrate or threshold separately per group
- Apply a fairness-preserving wrapper to the model outputs
- Easy to deploy and audit
- Can run afoul of disparate-treatment regulations in some jurisdictions
- Useful when retraining the model is not an option

---

## Mitigation Trade-offs

![mitigation_tradeoffs](svg/courses/ai/natural-language-processing/24_bias_fairness_and_ethics/mitigation_tradeoffs.svg)

---

## Privacy and Memorization

- `LLMs` can memorize and regurgitate training data
- Personal information, copyrighted text, and credentials all leak
- Membership inference and extraction attacks are practical
- Differential privacy reduces but does not eliminate the problem
- Training on user data without consent is increasingly a legal risk

---

## Differential Privacy

- A formal framework for bounding what one record can reveal about itself
- `DP-SGD` adds calibrated noise during training
- Privacy budget tracks how much information has leaked
- Costly: large privacy budgets often hurt accuracy
- The strongest privacy guarantee available, but rarely deployed at scale

---

## Federated and On-Device Learning

- Train on user data without the data leaving the device
- Aggregated updates reach a central server
- Pairs naturally with differential privacy for stronger guarantees
- Latency, battery, and convergence are real constraints
- Used in production by major mobile keyboards and assistants

---

## Toxic Content and Safety

- Pretrained models reproduce the toxic content they trained on
- Refusal training hides but does not erase this capacity
- Red-teaming surfaces failure modes before users do
- Safety measures must keep up with adversarial creativity
- Layered defenses beat any single filter

---

## Misinformation Risks

- Generative models produce plausible falsehoods at scale
- Detection of synthetic text is not reliable
- Watermarking is partial: degrades across paraphrasing
- Content provenance standards (`C2PA`) are starting to emerge
- Engineering controls can slow misuse, not stop it

---

## Consent and Data Provenance

- Most pretraining data was scraped without explicit consent
- Some jurisdictions require opt-in or compensation for content used in training
- Data cards and model cards document what was used and why
- Auditable provenance is becoming a hiring requirement at major labs
- The honor system is no longer enough

---

## Regulatory Landscape

- `EU AI Act` classifies systems by risk and imposes obligations
- `GDPR` constrains what personal data can train a model
- US state laws on automated decision-making (`AEDT`, `Algorithmic Bias Audits`)
- Sector-specific rules: healthcare, finance, hiring, education
- Treat regulation as a moving target you must engineer for

---

## Documentation: Model Cards

- A short document accompanying the model
- Intended use, training data, evaluation results, ethical considerations
- Originally proposed by `Mitchell et al. 2019`
- Standard at major model providers and increasingly required by regulators
- Cheap to write, catches deployment mistakes early

---

## Documentation: Data Sheets

- Companion document for datasets
- Provenance, motivation, composition, collection process, limitations
- `Gebru et al. 2018` introduced the format
- Catches mismatches between dataset intent and downstream use
- Underused but growing in adoption

---

## Auditing in Practice

- Internal: red-team, prompt-injection drills, fairness regression tests
- External: third-party audits with structured methodology
- Continuous: monitor production outputs for drift in fairness metrics
- A single launch audit is not enough — bias re-emerges as data changes
- Audits cost money but cost less than launch incidents

---

## Stakeholder Engagement

- Affected communities should be involved before deployment
- Token consultation late in the cycle does more harm than no consultation
- Pay community partners for their time and expertise
- This is product work, not just ethics work
- The systems that succeed have stakeholder input woven through them

---

## Engineer Responsibility

- You build it, you own the consequences
- "I just trained the model" is not a credible defense
- Push back on launches you cannot defend
- Document the trade-offs so future engineers can revisit them
- Professional codes (`ACM`, `IEEE`) outline the duty of care

---

## Common Production Pitfalls

- Treating fairness as a one-time checklist instead of a property to monitor
- Using off-the-shelf metrics without checking they match the use case
- Ignoring intersectional groups (e.g. older women, not just women or older people)
- Privacy decisions made by engineering with no legal review
- Crisis communication plans for bias incidents that do not exist

---

## Anti-Patterns

- "We removed gendered terms, the model is now fair"
- Demographic parity reported without per-group accuracy
- Auditing English-only when the product ships in 15 languages
- Treating consent as boilerplate rather than a substantive process
- Deploying a model whose training data you cannot trace

---

## Summary

- Bias in `NLP` is structural, not accidental — it lives in data and design
- Statistical bias becomes harm when systems make consequential decisions
- Measurement, mitigation, and monitoring are all needed; none alone suffices
- Privacy and consent are engineering constraints, not soft suggestions
- The systems we ship reflect the choices we make at every stage
