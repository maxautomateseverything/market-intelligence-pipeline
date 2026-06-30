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

def main():

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

    final_df.to_csv(
        r"C:\Users\maxan\OneDrive\Desktop\0. Personal Projects\market-intelligence-pipeline\data\inspect\features.csv",
        index = False
    )

    insert_price_features(final_df)

    print(read_order_table("price_features"))

if __name__ == "__main__":
    main()  