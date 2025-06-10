import streamlit as st
import pandas as pd
import pymysql
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="전기차 충전소 지도/검색 서비스", layout="wide")

# DB 연결
DB_CONF = dict(
    host='192.168.0.22', user='team_3', password='123', database='sk15_3team', port=3306
)
conn = pymysql.connect(**DB_CONF)
df = pd.read_sql("SELECT * FROM charging_stations", conn)
conn.close()

# --- sidebar ---
st.sidebar.title("메뉴")
page = st.sidebar.radio(
    "페이지를 선택하세요",
    ("충전소 검색", "지도 보기"),
    index=0
)

# --- 지도 페이지 ---
if page == "지도 보기":
    st.header("🚗 전기차 충전소 지도")

    # 위경도 포함 데이터만 조회 (조인)
    conn = pymysql.connect(**DB_CONF)
    sql = """
        SELECT 
            cs.station_name, cs.address, cs.operator, cs.charger_type, cs.facility_type,
            cs.capacity, cs.charger_count, cs.available_time,
            csu.latitude, csu.longitude
        FROM charging_stations cs
        LEFT JOIN charging_stations_update csu
        ON cs.station_name = csu.station_name AND cs.address = csu.address
        WHERE csu.latitude IS NOT NULL AND csu.longitude IS NOT NULL
    """
    df_map = pd.read_sql(sql, conn)
    conn.close()

    # # 지도 중심값
    # if len(df_map) > 0:
    #     center_lat = df_map["latitude"].mean()
    #     center_lon = df_map["longitude"].mean()
    # else:
    #     center_lat, center_lon = 37.55, 126.98

    # 지도 생성
    # m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    m = folium.Map(location=[37.55, 126.98], zoom_start=14)

    # 처음엔 10개만 마커 표시 (많을 때는 느릴 수 있으므로)
    for _, row in df_map.head(10).iterrows():
        popup_html = f"""
        <b>{row['station_name']}</b><br>
        기관명: {row['operator']}<br>
        주소: {row['address']}<br>
        타입: {row['charger_type']}<br>
        용량: {row['capacity']}<br>
        대수: {row['charger_count']}<br>
        이용가능: {row['available_time']}
        """
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup_html,
            tooltip=row['station_name'],
            icon=folium.Icon(color="blue", icon="bolt")
        ).add_to(m)

    # 지도 표시 및 현재 지도 bounds 반환
    map_data = st_folium(m, width=700, height=600)

    # 지도 내부 충전소만 보여주기 (데이터)
    if map_data and "bounds" in map_data:
        bounds = map_data["bounds"]
        sw_lat = bounds["_southWest"]["lat"]
        sw_lon = bounds["_southWest"]["lng"]
        ne_lat = bounds["_northEast"]["lat"]
        ne_lon = bounds["_northEast"]["lng"]
        # 지도 범위 내의 충전소 필터링
        visible_df = df_map[
            (df_map['latitude'] >= sw_lat) & (df_map['latitude'] <= ne_lat) &
            (df_map['longitude'] >= sw_lon) & (df_map['longitude'] <= ne_lon)
        ]
        st.write(f"현재 지도 내 충전소: {len(visible_df)}개")
        st.dataframe(visible_df, use_container_width=True)
    else:
        st.info("지도를 이동하면 현재 영역 내 충전소 목록이 표시됩니다.")



# --- 검색 페이지 ---
elif page == "충전소 검색":
    st.title("🔍 전기차 충전소 통합 검색")
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

    filtered = df
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
