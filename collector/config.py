from datetime import datetime, timedelta
import pandas as pd
import requests
import os
from dotenv import load_dotenv

def config():
    # 수집 기간 6개월
    end_date = datetime.strptime("2026-06-30", "%Y-%m-%d")
    start_date = datetime.strptime("2026-01-01", "%Y-%m-%d")

    # 지역코드
    df = pd.read_csv('data/raw/소상공인시장진흥공단_상가(상권)정보_서울_202606.csv', encoding='utf-8')
    cafe_df = df[df['상권업종소분류명'] == '카페']
    cafe_df_clean = cafe_df[['상가업소번호', '상호명', '시군구명', '시군구코드']]
    area_codes = cafe_df_clean['시군구코드'].unique()

    # OPEN API 엔드포인트
    url = f'http://openapi.seoul.go.kr:8088/'
    tts = ["08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]  # 시간대 (00~23)


    return (start_date, end_date, area_codes, url, tts)