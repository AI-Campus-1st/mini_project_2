PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS raw_flow_population (
    region_code TEXT NOT NULL,
    collected_at TEXT NOT NULL,
    flow_population INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (region_code, collected_at)
);

CREATE TABLE IF NOT EXISTS raw_resident_population (
    region_code TEXT NOT NULL,
    collected_at TEXT NOT NULL,
    resident_population INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (region_code, collected_at)
);

CREATE TABLE IF NOT EXISTS mart_population_summary (
    region_code TEXT NOT NULL,
    summary_date TEXT NOT NULL,
    flow_population INTEGER NOT NULL DEFAULT 0,
    resident_population INTEGER NOT NULL DEFAULT 0,
    total_population INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (region_code, summary_date)
);

CREATE INDEX IF NOT EXISTS idx_raw_flow_population_date
    ON raw_flow_population (collected_at);

CREATE INDEX IF NOT EXISTS idx_raw_resident_population_date
    ON raw_resident_population (collected_at);
