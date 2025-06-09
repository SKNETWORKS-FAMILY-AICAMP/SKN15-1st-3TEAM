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
selected_menu = st.sidebar.radio("메뉴 선택", ["전기차 FAQ"])




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
    try:
        conn = pymysql.connect(
            host='127.0.0.1',      # MySQL 서버 주소
            user='play',           # 사용자 이름
            password='123',    # 본인의 MySQL 비밀번호
            database='sk15',       # 데이터베이스 이름
            charset='utf8mb4'      # 한글을 저장할 때 깨지지 않도록 설정
        )
        cursor = conn.cursor()

        # 데이터 삽입
        for question, answer in faq_list:
            cursor.execute("INSERT INTO pse_faq (question, answer) VALUES (%s, %s)", (question, answer))

        conn.commit()
        st.success("✅ MySQL에 FAQ 데이터 저장 완료!")
    except pymysql.MySQLError as e:
        st.error(f"❌ MySQL 오류: {e}")
    finally:
        conn.close()

# 4. MySQL에서 FAQ 데이터 불러오는 함수
def load_from_mysql():
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            user='play',
            password='123',
            database='sk15',
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT question, answer FROM pse_faq")

        rows = cursor.fetchall()
        faq_data = [(row[0], row[1]) for row in rows]
        return faq_data

    except pymysql.MySQLError as e:
        st.error(f"❌ MySQL 오류: {e}")
    finally:
        conn.close()

# Streamlit UI
st.title("전기차 FAQ")


# 6. MySQL에서 저장된 FAQ 데이터 확인
if st.button("전기차 FAQ"):
    faq_data = load_from_mysql()
    if faq_data:
        for idx, (question, answer) in enumerate(faq_data, 1):
            st.subheader(f"❓ {question}")
            st.write(f"💬 {answer}")
            st.write("-" * 50)
    else:
        st.warning("저장된 FAQ 데이터가 없습니다.")

