# Risk Analysis Report

Risk analysis evaluates the stability and vulnerability of each asset over time. This step aims to identify which assets carry higher downside risk, which assets experience more volatile regimes, and which assets may require careful treatment during modelling or portfolio analysis.

Our risk analysis comprises of two things:

- Rolling volatility analysis.

- Drawdown analysis.

Insepction of our data shows that high volatlity does not always produce the longest drawdown. RPI.: and SNDK experience sharp price swings, while TLT's main risk is prolonged capital impairment. This distinction is important - volatility measures short term instability while drawdown captures the depth and persistence of investor losses.

Risk is unevenly distributed across the seven assets. GLD and SPY show the lowest overall risk, combining relatively low volatility with shallower drawdowns and stronger recovery behaviour. TLT appears stable on a volatility basis but carries substantial duration risk, remaining below its previous peak for an extended period. In contrast, MU, SNDK, NKE and RPI.L present the greatest portfolio risk through higher volatility, deeper losses and more unstable recovery patterns. Overall, RPI.L and MU are likely to dominate volatility-based risk, NKE dominates downside risk, and TLT dominates prolonged drawdown risk.

## Rolling Volatility:

Graph 1 of the Notebook: `05 - Risk Analysis.ipynb` plots 30 day rolling volatility. 

More recent risk is concentrated in individual equities, which in this case points toward sector-specific events. RPI.L and SNDK show the highest volatility, reflecting IPO/spin-off instability and strong reactions to company news. MU remains structurally volatile due to the cyclical semiconductor sector, while NKE volatility is concentrated around earnings and guidance periods. In contrast, SPY, GLD and TLT remain comparatively stable, suggesting recent portfolio risk is driven more by stock-specific exposure than broad market instability.

Graph 1 also shows volatility spikes and clustering of all assets in the first half of 2020 and 2025. The first can be linked with macro shocks caused by COVID-19 while the latter can be attributed to weak consumer-confidence and economic data, combined with trade-policy uncertainty and pressure on highly valued technology stocks.

OVer time, earlier volatility is braodly distirbuted across assets while recently volaltity is increasingly oncetrated in technology and AI related equities.

## Drawdown Analysis:

Table 1 shows various statistics related to drawdown. SPY's largest decline occured during the 2020 market crash but recovered within 140 days, demonstrating strong resiliance. In constrast, TLT remains below its previous peak, with an open drawdown lasting apprximately 985 days, indicating prolong interest-rate sensitivity and the strongest persistence risk, supported by Table 2 and Graph 2.

Table 2 and Graph 2 shows equities having the greatest loss severity. NKE expereinced the largest peak to trough loss at -75.1% following by RPI.L (-66.4%) and MU (-57.6%). These represent the maximum losses an investor could have eperienced by buying at a previous peak and holding through the trough.

## Comparing Risk Across Assets:

As expected larger risk is seen from individual stocks compared to the more stable movements of commodities, bonds and indexes.

Inspecting the chosen stocks further, we see increasing risk from 2025 onwards whcih can be linked to higher price movements from AI-related tech stocks.

Diving into indivudal assets:

GLD demonstrates low rolling volatility and the lowest max drawdown of -26.2% making it the asset with the lowest overall risk.

SPY has low volatility and the second lowest max drawdown (-33.7%). Its ability to recover from its 2020 trough in 140 days indicates strong recovery behaviour but higher drawdown potential indicates slightly higher risk.

TLT shows low volaitlity but its inability to recover for is previous peak taking 985 days and counting indcates it moderately high risk.

SNDK has extremely high volatility and relatively high max drawdown. It recovered in 135 days, but due to its short and unstable trading history it can only be concluded as a high risk asset.

MU shows consistently high volatility and a high  drawdown. Its ability to recover in 161 days indicates potential strong recovery potential but previous recoveries have laste up to 700 days making this asset very risky.

NKE has shows moderately high volatility, but its inability torecover from its deepest loss of -75.1% makes it a very high risk asset.

RPI.L shows extreme volaitlity and compartively high max drawdown making it the riskiest asset when combining the two measures.

## Conclusion:

GLD and SPY present the lowest combined risk, with relatively low volatility and shallower drawdowns. TLT appears stable under volatility measures but carries significant duration risk, remaining below its previous peak for almost 1,000 days.

MU, SNDK and RPI.L are likely to dominate volatility-based portfolio or model risk because of their large and persistent price movements. NKE dominates downside-loss risk due to its −75.1% maximum drawdown, while TLT dominates recovery-duration risk.

Overall, RPI.L is the highest composite-risk asset, combining extreme volatility, a deep drawdown and a short trading history. The ranking may change depending on whether the model gives greater weight to volatility, drawdown depth or recovery time.