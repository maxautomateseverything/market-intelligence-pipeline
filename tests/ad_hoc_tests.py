import pandas_market_calendars as mcal
import pandas as pd

# Calculate expected previous trading date per calendar lookup
# This is respective to the specific exchange.

calendar_name = "NYSE"
start_date = "2018-01-01"
end_date = "2026-01-01"


# Get the market calendar object
# For example if calendar_name is "NYSE" it gets the NYSE trading calendar
calendar = mcal.get_calendar(calendar_name)

# We build the trading schedule between start and end date.
schedule = calendar.schedule(
    start_date = start_date,
    end_date = end_date
)

print(schedule)

# Creates a pandas series containing the trading dates.
# schedule.index contains the dates from the market schedule.
# converts the index into datetime values.
# tz_localise removes the timezone information, making the dates timezone-naive.
trading_days = pd.Series(
    pd.to_datetime(schedule.index).tz_localize(None),
    name="date"
)

print(trading_days)

lookup = pd.DataFrame({
    "date": trading_days,
    "expected_previous_trading_Date": trading_days.shift(1),
    "calendar": calendar_name
})

print(lookup)
