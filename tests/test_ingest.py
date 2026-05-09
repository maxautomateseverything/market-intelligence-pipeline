from datetime import datetime, timezone

import pandas as pd
import yfinance as yf

from src.config import RAW_DATA_DIR, RAW_PRICES_FILE, TICKERS, START_DATE, END_DATE
from src.ingest import download_prices, save_raw_prices

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