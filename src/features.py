import pandas as pd
import numpy as np
import pandas_market_calendars as mcal

from src.config import (
    EXCHANGE_TO_CALENDAR, 
    CALENDARS,
    ROLLING_WINDOWS,
    LAGGED_WINDOWS
)
from src.database import (
    read_table,
    read_order_table
)
#poo - lissi

#--RETURNS--#

def prepare_df(input_df: pd.DataFrame) -> pd.DataFrame:

    df = input_df.copy()

    # convert to proper pandas datetime values.
    # normlaises all dates to the same time (00:00:00).
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()

    # sorts value by ticekr first then date.
    # resets row numbers after sorting.
    df = df.sort_values(["ticker", "date"]).reset_index(drop = True)

    return df

def add_lagged_price(
        input_df: pd.DataFrame, 
        days: int,
        calendar: str
        ) -> pd.DataFrame:

    lag_price_col = f"adj_close_{days}d_ago_{calendar}"
    
    expected_date_col = f"date_{days}d_ago_{calendar}"

    date_col = "date"
    group_col = "ticker"
    price_col = "adj_close"

    df = prepare_df(input_df.copy())

    if calendar == "no_calendar":

        df[lag_price_col] = (
            df.groupby(group_col)[price_col].shift(days)
        )

        print(f"[INFO] Calendar: {calendar}, Days_ago: {days} - ADDED")

    elif calendar == "business_calendar":

        df[expected_date_col] = (
            df[date_col] - pd.tseries.offsets.BDay(days)
        )

        business_lookup = df[[group_col, date_col, price_col]].copy()

        business_lookup = business_lookup.rename(
            columns = {
                date_col: expected_date_col,
                price_col: lag_price_col
            }
        )

        df = df.merge(
            business_lookup,
            on = [group_col, expected_date_col],
            how = "left",
            validate="many_to_one"
        )

        print(f"[INFO] Calendar: {calendar}, Days_ago: {days} - ADDED")

    elif calendar == "exchange_calendar":

        if "market_calendar" in df.columns:

            print("[INFO] Exchange calendar mapping exists: Proceeding")

        else: 

            print("[INFO] Exchange calendar does not exist: Creating before proceeding")

            metadata_table_df = read_table("ticker_metadata")

            # Map yfinance exchange names to mcal names
            metadata_table_df["market_calendar"] = metadata_table_df["exchange"].map(EXCHANGE_TO_CALENDAR)

            # Inspect missing mappings
            print(metadata_table_df[metadata_table_df["market_calendar"].isna()])

            df = df.merge(
            metadata_table_df[[group_col, "market_calendar"]],
            on = group_col,
            how = "left",
            validate="many_to_one"
            )

            print("[INFO] Exchange calendar created: Proceeding")

        calendar_lookups = []
        start_date = df[date_col].min()
        end_date = df[date_col].max()

        for calendar_name in df["market_calendar"].dropna().unique():
            
            market_calendar_obj = mcal.get_calendar(calendar_name)

            schedule = market_calendar_obj.schedule(
                start_date = start_date,
                end_date = end_date
            )

            trading_days = pd.Series(
                pd.to_datetime(schedule.index).tz_localize(None),
                name="date"
            )

            lookup = pd.DataFrame({
                "date": trading_days,
                expected_date_col: trading_days.shift(days),
                "market_calendar":calendar_name
            })

            calendar_lookups.append(lookup)

        if not calendar_lookups:
            raise ValueError(
                "[ERROR] No valid mapped exchange calendar found"
            )

        exchange_date_lookup = pd.concat(calendar_lookups, ignore_index = True)

        df = df.merge(
            exchange_date_lookup,
            on = ["market_calendar", date_col],
            how = "left",
            validate = "many_to_one"
        )

        exchange_price_lookup = df[[group_col, date_col, price_col]].copy()

        exchange_price_lookup = exchange_price_lookup.rename(
            columns={
                date_col: expected_date_col,
                price_col: lag_price_col
            }
        )

        df = df.merge(
            exchange_price_lookup,
            on=[group_col, expected_date_col],
            how="left",
            validate="many_to_one"
        )

        print(f"[INFO] Calendar: {calendar}, Days_ago: {days} - ADDED")

    else:
        raise ValueError(
            "[ERROR] Calendar must be one of: 'no_calendar', 'business_calendar', 'exchange_calendar'"
        )

    return df

def calculate_return_from_lagged_price(
        input_df: pd.DataFrame,
        days: int,
        calendar: str,
        return_type: str
        ) -> pd.DataFrame:
    
    lag_price_col = f"adj_close_{days}d_ago_{calendar}"

    price_col = "adj_close"

    return_col = f"{days}d_{calendar}_{return_type}_return"

    df = input_df.copy()

    if return_type == "rolling" and days == 1:
        raise ValueError("[ERROR] Rolling return should use days > 1")

    if return_type == "simple" and days != 1:
        raise ValueError("[ERROR] Simple return where days > 1 is rolling return")

    if lag_price_col in df.columns:

        print(f"[INFO] {lag_price_col} exists: Proceeding")

    else:

        print(f"[INFO] {lag_price_col} does not exist: Creating before proceeding")
    
        df = add_lagged_price(df, days, calendar)  

        print(f"[INFO] {lag_price_col} created: Proceeding")  

    if return_type in ["simple", "rolling"]:

        valid = (
            df[lag_price_col].notna() 
            & (df[lag_price_col] != 0)
            & df[price_col].notna()
        )

        print(f"[START] Calculating simple return. Period: {days}d. Calendar: {calendar}.")

        df[return_col] = np.nan

        df.loc[valid, return_col] = (
            df.loc[valid, price_col] / df.loc[valid, lag_price_col] - 1
        )

    elif return_type == "log":

        valid = (
            df[lag_price_col].notna()
            & (df[lag_price_col] > 0)
            & df[price_col].notna()
            &(df[price_col] > 0)
        )

        print(f"[START] Calculating log return. Period: {days}d. Calendar: {calendar}.")

        df[return_col] = np.nan

        df.loc[valid, return_col] = (

        np.log(df.loc[valid, price_col] / df.loc[valid, lag_price_col])

        )

    else:
        raise ValueError(
            "[ERROR] Return_type must be one of: 'simple', 'log', 'rolling'"
        )

    return df

def calculate_dependent_returns(
        input_df: pd.DataFrame,
        days: int,
        calendar: str, 
        return_type: str
        ) -> pd.DataFrame:

    df = input_df.copy()

    daily_return_col = f"1d_{calendar}_simple_return"

    group_col = "ticker"

    if daily_return_col in df.columns:

        print(f"[INFO] {daily_return_col} exists: Proceeding")

    else:

        print(f"[INFO] {daily_return_col} does not exist: Creating before proceeding")

        df = calculate_return_from_lagged_price(
            input_df = df,
            days = 1,
            calendar = calendar,
            return_type = "simple"
        )

        print(f"[INFO] {daily_return_col} created: Proceeding")

    if return_type == "cumulative":

        print(f"[START] Calculating cumulative return. Calendar: {calendar}.")

        return_col = f"{return_type}_returns_{calendar}"

        df[return_col] = (
            df.groupby(group_col)[daily_return_col]
            .transform(lambda x: ((1 + x.fillna(0)).cumprod() - 1).where(x.notna()))
        )

    elif return_type == "lagged":

        print(f"[START] Calculating lagged returns. Days: {days}. Calendar: {calendar}.")
    
        return_col = f"{days}d_{calendar}_{return_type}_returns"

        df[return_col] = df.groupby(group_col)[daily_return_col].shift(days)

    else:

        raise ValueError(
            "[ERROR] Return type must be one of: 'cumulative', 'lagged'."
        )

    return df

def generate_return_features(
        input_df: pd.DataFrame,
        calendars: list[str],
        rolling_windows: list[int],
        lagged_windows: list[int]
        ) -> pd.DataFrame:
    
    df = input_df.copy()

    df = prepare_df(df)

    for calendar in calendars:

        df = calculate_return_from_lagged_price(
            input_df = df,
            days = 1,
            calendar = calendar,
            return_type = "simple"
        )

        for rolling_window in rolling_windows:

            df = calculate_return_from_lagged_price(
                input_df = df,
                days = rolling_window,
                calendar = calendar,
                return_type = "rolling"
            )

        df = calculate_return_from_lagged_price(
            input_df = df,
            days = 1,
            calendar = calendar,
            return_type = "log"
        )

        df = calculate_dependent_returns(
            input_df = df,
            days = 1,
            calendar = calendar,
            return_type = "cumulative"
        )

        for lagged_window in lagged_windows:

            df = calculate_dependent_returns(
                input_df = df,
                days = lagged_window,
                calendar = calendar,
                return_type = "lagged"
            )

    return df


#--MOVING AVERAGES--#
### Still need to group by ticker and sort by date.
### Also need to implement the various calendars.

def generate_moving_averages(
            input_df: pd.DataFrame,
            columns: list[str],
            windows: list[int]
        ) -> pd.DataFrame:

        df = input_df.copy()

        for window in windows:

            if window < 1:

                raise ValueError("[ERROR] Invalid window size (n < 0) chosen for moving averages")
            
            for column in columns:

                if df[column].count() < window:

                    raise ValueError("[ERROR] Window range too large or number of values too small")

                upper = df[column].count() - window + 1

                ma_col = f"{window}d_{column}_moving_average"

                df[ma_col] = np.nan

                for i in range(upper):

                    index = df.index[i + window - 1]

                    df.loc[index, ma_col] = (df[column].iloc[i: i + window]).sum()/window




def main():

    clean_df = read_order_table("clean_prices")

    returns_df = generate_return_features(
        input_df = clean_df,
        calendars = CALENDARS,
        rolling_windows = ROLLING_WINDOWS,
        lagged_windows = LAGGED_WINDOWS
    )

if __name__ == "__main__":
    main()  
