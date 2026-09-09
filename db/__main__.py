from .build_mart import make_monthly_de_facto_population_per_time_mart, make_state_monthly_mart, make_state_hourly_mart, make_priority_score_mart
from collector.loader import make_engine, insert_data
from collector.client import make_logger

import pandas as pd
from sqlalchemy import text

def main():
    logger = make_logger()
    engine = make_engine()
    try:
        with engine.connect() as conn:
            de_facto_population_raw = pd.read_sql("SELECT * FROM de_facto_population_raw", conn)
            cafe_clean = pd.read_sql("SELECT * FROM cafe_clean", conn)
            state_dim = pd.read_sql("SELECT * FROM state_dim", conn)
            population_clean = pd.read_sql("SELECT * FROM population_clean", conn)
    finally:
        engine.dispose()

    # 1. 월별/시간대별 마트 생성
    mart_monthly_de_facto_population_per_time = make_monthly_de_facto_population_per_time_mart(de_facto_population_raw)
    insert_data(mart_monthly_de_facto_population_per_time, "mart_monthly_de_facto_population_per_time", logger)

    # 2. 지역별 월별 마트 생성
    mart_state_monthly = make_state_monthly_mart(de_facto_population_raw, cafe_clean, state_dim)
    insert_data(mart_state_monthly, "mart_state_monthly", logger)
    # 3. 지역별 시간대별 마트 생성
    mart_state_hourly = make_state_hourly_mart(de_facto_population_raw, state_dim)
    insert_data(mart_state_hourly, "mart_state_hourly", logger)

    # 4. 우선순위 점수 마트 생성
    priority_score_mart = make_priority_score_mart(mart_state_monthly, population_clean)
    insert_data(priority_score_mart, "mart_priority_score", logger)


if __name__ == "__main__":
    main()
