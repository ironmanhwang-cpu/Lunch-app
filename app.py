import streamlit as st
import pandas as pd
import requests
import io
import random

# 1. 페이지 설정
st.set_page_config(page_title="서울 점메추 Speed", layout="centered")

# 2. 스타일링
st.markdown("""
<style>
    :root { --primary: #FF4B4B; }
    .result-card {
        border: 3px solid var(--primary); border-radius: 20px;
        padding: 30px; text-align: center; background-color: #fff;
        margin-top: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .restaurant-box {
        background-color: white; border: 1px solid #ddd;
        border-radius: 12px; padding: 15px; margin-top: 10px;
        text-align: left; transition: transform 0.2s;
    }
    .restaurant-box:hover { transform: scale(1.02); border-color: var(--primary); }
    .stButton > button { width: 100%; height: 65px; font-size: 19px; border-radius: 12px; font-weight: bold; }
    a { text-decoration: none; color: #FF4B4B; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# ⚡ 핵심 성능 최적화: 데이터 캐싱
# ==========================================
# 이 함수 위에 @st.cache_data를 붙이면, 데이터를 한 번만 가져오고 저장해둡니다.
# 버튼을 눌러도 다시 다운로드하지 않아서 엄청나게 빨라집니다.
@st.cache_data(ttl=3600) # 1시간 동안 기억함
def fetch_seoul_restaurants(api_key):
    # 서울시 모범음식점 데이터 (1000개 요청)
    url = f'http://openapi.seoul.go.kr:8088/{api_key}/json/CrtfcUpsoInfo/1/1000/'
    try:
        response = requests.get(url)
        data = response.json()
        if 'CrtfcUpsoInfo' in data and 'row' in data['CrtfcUpsoInfo']:
            rows = data['CrtfcUpsoInfo']['row']
            df = pd.DataFrame(rows)
            return df[['UPSO_NM', 'CGG_CODE_NM', 'COB_CODE_NM', 'FOOD_MENU']]
        else:
            return pd.DataFrame()
    except:
        return pd.DataFrame()

# API 키 가져오기 (없으면 에러 방지용 더미 값)
try:
    API_KEY = st.secrets["SEOUL_API_KEY"]
except:
    # 키가 없을 때를 대비해 로컬 테스트용으로 비워둠 (나중에 secrets 채우면 작동)
    API_KEY = "TEST_KEY" 

# 데이터 로드 (캐싱 덕분에 순식간에 끝남)
if API_KEY != "TEST_KEY":
    df_seoul = fetch_seoul_restaurants(API_KEY)
else:
    df_seoul = pd.DataFrame()

# 내장 메뉴 데이터
menu_csv = """메뉴명,맵기,온도,종류,주재료
김치찌개,매운 맛,뜨거운 것,한식,밥
된장찌개,순한 맛,뜨거운 것,한식,밥
비빔밥,순한 맛,차가운 것,한식,밥
불고기,순한 맛,뜨거운 것,한식,고기
삼겹살,순한 맛,뜨거운 것,한식,고기
육개장,매운 맛,뜨거운 것,한식,밥
냉면,순한 맛,차가운 것,한식,면
짜장면,순한 맛,뜨거운 것,중식,면
짬뽕,매운 맛,뜨거운 것,중식,면
탕수육,순한 맛,뜨거운 것,중식,고기
마라탕,매운 맛,뜨거운 것,중식,면
초밥,순한 맛,차가운 것,일식,밥
돈가스,순한 맛,뜨거운 것,일식,고기
우동,순한 맛,뜨거운 것,일식,면
소바,순한 맛,차가운 것,일식,면
파스타,순한 맛,뜨거운 것,양식,면
피자,순한 맛,뜨거운 것,양식,빵
햄버거,순한 맛,뜨거운 것,양식,빵
스테이크,순한 맛,뜨거운 것,양식,고기
쌀국수,순한 맛,뜨거운 것,아시안,면
"""
df_logic = pd.read_csv(io.StringIO(menu_csv))

# 상태 관리
if 'choices' not in st.session_state:
    st.session_state.choices = {'step1': None, 'step2': None, 'step3': None, 'step4': None}

def set_choice(step, value):
    st.session_state.choices[step] = value

def draw_step(step_key, title, options):
    with st.container(border=True):
        current = st.session_state.choices[step_key]
        icon = "✅" if current else "🔹"
        st.subheader(f"{icon} {title}")
        cols = st.columns(len(options))
        for i, option in enumerate(options):
            with cols[i]:
                btn_type = "primary" if current == option else "secondary"
                if st.button(option, key=f"{step_key}_{option}", type=btn_type):
                    set_choice(step_key, option)
                    st.rerun()

# ================= 메인 프로그램 =================

st.title("⚡ 서울 점메추 (초고속)")

# 선택값
c1 = st.session_state.choices['step1']
c2 = st.session_state.choices['step2']
c3 = st.session_state.choices['step3']
c4 = st.session_state.choices['step4']

# [UI 단계]
draw_step('step1', "맵기", ["매운 맛", "순한 맛"])
if c1: draw_step('step2', "온도", ["뜨거운 것", "차가운 것"])
if c1 and c2: draw_step('step3', "종류", ["한식", "중식", "일식", "양식", "아시안"])
if c1 and c2 and c3: draw_step('step4', "재료", ["밥", "면", "고기", "빵", "기타"])

# [결과 화면]
if c1 and c2 and c3 and c4:
    st.divider()
    result_menu = df_logic[(df_logic['맵기']==c1) & (df_logic['온도']==c2) & (df_logic['종류']==c3) & (df_logic['주재료']==c4)]
    
    if not result_menu.empty:
        final_menu = result_menu.sample(1).iloc[0]['메뉴명']
        search_menu_url = f"https://search.naver.com/search.naver?query={final_menu}"
        
        st.markdown(f"""
        <div class="result-card">
            <h3 style="color:#666; margin:0;">오늘의 메뉴</h3>
            <h1 style="color:#FF4B4B; font-size:3.5rem; margin:10px 0;">{final_menu}</h1>
            <p><a href="{search_menu_url}" target="_blank">🔍 메뉴 정보</a></p>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
        
        st.write("")
        st.subheader(f"📍 '{c3}' 추천 맛집")
        
        if not df_seoul.empty:
            matched = df_seoul[df_seoul['COB_CODE_NM'].str.contains(c3, na=False)]
            if not matched.empty:
                picks = matched.sample(min(3, len(matched)))
                for _, row in picks.iterrows():
                    r_name = row['UPSO_NM']
                    r_gu = row['CGG_CODE_NM']
                    map_url = f"https://map.naver.com/v5/search/{r_name}"
                    st.markdown(f"""
                    <div class="restaurant-box">
                        <div style="font-weight:bold; font-size:18px;">
                            🏢 {r_name}
                            <a href="{map_url}" target="_blank" style="float:right; font-size:14px;">지도 보기 ➡</a>
                        </div>
                        <div style="color:gray; font-size:14px; margin-top:5px;">📍 {r_gu}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(f"데이터에 '{c3}' 관련 맛집이 없네요.")
        else:
            if API_KEY == "TEST_KEY":
                 st.warning("⚠️ API 키 설정을 완료하면 실제 맛집이 나옵니다.")
            else:
                 st.error("데이터 로드 실패")
            
    else:
        st.warning("조건에 맞는 메뉴가 없어요.")
        backup = df_logic[df_logic['종류']==c3].sample(1).iloc[0]['메뉴명']
        st.success(f"대신 **{backup}** 어때요?")

    st.write("")
    if st.button("🔄 처음부터 다시 하기"):
        for k in st.session_state.choices: st.session_state.choices[k] = None
        st.rerun()
