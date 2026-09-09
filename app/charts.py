import pandas as pd
import plotly.express as px


def make_monthly_de_facto_population_chart(df):
    df["time_hour"] = pd.to_numeric(df["time_hour"], errors="coerce")
    df["de_facto_population"] = pd.to_numeric(df["de_facto_population"], errors="coerce")
    df["month"] = pd.to_datetime(df["ym"].astype(str), format="%Y%m").dt.strftime("%Y-%m")

    df = df.sort_values(["month", "time_hour"])

    fig = px.line(
        df,
        x="time_hour",
        y="de_facto_population",
        color="month",
        markers=True,
        labels={
            "time_hour": "시간대",
            "de_facto_population": "평균 생활인구(명)",
            "month": "월",
        },
        title="월별 영업시간대(8~22시) 평균 생활인구",
        template="plotly_white",
    )

    fig.update_xaxes(
        tickvals=list(range(8, 23)),
        ticktext=[f"{hour}시" for hour in range(8, 23)],
    )
    fig.update_yaxes(
        tickformat=",", 
        autorange=True
    )
    fig.update_layout(
        hovermode="x unified",
        legend_title_text="월",
    )
    fig.update_traces(
        hovertemplate="%{x}: %{y:,.0f}명"
    )

    return fig

def make_activity_ratio_chart(df):
    data = df[["state_name", "activity_ratio"]].copy()

    data["activity_ratio"] = pd.to_numeric(data["activity_ratio"], errors="coerce")

    data = data.sort_values("activity_ratio")

    fig = px.bar(
        data,
        x="activity_ratio",
        y="state_name",
        orientation="h",
        text="activity_ratio",
        labels={
            "activity_ratio": "생활인구 활동 배율(배)",
            "state_name": "자치구",
        },
        title="자치구별 생활인구 활동 배율",
        template="plotly_white"
    )
    fig.update_traces(
        texttemplate="%{x:.2f}배",
        textposition="outside",
        hovertemplate=(
            "%{y} : 생활인구 활동 배율: %{x:.2f}배"
        )
    )
    fig.add_vline(
        x=1,
        line_dash="dash",
        line_color="yellow",
        annotation_text="기준 1배",
        annotation_position="top"
    )
    fig.add_vline(
            x=data["activity_ratio"].mean(),
            line_dash="dash",
            line_color="red",
            annotation_text="평균",
            annotation_position="top"
        )
    fig.update_layout(height=800)

    return fig

def make_population_per_cafe_chart(df):
    data = df[["state_name", "de_facto_population_per_cafe"]].copy()

    x = "de_facto_population_per_cafe"

    data[x] = pd.to_numeric(data[x], errors="raise")
    data = data.sort_values(x)

    fig = px.bar(
        data,
        x=x,
        y="state_name",
        text=x,
        labels={
            x: "카페 1개당 생활인구",
            "state_name": "자치구",
        },
        title="자치구별 카페 1개당 생활인구",
        template="plotly_white"
    )

    fig.update_traces(
        texttemplate="%{x:,.0f}명",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "%{y} > 카페 1개당 생활인구: "
            "%{x:.1f}명"
        )
    )
    fig.add_vline(
        x=data[x].mean(),
        line_dash="dash",
        line_color="red",
        annotation_text="평균",
        annotation_position="top"
    )
    fig.update_layout(height=800)

    return fig

def make_population_growth_rate_chart(df):
    data = df[["state_name", "growth_rate"]].copy()

    data["growth_rate"] = pd.to_numeric(data["growth_rate"], errors="coerce")
    data = data.sort_values("growth_rate")

    data["change"] = data["growth_rate"].apply(lambda value: "증가" if value > 0 else "감소" if value < 0 else "변동 없음")

    fig = px.bar(
        data,
        x="growth_rate",
        y="state_name",
        color="change",
        orientation="h",
        text="growth_rate",
        color_discrete_map={
            "증가": "#2563EB",
            "감소": "#EF4444",
            "변동 없음": "#9CA3AF",
        },
        labels={
            "growth_rate": "생활인구 증가율",
            "state_name": "자치구",
            "change": "변동",
        },
        title="자치구별 최근 생활인구 증가율",
        template="plotly_white"
    )

    fig.update_traces(
        texttemplate="%{x:.2f}%",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=("%{y} >생활인구 증가율: %{x:.2f}%")
    )
    fig.add_vline(
        x=0,
        line_dash="solid",
        line_color="white",
    )
    fig.update_xaxes(ticksuffix="%")
    fig.update_layout(
        height=800,
        legend=dict(traceorder="reversed")
    )

    return fig

def make_weekend_concentration_chart(df, ym):
    data = df[
        [
            "ym",
            "state_name",
            "weekday_avg_de_facto_population",
            "weekend_avg_de_facto_population",
        ]
    ].copy()

    data["ym"] = data["ym"].astype(str)

    selected_ym = str(ym)
    data = data.loc[data["ym"].eq(selected_ym)].copy()

    weekday = "weekday_avg_de_facto_population"
    weekend = "weekend_avg_de_facto_population"

    for column in [weekday, weekend]:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data["weekend_ratio"] = (data[weekend] / data[weekday])
    data = data.sort_values("weekend_ratio")

    month_label = pd.to_datetime(
        selected_ym, format="%Y%m"
    ).strftime("%Y년 %m월")

    fig = px.bar(
        data,
        x="weekend_ratio",
        y="state_name",
        orientation="h",
        text="weekend_ratio",
        custom_data=[weekday, weekend],
        labels={
            "weekend_ratio": "주말 집중도",
            "state_name": "자치구",
        },
        title=f"자치구별 주말 집중도 ({month_label})",
        template="plotly_white",
    )

    fig.update_traces(
        texttemplate="%{x:.2f}배",
        textposition="outside",
        hovertemplate=(
            "%{y}<br>"
            "주말 집중도: %{x:.2f}배<br>"
            "평일 평균 생활인구: %{customdata[0]:,.0f}명<br>"
            "주말 평균 생활인구: %{customdata[1]:,.0f}명"
            "<extra></extra>"
        ),
    )
    fig.add_vline(
        x=1,
        line_dash="dash",
        line_color="red",
        annotation_text="1배",
        annotation_position="top",
    )
    fig.update_layout(height=800)

    return fig

def make_priority_score_chart(df):
    data = df[
        [
            "state_name",
            "priority_score",
            "rank",
            "de_facto_population_per_cafe",
            "growth_rate",
            "activity_ratio",
        ]
    ].copy()

    numeric_columns = [
        "priority_score",
        "rank",
        "de_facto_population_per_cafe",
        "growth_rate",
        "activity_ratio",
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data = data.sort_values(["priority_score", "state_name"])

    fig = px.bar(
        data,
        x="priority_score",
        y="state_name",
        orientation="h",
        text="priority_score",
        custom_data=[
            "rank",
            "de_facto_population_per_cafe",
            "growth_rate",
            "activity_ratio",
        ],
        labels={
            "priority_score": "우선순위 점수",
            "state_name": "자치구",
        },
        title="자치구별 우선순위 점수",
        template="plotly_white",
    )

    fig.update_traces(
        marker_color="#2563EB",
        texttemplate="%{x:.1f}점",
        textposition="outside",
        hovertemplate=(
            "%{y}<br>"
            "순위: %{customdata[0]:.0f}위<br>"
            "우선순위 점수: %{x:.1f}점<br>"
            "카페 1개당 생활인구: %{customdata[1]:,.1f}명<br>"
            "최근 생활인구 증가율: %{customdata[2]:.2f}%<br>"
            "생활인구 활동 배율: %{customdata[3]:.2f}배"
        ),
    )
    fig.update_xaxes(range=[0, 100], dtick=20)
    fig.update_layout(height=800)

    return fig

def make_condition_score(df):
    data = df.copy()

    condition_columns = [
        "condition_pop_per_cafe",
        "condition_growth_rate",
        "condition_activity_ratio",
    ]

    data["condition_score"] = data[condition_columns].eq(1).sum(axis=1).astype(int)

    return data

def condition_checker(df):
    df_all_condition = df[(df["condition_pop_per_cafe"] == 1) & (df["condition_growth_rate"] == 1) & (df["condition_activity_ratio"] == 1)]
    return df_all_condition