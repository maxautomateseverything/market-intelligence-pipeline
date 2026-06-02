from src.database import read_order_table

from src.config import (
    CALENDARS,
    ROLLING_WINDOWS,
    LAGGED_WINDOWS,
    MA_WINDOWS,

)

from src.features import (
    generate_return_features,
    generate_moving_averages
)

def main():

    clean_df = read_order_table("clean_prices")

    returns_df = generate_return_features(
        input_df = clean_df,
        calendars = CALENDARS,
        rolling_windows = ROLLING_WINDOWS,
        lagged_windows = LAGGED_WINDOWS
    )

    returns_df.to_csv(
    r"C:\Users\maxan\OneDrive\Desktop\0. Personal Projects\market-intelligence-pipeline\data\inspect\returns_inspect.csv",
    index=False
    )

    ma_df = generate_moving_averages(
        input_df = returns_df,
        value_columns = ["adj_close"],
        windows = MA_WINDOWS,
        calendars = CALENDARS       
    )

    ma_df.to_csv(
    r"C:\Users\maxan\OneDrive\Desktop\0. Personal Projects\market-intelligence-pipeline\data\inspect\ma_inspect.csv",
    index=False
    )

if __name__ == "__main__":
    main()