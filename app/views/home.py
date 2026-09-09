import streamlit as st
import pandas as pd

from components import make_kpi
from views.repository import load_mart_priority_score

st.title("송파구, 노원구, 구로구 순으로 카페 출점 후보 선정")

st.divider()

st.markdown("## 출점 후보 선정 조건")
st.markdown("1. **카페 1개당 생활인구**가 평균보다 높은 자치구")
st.markdown("2. **최근 생활인구 증가율**이 늘어나고 있는 자치구")
st.markdown("3. **생활인구 활동 배율**이 평균보다 높은 자치구")

st.divider()

df = load_mart_priority_score()
make_kpi(df)

st.divider()

st.markdown("출점이 결정된 후에는 **월별 영업시간대(8~22시) 평균 생활인구**를 분석하여 매장 운영 전략을 수립하고 **주말 집중도**를 고려해 마케팅 전략을 수립할 수 있습니다.")
