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
- lag_1_return
- lag_5_return
- moving_avg_20
- moving_avg_50
- price_vs_ma20
- relative_volume
- rolling_30d_volatility
- drawdown
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

## Return Features

Across all calculations we use adj_close as current price as it includes adjustments for various corporate actions such as:
- stock splits.
- dividends.
- corporate spinoffs.

The function `generate_return_features` generates the following return features:
- daily return or simple 1 day return.
- log return.
- rolling returns (across intervals configured in `ROLLING_INTERVALS`).
- cumulative returns.
- lagged returns (across intervals configured in `LAGGED_INTERVALS`)

The function `generate_return_features` takes 4 input variables:
- input_df: pandas dataframe containing clean prices data.
- calendars: list of string values configured in `CALENDARS`.
- rolling_windows: list of integer values configured in `ROLLING_WINDOWS`.
- lagged_windows: list of integer values configured in `LAGGED_WINDOWS`.

### Calendars

One thing to note is the consideration of various calendars of which the calculations are based. We cosnider three types of calendars:
- no_calendar
- business_calendar
- exchange_ calendar

`no_calendar` assumes that there are no missing dates in the data, taking each sequential row at face value.

`business_calendar` takes into account weekends basing returns simply on the previous business day. This will capture possible missing rows, e.g., a random wednesday missing preventing you from calculating returns that require that days adj_close.

`exchange_calendar` takes into account additional holidays and closures of the specific exchange of the stock, allowing true representation of truly missing dates.





