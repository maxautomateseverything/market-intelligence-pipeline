## Cleaning:

Our cleaning process has several steps:

(1) ```column_validation()```:
- Validates the column data types against a dictionayr of column and dtype pairs.
- Identifies missing columns from the approved list (```EXPECTED_DTYPES```) not in the df.
- Outputs a report of issues if there are any.
- Errors if data types are wring.

(2) ```data_validation()```:
- Converts date to datetime format.
- Ensures no dates earlier than predefined ```START_DATE``` are present.
- Ensures no rows with missing dates are present.
- Report on how many rows are dropped.

(3) ```drop_missing()```:
- Drops rows with poor data quality.
- Poor data quality defined as rows with missing data in any of the columns listed in ```NON_NULL_COLUMNS```

(4) ```drop_duplcaites()```:
- Drops duplicate rows defined by ```DUPLICATE_KEY_COLS``` column list.

(5) ```ticker_validation()```:
- Ensures tickers contained in df match expected tickers listed in ```TICKERS```
- Identifies missing adn extra tickers.

(6) ```sanity_check()```:
- Basic sanity check to ensure values are >0 or >=0 for the respective columns defined in ```NON_ZERO_COLS``` and ```ALLOW_ZEROS_COLS```.
- For example, price > 0 or volumne >= 0.

(7) ```ohlc_logic()```:
- Sanity check on open, high, low and close values.
- Implements the following checks:
```
high >= low
high >= open
high >= close
low <= open
low <= close
```

(8) ```time_series_sort()```:
- Sorts df by date in groups of tickers.

(9) ```insert_clean_prices()```:
- Inserts the cleaned df into the clean_prices table.

(10) ```reporting()```:
- Pulls reporting of the clean_prices table including:
    - Rows of each ticker.
    - Date range of each ticker.