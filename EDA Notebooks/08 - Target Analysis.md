# Target Analysis Report

Target analysis verifies that the prediction variables are correctly constructed and suitable for modelling. Our pipeline holds two target variables: target next day return, which captures the next trading day's return, and target direction, which converts next day return into a binary classification. This step aims to determine whether next day return prediction is realistic and what baseline models should be used.

Our target analysis consists of the following:

- Understanding target return distributions.

- Confirming target direction logic and evaluate up-down split.

- Comparing target behaviour across tickers.

Overall, the targets are suitable for further modelling experiments, but they present a difficult next-day prediction problem. Most tickers have next-day return distributions centred close to zero, although SNDK is a clear exception and RPI.L’s mean is strongly influenced by a large positive tail. Dispersion varies substantially across assets: SNDK, RPI.L and MU are the most volatile, while RPI.L, SPY and NKE show particularly heavy-tailed behaviour. The direction target is broadly balanced, with 52.25% up days and 47.75% down or unchanged days overall, giving a majority-class baseline accuracy of 52.25%. These results suggest a low signal-to-noise problem, but target unpredictability cannot be concluded from distributions alone and must be tested through feature relationships and time-based out-of-sample performance. Before modelling, the target shift, zero-return treatment, final missing labels and absence of leakage should be explicitly validated.

## Inspecting Target Next-Day Returns

Table 1 and Graph 1 show substantial differences in next-day return behaviour across the seven assets. GLD, SPY, NKE and TLT have means and medians close to zero, while MU has a modest positive centre. SNDK is a notable exception, with a mean return of 1.412% and median of 0.818%, indicating that its distribution is not centred as closely around zero as the other assets. RPI.L has a mean of 0.250% but a median of −0.103%, showing that large positive observations materially raise its average.

Dispersion differs considerably by ticker. SNDK has the highest standard deviation at 6.43%, followed by RPI.L at 4.74%, MU at 3.31% and NKE at 2.14%. The same ordering is broadly supported by the p1–p99 ranges. TLT, GLD and SPY have the tightest central distributions, with standard deviations close to 1%.

Extreme-value analysis produces a slightly different picture from standard deviation alone. RPI.L has the widest full return range and the largest positive return at 47.09%, while SNDK has the most negative return at −21.30%. RPI.L is also strongly positively skewed and has exceptionally high excess kurtosis, indicating that rare positive events have a major influence on its distribution. SPY and NKE also have high kurtosis despite lower overall volatility, showing that occasional severe movements occur even within otherwise narrower distributions.

The percentage of returns within ±0.5% ranges from 47.4% for GLD to only 9.9% for SNDK. Small daily movements are therefore common for GLD, SPY and TLT, but substantially less common for SNDK, RPI.L and MU. Overall, the target distributions combine small average movements, varying levels of dispersion and occasional extreme events. This is consistent with a difficult regression problem, although predictability cannot be determined from the target distribution alone.

## Inspecting Target Direction

Table 2 identifies two valid direction classes and seven missing target returns. The seven missing values are consistent with one final observation per ticker being unavailable after applying a one-period forward shift, but their positions and the corresponding direction labels should be verified explicitly.

There are 42 exact-zero target returns, representing 0.364% of valid observations. These are currently assigned to class 0. Consequently, class 0 represents down or unchanged days rather than strictly negative days. Because unchanged observations are rare, either excluding them or describing class 0 as non-positive would produce a clearer binary target definition.

The direction labels are broadly balanced. Across all tickers, 52.25% of valid observations are classified as up and 47.75% as down or unchanged. The resulting majority-class baseline is 52.25%, meaning that classification models should demonstrate meaningful improvement over an always-up prediction.

SNDK has the strongest upward class bias, with 56.98% up days, followed by SPY at 55.37%. GLD and MU have smaller upward biases, while TLT and NKE are almost evenly balanced. RPI.L has the strongest downward bias, although its majority class accounts for only 52.51% of observations. None of the tickers displays severe class imbalance.

## Target Behaviour by Ticker

Graph 1 provides a clear comparison of the central return distributions using a shared axis. SNDK has the widest distribution, followed by RPI.L, MU and NKE. TLT, GLD and SPY are much more concentrated around zero. However, the graph displays only the central return range and excludes several extreme observations reported in Table 1. It should therefore be interpreted alongside the minimum, maximum, percentile and kurtosis statistics.

SNDK has the most volatile target and strongest upward directional bias, but it also has the shortest usable sample at 344 observations. RPI.L has 518 observations and displays the strongest positive skewness, highest kurtosis and largest positive extreme. These shorter histories make their distributional statistics and potential model results less stable than those for the five assets with 2,133 valid observations.

A pooled model may benefit from the larger combined sample and common relationships across assets, but it should include ticker identity and be evaluated separately for every ticker. Robust regression metrics such as MAE should accompany RMSE because large errors from SNDK, RPI.L and MU could dominate pooled results. Ticker-specific models can also be tested, although the limited histories of SNDK and RPI.L may make separate estimates unreliable.

## Assessment of Target Noise and Modelling Implications

The small means relative to the daily dispersion of most assets, the broadly balanced direction labels and the presence of heavy tails suggest that exact next-day prediction may have a low signal-to-noise ratio. This is especially relevant for classification because very small positive and negative returns receive different labels despite being economically similar.

However, standard deviation and class balance do not prove that returns are random. Predictability should be assessed using feature-target relationships and chronological out-of-sample comparisons. Regression models should be compared with predictions of zero, the training-period mean and a rolling historical mean. Classification models should be compared with the 52.25% overall majority-class baseline and the relevant per-ticker baselines.

Longer-horizon targets, such as five-day returns, remain possible for all tickers, including SNDK and RPI.L. Their shorter histories reduce the available sample but do not prevent their construction. A longer horizon may improve signal strength, although overlapping future-return windows would introduce dependence between neighbouring observations. Next-day and longer-horizon targets should therefore be treated as alternative experiments and evaluated under the same time-based framework.