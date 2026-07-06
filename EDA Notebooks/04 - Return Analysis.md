# Return Analysis Report

Return analysis aims to identify periods of market stress, ticker specific shocks and differences in risk-return behvaiour across assets.

We evaluate asset performance through:

- Plotting Daily Returns.

- Plotting Return Distributions.

- Comparing Average Returns, Volatility, and Extreme Return Days.

- Inspecting Skewness and Kurtosis.

The return analysis shows that risk differs far more clearly than average return across the assets. While SNDK, RPI.L and MU show the strongest headline returns, these returns are accompanied by high volatility, short sample effects, and extreme outlier risk. SPY and GLD provide more stable profiles, although both still show evidence of tail risk during stress periods. NKE and TLT appear weakest on a risk-reward basis over this sample. Overall, the results confirm that asset returns are fat-tailed, regime-dependent and affected by volatility clustering, meaning future modelling should account for skewness, kurtosis, drawdowns and unequal data histories rather than relying only on average returns.

## Daily Returns:

Daily return plots show all assets, as expected, fluctuate round 0. However, the size and frequency of return swings differ greatly across assets.

Extremely large positive and negative returns can indicate high volatility. For assets holding data all from 2018 onwards (i.e., excl. IPO assets: SNDK, RPI.L) we see huge volatility clustering in 2020 relating to COVID-19.

Still  present, but less obvious, volatility clustering is seen between 2022 and 2023 where that extended period experiences wider fluctuation comapres with calmer periods before (2021-22) and after (2023-24). This behaviour is especially evident in SPY and TLT.

Plotted daily returns can be seen in the Notebook: `04 - Return Analysis.ipynb`

Graph 1 (GLD): Apart from the volaitlity clustering seen in 2020, GLD has experienced a huge spike in volatility in 2026.

Graph 2 (MU): While already a volatile asset, MU has experienced an increase in volatility in 2025 and 2026 suggesting an increase in risk return profile.

Graph 3 (NKE): NKE returns are relatively stable with occassional extreme sginle day movements. This likely reflects firm-specific news or earnings.

Graph 4 (RPI.L): Having IPO'd in mid-2024, TPI.L demonstrates extreme volatilty in 2026. Notably, it has extremely large upspikes indicating less stable returns and greater exposure to recent idiosyncratic shocks.

Graph 5 (SNDK): SNDK IPO'd even later in 2025. Sicne IPO it shows extreme volatility. This may be due to the initial volatility from IPO as well as recent idiosyncratic shocks.

Graph 6 (SPY): Mostly stable returns and best demonstrates market shocks and locations of volatility clustering that we see in other graphs. We see varying levels of volatility clustering in 2018, 2019, 2020, 2022, and 2025.

Graph 7 (TLT): Most returns are close to 0, but a major volatility cluster occurs in 2020 with sharp positive and negative moves. Volatility also remains elevated in 2022-23 reflecting sensitivity to interest-rate conditions which is expected.

## Return Distributions:

Return distributions further support the insights derived from inspecting daily returns plots.

We aim to compare x-axis spread and almost disregard the height of the bars as y-axis differs and sample size differs due to later IPO assets.

Plotted return distributions can be seen in the Notebook: `04 - Return Analysis.ipynb`

Graph 8 (GLD): Fairly normal distribution wiht some extreme returns at -10% and +6% which we can link to the extreme volatility seen in 2026.

Graph 9 (MU): Much wider distribution from -20% to +20% demonstrating higher volatility.

Graph 10 (NKE): Another wide distribution with tails at -20% and +15%.

Graph 11 (RPI.L): RPI.: is notable as its visual plot is shifted left showing very large positive of up to 45% compared to negatives. The right tail is very large so normal mean/standard deviation assumptions can be misleading.

Graph 12 (SNDK): Fewer observaions and a wider, somewhat right skewed profile with long tails.

Graph 13 (SPY): Tightly centred around 0 with most returns close to zero and a few outliers. Demonstrates the diversified market exposire expected from an index, but existing sensitivity to makret crashes seen at tails.

Graph 14 (TLT): Very narrow core extending form -6% to +8%. Bonds, especially long-duration ones, can be volatile as they are sensitive to interest rate chocks, inflation expectations and FED policy.

The distributionss are not clean normal bell curves. Distirbutiosn show fat tails, some skewness, and outliers. This means that risk models based on only average return and standard deviation may understate the chance of extreme moves.

## Average Returns, Volatility, and Extreme Returns:

While average returns are often small and noisy, we see clear higher returns from the likes of SNDK (1.41%), RPI.L (0.25%) and MU (0.21%) in Table 1, however, they also hold the highest level of volatility.

Drilling further, it seems SNDK is the only asset to provide a better return to risk ratio, as RPI.L and MU offer similar levels of risk returns as SPY, GLD and NKE. However, that could likely be due to shorter history (338 observations vs 2133) and recent exposure to positive idiosyncratic shocks.

Among longer history assets, MU has the best return to risk, while GLD and SPY are steader lower risk options. NKE and TLT are extremely weak likely reflecting their decreasing prices and poor recovery ability from drawdowns.

RPI.L has good headline return, but demosntrates obvious outlier risk. A 47.09% largest daily gain is huge suggesting the mean return could be materially influenced by a small number of extreme positive days, espcially in a small sample size.

## Extreme Return Days:

Largest daily gains (Table 2) shows RPI.L and SNDK being heavily outlier driven, even MU has large event risk as they demonstrate occasional explosive moves. Similar assets have equally severe downside (Table 3).

Notably, GLD an often considered defensive asset has had a sharp drawdown (-10.27%) in 2026. 

From weekly gains and losses in Table 3 and 4 SNDK, MU, RPI.L and NKE show the most extreme weekly pricing risk.

Turning to the same data sorted in order of date in Table 6 to 9, we are able to see market wide and firm specific driven swings.

We see many extreme moves round 2026 high volatility. It is clear recent news has affected the AI indsutry as SNDK, MU and RPI.L are all expecriecing greater volatility - although possibly skewed by less past data.

Another cluseter occurs round April 2025. SNDK, MU, NKE and SPY experienced major losses but SPY, MU and NKE showed sharp rebounds after.

March 2020 shows another high volatility cluster with very high gains and losses from all assets who were in the market then.

SNDK still has the best headline return-to-risk, but its -38.51% worst week makes it highly speculative. MU looks like the more credible high-risk performer. GLD and SPY remain the cleaner lower-risk options. RPI.L is interesting but very outlier-driven. NKE and TLT still look unattractive in this sample.

## Skewness and Kurtosis:

Positive skewness indicates more extreme positive returns, seen by the likes of TLT, MU, SNDK and notably RPI.L with a very large skewness of +3.27 confirming that RPI.L's average return is likley being pulled upward bya  few huge positive days.

Negative skewness indicates the asset has more negative returns seen only slightly by GLD, NKE, and SPY. GLD's slight negative skew but low volatility indicate it is being drandown by a few large daily losses, ,as supported by earlier tables. NKE is demonstrated as extremely unattractive as it has a wek mean and ngative skew.

Kurtosis shows how muhc of the distribution is demonstrated by relative extremes. Where a normal distribution has a kurtosis of 0, these assets show extreme movements occuring more often than a normal distirbution would expect.

So a simple mean/volatility analysis is not enough. You need tail-risk metrics like VaR, CVaR, drawdown and stress-period performance.

## Conclusion:

The return analysis shows that average daily return alone is a weak and potentially misleading measure of performance. Across all seven assets, returns are generally centred around zero, but the degree of volatility, tail risk, skewness, and sensitivity to market shocks differs substantially by ticker. This means that assets should not be judged simply by which had the highest average return; they must also be assessed by how unstable those returns were and whether the returns were driven by repeatable performance or by a small number of extreme events.

The clearest finding is that SNDK, RPI.L and MU offer the highest headline returns, but they also carry the greatest risk. SNDK has the strongest return-to-risk ratio, but this result should be treated with caution because it is based on a much shorter post-IPO sample and includes very large price swings. RPI.L is even more clearly outlier-driven, with very high positive skewness and extreme kurtosis, suggesting that its average return is heavily influenced by a few unusually large upside moves rather than stable daily performance. MU appears to be the most credible high-risk performer among the assets with a longer history, but its large daily and weekly losses show that it still carries significant downside risk.

By contrast, SPY and GLD provide more stable return profiles. Their average daily returns are lower, but their volatility is also much lower than the single-stock and recent IPO names. SPY behaves as expected for a diversified equity benchmark: mostly stable, but still exposed to major market-wide shocks such as March 2020. GLD also appears relatively stable overall, but its negative skewness and sharp 2026 loss show that it should not be treated as risk-free or purely defensive. TLT has the lowest volatility, but its near-zero or slightly negative average return makes its risk-reward profile weak over this period, while NKE is unattractive because it combines low average return with meaningful volatility, negative skewness, and large downside events.

Overall, the analysis demonstrates that these assets have fat-tailed, non-normal return distributions. Extreme return days are not random noise; they are central to understanding risk. Volatility clustering in 2020, elevated movement in 2022–2023, and renewed extreme moves in 2025–2026 show that risk changes over time and often concentrates around market stress or ticker-specific events. Therefore, any future modelling or portfolio comparison should account for unequal sample lengths, later IPO effects, volatility clustering, skewness, kurtosis, and extreme drawdowns. A common-period comparison and additional downside-risk measures such as maximum drawdown, VaR and CVaR would provide a fairer and more robust assessment than mean return and volatility alone.