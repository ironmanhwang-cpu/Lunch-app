import streamlit as st
import pandas as pd
import io
import random

# ==========================================
# 1. 💾 내장된 대용량 메뉴 데이터 (130개+)
# ==========================================
csv_data = """메뉴명,맵기,온도,종류,주재료
김치찌개,매운 맛,뜨거운 것,한식,밥
참치김치찌개,매운 맛,뜨거운 것,한식,밥
돼지김치찌개,매운 맛,뜨거운 것,한식,밥
꽁치김치찌개,매운 맛,뜨거운 것,한식,밥
된장찌개,순한 맛,뜨거운 것,한식,밥
차돌된장찌개,순한 맛,뜨거운 것,한식,밥
해물된장찌개,순한 맛,뜨거운 것,한식,밥
강된장보리밥,순한 맛,뜨거운 것,한식,밥
순두부찌개,매운 맛,뜨거운 것,한식,밥
해물순두부,매운 맛,뜨거운 것,한식,밥
들깨순두부,순한 맛,뜨거운 것,한식,밥
부대찌개,매운 맛,뜨거운 것,한식,밥
청국장,순한 맛,뜨거운 것,한식,밥
비빔밥,순한 맛,차가운 것,한식,밥
육회비빔밥,매운 맛,차가운 것,한식,밥
돌솥비빔밥,순한 맛,뜨거운 것,한식,밥
제육볶음,매운 맛,뜨거운 것,한식,고기
오징어볶음,매운 맛,뜨거운 것,한식,기타
쭈꾸미볶음,매운 맛,뜨거운 것,한식,기타
불고기,순한 맛,뜨거운 것,한식,고기
소불고기,순한 맛,뜨거운 것,한식,고기
돼지불백,순한 맛,뜨거운 것,한식,고기
삼겹살,순한 맛,뜨거운 것,한식,고기
목살구이,순한 맛,뜨거운 것,한식,고기
항정살,순한 맛,뜨거운 것,한식,고기
갈비찜,순한 맛,뜨거운 것,한식,고기
매운갈비찜,매운 맛,뜨거운 것,한식,고기
닭갈비,매운 맛,뜨거운 것,한식,고기
찜닭,순한 맛,뜨거운 것,한식,고기
로제찜닭,순한 맛,뜨거운 것,한식,고기
닭볶음탕,매운 맛,뜨거운 것,한식,고기
삼계탕,순한 맛,뜨거운 것,한식,고기
설렁탕,순한 맛,뜨거운 것,한식,밥
곰탕,순한 맛,뜨거운 것,한식,밥
갈비탕,순한 맛,뜨거운 것,한식,밥
도가니탕,순한 맛,뜨거운 것,한식,밥
육개장,매운 맛,뜨거운 것,한식,밥
닭개장,매운 맛,뜨거운 것,한식,밥
콩나물국밥,순한 맛,뜨거운 것,한식,밥
뼈해장국,매운 맛,뜨거운 것,한식,밥
감자탕,매운 맛,뜨거운 것,한식,밥
선지해장국,매운 맛,뜨거운 것,한식,밥
순대국,순한 맛,뜨거운 것,한식,밥
돼지국밥,순한 맛,뜨거운 것,한식,밥
떡볶이,매운 맛,뜨거운 것,한식,기타
라볶이,매운 맛,뜨거운 것,한식,면
로제떡볶이,순한 맛,뜨거운 것,한식,기타
김밥,순한 맛,차가운 것,한식,밥
참치김밥,순한 맛,차가운 것,한식,밥
치즈김밥,순한 맛,차가운 것,한식,밥
라면,매운 맛,뜨거운 것,한식,면
치즈라면,순한 맛,뜨거운 것,한식,면
칼국수,순한 맛,뜨거운 것,한식,면
바지락칼국수,순한 맛,뜨거운 것,한식,면
닭칼국수,순한 맛,뜨거운 것,한식,면
장칼국수,매운 맛,뜨거운 것,한식,면
수제비,순한 맛,뜨거운 것,한식,기타
들깨수제비,순한 맛,뜨거운 것,한식,기타
잔치국수,순한 맛,뜨거운 것,한식,면
비빔국수,매운 맛,차가운 것,한식,면
물냉면,순한 맛,차가운 것,한식,면
비빔냉면,매운 맛,차가운 것,한식,면
쫄면,매운 맛,차가운 것,한식,면
짜장면,순한 맛,뜨거운 것,중식,면
간짜장,순한 맛,뜨거운 것,중식,면
쟁반짜장,순한 맛,뜨거운 것,중식,면
짬뽕,매운 맛,뜨거운 것,중식,면
삼선짬뽕,매운 맛,뜨거운 것,중식,면
백짬뽕,순한 맛,뜨거운 것,중식,면
차돌짬뽕,매운 맛,뜨거운 것,중식,면
볶음밥,순한 맛,뜨거운 것,중식,밥
새우볶음밥,순한 맛,뜨거운 것,중식,밥
잡채밥,순한 맛,뜨거운 것,중식,밥
마파두부밥,매운 맛,뜨거운 것,중식,밥
유산슬밥,순한 맛,뜨거운 것,중식,밥
탕수육,순한 맛,뜨거운 것,중식,고기
찹쌀탕수육,순한 맛,뜨거운 것,중식,고기
깐풍기,매운 맛,뜨거운 것,중식,고기
유린기,순한 맛,뜨거운 것,중식,고기
마라탕,매운 맛,뜨거운 것,중식,면
마라샹궈,매운 맛,뜨거운 것,중식,고기
양꼬치,순한 맛,뜨거운 것,중식,고기
우동,순한 맛,뜨거운 것,일식,면
튀김우동,순한 맛,뜨거운 것,일식,면
김치우동,매운 맛,뜨거운 것,일식,면
냉우동,순한 맛,차가운 것,일식,면
소바,순한 맛,차가운 것,일식,면
돈코츠라멘,순한 맛,뜨거운 것,일식,면
미소라멘,순한 맛,뜨거운 것,일식,면
소유라멘,순한 맛,뜨거운 것,일식,면
카라이라멘,매운 맛,뜨거운 것,일식,면
마제소바,순한 맛,뜨거운 것,일식,면
초밥,순한 맛,차가운 것,일식,밥
연어초밥,순한 맛,차가운 것,일식,밥
광어초밥,순한 맛,차가운 것,일식,밥
회덮밥,매운 맛,차가운 것,일식,밥
돈가스,순한 맛,뜨거운 것,일식,고기
치즈돈가스,순한 맛,뜨거운 것,일식,고기
히레카츠,순한 맛,뜨거운 것,일식,고기
규동,순한 맛,뜨거운 것,일식,밥
가츠동,순한 맛,뜨거운 것,일식,밥
사케동,순한 맛,차가운 것,일식,밥
장어덮밥,순한 맛,뜨거운 것,일식,밥
카레라이스,순한 맛,뜨거운 것,일식,밥
오꼬노미야끼,순한 맛,뜨거운 것,일식,기타
타코야끼,순한 맛,뜨거운 것,일식,기타
토마토파스타,순한 맛,뜨거운 것,양식,면
미트볼파스타,순한 맛,뜨거운 것,양식,면
크림파스타,순한 맛,뜨거운 것,양식,면
까르보나라,순한 맛,뜨거운 것,양식,면
로제파스타,순한 맛,뜨거운 것,양식,면
알리오올리오,순한 맛,뜨거운 것,양식,면
봉골레파스타,순한 맛,뜨거운 것,양식,면
피자,순한 맛,뜨거운 것,양식,빵
페퍼로니피자,매운 맛,뜨거운 것,양식,빵
고구마피자,순한 맛,뜨거운 것,양식,빵
햄버거,순한 맛,뜨거운 것,양식,빵
치즈버거,순한 맛,뜨거운 것,양식,빵
치킨버거,순한 맛,뜨거운 것,양식,빵
샌드위치,순한 맛,차가운 것,양식,빵
서브웨이,순한 맛,차가운 것,양식,빵
스테이크,순한 맛,뜨거운 것,양식,고기
함박스테이크,순한 맛,뜨거운 것,양식,고기
샐러드,순한 맛,차가운 것,양식,기타
닭가슴살샐러드,순한 맛,차가운 것,양식,기타
포케,순한 맛,차가운 것,양식,밥
브리또,순한 맛,뜨거운 것,양식,빵
타코,매운 맛,차가운 것,양식,빵
쌀국수,순한 맛,뜨거운 것,아시안,면
매운쌀국수,매운 맛,뜨거운 것,아시안,면
팟타이,순한 맛,뜨거운 것,아시안,면
나시고랭,순한 맛,뜨거운 것,아시안,밥
"""

# ==========================================
# 2. 웹사이트 설정 및 디자인
# ==========================================
st.set_page_config(page_title="점메추 Master", layout="centered")

# 데이터 로드 (문자열 -> 데이터프레임 변환)
df = pd.read_csv(io.StringIO(csv_data))

st.markdown("""
<style>
    /* 1. 디자인 테마 (부드러운 느낌) */
    :root { --primary: #FF4B4B; --line: #e0e0e0; }
    
    /* 2. 등장 애니메이션 */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translate3d(0, 20px, 0); }
        to { opacity: 1; transform: translate3d(0, 0, 0); }
    }
    .step-wrapper { animation: fadeInUp 0.5s ease-out; margin-bottom: 15px; }

    /* 3. 연결선 (트리 구조) */
    .tree-line {
        width: 4px; height: 35px; background: #ddd; margin: 0 auto;
        border-radius: 2px;
    }
    .tree-line.active {
        background: var(--primary);
        box-shadow: 0 0 8px rgba(255, 75, 75, 0.4);
    }

    /* 4. 버튼 스타일 (크고 둥글게) */
    .stButton > button {
        width: 100%; height: 65px; border-radius: 15px;
        font-size: 19px !important; font-weight: 600;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.2s;
    }
    .stButton > button:hover { transform: translateY(-2px); }

    /* 5. 결과 카드 */
    .result-card {
        animation: fadeInUp 0.7s ease-out;
        background-color: #fff; border: 3px solid var(--primary);
        border-radius: 25px; padding: 30px; text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); margin-top: 20px;
    }
    a { text-decoration: none; color: #FF4B4B; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 상태 관리
if 'choices' not in st.session_state:
    st.session_state.choices = {'step1': None, 'step2': None, 'step3': None, 'step4': None}

def set_choice(step, value):
    st.session_state.choices[step] = value

# --- UI 그리기 함수 ---
def draw_line(is_active=False):
    css = "active" if is_active else ""
    st.markdown(f'<div class="step-wrapper"><div class="tree-line {css}"></div></div>', unsafe_allow_html=True)

def draw_step(step_key, title, options):
    st.markdown('<div class="step-wrapper">', unsafe_allow_html=True)
    with st.container():
        current = st.session_state.choices[step_key]
        icon = "✅" if current else "🔹"
        st.subheader(f"{icon} {title}")
        cols = st.columns(len(options))
        for i, option in enumerate(options):
            with cols[i]:
                btn_type = "primary" if current == option else "secondary"
                if st.button(option, key=f"{step_key}_{option}", type=btn_type):
                    set_choice(step_key, option)
                    # 자동 리런
    st.markdown('</div>', unsafe_allow_html=True)

# ================= 메인 프로그램 =================

st.title("🍽️ 점메추 Master")
st.caption(f"현재 {len(df)}개의 맛집 데이터가 대기 중입니다.")

c1 = st.session_state.choices['step1']
c2 = st.session_state.choices['step2']
c3 = st.session_state.choices['step3']
c4 = st.session_state.choices['step4']

# [1단계] 맵기
draw_step('step1', "맵기", ["매운 맛", "순한 맛"])

# [2단계] 온도
if c1:
    draw_line(True)
    draw_step('step2', "온도", ["뜨거운 것", "차가운 것"])

# [3단계] 종류
if c1 and c2:
    draw_line(True)
    draw_step('step3', "종류", ["한식", "중식", "일식", "양식", "아시안"])

# [4단계] 재료
if c1 and c2 and c3:
    draw_line(True)
    draw_step('step4', "주재료", ["밥", "면", "고기", "빵", "기타"])

# [최종 결과]
if c1 and c2 and c3 and c4:
    draw_line(True)
    
    # 🔍 데이터 필터링
    result_df = df[
        (df['맵기'] == c1) &
        (df['온도'] == c2) &
        (df['종류'] == c3) &
        (df['주재료'] == c4)
    ]
    
    st.divider()
    
    if not result_df.empty:
        # 랜덤 추천
        recommendation = result_df.sample(1).iloc[0]
        menu_name = recommendation['메뉴명']
        
        # 네이버 검색 링크 생성
        search_url = f"https://search.naver.com/search.naver?query=근처 {menu_name} 맛집"
        
        st.markdown(f"""
        <div class="result-card">
            <h3 style="color:#666; margin:0;">오늘의 추천 메뉴</h3>
            <h1 style="color:#FF4B4B; font-size: 3.2rem; margin: 10px 0;">{menu_name}</h1>
            <p style="font-size: 1.1rem; color:#888;">
                <a href="{search_url}" target="_blank">📍 근처 맛집 검색하기 (클릭)</a>
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
        
        # 다른 후보 보여주기
        others = result_df['메뉴명'].tolist()
        if len(others) > 1:
            others_str = ", ".join([m for m in others if m != menu_name])
            if others_str:
                st.info(f"💡 같은 조건의 다른 메뉴: {others_str}")
                
    else:
        # 데이터 없을 때 차선책
        st.warning("조건에 딱 맞는 메뉴가 없어요 😭")
        backup = df[df['종류'] == c3].sample(1).iloc[0]['메뉴명']
        st.success(f"대신 같은 **{c3}** 종류인 **{backup}** 어때요?")

    st.write("")
    if st.button("🔄 처음부터 다시 하기", type="secondary"):
        for k in st.session_state.choices: st.session_state.choices[k] = None
        st.rerun()
