# Phase 1 — Define the modelling experiment

Before training anything, decide exactly what question each model is answering.

You currently have two valid modelling problems:

### Regression

Predict:

> **next-day return**

Target:

```text
target_next_day_return_no_calendar
```

### Classification

Predict:

> **whether the next trading observation is positive or non-positive**

Target:

```text
target_direction_no_calendar
```

I recommend doing **both**, but treat them as separate experiments.

Why? Your EDA suggests next-day returns are centred near zero with high noise, while the directional target is approximately 52.25% positive overall.  They therefore test two different questions:

```text
Regression:
"How much will the asset move?"

Classification:
"Which direction will it move?"
```

---

# Phase 2 — Decide your modelling structure

This is probably your most important design decision.

You should test **two approaches**.

## Experiment A — Per-ticker models

Train separate models for:

```text
GLD
MU
NKE
RPI.L
SNDK
SPY
TLT
```

For example:

```text
SPY data → SPY model
MU data  → MU model
...
```

### Why this matters

Your EDA repeatedly found significant ticker-specific behaviour:

* volatility differs materially between assets 
* risk profiles differ substantially 
* feature distributions differ substantially between assets 
* feature-target effects are often ticker-specific 

So it is entirely plausible that:

```text
MU behaviour ≠ SPY behaviour ≠ GLD behaviour
```

---

## Experiment B — Pooled model

Combine all assets:

```text
GLD
MU
NKE
RPI.L
SNDK
SPY
TLT
        ↓
one model
```

But give the model some representation of ticker identity.

### Why test this?

It gives you substantially more observations.

This is particularly relevant because RPI.L and SNDK have much shorter histories than the other assets. 

The comparison itself becomes an interesting portfolio result:

> Do common cross-asset patterns outperform ticker-specific models?

That is a good data-science question.

---

# Phase 3 — Lock down your feature set

Do **not** throw every generated column into the model.

Your feature analysis already showed redundancy.

For example, daily and log returns have essentially identical rank ordering, while rolling returns and `price_vs_ma20` share considerable information. 

Start with a deliberately compact feature set.

Something approximately like:

### Momentum

* Daily return
* Lag-1 return
* Lag-5 return
* 7-observation return
* 30-observation return

### Trend

* Price vs MA20
* MA20
* MA50

### Risk

* Rolling 30-day volatility
* Drawdown

### Activity

* Relative volume

Then later compare:

```text
all features
vs
reduced feature set
```

Do not perform aggressive feature selection before you have a baseline.

---

# Phase 4 — Perform a leakage audit

This is mandatory.

For every input feature ask:

> **Would I actually know this value at the moment I make the prediction?**

Your EDA already recognised that the features are only leakage-free if the prediction is made **after market close and before the next trading day**. 

Define your prediction point explicitly:

> At the close of trading day (t), use information available through day (t) to predict return/direction for trading day (t+1).

Then verify:

* no future price appears in X
* target columns never appear in X
* scalers never see future data
* feature selection never sees test data
* model tuning never sees final test data

---

# Phase 5 — Define chronological train / validation / test sets

This is one of the most important skills this project can teach you.

### Do not randomly split the data.

Your data is time series.

Instead:

```text
PAST                                        FUTURE
──────────────────────────────────────────────────>

TRAIN                  VALIDATION          TEST
████████████████████    █████████          ███████
```

A reasonable conceptual starting point might be:

```text
Training:     earliest 70%
Validation:   next 15%
Test:         final 15%
```

The exact percentages aren't important yet.

The important requirement is:

> **The test period must always occur after the training period.**

---

# Phase 6 — Establish baselines BEFORE ML

This is essential because your EDA shows weak predictive signal. 

You need to prove that an ML model actually improves on something trivial.

## Regression baselines

Compare models against:

### Baseline 1

Always predict:

```text
0% return
```

Very important because daily returns are generally near zero. 

### Baseline 2

Predict:

```text
training-period mean return
```

### Optional Baseline 3

Predict a rolling historical average.

---

# Classification baselines

Your overall positive class rate is roughly:

```text
52.25%
```



Therefore an extremely stupid model that says:

```text
"UP"
```

every day already achieves roughly:

```text
52.25% accuracy
```

So if your ML model achieves:

```text
52.4%
```

that is not impressive.

Your baseline should therefore include:

### Majority-class classifier

And importantly:

### Per-ticker majority baseline

because individual ticker class balances differ.

---

# Phase 7 — Preprocessing

Do this **after splitting**.

Your feature analysis showed significant differences in feature magnitude, skewness and outlier behaviour. 

You should experiment with:

### No scaling

Useful for tree-based models.

### Standardisation

Useful for:

* Logistic Regression
* Linear Regression
* regularised models

### Possibly robust scaling later

Useful because your data contains:

* fat tails
* outliers
* extreme ticker-specific observations

But don't start with complex transformations.

Most importantly:

> Fit the scaler using **training data only**.

Never calculate scaling parameters from the full dataset.

---

# Phase 8 — Build simple models first

Don't jump straight to XGBoost or neural networks.

## Regression progression

### Model 0

Zero-return baseline

### Model 1

Linear Regression

Purpose:

> Can simple linear relationships explain anything?

### Model 2

Regularised linear regression

For example conceptually:

```text
Ridge
```

Useful because your EDA found feature correlation/redundancy.

### Model 3

Random Forest

Purpose:

> Are there nonlinear interactions between features?

Later you can consider gradient boosting.

---

# Classification progression

### Model 0

Majority-class baseline

### Model 1

Logistic Regression

This should be your primary interpretable baseline.

### Model 2

Random Forest Classifier

Tests nonlinear relationships.

### Model 3

Gradient boosting

Only after the earlier models are working properly.

---

# Phase 9 — Choose evaluation metrics

Do not optimise only one metric.

## Regression

Use at least:

* **MAE**
* **RMSE**

MAE is especially important because your data contains extreme returns.

Your EDA explicitly identified heavy tails and very large movements in RPI.L, SNDK and MU. 

RMSE will heavily penalise these extreme misses.

That comparison itself will tell you something.

---

## Classification

Use:

* Accuracy
* Precision
* Recall
* F1
* Confusion matrix

And always compare against:

```text
majority baseline
```

---

# Phase 10 — Evaluate by ticker

Even for your pooled model, do not report just:

```text
Model accuracy = 54%
```

Break it down:

| Ticker | Baseline | Model | Improvement |
| ------ | -------: | ----: | ----------: |
| SPY    |      ... |   ... |         ... |
| GLD    |      ... |   ... |         ... |
| MU     |      ... |   ... |         ... |
| NKE    |      ... |   ... |         ... |
| RPI.L  |      ... |   ... |         ... |
| SNDK   |      ... |   ... |         ... |
| TLT    |      ... |   ... |         ... |

This matters because your feature-target EDA found the strongest relationships were frequently **ticker-specific** rather than universal. 

---

# Phase 11 — Add walk-forward validation

Once the first models work, upgrade your evaluation.

Instead of testing once:

```text
Train → Test
```

do:

```text
Train ────────→ Validate
Train ───────────────→ Validate
Train ─────────────────────→ Validate
```

This is usually called:

> **walk-forward / expanding-window validation**

It is much closer to how financial modelling is evaluated in practice.

It tests:

> Does the model work across different market periods?

That is particularly relevant because your EDA found clear regime changes in volatility and correlations.  

---

# Phase 12 — Analyse model behaviour

After model performance, don't immediately move to trading strategies.

Perform **model analysis**.

You want to understand:

* which features matter
* whether importance changes by ticker
* whether predictions degrade over time
* which market regimes cause failures
* whether high-volatility periods reduce accuracy
* whether models perform differently on positive vs negative days
* whether RPI.L/SNDK results are unstable because of limited observations

This turns:

> “I trained Random Forest.”

into:

> “I investigated when and why the model worked.”

Much stronger portfolio work.

---

# Phase 13 — Only then: backtesting

Once you've built a genuinely out-of-sample model:

```text
features
    ↓
prediction
    ↓
signal
    ↓
strategy
```

For example:

```text
Predicted positive return
        ↓
Long asset

Predicted negative return
        ↓
Cash
```

Then compare against:

```text
Buy and hold
```

Eventually include:

* transaction costs
* Sharpe ratio
* volatility
* cumulative return
* maximum drawdown
* turnover

But **do not start this yet**.

You first need trustworthy model predictions.

---

# Your immediate modelling checklist

I would now create something like:

```text
10 - Modelling Preparation.ipynb
11 - Regression Modelling.ipynb
12 - Classification Modelling.ipynb
13 - Model Evaluation.ipynb
```

And proceed in this order:

* [ ] Define prediction timing
* [ ] Define regression and classification experiments
* [ ] Select initial feature set
* [ ] Audit leakage
* [ ] Define chronological train/validation/test splits
* [ ] Calculate regression baselines
* [ ] Calculate classification baselines
* [ ] Build Linear Regression
* [ ] Build Logistic Regression
* [ ] Evaluate against baselines
* [ ] Add Random Forest regression/classification
* [ ] Compare models
* [ ] Evaluate each ticker separately
* [ ] Compare pooled vs ticker-specific models
* [ ] Add walk-forward validation
* [ ] Analyse feature importance/model behaviour
* [ ] Select final candidate model
* [ ] Generate strictly out-of-sample predictions
* [ ] Move into strategy/backtesting

## The key mindset for this stage

Given your EDA, I would **not expect a spectacular predictive model**.

Your feature-target analysis already suggests the signal is weak. 

That is actually useful for the portfolio.

A credible project where you conclude:

> “Most models failed to materially outperform appropriate time-series baselines, and the apparent signals were unstable across assets and periods.”

can demonstrate **far more data-science maturity** than claiming that a Random Forest achieved 85% stock-market prediction accuracy.

The objective now is therefore not to manufacture impressive performance. It is to determine, rigorously, **whether the features contain reproducible out-of-sample information at all**.
