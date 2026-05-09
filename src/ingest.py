from datetime import datetime, timezone

import pandas as pd
import yfinance as yf

from src.config import RAW_DATA_DIR, RAW_PRICES_FILE, TICKERS, START_DATE, END_DATE

def download_prices(tickers: list[str]) -> pd.DataFrame:
# We define a function called download_prices that accepts one argument.
# The single argument that download_prices accepts is a list of strings.
# The function returns a pandas dataframe.

    all_data = []
    # Creates an empty list to store the data.
    # Each ticker will produce a dataframe and those dataframes will 
    # be stored in this list, and later will be combined into a single dataframe.

    for ticker in tickers:
    # Loops through all the tickers in ticker list that was passed as an argument.
    
        print(f"Downlaoding data for {ticker}...")
        
        raw_prices_df = yf.download(
            ticker,
            start=START_DATE,
            end=END_DATE,
            progress=False,
            auto_adjust=False,
            multi_level_index=False,
        )
        # Download the data using yfinance.
        # For a given ticker we download:
        # - first date of data to request
        # - last date of data to request, which is set to None 
        #   in the config file meaning no fixed end date.
        # - do not show a download progress bar by setting progress to False.
        # - keep raw OHLC (open, high, low, close) prices rather than
        #   automatically adjusting them.
        # - set multi_index_level to false to prevent duplciate column headers.

        if raw_prices_df.empty:
            print(f"Warning: no data returned for {ticker}")
            continue
        # We check whether the dateframe just generated has no rows.
        # if it is empty it proceeeds to continue meaning it skips the rest
        # of the function's loop and moves onto the next ticker.

        raw_prices_df = raw_prices_df.reset_index()
        # The raw data downloaded from yfinance has the date as an index
        # rather than as a column. Using .reset_index() we convert the
        # date values stored in the index into a normal date column.

        raw_prices_df["ticker"] = ticker
        raw_prices_df["downloaded_at"] = datetime.now(timezone.utc).isoformat()
        raw_prices_df["source"] = "yfinance"
        # Add additional metadata columns.

        all_data.append(raw_prices_df)
        # Add the current ticker's dataframe tot he all_data list.

    if not all_data:
        raise ValueError("No data was downloaded.")
    # Case handling when nothing at all was downloaded.
    # Checks whether all_data is still empty at the end.

    return pd.concat(all_data, ignore_index=True)
    # Combines all ticker dataframes into a single dataframe.
    # Ignore_index=True helps keep the index column clean instead of
    # having duplciate index values due to combining multiple dataframes.

def save_raw_prices(raw_prices_df: pd.DataFrame) -> None:
# Takes a dataframe as an argument and returns nothing.

    RAW_DATA_DIR.mkdir(parents=True,exist_ok=True)
    # Esnures that the RAW DATA Directory exists.
    # If it doesn't then it will create it.

    raw_prices_df.to_csv(RAW_PRICES_FILE, index=False)
    # Export dataframe to CSV at the path, not saving the index.

    print(f"Saved raw data to: {RAW_PRICES_FILE}")

def main() -> None:
# Defines main workflows script and returns nothing.

    prices = download_prices(TICKERS)
    save_raw_prices(prices)
    # Calls download function passing TICKERS list to function.
    # Calls saving function and passes variable holding dataframe as argument.

    print("\nDownloade Complete.")
    print(f"Rows Downloaded: {len(prices):,}")
    # Gives number of rows in the dataframe.
    # the :, formatting adds commas to large numbers.
    print(f"Tickers: {prices['ticker'].unique().tolist()}")
    # Gets unique ticker values and converts the array into a list.
    print(f"Date Range: {prices['Date'].min()} to {prices['Date'].max()}")
    # Prints earlist date in downloaded data and older date.
    
if __name__ == "__main__":
    main()
# Common python pattern that essetnially says to only run main() if the file
# is being executed directly, e.g., python download_prices.py but
# if another file tries to import the functions then python does not set __name__ 
# to "__main__" and so the whole function does not run but still allows you to
# call and reuse the function.


