# Feature Analysis Report

Feature analysis checks whether the engineered variables are correctly calculated, iterpretable, and suitable for later modelling. Overall, this step helps confirm whether the features are sensible, whether missing values are expected, and whether scaling or outlier treatment is needed before modelling.

We perfrom feature analysis by:

- Generating a global validation layer.

- Plotting moving averages.

- Inspecting relative volume.

- Inspecting lagged-returns.

- Inspecting rolling returns.

- Inspecting feature distributions.

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