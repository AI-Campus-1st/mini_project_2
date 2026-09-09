import streamlit as st
import pandas as pd

from views.repository import load_mart_state_monthly
from charts import make_weekend_concentration_chart

st.title("주말 집중도")
st.caption("지역별 주말 집중도를 비교하는 보조 지표입니다.")
st.info("배율이 높을 수록 주말에 사람이 많이 몰리는 지역입니다.  \n출점 후 전략 같은 것들을 세울 때 참고할 수 있습니다.")

df = load_mart_state_monthly()
selected_ym = st.selectbox(
    "월 선택",
    options=sorted(df["ym"].astype(str).unique()),
    format_func=lambda x: pd.to_datetime(x, format="%Y%m").strftime("%Y-%m")
)

st.plotly_chart(make_weekend_concentration_chart(df, ym=selected_ym))