INSERT OR IGNORE INTO raw_flow_population (
    region_code,
    collected_at,
    flow_population
) VALUES
    ('11110', '2026-08-18T09:00:00', 1200),
    ('11110', '2026-08-18T18:00:00', 1850),
    ('11680', '2026-08-18T09:00:00', 980);

INSERT OR IGNORE INTO raw_resident_population (
    region_code,
    collected_at,
    resident_population
) VALUES
    ('11110', '2026-08-18T00:00:00', 950),
    ('11680', '2026-08-18T00:00:00', 1100);
