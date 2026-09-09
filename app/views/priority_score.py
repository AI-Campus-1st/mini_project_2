import streamlit as st

from views.repository import load_mart_priority_score
from charts import make_priority_score_chart

st.title("우선순위 점수")
st.caption("우선순위 점수 = (카페 1개당 생활인구 x 0.5) + (최근 생활인구 증가율 x 0.3) + (생활인구 활동 배율 x 0.2)")
st.info("우선순위 점수는 각 자치구의 상권 잠재력을 평가하기 위한 지표입니다.  \n점수가 높을수록 상권 잠재력이 높다는 의미입니다.")

df = load_mart_priority_score()
st.plotly_chart(make_priority_score_chart(df))