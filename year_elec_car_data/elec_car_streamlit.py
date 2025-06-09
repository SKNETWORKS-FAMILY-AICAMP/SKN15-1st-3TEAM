import streamlit as st
import pymysql

@st.cache_data
def load_data():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='play',
        passwd='123',
        database='sk15',
        port=3306,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT year, region, count FROM ev_car_statistics_yearly")
    rows = cursor.fetchall()
    conn.close()

    data = {}
    for year, region, count in rows:
        if year not in data:
            data[year] = {}
        data[year][region] = count
    return data

# 사이드바 메뉴
st.sidebar.title("📊 메뉴")
selected_menu = st.sidebar.radio("메뉴 선택", ["홈", "전기차 연도별 변화 추이"])

if selected_menu == "홈" :
    st.title("⚡🚗 전기차 관련 변화 추이")
    st.write("<----- 원하는 메뉴를 선택하세요")


if selected_menu == "전기차 연도별 변화 추이":
    st.title("⚡🚗 전기차 등록 통계 시각화")

    # 데이터 로드
    yearly_data = load_data()
    years = sorted(yearly_data.keys(), reverse=True)
    regions = list(next(iter(yearly_data.values())).keys())

    # ──────────────
    # 사이드바 설정
    st.subheader("🔧 설정")

        # 연도 선택
    selected_year = st.selectbox("연도 선택", years)
    # 체크박스 + 조건부 지역 선택
    
    selected_region = None
    

    # ──────────────
    # 메인 화면: 막대그래프
    region_data = yearly_data[selected_year]
    st.subheader(f"📊 {selected_year}년 지역별 전기차 등록 대수")
    st.bar_chart(region_data)
    #show_trend = st.checkbox("📈 지역별 연도 추이 보기")
    #if show_trend:
    selected_region = st.selectbox("지역 선택", regions)
    # 꺾은선 그래프 (조건부)
    #if show_trend and selected_region:
    trend_data = {year: yearly_data[year].get(selected_region, 0) for year in sorted(yearly_data.keys())}
    st.subheader(f"📈 {selected_region}의 연도별 등록 변화")
    st.line_chart(trend_data)
