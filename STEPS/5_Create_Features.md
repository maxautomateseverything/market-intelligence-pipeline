## Feature Creation

We create features from the `clean_prices` table so the data can be used for analysis, modelling, and prediction.

The main question is:

**What useful signals can be created from price and volume data?**

```text
clean_prices
    ↓
generate return, trend, risk, volume, and target features
    ↓
price_features
```

The final `price_features` table contains:

* clean price data
* engineered financial features
* prediction targets for modelling

## Features Created

`Features.py` creates the following groups of features:

### Return Features

Return features measure how prices change over time.

Created features include:

* `daily_return`
* `log_return`
* `cumulative_returns`
* `rolling_Xd_return`
* `lag_X_return`

These features are generated using `adj_close`, because adjusted close accounts for corporate actions such as:

* stock splits
* dividends
* spinoffs

The main function used is:

```python
generate_return_features()
```

This function creates simple daily returns, log returns, rolling returns, cumulative returns, and lagged returns across the configured calendars and window sizes.

## Calendar Handling

The code supports three calendar types:

### `no_calendar`

Uses the previous row directly.

This assumes the data has no missing dates and treats each row as the next valid observation.

### `business_calendar`

Uses the previous business day.

This accounts for weekends and helps detect missing business-day rows.

### `exchange_calendar`

Uses the actual trading calendar for each stock exchange.

This accounts for weekends, exchange holidays, and market closures.

This is the most accurate calendar option for financial market data.

## Moving Average Features

Moving averages are used to measure trend.

The main function used is:

```python
generate_moving_averages()
```

Created features include:

* `moving_avg_20`
* `moving_avg_50`

These are calculated for `adj_close` across the configured moving average windows.

Moving averages help identify whether a stock price is trading above or below its recent trend.

## Technical and Model Features

The script also creates additional features used for analysis and modelling.

### Price vs Moving Average

```python
price_vs_ma20
```

Measures how far the current adjusted close price is from its 20-day moving average.

This helps identify trend strength.

### Relative Volume

```python
relative_volume
```

Compares current volume against average volume.

This helps identify unusually high or low trading activity.

### Rolling Volatility

```python
rolling_30d_volatility
```

Measures recent risk by calculating the rolling standard deviation of daily returns.

Higher volatility means the stock price has been moving more aggressively.

### Drawdown

```python
drawdown
```

Measures how far the current price is below its previous running maximum.

This is useful for risk analysis.

## Prediction Targets

The code creates target variables for modelling.

### Next-Day Return

```python
target_next_day_return
```

Measures the return from the current day to the next valid trading day.

### Target Direction

```python
target_direction
```

Converts next-day return into a classification target:

* `1` if the next-day return is positive
* `0` if the next-day return is zero or negative

These targets allow the dataset to be used for machine learning prediction tasks.

## Final Output

Before inserting into the database, the script keeps and renames the expected final columns using:

```python
keep_and_rename_expected_feature_columns()
```

The final table includes:

* base price columns
* return features
* moving average features
* technical/risk features
* prediction targets

The data is then inserted into the `price_features` table using:

```python
insert_price_features()
```

## Overall Pipeline

```text
clean_prices
    ↓
generate_return_features()
    ↓
generate_moving_averages()
    ↓
generate_remaining_features()
    ↓
keep_and_rename_expected_feature_columns()
    ↓
insert_price_features()
    ↓
price_features
```

## Feature Purpose Summary

| Purpose          | Feature Examples                                  |
| ---------------- | ------------------------------------------------- |
| Performance      | `daily_return`, `cumulative_returns`              |
| Momentum         | `rolling_Xd_return`, `lag_X_return`               |
| Trend            | `moving_avg_20`, `moving_avg_50`, `price_vs_ma20` |
| Volume analytics | `relative_volume`                                 |
| Risk             | `rolling_30d_volatility`, `drawdown`              |
| Prediction       | `target_next_day_return`, `target_direction`      |

In summary, this script transforms raw clean price data into a feature-rich table that can be used for financial analysis, risk measurement, trend analysis, and machine learning.
