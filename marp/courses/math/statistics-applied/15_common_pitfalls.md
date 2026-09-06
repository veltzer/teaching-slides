---
tags:
  - math:statistics
level: beginner
category: math
audience:
  - audiences:data-analysts
  - audiences:developers

---

# Common Pitfalls and How to Avoid Them

---

## What This Chapter Covers

- p-hacking and the garden of forking paths
- Multiple comparisons
- Simpson's paradox
- Survivorship and selection bias
- Regression to the mean
- Goodhart's law and a short defensive checklist

---

## Simpson's Paradox

![simpsons_paradox](svg/courses/math/statistics-applied/15_common_pitfalls/simpsons_paradox.svg)

---

## Why A Whole Chapter On Mistakes

- Most bad analyses aren't from bad arithmetic — the formulas were fine
- They're from asking the data the wrong question, or too many questions
- These traps are *systematic*: smart, honest people fall in them constantly
- Knowing their names is half the defense — you spot them in your own work
- The other half is a few habits, listed at the end

---

## p-Hacking And Forking Paths

- Test 20 things at &alpha; = 0.05 and ~1 comes up "significant" by pure chance
- p-hacking: trying many analyses and reporting only the one that "worked"
- The subtler version — the *garden of forking paths*: you'd have analyzed it differently had the data looked different, so every result is implicitly cherry-picked
- Defense: pre-register the question and the analysis; treat post-hoc findings as hypotheses to be tested on *new* data, not conclusions
- "We found something interesting after slicing it 12 ways" is a hypothesis, not a result

---

## Multiple Comparisons

- Every extra test is another lottery ticket for a false positive
- Subgroups, metrics, time windows, model variants — they all count
- Corrections: Bonferroni (divide &alpha; by the number of tests — strict), Holm (less strict), or control the false discovery rate (Benjamini&ndash;Hochberg — good for many tests)
- Or sidestep it: decide on one primary comparison up front
- Reporting the smallest p out of many without saying how many you ran is misleading

---

## Simpson's Paradox

- A trend that holds in every subgroup can *reverse* when the groups are pooled — and vice versa
- Classic case: a treatment looks worse overall but is better for both mild and severe cases, because it was given more often to severe cases
- Caused by a lurking variable correlated with both group and outcome (a *confounder*)
- Always ask: "is there a variable that differs between my groups and also affects the outcome?"
- Slice by the confounder, or use a model that adjusts for it

---

## Survivorship And Selection Bias

- **Survivorship bias**: you only see the units that made it — surviving funds, returned WWII bombers, companies still in business
- Reinforcing the planes where they came back, not where the lost ones were hit
- **Selection bias** more broadly: the data you have isn't a fair sample of the data you care about
- "Our happiest customers love us" — you didn't survey the ones who churned
- Ask "who or what is *missing* from this dataset, and why?" before drawing conclusions

---

## Regression To The Mean

- Extreme measurements tend to be followed by less extreme ones — partly real, partly luck running out
- The worst-performing stores "improve" after intervention even if the intervention did nothing
- Picking units *because* they were extreme guarantees they'll drift back — that drift is not your effect
- This is exactly why you need a randomized control group, not a before/after on the extremes
- Any "we targeted the worst and they got better" claim should set off alarms

---

## Goodhart's Law

- "When a measure becomes a target, it ceases to be a good measure"
- Optimize the proxy and people game the proxy — support tickets "resolved" fast but not solved
- The metric and the thing you actually want quietly drift apart
- Defense: track guardrail metrics, rotate or audit metrics, prefer outcomes over proxies
- A KPI is a thermometer; don't warm it with a lighter and call yourself healthy

---

## Five Named Traps

![pitfalls_checklist](svg/courses/math/statistics-applied/15_common_pitfalls/pitfalls_checklist.svg)

---

## A Defensive Checklist

- Plot the raw data before you summarize or test it
- Write down the question and the analysis *before* looking at results
- Count your comparisons; correct, or pre-pick one
- Ask what's missing from the data and what confounders lurk between groups
- Report effect sizes and intervals, not bare p-values — and when you're unsure, say so

---

## Common Mistakes

- Hunting through subgroups and reporting only the "significant" one
- Forgetting that every extra metric or slice is another false-positive chance
- Comparing pooled groups without checking for a confounder (Simpson's paradox)
- Drawing conclusions from a dataset that systematically excludes the failures
- Crediting an intervention for what was just regression to the mean
