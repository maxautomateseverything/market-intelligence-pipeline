import duckdb
import pandas as pd
import numpy as np
import pandas_market_calendars as mcal

from src.config import EXCHANGE_TO_CALENDAR
from src.database import read_order_table, read_table

#poo - lissi

#---RETURNS---#

# Map the mcal exchnage values to the yfinance excahnge values.
# Allow us to accurately calculate actual missing data vs holiday days.
def apply_metadata(clean_df: pd.DataFrame) -> pd.DataFrame:

    df = clean_df.copy()

    # Read ticker_metadata tables.
    metadata_table_df = read_table("ticker_metadata")

    # Map yfinance excahnge names to mcal names
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
def build_trading_days_lookup(calendar_name: str, start_date, end_date) -> pd.DataFrame:

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
        "expected_previous_trading_date": trading_days.shift(1),
        "calendar": calendar_name
    })

    return lookup

# Calculate daily returns based on excahnge's actual trading days.
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

    df[cum_col] = (1 + df[return_col]).cumprod() - 1

    calendar_lookups = []
    start_date = df[date_col].min()
    end_date = df[date_col].max()

    for calendar_name in df["calendar"].dropna().unique():
        lookup = build_trading_days_lookup(
            calendar_name = calendar_name,
            start_date = start_date,
            end_date = end_date
        )

        calendar_lookups.append(lookup)

    trading_lookup_df = pd.concat(calendar_lookups, ignore_index=True)

    df = df.merge(
        trading_lookup_df,
        on = ["calendar", "date"],
        how = "left"
    )

    mask = previous_date != df["expected_previous_trading_date"]

    cols_to_null = [return_col, log_col, cum_col]

    df.loc[mask, cols_to_null] = pd.NA

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

    df[cum_col] = (1 + df[return_col]).cumprod() - 1

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

    df[cum_col] = (1 + df[return_col]).cumprod() - 1

    # Calculates what the previous business day should be.
    # e.g., Monday - 1 = Friday.
    expected_previous_date = df[date_col] - pd.tseries.offsets.BDay(1)

    # Checks whether previous date matches expected.
    # Rows which they don't match set daily_return to missing.
    mask = previous_date != expected_previous_date

    cols_to_null = [return_col, log_col, cum_col]

    df.loc[mask, cols_to_null] = pd.NA

    return df





def main():

    clean_df = read_order_table("clean_prices")

    print(clean_df.head(10))

    return_df = return_no_calendar(clean_df)

    
