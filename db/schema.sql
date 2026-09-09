CREATE DATABASE IF NOT EXISTS mini_project2;
USE mini_project2;

CREATE TABLE IF NOT EXISTS de_facto_population_raw (
    ymd DATE NOT NULL,
    time_hour VARCHAR(2) NOT NULL,
    state_code VARCHAR(10) NOT NULL,
    de_facto_population BIGINT NOT NULL,
    male_de_facto_population BIGINT NOT NULL,
    female_de_facto_population BIGINT NOT NULL,
    
    PRIMARY KEY (state_code, ymd, time_hour),
    INDEX idx_ymd (ymd),
    INDEX idx_state (state_code)
);

CREATE TABLE IF NOT EXISTS cafe_clean (
    cafe_code VARCHAR(20) NOT NULL, 
    cafe_name VARCHAR(100) NOT NULL, 
    state_name VARCHAR(20) NOT NULL,
    state_code VARCHAR(5) NOT NULL,

    PRIMARY KEY (cafe_code),
    INDEX idx_state_name (state_name),
    INDEX idx_state_code (state_code)
);

CREATE TABLE IF NOT EXISTS population_clean (
    state_name VARCHAR(50) NOT NULL,
    total_population BIGINT NOT NULL,
    male_population BIGINT NOT NULL,
    female_population BIGINT NOT NULL,
    male_average_age FLOAT NOT NULL,
    female_average_age FLOAT NOT NULL,
    average_age FLOAT NOT NULL,
    children_population INT NOT NULL,
    youth_population INT NOT NULL,
    adult_population INT NOT NULL,
    senior_population INT NOT NULL,
    elderly_population INT NOT NULL,

    PRIMARY KEY (state_name),
    INDEX idx_state_name (state_name)
);

CREATE TABLE IF NOT EXISTS state_dim (
    state_code VARCHAR(10) NOT NULL,
    state_name VARCHAR(50) NOT NULL,

    PRIMARY KEY (state_code),
    INDEX idx_state_name (state_name)
);

CREATE TABLE IF NOT EXISTS mart_monthly_de_facto_population_per_time (
    ym VARCHAR(6) NOT NULL,
    time_hour VARCHAR(2) NOT NULL,
    de_facto_population INT NOT NULL,

    PRIMARY KEY (ym, time_hour),
    INDEX idx_ym (ym),
    INDEX idx_time_hour (time_hour)
);

CREATE TABLE IF NOT EXISTS mart_state_monthly (
    state_code VARCHAR(10) NOT NULL,
    state_name VARCHAR(50) NOT NULL,
    ym VARCHAR(6) NOT NULL,

    avg_de_facto_population FLOAT NOT NULL,
    weekday_avg_de_facto_population FLOAT NOT NULL,
    weekend_avg_de_facto_population FLOAT NOT NULL,

    cafe_count INT NOT NULL,
    de_facto_population_per_cafe FLOAT NOT NULL,

    PRIMARY KEY (state_code, ym),
    INDEX idx_state_monthly (state_code, ym)
);

CREATE TABLE IF NOT EXISTS mart_state_hourly (
    state_code VARCHAR(10) NOT NULL,
    state_name VARCHAR(50) NOT NULL,
    ym CHAR(6) NOT NULL,
    day_type VARCHAR(10) NOT NULL,
    time_hour VARCHAR(2) NOT NULL,
    avg_de_facto_population FLOAT NOT NULL,

    PRIMARY KEY (state_code, ym, day_type, time_hour),
    INDEX idx_hourly_period (ym, time_hour)
);

CREATE TABLE IF NOT EXISTS mart_priority_score (
    state_code VARCHAR(10) NOT NULL,
    state_name VARCHAR(50) NOT NULL,
    priority_score FLOAT NOT NULL,
    rank INT NOT NULL,

    recent_3m_avg_de_facto_population FLOAT NOT NULL,
    previous_3m_avg_de_facto_population FLOAT NOT NULL,
    growth_rate FLOAT NOT NULL,

    de_facto_population FLOAT NOT NULL,
    living_population FLOAT NOT NULL,
    activity_ratio FLOAT NOT NULL,

    cafe_count INT NOT NULL,
    de_facto_population_per_cafe FLOAT NOT NULL,

    condition_pop_per_cafe BOOLEAN NOT NULL,
    condition_growth_rate BOOLEAN NOT NULL,
    condition_activity_ratio BOOLEAN NOT NULL,

    PRIMARY KEY (state_code),
    INDEX idx_state_priority_rank (state_code, priority_score, rank)
);
