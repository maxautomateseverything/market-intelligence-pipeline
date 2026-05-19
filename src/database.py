import duckdb
import pandas as pd

from src.config import DATABASE_PATH

# Function to check whether table exists.
# Use parameterised ? to avoid SQL injection.
# Use try adn finally to close connection even if SQL query errors.
def table_exists (table_name: str) -> bool:

    con = duckdb.connect(DATABASE_PATH)

    try:
        # Look insiude DuckDB metadata table for raw_prices table.
        # Fetch the first result from that query.
        # Get the first value from the returned tuple.
        # Convert into boolean taking True if greater than 0 and False if not.
        exists = con.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = ?  
        """,
            [table_name]).fetchone()[0] > 0
        
        return exists
    
    finally:
        con.close()

# Create all database tables needed for market pipeline
# Function is safe to run multiple times through us of IF NOT EXISTS
def create_tables() -> None:

    # Connect to DuckDB
    print("[START] Connecting to database...")
    con = duckdb.connect(DATABASE_PATH)

    if table_exists("raw_prices"):
        print("[INFO] Table raw_prices already exists")

    else:
    # Create the raw_prices table.
        print("[START] Creating raw_prices table...")
        con.execute("""
            CREATE TABLE IF NOT EXISTS raw_prices (
                    date DATE,
                    ticker VARCHAR,
                    open DOUBLE,
                    high DOUBLE,
                    low DOUBLE,
                    close DOUBLE,
                    adj_close DOUBLE,
                    volume BIGINT,
                    downloaded_at TIMESTAMP,
                    source VARCHAR,

                    UNIQUE(date, ticker, source)
                )               
                    """)
        print("[DONE] Table raw_prices created")

    if table_exists("ticker_metadata"):
        print("[INFO] Table ticker_metadata already exists")

    else:
        print("[START] Creating ticker_metadata table...")
        con.execute("""
            CREATE TABLE IF NOT EXISTS ticker_metadata (
                ticker VARCHAR,
                exchange VARCHAR,
                quote_type VARCHAR,
                currency VARCHAR,
                timezone VARCHAR,
                short_name VARCHAR,
                
                UNIQUE(ticker)
                )
                    """)

        print("[DONE] Table ticker_metadata created")

    if table_exists("clean_prices"):
        print("[INFO] Table clean_prices already exists")

    else:    
    # Create the clean_prices table.
        print("[START] Creating clean_prices table...")
        con.execute("""
            CREATE TABLE IF NOT EXISTS clean_prices (
                date DATE,
                ticker VARCHAR,
                open DOUBLE,
                high DOUBLE,
                low DOUBLE,
                close DOUBLE,
                adj_close DOUBLE,
                volume BIGINT,
                downloaded_at TIMESTAMP,
                source VARCHAR,

                UNIQUE(date, ticker)
            )
                """)
        print("[DONE] Table clean_prices created")

    # Create the price_features table.


    # Create the model_predictions table.

    # Create the pipeline_runs table.
    
    # Close the connection
    con.close()
    print("[DONE] Tables created successfully")


def insert_metadata(metadata_df: pd.DataFrame) -> None:

    print("[START] Insert metadata")
    con = duckdb.connect(DATABASE_PATH)

    df = metadata_df.copy()

    columns = ["ticker","exchange","quote_type","currency","timezone","short_name"]

    df = df[columns]

    con.register("df", df)

    # Insert the data into the table.
    # We insert using BY NAME which inserts into the respective columsn 
    # by matching column names.
    # We use the ON CONFLICT logic and exclude the old data values and
    # update with the new data values.
    print("[START] Inserting data")
    con.execute("""
        INSERT INTO ticker_metadata BY NAME
        SELECT
            ticker,
            exchange,
            quote_type,
            currency,
            timezone,
                short_name
        FROM df
        ON CONFLICT (ticker) DO UPDATE SET
                exchange = EXCLUDED.exchange,
                quote_type = EXCLUDED.quote_type,
                currency = EXCLUDED.currency,
                timezone = EXCLUDED.timezone,
                short_name = EXCLUDED.short_name            
                """)
    print("[DONE] Data inserted")
    
    con.close()
    print("[DONE] Tables updated")



# Insert pandas datafrmae into raw_prices table.
# Assume that create_tables() has been run and raw_prices_df contains raw data.
def insert_raw_prices(raw_prices_df: pd.DataFrame) -> None:

    # Connect to DuckDB
    print("[START] Connecting to database...")
    con = duckdb.connect(DATABASE_PATH)

    # Inspect incoming columns from dataframe.
    print("[INSPECT] Incoming columns:")
    print(raw_prices_df.columns.tolist())

    # Create copy inside the function that allows editing of dataframe 
    # withou altering the original outside of the function.
    print("[START] Copying dataframe locally")
    df = raw_prices_df.copy()
    print("[DONE] Copied dataframe locally")

    # Standardise column names as SQL prefers snake_case names.
    print("[START] Standardise and select columns")
    df = df.rename(columns={
        "Date": "date",
        "Adj Close": "adj_close",
        "Close": "close",
        "High": "high",
        "Low": "low",
        "Open": "open",
        "Volume": "volume",
        "ticker": "ticker",
        "downloaded_at": "downloaded_at",
        "source": "source",
    })

    # Select the required columns
    raw_columns = [
        "date",
        "ticker",
        "open",
        "high",
        "low",
        "close",
        "adj_close",
        "volume",
        "downloaded_at",
        "source",
    ]

    df = df[raw_columns]
    print("[DONE] Standardised and renamed columns")
    print("[INSPECT] Selected columns:")
    print(raw_columns)

    # Load dataframe to query in INSERT query
    print("[START] Registering dataframe")
    con.register("df", df)
    print("[DONE] Registered dataframe")

    # Insert the data into the table.
    # We insert using BY NAME which inserts into the respective columsn 
    # by matching column names.
    # We use the ON CONFLICT logic and exclude the old data values and
    # update with the new data values.
    print("[START] Inserting data")
    con.execute("""
        INSERT INTO raw_prices BY NAME
        SELECT
            date,
            ticker,
            open,
            high,
            low,
            close,
            adj_close,
            volume,
            downloaded_at,
            source
        FROM df
        ON CONFLICT (date, ticker, source) DO UPDATE SET
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                adj_close = EXCLUDED.adj_close,
                volume = EXCLUDED.volume,
                downloaded_at = EXCLUDED.downloaded_at                
                """)
    print("[DONE] Data inserted")
    
    con.close()
    print("[DONE] Tables updated")

def read_table(table_name: str) -> pd.DataFrame:

    print("[START] Connecting to database...")
    con = duckdb.connect(DATABASE_PATH)

    print(f"[START] Reading {table_name}")
    df = con.sql(f"""
        SELECT *
        FROM {table_name}
                 """).df()
    
    con.close()
    print(f"[DONE] Read {table_name}")
    
    return df

def read_order_table(table_name: str) -> pd.DataFrame:

    print("[START] Connecting to database...")
    con = duckdb.connect(DATABASE_PATH)

    print(f"[START] Reading {table_name}")
    df = con.sql(f"""
        SELECT *
        FROM {table_name}
        ORDER BY ticker, date
                 """).df()
    
    con.close()
    print(f"[DONE] Read {table_name}")
    
    return df
