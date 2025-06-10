import pymysql
import streamlit as st
import pandas as pd

st.title("전기차")

st.subheader("전기차 정보 조회")
st.sidebar.title("메뉴")

buttons = ["홈", "전기차 연도별 변화 추이", "전기차 가격 조회"]

for btn in buttons:
    if st.sidebar.button(btn):
        st.write(f"{btn} 버튼 클릭됨")

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


