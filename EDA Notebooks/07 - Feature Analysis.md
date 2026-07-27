# Feature Analysis Report

Feature analysis checks whether the engineered variables are correctly calculated, iterpretable, and suitable for later modelling. Overall, this step helps confirm whether the features are sensible, whether missing values are expected, and whether scaling or outlier treatment is needed before modelling.

We perfrom feature analysis by:

- Generating a global validation layer.

- Plotting moving averages.

- Inspecting relative volume.

- Inspecting lagged-returns.

- Inspecting rolling returns.

- Inspecting feature distributions.

Feature analysis found no material structural or calculation failures in the engineered variables. The features behave consistently with their definitions and capture distinct aspects of momentum, trading activity, volatility and drawdown. However, their distributions and scales vary materially across assets, with SNDK, RPI.L and MU showing the greatest instability and GLD, SPY and TLT appearing comparatively concentrated. Lagged returns provide little standalone predictive evidence, while several rolling-return and moving-average features contain overlapping information. Relative volume and rolling volatility are more distinct but behave differently across tickers. These findings support ticker-aware evaluation, chronological validation, selective feature reduction and training-only scaling or robust transformation where required.

## Global Validation:

This single validation check reduces duplicate work of checking structurally valid and correctly calculated values.

Table 1 of Notebook: `07 - Feature Analysis.ipynb` defines expected behaviour we expect to see from each of the features. We then go on to validate the actual behvaiour of the features against the expected behaviour of the features in Table 2, which indicates that all features have passed. We do this by calculating expected feature set independently and compare it with our actual feature set.

Table 3 for all features and tickers identifies leading NULLs, internal NULLs, trailing NULLs, infinite values, and extreme robust outliers. For some features, leading NULLs are expected because they shift the dataset down creating null values as ealier rows now have insufficeint data to be used for calculating the feature. Alternatively, we should expect no internal or trailing NULLs which is seen. We also expect and see no infinite values both at the positive and negative end of the scale that may have been caused by division by zero. Extreme robust observations count for each feature the number of extreme observations using the modified z-score. We use a high threshold because this is simply a validity check rather than a normal statistical outlier removal. This gives us insight into the number of rows that are deemed potentially unusual. Table 4 dives into these checks further at a ticker level.

Table 5 shows missing value percentage across features for each ticker. As expected earlier with the leading NULLs we expect to see some missing values for most engineered features. We see RPI.L and SNDK which higher missing proportions due to their later IPO. This is further supported by Graph 1 that shows the missingness through time.
 
When interpreting Table 8 we understand that predictions are only valid with no leakage when they are made at the end of the trading day when markets close and before the next day.

Overall, our engineered features show no issues.

## Inspecting Moving Averages:

Graph 1 and Table 10 confirm that the moving-average features behave largely as expected: MA20 follows adjusted close more closely, while MA50 is generally smoother and changes more slowly. GLD, SPY and TLT remain relatively close to their moving averages, whereas MU, RPI.L and especially SNDK show larger deviations during stronger price movements. 

Graph 2 supports this by showing that price_vs_ma20 usually fluctuates around zero but becomes persistently positive or negative during sustained trend regimes. Table 10 also shows no long unchanged runs, suggesting that the moving averages have not become incorrectly frozen. 

Crossover frequency differs substantially between assets, with NKE showing frequent reversals and RPI.L and SNDK showing fewer, more sustained regimes. However, Table 11 demonstrates that crossovers do not always coincide with price being above or below MA20 and that closely spaced reversals can represent whipsaw rather than a reliable trend change. 

Overall, the features appear valid and capture short- and medium-term momentum, but their usefulness varies according to asset volatility and market regime.

## Inspecting Relative Volume:

Graphs 4 and 5, together with Tables 12 and 13, indicate that the relative-volume feature behaves sensibly. 

Most observations are concentrated around 1, meaning daily volume is usually close to its recent average, while occasional large spikes create positively skewed distributions. This explains why every ticker has a median below 1 but a mean close to or slightly above 1 where a small number of unusually high-volume days pull the mean upwards.

RPI.L has the most extreme relative-volume behaviour, with 8% of observations above 2 and 4% above 3, while NKE records the largest maximum of 8.16 and the greatest skewness. By comparison, SPY has the least extreme distribution, with only 1.84% of observations above 2 and 0.09% above 3. Table 13 also shows that unusually high volume can accompany substantial price movements, such as GLD’s 10.27% fall on 30 January 2026, but not always: TLT recorded relative volume of 2.93 on 7 August 2019 despite an almost unchanged price. 

Relative volume therefore identifies unusual trading activity, but does not independently determine either the size or direction of the associated price movement.

## Inspecting Lagged Returns

Table 16 shows that nearly all Spearman correlations are close to zero, with only one correlation exceeding 0.1 in absolute value. This indicates little evidence of a consistent monotonic relationship between lagged returns and either current or next-day returns. The exception is SNDK, where the correlation between the lag-1 return and next-day return is −0.113, suggesting a weak short-term mean-reversion effect. In most cases, lag-5 correlations are smaller than lag-1 correlations, indicating that older returns generally contain less information about subsequent returns.

The quantile plots support the conclusion that lagged returns provide limited and inconsistent standalone predictive signal. SNDK shows a notable positive next-day median return following its lowest lag-1 returns, which may indicate a rebound after unusually negative days. However, the relationship is not consistent across all quantiles, so it should not be interpreted as strong or stable mean reversion. Most other tickers remain close to zero or show irregular, non-monotonic patterns. SNDK’s larger returns also stretch the shared y-axis and make smaller differences between the other tickers harder to see. Separate ticker plots and confidence intervals would help determine whether the apparent patterns are reliable.

## Inspecting Rolling Returns

Because the dataset uses a no-calendar structure, the rolling windows represent seven and 30 trading observations rather than seven and 30 calendar days.

Graph 8 shows clear differences in volatility and momentum persistence across assets. SPY, GLD and TLT have comparatively stable rolling returns, whereas MU, RPI.L and SNDK experience larger and less stable return regimes. Periods in which both horizons have the same sign indicate agreement between short- and medium-horizon momentum. A change in the sign of the 7-observation return while the 30-observation return retains its previous sign may indicate a short-term reversal within the broader trend.

The scatterplots in Graph 9 show broad directional agreement between the 7- and 30-observation returns. SPY, GLD and TLT form relatively compact upward-sloping distributions, while MU and NKE show greater dispersion. RPI.L and SNDK exhibit wider ranges and more extreme momentum regimes.

Table 19 confirms that the two rolling returns agree in direction approximately two-thirds of the time across all assets. SPY has the clearest persistent positive-momentum profile, with both returns positive in 49.4% of observations, while RPI.L has the highest proportion of jointly negative periods at 39.7%. SNDK is dominated by jointly positive returns at 61.6%, although its shorter and unusually bullish sample limits comparability. Because the 7-observation window is contained within the 30-observation window, some of this agreement is mechanically produced by overlapping data and should not be interpreted as independent predictive evidence.

## Checking Feature Distributions

Table 21 shows that feature asymmetry varies substantially across assets. RPI.L displays extreme positive skewness across its return features, while SPY shows pronounced negative skewness in drawdown, distance from the 20-observation moving average and rolling returns. Rolling volatility is strongly positively skewed for most assets, reflecting relatively normal volatility conditions interrupted by occasional spikes. The near-identical skewness of daily and lagged returns is expected because lagging changes the timing of the observations rather than their underlying distribution. These results indicate that several features are asymmetric or heavy-tailed and that extreme values should be checked against the original price data to distinguish genuine market events from data-quality problems.

The standard-deviation matrix in Table 22 confirms substantial differences in feature variability between assets. When comparing the same feature across tickers, SNDK, RPI.L and MU generally have the greatest return and momentum dispersion, while GLD, SPY and TLT have comparatively stable daily returns. SNDK is particularly dispersed in its rolling-return and moving-average-distance features, consistent with its short and unusually volatile trading history. The near-identical standard deviations of daily and lagged returns are again expected because lagging largely shifts the same return observations through time.

Table 23 shows that outlier frequency also varies considerably across assets and features. RPI.L has a particularly high concentration of outliers in rolling volatility, rolling returns and distance from the 20-observation moving average. GLD has a relatively high rolling-volatility outlier rate, while SPY has frequent daily-return outliers despite its lower overall return variability. However, outlier frequency measures how often observations exceed the IQR thresholds, not how severe those observations are. Zero or low IQR outlier rates should therefore not be interpreted as an absence of extreme market behaviour, especially for bounded, skewed or short-history distributions.

The boxplots and ECDFs reinforce these findings. SNDK, RPI.L and MU have the broadest return and momentum distributions, while GLD, SPY and TLT are more concentrated. SNDK has the highest typical rolling volatility and a strongly positive displacement from its 20-observation moving average, although its short and unusually bullish sample limits direct comparison. NKE and RPI.L show particularly broad drawdown distributions, while TLT demonstrates that relatively low daily volatility can still accumulate into persistent and substantial drawdowns. Differences become more pronounced over longer rolling horizons, with SNDK displaying an especially wide and right-shifted 30-observation return distribution. Because the ECDFs display only the 0.5th to 99.5th percentiles and the boxplot outlier markers are hidden, neither visualisation shows the full severity of the extreme tails.

Overall, the differences in scale, skewness and outlier behaviour support applying standardisation or robust scaling before using scale-sensitive models. Any transformation or scaler must be fitted using the training period only and then applied unchanged to validation and test data to prevent information leakage.

Tables 24 and 25, together with the correlation heatmaps, show substantial overlap among several price-derived features. Daily and log returns have identical rank ordering, indicating that they are redundant for rank-based analysis and are unlikely to provide meaningful additional information when used together. Rolling 7-observation return is strongly correlated with price relative to MA20, while rolling 30-observation return is strongly related to price relative to MA20 and moderately related to drawdown. These relationships are partly mechanical because the features are calculated from overlapping price observations.

The low ticker-to-ticker IQRs for these momentum relationships show that the overlap is relatively consistent across assets. In contrast, relative volume and rolling volatility have weak median correlations with most directional features, suggesting that they may contain more distinct information. However, their higher correlation IQRs show that relationships involving volume, volatility and drawdown vary materially between assets. These findings indicate feature redundancy and potential multicollinearity, particularly among the return, moving-average and rolling-momentum variables. Feature selection should therefore consider the model type, individual-ticker relationships and out-of-sample performance rather than relying on a single correlation threshold.

Table 26 shows that next-day returns are noisy and generally centred close to zero, although their dispersion differs substantially across assets. SNDK has the highest mean and standard deviation, but its shorter and unusually bullish sample limits comparability. RPI.L has a positive mean but a negative median because a small number of exceptionally large positive returns produce strong right skewness. GLD, SPY and TLT have considerably narrower target distributions, while TLT’s average next-day return is effectively zero. Because the target is the following observation’s return, its distribution appropriately resembles the daily-return distribution shifted forward by one trading observation.

Table 27 shows that the directional target is broadly balanced across tickers, with positive rates ranging from 47.5% to 57.0%. SNDK and SPY have modest positive-class majorities, whereas RPI.L has a slight negative-class majority. Severe class-imbalance treatment is therefore unnecessary. Nevertheless, classification performance should be compared with ticker-specific majority-class baselines and evaluated using chronological splits rather than random sampling.