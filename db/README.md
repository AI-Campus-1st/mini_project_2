# 데이터베이스 스키마

## 테이블 목록

| 테이블 | 용도 | 한 행의 기준 | 기본키 |
| --- | --- | --- | --- |
| `de_facto_population_raw` | 일별·시간대별 생활인구 | 자치구 × 날짜 × 시간대 | `state_code, ymd, time_hour` |
| `cafe_clean` | 카페 기본 정보 | 카페 1개 | `cafe_code` |
| `population_clean` | 자치구별 거주인구 | 자치구명 | `state_name` |
| `state_dim` | 자치구 코드·이름 매핑 | 자치구 코드 | `state_code` |
| `mart_monthly_de_facto_population_per_time` | 월별·시간대별 생활인구 | 월 × 시간대 | `ym, time_hour` |
| `mart_state_monthly` | 자치구별 월간 생활인구·카페 지표 | 자치구 × 월 | `state_code, ym` |
| `mart_state_hourly` | 자치구별 평일·주말 시간대 지표 | 자치구 × 월 × 일 유형 × 시간대 | `state_code, ym, day_type, time_hour` |
| `mart_priority_score` | 자치구별 우선순위와 조건 충족 여부 | 자치구 | `state_code` |

## 1. de_facto_population_raw

| 컬럼 | SQL 타입 | 설명 |
| --- | --- | --- |
| `ymd` | `DATE` | 기준 날짜 |
| `time_hour` | `VARCHAR(2)` | 기준 시간대 |
| `state_code` | `VARCHAR(10)` | 자치구 코드 |
| `de_facto_population` | `BIGINT` | 전체 생활인구 |
| `male_de_facto_population` | `BIGINT` | 남성 생활인구 |
| `female_de_facto_population` | `BIGINT` | 여성 생활인구 |

- PK: `(state_code, ymd, time_hour)`
- 인덱스: `idx_ymd (ymd)`, `idx_state (state_code)`

## 2. cafe_clean

| 컬럼 | SQL 타입 | 설명 |
| --- | --- | --- |
| `cafe_code` | `VARCHAR(20)` | 카페 식별 코드 |
| `cafe_name` | `VARCHAR(100)` | 카페 이름 |
| `state_name` | `VARCHAR(20)` | 자치구 이름 |
| `state_code` | `VARCHAR(5)` | 자치구 코드 |

- PK: `(cafe_code)`
- 인덱스: `idx_state_name (state_name)`, `idx_state_code (state_code)`

## 3. population_clean

| 컬럼 | SQL 타입 | 설명 |
| --- | --- | --- |
| `state_name` | `VARCHAR(50)` | 자치구 이름 |
| `total_population` | `BIGINT` | 전체 거주인구 |
| `male_population` | `BIGINT` | 남성 거주인구 |
| `female_population` | `BIGINT` | 여성 거주인구 |
| `male_average_age` | `FLOAT` | 남성 평균 연령 |
| `female_average_age` | `FLOAT` | 여성 평균 연령 |
| `average_age` | `FLOAT` | 전체 평균 연령 |
| `children_population` | `INT` | 아동 인구 |
| `youth_population` | `INT` | 청소년 인구 |
| `adult_population` | `INT` | 성인 인구 |
| `senior_population` | `INT` | senior 연령 구간 인구 |
| `elderly_population` | `INT` | elderly 연령 구간 인구 |


- PK: `(state_name)`
- 인덱스: `idx_state_name (state_name)`

## 4. state_dim

| 컬럼 | SQL 타입 | 설명 |
| --- | --- | --- |
| `state_code` | `VARCHAR(10)` | 자치구 코드 |
| `state_name` | `VARCHAR(50)` | 자치구 이름 |

- PK: `(state_code)`
- 인덱스: `idx_state_name (state_name)`

## 5. mart_monthly_de_facto_population_per_time

자치구 구분 없이 월별·시간대별 생활인구 지표를 저장한다.

| 컬럼 | SQL 타입 | 설명 |
| --- | --- | --- |
| `ym` | `VARCHAR(6)` | 기준 월 |
| `time_hour` | `VARCHAR(2)` | 기준 시간대 |
| `de_facto_population` | `INT` | 월별·시간대별 평균 생활인구 |

- PK: `(ym, time_hour)`
- 인덱스: `idx_ym (ym)`, `idx_time_hour (time_hour)`

## 6. mart_state_monthly

자치구별 월평균 생활인구와 카페 대비 인구 지표를 저장한다.

| 컬럼 | SQL 타입 | 설명 |
| --- | --- | --- |
| `state_code` | `VARCHAR(10)` | 자치구 코드 |
| `state_name` | `VARCHAR(50)` | 자치구 이름 |
| `ym` | `VARCHAR(6)` | 기준 월 |
| `avg_de_facto_population` | `FLOAT` | 평균 생활인구 |
| `weekday_avg_de_facto_population` | `FLOAT` | 평일 평균 생활인구 |
| `weekend_avg_de_facto_population` | `FLOAT` | 주말 평균 생활인구 |
| `cafe_count` | `INT` | 카페 수 |
| `de_facto_population_per_cafe` | `FLOAT` | 카페 1개당 생활인구 |

- PK: `(state_code, ym)`
- 인덱스: `idx_state_monthly (state_code, ym)`

## 7. mart_state_hourly

자치구·월·일 유형별 시간대 평균 생활인구를 저장한다.

| 컬럼 | SQL 타입 | 설명 |
| --- | --- | --- |
| `state_code` | `VARCHAR(10)` | 자치구 코드 |
| `state_name` | `VARCHAR(50)` | 자치구 이름 |
| `ym` | `CHAR(6)` | 기준 월 |
| `day_type` | `VARCHAR(10)` | 평일·주말 등 일 유형 |
| `time_hour` | `VARCHAR(2)` | 기준 시간대 |
| `avg_de_facto_population` | `FLOAT` | 평균 생활인구 |

- PK: `(state_code, ym, day_type, time_hour)`
- 인덱스: `idx_hourly_period (ym, time_hour)`

## 8. mart_priority_score

자치구별 분석 지표, 우선순위 점수, 세 가지 조건 충족 여부를 저장한다. 기준월 컬럼이 없어 같은 자치구의 기간별 점수를 별도 행으로 보관할 수 없다.

| 컬럼 | SQL 타입 | 설명 |
| --- | --- | --- |
| `state_code` | `VARCHAR(10)` | 자치구 코드 |
| `state_name` | `VARCHAR(50)` | 자치구 이름 |
| `priority_score` | `FLOAT` | 우선순위 점수 |
| `rank` | `INT` | 우선순위 순위 |
| `recent_3m_avg_de_facto_population` | `FLOAT` | 최근 3개월 평균 생활인구 |
| `previous_3m_avg_de_facto_population` | `FLOAT` | 직전 3개월 평균 생활인구 |
| `growth_rate` | `FLOAT` | 생활인구 증가율 |
| `de_facto_population` | `FLOAT` | 분석에 사용하는 생활인구 |
| `living_population` | `FLOAT` | 비교 기준 거주인구 |
| `activity_ratio` | `FLOAT` | 생활인구 활동 배율 |
| `cafe_count` | `INT` | 카페 수 |
| `de_facto_population_per_cafe` | `FLOAT` | 카페 1개당 생활인구 |
| `condition_pop_per_cafe` | `BOOLEAN` | 카페 1개당 생활인구 조건 충족 여부 |
| `condition_growth_rate` | `BOOLEAN` | 증가율 조건 충족 여부 |
| `condition_activity_ratio` | `BOOLEAN` | 활동 배율 조건 충족 여부 |

- PK: `(state_code)`
- 인덱스: `idx_state_priority_rank (state_code, priority_score, rank)`

## 논리적 연결 관계

아래는 조회 시 사용할 수 있는 연결 키이다.

| 기준 테이블·컬럼 | 연결 대상 | 연결 키 |
| --- | --- | --- |
| `state_dim.state_code` | `de_facto_population_raw` | `state_code` |
| `state_dim.state_code` | `cafe_clean` | `state_code` |
| `state_dim.state_code` | `mart_state_monthly` | `state_code` |
| `state_dim.state_code` | `mart_state_hourly` | `state_code` |
| `state_dim.state_code` | `mart_priority_score` | `state_code` |
| `state_dim.state_name` | `population_clean` | `state_name` |

