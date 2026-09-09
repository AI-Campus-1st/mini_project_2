import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import asyncio, httpx

from .sources.cafe import get_cafe_data
from .sources.flow_pop import get_de_facto_population
from .sources.resident_pop import get_living_population

from .client import make_logger
from .config import config
from .loader import insert_data
from .transform import transform_de_facto_population, transform_cafe, transform_population, make_state_dim

async def main():
    # config
    logger = make_logger()
    start_date, end_date, area_codes, url, tts = config()
    delta = timedelta(days=1)
    sem = asyncio.Semaphore(5)  # limit concurrent requests to 5

    load_dotenv()
    api_key = os.getenv("OPEN_API_KEY")

    # Start Logging
    logger.info("Starting the data collection process...")

    # 카페 데이터
    df_cafe = get_cafe_data()
    logger.info("카페 데이터 수집완료")
    df_cafe_clean = transform_cafe(df_cafe)
    logger.info("카페 데이터 전처리 완료")
    insert_data(df_cafe_clean, "cafe_clean", logger)

    # state_dim 데이터
    state_dim_df = make_state_dim(df_cafe_clean)
    insert_data(state_dim_df, "state_dim", logger)

    # 거주인구 데이터
    df_population = get_living_population()
    logger.info("거주인구 수집완료")
    df_population_raw = transform_population(df_population)
    logger.info("거주인구 전처리 완료")
    insert_data(df_population_raw, "population_clean", logger)

    # 생활인구 데이터/de_facto_population

    de_facto_raw = []

    # testing
    # start_date = datetime.strptime("2026-01-01", "%Y-%m-%d")
    # end_date = datetime.strptime("2026-01-01", "%Y-%m-%d")

    # area_codes = ["11545"]

    # Open API 호출 및 데이터 수집
    async with httpx.AsyncClient(timeout = 30.0) as client:
        async def collect_one(day, code, tt):
            try:
                data = await get_de_facto_population(
                    client=client,
                    sem=sem,
                    api_key=api_key,
                    url=url,
                    day=day,
                    tt=tt,
                    code=code,
                )

                # HTTP 200이어도 예상 데이터가 없으면 실패로 기록
                rows = data["Spop250mLocalResdJachi"]["row"]

                logger.info(
                    "수집 완료: date=%s, code=%s, time=%s",
                    day, code, tt,
                )
                return rows

            except Exception as e:
                logger.error(
                    "수집 실패: date=%s, code=%s, time=%s, error=%s",
                    day, code, tt, type(e).__name__,
                )
                return []

        current_date = start_date

        while current_date <= end_date:
            tasks = [collect_one(current_date, code, tt) for code in area_codes for tt in tts]
            results = await asyncio.gather(*tasks)

            for rows in results:
                de_facto_raw.extend(rows)

            current_date += delta

    df = pd.DataFrame(de_facto_raw)
    df.to_csv("data/raw/de_facto_population_raw.csv", index=False)
    clean_de_facto_df = transform_de_facto_population(df)
    clean_de_facto_df.to_csv("data/clean/de_facto_population_raw.csv", index=False)
    insert_data(clean_de_facto_df, "de_facto_population_raw", logger)

    # Finished logging
    logger.info("Data collection process completed.")

if __name__ == "__main__":
    asyncio.run(main())