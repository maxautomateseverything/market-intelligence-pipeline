import pandas as pd
import duckdb

from src.config import TICKERS
from src.ingest import download_prices, save_raw_prices, get_ticker_metadata, save_metadata

from src.config import RAW_PRICES_FILE, METADATA_FILE
from src.database import create_tables, insert_raw_prices, read_table, insert_metadata

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

from src.database import read_order_table

from src.config import (
    CALENDARS,
    ROLLING_WINDOWS,
    LAGGED_WINDOWS,
    MA_WINDOWS,

)

from src.features import (
    generate_return_features,
    generate_moving_averages,
    generate_remaining_features,
    keep_and_rename_expected_feature_columns,
    insert_price_features
)

def main() -> None:

    #Ingest

    prices = download_prices(TICKERS)
    save_raw_prices(prices)

    print("\nDownloade Complete.")
    print(f"Rows Downloaded: {len(prices):,}")
   
    print(f"Tickers: {prices['ticker'].unique().tolist()}")
    print(f"Date Range: {prices['Date'].min()} to {prices['Date'].max()}")

    metadata = get_ticker_metadata(TICKERS)
    
    print("\nTicker metadata:")
    print(metadata.head())

    save_metadata(metadata)

    #Database

    create_tables()
    
    raw_prices_df = pd.read_csv(RAW_PRICES_FILE)
    insert_raw_prices(raw_prices_df)

    metadata_df = pd.read_csv(METADATA_FILE)
    insert_metadata(metadata_df)

    result = read_table("raw_prices")
    print(result.head())
    print(result.shape)

    result2 = read_table("ticker_metadata")
    print(result2.head())
    print(result2.shape)

    #Transform

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

    #Features

    clean_df = read_order_table("clean_prices")

    returns_df = generate_return_features(
        input_df = clean_df,
        calendars = CALENDARS,
        rolling_windows = ROLLING_WINDOWS,
        lagged_windows = LAGGED_WINDOWS
    )

    ma_df = generate_moving_averages(
        input_df = returns_df,
        value_columns = ["adj_close"],
        windows = MA_WINDOWS,
        calendars = CALENDARS       
    )

    further_features_df = generate_remaining_features(
        input_df = ma_df,
        calendars = CALENDARS
    )

    final_df = keep_and_rename_expected_feature_columns(
        input_df = further_features_df,
        calendars = CALENDARS,
        rolling_windows = ROLLING_WINDOWS,
        lagged_windows = LAGGED_WINDOWS,
        ma_windows = MA_WINDOWS,
        strict = True
    )

    insert_price_features(final_df)

    print(read_order_table("price_features"))

if __name__ == "__main__":
    main()