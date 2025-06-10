import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px

# DB 연결 엔진 생성
engine = create_engine("mysql+pymysql://team_3:123@192.168.0.22:3306/sk15_3team")

st.title("전기차 보조금 데이터")

# DB에서 데이터 읽기
df = pd.read_sql("SELECT * FROM subsidy_data", engine)

# 사용자 입력
input_value = st.text_input("검색어 입력 (지역명, 차종, 제조사)")

# 필터링 조건: 입력값이 포함된 행들만 추출 (대소문자 무시)
if input_value:
    # 필터링 조건 생성
    mask = (
        df['지역명'].astype(str).str.contains(input_value, case=False, na=False) |
        df['차종'].astype(str).str.contains(input_value, case=False, na=False) |
        df['제조사'].astype(str).str.contains(input_value, case=False, na=False)
    )
    filtered_df = df[mask]

    # 결과 출력
    if not filtered_df.empty:
        st.subheader(f"🔍 '{input_value}'에 대한 검색 결과")
        st.dataframe(filtered_df)
    else:
        st.warning(f"'{input_value}'에 해당하는 데이터가 없습니다.")


st.write("[ 전기차 보조금 전체 데이터 ]")
# 전체 데이터 표시 (선택사항)
st.dataframe(df)







