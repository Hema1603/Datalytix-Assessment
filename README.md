# Datalytix-Assessment
Bronze stores raw data after schema alignment.
Silver removes duplicates, keeps the latest ingest_time, standardizes timestamps to UTC, and quarantines invalid rows.
Gold joins advertiser metadata, converts INR to USD using a fixed exchange rate (1 USD = 85 INR), and creates daily spend and event-count aggregates
