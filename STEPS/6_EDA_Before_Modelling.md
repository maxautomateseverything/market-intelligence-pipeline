# EDA Checklist Before Modelling

## 1. Create EDA notebook
* \[x] Create notebooks/01\_eda.ipynb
* \[x] Load price\_features from DuckDB
* \[x] Sort by ticker, date
* \[x] Confirm row count and column count
* \[x] Confirm date range
* \[x] Confirm tickers included

## 2. Data quality checks
* \[x] Check missing values by column
* \[x] Check missing values by ticker
* \[x] Check duplicate ticker + date rows
* \[x] Check infinite values
* \[x] Check zero/negative prices
* \[x] Check date gaps per ticker
* \[x] Check whether all tickers have enough history
* \[x] Check target columns have expected nulls at the final row per ticker

### Missingness by column:
- identify which fields have missing values.
- Is it  structural issue or accidental.
- Is imputation or dropping of data required.

### Missingness by ticker:
- Is missingness concentrated in one asset.
- Does an asset have realiable coverage.

### Duplicates:
- Does any asset have duplicate rows.
- Duplicates should be removed or aggregated.

### Infinite values:
- check whether any calculation creaed inifint values.
- usually indiciated by zero division or an invalid transformation and should be replaced with NaN.

### Zero/negative prices:
- Verify open, high, low, close and adj close are strictly positive.
- zero or negative prices are invalid and should be investigated.

### Date gaps per ticker:
- Expected missing dates based on the calendar.

### Enough history per ticker:
- Ticker meets min observations required for rolling calculations.
- Shorter sample period may be needed or ticker be removed.

### Expected nulls in target columns:
- Ensure final row horizons are null.
- Ensure correct construction and avoid look ahead bias.

### Should produce:

Example:
The dataset contains seven assets downloaded from Yahoo Finance covering 2018 to the present. Data quality checks were performed at both the column level and ticker level. The checks confirm whether the panel contains missing values, duplicate ticker-date observations, invalid prices, infinite values, irregular date gaps, and sufficient historical coverage for feature engineering and modelling. Target-column nulls were also checked to ensure they only occur where expected due to forward-looking target construction.

### Comment on:

- Dataset reliability: enough clean data?
- Cross asset consistency: similar data coverage?
-- Do all assets start in 2018?
-- Do all assets end on the same most recent date?
-- Are there assets with fewer observations?
-- Are missing values concentrated in one ticker?
- Trading calendar alignment: expected vs unexpected gaps.
-- Expected gaps: weekends, public holidays, market closures.
-- Unexpected gaps: missing trading days for only one ticker while others have data.
- Modelling impact: how it affects later stages?
-- Missing prices affect return calculations.
-- Duplicate rows distort rolling features.
-- Infinite values break scaling and model training.
-- Invalid prices make log returns impossible.
-- Insufficient history affects train/test split reliability.
-- Incorrect target nulls may indicate look-ahead bias.

### Conclusion:

Example:
This data quality step verifies that the financial time-series panel is structurally valid before feature engineering and modelling. The main objective is to ensure that each ticker has clean, continuous, and sufficiently long price history, with no duplicate ticker-date rows, invalid price values, or unintended missing values. The target-null check is particularly important because it confirms that missing target values occur only at the final forecast horizon per ticker, reducing the risk of look-ahead bias.


## 3. Price behaviour
* \[x] Plot adjusted close over time per ticker
* \[x] Compare normalized prices starting at 100
* \[x] Identify major price jumps or drops
* \[x] Check whether any ticker behaves unusually
* \[x] Write 2–3 observations

### Plot adjusted close over time per ticker:
- show long term price path for each asset using adj close.
- identify broad trends: upward, downward, sideways, volatile, regime changing?

### Compare normalised prices starting at 100:
- rebase each ticker to 100 at first available price date.
- compare relative growth fairly, especially since some IPO later.

### Identify major price movements:
- Look for large movements.
- determine whether they are caused by market, event, IPO behaviour or possible data issues.

### Check whether any ticker behaves unusually:
- compare volatility, trend, drawdowns, and price path shape across assets.
- identify assets that may dominate the model due to extreme voalitlity or unusual price behaviour split or adjustment related issues)

### Note on later IPO assets:
- Don't treat later IPO assets as having missing data, instead mention their shorter trading history.
- comparisons also need to be drawn from a point at which all assets begin to make a fair comparison.

### Points to draw for adj close plots:
- Which assets increased the most in absolute price terms.
- Which assets experienced long drawdowns.
- Whether any asset had sharp structural breaks.
- Whether price trends changed after major market periods.
- Whether newer IPO assets have more volatile early trading behaviour.

### Points to draw from normalised prices:
- If £100 or $100 had been invested at each asset’s first available date, which asset grew the most?
- Which assets underperformed relative to the group?
- Which assets had the largest drawdowns?
- Which assets recovered faster after drops?
- Whether later IPO assets appear stronger or weaker when measured from their own start date.

### Points to draw from major movements:
- largest daily gain per ticker: extreme upside moves.
- largest daily loss per ticker: extreme downside moves.
- largest weekly gain/loss: reduce noise compared with daily moves.
- maximum drawdown: shows worst peak to trough decline.
- recovery after drawdown: shows resilience of the asset.

### Points to draw for unusual ticker behaviour:
- Much higher volatility than the others.
- Very short history compared with the rest.
- Very large jumps or crashes.
- Flat or near-zero movement for long periods.
- A sudden price level shift.
- A price path that looks inconsistent with market behaviour.

### Strong observations:

Example:
1. Relative performance differs significantly across assets.
The normalized price chart shows which assets delivered the strongest cumulative growth after rebasing each ticker to 100 at its first available trading date.
2. Some assets have shorter histories due to later IPO dates.
These assets should not be directly compared over the full 2018–present period. A common-period comparison may be needed for fair cross-asset analysis.
3. Large price jumps or drawdowns indicate different risk profiles.
Assets with sharper drops or more volatile movements may require careful treatment during feature engineering, scaling, and model evaluation.

### Conclusion:

Example:
The price behaviour analysis shows how each asset evolved over time and whether the assets are comparable on a relative basis. Using adjusted close prices accounts for corporate actions, while normalized prices allow performance comparison across assets with different price levels and IPO dates. This step helps identify unusual price behaviour, major jumps or drops, and differences in volatility that may affect later return analysis, feature engineering, and predictive modelling.

## 4. Return analysis
* \[x] Plot daily returns over time
* \[x] Plot return distributions
* \[x] Compare average daily returns by ticker
* \[x] Compare return volatility by ticker
* \[x] Identify extreme return days
* \[x] Check skewness/kurtosis if you want extra depth
* \[ ] Write 2–3 observations

### Plot daily returns over time:
- Check how returns fluctuate through time for each ticker.
- Identify periods of high volatility, calm periods, market shocks, and whether volatility changes over time.

### Plot return distributions:
- Check the shape of each ticker's daily return distribution.
- Determine whther returns are centred around zero, whether they are summetric, and whether they have fat tails.

### Compare average daily returns by ticker:
- Calculate the mean daily return for each asset.
- Identify which assets had higher average daily performance, but interpret carefully because daily mean returns are usually small and noisy.

### Compare return volatility by ticker:
- Calculate standard deviation of daily return per ticker.
- Identify which assets are riskier or more unstable. This is foten more informative than average daily return.

### Identify extreme return days:
- Find the largest positive and negative return days.
- Detect event drive moves, market shocks, IPO related volatility, or possible data issues.

### Check skewness / kurtosis:
- Measure asymmetry and tail risk in returns.
- Udenrstand whether returns have more downside risk, upside spikes, or extreme tails compared with a normal distribution.

### Key metrics per ticker:
- Start date.
- Observations.
- Mean daily return.
- Daily volatility.
- Min daily return.
- Max daily return.
- Skewness.
- Kurtosis.

### Important note on later IPO assets:
- their average return is based on a shorter sample
- they may miss earlier market regimes, such as 2018–2020
- their early trading period may be unusually volatile
- direct comparison with assets available since 2018 may be unfair

### What to derive from daily return plots:
- identify volatility clustering.
- are returns mostly close to zero.
- are there perios with unusually large swings.
- do some tickers have visibly higher volatility.
- do later IPO assets show larger eary stage return swinfs.
- are extreme returns isolated or clustered.

### What to derive from return distributions:
- centred near zero: normal for daily financial returns.
- wide distributions: high volatility.
- long left tail: large downside risk.
- long right tail: large upside jumps.
- fat tails: extreme returns occur mode often than a normal distribution would suggest.
- skewness: whether extreme moves are more positive or negative.
- kurtosis: whether asset has usually large outliers.

### Average return vs volatility:
- return to risk ratio = mean daily return / daily return standard deviation.
- this is not full sharpe ration unless we adjust for the risk free rate.

### Extreme return days:
- for each ticker identify:
	- top 5 largest daily gains
	- top 5 largest daily losses
	- dates of those events
	- whether they occur around known market events
	- whether they happen near IPO dates
	- whether they look like data errors
- market wide: many tickers move sharply on the same date.
- ticker specific: only one asset has an extreme move.
- IPO related: occurs soon after the asset starts trading.
- data related: looks too large or inconsistent with price behaviour.

### Skewness and kutsosi interpretation:
- skewness > 0: more extreme positiveve returns - upside jumps are more common/larger.
- skewness < 0: more extreme negative returns - downside shocks are more common/larger.
- high kurtosis: fat tails / many outliers - extreme return days occur more often than expected.

### Observations:

example:

Observation 1: Returns fluctuate around zero but volatility differs by ticker

Daily returns are generally centred around zero, which is expected for financial assets, but the size of daily fluctuations differs across tickers. Some assets show wider return ranges, indicating higher volatility and greater short-term risk.

Observation 2: Later IPO assets need cautious comparison

Assets that IPO later have shorter return histories, so their average return and volatility are based on fewer observations. This means they may not be directly comparable with assets that have full data from 2018, especially if they missed earlier market regimes.

Observation 3: Extreme return days indicate tail risk

Several tickers may show large positive or negative return days, suggesting the presence of outliers and fat-tailed return distributions. These extreme values should be considered during modelling because they can affect scaling, error metrics, and prediction stability.

### Conclusion:

example: 

The return analysis shows that asset performance should be evaluated not only by average returns but also by volatility, extreme movements, and distribution shape. Daily returns help identify periods of market stress, ticker-specific shocks, and differences in risk across the seven assets. Since some assets IPO later, comparisons should account for unequal history lengths, and a common-period analysis may be useful for fair cross-asset evaluation.

## 5. Risk analysis
* \[ ] Plot rolling volatility by ticker
* \[ ] Identify periods of high volatility
* \[ ] Calculate max drawdown by ticker
* \[ ] Plot drawdown over time
* \[ ] Compare risk across assets
* \[ ] Write 2–3 observations

### Plot rolling volatility by ticker:
- how each asset's volatility changes over time.
- 30 day, 60 day or 90 day rolling standard deviation.
- identify whether risk is table, increasing, decreasing or concentrated in specific market periods.

### Identify periods of high volatility:
- periods where rolling volatility spikes for one or more ticker.
- link volatility spikes to market stress, asset-specific events, IPO instability, eanigns periods, or major macro shocks.

### Calculate max drawdown by ticker:
- worst peak to trough fall or each asset.
- identify the maximum loss an investor would have experienced from buying at a peak and holding through till the lowest point.

### Plot drawdown over time:
- how deep and how long each asset stayed below its prviosu peak.
- evaluate downside risk, recovery behaviour, and whether some assets reman in prolonged drwdown.

### Compare risk across assets:
- compare rolling volatility, max drawdown, and drawdown duration across the 7 assets.
- rankt he assets form lower risk to higher risk and identify which assets may domainte portfolio/model risk.

### Important note on later IPO assets:
- for fair cross-asset comparison we should also compare all assets from he latest common start date.

### Inspecting rolling volatility plot:
- Spikes shared by most tickers.
- Spikes affecting only one ticker.
- Assets with consistently higher volatility.
- Assets whose volatility decreases as they mature.
- IPO assets with unstable early trading periods.

### Inspecting drawdown plot:
- The deepest drawdowns.
- The longest periods below previous highs.
- Whether assets recovered quickly or stayed depressed.
- Whether drawdowns happen at similar times across assets.
- Whether some assets are still below previous peaks near the end of the dataset.

### Observation:

example:

Observation 1 — volatility clustering

Rolling volatility is not constant over time. Several assets experience clear volatility spikes during stressful market periods, showing that risk is time-varying rather than stable.

Observation 2 — later IPO assets

Assets with later IPO dates have shorter histories, so their risk metrics are based on fewer observations. These assets should be compared both over their full available history and over a common period shared by all tickers.

Observation 3 — downside risk differences

Maximum drawdown varies across assets, indicating different downside-risk profiles. Assets with deeper or longer drawdowns may be riskier even if their average returns appear attractive.

### Conclusion:

example: 

The risk analysis evaluates how unstable and vulnerable each asset has been over time. Rolling volatility highlights periods of changing return variability, while drawdown analysis captures the severity of peak-to-trough losses. Since some assets IPO later, risk comparisons should be interpreted carefully and supported by a common-period comparison. This step helps identify which assets carry higher downside risk, which assets experience more volatile regimes, and which tickers may require careful treatment during modelling or portfolio analysis.

## 6. Correlation analysis
* \[ ] Create daily return correlation matrix
* \[ ] Compare asset relationships
* \[ ] Check whether correlations change during volatile periods
* \[ ] Identify diversification patterns
* \[ ] Write 1–2 observations

### Create daily return correlation matrix:
- Calculate pariwise correaltions between the daily returns of all 7 assets.
- Identify which assets move closely together and which assets behave more independently.

### Compare asset relationships:
- Look for highly positive, weak or negative correlations.
- Understand whether assets belong to similar risk groups or provide different market exposure.

### Check whether correlations change during volatile periods:
- compare correlations in normal periods versus high volatility periods.
- determine whether diversification breaks down when markets become stressed.

### Identify diversification patterns:
- find assets with lower or negative correlations to the rest.
- idenifu which assets may reduce portfolio risk when combined with others.

### Interpreting return correlation matrix:
- 0.7-1.0: strong positive relationship.
- 0.4-0.7: moderate positive relationship.
- 0.1-0.4: weak positive relationship.
- -0.1-0.1: very weak or no relationship.
- <-0.10: potential diversification benefit.

### Improtant not on later IPO assets:
- correlations are calculated on only overlapping dates so the correlations may be based on differtn sample periods.
- do full pairwise correlation as well as common period correlation.

### Chosing high volatile periods:
- can inspect on:
	- full sample: using all available date.
	- high volaitly periods: where rolling volatility is unusually high.
	- normal periods: correlation during calmer market periods.
	- rolling correlation: 60 day or 90 day rolling correlation between selected asset pairs.

### Identifying diversification patterns:
- useful to derive average correlation with other assets.
- Pairs with high positive correlation.
- Assets with low average correlation to the rest.
- Assets that become highly correlated during stress periods.
- Assets that behave differently due to sector, geography, asset class, or maturity.
- Later IPO assets whose short history may make correlation estimates less reliable.

### Observations:

example:

Observation 1 — asset relationships

The daily return correlation matrix shows that some assets move closely together, suggesting shared exposure to similar market or sector factors. Assets with weaker correlations may provide better diversification benefits within the group.

Observation 2 — correlation during volatility

Correlations should be compared across normal and high-volatility periods because diversification can weaken during market stress. If correlations rise during volatile periods, the assets may offer less protection when downside risk is highest.

### Conclusion:

example:

The correlation analysis evaluates how closely the seven assets move together based on daily returns. This helps identify whether the asset universe provides meaningful diversification or whether several tickers share similar market behaviour. Since some assets IPO later, correlations should be interpreted carefully because the available overlapping history differs across assets. Comparing correlations during normal and high-volatility periods also shows whether diversification remains stable during market stress.

## 7. Feature Analysis

### Analysis checklist

* [ ] Check whether feature values are sensible
* [ ] Inspect moving averages
* [ ] Plot adjusted close against moving averages
* [ ] Inspect `price_vs_ma20`
* [ ] Inspect `relative_volume`
* [ ] Inspect lagged returns
* [ ] Inspect rolling returns
* [ ] Check feature distributions
* [ ] Check relationships and redundancy between features
* [ ] Confirm that predictor features do not contain future information

---

#### 7.1 Checking sensible feature values

##### Purpose

Check whether the engineered features have been calculated correctly and whether their values are structurally valid.

This section should identify:

* Missing values
* Infinite values
* Unexpected internal gaps
* Incorrect rolling-window start positions
* Incorrect signs
* Incorrect scales
* Impossible values
* Division-by-zero errors
* Ticker-specific abnormalities
* Features that accidentally use future information

General validity checks should be completed here rather than repeated in every later feature section.

##### Outputs to inspect

* Feature-definition table
* Independent feature-recalculation table
* Feature-health matrix
* Missing-value percentage matrix
* Missing-feature heatmap
* Expected-domain violation table
* Zero-volume summary
* Feature-lineage and leakage table

##### Questions to answer

* Do independently recalculated features match the stored feature values?
* Are differences small enough to be explained by floating-point precision?
* Do rolling features begin only after the required number of observations?
* Are missing values concentrated at the beginning of each ticker’s history?
* Are there missing values after a feature has already become available?
* Are there positive or negative infinite values?
* Are adjusted prices positive?
* Is volume non-negative?
* Are simple returns normally greater than `-1`?
* Are moving averages positive when available?
* Is relative volume non-negative?
* Is rolling volatility non-negative?
* Is drawdown normally between `-1` and `0`?
* Does `price_vs_ma20` have the same sign as `adj_close - MA20`?
* Does `target_direction` contain only its expected classes?
* Are target features excluded from the predictor set?
* Are features calculated separately within each ticker?
* Does the assumed prediction time make the current closing price and current volume available?

##### How to analyse the results

A feature should normally pass the independent recalculation check with zero mismatched rows or only negligible floating-point differences.

Initial missing values are expected when a feature requires historical observations. For example:

* A one-period return normally has one initial missing value.
* MA20 normally has 19 initial missing values when the current observation is included in the 20-observation window.
* MA50 normally has 49 initial missing values.
* A seven-observation return based on `price / price.shift(7) - 1` normally has seven initial missing values.
* A 30-observation return normally has 30 initial missing values.
* A next-day target normally has a missing value at the end of each ticker’s history.

Later IPO assets should have shorter total feature histories, but the number of required initial observations should remain consistent.

Internal missing values are more concerning than initial missing values. They may indicate missing source data, an invalid denominator, or an implementation error.

Any infinite value should be investigated. Common causes include:

* A zero denominator
* A zero moving average
* A zero rolling-volume baseline
* Invalid logarithms
* Incorrect handling of missing values

The feature-lineage table should show that predictor features use only current and historical information. Target variables may use future information, but they must not be included as predictors.

The validity of current-day price and volume features also depends on the prediction timestamp. They are valid for a model predicting the next trading day after the current market close, but may represent leakage for a model making predictions before the current close.

---

#### 7.2 Inspecting moving averages

##### Purpose

Check whether the moving-average features are correctly calculated and behave as expected.

The available moving-average features are:

* `moving_avg_20_no_calendar`
* `moving_avg_50_no_calendar`

MA200 cannot be assessed unless a 200-observation moving average is created.

##### Outputs to inspect

* Moving-average availability table
* Adjusted-close, MA20, and MA50 time-series plots
* Moving-average responsiveness and smoothness table
* MA20–MA50 crossover table
* Unexpected jump and flat-section diagnostics

##### Questions to answer

* Does MA20 begin only after enough observations are available?
* Does MA50 begin only after enough observations are available?
* Does MA20 become available before MA50?
* Does MA20 react faster than MA50?
* Is MA50 smoother than MA20?
* Are both moving averages smoother than adjusted close?
* Do the moving averages follow the general direction of the price?
* Are there unexpected jumps in either moving average?
* Are there suspiciously long flat sections?
* Do later IPO assets have shorter moving-average histories?
* Do MA20 and MA50 cross at visually sensible points?

##### How to analyse the results

The expected responsiveness order is:

[
|\Delta MA50| < |\Delta MA20| < |\Delta Price|
]

MA20 should respond more quickly to recent changes because it uses fewer observations. MA50 should change more slowly and provide a smoother representation of the longer-term trend.

A moving average should not normally jump sharply unless:

* The underlying price changed substantially
* A large historical observation entered or left the rolling window
* There was a stock split or adjustment issue
* The feature was calculated incorrectly

Long flat sections may be valid for a very stable price series, but they should be reviewed when the underlying price is changing.

The moving averages should generally remain close to the price while smoothing daily noise. MA20 should normally be closer to the current price than MA50.

---

#### 7.3 Plotting adjusted close against moving averages

##### Purpose

Compare the adjusted closing price with MA20 and MA50 over time.

Use one panel per ticker so that differences in price scale do not make the plots difficult to interpret.

##### Questions to answer

* Do the moving averages follow the adjusted price correctly?
* Does MA20 turn before MA50 when the price changes direction?
* Are moving averages below the price during sustained upward trends?
* Are moving averages above the price during sustained downward trends?
* Do crossovers occur after meaningful changes in price direction?
* Are there periods where price repeatedly moves around a moving average?
* Do the moving averages appear to provide descriptive support or resistance?
* Do later IPO assets have shorter plotted histories?

##### How to analyse the results

During a sustained upward trend, the expected ordering is often:

[
Price > MA20 > MA50
]

During a sustained downward trend, the expected ordering is often:

[
Price < MA20 < MA50
]

When MA20 crosses above MA50, it may indicate improving short-term momentum relative to the medium-term trend. When MA20 crosses below MA50, it may indicate weakening momentum.

Crossovers should not be treated as automatically predictive. They are descriptive indicators whose usefulness must later be tested using out-of-sample modelling.

Support and resistance behaviour should also be described carefully. A moving average may appear to act as a reference level when price repeatedly rebounds from or falls back from it, but a visual pattern alone does not prove a stable trading relationship.

---

#### 7.4 Inspecting `price_vs_ma20`

##### Purpose

Measure how far the adjusted price is above or below its 20-observation moving average.

This feature can capture:

* Short-term momentum
* Short-term trend strength
* Temporary overextension
* Possible mean-reversion conditions

##### Outputs to inspect

* `price_vs_ma20` time-series plots
* Zero-reference line
* Sign-validation results
* Extreme-value dates
* Distribution and percentile summaries

##### Questions to answer

* Is the value close to zero when price is close to MA20?
* Is it positive when price is above MA20?
* Is it negative when price is below MA20?
* Does it increase during strong upward price movements?
* Does it decrease during sell-offs?
* Does it return toward zero after extreme movements?
* Are there unusually large values immediately after an IPO?
* Are there extreme values during market crashes or rallies?
* Are there infinite values caused by division by zero?
* Is the scale stored as a decimal or as percentage points?

##### How to analyse the results

When the feature is defined as:

[
price_vs_ma20_t =
\frac{Price_t}{MA20_t} - 1
]

the interpretation is:

* `0.00`: price is equal to MA20
* `0.05`: price is 5% above MA20
* `-0.05`: price is 5% below MA20

Large positive values indicate that price is substantially above its recent trend. This may reflect strong momentum, but it may also indicate an overextended movement.

Large negative values indicate that price is substantially below its recent trend. This may reflect downward momentum, panic selling, or a possible mean-reversion opportunity.

Extreme observations should be checked against the underlying price and moving-average plot before being labelled as errors. Large values during crashes, rallies, or early post-IPO periods may be unusual but valid.

---

#### 7.5 Inspecting relative volume

##### Purpose

Compare current trading volume with its recent normal level.

Relative volume may help identify:

* Unusual market participation
* Earnings-related trading
* News events
* IPO-period activity
* Market stress
* Abnormal investor interest

##### Outputs to inspect

* Relative-volume time-series plots
* Reference lines at `1`, `2`, and `3`
* Relative-volume summary table
* Relative-volume empirical distribution
* Largest relative-volume event table
* Zero-volume summary from the feature-validity section

##### Questions to answer

* Are most relative-volume values close to `1`?
* Are values greater than `2` or `3` uncommon?
* Are extreme spikes concentrated around a small number of dates?
* Do large volume spikes coincide with large absolute returns?
* Are spikes more common during the early IPO period?
* Are there periods where the normal volume level appears to change?
* Are there zero-volume days?
* Are there missing or infinite values?
* Is the feature strongly right-skewed?

##### How to analyse the results

A relative-volume value close to `1` indicates that trading volume is close to its recent average.

Typical interpretations are:

* Below `1`: lower-than-normal volume
* Around `1`: normal volume
* Above `2`: approximately twice normal volume
* Above `3`: approximately three times normal volume

The distribution is expected to be right-skewed. Most observations should be around ordinary trading levels, with occasional large spikes.

A large spike is not necessarily an error. Review the corresponding:

* Date
* Raw volume
* Daily return
* Absolute daily return
* Price relative to MA20
* Rolling returns

The dataset alone cannot prove that a spike was caused by earnings, news, or another event. Such dates should be described as candidate event dates unless external event data is available.

Extremely high values can compress the main time-series plot. A truncated display range or logarithmic scale may be used for visualisation, while the original observations should remain unchanged in the event table.

---

#### 7.6 Inspecting lagged returns

##### Purpose

Check whether previous-period return features are shifted correctly and whether past returns contain evidence of momentum or short-term reversal.

The lagged-return features are:

* `lag_1_return_no_calendar`
* `lag_5_return_no_calendar`

##### Outputs to inspect

* Lag-alignment audit table
* Full lag-alignment error summary
* Lag relationship matrix
* Lag-return quantile response plots
* Next-day return by lag quantile

##### Questions to answer

* Does `lag_1_return` equal the previous observation’s daily return?
* Does `lag_5_return` equal the daily return from five observations earlier?
* Are lag calculations performed separately for each ticker?
* Are there off-by-one errors?
* Does any ticker receive a lag value from the previous ticker?
* Are future returns accidentally used?
* Is the relationship between lagged and current returns positive or negative?
* Is the relationship between lagged and next-day returns positive or negative?
* Do high lagged-return quantiles lead to higher or lower future returns?
* Are the relationships consistent across tickers?

##### How to analyse the results

The required alignment is:

[
lag1_t = return_{t-1}
]

[
lag5_t = return_{t-5}
]

The first lagged observations should be missing because no earlier observations are available.

The lag-alignment table is primarily a calculation-validity check. Stored values should match independently shifted values within a small numerical tolerance.

The correlation matrix can then be used to inspect return behaviour:

* Positive correlation between past and future returns may indicate momentum.
* Negative correlation may indicate short-term reversal.
* Correlation close to zero suggests little monotonic relationship.
* Different signs across tickers suggest that the effect is not stable.

Spearman correlation is useful because return distributions often contain extreme values and may not have a purely linear relationship.

The quantile-response plots should be inspected for ordered patterns. For example:

* Increasing future returns across lag quantiles may indicate momentum.
* Decreasing future returns across lag quantiles may indicate reversal.
* A U-shaped or irregular pattern may indicate nonlinearity or instability.

These results are exploratory. Statistical and economic significance must later be assessed using time-aware, out-of-sample modelling.

---

#### 7.7 Inspecting rolling returns

##### Purpose

Use rolling returns to capture short- and medium-horizon momentum.

The available rolling-return features are:

* `rolling_7d_return_no_calendar`
* `rolling_30d_return_no_calendar`

Because the data uses a no-calendar structure, these names may represent seven and 30 trading observations rather than calendar days.

##### Outputs to inspect

* Rolling-return time-series plots
* Rolling-return availability table
* Rolling 7 versus rolling 30 scatter plots
* Rolling-return momentum-regime matrix

##### Questions to answer

* Are the initial observations missing until enough history is available?
* Does the seven-observation return become available before the 30-observation return?
* Are rolling returns positive during upward price trends?
* Are rolling returns negative during drawdowns?
* Does the shorter return horizon react faster?
* Is the 30-observation return smoother?
* Are extreme returns plausible when compared with the price history?
* Do later IPO assets have shorter rolling-return histories?
* How often do the short- and medium-term signals agree?
* How often does short-term momentum reverse relative to the longer trend?

##### How to analyse the results

The seven-observation return should react more quickly to recent price movements. The 30-observation return should provide a smoother view of medium-term momentum.

The combination of the two features produces four useful regimes:

| Rolling 30 return | Rolling 7 return | Interpretation                                      |
| ----------------- | ---------------- | --------------------------------------------------- |
| Positive          | Positive         | Short- and medium-term momentum are both positive   |
| Positive          | Negative         | Short-term pullback within a broader upward trend   |
| Negative          | Positive         | Short-term recovery within a broader downward trend |
| Negative          | Negative         | Short- and medium-term momentum are both negative   |

The regime matrix shows how frequently each ticker occupies these states.

Extreme rolling returns should be compared with the adjusted-price plot. A very large positive or negative value may be valid during:

* IPO volatility
* Market crashes
* Strong rallies
* Company-specific shocks

An extreme value that cannot be reconciled with the underlying price movement may indicate an incorrect return formula, price adjustment problem, or ticker-boundary error.

---

#### 7.8 Checking feature distributions

##### Purpose

Understand the statistical shape of each feature and determine whether scaling, transformation, clipping, or robust modelling methods may be required.

The main distribution analysis should focus on:

* Daily return
* Log return
* Lagged returns
* Rolling returns
* `price_vs_ma20`
* Rolling volatility
* Drawdown

Relative volume is analysed separately in its own section to avoid duplication.

Raw adjusted prices, moving-average levels, and cumulative returns should not be the main focus of pooled distribution plots because they are strongly affected by ticker price levels and the selected historical period.

##### Outputs to inspect

* Distribution summary matrix
* Skewness matrix
* Standard-deviation matrix
* IQR-outlier percentage matrix
* Boxplots by ticker
* Empirical cumulative distribution plots
* Median within-ticker Spearman correlation matrix
* Correlation consistency matrix
* Separate target-distribution summaries

##### Questions to answer

* Are return features centred close to zero?
* Are the distributions symmetric or skewed?
* Do the features have heavy tails?
* Which tickers contain the greatest variability?
* Which features contain the highest proportion of outliers?
* Are feature scales substantially different?
* Are transformations required?
* Would robust scaling be more appropriate than standard scaling?
* Are some engineered features highly correlated?
* Are correlations consistent across tickers?
* Is the target direction severely imbalanced?
* Does the target-return distribution contain extreme observations?

##### How to analyse the results

The distribution summary should be used to compare:

* Mean and median
* Standard deviation
* Percentiles
* Minimum and maximum
* Skewness
* Interquartile range
* Outlier percentages

Large differences between the mean and median suggest skewness or sensitivity to extreme values.

Return features are commonly centred near zero and may have heavy tails. A small number of large observations is not automatically evidence of an error, but these observations should be cross-checked against the price history.

Boxplots are useful for comparing scale and dispersion across tickers. Empirical cumulative distribution plots are useful for comparing the full distribution without relying on histogram bin choices.

Possible preprocessing implications include:

* **Standard scaling:** suitable when values are reasonably symmetric and not dominated by extreme observations.
* **Robust scaling:** suitable when features contain heavy tails or large outliers.
* **Log transformation:** potentially useful for strongly right-skewed non-negative features such as relative volume.
* **Winsorisation or clipping:** should only be considered after confirming that extreme values are valid and after thresholds are estimated using training data only.
* **No transformation:** suitable when tree-based models can naturally accommodate the observed scale and skewness.

Highly correlated features may contain overlapping information. For example:

* Daily return and log return are usually strongly correlated.
* Rolling 7- and 30-observation returns may be moderately correlated.
* MA-related features may overlap with rolling-return features.
* Drawdown and momentum features may be negatively related during declining markets.

Correlation alone does not require a feature to be removed. The decision should also consider:

* Interpretability
* Model type
* Out-of-sample performance
* Feature importance
* Stability across tickers and time

The target features should be analysed separately from predictor features. They should not be included in the predictor correlation matrix.

---

### Suggested observations

#### Observation 1 — Feature validity

The independently recalculated features broadly match the stored feature values, indicating that the rolling, lagged, and target calculations have been implemented consistently. Missing values are concentrated mainly at the beginning of each ticker’s history, where insufficient observations are available for moving averages and rolling returns, and at the end of each ticker’s history for next-day targets.

Any mismatched rows, internal missing values, or infinite observations should be investigated before modelling. Later IPO assets naturally contain fewer valid observations because their available price histories are shorter.

#### Observation 2 — Moving-average behaviour

MA20 reacts more quickly to changes in adjusted price, while MA50 produces a smoother and slower-moving representation of the broader trend. The moving averages generally follow the price without unexplained discontinuities, and MA20–MA50 crossovers occur after changes in price direction.

Periods where price remains above both averages are consistent with positive trend regimes, while periods below both averages are consistent with negative trend regimes. Any unusually long flat section or abrupt moving-average jump should be checked against the underlying adjusted-price data.

#### Observation 3 — Price relative to MA20

The `price_vs_ma20` feature is close to zero when price is near MA20, positive when price is above MA20, and negative when price is below MA20. This confirms that the feature has the expected sign and interpretation.

Large positive and negative values identify periods of strong momentum, sell-offs, or temporarily overextended price movements. Extreme observations should be compared with IPO periods, market crashes, and other large price movements before being treated as errors.

#### Observation 4 — Relative-volume behaviour

Relative volume is concentrated around normal trading levels and has a right-skewed distribution with occasional large spikes. Values above `2` or `3` identify days where trading activity is substantially greater than its recent baseline.

Some high-volume dates also coincide with large absolute returns, suggesting that the feature captures periods of unusual market participation. These dates may relate to earnings, news, IPO activity, or market stress, although external event data is required to establish the cause.

#### Observation 5 — Lagged-return behaviour

The lagged-return features align correctly with previous observations and do not cross ticker boundaries. Correlations between lagged and future returns are likely to be small and may differ across tickers.

Positive relationships may indicate momentum, while negative relationships may indicate short-term reversal. Quantile-response plots should be used to determine whether any relationship is ordered and consistent rather than being driven by a small number of extreme observations.

#### Observation 6 — Rolling-return behaviour

The rolling-return features become available only after sufficient history exists and behave consistently with the underlying price trends. Seven-observation returns respond more quickly to recent price changes, while 30-observation returns provide a smoother measure of medium-term momentum.

Periods where both rolling returns are positive represent aligned upward momentum. Disagreement between the two horizons identifies short-term pullbacks or recoveries within a broader trend.

#### Observation 7 — Feature distributions and preprocessing

Return-based features are centred close to zero but may contain heavy tails and large observations during volatile periods. Relative volume is strongly right-skewed, while rolling volatility and drawdown differ meaningfully across tickers.

These distributional differences suggest that some models may benefit from robust scaling or carefully justified transformations. Any clipping or winsorisation should be based only on the training data to avoid leakage.

Strong correlations between related return features may indicate overlapping information, but feature removal should be based on model validation rather than correlation alone.

---

### Conclusion

The feature analysis evaluates whether the engineered variables are correctly calculated, economically interpretable, and suitable for later modelling.

The feature-recalculation and health checks establish whether moving averages, rolling returns, lagged returns, relative volume, drawdown, volatility, and target variables have been constructed correctly. Expected missing values should appear mainly at the beginning of rolling or lagged features and at the end of next-day target features.

Moving averages and `price_vs_ma20` describe short- and medium-term trend behaviour. Relative volume captures unusual trading activity, while lagged and rolling returns represent momentum and reversal behaviour across different horizons. Distribution and correlation analysis identify skewness, heavy tails, scale differences, extreme observations, and potentially redundant features.

Because some assets listed later than others, the number of valid observations differs across tickers, particularly for features requiring longer histories. These differences should be considered when removing incomplete rows, splitting the data, and comparing model performance across assets.

Overall, this analysis determines whether the features are structurally valid, whether unusual values are plausible, whether transformations or robust scaling may be needed, and whether any features contain future information. Features should only proceed to modelling after unexplained mismatches, infinite values, internal missing values, and leakage risks have been resolved.

## 8. Target analysis
* \[ ] Inspect target\_next\_day\_return
* \[ ] Inspect target\_direction
* \[ ] Check class balance for direction target
* \[ ] Calculate percentage of up days vs down days
* \[ ] Compare target behaviour by ticker
* \[ ] Check whether targets are too noisy
* \[ ] Write modelling implications

### Inspect target next day returns:
- check distribution by ticker.
- understand whether the regression target is centred near zero, noisy, skewed, or affected by extreme values.

### Inspect target direction:
- check whether the direction target correctly maps returns into up/down classes.
- confirm the classification target is logically correct and suitable for prediction.

### Check class balance for direction target:
- Count how many observations are up vs down.
- Identify whether the classification problem is balanced or biased toward one class.

### Calculate percentage of up days vs down days:
- Calculate class percentages overall and per ticker.
- Establish a baseline accuracy for directional prediction.

### Compare target behaviour by ticker:
- Compare return distributions, up day ratios, volatility, and extreme across the 7 assets.
- Idenitfy whether some assets are harder to predict or behave differently.

### Check whether targets are too noisy:
- assess whether next day returns are highly random and close to zero.
- decide whether next day prediction is too difficult and whether longer horizon target may be better.

### Isnpecting target next day returns:
- Is the distribution centred close to zero?
- Are most values small?
- Are there extreme positive or negative returns?
- Are outliers concentrated in certain tickers?
- Are final rows per ticker NaN, as expected?
- Are there impossible values, such as infinite returns?

### Inspecting target direction:
- Does target_direction = 1 when next-day return is positive?
- Does target_direction = 0 when next-day return is negative?
- How are zero-return days handled?
- Are target labels missing only at the final row per ticker?
- Does the target accidentally use same-day return instead of next-day return?

### Inspecting class balance:
- 50% up / 50% down: Balanced target
- 55% up / 45% down: Slight upward bias
- 60% up / 40% down: Noticeable class imbalance
- 70% up / 30% down: Strong imbalance; accuracy can be misleading

### Inspecting target behaviour by ticker:
- Which ticker has the most volatile target.
- Which ticker has the strongest upward bias.
- Which ticker has the most extreme returns.
- Which ticker has the shortest usable target history.
- Whether all tickers should be modelled together or separately.

### Signs that the target is too noisy:
- Mean return close to zero: Average daily movement is small
- Large standard deviation: Daily movements vary widely
- Many observations near zero: Direction may be hard to classify
- Weak feature-target relationships: Features may not explain next-day movement
- Similar up/down proportions: Directional prediction may be close to random
- Extreme outliers: Model may overfit rare events

### Avoid target leakage:
- target_next_day_return uses shift(-1) only for the target.
- Features use only current or past information.
- Moving averages are calculated from current and past prices only.
- Lagged returns use shift(1), shift(5), etc.
- Rows with final target NaN per ticker are dropped before modelling.
- Scaling or imputation is fitted only on training data, not the full dataset.

### Observations:

example:

Observation 1 — target noise

The target_next_day_return distribution is expected to be centred close to zero, with most daily returns small in magnitude and occasional extreme movements. This suggests that predicting exact next-day returns may be challenging due to high noise.

Observation 2 — class balance

The target_direction variable should be checked for class balance across the full dataset and by ticker. If up days slightly exceed down days, a majority-class baseline should be used when evaluating classification models.

Observation 3 — ticker differences

Target behaviour may differ across tickers, especially for assets with later IPO dates or higher volatility. These assets may have fewer valid observations and less stable target statistics, which could affect model reliability.

### Conclusion:

example:

The target analysis verifies that the prediction variables are correctly constructed and suitable for modelling. target_next_day_return captures the next trading day’s return, while target_direction converts this into an up/down classification task. The key checks are whether target values are correctly shifted, whether final rows per ticker contain expected missing values, whether direction classes are balanced, and whether target behaviour differs across the seven assets. Since daily returns are often noisy, this step helps determine whether next-day return prediction is realistic and what baseline models should be used.


## 9. Feature-target relationships
* \[ ] Correlate features with target\_next\_day\_return
* \[ ] Compare features against target\_direction
* \[ ] Plot feature distributions for up days vs down days
* \[ ] Check whether lagged returns have any predictive signal
* \[ ] Check whether volatility affects next-day returns
* \[ ] Check whether price vs moving average relates to next-day direction

### Correlate features with target next day return:
- Check linear relationships between each feature and next day return.
- identify whether any features have weak, moderate, or no relationship with future returns.

### Compare features against target direction:
- compare feature values on up days vs down days.
- determine whether features differ meaningfully before positive and negative next day moves.

### Plot feature distributions for up days vs down days:
- use histograms, KDE plots, or boxplots grouped by target direction.
- check whether the feature separates the two classes or overlaps heavily.

### Check lagged returns for predictive signal:
- test whether previous returns relate to next day returns or direction.
- identify possible momentum or reversal effects.

### Check whether volatility affects next day returns:
- compare volatility features against future return direction.
- determine whether high risk periods are follows by larger weaker, or more negative returns.

### Check whether price vs ma20 relates to next day direction:
- compare whether price being above or below ma20 affects probability of an up day.
- derive whether short term trend/overextension has directional signal.

### Features to correlate with target next day returns:
- Trend features	ma20, ma50, price_vs_ma20
- Momentum features	return_lag_1, return_lag_5, rolling_return_5, rolling_return_20
- Risk features	rolling_volatility_20, rolling_volatility_60
- Volume features	relative_volume, volume_ma20
- Drawdown features	drawdown, distance_from_high

### Inspecting correlations with target next day returns:
- Which features have the strongest relationship with next-day return.
- Whether relationships are positive or negative.
- Whether signals are consistent across tickers.
- Whether any unusually high correlation suggests possible target leakage.

### Metrics to derive for features against target direction:
- Mean feature value on up days	Average feature value before positive next-day moves
- Mean feature value on down days	Average feature value before negative next-day moves
- Difference in means	Measures directional separation
- Median difference	More robust to outliers
- Distribution overlap	Shows whether the feature truly separates classes

### Features to plot for up vs down days:
- return_lag_1	Checks short-term reversal or continuation
- rolling_return_5	Checks short-term momentum
- rolling_return_20	Checks monthly momentum
- rolling_volatility_20	Checks whether risk conditions affect direction
- price_vs_ma20	Checks overbought/oversold behaviour
- relative_volume	Checks whether unusual volume predicts direction

### Inspecting features with target direction:
- Heavy overlap	Feature has weak standalone predictive power
- Up-day distribution shifted higher	Feature may have positive directional signal
- Up-day distribution shifted lower	Feature may indicate reversal or risk
- Wider distribution for down days	Feature may be linked to downside uncertainty
- Extreme outliers in one class	Feature may help detect rare events but may also overfit

### Inspecting lagged returns predictive signal:
- Positive lagged-return relationship	Momentum effect
- Negative lagged-return relationship	Mean-reversion effect
- Near zero relationship	Little predictive signal

### Inspecting volatility vs next day returns:
- Higher volatility followed by lower returns	Risk-off behaviour
- Higher volatility followed by higher absolute returns	Larger moves after unstable periods
- Higher volatility reduces up-day probability	Downside risk increases during stress
- No clear relationship	Volatility may not predict direction directly

### Interpreting price vs ma20 with target direction:
- Strongly positive	Is the next day more likely to be up or down?
- Around zero	Is the next day close to random?
- Strongly negative	Does the asset rebound or continue falling?

### Important note for later IPO assets:
- do both full and common period analysis.
- important because a featyre may look predictive for a later IPO asset simply because it only covers a specific market regime.

### What to be careful about:

1. Weak relationships are normal

For daily financial targets, feature-target relationships are often weak.

Do not overstate findings. A small correlation does not mean a strong predictive feature.

A good phrase:

The observed relationships should be interpreted as preliminary signals rather than proof of predictability.

2. Watch for target leakage

If any feature has a very high relationship with target_next_day_return, investigate it.

Possible leakage signs:

- Correlation unusually high, for example above 0.30.
- Feature uses shift(-1) accidentally.
- Rolling feature includes future values.
- Scaling was fitted on the full dataset before train/test split.
- Target is used directly or indirectly in feature creation.

3. Check per ticker

A relationship may exist for one ticker but not others.

Report:

- Overall feature-target correlation.
- Per-ticker feature-target correlation.
- Common-period feature-target correlation.

This helps avoid misleading pooled conclusions.

### Observations:

example:

Observation 1 — weak but useful signals

Feature-target correlations are expected to be weak for next-day returns, reflecting the noisy nature of daily financial prediction. Small relationships in lagged returns, rolling returns, volatility, or price_vs_ma20 may still be useful when combined in a multivariate model.

Observation 2 — up/down separation

Feature distributions for up days and down days should be compared to assess whether any variables separate the direction classes. If the distributions overlap heavily, individual features may have limited standalone predictive power.

Observation 3 — trend or mean-reversion behaviour

The relationship between price_vs_ma20 and target_direction can indicate whether assets show short-term momentum or mean-reversion. A higher up-day rate when price is above MA20 suggests momentum, while a higher up-day rate when price is below MA20 suggests rebound behaviour.

### Conclusion:

This step evaluates whether the engineered features contain predictive information about next-day returns or direction. If feature-target correlations are weak and up/down distributions overlap heavily, complex models may struggle to generalise. However, weak individual signals may still become useful when combined across multiple features and tickers. Results should be checked by ticker and over a common period because later IPO assets have shorter histories and may show less stable relationships.


## 10. Modelling readiness
* \[ ] Choose your modelling feature set
* \[ ] Choose your target variable
* \[ ] Decide whether to model all tickers together or separately
* \[ ] Decide train/test split date
* \[ ] Remove leakage columns
* \[ ] Confirm no future-looking features are used
* \[ ] Confirm target is only used as target, not input
* \[ ] Confirm features are available before prediction date

### Choose modelling feature set:
- select only features that would be known at prediction time.
- build a final set of usable input variables for modelling.

### Choose target variable:
- decide whether the model predicts target next day return or target direction.
- define whether the problem is regression or classification.

### Decide whether to model all tickers together or separately:
- compare pooled modelling vs ticker specific modelling.
- decide whether one model can learn across all assets or whether each ticker needs its own model.

### Decide train/test split date:
- choose chronological split, not a random split.
- preserve time series structure and avoid look ahead bias.

### Remove leakage columns:
- remove columns that reveal duture information or directly contain target information.
- ensure model performance is realistic.

### Confirm target is only used as target, not input:
- ensure target next day return or target direction is excluded from features.
- avoid direct target leakage.

### Confirm features are available before prediction date:
- validate that each feature would exist before the next day prediction is made.
- ensure the modelling setup matches a real trading / prediction scenario.

### Choosing the feature set:

Avoid using raw columns that may be less useful or create scale issues unless intentionally included.

suitable features may include:

| Feature type            | Example columns                                                         | Why useful                                             |
| ----------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------ |
| **Return features**     | `return_lag_1`, `return_lag_5`, `rolling_return_5`, `rolling_return_20` | Capture momentum or reversal                           |
| **Trend features**      | `ma20`, `ma50`, `price_vs_ma20`                                         | Capture price relative to trend                        |
| **Volatility features** | `rolling_volatility_20`, `rolling_volatility_60`                        | Capture recent risk conditions                         |
| **Volume features**     | `relative_volume`, `volume_ma20`                                        | Capture unusual trading activity                       |
| **Ticker identifier**   | `ticker` encoded as category                                            | Allows pooled model to learn ticker-specific behaviour |
| **Calendar features**   | month, quarter, day of week, year                                       | Capture seasonality or market timing effects           |

### Choosing target:

| Target                   | Modelling type | Meaning                                                   |
| ------------------------ | -------------- | --------------------------------------------------------- |
| `target_next_day_return` | Regression     | Predict tomorrow’s return magnitude                       |
| `target_direction`       | Classification | Predict whether tomorrow’s return is positive or negative |

Useful evaluation metrics for next day return:

| Metric               | Purpose                                                       |
| -------------------- | ------------------------------------------------------------- |
| MAE                  | Average prediction error                                      |
| RMSE                 | Penalises large errors                                        |
| R²                   | Measures explanatory power, but may be low for financial data |
| Directional accuracy | Checks whether predicted return sign is useful                |

Useful evaluation metrics for target direction:

| Metric           | Purpose                              |
| ---------------- | ------------------------------------ |
| Accuracy         | Overall correct direction rate       |
| Precision        | Reliability of predicted up days     |
| Recall           | Ability to capture actual up days    |
| F1-score         | Balance between precision and recall |
| ROC-AUC          | Ranking ability                      |
| Confusion matrix | Shows up/down classification errors  |


### Pool or separate tickers:

Pooled benefits:
- More training data.
- Model can learn shared patterns across assets.
- Useful if assets behave similarly.
- Later IPO assets still contribute whatever history they have.

Pooled risks:
- Some tickers may behave very differently.
- High-volatility assets may dominate.
- Later IPO assets have shorter histories.
- Ticker identity must be handled properly.

Separate benefits:
- Captures ticker-specific behaviour.
- Avoids forcing all assets into one pattern.
- Easier to interpret per asset.

Separate risks:
- Less training data per model.
- Later IPO assets may have too few observations.
- More models to evaluate and maintain.

Example practical approach:

I will first use a pooled model with ticker identifiers to maximise the training sample. Model performance will also be evaluated by ticker to check whether the pooled model works consistently across assets. If performance varies strongly by ticker, separate ticker-specific models may be considered.

### Example chronological train test split:

| Dataset section | Example period |
| --------------- | -------------- |
| Training set    | 2018–2023      |
| Validation set  | 2024           |
| Test set        | 2025–present   |

or

| Dataset section | Example split      |
| --------------- | ------------------ |
| Train           | First 70% of dates |
| Test            | Final 30% of dates |


### Important note on later IPO assets:

Should evaluate:
- Does every ticker have training data before the split date?
- Does every ticker have test data after the split date?
- Are later IPO assets only present in the test set?
- Are some tickers underrepresented in training?

Too little training data for a ticker:
- Move the split date later.
- Use a pooled model.
- Exclude that ticker from early modelling.
- Evaluate it separately.
- Use only the common period where all assets have data.

### Removing leakage columns:

| Column type                                                       | Why remove                                          |
| ----------------------------------------------------------------- | --------------------------------------------------- |
| `target_next_day_return` from features                            | Direct target leakage                               |
| `target_direction` from features                                  | Direct target leakage                               |
| Future returns                                                    | Uses unknown future data                            |
| Future price columns                                              | Not available at prediction time                    |
| Columns created using `shift(-1)`                                 | Future-looking                                      |
| Same-day close-to-close return if prediction is made before close | May not be available depending on prediction timing |
| Any post-event labels                                             | Not known at prediction time                        |

### Future looking features:

| Feature                  | Correct setup                            |
| ------------------------ | ---------------------------------------- |
| `return_lag_1`           | Uses return from `t-1`, not `t+1`        |
| `rolling_return_20`      | Uses data up to date `t` only            |
| `ma20`                   | Uses current and previous prices only    |
| `rolling_volatility_20`  | Uses previous/current returns only       |
| `relative_volume`        | Uses current/past volume only            |
| `target_next_day_return` | Uses future return but only as target    |
| `target_direction`       | Uses future direction but only as target |


### Confirm features available before prediction:

At the end of trading day t, use all available information up to day t to predict the return or direction for day t+1

| Feature                    | Available at end of day `t`? |
| -------------------------- | ---------------------------- |
| `adj_close_t`              | Yes                          |
| `volume_t`                 | Yes                          |
| `ma20_t`                   | Yes                          |
| `rolling_return_20_t`      | Yes                          |
| `return_lag_1_t`           | Yes, if shifted correctly    |
| `target_next_day_return_t` | No, target only              |
| `adj_close_t+1`            | No                           |
| `return_t+1`               | No                           |


### Suggested modelling readiness table checklist:

| Check                                 | Status   | Interpretation                                                                             |
| ------------------------------------- | -------- | ------------------------------------------------------------------------------------------ |
| Feature set selected                  | Complete | Inputs include lagged returns, rolling returns, volatility, trend, and volume features     |
| Target selected                       | Complete | `target_direction` used for classification or `target_next_day_return` used for regression |
| Time split selected                   | Complete | Chronological split used to avoid look-ahead bias                                          |
| Leakage columns removed               | Complete | Future-looking and target-derived columns excluded from `X`                                |
| Ticker history checked                | Complete | Later IPO assets checked for enough train/test rows                                        |
| Features available at prediction time | Complete | All features use only information known by date `t`                                        |
| Target missing rows removed           | Complete | Final rows per ticker dropped before modelling                                             |


### Suggesgted modelling dataset summary:

| Item               | Value                                                         |
| ------------------ | ------------------------------------------------------------- |
| Number of tickers  | 7                                                             |
| Date range         | 2018–present                                                  |
| Modelling approach | Pooled model with ticker identifier / separate models         |
| Target             | `target_direction` or `target_next_day_return`                |
| Feature groups     | Returns, rolling returns, moving averages, volatility, volume |
| Split method       | Chronological train/test split                                |
| Leakage handling   | Future-looking columns removed                                |
| IPO handling       | Later IPO assets retained from first valid trading date       |


### Observations:

example:

Observation 1 — time-series split

A chronological train/test split should be used instead of a random split because the dataset is time-series based. This ensures the model is trained on past data and evaluated on future data, matching the real prediction setting.

Observation 2 — leakage prevention

Target columns and any future-looking variables must be removed from the feature set. All features should be calculated using only information available on or before the prediction date to avoid look-ahead bias.

Observation 3 — pooled vs separate models

Since some assets IPO later and may have fewer observations, a pooled model with ticker identifiers can help maximise training data. However, performance should be reviewed by ticker to check whether the model generalises across all assets.

### Conclusion:

example:

The modelling readiness step confirms that the dataset is suitable for supervised learning. The final feature set should include only past and present information, while the target variable should be used only as the prediction output. Since the data is financial time-series data, the train/test split must be chronological rather than random. Because some assets IPO later, each ticker should be checked for sufficient training and testing observations. This step reduces the risk of look-ahead bias and ensures that the modelling setup reflects a realistic prediction scenario.


## 11. Key EDA outputs to save
* \[ ] Summary statistics table
* \[ ] Missing-values report
* \[ ] Correlation matrix
* \[ ] Risk/return table
* \[ ] Class balance table
* \[ ] Feature-target correlation table
* \[ ] 5–10 written insights
* \[ ] Modelling decisions section

### Summary statistics table:
- Counts, mean, std, min, max, quartiles for price, return, volume, volatility, and features.
- understand general scale, spread, outliers, and ticker differences.

| Variable group | Example columns                                         |
| -------------- | ------------------------------------------------------- |
| Price          | `adj_close`, `open`, `high`, `low`, `close`             |
| Volume         | `volume`, `relative_volume`                             |
| Returns        | `daily_return`, `rolling_return_5`, `rolling_return_20` |
| Risk           | `rolling_volatility_20`, `drawdown`                     |
| Trend          | `ma20`, `ma50`, `price_vs_ma20`                         |
| Target         | `target_next_day_return`                                |


### Missing-values report:
- missing values by column and by ticker.
- confirm whether missingness is epected especially for rolling features, target rows and later IPO assets.

| Source of missingness               | Expected? | Reason                                   |
| ----------------------------------- | --------- | ---------------------------------------- |
| Early moving averages               | Yes       | Rolling window needs enough history      |
| Early lagged returns                | Yes       | Lag features need previous observations  |
| Early rolling returns               | Yes       | Rolling window requirement               |
| Final target rows                   | Yes       | No future return available for final row |
| Pre-IPO dates                       | Yes       | Asset did not exist yet                  |
| Random missing prices in the middle | No        | Needs investigation                      |


### Correlation matrix:
- daily return correlation matrix across the 7 assets.
- identify asset relationships and diversification potential.

Should ideally save:
- Full available pairwise correlation matrix.
- Common-period correlation matrix where all 7 assets overlap.
- Optional high-volatility-period correlation matrix.

### Risk / return table:
- annualised return, annualised volatility, max drawdown, Sharpe-like ration, best and worst daily returns.
- compre assets by both reward and downside risk.

| Metric                 | Purpose                                 |
| ---------------------- | --------------------------------------- |
| Annualised return      | Measures average historical performance |
| Annualised volatility  | Measures return instability             |
| Max drawdown           | Measures worst peak-to-trough loss      |
| Best daily return      | Shows upside extremes                   |
| Worst daily return     | Shows downside extremes                 |
| Average daily return   | Shows central tendency                  |
| Sharpe-like ratio      | Compares return relative to volatility  |
| Start date             | Important for later IPO assets          |
| Number of observations | Shows reliability of estimates          |


### Class balance table:
- up/down counts and percentages for target direction, overall and by ticker.
- establish classification baseline and detect class imabalance.

| Level     | What to report                        |
| --------- | ------------------------------------- |
| Overall   | Total up/down days across all tickers |
| By ticker | Up/down percentage for each asset     |
| By period | Optional train/test class balance     |


### Feature target correlation table:
- correlations between engineered features and target next day return.
- identify which features show possible predictive signal.

| Feature group   | Example features                                 |
| --------------- | ------------------------------------------------ |
| Lagged returns  | `return_lag_1`, `return_lag_5`                   |
| Rolling returns | `rolling_return_5`, `rolling_return_20`          |
| Volatility      | `rolling_volatility_20`, `rolling_volatility_60` |
| Trend           | `price_vs_ma20`, `price_vs_ma50`                 |
| Volume          | `relative_volume`                                |


### 5-10 written insights:
- short written findings fro the full EDA.
- convert anlaysis into interpretable conclusions covering:
	- Data quality
	- Price behaviour
	- Risk
	- Correlation
	- Features
	- Targets
	- Modelling readiness

Example:

The dataset contains 7 assets with unequal histories.
Some assets IPO later, so their observations, rolling features, and target counts are lower than assets available since 2018.

Missing values are mostly expected.
Many missing values come from rolling-window calculations, lag features, final target rows, and later IPO start dates rather than random data errors.

Adjusted close should be used for return-based analysis.
This is more appropriate for modelling because it accounts for corporate actions such as splits and dividends.

Price behaviour differs across assets.
Normalised price charts show which assets had stronger relative growth and which experienced weaker or more volatile performance.

Risk varies meaningfully by ticker.
Rolling volatility and max drawdown show that some assets have much higher downside risk than others.

Correlations reveal diversification differences.
Some assets move closely together, while lower-correlation assets may offer better diversification benefits.

Feature values generally need validation before modelling.
Moving averages, relative volume, lagged returns, and rolling returns should be checked for sensible ranges, expected missingness, and outliers.

Next-day targets are likely noisy.
target_next_day_return is expected to be centred close to zero, making exact return prediction difficult.

Class balance defines the baseline model.
If up days are slightly more common than down days, the model must beat the majority-class benchmark.

A chronological split is required.
Random splitting would leak future market conditions into the training process, so train/test splitting must respect time order.

### Modelling decisions:
- final choices for features, target, split, pooled/separate model, leakage handling.
- justify the modelling setup before training.

| Decision             | Recommended choice                                                                    | Reason                                    |
| -------------------- | ------------------------------------------------------------------------------------- | ----------------------------------------- |
| **Target variable**  | `target_direction` or `target_next_day_return`                                        | Defines classification or regression task |
| **Feature set**      | Lagged returns, rolling returns, volatility, moving-average features, relative volume | Uses only past/current information        |
| **Model structure**  | Pooled model with ticker identifier as first approach                                 | Uses more data across all 7 assets        |
| **Ticker handling**  | Evaluate performance by ticker                                                        | Later IPO assets may behave differently   |
| **Train/test split** | Chronological split                                                                   | Prevents look-ahead bias                  |
| **Missing values**   | Drop rows with invalid rolling/target values after feature creation                   | Keeps model input valid                   |
| **Scaling**          | Fit scaler only on training set                                                       | Prevents data leakage                     |
| **Leakage removal**  | Exclude targets and future-looking columns from features                              | Ensures realistic modelling               |

### Output formats:

| Output                           | Suggested format                    |
| -------------------------------- | ----------------------------------- |
| Summary statistics table         | `.csv`                              |
| Missing-values report            | `.csv`                              |
| Correlation matrix               | `.csv` and heatmap `.png`           |
| Risk/return table                | `.csv`                              |
| Class balance table              | `.csv`                              |
| Feature-target correlation table | `.csv`                              |
| Key plots                        | `.png`                              |
| Written insights                 | `.md`, `.txt`, or notebook markdown |
| Modelling decisions              | `.md`, `.txt`, or notebook markdown |

### Output structure:

```
eda_outputs/
│
├── tables/
│   ├── summary_statistics.csv
│   ├── missing_values_report.csv
│   ├── correlation_matrix.csv
│   ├── risk_return_table.csv
│   ├── class_balance_table.csv
│   └── feature_target_correlation.csv
│
├── figures/
│   ├── adjusted_close_by_ticker.png
│   ├── normalized_prices.png
│   ├── rolling_volatility.png
│   ├── drawdown_plot.png
│   ├── correlation_heatmap.png
│   └── feature_distributions.png
│
└── notes/
    ├── eda_key_insights.md
    └── modelling_decisions.md
```

### Conclusion:

example:

The key EDA outputs summarise the main evidence needed before modelling. Summary statistics, missing-value checks, correlation analysis, risk/return metrics, class balance, and feature-target relationships provide a complete view of data quality, asset behaviour, target difficulty, and modelling suitability. Since some assets IPO later, all saved outputs should include ticker-level observation counts and start dates so that unequal histories are considered when interpreting results. These outputs justify the final modelling decisions and ensure that the modelling dataset is clean, interpretable, and leakage-free.

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

| Summary point                           | What to evaluate                                                                                | What to derive                                                         |
| --------------------------------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **1. What data I have**                 | Number of assets, date range, source, price/volume fields, engineered features, targets.        | Define the dataset scope clearly.                                      |
| **2. What quality issues I found**      | Missing values, duplicates, invalid prices, date gaps, shorter IPO histories.                   | Explain whether issues are expected or need fixing.                    |
| **3. Main return/risk patterns**        | Price trends, normalized returns, volatility, drawdowns, correlations.                          | Identify which assets look riskier, more volatile, or more correlated. |
| **4. Which features look useful**       | Moving averages, `price_vs_ma20`, relative volume, lagged returns, rolling returns, volatility. | Decide which features may contain useful modelling signal.             |
| **5. Which target I will model**        | `target_next_day_return` vs `target_direction`.                                                 | Choose regression or classification and justify it.                    |
| **6. How I will split train/test data** | Time-based split, ticker coverage, later IPO assets.                                            | Avoid leakage and preserve time-series structure.                      |
| **7. Limitations noticed**              | Noisy daily returns, unequal histories, Yahoo Finance limitations, market regime changes.       | State what may affect reliability or model performance.                |

## Example: EDA Summary

### 1. What data I have

The dataset contains seven financial assets pulled from Yahoo Finance, covering the period from 2018 to the most recent available date. The data includes daily market information such as open, high, low, close, adjusted close, and volume. The analysis mainly uses adjusted close prices because they account for corporate actions such as stock splits and dividends.

Some assets have shorter histories because they IPO later than 2018. Therefore, the dataset is an unbalanced panel, meaning not every ticker has observations for the full date range.

### 2. What quality issues I found

The main data quality checks focused on missing values, duplicate ticker-date rows, infinite values, invalid prices, date gaps, and whether each ticker had enough historical observations.

Some missing values are expected, especially at the beginning of rolling-window features, at the start of lagged features, and at the final row of each ticker where next-day target values cannot be calculated. Missing data before a ticker’s IPO date is also expected and should not be treated as an error.

Any unexpected missing prices, duplicate ticker-date rows, infinite values, or zero/negative prices should be removed or corrected before modelling.

### 3. Main return and risk patterns

The price behaviour analysis compared adjusted close prices and normalized prices across the seven assets. Normalized prices are useful because they allow assets with different price levels and IPO dates to be compared on a relative basis.

Risk analysis showed that assets may differ meaningfully in volatility and drawdown behaviour. Rolling volatility helps identify periods of high market uncertainty, while maximum drawdown shows the worst historical peak-to-trough loss for each asset. These metrics are important because an asset with strong returns may still carry high downside risk.

Correlation analysis using daily returns helps identify whether the assets move together or provide diversification benefits. Since some assets IPO later, correlation results should be interpreted carefully because different asset pairs may have different overlapping date ranges.

### 4. Which features look useful

The most useful modelling features are likely to be return-based, trend-based, volatility-based, and volume-based features. These include lagged returns, rolling returns, moving averages, `price_vs_ma20`, rolling volatility, and relative volume.

Moving averages and `price_vs_ma20` help capture trend and overextension. Lagged and rolling returns help capture possible momentum or reversal effects. Rolling volatility captures changing risk conditions, while relative volume may highlight unusual trading activity.

Feature values should be checked for sensible ranges, expected missing values, outliers, and possible leakage before modelling.

### 5. Which target I will model

The main target options are `target_next_day_return` and `target_direction`.

`target_next_day_return` is suitable for regression because it predicts the size of the next-day return. However, daily returns are usually noisy and centred close to zero, which may make accurate return prediction difficult.

`target_direction` is suitable for classification because it predicts whether the next day’s return will be positive or negative. This may be more practical for an initial modelling approach, but the model must be compared against a baseline such as always predicting the majority class.

Based on the EDA, `target_direction` is likely to be the more suitable first target for modelling, while `target_next_day_return` can be kept for additional regression experiments.

### 6. How I will split train/test data

The data should be split chronologically rather than randomly. This is important because financial data is time-series data, and random splitting could allow future market information to leak into the training process.

The training set should contain earlier dates, while the test set should contain later dates. If possible, a validation period should also be used between the training and test periods.

Because some assets IPO later, the split date should be checked carefully to ensure each ticker has enough observations in both the training and test sets. If a later IPO asset has limited training history, this should be considered when interpreting model performance.

### 7. Limitations noticed

The main limitation is that next-day financial returns are noisy and may have weak relationships with the engineered features. This means model performance may be limited, especially for regression.

Another limitation is that not all assets have the same history because some IPO later. This creates unequal observation counts and can affect summary statistics, correlations, risk comparisons, and model training.

The dataset is also based on Yahoo Finance data, so the analysis depends on the quality and completeness of that source. Market conditions also change over time, meaning patterns found in the historical data may not remain stable in the future.

Overall, the EDA suggests that the dataset is suitable for modelling if leakage is avoided, missing values are handled correctly, and model performance is evaluated using a time-aware train/test split.

