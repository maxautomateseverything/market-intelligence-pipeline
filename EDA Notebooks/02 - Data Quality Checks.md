# Data Quality Checks Report

This step aims to validate whether the data holds a suitable level of quality prior to modelling. 

The dataset contained 7 assets covering data from 2018 to present. Data quality checks were performed, inspecting:

- Missingness by column.

- Missingness by ticker.

- Duplicate date, ticker rows.

- Infinite values in numerical columns.

- Invalid (zero/negative) prices.

- Date gaps in data.

- Sufficient data per ticker.

- Target feature nulls.

The data **passed** all data quality checks with no unexpected instances.

## Missingness by Column:

Evidence suggests missingness is purely structural:

| Column                               | Missing Values | Interpretation                              |
| ------------------------------------ | -------------: | ------------------------------------------- |
| `moving_avg_50_no_calendar`          |            343 | `49 × 7` → first 49 rows missing per ticker |
| `moving_avg_20_no_calendar`          |            133 | `19 × 7` → first 19 rows missing per ticker |
| `rolling_30d_return_no_calendar`     |            210 | `30 × 7` → first 30 rows missing per ticker |
| `rolling_7d_return_no_calendar`      |             49 | `7 × 7` → first 7 rows missing per ticker   |
| `daily_return_no_calendar`           |              7 | first row missing per ticker                |
| `target_next_day_return_no_calendar` |              7 | last row missing per ticker                 |

This is further supported the 0 internal missing values and an even distribution of missingness in columns across tickers.

## Missingness by Ticker:

Missingness is evenly spread and not concentrated in one asset. All tickers ahve 186 missing values which is expected - supported by summing up the values in the Min or Max Missing per Ticker from Table 2 of the Notebook: `02 - Data Quality Checks.ipynb`.

## Duplicates:

There are 0 duplcaite ticker, date rows.

## Infinite Values:

There are no infinite values in any of the numerical columns.

## Zero/Negative Prices:

There are no invalid price values.

## Date Gaps per Ticker:

This notebook uses "no_calendar". Unlike "business_calendar", which accounts for weekends, and "market_calendar" which accounts for weekends and market holidays or closes, "no_calendar" takes account of nothing.

Therefore, we expect to see date gaps caused by weekends, holidays, etc.

SNDK nad RPI.L show a lower number of date gaps due to their later IPO status meaning the date range for the data of those assets is less and more recent, therefore, containing less holidays and weekends that contribute to the gaps.

## Sufficient Data:

Table 7 of the Notebook: `02 - Data Quality Checks.ipynb` shows that all assets have sufficient data relative to the longest window we define `config.py` - meaning all features can be calculated.

## Expected Nulls:

The final row of each ticker for the target features are all NaN or N/A as expected.