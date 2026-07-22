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
