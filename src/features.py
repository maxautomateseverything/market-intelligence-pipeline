import duckdb
import pandas as pd
import numpy as np
import pandas_market_calendars as mcal

from src.config import EXCHANGE_TO_CALENDAR
from src.database import read_order_table, read_table

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

    df = input_df.copy()

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
            how = "left"
        )

        print(f"[INFO] Calendar: {calendar}, Days_ago: {days} - ADDED")

    elif calendar == "exchange_calendar":

        metadata_table_df = read_table("ticker_metadata")

        # Map yfinance exchange names to mcal names
        metadata_table_df["market_calendar"] = metadata_table_df["exchange"].map(EXCHANGE_TO_CALENDAR)

        # Inspect missing mappings
        print(metadata_table_df[metadata_table_df["market_calendar"].isna()])

        df = df.merge(
        metadata_table_df[[group_col, "market_calendar"]],
        on = group_col,
        how = "left"
        )

        calendar_lookups = []
        start_date = df[date_col].min()
        end_date = df[date_col].max()

        for calendar_name in df["market_calendar"].dropna().unique():
            
            calendar = mcal.get_calendar(calendar_name)

            schedule = calendar.schedule(
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
                "calendar":calendar_name
            })

            calendar_lookups.append(lookup)

        if not calendar_lookups:
            raise ValueError(
                "[ERROR] No valid mapped exchange calendar found"
            )

        exchange_date_lookup = pd.concat(calendar_lookups, ignore_index = True)

        df = df.merge(
            exchange_date_lookup,
            on = ["calendar", date_col],
            how = "left"
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







#---RETURNS---#

# Map the mcal exchnage values to the yfinance exchange values.
# Allow us to accurately calculate actual missing data vs holiday days.
def apply_metadata(clean_df: pd.DataFrame) -> pd.DataFrame:

    df = clean_df.copy()

    # Read ticker_metadata tables.
    metadata_table_df = read_table("ticker_metadata")

    # Map yfinance exchange names to mcal names
    metadata_table_df["calendar"] = metadata_table_df["exchange"].map(EXCHANGE_TO_CALENDAR)

    # Inspect missing mappings
    print(metadata_table_df[metadata_table_df["calendar"].isna()])

    metadata_df = df.merge(
        metadata_table_df[["ticker", "calendar", "exchange", "timezone"]],
        on = "ticker",
        how = "left"
    )

    return metadata_df

# Calculate expected previous trading date per calendar lookup
# This is respective to the specific exchange.
def build_trading_days_lookup(calendar_name: str, days: int, start_date, end_date) -> pd.DataFrame:

    # Get the market calendar object
    # For example if calendar_name is "NYSE" it gets the NYSE trading calendar
    calendar = mcal.get_calendar(calendar_name)

    # We build the trading schedule between start and end date.
    schedule = calendar.schedule(
        start_date = start_date,
        end_date = end_date
    )

    # Creates a pandas series containing the trading dates.
    # schedule.index contains the dates from the market schedule.
    # converts the index into datetime values.
    # tz_localise removes the timezone information, making the dates timezone-naive.
    # then renames the series "date"
    trading_days = pd.Series(
        pd.to_datetime(schedule.index).tz_localize(None),
        name="date"
    )

    # Creates lookup showing the current trading day 
    # and expected previous trading day.
    # Takes into accoutn holidays, weekends, etc.
    # Creates dataframe called lookup with 3 columns shown below.
    lookup = pd.DataFrame({
        "date": trading_days,
        f"expected_previous_{days}d_exchange_calendar": trading_days.shift(days),
        "calendar": calendar_name
    })

    return lookup

# Calculate daily returns based on exchange's actual trading days.
def return_exchange_calendar(metadata_df: pd.DataFrame) -> pd.DataFrame:

    date_col = "date"
    group_col = "ticker"
    price_col = "adj_close"
    return_col = "daily_return_exchange_calendar"
    log_col = "log_return_exchange_calendar"
    cum_col = "cum_return_exchange_calendar"

    df = metadata_df.copy()

    df[date_col] = pd.to_datetime(df[date_col]).dt.normalize()

    df = df.sort_values([group_col, date_col]).reset_index(drop=True)

    previous_close = df.groupby(group_col)[price_col].shift(1)
    previous_date = df.groupby(group_col)[date_col].shift(1)

    df[return_col] = df[price_col] / previous_close - 1

    df[log_col] = np.log(df[price_col] / previous_close)

    calendar_lookups = []
    start_date = df[date_col].min()
    end_date = df[date_col].max()

    for calendar_name in df["calendar"].dropna().unique():
        lookup = build_trading_days_lookup(
            calendar_name = calendar_name,
            days = 1,
            start_date = start_date,
            end_date = end_date
        )

        calendar_lookups.append(lookup)

    if not calendar_lookups:
        print("[WARNING] No valid exchange calendars found.")
        return df

    trading_lookup_df = pd.concat(calendar_lookups, ignore_index=True)

    df = df.merge(
        trading_lookup_df,
        on = ["calendar", "date"],
        how = "left"
    )

    mask = previous_date != df["expected_previous_1d_exchange_calendar"]

    cols_to_null = [return_col, log_col]

    df.loc[mask, cols_to_null] = np.nan

    df[cum_col] = (
        df.groupby(group_col)[return_col]
        .transform(lambda x: (1 + x.fillna(0)).cumprod() - 1)
    )

    return df

# Calcualte daily returns simply based on the previous row.
def return_no_calendar(clean_df: pd.DataFrame) -> pd.DataFrame:

    date_col = "date"
    group_col = "ticker"
    price_col = "adj_close"
    return_col = "daily_return_no_calendar"
    log_col = "log_return_no_calendar"
    cum_col = "cum_return_no_calendar"

    df = clean_df.copy()

    df[date_col] = pd.to_datetime(df[date_col]).dt.normalize()

    df = df.sort_values([group_col, date_col]).reset_index(drop=True)

    previous_close = df.groupby(group_col)[price_col].shift(1)

    df[return_col] = (df[price_col] / previous_close) - 1

    df[log_col] = np.log(df[price_col] / previous_close)

    df[cum_col] = (
        df.groupby(group_col)[return_col]
        .transform(lambda x: (1 + x.fillna(0)).cumprod() - 1)
    )

    return df

# We calculate daily return as today's adjusted close divided by 
# yesterday's adjusted close minus 1, as adjusted close accounts for dividends,
# stock splits and corporate actions.
def return_business_calendar(clean_df: pd.DataFrame) -> pd.DataFrame:

    #Store the column names as variables
    date_col = "date"
    group_col = "ticker"
    price_col = "adj_close"
    return_col = "daily_return_business_calendar"
    log_col = "log_return_business_calendar"
    cum_col = "cum_returns_business_calendar"

    df = clean_df.copy()

    df[date_col] = pd.to_datetime(df[date_col]).dt.normalize()

    # Sorts dataframe first by ticker then by date.
    df = df.sort_values([group_col, date_col]).reset_index(drop=True)

    # groupby() groups dataframe by ticker preventing cross ticker 
    # values from afecting returns.
    # shift(1) moves values down by one row inside each ticker group,
    # get previous close within each ticker.
    previous_close = df.groupby(group_col)[price_col].shift(1)

    # Get previous date for each ticker prevous close.
    previous_date = df.groupby(group_col)[date_col].shift(1)

    # Calculates the return.
    df[return_col] = (df[price_col] / previous_close) - 1

    df[log_col] = np.log(df[price_col] / previous_close)

    # Calculates what the previous business day should be.
    # e.g., Monday - 1 = Friday.
    expected_previous_date = df[date_col] - pd.tseries.offsets.BDay(1)

    # Checks whether previous date matches expected.
    # Rows which they don't match set daily_return to missing.
    mask = previous_date != expected_previous_date

    cols_to_null = [return_col, log_col]

    df.loc[mask, cols_to_null] = np.nan

    df[cum_col] = (
        df.groupby(group_col)[return_col]
        .transform(lambda x: (1 + x.fillna(0)).cumprod() - 1)
    )

    return df

def rolling_return(clean_df: pd.DataFrame, calendar: str, days: int) -> pd.DataFrame:

    date_col = "date"
    group_col = "ticker"
    price_col = "adj_close"

    past_price = f"adj_close_{days}d_ago_{calendar}"
    rolling = f"rolling_{days}d_return_{calendar}"

    df = clean_df.copy()

    df[date_col] = pd.to_datetime(df[date_col]).dt.normalize()

    df = df.sort_values([group_col, date_col]).reset_index(drop = True)

    df[rolling] = np.nan

    if calendar == "no_calendar":

        df[past_price] = (
            df.groupby("ticker")["adj_close"]
            .shift(days)
        )

        mask = df[past_price].notna() & (df[past_price] != 0)

        df.loc[mask, rolling] = (
            df.loc[mask, price_col] / df.loc[mask, past_price] - 1
        )

    elif calendar == "business_calendar":

        df[f"{days}d_ago_{calendar}"] = (
            df[date_col] - pd.tseries.offsets.BDay(days)
        )

        business_lookup = df[[group_col, date_col, price_col]].copy()

        business_lookup = business_lookup.rename(
            columns = {
                date_col: f"{days}d_ago_{calendar}",
                price_col: past_price
            }
        )

        df = df.merge(
            business_lookup,
            on = [group_col, f"{days}d_ago_{calendar}"],
            how = "left"
        )

        mask = df[past_price].notna() & (df[past_price] != 0)

        df.loc[mask, rolling] = (
            df.loc[mask, price_col] / df.loc[mask, past_price] - 1
        )

    elif calendar == "exchange_calendar":

        target_date_col = f"{days}d_ago_{calendar}"
        expected_col = f"expected_previous_{days}d_exchange_calendar"

        calendar_lookups = []

        for calendar_name in df["calendar"].dropna().unique():
            lookup = build_trading_days_lookup(
                calendar_name = calendar_name,
                days = days,
                start_date = df[date_col].min(),
                end_date = df[date_col].max()
            )

            calendar_lookups.append(lookup)

        if not calendar_lookups:
            print("[WARNING] No valid exchange calendars found.")
            return df

        exchange_lookup = pd.concat(calendar_lookups, ignore_index = True)

        df = df.merge(
            exchange_lookup,
            on = ["calendar", "date"],
            how = "left"
        )

        df = df.rename(
            columns={
                expected_col: target_date_col
            }
        )

        exchange_price_lookup = df[[group_col, date_col, price_col]].copy()

        exchange_price_lookup = exchange_price_lookup.rename(
            columns = {
                date_col: target_date_col,
                price_col: past_price
            }
        )

        df = df.merge(
            exchange_price_lookup,
            on = [group_col, target_date_col],
            how = "left"
        )

        mask = df[past_price].notna() & (df[past_price] != 0)

        df.loc[mask, rolling] = (
            df.loc[mask, price_col] / df.loc[mask, past_price] - 1
        )

    else:
        raise ValueError(
            "calendar must be one of: 'no_calendar', 'business_calendar', 'exchange_calendar'"
        )

    return df
    
    





def main():

    clean_df = read_order_table("clean_prices")

    print(clean_df.head(10))

    metadata_df = apply_metadata(clean_df)

    print(metadata_df.head(10))

    return_1_df = return_no_calendar(metadata_df)

    return_2_df = return_business_calendar(return_1_df)

    return_3_df = return_exchange_calendar(return_2_df)
    
    rolling_1_df = rolling_return(return_3_df, "no_calendar", 7)

    rolling_2_df = rolling_return(rolling_1_df, "business_calendar", 7)

    rolling_3_df = rolling_return(rolling_2_df, "exchange_calendar", 7)

    rolling_3_df.to_csv(
    r"C:\Users\maxan\OneDrive\Desktop\0. Personal Projects\market-intelligence-pipeline\data\inspect\returns_inspect.csv",
    index=False
    )

if __name__ == "__main__":
    main()  
