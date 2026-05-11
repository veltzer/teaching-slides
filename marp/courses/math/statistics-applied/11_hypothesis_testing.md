---
tags:
  - math:hypothesis-testing
level: beginner
category: math
audience:
  - audiences:data-analysts
  - audiences:developers

---
# Hypothesis Testing

---
## What This Chapter Covers

- The null and alternative hypotheses
- Test statistics and p-values
- What "statistically significant" does and doesn't mean
- Type I and Type II errors, and power
- One-sided vs two-sided tests
- The relationship between tests and confidence intervals

---
## Null Distribution and Rejection Regions

![null_and_rejection](svg/courses/math/statistics-applied/11_hypothesis_testing/null_and_rejection.svg)

---
## The Core Idea

- You have a claim ("the new design changed conversion") and noisy data
- Hypothesis testing asks: *could this result plausibly be just noise?*
- If "just noise" is implausible, you have evidence for a real effect
- If not, you can't distinguish the result from chance — that's all
- It never *proves* anything; it controls how often you cry wolf

---
## Null And Alternative

- **Null hypothesis (H&#8320;)**: the boring default — no effect, no difference
- **Alternative (H&#8321;)**: what you're actually interested in — there *is* an effect
- You assume H&#8320; is true, then see how strange your data would be under it
- "Strange enough" &#8594; reject H&#8320;. Not strange &#8594; fail to reject (not "accept")
- The asymmetry is deliberate: the burden of proof is on the effect

---
## Test Statistic And p-Value

- A **test statistic** condenses the data into one number measuring "distance from H&#8320;" (a t, z, F, or &chi;&sup2; value)
- The **p-value** is P(a result this extreme or more | H&#8320; is true)
- Small p &#8594; this data would be surprising under H&#8320; &#8594; evidence against H&#8320;
- Large p &#8594; consistent with H&#8320; &#8594; you simply can't tell
- p &lt; 0.05 is the customary threshold (&alpha;) — convention, not magic

---
## What Significance Does Not Mean

- "Statistically significant" &#8800; "large", "important", or "real-world meaningful"
- A trivial effect becomes "significant" with a big enough sample
- A real, big effect can be "not significant" with too small a sample
- p is *not* the probability that H&#8320; is true
- Always report the **effect size** alongside the p-value — the size is the point

---
## Two Kinds Of Error

- **Type I error** (false positive): reject H&#8320; when it's true — probability &alpha;, you set it (usually 0.05)
- **Type II error** (false negative): fail to reject H&#8320; when it's false — probability &beta;
- **Power** = 1 &minus; &beta;: the chance of detecting a real effect of a given size
- Bigger samples and bigger true effects &#8594; more power
- Underpowered studies waste effort and litter the literature with false negatives

---
## Type I and Type II Errors

![error_types](svg/courses/math/statistics-applied/11_hypothesis_testing/error_types.svg)

---
## One-Sided vs Two-Sided

- **Two-sided**: "is it different?" — splits &alpha; across both tails (the safe default)
- **One-sided**: "is it bigger?" — puts all of &alpha; in one tail, more power *in that direction*
- Only go one-sided if a difference the other way is genuinely irrelevant or impossible
- Choosing one-sided *after* seeing the data is a form of cheating
- When unsure, use two-sided

---
## Tests And Confidence Intervals Agree

- A two-sided test at level &alpha; rejects H&#8320;: "mean = m&#8320;" exactly when m&#8320; falls outside the (1&minus;&alpha;) confidence interval
- So a CI tells you the test result *and* the plausible range — strictly more information
- "0 is not in the 95% CI for the difference" &#8801; "significant at 0.05, two-sided"
- Prefer reporting the interval; it answers more questions
- This is why many statisticians push CIs over bare p-values

---
## A Hypothesis Test In Python

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(1)
sample = rng.normal(102, 15, size=40)            # is the mean different from 100?
t, p = stats.ttest_1samp(sample, popmean=100)
print(f"t = {t:.2f}, p = {p:.3f}")
lo, hi = stats.t.interval(0.95, len(sample)-1,
                          loc=sample.mean(), scale=stats.sem(sample))
print(f"95% CI for the mean: [{lo:.1f}, {hi:.1f}]")
```

---
## Common Mistakes

- Reading "p &lt; 0.05" as proof, or as "95% sure there's an effect"
- Reporting significance with no effect size
- Running an underpowered test and treating "not significant" as "no effect"
- Switching to a one-sided test after peeking at the data
- Testing many hypotheses and reporting only the ones that came out small
