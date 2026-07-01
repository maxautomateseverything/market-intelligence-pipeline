# Market Data Pipeline + Forecasting System.

Title: Automated Market Intelligence Pipeline with Forecasting and Financial Dashboard.

Core Stack: python (main language), pandas (data cleaning), yfinance (data source), 
		duckdb (local database), sql (analysis), scikit-learn (modeling), 
		streamlit (dashboard), prefect (orchastration).

1. Project Summary:

Build something that:
	(1) Pulls stock market data from  a free source (yfinance).
	(2) Stores the data in a local analytical database (duckdb).
	(3) Cleans the validates the data (pandas).
	(4) Creates financial features.
	(5) Builds simple forecasting/trading signal models (scikit-learn)
	(6) Displays results in an interactive dashboard (streamlit).
	(7) Runs as a repeatable pipeline (prefect)

2. Role-Project Alignment:
	- Data Engineering: APIs, pipelines, storage, orchestration.
	- Data Analysis: KPIs, SQL, trends, dashboarding.
	- Data Science: feature engineering, forecasting, model evaluation.
	- Financial Analysis: returns, volatility, drawdowns, signals.

3. Checkpoints:
	(1) MVP:
		A dashboard that shows price history, daily returns, cumulative returns,
		volatility, moving averages, simple buy/sell signals, forecast vs actual price.
	(2) Portfolio Ready:
		Build a full local pipeline: market API -> raw data table -> cleaned price table
		-> feature table -> model predictions table -> streamlit dashboard.
	(3) Advanced Extension:
		Add multiple tickers, portfolio comparison, data quality checks, 
		pipeline scheduling, model evaluation tracking, README with architecture diagram.

4. Chosen Assets:

TICKERS = ["SPY", "GLD", "TLT", "SNDK", "MU", "RPI.L", "NKE"]

Aim to gain exposure to ETFs / Market, Commodity, Bonds and a few personal individual stock choices.

5. Learning Objectives:

Data Engineering:
- How API ingestion works.
- How to structure raw vs cleaned data.
- Why pipelines should be repeatable.
- How to log pipeline runs.
- Why data quality matters.

Data Analysis:
- How to calculate financial KPIs.
- How to write SQL queries over analytical data.
- How to build dashboards for decision-making.
- How to tell a story from market data.

Data Science:
- Why time series modelling is different.
- Why random train/test splits are wrong for time-series data.
- How to create lag features and rolling statistics.
- How to evaluate forecasts properly.
- How to use TimeSeriesSplit, which is designed so models train on past data and
	test on future data rather than leaking future information.

Financial Analysis:
- Daily returns.
- Cumulative returns.
- Volatility.
- Moving averages.
- Drawdown.
- Sharpe ratio.
- Basic signal generation.

6. Project Phases:

(1) Ingest Market Data: download historical market data for selected tickers.
	- src/ingest.py:
		- accepts a list of tickers.
		- download data from yfinance.
		- save raw data.
		- add metadata columns.
	- key concept: raw data should be saved before transformation for future debugging.
	- success criteria:
		- data/raw/prices_raw.csv
		- contains: date, open, high, low, close, volume, ticker, downlowded_at

(2) Store Data in DuckDB: move data from CSV into a DB.
	- why DuckDB:
		- lightweight and local, SQL friendly DB that works well with python.
		- easily installed using pip.
		- supports common file workflows like CSV and Paraquet.
	- tables to create:
		- raw_prices
		- clean_prices
		- price_features
		- model_predictions
		- piepline_runs
	- src/database.py:
		- create_tables() function
		- insert_raw_prices(df) function
		- read_table() function
	- checkpoint:
		- able to connect to DB ```con = duckdb.connect("data/market.duckdb")```
		- query data using SQL ```con.sql("SELECT ticker, COUNT(*) 
							FROM raw_prices 
							GROUP BY ticker"). show()```

(3) Clean and Transform Data: turn raw data into reliable analysis ready data.
	- src/transform.py handles:
		- type validation
		- rows with missing values
		- duplicate rows
		- date validation 
		- sanity check (e.g., price > 0)
		- OHLC logic checks (e.g., high >= low)
		- ticker validation 
		- sorting/order by ticker/date.
		- row count reporting by ticker *
		- date range reporting by ticker *
	- flow into clean_prices table:
		- date - trading date.
		- ticker - asset symbol.
		- open - opening price.
		- high - high price.
		- low - low price.
		- close - closing price.
		- adjusted_close - adjusted closing price.
		- volume - trading volume.
	- checkpoint:
		- should be able to answer ``` SELECT 
						    ticker,
						    MIN(date) AS first_date,
						    MAX(date) AS last_date,
						    COUNT(*) AS rows
						FROM clean_prices
						GROUP BY ticker;```
	- success criteria: no bad data quality, e.g., duplicate ticker-date pairs.

(4) Feature Engineering: create financial features used in analysis and modelling.
	- src/features.py creates required features:
		- daily_return (%)
		- log_return
		- rolling_7d_return *
		- rolling_30d_return *
		- rolling_30d_volatility *
		- moving_avg_20 *
		- moving_avg_50 *
		- price_vs_ma20 *
		- target_next_day_return * (prediction)
	- some rows become invalid after creating features and should be dropped, e.g., first 29 days for 30 day volatility.
	- price_features table should contain date, ticker, all original clean price data and all the features.
	- success criteria: being able to explain every feature in plain English.

(5) EDA: understand the data before modelling.
	- notebooks/01_exploration.ipynb should answer:
		- which asset had highest total return?
		- which asset had the highest volatility?
		- which asset had the largest drawdown?
		- how did assets behave during downturns?
		- are returns normally distributed?
		- do moving average signals look useful?
	- required charts:
		- price over time.
		- cumulative return.
		- rolling volatility.
		- drawdown.
		- correlation heatmap.
		- distribution of returns,
	- checkpoint: write 5- insights in markdown, e.g., QQQ had higher returns than 
		SPY over the period, but also experienced larger drawdowns and higher volatility.

(6) Baseline Forecasting Model: predict next day returns or next-day direction rather than exact prices.
	- prediction targets:
		- target_next_day_return, or
		- target_direction if next_day_return > 0
	- models to build in src/model.py:
		- naïve baseline (regression): today = tomorrow.
		- linear regression (regression): simple, explainable.
		- random forest (regression/classification): captures non-linear relationships.
		- logistic regression (classification): predicts direction.
		- dummy/classifier (classification baseline): check if models add value.
	- important not to randomly shuffle time-series data, we should use chronological splits
		or TimeSeriesSplit.
	- evaluation metrics:
		- for return prediction: MAE, RMSE, R^2.
		- for direction prediction: accuracy, precision, recall, confusion matrix.
	- model_predictions table:
		- should have columns: model, ticker, followed by the evaluation metrics.
	- success criteria: honest comparison of models against baselines.

(7) Create Trading Signals: convert analysis / model outputs into simple decision-support signals.
	- signals to create:
		- moving average signal: buy when MA20 > ma50.
		- momentum signal: buy when 30d return >0
		- model signal: buy when predicted return > 0
		- risk-off signal: avoid when volatility is high.
	- model_predictions table:
		- contains date, ticker, predicted_return, predicted_direction and signal.
	- checkpoint: explain when
		- why a signal fired.
		- whether it worked historically.
		- where it failed.

(8) Backtest Simple Strategy: evaluate signals historically.
	- strategies to compare:
		- buy and hold SPY.
		- moving average strategy.
		- momentum strategy.
		- model-based strategy.
	- metrics:
		- total return.
		- annualised return.
		- annualised volatility.
		- sharpe ratio (risk adjusted returns).
		- max drawdown (worst peak to trough loss).
	- strategy_comparison table:
		- table contains strategy, and the metrics.
	- success criteria: do not cherry pick only the winning strategy but also where the model fails.

(9) Build Streamlit Dashboard: create user facing product.
	- add/dashboard.py:
		- page 1 market overview.
		- page 2 asset comparison.
		- page 3 forecasting.
		- page 4 strategy backtest.
	- success criteria: recruiter can understand the project in 2 minutes.

