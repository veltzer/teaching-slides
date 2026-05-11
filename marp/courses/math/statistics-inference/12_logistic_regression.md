---
tags:
  - math:regression
level: intermediate
category: math
audience:
  - audiences:data-analysts
  - audiences:data-scientists

---
# Logistic Regression

---
## What This Chapter Covers

- Why linear regression fails for a yes/no outcome
- The logit link and the logistic curve
- Odds, log-odds, and odds ratios
- Fitting by maximum likelihood; deviance
- Inference on coefficients
- Using the model for classification, and where it sits among GLMs

---
## The Logistic (Sigmoid) Curve

![sigmoid](svg/courses/math/statistics-inference/12_logistic_regression/sigmoid.svg)

---
## A Binary Outcome Breaks The Line

- The response is 0/1: converted or not, churned or not, defective or not
- A straight line predicts values below 0 and above 1 — nonsense as probabilities — and the equal-variance assumption is automatically violated
- We want to model **P(y = 1 | x)**, which must stay in [0, 1]
- Solution: model a *transform* of the probability that *can* range over the whole real line
- That transform is the **logit** — and the model is logistic regression

---
## The Logit Link And The S-Curve

- Define **odds** = p / (1 &minus; p), and **logit(p) = log(odds)** — maps (0, 1) to (&minus;&infin;, +&infin;)
- Logistic regression fits: logit(P(y=1|x)) = &beta;&#8320; + &beta;&#8321;x&#8321; + ... + &beta;&#8345;x&#8345; — linear *on the log-odds scale*
- Inverting the logit gives the **logistic (sigmoid) function**: P = 1 / (1 + e^&minus;(&beta;&#8320; + ...)) — the familiar S-shaped curve, squashed into [0, 1]
- It's a **generalized linear model (GLM)**: a linear predictor, a link function, and a non-normal response distribution (here, Bernoulli)
- Same idea generalizes — Poisson regression for counts, etc. — same fitting machinery

---
## Odds, Log-Odds, And Odds Ratios

- Coefficients live on the **log-odds** scale: &beta;&#8332; = the change in log-odds of y=1 per one-unit increase in x&#8332;, holding the rest fixed
- **Exponentiate** to get an **odds ratio**: e^&beta;&#8332; = the multiplicative change in the odds per unit of x&#8332; — far more interpretable
- OR = 1: no effect. OR = 1.5: each unit multiplies the odds by 1.5. OR = 0.7: each unit cuts the odds by 30%
- An odds ratio is **not** a risk (probability) ratio — they coincide only when the outcome is rare; don't say "1.5&times; as likely" when you mean "1.5&times; the odds"
- For a categorical predictor, e^&beta; is the odds ratio for that level versus the baseline

---
## Odds Ratios on a Forest Plot

![odds_ratio_forest](svg/courses/math/statistics-inference/12_logistic_regression/odds_ratio_forest.svg)

---
## Fitting And Deviance

- No closed form — fit by **maximum likelihood**, maximizing the (log-)likelihood of the observed 0s and 1s, solved iteratively (IRLS / Newton steps)
- Goodness of fit is summarized by the **deviance** (= &minus;2 &times; log-likelihood) — the GLM analog of the residual sum of squares; lower is better
- Compare nested models with the **likelihood-ratio test**: the drop in deviance is chi-square distributed with df = (number of extra parameters)
- **AIC/BIC** (deviance plus a complexity penalty) compare non-nested models — lower is better
- Watch for **complete separation** (a predictor perfectly splits the classes): the MLE runs off to infinity, coefficients and SEs explode — the fitter will usually warn you

---
## Inference On Coefficients

- Each &beta;&#8332; has a standard error; the **Wald test** (z = &beta;&#8332; / SE) tests H&#8320;: &beta;&#8332; = 0, i.e. OR = 1
- The likelihood-ratio test is more reliable than the Wald test for small samples or near-separation — prefer it when they disagree
- Confidence intervals: build on the log-odds scale, then exponentiate the endpoints to get a CI for the **odds ratio** (it'll be asymmetric — that's correct)
- "OR = 1.42, 95% CI [1.10, 1.83]" is the headline; the p-value is secondary
- Same modeling discipline as linear regression: watch multicollinearity (VIFs still apply), don't run stepwise then trust the p-values, validate out of sample

---
## From Probabilities To Decisions

- The model outputs a **probability** for each case; turning it into a 0/1 prediction needs a **threshold** (0.5 is a default, rarely the right one)
- Choose the threshold from the costs of the two error types — a cheap follow-up favors a low threshold; an expensive intervention favors a high one
- Threshold-free evaluation: the **ROC curve** and its area (AUC) summarize ranking quality across all thresholds; **precision&ndash;recall** curves are better when the positive class is rare
- Check **calibration** too: among cases predicted ~30%, do about 30% actually occur? A model can rank well yet be poorly calibrated
- Logistic regression is a solid, interpretable baseline classifier — and the building block for much of applied ML

---
## Logistic Regression In Python

```python
import numpy as np, pandas as pd
import statsmodels.formula.api as smf
rng = np.random.default_rng(10)
n = 500
df = pd.DataFrame({"tenure": rng.normal(12, 5, n), "plan_pro": rng.integers(0, 2, n)})
logit = -2 + 0.15*df.tenure + 0.8*df.plan_pro
df["churn"] = rng.binomial(1, 1/(1+np.exp(-(-logit))))   # note: higher logit -> less churn here
fit = smf.logit("churn ~ tenure + plan_pro", df).fit(disp=0)
print(fit.summary().tables[1])
print("odds ratios:\n", np.exp(fit.params).round(3))
print("odds-ratio 95% CI:\n", np.exp(fit.conf_int()).round(3))
```

---
## Common Mistakes

- Using linear regression for a 0/1 outcome
- Reading an odds ratio as a probability ("risk") ratio when the outcome isn't rare
- Trusting Wald p-values under (near-)complete separation instead of a likelihood-ratio test
- Treating the 0.5 cutoff as sacred instead of choosing the threshold from error costs
- Reporting accuracy on imbalanced data and ignoring AUC, precision/recall, and calibration
