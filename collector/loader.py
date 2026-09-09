import pymysql
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL

def connect():
    load_dotenv()
    conn = pymysql.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        charset='utf8mb4'
    )
    return conn

def make_engine():
    load_dotenv()
    db_url = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
        query={"charset": "utf8mb4"},
    )

    return create_engine(db_url)

def insert_data(df, table_name, logger):
    BATCH_SIZE = 500
    # change dataframe to list of dictionaries for insertion
    data = df.to_dict(orient='records')

    try:        
        # Insert data into the specified table
        if table_name == "de_facto_population_raw":
            insert_query = """
                INSERT INTO de_facto_population_raw (ymd, time_hour, state_code, de_facto_population, male_de_facto_population, female_de_facto_population)
                VALUES (%(ymd)s, %(time_hour)s, %(state_code)s, %(de_facto_population)s, %(male_de_facto_population)s, %(female_de_facto_population)s)
                ON DUPLICATE KEY UPDATE
                    de_facto_population = VALUES(de_facto_population),
                    male_de_facto_population = VALUES(male_de_facto_population),
                    female_de_facto_population = VALUES(female_de_facto_population)
                """
        elif table_name == "population_clean":
            insert_query = """
                INSERT INTO population_clean (state_name, total_population, male_population, female_population, male_average_age, female_average_age, average_age, children_population, youth_population, adult_population, senior_population, elderly_population)
                VALUES (%(state_name)s, %(total_population)s, %(male_population)s, %(female_population)s, %(male_average_age)s, %(female_average_age)s, %(average_age)s, %(children_population)s, %(youth_population)s, %(adult_population)s, %(senior_population)s, %(elderly_population)s)
                ON DUPLICATE KEY UPDATE
                    total_population = VALUES(total_population),
                    male_population = VALUES(male_population),
                    female_population = VALUES(female_population),
                    male_average_age = VALUES(male_average_age),
                    female_average_age = VALUES(female_average_age),
                    average_age = VALUES(average_age),
                    children_population = VALUES(children_population),
                    youth_population = VALUES(youth_population),
                    adult_population = VALUES(adult_population),
                    senior_population = VALUES(senior_population),
                    elderly_population = VALUES(elderly_population)
                """
        elif table_name == "cafe_clean":
            insert_query = """
                INSERT INTO cafe_clean (cafe_code, cafe_name, state_name, state_code)
                VALUES (%(cafe_code)s, %(cafe_name)s, %(state_name)s, %(state_code)s)
                ON DUPLICATE KEY UPDATE
                    cafe_name = VALUES(cafe_name),
                    state_name = VALUES(state_name),
                    state_code = VALUES(state_code)
                """
        elif table_name == "state_dim":
            insert_query = """
                INSERT INTO state_dim (state_code, state_name)
                VALUES (%(state_code)s, %(state_name)s)
                ON DUPLICATE KEY UPDATE
                    state_name = VALUES(state_name)
                """
        elif table_name == "mart_monthly_de_facto_population_per_time":
            insert_query = """
                INSERT INTO mart_monthly_de_facto_population_per_time (ym, time_hour, de_facto_population)
                VALUES (%(ym)s, %(time_hour)s, %(de_facto_population)s)
                ON DUPLICATE KEY UPDATE
                    de_facto_population = VALUES(de_facto_population)
                """
        elif table_name == "mart_state_monthly":
            insert_query = """
                INSERT INTO mart_state_monthly (state_code, state_name, ym, avg_de_facto_population, weekday_avg_de_facto_population, weekend_avg_de_facto_population, cafe_count, de_facto_population_per_cafe)
                VALUES (%(state_code)s, %(state_name)s, %(ym)s, %(avg_de_facto_population)s, %(weekday_avg_de_facto_population)s, %(weekend_avg_de_facto_population)s, %(cafe_count)s, %(de_facto_population_per_cafe)s)
                ON DUPLICATE KEY UPDATE
                    avg_de_facto_population = VALUES(avg_de_facto_population),
                    weekday_avg_de_facto_population = VALUES(weekday_avg_de_facto_population),
                    weekend_avg_de_facto_population = VALUES(weekend_avg_de_facto_population),
                    cafe_count = VALUES(cafe_count),
                    de_facto_population_per_cafe = VALUES(de_facto_population_per_cafe)
                """
        elif table_name == "mart_state_hourly":
            insert_query = """
                INSERT INTO mart_state_hourly (state_code, state_name, ym, day_type, time_hour, avg_de_facto_population)
                VALUES (%(state_code)s, %(state_name)s, %(ym)s, %(day_type)s, %(time_hour)s, %(avg_de_facto_population)s)
                ON DUPLICATE KEY UPDATE
                    avg_de_facto_population = VALUES(avg_de_facto_population)
                """
        elif table_name == "mart_priority_score":
            insert_query = """
                INSERT INTO mart_priority_score (state_code, state_name, priority_score, rank, recent_3m_avg_de_facto_population, previous_3m_avg_de_facto_population, growth_rate, de_facto_population, living_population, activity_ratio, cafe_count, de_facto_population_per_cafe, condition_pop_per_cafe, condition_growth_rate, condition_activity_ratio)
                VALUES (%(state_code)s, %(state_name)s, %(priority_score)s, %(rank)s, %(recent_3m_avg_de_facto_population)s, %(previous_3m_avg_de_facto_population)s, %(growth_rate)s, %(de_facto_population)s, %(living_population)s, %(activity_ratio)s, %(cafe_count)s, %(de_facto_population_per_cafe)s, %(condition_pop_per_cafe)s, %(condition_growth_rate)s, %(condition_activity_ratio)s)
                ON DUPLICATE KEY UPDATE
                    priority_score = VALUES(priority_score),
                    rank = VALUES(rank),
                    recent_3m_avg_de_facto_population = VALUES(recent_3m_avg_de_facto_population),
                    previous_3m_avg_de_facto_population = VALUES(previous_3m_avg_de_facto_population),
                    growth_rate = VALUES(growth_rate),
                    de_facto_population = VALUES(de_facto_population),
                    living_population = VALUES(living_population),
                    activity_ratio = VALUES(activity_ratio),
                    cafe_count = VALUES(cafe_count),
                    de_facto_population_per_cafe = VALUES(de_facto_population_per_cafe),
                    condition_pop_per_cafe = VALUES(condition_pop_per_cafe),
                    condition_growth_rate = VALUES(condition_growth_rate),
                    condition_activity_ratio = VALUES(condition_activity_ratio)
                """
        # Execute the insert query
        with connect() as conn:
            for i in range(0, len(data), BATCH_SIZE):
                cursor = conn.cursor()
                cursor.executemany(insert_query, data[i:i+BATCH_SIZE])
                conn.commit()
                logger.info(f"Inserted batch {i//BATCH_SIZE + 1} into {table_name} successfully.")
        logger.info(f"Data inserted into {table_name} successfully.")
    except Exception as e:
        logger.error(f"Error inserting data into {table_name}: {e}")