USE mini_project2;

INSERT INTO mart_monthly_de_facto_population_per_time (ym, time_hour, de_facto_population) VALUES
('202601', '00', 1000000),
('202601', '01', 950000),
('202601', '02', 900000),
('202601', '03', 850000),
('202601', '04', 800000),
('202601', '05', 750000),
('202601', '06', 700000),
('202601', '07', 650000),
('202601', '08', 600000),
('202601', '09', 550000);

INSERT INTO mart_state_monthly (state_code, state_name, ym, avg_de_facto_population, weekday_avg_de_facto_population, weekend_avg_de_facto_population, cafe_count, de_facto_population_per_cafe) VALUES
('10101', 'State X', '202601', 750000, 700000, 800000, 10, 75000),
('10102', 'State Y', '202601', 600000, 550000, 650000, 8, 75000),
('10103', 'State Z', '202601', 900000, 850000, 950000, 12, 75000);  

INSERT INTO mart_state_hourly (state_code, state_name, ym, day_type, time_hour, avg_de_facto_population) VALUES
('10101', 'State X', '202601', 'weekday', '00', 1000000),
('10101', 'State X', '202601', 'weekday', '01', 950000),
('10101', 'State X', '202601', 'weekday', '02', 900000),
('10101', 'State X', '202601', 'weekday', '03', 850000),
('10101', 'State X', '202601', 'weekday', '04', 800000),
('10101', 'State X', '202601', 'weekday', '05', 750000),
('10101', 'State X', '202601', 'weekday', '06', 700000),
('10101', 'State X', '202601', 'weekday', '07', 650000),
('10101', 'State X', '202602', 'weekend', '08', 600000),
('10101', 'State X', '202602', 'weekend', '09', 550000);

INSERT INTO mart_priority_score (state_code, state_name, priority_score, rank, recent_3m_avg_de_facto_population, previous_3m_avg_de_facto_population, growth_rate, de_facto_population, living_population, activity_ratio, cafe_count, de_facto_population_per_cafe, condition_pop_per_cafe, condition_growth_rate, condition_activity_ratio) VALUES
('10101', 'State X', 95.5, 1, 750000, 700000, 0.0714, 550000, 500000, 0.9, 10, 55000, TRUE, TRUE, TRUE),
('10102', 'State Y', 85.0, 2, 600000, 580000, 0.0345, 450000, 400000, 0.8889, 8, 56250, TRUE, TRUE, FALSE),
('10103', 'State Z', 75.0, 3, 900000, 850000, 0.0588, 700000, 650000, 0.9286, 12, 58333.33, TRUE, TRUE, TRUE);
