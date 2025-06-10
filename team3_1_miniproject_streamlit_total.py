import streamlit as st
import pymysql
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from streamlit_option_menu import option_menu
from PIL import Image
import folium
from streamlit_folium import st_folium
@st.cache_data
def load_data():
    conn = pymysql.connect(
        host='192.168.0.22',
        user='team_3',
        passwd='123',
        database='sk15_3team',
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
# st.sidebar.title("📊 메뉴")
with st.sidebar:
    selected_menu = option_menu(
        "📊 메뉴",                        
        ["홈", "전기차 연도별 변화 추이", "전기차 가격 조회", "전기차 보조금 조회", "전기차 충전소 검색", "전기차 FAQ"],
        icons=[
            "house",          # 홈
            "bar-chart",      # 전기차 연도별 변화 추이
            "cash",           # 전기차 가격 조회
            "wallet",         # 전기차 보조금 조회
            #"map",            # 전기차 충전소 지도보기
            "search",         # 전기차 충전소 검색
            "question-circle" # 전기차 FAQ
        ],
        menu_icon="cast",  
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f0f2f6"},
            "icon": {"color": "blue", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px",
                "--hover-color": "#eee"
            },
            "nav-link-selected": {
                "background-color": "#d1e0ff",
                "font-weight": "bold"
            }
        }
    )

if selected_menu == "홈" :
    st.title("⚡🚗 전기차 보급 목적과 목표")
    st.image("https://dimg.donga.com/ugc/CDB/WEEKLY/Article/62/be/3f/5e/62be3f5e1710d2738250.jpg", caption="출처 : https://weekly.donga.com/economy/article/all/11/3482755/1", use_container_width=True)

    with st.expander("환경적 측면") :
        st.subheader("자동차로 인한 대기오염 해결")
        st.write("수도권에서 발생하는 미세먼지의 30%이상이 경유차 등 자동차에서 배출되는 오염물질로서, 자동차로 인한 대기오염이 심각해지고 있습니다. \n 또한, 아파트 주변도로, 지하주차장 등 국민 생활에 밀접한 곳에서 발생하는 자동차 배출가스는 인체 위해도가 매우 높아 '12년에 국제암연구소에서 1군 발암물질로 지정하기도 하였습니다. \n내연기관차를 친환경차인 전기차로 대체해나갈 경우 자동차로 인한 대기오염 문제를 획기적으로 해결할 수 있습니다.\n자동차에서 배출되는 유해물질은 일산화탄소(CO), 탄화수소(HC), 질소산화물(NOx), 미세먼지(PM)등이 있습니다.")
        try :
            image = Image.open('enviroment_1.png')
            st.image(image, caption='출처 : https://ev.or.kr/nportal/evcarInfo/initEvcarSupplyPurposeAction.do', use_container_width=True)
            image = Image.open('enviroment_2.png')
            st.image(image, caption='출처 : https://ev.or.kr/nportal/evcarInfo/initEvcarSupplyPurposeAction.do', use_container_width=True)
        except :
            pass
    with st.expander("경제적 측면") :
        st.subheader("전기차 연료비 (급속충전기 기준)")
        st.write("시간대별 전기차 평균 충전요금은 경부하 66원/kWh, 중간부하 108원/kWh, 최대부하 153원/kWh 입니다. \n 아이오닉(연비 6.3km/kWh) 기준으로 100km당 2,759원 비용이 발생합니다.")    
        try :
            image = Image.open('money_1.png')
            st.image(image, caption='출처 : https://ev.or.kr/nportal/evcarInfo/initEvcarSupplyPurposeAction.do', use_container_width=True)
            image = Image.open('money_2.png')
            st.image(image, caption='출처 : https://ev.or.kr/nportal/evcarInfo/initEvcarSupplyPurposeAction.do', use_container_width=True)
        except :
            pass
    with st.expander("산업적 측면") :
        st.subheader("전기차 연료비 (급속충전기 기준)")
        st.write("V2G는 Vehicle To Grid로, 자동차에서 전력망으로 전기를 이동하는 것을 의미하는데, 즉, V2G란 전기차에 저장한 배터리를 에너지저장장치(ESS)처럼 활용해 전력계통에 연계하는 기술을 의미합니다.\n 이산화탄소의 배출을 줄이면서 친환경적이고 경제성을 갖추어 지속가능한 성장을 이어갈 수 있는 산업모델로 정착하게되고 향후 V2G사업자와 수요관리 사업자 등, V2G를 활용하여 피크절감효과뿐 아니라 선진국과 같은 전력계통 주파수 조정, 신재생에너지 발판 등 다양한 전력보조서비스와 부가가치를 창출할 것입니다.")
        try :
            image = Image.open('a_1.png')
            st.image(image, caption='출처 : https://ev.or.kr/nportal/evcarInfo/initEvcarSupplyPurposeAction.do', use_container_width=True)
            image = Image.open('a_2.png')
            st.image(image, caption='출처 : https://ev.or.kr/nportal/evcarInfo/initEvcarSupplyPurposeAction.do', use_container_width=True)
        except :
            pass
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

    trend_data = {year: yearly_data[year].get(selected_region, 0) for year in sorted(yearly_data.keys())}
    st.subheader(f"📈 {selected_region}의 연도별 등록 변화")
    st.line_chart(trend_data)


# 1. URL 설정 및 요청 보내기
url = "https://www.pse.com/ko/pages/electric-cars/electric-vehicles-faq"
headers = {
    "User-Agent": "Mozilla/5.0"
}

# 2. 크롤링 함수
def crawl_faq():
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # 질문과 답변 추출
    questions = soup.find_all("p", class_="collapsed")
    answers = soup.find_all("div", class_="panel-body collapse-content")

    # 리스트로 정리
    faq_list = []
    for q, a in zip(questions, answers):
        question = q.text.strip()
        answer = a.text.strip()
        faq_list.append((question, answer))
    
    return faq_list

# 3. MySQL에 데이터 저장 함수
def save_to_mysql(faq_list):
    conn = None
    try:
        conn = pymysql.connect(
            host='192.168.0.22',      # MySQL 서버 주소
            user='team_3',           # 사용자 이름
            password='123',    # 본인의 MySQL 비밀번호
            database='sk15_3team',       # 데이터베이스 이름
            port= 3306,
            charset='utf8mb4'      # 한글을 저장할 때 깨지지 않도록 설정
        )
        cursor = conn.cursor()

        # 데이터 삽입
        for question, answer in faq_list:
            cursor.execute("INSERT INTO ecar_faq (question, answer) VALUES (%s, %s)", (question, answer))

        conn.commit()
        st.success("✅ MySQL에 FAQ 데이터 저장 완료!")
    except pymysql.MySQLError as e:
        st.error(f"❌ MySQL 오류: {e}")
    finally:
        if conn:
            conn.close()

# 4. MySQL에서 FAQ 데이터 불러오는 함수
def load_from_mysql():
    conn = None
    try:
        conn = pymysql.connect(
            host='192.168.0.22',
            user='team_3',
            password='123',
            database='sk15_3team',
            port= 3306
        )
        cursor = conn.cursor()
        cursor.execute("SELECT question, answer FROM ecar_faq")

        rows = cursor.fetchall()
        faq_data = [(row[0], row[1]) for row in rows]
        return faq_data

    except pymysql.MySQLError as e:
        st.error(f"❌ MySQL 오류: {e}")
    finally:
        if conn :
            conn.close()

# Streamlit UI

# 6. MySQL에서 저장된 FAQ 데이터 확인

if selected_menu == "전기차 FAQ" :

    st.title("자주 묻는 질문 (FAQ)❓")
    faq_data = load_from_mysql()
    if faq_data:
        for question, answer in faq_data :
            with st.expander("❓." + question) :
                st.write(answer)
        #for idx, (question, answer) in enumerate(faq_data, 1):
        #    st.toggle(f"❓ {question}")
        #    # st.subheader(f"❓ {question}")
        #    st.write(f"💬 {answer}")
        #    st.write("-" * 50)
    else:
        st.warning("저장된 FAQ 데이터가 없습니다.")

if selected_menu == "전기차 가격 조회" :
    st.title("⚡🚗전기차 가격 조회")
    input_name = st.text_input(label='차량명을 입력해주세요.', placeholder='예) BMW iX')
    
    def srch_elec_car_info(input_name=""):
        conn = pymysql.connect(host='192.168.0.22', user='team_3', passwd='123', database='sk15_3team', port=3306)
        cursor = conn.cursor()
        if input_name == "" :
            sql = """SELECT * FROM electric_cars"""
        else:
            sql = f"""SELECT * FROM electric_cars WHERE car_model LIKE '%{input_name}%'"""

        cursor.execute(sql)
        result = cursor.fetchall()

        columns = ['회사명', '차종', '승차인원', '최고속도출력', '1회충전주행거리', '배터리', '국고보조금', '판매사연락처', '제조사', '제조국가']
        return pd.DataFrame(result, index=range(1, len(result) + 1) , columns=columns)

    st.write(srch_elec_car_info(input_name))



if selected_menu == "전기차 보조금 조회" :
    engine = create_engine("mysql+pymysql://team_3:123@192.168.0.22:3306/sk15_3team")

    st.title("⚡🚗전기차 보조금 검색")
    
    # DB에서 데이터 읽기
    df = pd.read_sql("SELECT * FROM subsidy_data", engine)

    # 사용자 입력
    # input_value = st.text_input("검색어 입력 (지역명, 차종, 제조사)", label='지역명, 차종, 제조사를 입력해주세요!.', placeholder='예) 경기, 일반승용, BMW')
    input_value = st.text_input(label='지역명, 차종, 제조사중 하나 이상만 입력해주세요!.', placeholder='예) 경기, 일반승용, BMW     예) 서울')
    # 필터링 조건: 입력값이 포함된 행들만 추출 (대소문자 무시)
    if input_value:
    # 입력값을 쉼표로 분리하고 양쪽 공백 제거
        values = [v.strip() for v in input_value.split(',')]

        mask = pd.Series([True] * len(df))  # 초기값: 전체 True

        if len(values) > 0:
            mask &= df['region'].astype(str).str.contains(values[0], case=False, na=False)
        if len(values) > 1:
            mask &= df['vehicle_type'].astype(str).str.contains(values[1], case=False, na=False)
        if len(values) > 2:
            mask &= df['manufacturer'].astype(str).str.contains(values[2], case=False, na=False)

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



# if selected_menu == "전기차 충전소 지도보기" :
#     st.header("🚗 전기차 충전소 지도")

#     DB_CONF = dict(
#     host='192.168.0.22', user='team_3', password='123', database='sk15_3team', port=3306
#     )

#     # --- 데이터 로딩 & 마커 표시 안내 메시지 ---
#     with st.spinner("잠시만 기다려주세요, 데이터를 가져오는 중입니다."):

#         # 위경도 포함 데이터만 조회 (조인)
#         conn = pymysql.connect(**DB_CONF)
#         sql = """
#             SELECT 
#                 cs.station_name, cs.address, cs.operator, cs.charger_type, cs.facility_type,
#                 cs.capacity, cs.charger_count, cs.available_time,
#                 csu.latitude, csu.longitude
#             FROM charging_stations cs
#             LEFT JOIN charging_stations_update csu
#             ON cs.station_name = csu.station_name AND cs.address = csu.address
#             WHERE csu.latitude IS NOT NULL AND csu.longitude IS NOT NULL
#         """
#         df_map = pd.read_sql(sql, conn)
#         conn.close()

#         # 지도 중심값 (평균값, 없으면 서울)
#         m = folium.Map(location=[37.55, 126.98], zoom_start=27)

#         # 빈 지도 먼저 그림, bounds 정보 받아옴
#         map_data = st_folium(m, width=900, height=650, returned_objects=["bounds"])

#         # 지도 바운드 내 데이터만 마커로 표시
#         if map_data and "bounds" in map_data:
#             bounds = map_data["bounds"]
#             sw_lat = bounds["_southWest"]["lat"]
#             sw_lon = bounds["_southWest"]["lng"]
#             ne_lat = bounds["_northEast"]["lat"]
#             ne_lon = bounds["_northEast"]["lng"]
#             # 지도 범위 내 충전소만 추출
#             visible_df = df_map[
#                 (df_map['latitude'] >= sw_lat) & (df_map['latitude'] <= ne_lat) &
#                 (df_map['longitude'] >= sw_lon) & (df_map['longitude'] <= ne_lon)
#             ]

#             # 마커는 최대 200개만 표시 (성능 문제 방지)
#             for _, row in visible_df.head(50).iterrows():
#                 popup_html = f"""
#                 <b>{row['station_name']}</b><br>
#                 기관명: {row['operator']}<br>
#                 주소: {row['address']}<br>
#                 타입: {row['charger_type']}<br>
#                 용량: {row['capacity']}<br>
#                 대수: {row['charger_count']}<br>
#                 이용가능: {row['available_time']}
#                 """
#                 folium.Marker(
#                     location=[row['latitude'], row['longitude']],
#                     popup=popup_html,
#                     tooltip=row['station_name'],
#                     icon=folium.Icon(color="blue", icon="bolt")
#                 ).add_to(m)
#             # 마커 추가된 지도 다시 그림
#             st_folium(m, width=900, height=650)

#             st.write(f"현재 지도 내 충전소: {len(visible_df)}개 (마커 최대 200개 표시)")
#             st.dataframe(visible_df, use_container_width=True)
#         else:
#             st.info("지도를 이동/확대하면 현재 영역 내 충전소 목록이 표시됩니다.")



if selected_menu == "전기차 충전소 검색":
    st.title("🔍 전기차 충전소 통합 검색")
    
    DB_CONF = dict(
    host='192.168.0.22', user='team_3', password='123', database='sk15_3team', port=3306
    )
    
    conn = pymysql.connect(**DB_CONF)
    df_2 = pd.read_sql("SELECT * FROM charging_stations", conn)
    conn.close()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        search_operator = st.text_input("기관명", "")
    with col2:
        search_name = st.text_input("충전소 이름", "")
    with col3:
        search_address = st.text_input("주소", "")
    with col4:
        charger_type_list = [
            "전체",
            "DC차데모", "AC완속", "DC차데모+AC3상",
            "DC콤보", "DC차데모+DC콤보",
            "DC차데모+AC3상+DC콤보", "AC3상"
        ]
        search_charger_type = st.selectbox("충전기 타입", charger_type_list)

    filtered = df_2
    if search_operator:
        filtered = filtered[filtered['operator'].str.contains(search_operator, case=False, na=False)]
    if search_name:
        filtered = filtered[filtered['station_name'].str.contains(search_name, case=False, na=False)]
    if search_address:
        filtered = filtered[filtered['address'].str.contains(search_address, case=False, na=False)]
    if search_charger_type != "전체":
        filtered = filtered[filtered['charger_type'] == search_charger_type]

    st.write(f"검색 결과: {len(filtered)}건")
    view_df = filtered.rename(columns={
        'operator': '기관명',
        'station_name': '충전소 이름',
        'charger_type': '충전기 타입',
        'facility_type': '충전소 분류',
        'address': '주소',
        'available_time': '이용가능 시간',
        'capacity': '용량',
        'charger_count': '충전기 대수'
    })[['기관명', '충전소 이름', '주소', '충전소 분류', '충전기 타입', '용량', '이용가능 시간', '충전기 대수']]

    if not search_operator and not search_name and not search_address and search_charger_type == "전체":
        st.dataframe(view_df.head(40), use_container_width=True)
    else:
        st.dataframe(view_df, use_container_width=True)
