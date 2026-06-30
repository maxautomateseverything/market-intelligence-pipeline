import duckdb
import pandas as pd

from src.database import read_table
from src.config import (EXPECTED_DTYPES, 
                        START_DATE,
                        NON_NULL_COLS,
                        TICKERS, 
                        DUPLICATE_KEY_COLS, 
                        NON_ZERO_COLS, 
                        ALLOW_ZERO_COLS, 
                        TICKER_COL, 
                        DATE_COL, 
                        EARLIEST_FIRST)
from src.transform import (column_validation,
                           date_validation, 
                           drop_missing, 
                           drop_duplicates, 
                           sanity_check,
                           ticker_validation,
                           ohlc_logic,
                           time_series_sort,
                           insert_clean_prices,
                           reporting)

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