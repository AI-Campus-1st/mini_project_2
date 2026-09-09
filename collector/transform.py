import pandas as pd
import numpy as np

def transform_de_facto_population(df):
    try:
        man0_idx = df.columns.get_loc('M00')
        man70_idx = df.columns.get_loc('M70')
        female0_idx = df.columns.get_loc('F00')
        female70_idx = df.columns.get_loc('F70')

        male_df = df.iloc[:, man0_idx:man70_idx+1]
        female_df = df.iloc[:, female0_idx:female70_idx+1]

        male_df = male_df.apply(pd.to_numeric, errors='coerce')
        female_df = female_df.apply(pd.to_numeric, errors='coerce')

        male_sum_df = male_df.sum(axis=1)
        female_sum_df = female_df.sum(axis=1)   

        df_clean = df[["YMD", "TT", "H_DNG_CD", "SPOP"]].copy()
        df_clean['male_de_facto_population'] = male_sum_df
        df_clean['female_de_facto_population'] = female_sum_df
        df_clean.rename(columns={"YMD": "ymd", "TT": "time_hour", "H_DNG_CD": "state_code", "SPOP": "de_facto_population"}, inplace=True)
        return df_clean.round(2)
    
    except Exception as e:
        print(f"Error transforming de facto population data: {e}")
        return None

def transform_population(df):
    try:
        seoul_df = df[df['시도명'] == '서울특별시']
        population_df = seoul_df.drop(columns=['기준연월', '시도명', '읍면동명'])
        population_df = population_df.copy()
        population_grouped = population_df.groupby('시군구명').sum().reset_index()

        man0_idx = population_grouped.columns.get_loc('0세남자')
        man110_idx = population_grouped.columns.get_loc('110세이상 남자')
        female0_idx = population_grouped.columns.get_loc('0세여자')
        female110_idx = population_grouped.columns.get_loc('110세이상 여자')

        male_df = population_grouped.iloc[:, man0_idx:man110_idx+1]
        female_df = population_grouped.iloc[:, female0_idx:female110_idx+1]

        avg_male_df = (male_df.mul(np.arange(0, 111), axis=1).sum(axis=1) / male_df.sum(axis=1)).round(1)
        avg_female_df = (female_df.mul(np.arange(0, 111), axis=1).sum(axis=1) / female_df.sum(axis=1)).round(1)
        avg_age_df = ((male_df.mul(np.arange(0, 111), axis=1).sum(axis=1) + female_df.mul(np.arange(0, 111), axis=1).sum(axis=1)) / (male_df.sum(axis=1) + female_df.sum(axis=1))).round(1)

        population_df_clean = population_grouped.copy()[['시군구명', '계', '남자', '여자']]
        population_df_clean.rename(columns={'시군구명': 'state_name', '계': 'total_population', '남자': 'male_population', '여자': 'female_population'}, inplace=True)

        population_df_clean['male_average_age'] = avg_male_df
        population_df_clean['female_average_age'] = avg_female_df
        population_df_clean['average_age'] = avg_age_df

        # 남자 추가
        population_df_clean['children_population'] = male_df.iloc[:, male_df.columns.get_loc('0세남자'):male_df.columns.get_loc('20세남자')+1].sum(axis=1)
        population_df_clean['youth_population'] = male_df.iloc[:, male_df.columns.get_loc('21세남자'):male_df.columns.get_loc('40세남자')+1].sum(axis=1)
        population_df_clean['adult_population'] = male_df.iloc[:, male_df.columns.get_loc('41세남자'):male_df.columns.get_loc('60세남자')+1].sum(axis=1)
        population_df_clean['senior_population'] = male_df.iloc[:, male_df.columns.get_loc('61세남자'):male_df.columns.get_loc('80세남자')+1].sum(axis=1)
        population_df_clean['elderly_population'] = male_df.iloc[:, male_df.columns.get_loc('81세남자'):male_df.columns.get_loc('95세남자')+1].sum(axis=1)

        #여자 추가
        population_df_clean['children_population'] += female_df.iloc[:, female_df.columns.get_loc('0세여자'):female_df.columns.get_loc('20세여자')+1].sum(axis=1)
        population_df_clean['youth_population'] += female_df.iloc[:, female_df.columns.get_loc('21세여자'):female_df.columns.get_loc('40세여자')+1].sum(axis=1)
        population_df_clean['adult_population'] += female_df.iloc[:, female_df.columns.get_loc('41세여자'):female_df.columns.get_loc('60세여자')+1].sum(axis=1)
        population_df_clean ['senior_population'] += female_df.iloc[:, female_df.columns.get_loc('61세여자'):female_df.columns.get_loc('80세여자')+1].sum(axis=1)
        population_df_clean['elderly_population'] += female_df.iloc[:, female_df.columns.get_loc('81세여자'):female_df.columns.get_loc('95세여자')+1].sum(axis=1)    

        return population_df_clean
    
    except Exception as e:
        print(f"Error transforming population data: {e}")
        return None

def transform_cafe(df):
    try:
        cafe_df = df[df['상권업종소분류명'] == '카페']
        cafe_df_clean = cafe_df[['상가업소번호', '상호명', '시군구명', '시군구코드']]
        cafe_df_clean.rename(columns={'상가업소번호': 'cafe_code', '상호명': 'cafe_name', '시군구명': 'state_name', '시군구코드': 'state_code'}, inplace=True)
        return cafe_df_clean
    
    except Exception as e:
        print(f"Error transforming cafe data: {e}")
        return None

def make_state_dim(df):
    try:
        state_dim_df = df[['state_code', 'state_name']].drop_duplicates().reset_index(drop=True)
        return state_dim_df
    
    except Exception as e:
        print(f"Error creating state_dim data: {e}")
        return None