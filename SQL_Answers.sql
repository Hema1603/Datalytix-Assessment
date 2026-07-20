-- 7-Day Rolling Average
SELECT
advertiser_id,
date,
daily_spend,

AVG(daily_spend)
OVER(
PARTITION BY advertiser_id
ORDER BY date
ROWS BETWEEN 6 PRECEDING
AND CURRENT ROW
) rolling_avg,

100*
(
daily_spend-
LAG(daily_spend)
OVER(
PARTITION BY advertiser_id
ORDER BY date
)
)
/
LAG(daily_spend)
OVER(
PARTITION BY advertiser_id
ORDER BY date
)
AS pct_change

FROM gold_events;


-- Longest Active Streak
WITH cte AS
(
SELECT *,
ROW_NUMBER()
OVER(
PARTITION BY advertiser_id
ORDER BY date
) rn
FROM gold_events
),

grp AS
(
SELECT *,
DATEADD(day,-rn,date) grp
FROM cte
)

SELECT
advertiser_id,
COUNT(*) streak
FROM grp
GROUP BY advertiser_id,grp;

-- Merge Statement
MERGE INTO silver s
USING incoming i
ON s.event_id=i.event_id

WHEN MATCHED
AND i.ingest_time>s.ingest_time
THEN UPDATE SET *
  
WHEN NOT MATCHED
THEN INSERT *;
