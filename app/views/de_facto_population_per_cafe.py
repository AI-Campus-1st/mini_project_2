import streamlit as st

from views.repository import load_mart_priority_score
from charts import make_population_per_cafe_chart

st.title("카페 1개당 생활인구")
st.caption("높을수록 생활하는 생활인구 수에 비해 카페 공급이 상대적으로 적다는 뜻")
st.info("카페 1개당 생활인구 수가 평균보다 높은 곳들을 우선으로 고려해야합니다.")

df = load_mart_priority_score()

st.plotly_chart(make_population_per_cafe_chart(df))
 