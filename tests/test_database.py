import duckdb
import pandas as pd

from src.config import RAW_PRICES_FILE
from src.database import create_tables, insert_raw_prices, read_table

def main():
    create_tables()

    raw_prices_df = pd.read_csv(RAW_PRICES_FILE)
    insert_raw_prices(raw_prices_df)

    result = read_table("raw_prices")
    print(result.head())
    print(result.shape)


if __name__ == "__main__":
    main()