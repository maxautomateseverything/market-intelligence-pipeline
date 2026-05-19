import duckdb
import pandas as pd

from src.database import read_table
from src.config import (EXPECTED_DTYPES, TICKERS, NON_NULL_COLS, DUPLICATE_KEY_COLS, 
                        NON_ZERO_COLS, ALLOW_ZERO_COLS, TICKER_COL, DATE_COL, 
                        EARLIEST_FIRST, START_DATE, DATABASE_PATH)

# Checks data type of columns, erorring out otherwise.
def column_validation (df: pd.DataFrame, expected_dtypes: dict) -> None:
    
    print("\n   [START] DTYPE CHECK")

    results = []

    for column, expected_dtype in expected_dtypes.items():

        if column not in df.columns:
            results.append({
                "column": column,
                "expected_dtype": expected_dtype,
                "actual_dtype": None,
                "valid": False,
                "issue": "data has missing column"
            })
            continue

        actual_dtype = str(df[column].dtype)

        if actual_dtype == expected_dtype:
            valid = True
            issue = None
        else:
            valid = False
            issue = "wrong dtype"

        results.append({
            "column": column,
            "expected_dtype": expected_dtype,
            "actual_dtype": actual_dtype,
            "valid": valid,
            "issue": issue
        })

    report = pd.DataFrame(results)

    print("\n")
    print(report)

    invalid_columns = report[report["valid"] == False]

    if not invalid_columns.empty:
        raise TypeError(f"[ERROR] Invalid column data types:\n{invalid_columns}")
    else:
        print("\n   [DONE] Finished dtype check - no issues")

# Date check, dropping invalid dates
def date_validation (df: pd.DataFrame, start_date_string: str, ) -> pd.DataFrame:

    print("\n   [START] DATE VALIDATION")

    # Convert the start date string to a datetime dtype.
    start_date = pd.to_datetime(start_date_string)

    raw_df = df.copy()

    original_row_count = len(raw_df)
    print(f"[INFO] Original rows {original_row_count}")

    # Convert date column to datetime.
    # Invalid values that cannot be converted to dates become NaT.
    raw_df["date"] = pd.to_datetime(raw_df["date"], errors="coerce")

    # Assigns rows where date is before start date to invalid rows.
    invalid_rows = raw_df[raw_df["date"] < start_date]

    if invalid_rows.empty:
        print("[INFO] No dates before start date")
    else:
        print(f"[INFO] Rows are before the start date {len(invalid_rows)} ")

    # Drop NaT rows and rows before start date.
    cleaned_df = raw_df[raw_df["date"] >= start_date].copy()

    rows_dropped = original_row_count - len(cleaned_df)

    print(f"[INFO] NaT rows dropped: {rows_dropped - len(invalid_rows)}")

    print(f"[INFO] Total rows dropped: {rows_dropped}")

    print(f"[INFO] Valid rows {len(cleaned_df)}")

    print(cleaned_df.head())

    return cleaned_df

# Drop rows with missing values (None, NaN, or empty strings)
def drop_missing (df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    
    raw_df = df.copy()
    
    print("\n   [START] DROPPING NULLS")
    
    # Get number of rows in original dataframe.
    original_row_count = len(raw_df)
    print(f"[INFO] Original rows {original_row_count}")

    # Row by row check for NaN or None.
    # .notna() returns True or False depending on missing or not.
    # .all() checks whether all values are True.
    # axis=1 means cehck across each row.
    not_missing = raw_df[columns].notna().all(axis=1)

    # Check for empty strings.
    # .apply() runs a function on each selected column
    not_blank = raw_df[columns].apply(
        # lambda is a short unamed function
        # means for each column run col.map()
        # .map() runs a function on each individual value in the column.
        lambda col: col.map(
            # Returns False for blank or empty strings.
            # isinstance(value, str) checks if is string value or not allowing
            # number to be passed through.
            lambda value: not isinstance(value, str) or value.strip() != ""
        )
    ).all(axis=1)

    # Combines the missing value and blank string checks.
    # The & means AND for pandas boolean series meaning a row is only
    # kept if both are True.
    mask = not_missing & not_blank

    # Keep rows from oroginal dataframe where mask is True.
    # Make separate copy of the dataframe.
    cleaned_df = raw_df[mask].copy()
    
    rows_dropped = original_row_count - len(cleaned_df)
    print(f"[INFO] Rows dropped {rows_dropped}")

    print(f"[INFO] Non-null rows {len(cleaned_df)}")

    print(cleaned_df.head())

    return cleaned_df

# Drop duplicate (ticker, date) rows keeping the row with a more recent downloaded_at value.
def drop_duplicates (df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:

    raw_df = df.copy()
    
    print("\n   [START] DROPPING DUPLICATES")

    original_row_count = len(raw_df)
    print(f"[INFO] Raw rows {original_row_count}")

    raw_df["downloaded_at"] = pd.to_datetime(
    raw_df["downloaded_at"],
    errors="coerce"
    )

    # Sorts by downloaded at in descening order - puts more recent at top.
    # Drops duplciate rows keeping first instance (most recent)
    cleaned_df = (raw_df. sort_values("downloaded_at", ascending=False)
                  .drop_duplicates(subset=columns, keep="first")
                  .copy()
                  )

    rows_dropped = original_row_count - len(cleaned_df)

    print(f"[INFO] Rows dropped {rows_dropped}")

    print(f"[INFO] Duplicate rows {len(cleaned_df)}")

    print(cleaned_df.head())

    return cleaned_df

def ticker_validation (df: pd.DataFrame, expected_tickers: list[str]) -> pd.DataFrame:
    
    print("\n   [START] TICKER VALIDATION")

    raw_df = df.copy()

    original_row_count = len(raw_df)
    print(f"[INFO] Original rows {original_row_count}")

    # Creating sets using Set() creates a set of unique values.
    actual_tickers_set = set(raw_df["ticker"].dropna().unique())

    # Converts ticker list into set.
    expected_tickers_set = set(expected_tickers)

    # Using sorted() sorts them.
    missing_tickers = sorted(expected_tickers_set - actual_tickers_set)

    if missing_tickers:
        raise (f"[WARNING] Expected tickers missing from data: {missing_tickers}")
    else:
        print("[INFO] All expected tickers present")
    
    cleaned_df = raw_df[raw_df["ticker"].isin(expected_tickers)].copy()

    unexpected_df = raw_df[~raw_df["ticker"].isin(expected_tickers)].copy()

    unexpected_ticker_set = set(unexpected_df["ticker"].dropna().unique())

    rows_dropped = original_row_count - len(cleaned_df)

    print(f"[INFO] Rows dropped {rows_dropped}")

    print(f"[INFO] Tickers dropped {sorted(unexpected_ticker_set)}")

    print(f"[INFO] Valid rows {len(cleaned_df)}")

    print(cleaned_df.head())

    return cleaned_df


# Sanity check on columns ensurin non-zero and negative values are removed where relevant.
def sanity_check (df: pd.DataFrame, non_zero_cols: list[str], allow_zero_cols: list[str]) -> pd.DataFrame:
    
    raw_df = df.copy()

    print("\n   [START] SANITY CHECK")

    original_row_count = len(raw_df)
    print(f"[INFO] Raw rows {original_row_count}")

    # Set True if greater than or equal to zero in chosen column(s)
    allow_zero = (raw_df[allow_zero_cols] >= 0).all(axis=1)

    # Set True if greater than zero in chosen column(s)
    non_zero = (raw_df[non_zero_cols] > 0).all(axis=1)

    # Keep only rows that pass both checks (Has True) for both checks.
    mask = allow_zero & non_zero

    cleaned_df = raw_df[mask].copy()

    rows_dropped = original_row_count - len(cleaned_df)
    print(f"[INFO] Rows dropped {rows_dropped}")

    invalid_df = raw_df[~mask].copy()
    print(invalid_df.head())

    print(f"\n[INFO] Valid rows {len(cleaned_df)}")

    print(cleaned_df.head())

    return cleaned_df

# Validate OHLC values
def ohlc_logic (df:pd.DataFrame) -> pd.DataFrame:

    raw_df = df.copy()
    
    print("\n   [START] OHLC SANITY CHECK")

    original_row_count = len(raw_df)
    print(f"[INFO] Raw rows {original_row_count}")

    # Sanity check for OLHC values.
    rules = {
        "high < low": raw_df["high"] >= raw_df["low"],
        "high < open": raw_df["high"] >= raw_df["open"],
        "high < close": raw_df["high"] >= raw_df["close"],
        "low > open": raw_df["low"] <= raw_df["open"],
        "low > close": raw_df["low"] <= raw_df["close"]
    }

    rules_df = pd.DataFrame(rules)

    mask = rules_df.all(axis=1)

    cleaned_df = raw_df[mask].copy()

    rows_dropped = original_row_count - len(cleaned_df)

    print(f"[INFO] Rows dropped {rows_dropped}")

    invalid_df = raw_df[~mask].copy()

    invalid_df["broken_rules"] = rules_df[~mask].apply(
        lambda row: list(row.index[~row]),
        axis=1
    )

    inspect_df = invalid_df[["date", "ticker", "open", "high", "low", "close", "broken_rules"]].copy()

    print(inspect_df.head())

    print(f"\n[INFO] Valid rows {len(cleaned_df)}")

    print(cleaned_df.head())

    return cleaned_df
    
# Sort and reindex dataframe.
# Kind of useless because the SQL table by deifnition has no order.
def time_series_sort (df: pd.DataFrame, ticker: str, date: str, earliest_first) -> pd.DataFrame:

    print("\n   [START] TICKER, DATE SORT")

    raw_df = df.copy()

    raw_df[date] = pd.to_datetime(
        raw_df[date],
        errors="coerce"
        )
    
    sorted_df = raw_df.sort_values(
        by=[ticker,date],
        ascending=[True, earliest_first]
        ).copy()
    
    print(sorted_df.head())

    print("[START] Reseting index")

    sorted_df = sorted_df.reset_index(drop=True)
    
    print(sorted_df.head())

    print(f"FINAL ROW COUNT {len(sorted_df)}")
    
    return sorted_df

# Input cleaned data into clean_prices DB table.
def insert_clean_prices(cleaned_df: pd.DataFrame) -> None:

    print("\n   [START] INSERT CLEAN PRICES INTO DB")

    print("[START] Connecting to database...")
    con = duckdb.connect(DATABASE_PATH)

    print("[INSPECT] Incoming columns:")
    print(cleaned_df.columns.tolist())

    df = cleaned_df.copy()

    print("[START] Inserting data...")

    con.register("df", df)

    con.execute("""
            INSERT INTO clean_prices BY NAME
            SELECT
                date, 
                ticker,
                open,
                high,
                low,
                close,
                adj_close,
                volume,
                downloaded_at,
                source
            FROM df
            ON CONFLICT (date, ticker) DO UPDATE SET
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                adj_close = EXCLUDED.adj_close,
                volume = EXCLUDED.volume,
                downloaded_at = EXCLUDED.downloaded_at,
                source = EXCLUDED.source    
                """)
    
    preview = con.sql("""
                SELECT *
                FROM clean_prices
                LIMIT 5
                """)

    print(preview)

    con.close()

    print("[DONE] Data inserted, table updated")

def reporting() -> None:

    con = duckdb.connect(DATABASE_PATH)

    report = con.sql("""
                        SELECT ticker, 
                            COUNT(date),
                            MIN(date) AS 't=0',
                            MAX(date) AS 't=1'
                        FROM clean_prices
                        WHERE date IS NOT NULL
                        GROUP BY ticker
                            """)

    print("\n   [START] Date range and row count report:")
    print(report)

    dup_report = con.sql("""
                        SELECT
                            date, ticker,
                         COUNT(*) as duplicate_count
                        FROM clean_prices
                         GROUP BY
                            date, ticker
                         HAVING COUNT(*) > 1
                        """)

    print("\n   [START] Duplicate row check")
    print(dup_report)
    
    con.close()

    


def main():

    raw_df = read_table("raw_prices")

    column_validation(raw_df, EXPECTED_DTYPES)

    date_df = date_validation(raw_df, START_DATE)

    na_df = drop_missing(date_df, NON_NULL_COLS)

    dup_df = drop_duplicates(na_df, DUPLICATE_KEY_COLS)

    tck_df = ticker_validation(dup_df, TICKERS)

    san_df = sanity_check(tck_df, NON_ZERO_COLS, ALLOW_ZERO_COLS)

    ohlc_df = ohlc_logic(san_df)

    sort_df = time_series_sort(ohlc_df, TICKER_COL, DATE_COL, EARLIEST_FIRST)

    insert_clean_prices(sort_df)

    reporting()

if __name__ == "__main__":
    main()