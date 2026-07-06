# Price Behaviour Report

Price behaviour analysis inspects how assets evolve over time. We aim to find differences between assets that may affect later analysis and modelling.

The dataset contained 7 assets, of which 2 IPO'd in the period between the start of  our dataset till present. We analysed price behaviour by:

- Plotting adjusted close over time by ticker.

- Comparing normalised prices, rebasing to 100.

- Inspecting major movements and unsual behaviour.


Overall, the analysis shows a clear split between stable long-term performers, volatile high-growth assets, and persistent underperformers. SPY and GLD display stronger long-term upward trends, while MU, SNDK and RPI.L show exceptional recent gains linked to speculative or sector-driven momentum, but with much higher volatility and drawdown risk. In contrast, NKE and TLT show sustained weakness, with NKE particularly standing out due to its prolonged decline and unrecovered drawdown. Therefore, while some assets offer strong upside potential, their risk profiles differ significantly, making drawdown and recovery behaviour essential for interpreting price performance beyond headline gains.

## Plotting Adjusted Close:

Plotting adjusted close aimed to identify long term trends of assets.

Graph 1 of the Notebook: `03 - Price Behaviour.ipynb` shows a consisntent and stable upward trend of SPY and GLD.

We see 3 assets (MU, SNDK, and RPI.L) with steep rises from the start of 2026 onwards likely related to trends in AI.

NKE has shown a consistent decrease in price since 2022.

## Comparing Normalised Prices:

We first rebased all tickers to 100 by their first available price date.

Graph 2 shows the relative changes have been hugely distorted by recent steep increases from  MU and SNDK. It may also have been distorted since SNDK and RPI.L had later IPO dates midway through the dataset.

Starting all tickers from a shared start date, we get Graph 3. This demonsttrates that the huge price increases from MU and SNDK still distort the analysis. They showed huge relative gains starting 09-2025 that accelerated starting 01-2026, especially from the likes of SNDK.

Removing the distorting assets (SNDK and MU) we derive Graph 4, giving a more representative insight into the remaining assets. NKE shows huge underperformance and a downward trend since 2022. TLT also shows a downward trend since 2021 while SPY shows a consistent upward trend despite experiencing cyclical crashes in 2020, 2022, 2025 and 2026. GLD an shown huge growth up till 2026 where its price has begun to fall at a rapid rate.

## Major Movements and Unusual Behaviour:

RPI.L, SNDK and MU demonstrated the highest weekly and daily gains (see Table 1 and 3) with RIP.L and MU experiencing these movements in 2026 and SNDK in 2025.

Surprisingly NKE comes fourth, but when further inspecting the date this is likely due to a bounceback post COVID.

Looking at the losses (see Table 2 and 4) we see RPI.L, SNDK and MU holding the top 3 positions in weekly loss and top 4 in daily. This indicates high volatility and risk as despite the high potential gains they also hold high potential losses.

NKE holds the second spot in daily losses after the release of Q4 fiscal results where revenue fell by **8%**.

What we can also conclude is that SPY, GLD and TLT are reltively 'safe' showing reltively equal and low gains and losses.

Table 5 looks at drawdown and further supports NKE poor performance and trend, having yet to recover.

The high volaility of MU, SNDK and RPI.L is further seen as they bounce back within the year despite their high drawdown values. SNDK is especially volatile demosntrating a higher rate of drawdown events as it has a high relative number of drawdown events despite having the most recent IPO (see Table 6).

MU has a very high average drawdown and abnormally high recovery rate, further supporting volatile performance.

RPI.L shows a relatively low recovery rate and high average drawdown suggesting poor previous performance prior to recent price boosts we have seen in other Graphs.




