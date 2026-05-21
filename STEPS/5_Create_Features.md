## Feature Creation

We aim to create features we will use further in the analysis and modelling and answer the question "what useful signals and measurements can i create from this data?"

```
clean_prices
    ↓
calculate financial/statistical features
    ↓
price_features
```

Features.py creates the following features:
- daily_return
- log_return
- cumulative_returns
- rolling_7d_return
- rolling_30d_return
- rolling_30d_volatility
- moving_avg_20
- moving_avg_50
- price_vs_ma20
- relative_volume
- drawdown
- lag_1_return
- lag_5_return
- target_next_day_return (prediction)
- target_dreiction (prediction)

This data will flow into the price_features table and should contain:
- clean price data
- engineered financial metrics / features
- predictive targets

Every feature should satisfy at least on of these purposes:
- Performance -> cumulative returns.
- Risk -> volatility.
- Trend -> movign average.
- Momentum -> rolling return.
- Volume analytics -> relative volume
- Risk analytics -> drawdown.
- Predict future returns (ML features) -> lagged returns.
- Feed ML model (targets) -> target variables.

## Daily, Log, and Cumulative Return

We use adj_close to calculate return since adj_close inludes adkjustments for various corporate actions such as stock splits, dividends, and corporate spinoffs.

We calculate return as adj_close at t divided by adj_close at t-1 minus 1, giving the decimal equivalent of the percent (i.e., 0.2 = 20%)

We calculate log return as the natural log of adj_close at t divided by adj_close at t-1.

The features provide answers to the following questions:
- simple return: how much did the wealth change in a day.
- log return: what continuously compounded growth rate would cause this price change in a day.

Simple return acts as the intuitive return whcih is useful for dashboards and human understanding while  log return is more mathematically convenient and good for modelling.

In calculating returns it should be noted that one consideration was taken into account - single day returns are based on the previous possible trading day rather than previous calendar or business day (markets close on additional days not included). We therefore outputted 3 returns to analyse:
- no calendar returns: returns simply based on the previous row.
- busienss calendar returns: returns simply based on the previous business day.
- excahnge calendar returns: returns simply baed on the previous trading day for that exchange.

This worked great, the results of whch can be seen in the data/inspect/returns.inspect.csv file. The exchange calendar returns would have been used if we had not had to remove a row due to OCLH logic in the transform.py step. The single row that was removed was 02.03.2026 for RPI.L ticker that had an open stock value lower than the apparent low value for that trading day.

Additionally, since quality is not a huge deal and this was a learning project we opted for the more simple no calendar returns since that would suffice for this project and it would be easier for time-series forcasting as we wouldn't have any missing values.

## Rolling Returns

The same calendar concept applies here.

We created a resusable rolling return function that allows us to reuse the function for variosu calendars and for various return windows (e.g., 7d or 30d).