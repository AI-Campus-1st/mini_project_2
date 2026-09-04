"""Streamlit application entry point."""

import streamlit as st

st.set_page_config(page_title="mini_project_2", layout="wide")

st.title("mini_project_2 대시보드 스캐폴드")
st.write("수집기, DB 계층, 대시보드 계층을 연결하기 위한 기본 진입점을 제공합니다.")
st.markdown(
    """
    - `collector/`: 데이터 수집 파이프라인
    - `db/`: 원본/마트 스키마와 집계 SQL
    - `app/`: Streamlit 대시보드
    """
)
