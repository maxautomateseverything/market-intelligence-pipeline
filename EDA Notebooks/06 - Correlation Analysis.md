# Correlation Analysis Report

Correlation anlaysis evaluates how close our 7 assets move together based on daily returns. It helps in identifying whether assets provide meaningful diversification or whether several tickers share similar market behaviour.

We analyse correlation by:

- Creating daily return correlation matrices.

- Comparing asset relationships.

- Inspecting changes in correlations during high volatile periods.

- Identifying diversification patterns.

The correlation results show that the equity-related assets generally move together, with the closest relationships observed among SPY, MU, NKE and SNDK. TLT and GLD display the lowest average correlations and therefore provide the strongest historical diversification, although TLT’s relationships have become more positive since 2021. Correlations increased for several assets during the 2020–2021 volatile period, demonstrating that diversification can weaken when common market risks dominate, but this pattern was less evident during the more recent volatile period. Results for RPI.L and SNDK should be interpreted cautiously because their later IPO dates mean that their correlations are based on shorter and potentially less reliable samples.

## Creating Daily Return Correlation Matrices:

We have two forms of returns: log returns and simple returns. Simple returns are multiplicative while log returns are additive making them better for statistical analysis. Over single day time frames, the returns values are almost identical. Generally, it is better to use log returns unless interpreting actual investor gain or loss where simple returns are preferred.

Daily returns are seen in Matrix 1 and 2 of Notebook: `06 - Correlation Analysis.ipynb` and their absolute difference shown in Matrix 3 proving the negligible difference of the two returns over a daily time horizon.

We also consider later IPO assets in creating correlation matrices. In our data and often in reality, tickers don't all have the same number of values for various reasons: later IPO, missing price records, different trade calendars, etc. By default, pandas create pairwise observations meaning the matrix will compute each correlation value based on a number of different data points.

Matrix 4 shows overlapping pairwise datapoints across assets. RPI.L and SNDK have significantly less data points that the other assets since they IPO later.

Matrix 5 further inspects correlations by creating a correlation matrix from data points in which all assets share.


## Comparing Asset Relationships:

SNDK and MU show relatively strong positive correlation indicating possible within sector market effects. Interestingly, SPY and MU, as well as SPY and NKE have relatively strong positive correlations as well. We see weak positive correlations between NKE and MU, SNDK and SPY, TLT and GLD.

Other pairwise correlations indicate independent relationships with very very weak positive or no relationhip shown. Interestingly, TLT has pairwise correlations that lean more negative, except with GLD. It may indicate its ability as a diversification asset.

## Inspecting Changes in Correlations During High Volatile Periods:

We chose two periods of high volatility based on our previous analysis in `05 - Risk Analysis`: 2020-21 and 2025-present.

RPI.L and SNDK had yet to IPO in our first chosen period. In this specific high volatility period, we see less weak or no relationship correlations. Most correlations get stronger relative to the correlations seen across the whoe time horizon. SPY's correlations wiht MU and NKE which were relatively strong positive correlations sitting at roughly 0.61 and 0.59 respectively have increased to 0.78 and 0.79 during this period. The weak negative correlations pf TLT with other assets also got stronger.

In comparison, the more recent high volatility period does not show similar effects. Assets are shown to have equavilent correlations to that seen in the general correlation matrix.

## Identifying Diversification Patterns:

Table 1 shows the average correlation of each asset against all other assets.

GLD provides strong diversification benefits. Its overall average correlation is low at 0.117, and its annual correlations remain relatively small across the sample. The slightly negative correlation in 2019 and generally low values suggest that gold often behaves differently from the equity-related assets. However, its correlation rises to 0.204 in 2026, indicating that its diversification benefit may weaken in some periods.

TLT is the strongest historical diversifier, with an overall average correlation of −0.013. Its negative correlations between 2018 and 2021 indicate that long-term US government bonds often moved in the opposite direction to the other assets. This relationship changed after 2021, with correlations becoming positive from 2022 onward. Therefore, although TLT was an effective diversifier over the full period, its recent diversification benefit appears weaker.

SPY and MU have the highest overall average correlations, both at approximately 0.306. This suggests that they tend to move more closely with the rest of the portfolio and provide less diversification. SPY’s particularly high correlations in 2022 and 2026 indicate periods when the portfolio became more exposed to common market-wide movements. MU also shows consistently positive correlations, reflecting its sensitivity to broad equity and technology-sector conditions.

NKE provides moderate diversification. Its overall average correlation of 0.187 is lower than those of SPY and MU but higher than those of GLD and TLT. Its correlation increased sharply to 0.397 in 2022, suggesting that company-specific or consumer-sector differences provided less protection during that period.

RPI.L and SNDK should be interpreted cautiously because of their shorter histories. RPI.L only has observations from 2024 onward, while SNDK only has observations from 2025 onward. Their overall correlations of 0.097 and 0.281, respectively, are therefore based on fewer observations and may be less stable than estimates for assets with complete histories. RPI.L currently appears to offer diversification, whereas SNDK appears relatively correlated with the rest of the portfolio, but more data are required before drawing strong conclusions.

At the portfolio level, average correlations generally increased during 2020, 2022 and 2026. The broad increase in 2022 is particularly noticeable and suggests that diversification weakened when common economic and market factors affected several assets simultaneously. This demonstrates that assets with low average correlations over the full sample may still become more correlated during unusual or stressed market conditions.

Overall, TLT and GLD provide the strongest historical diversification, while SPY and MU contribute the greatest exposure to common market movements. NKE occupies a middle position, and conclusions concerning RPI.L and SNDK remain less reliable because of their limited return histories.

## Conclusion

The correlation analysis demonstrates that the seven assets do not respond uniformly to market movements and therefore provide varying levels of diversification. The equity-related assets generally exhibit the strongest positive relationships. In particular, MU and SNDK appear to share exposure to similar semiconductor and technology-sector factors, while SPY is moderately to strongly correlated with MU and NKE because of their sensitivity to broader equity-market conditions. These relationships suggest that combining these assets may provide less diversification than their individual company or sector classifications initially imply.

In contrast, TLT and GLD have historically provided the greatest diversification benefits. TLT has the lowest average correlation with the rest of the asset universe and recorded negative relationships with several assets during the earlier part of the sample. However, its correlations became more positive after 2021, indicating that the traditional diversification benefit of long-term government bonds has weakened in recent years. GLD also maintains a relatively low average correlation and generally behaves differently from the equity-related assets, although its diversification benefit is not constant and has weakened during certain periods.

The volatility-period analysis shows that correlations can change materially when markets become stressed. During the 2020–2021 high-volatility period, several equity correlations increased substantially. For example, SPY’s correlations with MU and NKE rose from approximately 0.61 and 0.59 over the broader sample to around 0.78 and 0.79. This indicates that assets with different company-specific exposures may still move together when broad market risk becomes dominant. The strengthening of some negative TLT relationships during this period also suggests that its diversification role was more effective during that particular episode. However, the 2025–present high-volatility period does not display the same widespread increase in correlations, showing that diversification breakdown is not identical across every period of market stress.

The annual average-correlation results reinforce the importance of examining relationships over time rather than relying solely on a full-sample matrix. Portfolio-wide correlations increased notably in 2020, 2022 and 2026, with the broad rise in 2022 providing especially strong evidence that common economic factors can cause otherwise distinct assets to move together. Consequently, a low long-term average correlation does not guarantee that an asset will continue to provide protection during the periods when diversification is most valuable.

The results for RPI.L and SNDK should be treated with additional caution because their later IPO dates produce shorter return histories. The full pairwise matrix uses all available overlapping observations for each asset pair, meaning individual correlations are calculated over different sample periods. The common-period matrix improves comparability by restricting the analysis to dates shared by all seven assets, but it also considerably reduces the amount of available data. RPI.L currently appears to have a relatively low correlation with the wider asset group, while SNDK appears more closely related to MU and the broader equity market. Nevertheless, these estimates are likely to be less stable than those for assets with longer histories.

Overall, the asset universe offers some meaningful diversification, but the benefits are uneven and time-varying. TLT and GLD are the strongest historical diversifiers, while SPY and MU provide the greatest exposure to common equity-market movements. NKE occupies a middle position, offering some company- and sector-specific diversification while remaining sensitive to the broader market. RPI.L may provide additional diversification, whereas SNDK is more likely to reinforce existing technology and equity exposure, although both conclusions remain provisional because of their limited histories. The analysis therefore supports using multiple correlation measures—including pairwise, common-period, annual and volatility-regime correlations—when evaluating portfolio diversification rather than relying on a single full-sample estimate.
