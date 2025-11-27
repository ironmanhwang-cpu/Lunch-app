import streamlit as st
import pandas as pd
import io
import random

# ==========================================
# 1. 메뉴 데이터
# ==========================================
csv_data = """메뉴명,맵기,온도,종류,주재료
김치찌개,매운 맛,뜨거운 것,한식,밥
된장찌개,순한 맛,뜨거운 것,한식,밥
순두부찌개,매운 맛,뜨거운 것,한식,밥
비빔밥,순한 맛,차가운 것,한식,밥
불고기,순한 맛,뜨거운 것,한식,고기
삼겹살,순한 맛,뜨거운 것,한식,고기
갈비탕,순한 맛,뜨거운 것,한식,밥
육개장,매운 맛,뜨거운 것,한식,밥
떡볶이,매운 맛,뜨거운 것,한식,기타
김밥,순한 맛,차가운 것,한식,밥
라면,매운 맛,뜨거운 것,한식,면
칼국수,순한 맛,뜨거운 것,한식,면
냉면,순한 맛,차가운 것,한식,면
짜장면,순한 맛,뜨거운 것,중식,면
짬뽕,매운 맛,뜨거운 것,중식,면
볶음밥,순한 맛,뜨거운 것,중식,밥
탕수육,순한 맛,뜨거운 것,중식,고기
마라탕,매운 맛,뜨거운 것,중식,면
우동,순한 맛,뜨거운 것,일식,면
소바,순한 맛,차가운 것,일식,면
돈가스,순한 맛,뜨거운 것,일식,고기
초밥,순한 맛,차가운 것,일식,밥
파스타,순한 맛,뜨거운 것,양식,면
피자,순한 맛,뜨거운 것,양식,빵
햄버거,순한 맛,뜨거운 것,양식,빵
돈가스,순한 맛,뜨거운 것,일식,고기
쌀국수,순한 맛,뜨거운 것,아시안,면
"""

# 2. 페이지 설정
st.set_page_config(page_title="점메추 Master", layout="centered")

# 3. 스타일링
st.markdown("""
<style>
    :root { --primary: #FF4B4B; }
    .stButton > button {
        width: 100%; height: 60px; border-radius: 12px;
        font-size: 18px; font-weight: bold;
    }
    .result-card {
        background-color: #fff; border: 3px solid var(--primary);
        border-radius: 20px; padding: 30px; text-align: center;
        margin-top: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    a { text-decoration: none; color: #FF4B4B; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 4. 데이터 로드
df = pd.read_csv(io.StringIO(csv_data))

# 5. 상태 관리
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

st.title("🍽️ 점메추 Master")

c1 = st.session_state.choices['step1']
c2 = st.session_state.choices['step2']
c3 = st.session_state.choices['step3']
c4 = st.session_state.choices['step4']

draw_step('step1', "맵기", ["매운 맛", "순한 맛"])
if c1: draw_step('step2', "온도", ["뜨거운 것", "차가운 것"])
if c1 and c2: draw_step('step3', "종류", ["한식", "중식", "일식", "양식", "아시안"])
if c1 and c2 and c3: draw_step('step4', "재료", ["밥", "면", "고기", "빵", "기타"])

if c1 and c2 and c3 and c4:
    st.divider()
    result_df = df[(df['맵기']==c1) & (df['온도']==c2) & (df['종류']==c3) & (df['주재료']==c4)]
    
    if not result_df.empty:
        menu_name = result_df.sample(1).iloc[0]['메뉴명']
        search_url = f"https://search.naver.com/search.naver?query=근처 {menu_name} 맛집"
        
        st.markdown(f"""
        <div class="result-card">
            <h3 style="color:gray;">오늘의 추천 메뉴</h3>
            <h1 style="color:#FF4B4B; font-size: 3rem;">{menu_name}</h1>
            <p><a href="{search_url}" target="_blank">📍 근처 맛집 보기 (클릭)</a></p>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
    else:
        st.warning("조건에 맞는 메뉴가 없어요 😭")
        backup = df[df['종류']==c3].sample(1).iloc[0]['메뉴명']
        st.success(f"대신 **{backup}** 어때요?")

    st.write("")
    if st.button("🔄 처음부터 다시 하기"):
        for k in st.session_state.choices: st.session_state.choices[k] = None
        st.rerun()
