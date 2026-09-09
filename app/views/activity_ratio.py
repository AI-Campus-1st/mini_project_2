import streamlit as st

from views.repository import load_mart_priority_score
from charts import make_activity_ratio_chart

st.title("생활인구 활동 배율")
st.caption("생활인구 활동 배율 = 생활인구 / 거주인구")
st.info("즉 1배를 초과하면 생활인구가 거주인구보다 많다는 의미입니다.  \n영업시간에 사람들이 많이 몰리는 자치구 일수록 생활인구 활동 배율이 높게 나타납니다.")


df = load_mart_priority_score()
st.plotly_chart(make_activity_ratio_chart(df))

st.write("미니 프로젝트 1에서 찾았던 중구, 종로구 등 중심 상권 자치구들이 생활인구 활동 배율이 높게 나타났습니다.")
