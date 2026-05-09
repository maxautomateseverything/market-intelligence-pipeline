## Overall Flow:
```
Start script
   ↓
main()
   ↓
download_prices(TICKERS)
   ↓
For each ticker:
   - download data from yfinance
   - skip if empty
   - reset Date index
   - add ticker column
   - add downloaded_at column
   - add source column
   - store DataFrame
   ↓
combine all ticker DataFrames
   ↓
save_raw_prices(prices)
   ↓
create raw data folder if needed
   ↓
save CSV file
   ↓
print summary
```

# Files Used:
- config.py
- ingest.py