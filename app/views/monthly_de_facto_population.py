import streamlit as st

from views.repository import load_mart_monthly_de_facto_population_per_time
from charts import make_monthly_de_facto_population_chart

st.title("월별 영업시간대(8~22시) 평균 생활인구")
st.caption("월별·시간대별 생활인구 현황을 확인하는 보조 지표입니다.")
st.info("제일 사람이 많이 몰리는 시간대는 13시~15시를 주목할 필요가 있습니다.  \n출점 후 고용 계획 수립에 참고할 수 있습니다.")

df = load_mart_monthly_de_facto_population_per_time()
st.plotly_chart(make_monthly_de_facto_population_chart(df))
