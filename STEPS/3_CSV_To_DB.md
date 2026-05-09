## Installing DuckDB

The DuckDB python client can be installed v:

```
pip install duckdb
```

Or using conda:

```
conda install python-duckdb -c conda-forge
```


## DuckDB create_tables() function:

DuckDB offer multiple  fucntions after connecting to a DB.

```con.execute()``` we use when running SQL statements in scripts/pipelines.

```con.sql()``` can also be used in the same contexts as con.sql but we will use this specifically for returning a DuckDB relation.

```con.table()``` is used for referecing an existing table.

The following outlines the various data types that can be used:
- INT: whole numbers (32-bit).
- BIGINT: store larger integers (64-bit).
- VARCAHR(n): store text up to n characters.
- VARCHAR: general variable length text.
- TEXT: longer free form text.
- DATE: dates.
- DATETIME: date and time.
- TIMESTAMP: timestamp.
- DECIMAL(m, n): Floating number with n decimal points with m digits allowed in total.
- DOUBLE: floating point decimal number with no limit.

Primary and foreign keys:
- Not every table needs a primary and foreign key, especially in a analytics/data warehouse style project where raw data needs to be stored as its true state which keys can cause issues in doing.
- The more important concept here is unique grain, e.g., unique rows in raw_prices table indicated by unique ticker + date + downloaded_at values.
- We therefore include the UNIQUE() constraint in creating the table to enforce this. Using this also allows us to insert non-duplciate data by using conflict handling.

## DuckDB insert_raw_prices(df) function:

We take the dataframe as an input rather than the CSV because the dataframe is already loaded. 
- This avoids unecessary work of saving it as a CSV then loading it again.
- It keeps the pipeline steps flexible allowing us to work with data from multiple sources and reuse the same function if we convert the data into a dataframe before hand.
- Allows testing with a test dataframe if needed.

We use this flow:

```
yfinance API
   ↓
DataFrame
   ↓
save CSV backup
   ↓
insert DataFrame into DuckDB
```

Instead of this flow:

```
yfinance API
   ↓
CSV
   ↓
read CSV again
   ↓
insert into DuckDB
```

When doing this we make 2 assumptions:
- The create_tables() function has already been run so that raw_prices table already exists.
- The dataframe is already contained in raw_prices_df.

The process we use is as follos:
1. We connect to the database.
2. We inspect the incoming feilds in the dataframe.
3. Make a local copy of the dataframe to df.
4. Standaradise and select the requried columns.
5. Load the dataframe to be queried using SQL.
6. INSERT the data to the DB.
7. Use ON CONFLICT based on the UNIOUE constraint to update any duplicate rows
    with the new values.


## DuckDB read_table() function:

We also created a function to read the tables we have created and return the tables in a dataframe format.
