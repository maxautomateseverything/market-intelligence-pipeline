# EDA Checklist Before Modelling

1. Create EDA notebook
[] Create notebooks/01_eda.ipynb
[] Load price_features from DuckDB
[] Sort by ticker, date
[] Confirm row count and column count
[] Confirm date range
[] Confirm tickers included

2. Data quality checks
[] Check missing values by column
[] Check missing values by ticker
[] Check duplicate ticker + date rows
[] Check infinite values
[] Check zero/negative prices
[] Check date gaps per ticker
[] Check whether all tickers have enough history
[] Check target columns have expected nulls at the final row per ticker
3. Price behaviour
[] Plot adjusted close over time per ticker
[] Compare normalized prices starting at 100
[] Identify major price jumps or drops
[] Check whether any ticker behaves unusually
[] Write 2–3 observations
4. Return analysis
[] Plot daily returns over time
[] Plot return distributions
[] Compare average daily returns by ticker
[] Compare return volatility by ticker
[] Identify extreme return days
[] Check skewness/kurtosis if you want extra depth
[] Write 2–3 observations
5. Risk analysis
[] Plot rolling volatility by ticker
[] Calculate max drawdown by ticker
[] Plot drawdown over time
[] Compare risk across assets
[] Identify periods of high volatility
[] Write 2–3 observations
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