DELETE FROM mart_population_summary;

WITH base AS (
    SELECT region_code, substr(collected_at, 1, 10) AS summary_date
    FROM raw_flow_population
    UNION
    SELECT region_code, substr(collected_at, 1, 10) AS summary_date
    FROM raw_resident_population
),
flow_daily AS (
    SELECT
        region_code,
        substr(collected_at, 1, 10) AS summary_date,
        MAX(flow_population) AS flow_population
    FROM raw_flow_population
    GROUP BY region_code, substr(collected_at, 1, 10)
),
resident_daily AS (
    SELECT
        region_code,
        substr(collected_at, 1, 10) AS summary_date,
        MAX(resident_population) AS resident_population
    FROM raw_resident_population
    GROUP BY region_code, substr(collected_at, 1, 10)
)
INSERT INTO mart_population_summary (
    region_code,
    summary_date,
    flow_population,
    resident_population,
    total_population,
    updated_at
)
SELECT
    base.region_code,
    base.summary_date,
    COALESCE(flow_daily.flow_population, 0) AS flow_population,
    COALESCE(resident_daily.resident_population, 0) AS resident_population,
    COALESCE(flow_daily.flow_population, 0) + COALESCE(resident_daily.resident_population, 0) AS total_population,
    CURRENT_TIMESTAMP
FROM base
LEFT JOIN flow_daily
    ON flow_daily.region_code = base.region_code
   AND flow_daily.summary_date = base.summary_date
LEFT JOIN resident_daily
    ON resident_daily.region_code = base.region_code
   AND resident_daily.summary_date = base.summary_date;
