import pandas as pd

''' Bronze Layer '''
day1 = pd.read_csv("events_day1.csv")
day2 = pd.read_csv("events_day2.csv")
advertisers = pd.read_csv("advertisers.csv")

#Handling schema drift Rename media_cost → spend
day2 = day2.rename(columns={
    "media_cost":"spend"
})

# Add missing column to Day1
day1["viewability"] = None

# Now both datasets have same columns
bronze = pd.concat([day1, day2], ignore_index=True)

bronze.to_csv("bronze_events.csv",index=False)

'''Silver Layer'''
# Remove Exact Duplicates
silver = bronze.drop_duplicates()

# Keep Latest ingest_time - Convert timestamp
silver["ingest_time"] = pd.to_datetime(silver["ingest_time"])

#sort the dataframe by ingest_time
silver = silver.sort_values("ingest_time")

#Keep latest event_id
silver = silver.drop_duplicates(
        subset=["event_id"],
        keep="last"
)

#Convert timestamps to UTC
silver["event_time"] = pd.to_datetime(
    silver["event_time"],
    utc=True
)

#Quarantine Bad Records
bad_rows = silver[
    (silver["spend"] < 0)
]

good_rows = silver[
    silver["spend"] >=0
]

bad_rows.to_csv("quarantine.csv",index=False)
good_rows.to_csv("silver.csv",index=False)

'''Gold Layer 
Join advertiser dimension'''
gold = good_rows.merge(
    advertisers,
    on="advertiser_id",
    how="left"
)


# convert INR to USD
gold.loc[
    gold.currency=="INR",
    "spend"
] /= 85

gold.loc[
    gold.currency=="INR",
    "currency"
]="USD"


# Daily Spend
gold["date"] = pd.to_datetime(
    gold["event_time"]
).dt.date

daily = gold.groupby(
    ["advertiser_id","date"]
).agg(
    daily_spend=("spend","sum"),
    event_count=("event_id","count")
).reset_index()

result = run_dq_checks(
    silver,
    rules
)

print(result)