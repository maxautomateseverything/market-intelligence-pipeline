# Feature Analysis Report

Feature target analysis aims to understand whether the validated engineered features conain measurable realtionships with target returns or target direction.

Our analysis investigates:

- Feature relaionshiups with target return.

- Feature relationships with target direction.

- Full vs common period robustness.

## Feature–Target Analysis

Feature relationships with **next-day return are weak across all tickers**, with absolute Pearson correlations no higher than approximately **0.13** and generally weaker Spearman relationships. This indicates limited standalone linear or monotonic predictive signal. The difference between Pearson and Spearman for several features, particularly daily/log returns, also suggests that some Pearson relationships may be influenced by the magnitude of extreme observations rather than a consistent rank-based relationship. This directly addresses the requirement to assess feature strength, direction, consistency across tickers and potential predictive signal.  

Directional separation is similarly limited. **Cohen's d values are small across almost all feature–ticker combinations**, showing substantial overlap between Up- and Down-day feature distributions. `lag_1_return` has the largest median absolute separation (**0.058**), while `daily_return`, `log_return`, `cumulative_returns` and `drawdown` show comparatively consistent directions across tickers. The largest isolated effect is SNDK `relative_volume` (**d = 0.208**), indicating that stronger effects are mainly ticker-specific rather than general across assets. The violin/box plots reinforce the heavy class overlap expected when standalone directional information is weak.  

There is **little evidence of a consistent lagged-return, volatility or price-relative-to-MA20 signal**. Lagged-return effects vary in both magnitude and direction between tickers, while volatility and `price_vs_ma20` relationships remain small. This suggests no clear universal momentum, reversal, volatility or short-term trend effect for predicting the following day. 

Restricting all tickers to a **common observation period increases several median Spearman correlations**, particularly for `drawdown`, `relative_volume` and `cumulative_returns`. However, even the largest common-period median correlation remains only about **0.063**. The relationships are therefore somewhat **period-sensitive**, but the overall conclusion of weak univariate predictive signal remains unchanged. This common-period check is important because later-listed assets cover different market regimes. 

### Conclusion

Overall, the engineered features provide **limited standalone predictive information for next-day return or direction**. The strongest effects are mostly ticker-specific, while cross-ticker relationships remain weak. These features may still contribute useful information when combined in a multivariate model, but the results should be treated as preliminary signals rather than evidence of strong predictability.  
