import streamlit as st

from charts import condition_checker, make_condition_score

def make_tab():
    sidebar = st.navigation(
        {
            "메뉴": [
                st.Page("views/home.py", title="**홈**", default=True),
                st.Page("views/priority_score.py", title="**우선순위 점수**", url_path="priority_score"),
                st.Page("views/de_facto_population_per_cafe.py", title="카페 1개당 생활인구", url_path="de_facto_population_per_cafe"),
                st.Page("views/de_facto_population_increase.py", title="최근 생활인구 증가율", url_path="de_facto_population_increase"),
                st.Page("views/activity_ratio.py", title="생활인구 활동 배율", url_path="activity_ratio"),
                st.Page("views/monthly_de_facto_population.py", title="월별 영업시간대(8~22시) 평균 생활인구", url_path="monthly_de_facto_population"),
                st.Page("views/weekend_concentration.py", title="주말 집중도", url_path="weekend_concentration")
            ]
        },
        position="sidebar",
        expanded=True,
    )
    return sidebar

def make_kpi(df):
    col1, col2, col3 = st.columns(3)
    df_all_condition = condition_checker(df)
    col1.metric("3 조건 충족 자치구 수", f"{len(df_all_condition)}개")
    col2.metric("전체 자치구 수", f"{len(df)}개")
    col3.metric("조건을 모두 충족하는 자치구", f"{list(df_all_condition['state_name'])[0]}")

    st.write("모든 조건을 충족하는 자치구는 송파구 단 하나이나, 다른 자치구들도 조건을 일부 충족하고 있습니다.")
    
    df_with_condition_score = make_condition_score(df)
    st.write("자치구별 조건 충족 수:")
    with st.expander("자치구별 조건 충족 수 보기"):
        st.dataframe(df_with_condition_score[["state_name", "condition_score"]].sort_values(by="condition_score", ascending=False).reset_index(drop=True),
                     column_config={
                         "state_name": "자치구",
                         "condition_score": "조건 충족 수"
                     })

    st.write("조건을 전부 충족하지 않았어도 우선순위 점수가 높은 자치구:")
    with st.expander("우선순위 점수 높은 자치구 보기"):
        st.dataframe(df[["state_name", "priority_score"]].sort_values(by="priority_score", ascending=False).reset_index(drop=True),
                     column_config={
                         "state_name": "자치구",
                         "priority_score": "우선순위 점수"
                     })
    st.write("우선순위 점수 상으로는 노원구가 송파구보다 높으나, 송파구가 모든 조건을 충족하여 최종 출점 후보로 선정되었습니다.")
    st.write("송파구를 제외한 2, 3순위 출점 후보는 노원구와 구로구입니다.")