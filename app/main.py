import streamlit as st

from components import make_tab

st.set_page_config(
    page_title="카페 상권 분석 대시보드",
    layout="wide",
    initial_sidebar_state="expanded",
)

page = make_tab()
page.run()
