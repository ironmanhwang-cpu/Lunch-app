import streamlit as st
import pandas as pd
import random
import time

# ==========================================
# 1. 페이지 설정 & 테마
# ==========================================
st.set_page_config(page_title="점메추 GPS", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

    /* 제목 스타일 */
    h3 { color: var(--text-color); margin-bottom: 10px; }

    /* 버튼 스타일 */
    div.stButton > button {
        width: 100%; height: 65px; border-radius: 16px;
        background-color: var(--secondary-background-color);
        color: var(--text-color); font-size: 19px; font-weight: 700;
        border: 1px solid rgba(128,128,128,0.2);
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        transform: translateY(-2px); border-color: #FF4B4B; color: #FF4B4B;
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        color: white !important; border: none;
    }

    /* 프로그레스 바 */
    .progress-container {
        width: 100%; height: 8px; background-color: rgba(128,128,128,0.2);
        border-radius: 10px; margin-bottom: 30px; overflow: hidden;
    }
    .progress-bar {
        height: 100%; background: linear-gradient(90deg, #FF6B6B, #FF8E53);
        transition: width 0.5s ease-in-out;
    }

    /* 결과 카드 */
    .result-card {
        background: var(--secondary-background-color);
        border: 2px solid #FF6B6B; border-radius: 24px; padding: 40px;
        text-align: center; margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        animation: popUp 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    @keyframes popUp { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }

    /* 지도 버튼 (네이버/카카오) */
    .map-btn {
        display: block; width: 100%; padding: 15px 0; margin-top: 10px;
        border-radius: 15px; text-decoration: none; font-weight: bold; font-size: 18px;
        text-align: center; transition: opacity 0.3s;
    }
    .naver-btn { background-color: #03C75A; color: white !important; }
    .kakao-btn { background-color: #FEE500; color: #191919 !important; }
    .map-btn:hover { opacity: 0.8; }

</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 데이터 로드 (250개 메뉴)
# ==========================================
@st.cache_data
def load_data():
    raw_list = [
        "김치찌개", "된장찌개", "순두부찌개", "비빔밥", "불고기", "삼겹살", "갈비탕", "육개장", "떡볶이",
        "짜장면", "짬뽕", "탕수육", "마라탕", "마라샹궈", "초밥", "돈가스", "우동", "소바", "라멘",
        "파스타", "피자", "햄버거", "스테이크", "쌀국수", "팟타이", "족발", "보쌈", "닭갈비", "찜닭",
        "부대찌개", "청국장", "동태찌개", "설렁탕", "곰탕", "삼계탕", "뼈해장국", "순대국", "콩나물국밥",
        "제육덮밥", "오징어덮밥", "김치볶음밥", "오므라이스", "카레라이스", "하이라이스",
        "칼국수", "수제비", "잔치국수", "비빔국수", "냉면", "쫄면", "만두국", "라면", "김밥", "순대",
        "양꼬치", "훠궈", "우육면", "탄탄면", "깐풍기", "유린기", "고추잡채", "잡채밥",
        "규동", "가츠동", "사케동", "텐동", "오꼬노미야끼", "타코야끼", "샤브샤브", "스키야키",
        "리조또", "라자냐", "뇨끼", "샐러드", "포케", "샌드위치", "토스트", "베이글", "브런치",
        "타코", "부리또", "퀘사디아", "반미", "분짜", "나시고랭"
    ]
    def auto_tag(m):
        spicy, temp, kind, main = "순한 맛", "뜨거운 것", "한식", "기타"
        if any(k in m for k in ["김치","매운","짬뽕","마라","떡볶이","육개장","비빔","낙지","얼큰","닭갈비","부대","탄탄","타코"]): spicy="매운 맛"
        if any(k in m for k in ["냉","소바","초밥","회","샐러드","샌드위치","김밥","빙수","쫄면","막국수","포케","월남쌈"]): temp="차가운 것"
        if any(k in m for k in ["짜장","짬뽕","탕수육","마라","꿔바로우","유린기","양꼬치","훠궈","깐풍"]): kind="중식"
        elif any(k in m for k in ["초밥","우동","소바","라멘","카츠","가츠","규동","텐동","오꼬노미","스시","샤브"]): kind="일식"
        elif any(k in m for k in ["파스타","피자","버거","스테이크","샐러드","샌드위치","리조또","스프","브런치"]): kind="양식"
        elif any(k in m for k in ["쌀국수","팟타이","나시고랭","분짜","타코","부리또","반미","커리"]): kind="아시안"
        if any(k in m for k in ["밥","죽","리조또","동","초밥","필라프","포케","국밥","백반"]): main="밥"
        elif any(k in m for k in ["면","국수","우동","파스타","라멘","짜장","짬뽕","팟타이","잡채"]): main="면"
        elif any(k in m for k in ["고기","스테이크","삼겹살","갈비","제육","보쌈","족발","탕수육","돈가스","치킨","찜닭","곱창"]): main="고기"
        elif any(k in m for k in ["빵","버거","샌드위치","토스트","피자","베이글","타코"]): main="빵"
        return {"메뉴명":m, "맵기":spicy, "온도":temp, "종류":kind, "주재료":main}
    return pd.DataFrame([auto_tag(m) for m in raw_list])

df_logic = load_data()

# ==========================================
# 3. UI 및 로직
# ==========================================
if 'choices' not in st.session_state:
    st.session_state.choices = {'step1': None, 'step2': None, 'step3': None, 'step4': None}

def set_choice(step, value):
    st.session_state.choices[step] = value

def draw_progress_bar(percent):
    st.markdown(f'<div class="progress-container"><div class="progress-bar" style="width: {percent}%;"></div></div>', unsafe_allow_html=True)

def draw_step(step_key, title, options):
    current = st.session_state.choices[step_key]
    icon = "✅" if current else "🔹"
    st.markdown(f"### {icon} {title}")
    cols = st.columns(len(options))
    for i, option in enumerate(options):
        with cols[i]:
            btn_type = "primary" if current == option else "secondary"
            if st.button(option, key=f"{step_key}_{option}", type=btn_type):
                set_choice(step_key, option)
                st.rerun()

# 메인 화면
st.title("📍 전국구 점메추 AI")
st.caption("현재 위치 기반으로 주변 맛집을 찾아줍니다.")

# 진행률
current_step = 0
if st.session_state.choices['step1']: current_step = 1
if st.session_state.choices['step2']: current_step = 2
if st.session_state.choices['step3']: current_step = 3
if st.session_state.choices['step4']: current_step = 4
draw_progress_bar(current_step * 25)

# 선택 변수
c1 = st.session_state.choices['step1']
c2 = st.session_state.choices['step2']
c3 = st.session_state.choices['step3']
c4 = st.session_state.choices['step4']

# UI 렌더링
draw_step('step1', "맵기", ["매운 맛", "순한 맛"])
if c1:
    st.write("")
    draw_step('step2', "온도", ["뜨거운 것", "차가운 것"])
if c1 and c2:
    st.write("")
    draw_step('step3', "장르", ["한식", "중식", "일식", "양식", "아시안"])
if c1 and c2 and c3:
    st.write("")
    draw_step('step4', "재료", ["밥", "면", "고기", "빵", "기타"])

# 결과 화면
if c1 and c2 and c3 and c4:
    st.markdown("---")
    result_df = df_logic[(df_logic['맵기']==c1) & (df_logic['온도']==c2) & (df_logic['종류']==c3) & (df_logic['주재료']==c4)]
    
    if not result_df.empty:
        final_menu = result_df.sample(1).iloc[0]['메뉴명']
        
        # 🟢 여기가 핵심: '내 주변' 키워드를 붙여서 검색 링크 생성
        naver_url = f"https://map.naver.com/v5/search/내주변 {final_menu}"
        kakao_url = f"https://map.kakao.com/link/search/내주변 {final_menu}"
        
        st.markdown(f"""
        <div class="result-card">
            <h3>오늘의 추천</h3>
            <h1 style="font-size: 3.5rem; background: linear-gradient(90deg, #FF6B6B, #FF8E53); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                {final_menu}
            </h1>
            <p style="opacity: 0.7;">{c1} · {c2} · {c3} · {c4}</p>
            
            <div style="margin-top: 30px;">
                <a href="{naver_url}" target="_blank" class="map-btn naver-btn">
                    N 네이버지도로 주변 식당 찾기
                </a>
                <a href="{kakao_url}" target="_blank" class="map-btn kakao-btn">
                    K 카카오맵으로 주변 식당 찾기
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
        
    else:
        backup = df_logic[df_logic['종류']==c3].sample(1).iloc[0]['메뉴명']
        st.warning("조건에 딱 맞는 메뉴가 없어요 🥲")
        st.markdown(f"""
        <div class="result-card">
            <h3>대신 이건 어때요?</h3>
            <h1>{backup}</h1>
            <a href="https://map.naver.com/v5/search/내주변 {backup}" target="_blank" class="link-btn">
                네이버지도로 주변 찾기
            </a>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    if st.button("🔄 다시 하기", type="secondary"):
        for k in st.session_state.choices: st.session_state.choices[k] = None
        st.rerun()
