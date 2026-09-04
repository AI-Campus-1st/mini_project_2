# mini_project_2

## 개요
유동인구/거주인구 수집기, DB 저장소, Streamlit 대시보드로 구성된 프로젝트 스캐폴드입니다.

## 실행 순서
1. 환경 변수를 설정합니다.
2. DB 스키마를 생성합니다.
3. 더미 데이터를 적재합니다.
4. 수집기를 실행해 원천 데이터를 적재합니다.
5. 마트 테이블을 생성합니다.
6. 대시보드를 실행해 조회합니다.

```bash
sqlite3 app.db < db/schema.sql
sqlite3 app.db < db/seed_dummy.sql
python -m collector
sqlite3 app.db < db/build_mart.sql
streamlit run app/main.py
```

전체 명령어 예시는 저장소 루트의 `commands` 파일에도 정리했습니다.

## 스크린샷
추후 추가 예정
