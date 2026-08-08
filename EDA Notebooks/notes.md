You were right to challenge the earlier outline. After reviewing the notebooks, this section should be much narrower and should **only cover relationships between predictors and future targets**.

A suitable title would be:

# 09 — Feature–Target Relationship Analysis

## What should not be repeated

| Existing notebook             | Already covered                                                                                                                                                                | Exclude from this section                                                                 |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| **02 — Data Quality Checks**  | Missingness, duplicates, invalid values, target nulls and sufficient history                                                                                                   | General data-quality checks and another full leakage-validation section                   |
| **03 — Price Behaviour**      | Price trends, normalised prices, major movements and later-IPO distortions                                                                                                     | Price charts and general trend interpretation                                             |
| **04 — Return Analysis**      | Daily-return plots, return distributions, volatility, extreme days, skewness and kurtosis                                                                                      | General return histograms, outlier analysis and risk–return comparisons                   |
| **05 — Risk Analysis**        | Rolling volatility over time, volatility clustering, drawdown depth and recovery                                                                                               | Volatility time-series, stress-period analysis and drawdown investigation                 |
| **06 — Correlation Analysis** | Correlations **between assets**, common-period matrices and stress-period correlations                                                                                         | Asset-to-asset correlation matrices and another market-regime analysis                    |
| **07 — Feature Analysis**     | Feature validation, moving averages, relative volume, lagged-return correlations and quantile tests, rolling returns, feature distributions and feature-to-feature correlation | Lag-return quantile plots, general feature boxplots/ECDFs and multicollinearity heatmaps  |
| **08 — Target Analysis**      | Target-return distributions, target logic, zero returns, class balance, up/down percentages and target noise                                                                   | Target histograms, class-balance tables and target-by-ticker distribution summaries       |

The largest duplication in your original plan is **lagged-return predictive analysis**. Notebook 07 already calculates Spearman correlations between lagged returns and next-day returns and plots next-day returns by lag quantile. That analysis should not be recreated. 

---

# Revised outline

## 1. Purpose and analysis scope

Briefly state that the section asks:

> Do the validated engineered features contain measurable relationships with next-day return or next-day direction?

Specify that:

* Relationships are calculated separately by ticker.
* Full-history and common-period results are compared.
* This is association analysis, not proof of out-of-sample predictability.
* Existing feature, return and target distributions are not repeated.

No table or graph is needed here.

---

## 2. Feature relationships with `target_next_day_return`

### Analysis

Calculate, by ticker:

* Pearson correlation
* Spearman correlation
* Number of valid observations

Use the complete intended modelling feature set. However:

* Do not pool raw moving-average values across tickers.
* Treat daily and log returns as redundant if both remain in the dataset.
* Keep lagged returns in the overall comparison matrix, but do not repeat their dedicated quantile analysis.

### Figure 1 — Feature–return correlation heatmaps

Create one figure with two panels:

1. Pearson correlation by feature and ticker
2. Spearman correlation by feature and ticker

Use the same symmetric colour limits for both panels.

This is different from Notebook 06 because that notebook examines **ticker-to-ticker relationships**, whereas this figure examines **feature-to-future-target relationships**.

### Table 1 — Ranked feature–return relationship summary

One row per feature:

| Column                               | Purpose                                    |
| ------------------------------------ | ------------------------------------------ |
| Median absolute Pearson correlation  | Typical linear relationship across tickers |
| Median absolute Spearman correlation | Typical monotonic relationship             |
| Maximum absolute correlation         | Largest individual result                  |
| Ticker of maximum                    | Identifies ticker-specific effects         |
| Positive correlations                | Sign consistency                           |
| Negative correlations                | Sign consistency                           |
| Valid ticker count                   | Reliability check                          |

Sort using median absolute Spearman or Pearson correlation.

Do not create separate detailed sections for lagged returns, volatility or momentum. They are simply rows in this comparison.

---

## 3. Feature relationships with `target_direction`

Raw mean differences cannot be compared directly across moving averages, returns, volume and volatility. Use a standardised measure.

### Analysis

For each feature and ticker, calculate:

* Mean before up days
* Mean before non-positive days
* Difference in means
* Median before up days
* Median before non-positive days
* Difference in medians
* Standardised mean difference
* Up and non-positive observation counts

Here, a positive standardised difference means the feature tends to be higher before up days.

### Figure 2 — Directional-separation heatmap

Plot:

* Rows: features
* Columns: tickers
* Values: standardised mean difference

This directly shows:

* Strength of separation
* Direction of separation
* Whether the result is consistent across tickers

### Table 2 — Ranked directional-separation summary

One row per feature:

| Column                                  | Purpose                          |
| --------------------------------------- | -------------------------------- |
| Median absolute standardised difference | Typical class separation         |
| Median signed difference                | Typical direction                |
| Maximum absolute difference             | Strongest ticker-specific result |
| Ticker of maximum                       | Identifies where it occurs       |
| Consistent-sign tickers                 | Cross-ticker consistency         |
| Minimum class count                     | Detects weak samples             |

Keep the complete up/down statistics in a long-form DataFrame, but display detailed values only for the highest-ranked features.

---

## 4. Visual confirmation of class overlap

Notebook 07 already plots the **overall distributions** of features. Do not reproduce those plots. 

The only genuinely new distribution plots here are distributions split by the future target class.

### Figure 3 — Up versus non-positive distributions

Select only the **three highest-ranked features from Table 2**.

For each selected feature:

* x-axis: ticker
* y-axis: feature value
* grouping: up versus non-positive next day
* use paired boxplots or violin plots
* hide or clip extreme display values for readability

Do not automatically plot:

* `lag_1_return`
* volatility
* `price_vs_ma20`
* relative volume

Instead, let the numerical ranking determine which features deserve visual inspection. This prevents the section from becoming a repeated feature-family analysis.

The purpose is only to verify whether:

* The class distributions are visibly shifted
* A mean difference is driven by outliers
* The two classes overlap heavily

---

## 5. Full-history versus common-period robustness

Later IPO assets are already recognised as having shorter and less stable histories throughout the existing notebooks. The common-period method has also been used for asset correlations. 

Applying it to **feature–target relationships**, however, is new.

### Table 3 — Robustness comparison

For only the top five features from the earlier results, show:

| Feature   | Full-period relationship | Common-period relationship | Rank change | Sign changed? | Interpretation   |
| --------- | -----------------------: | -------------------------: | ----------: | ------------- | ---------------- |
| Feature A |                        … |                          … |           … | No            | Stable           |
| Feature B |                        … |                          … |           … | Yes           | Regime-sensitive |

Compare:

* Median absolute Spearman correlation with return
* Median absolute standardised difference for direction

Do not reproduce every heatmap twice. A compact comparison table is sufficient.

---

## 6. Suspicious-correlation check

Do not repeat all the feature-construction and target-alignment tests from Data Quality and Feature Analysis.

Instead, add an automatic flag to the result table:

* `Review` where absolute correlation is unusually high
* Inspect only flagged features
* Check timing, shifting and rolling-window construction

This is a safeguard rather than a new analytical section.

---

## 7. Final findings table

Finish with one concise table:

| Feature                  | Next-day return relationship | Direction separation | Cross-ticker consistency | Common-period stability | Overall assessment       |
| ------------------------ | ---------------------------- | -------------------- | ------------------------ | ----------------------- | ------------------------ |
| `lag_1_return`           | Weak                         | Minimal              | Low                      | Stable                  | Little standalone signal |
| `price_vs_ma20`          | …                            | …                    | …                        | …                       | …                        |
| `rolling_30d_volatility` | …                            | …                    | …                        | …                       | …                        |

This should answer:

1. Which features have the strongest relationship with each target?
2. Are relationships linear, monotonic or primarily directional?
3. Are the signs consistent across tickers?
4. Are apparent differences supported visually?
5. Do conclusions survive the common-period comparison?
6. Are any results suspicious enough to require leakage review?

---

# Final output set

The section only needs:

1. **Figure 1:** Pearson and Spearman feature–return heatmaps
2. **Table 1:** Ranked next-day-return relationship summary
3. **Figure 2:** Standardised up/down separation heatmap
4. **Table 2:** Ranked target-direction separation summary
5. **Figure 3:** Up/down distributions for the top three features
6. **Table 3:** Full-period versus common-period robustness
7. **Table 4:** Final feature assessment

Remove the separate focused tests for lagged returns, volatility quintiles and MA20 regimes. Those either duplicate existing analysis or expand beyond the purpose of this section.
