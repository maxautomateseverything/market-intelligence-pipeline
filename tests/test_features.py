from src.database import read_order_table

from src.features import (
    apply_metadata,
    return_no_calendar,
    return_business_calendar,
    return_exchange_calendar
)

def main():

    clean_df = read_order_table("clean_prices")

    print(clean_df.head(10))

    metadata_df = apply_metadata(clean_df)

    print(metadata_df.head(10))

    return_1_df = return_no_calendar(metadata_df)

    return_2_df = return_business_calendar(return_1_df)

    return_3_df = return_exchange_calendar(return_2_df)
    
    return_3_df.to_csv(r"C:\Users\maxan\OneDrive\Desktop\0. Personal Projects\market-intelligence-pipeline\data\inspect\returns_inspect.csv")

if __name__ == "__main__":
    main()