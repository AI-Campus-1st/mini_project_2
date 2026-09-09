import numpy as np
import pandas as pd

def make_monthly_de_facto_population_per_time_mart(df_raw):
    df = df_raw[["ymd", "time_hour", "de_facto_population"]].copy()

    df["ymd"] = pd.to_datetime(df["ymd"]).dt.normalize()
    df["time_hour"] = pd.to_numeric(df["time_hour"], errors="coerce")
    df = df.loc[df["time_hour"].between(8, 22)].copy()
    df["de_facto_population"] = pd.to_numeric(df["de_facto_population"], errors="coerce")

    daily_hourly = (df.groupby(["ymd", "time_hour"], as_index=False)["de_facto_population"].sum())

    daily_hourly["ym"] = daily_hourly["ymd"].dt.strftime("%Y%m")

    mart = (daily_hourly.groupby(["ym", "time_hour"], as_index=False)["de_facto_population"].mean())
    mart["de_facto_population"] = mart["de_facto_population"].round().astype(int)
    mart["time_hour"] = mart["time_hour"].astype(int).astype(str).str.zfill(2)

    return mart.sort_values(by=["ym", "time_hour"]).reset_index(drop=True)

def make_state_monthly_mart(df_raw, df_cafe, df_state):
    df = df_raw[["ymd", "time_hour", "state_code", "de_facto_population"]].copy()
    cafes = df_cafe[["cafe_code", "state_code"]].copy()
    states = df_state[["state_code", "state_name"]].copy()

    df["ymd"] = pd.to_datetime(df["ymd"]).dt.normalize()
    df["time_hour"] = pd.to_numeric(df["time_hour"], errors="coerce")
    df = df.loc[df["time_hour"].between(8, 22)].copy()
    df["de_facto_population"] = pd.to_numeric(df["de_facto_population"], errors="coerce")

    # 자치구별 하루 영업시간 평균
    daily = (
        df.groupby(["state_code", "ymd"], as_index=False)
        .agg(
            daily_avg=("de_facto_population", "mean"),
        )
    )

    daily["ym"] = daily["ymd"].dt.strftime("%Y%m")
    is_weekday = daily["ymd"].dt.dayofweek < 5

    daily["weekday_avg"] = daily["daily_avg"].where(is_weekday)
    daily["weekend_avg"] = daily["daily_avg"].where(~is_weekday)

    monthly = (
        daily.groupby(["state_code", "ym"], as_index=False)
        .agg(
            avg_de_facto_population=("daily_avg", "mean"),
            weekday_avg_de_facto_population=("weekday_avg", "mean"),
            weekend_avg_de_facto_population=("weekend_avg", "mean"),
        )
    )

    cafe_counts = (
        cafes.groupby("state_code")["cafe_code"]
        .nunique()
        .rename("cafe_count")
        .reset_index()
    )

    mart = monthly.merge(
        states,
        on="state_code",
        how="left",
        validate="many_to_one",
    )

    mart = mart.merge(
        cafe_counts,
        on="state_code",
        how="left",
        validate="many_to_one",
    )

    mart["cafe_count"] = mart["cafe_count"].astype(int)

    mart["de_facto_population_per_cafe"] = (
        mart["avg_de_facto_population"] / mart["cafe_count"]
    )

    columns = [
        "state_code",
        "state_name",
        "ym",
        "avg_de_facto_population",
        "weekday_avg_de_facto_population",
        "weekend_avg_de_facto_population",
        "cafe_count",
        "de_facto_population_per_cafe",
    ]

    return mart[columns].sort_values(["state_code", "ym"]).reset_index(drop=True)

def make_state_hourly_mart(df_raw, df_state):
    df = df_raw[["state_code", "ymd", "time_hour", "de_facto_population"]].copy()
    states = df_state[["state_code", "state_name"]].copy()

    df["ymd"] = pd.to_datetime(df["ymd"], errors="coerce")
    df["time_hour"] = pd.to_numeric(df["time_hour"], errors="coerce")
    df = df.loc[df["time_hour"].between(8, 22)].copy()
    df["de_facto_population"] = pd.to_numeric(
        df["de_facto_population"], errors="coerce"
    )

    df["ym"] = df["ymd"].dt.strftime("%Y%m")

    df["day_type"] = "weekday"
    df.loc[df["ymd"].dt.dayofweek >= 5, "day_type"] = "weekend"

    df["time_hour"] = df["time_hour"].astype(int).astype(str).str.zfill(2)

    mart = (
        df.groupby(
            ["state_code", "ym", "day_type", "time_hour"],
            as_index=False,
        )
        .agg(
            avg_de_facto_population=("de_facto_population", "mean")
        )
    )

    # 4. 지역 이름 결합
    mart = mart.merge(
        states,
        on="state_code",
        how="left",
        validate="many_to_one",
    )

    columns = [
        "state_code",
        "state_name",
        "ym",
        "day_type",
        "time_hour",
        "avg_de_facto_population",
    ]

    return mart[columns].sort_values(["state_code", "ym", "day_type", "time_hour"]).reset_index(drop=True)

def make_priority_score_mart(df_state_monthly, df_population):
    end_ym = "202606"
    monthly = df_state_monthly.copy()
    population = df_population[["state_name", "total_population"]].copy()

    monthly["month"] = pd.to_datetime(
        monthly["ym"].astype(str),
        format="%Y%m",
        errors="raise",
    ).dt.to_period("M")

    end_month = pd.to_datetime(
        end_ym, format="%Y%m", errors="raise"
    ).to_period("M")

    periods = pd.period_range(end=end_month, periods=6, freq="M")
    previous_months = periods[:3]
    recent_months = periods[3:]

    monthly = monthly[monthly["month"].isin(periods)].copy()

    for column in ["avg_de_facto_population", "cafe_count"]:
        monthly[column] = pd.to_numeric(
            monthly[column], errors="coerce"
        )

    population["total_population"] = pd.to_numeric(
        population["total_population"], errors="coerce"
    )

    # 2. 최근 3개월 / 직전 3개월 월평균의 산술평균
    recent = (
        monthly[monthly["month"].isin(recent_months)]
        .groupby("state_code")["avg_de_facto_population"]
        .mean()
        .rename("recent_3m_avg_de_facto_population")
    )

    previous = (
        monthly[monthly["month"].isin(previous_months)]
        .groupby("state_code")["avg_de_facto_population"]
        .mean()
        .rename("previous_3m_avg_de_facto_population")
    )

    mart = pd.concat([recent, previous], axis=1).reset_index()

    latest = monthly.loc[
        monthly["month"].eq(end_month),
        ["state_code", "state_name", "cafe_count"],
    ]

    mart = mart.merge(
        latest,
        on="state_code",
        how="left",
        validate="one_to_one",
    )

    mart = mart.merge(
        population,
        on="state_name",
        how="left",
        validate="many_to_one",
    ).rename(columns={"total_population": "living_population"})

    mart["cafe_count"] = mart["cafe_count"].astype(int)

    # 4. 주요 지표 계산
    mart["growth_rate"] = (
        ((mart["recent_3m_avg_de_facto_population"] - mart["previous_3m_avg_de_facto_population"]) / mart["previous_3m_avg_de_facto_population"]) * 100
    )

    mart["de_facto_population"] = (
        mart["recent_3m_avg_de_facto_population"]
    )

    mart["activity_ratio"] = (
        mart["de_facto_population"] / mart["living_population"]
    )

    mart["de_facto_population_per_cafe"] = (
        mart["de_facto_population"] / mart["cafe_count"]
    )

    def percent_rank(series):
        if len(series) <= 1:
            return pd.Series(0.0, index=series.index)

        return (series.rank(method="min") - 1) / (len(series) - 1)

    mart["priority_score"] = 100 * (
        0.5 * percent_rank(mart["de_facto_population_per_cafe"])
        + 0.3 * percent_rank(mart["growth_rate"])
        + 0.2 * percent_rank(mart["activity_ratio"])
    )

    mean_pop_per_cafe = mart["de_facto_population_per_cafe"].mean()

    mart["condition_pop_per_cafe"] = (
        mart["de_facto_population_per_cafe"] > mean_pop_per_cafe
    )
    mart["condition_growth_rate"] = mart["growth_rate"] > 0
    mart["condition_activity_ratio"] = mart["activity_ratio"] > 1

    mart["rank"] = (
        mart["priority_score"]
        .rank(method="min", ascending=False)
        .astype(int)
    )

    columns = [
        "state_code",
        "state_name",
        "priority_score",
        "rank",
        "recent_3m_avg_de_facto_population",
        "previous_3m_avg_de_facto_population",
        "growth_rate",
        "de_facto_population",
        "living_population",
        "activity_ratio",
        "cafe_count",
        "de_facto_population_per_cafe",
        "condition_pop_per_cafe",
        "condition_growth_rate",
        "condition_activity_ratio",
    ]

    return mart[columns].sort_values(["rank", "state_code"]).reset_index(drop=True)
    