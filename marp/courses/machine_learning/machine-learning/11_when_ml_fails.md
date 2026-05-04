---
tags:
  - data-and-ai:machine-learning
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---
# When ML Fails

---
## What This Chapter Covers

- Why some problems are not ML problems
- Data limits
- Causal limits
- Distribution shift
- Bias and fairness
- Interpretability requirements
- Edge cases
- Ethics and law

---
## ML Is Not Magic

- Pattern matcher, not oracle
- Learns what's in the data
- Can't go beyond it
- Bad fits exist

---
## The Big Question

- Can this problem be learned at all
- Is the right data available
- Is the cost of error acceptable
- Is the deployed system safe

---
## When To Walk Away

- You can solve it with rules
- The cost of mistakes is catastrophic
- Data is too sparse, biased, or wrong
- The world the model sees changes constantly

---
## No Signal In The Data

- Predict tomorrow's lottery numbers
- The features have nothing to do with the target
- More data won't help
- Stop trying

---
## Too Few Examples

- Predict rare cancers from few cases
- Learning needs enough examples
- Few-shot helps a bit, not enough
- Augment with priors or stop

---
## Long Tail

- Most cases handled, rare ones missed
- Rare cases sometimes the most important
- Retraining doesn't fix what isn't sampled
- Hybrid system with rules

---
## The Quality Of Labels

- Supervised needs labels
- Wrong labels = wrong model
- Inter-annotator disagreement = upper bound
- Improve labels before model

---
## Subjective Labels

- "Is this art good"
- No ground truth
- Whose opinion
- Build a critic, not a truth machine

---
## The Right Target

- Are we predicting what matters
- Or a proxy that misleads
- Click vs purchase, watch vs satisfaction
- Misalignment causes harm

---
## Goodhart's Law

- "When a measure becomes a target, it ceases to be a good measure"
- Optimising the metric breaks the system
- Engagement metrics, news feeds
- Beware your loss function

---
## Causality vs Correlation

- ML learns correlations
- Acting on a correlation can break the correlation
- Causal inference is a different field
- Counterfactuals matter

---
## Ice Cream And Drowning

- Both go up in summer
- Selling ice cream doesn't drown people
- Confounding variable: heat
- Model would see correlation, recommend nothing

---
## Spurious Patterns

- Anything is correlated with enough data
- Multiple comparisons inflate "findings"
- Holdout test, large effect, replicate
- Don't believe your first model

---
## Interventions

- Predicting and acting are different
- Predicting churn vs preventing it
- Need causal estimates for action
- Uplift modelling exists for this

---
## Distribution Shift

- World changes, model doesn't
- Performance decays
- Need monitoring and retraining
- Sometimes problem isn't learnable in production

---
## Covariate Shift

- Input distribution changes
- Same labels, different inputs
- Recalibrate or retrain

---
## Concept Drift

- Relationship between input and output changes
- Same inputs, different correct outputs
- Big retraining problem
- Sometimes signals abandon ML

---
## Selection Bias

- Training data not representative
- Loan approval based on past loans
- Already-rejected applicants invisible
- Model perpetuates the bias

---
## Survivorship Bias

- Only successes are visible
- Failures filtered out
- Predictions optimistic
- WW2 plane armour example

---
## Bias In Labels

- Annotators bring their views
- Historical data carries past discrimination
- Model amplifies it
- Audit before training

---
## Demographic Bias

- Underrepresented groups perform worse
- Compounding harm
- Slice metrics by group
- Address before deploying

---
## Fairness Definitions

- Demographic parity
- Equalised odds
- Predictive parity
- Multiple definitions, often incompatible

---
## Fairness vs Accuracy

- Often a tradeoff
- Fairness has many definitions
- Pick by stakes and context
- Not a technical fix alone

---
## Self-Fulfilling Predictions

- Predict crime hotspot, send police, find more crime
- Predict failure, give less help, see failure
- Prediction changes outcome
- Need to break the loop

---
## Adversaries

- People game the system
- Spammers, fraudsters, gamers
- Static models lose
- Robustness and updates required

---
## Adversarial Examples

- Tiny pixel changes flip predictions
- Vision and NLP affected
- Big problem in safety-critical
- Active research

---
## Privacy Limits

- Some data can't be used
- GDPR, HIPAA, sectoral law
- Differential privacy techniques
- Sometimes ML is illegal

---
## Right To Explanation

- EU GDPR
- Black-box models problematic
- Interpretable models or post-hoc explanations
- Sometimes simpler is mandated

---
## Interpretability Required

- Medical decisions
- Lending decisions
- Court decisions
- Pick interpretable algorithms

---
## Interpretable Models

- Linear regression
- Decision trees (small)
- GAMs
- Rule lists

---
## Post-Hoc Explanations

- SHAP, LIME
- Approximate explanations
- May not match the model
- Better than nothing, less than transparent

---
## Safety-Critical Systems

- Self-driving, medical devices, aviation
- Must verify behaviour
- Long tail of edge cases
- ML alone insufficient

---
## The Long Tail Problem

- 90% of cases are easy
- 9% are tricky
- 1% are catastrophic if wrong
- Models often fail on the 1%

---
## Lack Of Generalisation

- Models trained on one domain fail elsewhere
- Hospital A vs hospital B
- Camera A vs camera B
- Test in target environment

---
## Scale Of Errors

- Some errors are local
- Some errors propagate
- Recommender mistake = boredom
- Medical mistake = harm

---
## Cost Asymmetry

- False positive vs false negative
- Cancer screening vs spam
- Match loss to cost
- One number won't capture it

---
## Trust And Adoption

- Users may not trust the model
- Or trust it too much
- Behaviour change required
- Tech is the easy part

---
## Bad Process Wrapping

- ML on top of broken process
- Garbage in, garbage out
- Fix the process first
- Sometimes ML hides the rot

---
## Ethics

- Just because we can, should we
- Surveillance systems
- Manipulation systems
- Build with intent

---
## Dual Use

- Same model, different uses
- Face recognition: tagging vs profiling
- Plan for misuse
- Limit by access and context

---
## Environmental Cost

- Training big models is energy intensive
- Carbon footprint
- Worth it
- Smaller models often suffice

---
## When ML Is Wrong Tool

- Stable problem with known logic → rules
- Tiny data → expert judgement
- High-stakes black-box prohibited → interpretable model
- Causal action → causal methods

---
## Hybrid Systems

- ML scores, humans decide
- ML triages, rules enforce
- Humans on the edge cases
- Often the right answer

---
## Failure Modes Checklist

- Wrong target
- Wrong data
- Wrong labels
- Wrong distribution at deployment
- Wrong cost function

---
## Red Flags

- "We'll just add more data"
- "The model will learn it"
- "We'll figure out the metric later"
- "We'll fix bias in v2"

---
## When To Stop

- Repeated failures with more data
- Performance plateau
- Unfair across groups
- Doesn't ship safely

---
## Recovering From Bad ML

- Fall back to rules
- Add humans in the loop
- Reduce scope
- Sometimes withdraw the system

---
## Better Questions

- What are we trying to do
- Who pays the cost of mistakes
- Can we measure success honestly
- Is there a simpler way

---
## Common Mistakes

- Treating ML as default
- Ignoring causality
- No subgroup analysis
- Black-box in regulated setting

---
## Goodhart's Law

![goodharts_law](svg/courses/machine_learning/machine-learning/11_when_ml_fails/goodharts_law.svg)

---
## Distribution Shift

![distribution_shift](svg/courses/machine_learning/machine-learning/11_when_ml_fails/distribution_shift.svg)

---
## Causal vs Predictive

![causal_vs_predictive](svg/courses/machine_learning/machine-learning/11_when_ml_fails/causal_vs_predictive.svg)

---
## Long Tail

![long_tail](svg/courses/machine_learning/machine-learning/11_when_ml_fails/long_tail.svg)

---
## Fairness Tradeoff

![fairness_tradeoff](svg/courses/machine_learning/machine-learning/11_when_ml_fails/fairness_tradeoff.svg)

---
## Summary

- ML is a tool, not the answer
- Some problems lack signal
- Some are causal, not predictive
- Some need transparency
- Choose ML carefully
