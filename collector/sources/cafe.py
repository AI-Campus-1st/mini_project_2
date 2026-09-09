import pandas as pd

def get_cafe_data():
    try:
        df = pd.read_csv('data/raw/소상공인시장진흥공단_상가(상권)정보_서울_202606.csv', encoding='utf-8')
        return df
    except FileNotFoundError:
        print("카페 데이터 파일을 찾을 수 없습니다.")
        return None