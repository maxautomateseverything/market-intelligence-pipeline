# EDA Checklist Before Modelling

1. Create EDA notebook
- [x] Create notebooks/01_eda.ipynb
- [x] Load price_features from DuckDB
- [x] Sort by ticker, date
- [x] Confirm row count and column count
- [x] Confirm date range
- [x] Confirm tickers included

2. Data quality checks
- [x] Check missing values by column
- [x] Check missing values by ticker
- [x] Check duplicate ticker + date rows
- [x] Check infinite values
- [x] Check zero/negative prices
- [x] Check date gaps per ticker
- [x] Check whether all tickers have enough history
- [x] Check target columns have expected nulls at the final row per ticker

3. Price behaviour
- [x] Plot adjusted close over time per ticker
- [x] Compare normalized prices starting at 100
- [x] Identify major price jumps or drops
- [x] Check whether any ticker behaves unusually
- [x] Write 2–3 observations

4. Return analysis
- [x] Plot daily returns over time
- [x] Plot return distributions
- [x] Compare average daily returns by ticker
- [x] Compare return volatility by ticker
- [x] Identify extreme return days
- [x] Check skewness/kurtosis if you want extra depth
- [ ] Write 2–3 observations

5. Risk analysis
- [ ] Plot rolling volatility by ticker
- [ ] Identify periods of high volatility
- [ ] Calculate max drawdown by ticker
- [ ] Plot drawdown over time
- [ ] Compare risk across assets
- [ ] Write 2–3 observations

6. Correlation analysis
[] Create daily return correlation matrix
[] Compare asset relationships
[] Check whether correlations change during volatile periods
[] Identify diversification patterns
[] Write 1–2 observations
7. Feature analysis
[] Inspect moving averages
[] Plot adj_close vs moving averages
[] Inspect price_vs_ma20
[] Inspect relative_volume
[] Inspect lagged returns
[] Inspect rolling returns
[] Check whether feature values look sensible
[] Check feature distributions
8. Target analysis
[] Inspect target_next_day_return
[] Inspect target_direction
[] Check class balance for direction target
[] Calculate percentage of up days vs down days
[] Compare target behaviour by ticker
[] Check whether targets are too noisy
[] Write modelling implications
9. Feature-target relationships
[] Correlate features with target_next_day_return
[] Compare features against target_direction
[] Plot feature distributions for up days vs down days
[] Check whether lagged returns have any predictive signal
[] Check whether volatility affects next-day returns
[] Check whether price vs moving average relates to next-day direction
10. Modelling readiness
[] Choose your modelling feature set
[] Choose your target variable
[] Decide whether to model all tickers together or separately
[] Decide train/test split date
[] Remove leakage columns
[] Confirm no future-looking features are used
[] Confirm target is only used as target, not input
[] Confirm features are available before prediction date
11. Key EDA outputs to save
[] Summary statistics table
[] Missing-values report
[] Correlation matrix
[] Risk/return table
[] Class balance table
[] Feature-target correlation table
[] 5–10 written insights
[] Modelling decisions section


## Final EDA deliverable

End the notebook with:

EDA Summary:
1. What data I have
2. What quality issues I found
3. What the main return/risk patterns are
4. Which features look useful
5. Which target I will model
6. How I will split train/test data
7. What limitations I noticed