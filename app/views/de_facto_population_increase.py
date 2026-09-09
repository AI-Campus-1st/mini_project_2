import streamlit as st

from views.repository import load_mart_priority_score
from charts import make_population_growth_rate_chart

st.title("최근 생활인구 증가율")
st.caption("최근 3개월과 이전 3개월의 생활인구를 비교한 페이지입니다.")
st.info("증가한 자치구들은 생활인구가 늘어나고 있으니 카페의 잠재수요도 높아질 가능성이 있습니다.  \n다른 곳들에 비해 종로구가 생활인구 증가율이 높습니다.")

df = load_mart_priority_score()

st.plotly_chart(make_population_growth_rate_chart(df))
