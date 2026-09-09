import pandas as pd

def get_living_population():
    try:
        df = pd.read_csv('data/raw/행정안전부_지역별&#40;행정동&#41; 성별 연령별 주민등록 인구수_20260630.csv', encoding='cp949')
        return df
    except FileNotFoundError:
        print("거주인구 파일을 찾을 수 없습니다.")
        return None