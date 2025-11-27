import streamlit as st
import pandas as pd
import random
import time

# ==========================================
# 1. 페이지 설정 & 테마 최적화 CSS
# ==========================================
st.set_page_config(page_title="점메추 Ultimate", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 가독성 최적화: 제목 */
    h3 {
        color: var(--text-color) !important;
        font-weight: 700;
        opacity: 0.9;
        margin-bottom: 10px;
    }

    /* 버튼 스타일 */
    div.stButton > button {
        width: 100%;
        height: 65px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 16px;
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        font-size: 19px;
        font-weight: 700;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        border-color: #FF4B4B;
        color: #FF4B4B;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        color: white !important;
        border: none;
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
    }

    /* 프로그레스 바 */
    .progress-container {
        width: 100%;
        background-color: rgba(128, 128, 128, 0.2);
        border-radius: 10px;
        margin-bottom: 30px;
        height: 8px;
        overflow: hidden;
    }
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #FF6B6B, #FF8E53);
        transition: width 0.5s ease-in-out;
        border-radius: 10px;
    }

    /* 결과 카드 */
    .result-card {
        background: var(--secondary-background-color);
        border: 2px solid #FF6B6B;
        border-radius: 24px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        animation: popUp 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    @keyframes popUp {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }
    
    .link-btn {
        display: inline-block;
        margin-top: 20px;
        padding: 12px 24px;
        background: var(--text-color);
        color: var(--background-color) !important;
        border-radius: 30px;
        text-decoration: none;
        font-weight: bold;
        transition: opacity 0.3s;
    }
    .link-btn:hover { opacity: 0.8; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 데이터 로드 (250개 이상)
# ==========================================
@st.cache_data
def load_data():
    raw_list = [
        # [한식 - 찌개/국/탕]
        "김치찌개", "참치김치찌개", "돼지김치찌개", "꽁치김치찌개", "된장찌개", "차돌된장찌개", "해물된장찌개", 
        "순두부찌개", "해물순두부", "부대찌개", "청국장", "비지찌개", "동태찌개", "알탕", "대구탕", 
        "꽃게탕", "매운탕", "갈비탕", "설렁탕", "곰탕", "도가니탕", "꼬리곰탕", "삼계탕", "반계탕", 
        "닭곰탕", "육개장", "닭개장", "추어탕", "장어탕", "감자탕", "뼈해장국", "선지해장국", 
        "황태해장국", "콩나물국밥", "순대국", "돼지국밥", "소머리국밥", "미역국", "무국", "북엇국",
        
        # [한식 - 밥]
        "비빔밥", "돌솥비빔밥", "육회비빔밥", "꼬막비빔밥", "낙지비빔밥", "멍게비빔밥", 
        "김치볶음밥", "새우볶음밥", "오므라이스", "제육덮밥", "오징어덮밥", "낙지덮밥", "쭈꾸미덮밥", 
        "참치마요덮밥", "치킨마요덮밥", "스팸마요덮밥", "불고기덮밥", "잡채밥", "카레라이스", "짜장밥",
        "쌈밥", "보리밥", "생선구이백반", "게장백반", "불고기백반", "묵밥", "죽", "전복죽", "호박죽",
        
        # [한식 - 고기/메인]
        "삼겹살", "목살", "항정살", "돼지갈비", "갈매기살", "냉동삼겹살", "소갈비", "차돌박이", "등심", 
        "안심", "육회", "육사시미", "닭갈비", "숯불닭갈비", "찜닭", "안동찜닭", "로제찜닭", "닭볶음탕", 
        "닭한마리", "제육볶음", "두부김치", "오징어볶음", "낙지볶음", "쭈꾸미볶음", "코다리조림", "갈치조림", 
        "고등어조림", "보쌈", "마늘보쌈", "족발", "불족발", "냉채족발", "곱창", "대창", "막창", "곱창전골",
        "아구찜", "해물찜", "대구뽈찜", "등뼈찜", "파전", "해물파전", "김치전", "감자전", "육전", "모둠전",
        
        # [분식/면]
        "떡볶이", "라볶이", "즉석떡볶이", "로제떡볶이", "짜장떡볶이", "궁중떡볶이", "기름떡볶이", 
        "튀김", "순대", "김밥", "참치김밥", "치즈김밥", "돈가스김밥", "충무김밥", "키토김밥",
        "라면", "치즈라면", "만두라면", "해물라면", "부대라면", "칼국수", "바지락칼국수", "닭칼국수", 
        "장칼국수", "비빔칼국수", "들깨칼국수", "수제비", "들깨수제비", "잔치국수", "비빔국수", 
        "열무국수", "콩국수", "냉면", "물냉면", "비빔냉면", "회냉면", "평양냉면", "함흥냉면", 
        "막국수", "쫄면", "만두국", "떡만두국", "떡국", "비빔만두",
        
        # [중식]
        "짜장면", "간짜장", "삼선짜장", "쟁반짜장", "유니짜장", "사천짜장", "짬뽕", "삼선짬뽕", 
        "백짬뽕", "고기짬뽕", "차돌짬뽕", "굴짬뽕", "홍합짬뽕", "볶음짬뽕", "냉짬뽕", 
        "중화볶음밥", "마파두부밥", "유산슬밥", "잡탕밥", "고추잡채밥", 
        "탕수육", "찹쌀탕수육", "사천탕수육", "꿔바로우", "깐풍기", "유린기", "라조기", "난자완스", 
        "팔보채", "양장피", "유산슬", "고추잡채", "군만두", "물만두", "꽃빵", "멘보샤", 
        "마라탕", "마라샹궈", "훠궈", "양꼬치", "양갈비", "우육면", "탄탄면", "동파육", "크림새우", "칠리새우",
        
        # [일식]
        "초밥", "모듬초밥", "연어초밥", "광어초밥", "새우초밥", "참치초밥", "소고기초밥", "유부초밥", "후토마키",
        "회덮밥", "사케동", "규동", "가츠동", "에비동", "오야코동", "부타동", "차슈동", "장어덮밥", "텐동", "카이센동", 
        "우동", "튀김우동", "유부우동", "김치우동", "냉우동", "붓카케우동", "카레우동", "크림우동",
        "소바", "냉모밀", "판모밀", "온모밀", "마제소바", "라멘", "돈코츠라멘", "미소라멘", "소유라멘", 
        "시오라멘", "카라이라멘", "탄탄멘", "츠케멘", 
        "돈가스", "등심돈가스", "안심돈가스", "치즈돈가스", "고구마치즈돈가스", "카레돈가스", "경양식돈가스", 
        "돈가스나베", "김치나베", "밀푀유나베", "스키야키", "샤브샤브", "편백찜", 
        "일본카레", "하이라이스", "오꼬노미야끼", "타코야끼", "야끼소바",
        
        # [양식]
        "토마토파스타", "크림파스타", "로제파스타", "알리오올리오", "봉골레", "까르보나라", "볼로네제", "빠네파스타", 
        "명란파스타", "바질페스토파스타", "투움바파스타", "라자냐", "뇨끼", 
        "리조또", "크림리조또", "토마토리조또", "오징어먹물리조또", "전복리조또",
        "피자", "고르곤졸라", "페퍼로니피자", "포테이토피자", "불고기피자", "시카고피자", "하와이안피자", "마르게리따",
        "스테이크", "티본스테이크", "찹스테이크", "함박스테이크", "돈마호크", "폭립", "비프웰링턴",
        "햄버거", "치즈버거", "수제버거", "치킨버거", "새우버거", "베이컨버거",
        "샌드위치", "클럽샌드위치", "서브웨이", "에그드랍", "이삭토스트", "프렌치토스트", "베이글", "크림치즈베이글", "파니니", "핫도그", 
        "샐러드", "닭가슴살샐러드", "리코타치즈샐러드", "연어샐러드", "콥샐러드", "시저샐러드", "파스타샐러드", "포케", 
        "양송이스프", "콘스프", "클램차우더", "감바스", "에그인헬", "샥슈카",
        
        # [아시안/기타]
        "쌀국수", "매운쌀국수", "차돌쌀국수", "분짜", "반미", "월남쌈", "짜조", 
        "팟타이", "나시고랭", "미시고랭", "푸팟퐁커리", "똠양꿍", "그린커리",
        "타코", "부리또", "퀘사디아", "화이타", "엔칠라다", "케밥", 
        "인도커리", "난", "탄두리치킨", "라씨"
    ]
    
    def auto_tag(m):
        spicy, temp, kind, main = "순한 맛", "뜨거운 것", "한식", "기타"
        
        # 1. 맵기 키워드 확장
        if any(k in m for k in ["김치","매운","짬뽕","마라","떡볶이","육개장","비빔","양념","낙지","쭈꾸미","닭갈비","얼큰","핫","사천","불족발","카라이","탄탄","똠양","감자탕","해물탕","아구찜","해물찜","닭발"]): 
            spicy = "매운 맛"
            
        # 2. 온도 키워드 확장
        if any(k in m for k in ["냉","소바","초밥","회","샐러드","샌드위치","김밥","빙수","묵밥","포케","월남쌈","육회","쫄면","막국수","비빔면"]): 
            temp = "차가운 것"
            
        # 3. 종류 상세 분류
        if any(k in m for k in ["짜장","짬뽕","탕수육","마라","꿔바로우","유린기","동파육","우육","탄탄","양꼬치","훠궈","멘보샤","깐풍","라조기","난자완스","팔보채","중화"]): kind="중식"
        elif any(k in m for k in ["초밥","우동","소바","라멘","카츠","가츠","규동","사케동","오꼬노미","스시","나베","텐동","부타동","야끼","스키야키","샤브샤브","일식","후토마키"]): kind="일식"
        elif any(k in m for k in ["파스타","피자","버거","스테이크","샐러드","샌드위치","리조또","스프","라자냐","뇨끼","토스트","베이글","감바스","파니니","핫도그","바베큐","폭립"]): kind="양식"
        elif any(k in m for k in ["쌀국수","팟타이","나시고랭","미시고랭","분짜","타코","부리또","커리","반미","퀘사디아","케밥","화이타","똠양","난","탄두리","짜조"]): kind="아시안"
        
        # 4. 주재료 상세 분류
        if any(k in m for k in ["밥","죽","리조또","동","초밥","필라프","포케","볶음밥","덮밥","국밥","백반"]): main="밥"
        elif any(k in m for k in ["면","국수","우동","소바","파스타","라멘","짜장","짬뽕","팟타이","잡채","소면"]): main="면"
        elif any(k in m for k in ["고기","스테이크","삼겹살","갈비","제육","보쌈","족발","탕수육","돈가스","치킨","육회","찜닭","곱창","대창","막창","차돌","등심","안심","함박","동파육"]): main="고기"
        elif any(k in m for k in ["빵","버거","샌드위치","토스트","피자","베이글","핫도그","케밥","반미","타코","부리또"]): main="빵"
        
        return {"메뉴명":m, "맵기":spicy, "온도":temp, "종류":kind, "주재료":main}
    
    return pd.DataFrame([auto_tag(m) for m in raw_list])

df_logic = load_data()

# ==========================================
# 3. 상태 관리 및 UI 함수
# ==========================================
if 'choices' not in st.session_state:
    st.session_state.choices = {'step1': None, 'step2': None, 'step3': None, 'step4': None}

def set_choice(step, value):
    st.session_state.choices[step] = value

def draw_progress_bar(percent):
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {percent}%;"></div>
    </div>
    """, unsafe_allow_html=True)

def draw_step(step_key, title, options):
    current = st.session_state.choices[step_key]
    
    # 테마 적응형 아이콘 + 제목
    icon = "✅" if current else "🔹"
    st.markdown(f"### {icon} {title}")
    
    cols = st.columns(len(options))
    for i, option in enumerate(options):
        with cols[i]:
            btn_type = "primary" if current == option else "secondary"
            if st.button(option, key=f"{step_key}_{option}", type=btn_type):
                set_choice(step_key, option)
                st.rerun()

# ==========================================
# 4. 메인 화면 구성
# ==========================================
st.title("🍽️ 점메추 Ultimate")
st.caption(f"데이터베이스 업그레이드 완료: 총 {len(df_logic)}개의 메뉴가 대기 중입니다.")

# 진행률 계산
current_step = 0
if st.session_state.choices['step1']: current_step = 1
if st.session_state.choices['step2']: current_step = 2
if st.session_state.choices['step3']: current_step = 3
if st.session_state.choices['step4']: current_step = 4
draw_progress_bar(current_step * 25)

c1 = st.session_state.choices['step1']
c2 = st.session_state.choices['step2']
c3 = st.session_state.choices['step3']
c4 = st.session_state.choices['step4']

# 단계별 질문
draw_step('step1', "Q1. 맵기 선택", ["매운 맛", "순한 맛"])

if c1:
    st.write("")
    draw_step('step2', "Q2. 온도 선택", ["뜨거운 것", "차가운 것"])

if c1 and c2:
    st.write("")
    draw_step('step3', "Q3. 종류 선택", ["한식", "중식", "일식", "양식", "아시안"])

if c1 and c2 and c3:
    st.write("")
    draw_step('step4', "Q4. 주재료 선택", ["밥", "면", "고기", "빵", "기타"])

# 최종 결과
if c1 and c2 and c3 and c4:
    st.markdown("---")
    
    result_df = df_logic[
        (df_logic['맵기']==c1) & (df_logic['온도']==c2) & 
        (df_logic['종류']==c3) & (df_logic['주재료']==c4)
    ]
    
    if not result_df.empty:
        final_menu = result_df.sample(1).iloc[0]['메뉴명']
        search_url = f"https://map.naver.com/v5/search/근처 {final_menu}"
        
        st.markdown(f"""
        <div class="result-card">
            <h3>오늘의 최적 메뉴</h3>
            <h1 style="font-size: 3.5rem; background: linear-gradient(90deg, #FF6B6B, #FF8E53); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                {final_menu}
            </h1>
            <p style="opacity: 0.7; font-size:1.1rem; margin-bottom:30px;">
                {c1} · {c2} · {c3} · {c4}
            </p>
            <a href="{search_url}" target="_blank" class="link-btn">
                📍 근처 맛집 지도 보기
            </a>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
        
        # 추가 추천
        others = result_df['메뉴명'].tolist()
        if len(others) > 1:
            others = [x for x in others if x != final_menu]
            random.shuffle(others)
            others_txt = ", ".join(others[:5])
            st.info(f"💡 그 외 추천: {others_txt}")
            
    else:
        # 검색 실패 시 차선책 (종류만 같은 거)
        backup = df_logic[df_logic['종류']==c3].sample(1).iloc[0]['메뉴명']
        st.warning("조건에 딱 맞는 메뉴가 없어요 🥲")
        st.markdown(f"""
        <div class="result-card">
            <h3>대신 이건 어때요?</h3>
            <h1 style="color: var(--text-color);">{backup}</h1>
            <a href="https://map.naver.com/v5/search/근처 {backup}" target="_blank" class="link-btn">
                지도 보기
            </a>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    if st.button("🔄 처음부터 다시 하기", type="secondary"):
        for k in st.session_state.choices: st.session_state.choices[k] = None
        st.rerun()
