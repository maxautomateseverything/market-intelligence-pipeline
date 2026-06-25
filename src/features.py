import pandas as pd
import numpy as np

# Used to retrieve real stock market calendars.
import pandas_market_calendars as mcal

from src.config import (
    EXCHANGE_TO_CALENDAR, 
    CALENDARS,
    ROLLING_WINDOWS,
    LAGGED_WINDOWS,
    MA_WINDOWS
)
from src.database import (
    read_table,
    read_order_table
)
#poo - lissi

#--RETURNS--#

def prepare_df(input_df: pd.DataFrame) -> pd.DataFrame:

    # Creates local copy which is important to not accidently
    # modify the dataframe outside of the function.
    df = input_df.copy()

    # Convert to proper pandas datetime values.
    # Normlaises all dates to the same time (00:00:00).
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()

    # Sorts value by ticekr first then date.
    # Resets row numbers after sorting.
    df = df.sort_values(["ticker", "date"]).reset_index(drop = True)

    return df

# Create past value for a column based on a calendar type.
def add_lagged_value(
        input_df: pd.DataFrame, 
        days: int,
        calendar: str,
        value_col: str
        ) -> pd.DataFrame:

    lag_value_col = f"{value_col}_{days}d_ago_{calendar}"
    
    # Create temp column name that we drop later for expected
    # past date, no_calendar does not use this since it simply
    # shifts rows.
    expected_date_col = f"date_{days}d_ago_{calendar}"

    date_col = "date"
    group_col = "ticker"
    price_col = value_col

    # Copy and prepare the dataframe.
    df = prepare_df(input_df.copy())

    if calendar == "no_calendar":
        
        # Creates the lag column by:
        # grouping by group_col = "ticker" so each is handled separtely
        # selecting the column you want to lag
        # move the rows down by the integer days wihtin each ticker.
        # this is why prepare_df is important.
        df[lag_value_col] = (
            df.groupby(group_col)[price_col].shift(days)
        )

        print(f"[INFO] Calendar: {calendar}, Days_ago: {days} - ADDED")

    elif calendar == "business_calendar":

        # Calculates expected previous business date.
        df[expected_date_col] = (
            # get current date
            # creates pandas business day offset
            # if day = 1, creates current day minus one busienss day
            # means monday will go to friday
            df[date_col] - pd.tseries.offsets.BDay(days)
        )

        # Create smaller dataframe containing only columns
        # needed for the lookup, enabling us to find specific value
        # on the expected past date.
        business_lookup = df[[group_col, date_col, price_col]].copy()

        # Rename columns in lookup dataframe as we want to merge 
        # curren trow's epected past date against this lookup.
        business_lookup = business_lookup.rename(
            columns = {
                date_col: expected_date_col,
                price_col: lag_value_col
            }
        )

        # Merge lagged values onto main dataframe, merging on
        # group_col and expected_date_col, "left" to keep all 
        # rows on original dataframe.
        df = df.merge(
            business_lookup,
            on = [group_col, expected_date_col],
            how = "left",
            # Means many rows can map to one row in the lookup
            # protecting use from dupclaite ticker-date rows in
            # the lookup table - if there are duplcaites and error
            # is raised instead of silentily duplicating our rows.
            validate="many_to_one"
        )

        print(f"[INFO] Calendar: {calendar}, Days_ago: {days} - ADDED")

    elif calendar == "exchange_calendar":

        # Check whether market_calendar column exists.
        if "market_calendar" in df.columns:

            print("[INFO] Exchange calendar mapping exists: Proceeding")

        # Creates the column if it doesnt' exist.
        else: 

            print("[INFO] Exchange calendar does not exist: Creating before proceeding")

            metadata_table_df = read_table("ticker_metadata")

            # Map yfinance exchange names to mcal names and
            # place values in "market_calendar" column.
            metadata_table_df["market_calendar"] = metadata_table_df["exchange"].map(EXCHANGE_TO_CALENDAR)

            # Inspect missing mappings returning True when calendar is missing.
            print(metadata_table_df[metadata_table_df["market_calendar"].isna()])

            # Merge calendar back onto price dataframe, merging on "ticker",
            # allowing us to add the respective exchange calendar for each ticker.
            df = df.merge(
            metadata_table_df[[group_col, "market_calendar"]],
            on = group_col,
            how = "left",
            # Ensures each ticekr maps to one calendar.
            validate="many_to_one"
            )

            print("[INFO] Exchange calendar created: Proceeding")

        # Create an empty list that will store one lookup dataframe
        # per excahnge calendar. We will later combine it with pd.concat().
        calendar_lookups = []

        # Get ealiest and most recent date in dataframe.
        start_date = df[date_col].min()
        end_date = df[date_col].max()

        # Lookp through each unique exchagne calendar used in
        # the dataframe.
        for calendar_name in df["market_calendar"].dropna().unique():
            
            # Get the actual exchange calendar object.
            # Given calendar_name, e.g., NYSE, return the known trading
            # days for that exchange.
            market_calendar_obj = mcal.get_calendar(calendar_name)

            # Creates trading schedule between start and end date.
            # Schedule contains trading dates and market open/close times.
            # We mainly care about the index that contains the trading days.
            schedule = market_calendar_obj.schedule(
                start_date = start_date,
                end_date = end_date
            )

            # Converts the schedules index into a pandas series of trading days.
            # Ensures they are datetime values and then removes timezoen information
            # which helps match the format of our current date column in dataframe.
            # Then call the series "date".
            trading_days = pd.Series(
                pd.to_datetime(schedule.index).tz_localize(None),
                name="date"
            )

            # Creates a lookup table for one exchage calendar containing:
            # date, expected previous trading date, market calendar.
            # Creates lookup by shifting trading days down by days.
            lookup = pd.DataFrame({
                "date": trading_days,
                expected_date_col: trading_days.shift(days),
                "market_calendar":calendar_name
            })

            # Appends the lookup dateframe to the list.
            # With multiple exchages each excahnge gets its own lookup table.
            calendar_lookups.append(lookup)

        # Checks if no valid excahnge calendars were found.
        if not calendar_lookups:
            raise ValueError(
                "[ERROR] No valid mapped exchange calendar found"
            )

        # Combines the individual exchange lookup dataframes into one dataframe. 
        # Resets the row numbers in the combined dataframe.           
        exchange_date_lookup = pd.concat(calendar_lookups, ignore_index = True)

        # Merges expected previous exchange trading date onto main dataframe.
        # Matches on market_calendar and data 
        df = df.merge(
            exchange_date_lookup,
            on = ["market_calendar", date_col],
            how = "left",
            validate = "many_to_one"
        )

        # Creates a lookup table of actual values by ticker and date.
        exchange_price_lookup = df[[group_col, date_col, price_col]].copy()

        # Renames the lookup columsn so they can be merged.
        # Change the date and value column.
        exchange_price_lookup = exchange_price_lookup.rename(
            columns={
                date_col: expected_date_col,
                price_col: lag_value_col
            }
        )

        # Merge the actual lagged values on the dataframe.
        # Merge on ticekr and expected previous date that we previously shifted.
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
    
    # Ignore errors here because we no_calendar doesn't create
    # an expected date column and so will create an error if
    # causing code to stop if not ignored.
    df = df.drop(columns = [expected_date_col], errors="ignore")

    return df

# Calculate simple, rolling and lagged return all of which depend on the lagged
# column or previous adj_close.
def calculate_return_from_lagged_price(
        input_df: pd.DataFrame,
        days: int,
        calendar: str,
        return_type: str
        ) -> pd.DataFrame:
    
    # Define the name of the lag price column which would.
    lag_price_col = f"adj_close_{days}d_ago_{calendar}"

    # Hard code the adj_close as the price column since returns depend on adj_close
    price_col = "adj_close"

    # Define return column for various windows, calendars or return type.
    return_col = f"{days}d_{calendar}_{return_type}_return"

    # Create copy of dataframe to keep changes contained wihtout the function.
    df = input_df.copy()

    # Disallow rolling and singe day window since that is essentially simple return.
    if return_type == "rolling" and days == 1:
        raise ValueError("[ERROR] Rolling return should use days > 1")

    # Simple return can only have a single day window or else it is rolling return.
    if return_type == "simple" and days != 1:
        raise ValueError("[ERROR] Simple return where days > 1 is rolling return")

    # Check whether the expected lag_price column already exists to reduce duplciate effort.
    if lag_price_col in df.columns:

        print(f"[INFO] {lag_price_col} exists: Proceeding")

    # Generate the lag price column otherwise.
    else:

        print(f"[INFO] {lag_price_col} does not exist: Creating before proceeding")
    
        # Use lag value reusable function passing through the
        # dataframe, window, calendar and value column which is hard coded adj_close.
        df = add_lagged_value(df, days, calendar, value_col = "adj_close")  

        print(f"[INFO] {lag_price_col} created: Proceeding")  

    # If return type is one of the element in the list.
    if return_type in ["simple", "rolling"]:

        # Create mask to keep rows that have a non-blank lagged value,
        # non-zero lagged value and a non-blank price value.
        # Such values cause errors in return calculations.
        valid = (
            df[lag_price_col].notna() 
            & (df[lag_price_col] != 0)
            & df[price_col].notna()
        )

        print(f"[START] Calculating {return_type} return. Period: {days}d. Calendar: {calendar}.")

        # Set column to numpy nulls.
        df[return_col] = np.nan

        # Apply the return formula in the return column for only rows that are true
        # for the mask.
        df.loc[valid, return_col] = (
            df.loc[valid, price_col] / df.loc[valid, lag_price_col] - 1
        )

    # If return type is log returns.
    elif return_type == "log":

        # Create mask that selects rows if the lagged column is not null and
        # greater than zero, and price column is not null and greater than zero
        valid = (
            df[lag_price_col].notna()
            & (df[lag_price_col] > 0)
            & df[price_col].notna()
            &(df[price_col] > 0)
        )

        print(f"[START] Calculating log return. Period: {days}d. Calendar: {calendar}.")

        # Set column to numpy null
        df[return_col] = np.nan

        # Apply log return formula only to rows that have been selected in the mask
        # for the return column.
        df.loc[valid, return_col] = (

        np.log(df.loc[valid, price_col] / df.loc[valid, lag_price_col])

        )

    # Raise error if invalid return type choice is made.
    else:
        raise ValueError(
            "[ERROR] Return_type must be one of: 'simple', 'log', 'rolling'"
        )

    # Drop the lagged price columns to keep dataframe clean.
    df = df.drop(columns = [lag_price_col])

    return df

# Calculate returns that are dependent on the calculation of other returns.
def calculate_dependent_returns(
        input_df: pd.DataFrame,
        days: int,
        calendar: str, 
        return_type: str
        ) -> pd.DataFrame:

    # Create copy of dataframe to keep changes contained within the function.
    df = input_df.copy()

    # Define the daily return column which is simple returns.
    daily_return_col = f"1d_{calendar}_simple_return"

    # We group the rows by ticker to ensure that the calculations don't leak across.
    group_col = "ticker"

    # Check if simple return is present to prevent duplciating efforts.
    if daily_return_col in df.columns:

        print(f"[INFO] {daily_return_col} exists: Proceeding")

    # Otherwise generate the simple return column using the returns from lagged price function.
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

        # Define the return column name for this branch.
        return_col = f"{return_type}_returns_{calendar}"

        # Create cumulative return column.
        df[return_col] = (
            # Group by ticker then select the daily returns for each group.
            df.groupby(group_col)[daily_return_col]
            # Use .transform() to apply a function to each group of returns and return 
            # a result wihtt he same length and index as the original dataframe allowing
            # it to easily be assigned to the column of the original dataframe.
            # Use lambda to define a small anonymous function wiht variable x.
            # Add 1 to the value and turn nulls into 0 then calculate cumulative growth
            # then subtract 1 to revert it back to cumulative return.
            # Then only keep values where x was not originally null.
            .transform(lambda x: ((1 + x.fillna(0)).cumprod() - 1).where(x.notna()))
        )

    # If return type is lagged.
    elif return_type == "lagged":

        print(f"[START] Calculating lagged returns. Days: {days}. Calendar: {calendar}.")
    
        # Use lagged value fucntion to find the return from x days ago.
        df = add_lagged_value(
            input_df = df,
            days = days,
            calendar = calendar,
            value_col = daily_return_col
        )

        # Define the column names to change and clean the names.
        lag_return_col = f"{daily_return_col}_{days}d_ago_{calendar}"

        final_return_col = f"{days}d_{calendar}_{return_type}_returns"

        # Check whether column is present.
        if lag_return_col not in df.columns:
            
            raise ValueError(f"[ERROR] Expected lag column missing: {lag_return_col}")
        
        # If column present then rename.
        else:
            df = df.rename(
                columns={
                    lag_return_col: final_return_col
                }
            )

    # Check if return type was one of the choices.
    else:

        raise ValueError(
            "[ERROR] Return type must be one of: 'cumulative', 'lagged'."
        )

    return df

# Combine all functions into a wrapper function to generate all functions.
def generate_return_features(
        input_df: pd.DataFrame,
        calendars: list[str],
        rolling_windows: list[int],
        lagged_windows: list[int]
        ) -> pd.DataFrame:
    
    # Create contained copy of dataframe.
    df = input_df.copy()

    # Call prepare_df function to prepare the dataframe.
    df = prepare_df(df)

    # Iterate through all the calendars inputted in the function.
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

def generate_moving_averages(
        input_df: pd.DataFrame,
        value_columns: list[str],
        windows: list[int],
        calendars: list[str]
        ) -> pd.DataFrame:

        df = input_df.copy()

        df = prepare_df(df)

        # Iterate through the list of windows defined.
        for window in windows:

            # Sanity check for a window that is less than 1 because that is not a moving average
            # but simply a return.
            if window < 1:

                raise ValueError("[ERROR] Invalid window size (n < 1) chosen for moving averages")

            # Iterate through the columns we want to generate moving average for.
            for column in value_columns:

                # Generate a count of the chosen column within each ticker group.
                counts = df.groupby("ticker")[column].count()

                # Sanity check for counts that are less than the window which a moving average
                # cannot be calculated for.
                if counts.min() < window:

                    print("[WARNING] Window range too large or number of values too small")
                    print(counts)

                # Iterate through the calendars defined in the calendar list.
                for calendar in calendars:

                    if calendar == "no_calendar":

                        # Define the moving average column name.
                        ma_col = f"{calendar}_{window}d_{column}_ma"
                        
                        # For no_calendar we simply assume every row is valid.
                        # For each ticker we take the values in the column.
                        # Rolling creates a rolling window over the last window 
                        # rows within each ticekr group.
                        # Min periods defines the minimum number of rows required to
                        # calculate a rolling window.
                        # Take the average of each rolling window.
                        # Reset the group index as using groupby creates a multiindex result, 
                        # leaving only the original index that allows it to be added back.
                        df[ma_col] = (
                            df.groupby("ticker")[column]
                            .rolling(window=window, min_periods=window)
                            .mean()
                            .reset_index(level = 0, drop = True)
                        )

                    elif calendar == "exchange_calendar" or calendar == "business_calendar":

                        # Will contain a list of columns that will be used to calculate moving average.
                        # moving average includes the current days value as window - 1 days prior.
                        value_cols = [column]

                        # Create empty list of temporary lagged column that we will use to drop and clean
                        # the dataframe.
                        temp_lag_cols = []

                        # Define name of moving averages column.
                        ma_col = f"{calendar}_{window}d_{column}_ma"

                        # Iterate through the numbers from 1 to the window.
                        # this is becuase 0 is the current column, then
                        # we create column from 1 till window - 1 giving us
                        # a window number of columns.
                        for lag in range(1, window):

                            # Generate lagged columns for each day of the window.
                            df = add_lagged_value(
                                input_df = df,
                                days = lag,
                                calendar = calendar,
                                value_col = column
                            )

                            # Define the lag column generated.
                            lag_col = f"{column}_{lag}d_ago_{calendar}"

                            # Append that column to the value columns.
                            value_cols.append(lag_col)

                            # As well as the temp column list.
                            temp_lag_cols.append(lag_col)

                        # Select rows from the lagged columns that don't have null values.
                        valid = df[value_cols].notna().all(axis=1)

                        # Set the column to numpy nulls.
                        df[ma_col] = np.nan

                        # For the rows that do not have any nulls across the columns, 
                        # we define the moving average column as the mean across the value columns.
                        df.loc[valid, ma_col] = (
                            df.loc[valid, value_cols].mean(axis=1)
                        )

                        # Clean dataframe and drop temp columns.
                        df = df.drop(columns = temp_lag_cols)
                    
                    # Sanity check chosen calendar type is valid.
                    else:

                        raise ValueError("[ERROR] Calendar must be one of: 'no_calendar', 'business_calendar', 'exchange_calendar'.")

        return df    

#--TECHNICAL / MODEL FEATURES--#

def calculate_ma_dependents(
        input_df: pd.DataFrame,
        calendar: str,
        ma_window: int,
        value_col: str, 
        feature: str # choose options like relative_volume or price_vs_ma20
        ) -> pd.DataFrame:
    
    df = input_df.copy()

    df = prepare_df(df)
    
    ma_col = f"{calendar}_{ma_window}d_{value_col}_ma"

    if ma_col in df.columns:

        print(f"[INFO] {ma_col} exists: Proceeding")
    
    else:

        generate_moving_averages(
            input_df = df,
            value_columns = [value_col],
            calendars = [calendar],
            windows = [ma_window]
        )
    
    feature_col = f"{feature}_{calendar}"

    df[feature_col] = np.nan

    valid = (
        df[value_col].notna()
        & df[ma_col].notna()
        & (df[ma_col] != 0)
    )

    df.loc[valid, feature_col] = df.loc[valid, feature_col] / df.loc[valid, ma_col] - 1

    return df

def calculate_rolling_volatility(
        input_df: pd.DataFrame,
        calendar: str,
        window: int,
    ) -> pd.DataFrame:

    df = input_df.copy()

    df = prepare_df(df)

    return_col = f"1d_{calendar}_simple_return"

    if return_col in df.columns:

        print(f"[INFO] {return_col} exists: Proceeding")
    
    else:

        calculate_return_from_lagged_price(
            days = 1,
            calendar = calendar,
            return_type = "simple"
        )
    
    vol_col = f"{calendar}_{window}d_rolling_volatility"

    df[vol_col] = (
        df.groupby("ticker")[return_col]
        .rolling(window = window, min_periods = window)
        .std()
        .reset_index(level = 0, drop = True)
    )

    return df

def add_drawdown(
        input_df: pd.DataFrame,
        value_col: str,
        calendar: str
        ) -> pd.DataFrame:

    running_max_col = f"{value_col}_running_max"

    drawdown_col = f"{value_col}_drawdown_{calendar}"

    df[running_max_col] = df.groupby("ticker")[value_col].cummax()

    df[drawdown_col] = df[value_col] / df[running_max_col] - 1

    df = df.drop(columns = [running_max_col], errors="ignore")

return df


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

if __name__ == "__main__":
    main()  

