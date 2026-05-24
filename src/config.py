from pathlib import Path

# Path from Python's native library pathlib allows you to
# work with files and folder paths in a neater way than plain 
# strings. It allows concatenation of strings using / to create
# a path.


PROJECT_ROOT = Path(__file__).resolve().parents[1]

# __file__ is a special python variable that contains the path of 
# the current python file. In this case it would contain the path
# of the config.py file. Using .resolve() converts the path into 
# an absolute path rather than a relative path then .parents[1]
# gives you the directory of the current file where [0] is the 
# lowest (i.e., the folder holding the file itself), then [1] is 
# the folder holding the folder above that (in this case 
# /market-intelligence-pipeline) which we assign to the 
# PROJECT_ROOT variable.

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# we then define the paths of the various folders.

RAW_PRICES_FILE = RAW_DATA_DIR / "prices_raw.csv"
METADATA_FILE = RAW_DATA_DIR / "metadata.csv"

# we also define the path of the output prices_raw file.

TICKERS = ["SPY", "GLD", "TLT", "SNDK", "MU", "RPI.L", "NKE"]
START_DATE = "2018-01-01" 
END_DATE = None

# Variables we are going to import into the ingest.py file.

DATABASE_PATH = DATA_DIR / "market.duckdb"

# Variables we are going to import into transform.py file.

EXPECTED_DTYPES = {
    "date": "datetime64[us]",
    "ticker": "str",
    "open": "float64",
    "high": "float64",
    "low": "float64",
    "close": "float64",
    "adj_close": "float64",
    "volume": "int64",
    "downloaded_at": "datetime64[us]",
    "source": "str"
}

NON_NULL_COLS = ["date", "ticker", "open", "high", "low",
                  "close", "adj_close", "volume" ]

DUPLICATE_KEY_COLS = ["date", "ticker"]

ALLOW_ZERO_COLS = ["volume"]

NON_ZERO_COLS = ["open", "high", "low", "close", "adj_close"]

TICKER_COL = "ticker"

DATE_COL = "date"

EARLIEST_FIRST = True

# Variables to import into features.py file.

EXCHANGE_TO_CALENDAR = {
    "NMS": "NASDAQ",
    "NGM": "NASDAQ",
    "NCM": "NASDAQ",
    "NYQ": "NYSE",
    "ASE": "NYSE",
    "PCX": "NYSE",      # NYSE Arca, often ETFs like SPY/GLD
    "LSE": "LSE",
    "JPX": "JPX",
    "TOR": "TSX",
    "ASX": "ASX",
    "FRA": "XFRA",
}

## RETURNS CONFIG

CALENDARS = ["no_calendar", "business_calendar", "exchange_calendar"]

ROLLING_WINDOWS = [7, 30]

LAGGED_WINDOWS = [1, 5]