import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime, timedelta

# ==========================================
# 1. 페이지 설정
# ==========================================
st.set_page_config(page_title="오늘의 메뉴", layout="centered")

# ==========================================
# 2. 디자인 (레버 애니메이션의 핵심!)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

    /* 탭 버튼 스타일 */
    div.stButton > button {
        width: 100%; height: 60px; font-size: 19px; font-weight: 700;
        border-radius: 12px; border: 1px solid #ddd; background-color: #fff;
        transition: all 0.2s;
    }
    div.stButton > button:hover { border-color: #FF4B4B; color: #FF4B4B; }
    div.stButton > button[kind="primary"] { background-color: #FF4B4B; color: white !important; border: none; }

    /* 🕹️ [핵심] 리얼한 3D 레버 버튼 스타일 */
    .lever-container button {
        background: radial-gradient(circle at 30% 30%, #ff6b6b, #c92a2a); /* 3D 빨간 공 */
        color: white !important;
        border: 4px solid #8c1c1c !important;
        border-radius: 50% !important; /* 동그라미 */
        width: 100px !important;
        height: 100px !important;
        font-size: 16px !important;
        box-shadow: 
            0 10px 0 #5c0e0e, /* 두께감 (3D) */
            0 20px 20px rgba(0,0,0,0.4); /* 그림자 */
        margin: 0 auto;
        display: block;
        transition: all 0.1s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    /* 레버 기둥 (가상 요소로 그림) */
    .lever-container::before {
        content: '';
        display: block;
        width: 15px;
        height: 100px;
        background: linear-gradient(90deg, #999, #eee, #999);
        margin: 0 auto;
        position: relative;
        top: 60px; /* 공 아래에 위치 */
        z-index: -1;
    }

    /* 💥 레버 당겼을 때 효과 (애니메이션) */
    .lever-container button:active {
        transform: translateY(60px); /* 아래로 쑥 내려감 */
        box-shadow: 
            0 0 0 #5c0e0e, /* 두께 사라짐 */
            0 0 5px rgba(0,0,0,0.4); /* 그림자 줄어듦 */
        border-color: #5c0e0e !important;
    }

    /* 슬롯머신 화면 */
    .slot-frame {
        background-color: #222;
        padding: 20px;
        border-radius: 15px;
        border: 5px solid #d4af37; /* 금테 */
        box-shadow: inset 0 0 20px #000;
        text-align: center;
        margin-bottom: 20px;
    }
    .slot-screen {
        font-size: 40px;
        font-weight: 900;
        color: #fff;
        text-shadow: 0 0 10px #ffeb3b;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* 결과 카드 */
    .result-card {
        background-color: var(--secondary-background-color);
        border: 2px solid #FF4B4B; border-radius: 20px;
        padding: 30px; text-align: center; margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 데이터 로드 (350개 메뉴)
# ==========================================
@st.cache_data
def load_data():
    raw_list = [
        # [한식]
        "김치찌개", "참치김치찌개", "돼지김치찌개", "스팸김치찌개", "꽁치김치찌개",
        "된장찌개", "차돌된장찌개", "해물된장찌개", "우렁된장찌개", "냉이된장찌개", "강된장",
        "순두부찌개", "해물순두부", "햄치즈순두부", "들깨순두부", "만두순두부", "곱창순두부",
        "부대찌개", "존슨탕", "청국장", "비지찌개", "동태찌개", "알탕", "대구탕", "꽃게탕", "매운탕",
        "갈비탕", "왕갈비탕", "설렁탕", "곰탕", "나주곰탕", "사골국", "도가니탕", "꼬리곰탕", "우족탕",
        "삼계탕", "반계탕", "들깨삼계탕", "누룽지백숙", "닭곰탕", "닭개장",
        "육개장", "추어탕", "통추어탕", "장어탕", "감자탕", "뼈해장국", "선지해장국", "황태해장국", "북엇국",
        "콩나물국밥", "순대국", "얼큰순대국", "돼지국밥", "소머리국밥", "내장탕", "미역국", "소고기무국",
        "떡만두국", "사골만두국", "매생이굴국", "재첩국", "올갱이국", "민물새우탕",
        "비빔밥", "돌솥비빔밥", "산채비빔밥", "육회비빔밥", "꼬막비빔밥", "낙지비빔밥", "멍게비빔밥",
        "김치볶음밥", "참치김치볶음밥", "새우볶음밥", "오므라이스", "소고기볶음밥", "깍두기볶음밥",
        "제육덮밥", "오징어덮밥", "낙지덮밥", "쭈꾸미덮밥", "불고기덮밥", "잡채밥", "카레라이스", "짜장밥", 
        "치킨마요덮밥", "참치마요덮밥", "스팸마요덮밥", "장조림버터비빔밥", "연어덮밥",
        "쌈밥", "제육쌈밥", "우렁쌈밥", "보리밥", "강된장보리밥", "생선구이백반", "게장백반", "불고기백반", "기사식당불백",
        "묵밥", "도토리묵밥", "전복죽", "야채죽", "소고기죽", "호박죽", "팥죽", "낙지김치죽", "삼계죽",
        "삼겹살", "냉동삼겹살", "목살", "항정살", "가브리살", "돼지갈비", "매운돼지갈비찜", "간장갈비찜",
        "소갈비", "소갈비찜", "LA갈비", "차돌박이", "등심", "안심", "육회", "육사시미", 
        "곱창", "대창", "막창", "양대창", "곱창전골", "대창덮밥",
        "닭갈비", "숯불닭갈비", "물닭갈비", "찜닭", "안동찜닭", "로제찜닭", "닭볶음탕", "닭한마리", "치킨", "양념치킨", "파닭",
        "제육볶음", "두부김치", "오징어볶음", "낙지볶음", "쭈꾸미볶음", "코다리조림", "갈치조림", "고등어조림", 
        "고등어구이", "삼치구이", "임연수구이", "갈치구이", "굴비",
        "보쌈", "마늘보쌈", "굴보쌈", "족발", "불족발", "냉채족발", "미니족",
        "아구찜", "해물찜", "대구뽈찜", "등뼈찜", "파전", "해물파전", "김치전", "감자전", "육전", "모둠전", "빈대떡", "도토리묵",
        "떡볶이", "라볶이", "즉석떡볶이", "로제떡볶이", "짜장떡볶이", "궁중떡볶이", "기름떡볶이", "마라떡볶이", "가래떡떡볶이",
        "튀김", "오징어튀김", "새우튀김", "김말이", "순대", "순대볶음", "백순대",
        "김밥", "야채김밥", "참치김밥", "치즈김밥", "돈가스김밥", "새우김밥", "충무김밥", "키토김밥", "주먹밥", "유부초밥",
        "라면", "치즈라면", "만두라면", "해물라면", "부대라면", "짬뽕라면", "비빔면", "짜파게티", "불닭볶음면",
        "칼국수", "바지락칼국수", "닭칼국수", "장칼국수", "비빔칼국수", "들깨칼국수", "팥칼국수", "샤브샤브칼국수",
        "수제비", "들깨수제비", "얼큰수제비", "잔치국수", "비빔국수", "열무국수", "콩국수",
        "냉면", "물냉면", "비빔냉면", "회냉면", "평양냉면", "함흥냉면", "진주냉면",
        "막국수", "비빔막국수", "물막국수", "쫄면", "물쫄면", "비빔만두",
        
        # [중식]
        "짜장면", "간짜장", "삼선짜장", "쟁반짜장", "유니짜장", "사천짜장", "고추짜장",
        "짬뽕", "삼선짬뽕", "백짬뽕", "고기짬뽕", "차돌짬뽕", "굴짬뽕", "홍합짬뽕", "볶음짬뽕", "냉짬뽕", "순두부짬뽕",
        "볶음밥", "새우볶음밥", "삼선볶음밥", "게살볶음밥", "잡채밥", "마파두부밥", "유산슬밥", "잡탕밥", "고추잡채밥", "중화비빔밥",
        "탕수육", "찹쌀탕수육", "사천탕수육", "광동식탕수육", "꿔바로우",
        "깐풍기", "유린기", "라조기", "난자완스", "팔보채", "양장피", "유산슬", "고추잡채", "경장육사", "어향가지",
        "군만두", "물만두", "찐만두", "꽃빵", "멘보샤", "크림새우", "칠리새우", "깐쇼새우",
        "마라탕", "마라샹궈", "마라반", "훠궈", "양꼬치", "양갈비", "지삼선", "토마토계란볶음", "우육면", "탄탄면", "동파육",
        
        # [일식]
        "초밥", "모듬초밥", "특선초밥", "연어초밥", "광어초밥", "새우초밥", "참치초밥", "소고기초밥", "후토마키", "지라시스시",
        "회덮밥", "사케동", "연어뱃살덮밥", "규동", "가츠동", "에비동", "오야코동", "부타동", "차슈동", "장어덮밥", "우나기동", "텐동", "카이센동", "스테키동",
        "우동", "튀김우동", "유부우동", "김치우동", "냉우동", "붓카케우동", "카레우동", "크림우동", "니꾸우동",
        "소바", "냉모밀", "판모밀", "온모밀", "마제소바", "아부라소바", "자루소바",
        "라멘", "돈코츠라멘", "미소라멘", "소유라멘", "시오라멘", "카라이라멘", "탄탄멘", "츠케멘", "나가사키짬뽕",
        "돈가스", "등심돈가스", "안심돈가스", "치즈돈가스", "고구마치즈돈가스", "카레돈가스", "경양식돈가스", "생선가스", "멘치카츠",
        "돈가스나베", "김치나베", "밀푀유나베", "스키야키", "샤브샤브", "편백찜", "모츠나베", "창코나베",
        "일본카레", "하이라이스", "오꼬노미야끼", "타코야끼", "야끼소바",
        
        # [양식]
        "토마토파스타", "미트볼파스타", "해산물토마토파스타", "아라비아따", "뽀모도로",
        "크림파스타", "까르보나라", "해산물크림파스타", "베이컨크림파스타", "명란크림파스타", "빠네파스타",
        "로제파스타", "새우로제파스타", "게살로제파스타",
        "오일파스타", "알리오올리오", "봉골레", "명란오일파스타", "바질페스토파스타", "엔초비파스타",
        "투움바파스타", "라자냐", "뇨끼", "감자뇨끼", "단호박뇨끼",
        "리조또", "크림리조또", "토마토리조또", "오징어먹물리조또", "전복리조또", "버섯리조또",
        "피자", "고르곤졸라", "페퍼로니피자", "포테이토피자", "불고기피자", "시카고피자", "하와이안피자", "마르게리따", "루꼴라피자",
        "스테이크", "티본스테이크", "찹스테이크", "함박스테이크", "돈마호크", "폭립", "비프웰링턴", "바베큐플래터",
        "햄버거", "치즈버거", "수제버거", "치킨버거", "새우버거", "베이컨버거", "머쉬룸버거",
        "샌드위치", "클럽샌드위치", "에그샌드위치", "참치샌드위치", "치킨샌드위치", "잠봉뵈르", "반미샌드위치",
        "토스트", "프렌치토스트", "이삭토스트", "베이글", "크림치즈베이글", "연어베이글", "파니니", "핫도그",
        "샐러드", "닭가슴살샐러드", "리코타치즈샐러드", "연어샐러드", "콥샐러드", "시저샐러드", "파스타샐러드", "포케", "연어포케", "참치포케",
        "양송이스프", "콘스프", "클램차우더", "단호박스프", "감바스", "에그인헬", "샥슈카", "그라탕",
        
        # [아시안/기타]
        "쌀국수", "양지쌀국수", "차돌쌀국수", "매운쌀국수", "해산물쌀국수",
        "분짜", "반미", "월남쌈", "짜조", "스프링롤",
        "팟타이", "나시고랭", "미시고랭", "푸팟퐁커리", "똠양꿍", "그린커리", "레드커리", "파인애플볶음밥",
        "타코", "부리또", "퀘사디아", "화이타", "엔칠라다", "치미창가", "나초",
        "케밥", "양고기케밥", "치킨케밥", "인도커리", "버터치킨커리", "난", "갈릭난", "탄두리치킨", "라씨"
    ]
    
    def auto_tag(m):
        spicy, temp, kind, main = "순한 맛", "뜨거운 것", "한식", "기타"
        if any(k in m for k in ["김치","매운","짬뽕","마라","떡볶이","육개장","비빔","낙지","쭈꾸미","닭갈비","얼큰","핫","사천","불족발","카라이","탄탄","똠양","감자탕","해물탕","아구찜","해물찜","닭발","고추","레드","아라비아따","화이타"]): spicy = "매운 맛"
        if any(k in m for k in ["냉","소바","초밥","회","샐러드","샌드위치","김밥","빙수","묵밥","포케","월남쌈","쫄면","막국수","비빔면","족발","보쌈","양장피","냉채"]): temp = "차가운 것"
        if any(k in m for k in ["짜장","짬뽕","탕수육","마라","꿔바로우","유린기","양꼬치","훠궈","깐풍","동파육","우육","탄탄"]): kind="중식"
        elif any(k in m for k in ["초밥","우동","소바","라멘","카츠","가츠","규동","사케동","오꼬노미","스시","나베","텐동","부타동","야끼","스키야키","샤브샤브","일식","후토마키","장어","오야코"]): kind="일식"
        elif any(k in m for k in ["파스타","피자","버거","스테이크","샐러드","샌드위치","리조또","스프","라자냐","뇨끼","토스트","베이글","감바스","파니니","핫도그","바베큐","폭립","그라탕","잠봉","브런치"]): kind="양식"
        elif any(k in m for k in ["쌀국수","팟타이","나시고랭","분짜","타코","부리또","커리","반미","퀘사디아","케밥","화이타","똠양","난","탄두리","짜조","스프링롤","치미창가"]): kind="아시안"
        if any(k in m for k in ["밥","죽","리조또","동","초밥","필라프","포케","볶음밥","덮밥","국밥","백반"]): main="밥"
        elif any(k in m for k in ["면","국수","우동","파스타","라멘","짜장","짬뽕","팟타이","잡채"]): main="면"
        elif any(k in m for k in ["고기","스테이크","삼겹살","갈비","제육","보쌈","족발","탕수육","돈가스","치킨","육회","찜닭","곱창","대창","막창","차돌","등심","안심","함박","동파육"]): main="고기"
        elif any(k in m for k in ["빵","버거","샌드위치","토스트","피자","베이글","핫도그","반미","타코","부리또"]): main="빵"
        return {"메뉴명":m, "맵기":spicy, "온도":temp, "종류":kind, "주재료":main}
    return pd.DataFrame([auto_tag(m) for m in raw_list])

df_logic = load_data()

# ==========================================
# 3. 로직 및 UI 함수
# ==========================================
if 'mode' not in st.session_state:
    st.session_state.mode = 'logic' # 기본값
if 'choices' not in st.session_state:
    st.session_state.choices = {'step1': None, 'step2': None, 'step3': None, 'step4': None}
if 'slot_result' not in st.session_state:
    st.session_state.slot_result = "777"

def set_choice(step, value):
    st.session_state.choices[step] = value

# 추천 알고리즘
def recommend_food(df, choices):
    df['score'] = 0
    df.loc[df['종류'] == choices['step3'], 'score'] += 40
    df.loc[df['주재료'] == choices['step4'], 'score'] += 30
    df.loc[df['맵기'] == choices['step1'], 'score'] += 15
    df.loc[df['온도'] == choices['step2'], 'score'] += 15
    
    top = df.sort_values(by='score', ascending=False).head(20)
    best_score = top.iloc[0]['score']
    pool = top[top['score'] >= best_score - 15]
    final = pool.sample(1).iloc[0]['메뉴명']
    others = pool[pool['메뉴명'] != final].sample(min(2, len(pool)-1))['메뉴명'].tolist()
    return final, others

# 시간 기반 제목
def get_time_title():
    h = (datetime.utcnow() + timedelta(hours=9)).hour
    if 5 <= h < 11: return "☀️ 아메추"
    elif 11 <= h < 17: return "🕛 점메추"
    else: return "🌙 저메추"

# ==========================================
# 4. 메인 화면 & 탭
# ==========================================
st.title(get_time_title())

col_tab1, col_tab2 = st.columns(2)
with col_tab1:
    btn_type = "primary" if st.session_state.mode == 'logic' else "secondary"
    if st.button("🚀 스스로 선택", key="tab_logic", type=btn_type):
        st.session_state.mode = 'logic'; st.rerun()
with col_tab2:
    btn_type = "primary" if st.session_state.mode == 'random' else "secondary"
    if st.button("🎰 랜덤 룰렛", key="tab_random", type=btn_type):
        st.session_state.mode = 'random'; st.rerun()

st.write("")

# ----------------------------
# MODE 1: 스스로 선택
# ----------------------------
if st.session_state.mode == 'logic':
    st.subheader("취향을 선택해주세요")
    
    # 1. 맵기
    c1, c2 = st.columns(2)
    cur = st.session_state.choices['step1']
    if c1.button("매운 맛", type="primary" if cur=="매운 맛" else "secondary"): 
        set_choice('step1', "매운 맛"); st.rerun()
    if c2.button("순한 맛", type="primary" if cur=="순한 맛" else "secondary"): 
        set_choice('step1', "순한 맛"); st.rerun()
    
    # 2. 온도
    if st.session_state.choices['step1']:
        st.write("")
        c1, c2 = st.columns(2)
        cur = st.session_state.choices['step2']
        if c1.button("뜨거운 것", type="primary" if cur=="뜨거운 것" else "secondary"): 
            set_choice('step2', "뜨거운 것"); st.rerun()
        if c2.button("차가운 것", type="primary" if cur=="차가운 것" else "secondary"): 
            set_choice('step2', "차가운 것"); st.rerun()
            
    # 3. 종류 (버튼 3/2 배열)
    if st.session_state.choices['step2']:
        st.write("")
        st.subheader("종류")
        cols = st.columns(3)
        opts = ["한식", "중식", "일식", "양식", "아시안"]
        cur = st.session_state.choices['step3']
        for i, opt in enumerate(opts):
            with cols[i%3]:
                if st.button(opt, key=f"logic_{opt}", type="primary" if cur==opt else "secondary"):
                    set_choice('step3', opt); st.rerun()
                    
    # 4. 재료
    if st.session_state.choices['step3']:
        st.write("")
        st.subheader("주재료")
        cols = st.columns(3)
        opts = ["밥", "면", "고기", "빵", "기타"]
        cur = st.session_state.choices['step4']
        for i, opt in enumerate(opts):
            with cols[i%3]:
                if st.button(opt, key=f"logic_{opt}", type="primary" if cur==opt else "secondary"):
                    set_choice('step4', opt); st.rerun()

    # 결과
    if st.session_state.choices['step4']:
        st.markdown("---")
        final, similar = recommend_food(df_logic, st.session_state.choices)
        
        # 결과 표시
        st.markdown(f"""
        <div class="result-card">
            <p style="color:gray;">분석 결과</p>
            <h1 style="color:#FF4B4B; font-size:3em; margin:10px;">{final}</h1>
            <p style="opacity:0.7;">{st.session_state.choices['step1']} · {st.session_state.choices['step2']} · {st.session_state.choices['step3']}</p>
            <p style="font-size:14px; color:#555;">🤔 다른 추천: {', '.join(similar)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        col1, col2 = st.columns(2)
        col1.link_button("N 네이버지도", f"https://map.naver.com/v5/search/내주변 {final}", use_container_width=True)
        col2.link_button("K 카카오맵", f"https://map.kakao.com/link/search/내주변 {final}", use_container_width=True)
        
        st.write("")
        if st.button("🔄 다시 하기", type="secondary", use_container_width=True):
            st.session_state.choices = {'step1':None,'step2':None,'step3':None,'step4':None}
            st.rerun()

# ----------------------------
# MODE 2: 랜덤 슬롯머신
# ----------------------------
else:
    st.subheader("🎰 운명의 룰렛")
    
    slot_display = st.empty()
    
    # 대기 상태
    if st.session_state.slot_result == "777":
        slot_display.markdown("""
        <div class="slot-frame">
            <div class="slot-screen">🎰 777 🎰</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 🕹️ 레버 버튼 (3D Red Ball)
        st.markdown('<div class="lever-container">', unsafe_allow_html=True)
        if st.button("PULL", key="lever_btn"):
            # 애니메이션
            candidates = df_logic['메뉴명'].tolist()
            sleep_time = 0.05
            for i in range(15):
                temp = random.choice(candidates)
                slot_display.markdown(f"""
                <div class="slot-frame">
                    <div class="slot-screen" style="color:#aaa;">{temp}</div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(sleep_time)
                if i > 8: sleep_time += 0.05
            
            final = random.choice(candidates)
            st.session_state.slot_result = final
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
            
    # 결과 상태
    else:
        final = st.session_state.slot_result
        slot_display.markdown(f"""
        <div class="slot-frame" style="border-color:#FF4B4B; box-shadow:0 0 30px #FF4B4B;">
            <div class="slot-screen" style="color:#FF4B4B;">🎉 {final} 🎉</div>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
        
        col1, col2 = st.columns(2)
        col1.link_button("N 네이버지도", f"https://map.naver.com/v5/search/내주변 {final}", use_container_width=True)
        col2.link_button("K 카카오맵", f"https://map.kakao.com/link/search/내주변 {final}", use_container_width=True)
        
        st.write("")
        if st.button("🔄 한 번 더 돌리기", type="secondary", use_container_width=True):
            st.session_state.slot_result = "777"
            st.rerun()
