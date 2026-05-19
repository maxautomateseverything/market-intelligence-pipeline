import pandas as pd

from src.config import RAW_PRICES_FILE, METADATA_FILE
from src.database import create_tables, insert_raw_prices, read_table, insert_metadata

def main():
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


if __name__ == "__main__":
    main()