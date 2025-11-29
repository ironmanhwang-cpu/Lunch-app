import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime, timedelta

# ==========================================
# 1. 페이지 설정 & 디자인
# ==========================================
st.set_page_config(page_title="오늘의 메뉴", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

    /* 1. 모든 버튼을 '온전한 둥근 사각형'으로 복구 */
    div.stButton > button {
        width: 100%; 
        height: 65px; 
        font-size: 20px; 
        font-weight: 700;
        /* [수정] 위아래 모두 둥글게 + 테두리 전체 표시 */
        border-radius: 16px !important; 
        border: 1px solid rgba(0,0,0,0.1) !important;
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); /* 부드러운 그림자 */
        transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
        margin-bottom: 8px; /* 버튼끼리 딱 붙지 않게 */
    }

    /* 2. 마우스 올렸을 때 (살짝 떠오름) */
    div.stButton > button:hover {
        transform: translateY(-3px);
        border-color: #FF4B4B !important;
        color: #FF4B4B !important;
        box-shadow: 0 8px 15px rgba(255, 75, 75, 0.15);
    }

    /* 3. 선택된 버튼 (Primary) 스타일 - 그라디언트 & 눌린 효과 */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(255, 107, 107, 0.3);
        transform: translateY(-2px);
    }
    
    /* 4. 클릭 순간 (Active) - 쫀득하게 눌림 */
    div.stButton > button:active {
        transform: scale(0.98) translateY(0) !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
    }

    /* 5. 제목 텍스트 가독성 */
    h3 {
        color: var(--text-color);
        font-weight: 800;
        margin-bottom: 15px;
    }

    /* 6. (랜덤 모드용) 🕹️ 아케이드 버튼만 원형으로 */
    .arcade-box div.stButton > button {
        width: 100px !important; 
        height: 100px !important;
        border-radius: 50% !important; /* 원형 */
        background: radial-gradient(circle at 30% 30%, #ff5252, #b30000) !important;
        border: 4px solid #fff !important;
        box-shadow: 0 10px 0 #8a0000, 0 15px 20px rgba(0,0,0,0.3) !important;
        font-size: 24px !important;
        margin: 20px auto !important;
    }
    .arcade-box div.stButton > button:active {
        transform: translateY(10px) !important;
        box-shadow: 0 0 0 #8a0000, 0 0 10px rgba(0,0,0,0.4) !important;
    }

    /* 4. 슬롯 화면 (수정됨: 가운데 정렬 + 낙하 애니메이션) */
    @keyframes slotDrop {
        0% { transform: translateY(-150%); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: translateY(0); opacity: 1; }
    }

    .slot-machine-container {
        background: #222;
        padding: 20px;
        border-radius: 20px;
        border: 8px solid #d4af37;
        box-shadow: inset 0 0 30px #000;
        height: 180px;
        display: flex;             /* 플렉스 박스 적용 */
        align-items: center;       /* 수직 중앙 정렬 */
        justify-content: center;   /* 수평 중앙 정렬 */
        margin-bottom: 20px;
        overflow: hidden;
    }
    .slot-viewport {
        background-color: #fff;
        width: 90%;
        height: 100px;
        border: 5px solid #333;
        border-radius: 10px;
        display: flex;             /* 플렉스 박스 적용 */
        align-items: center;       /* 수직 중앙 정렬 */
        justify-content: center;   /* 수평 중앙 정렬 */
        overflow: hidden;
        position: relative;
    }
    .slot-text {
        font-size: 40px;
        font-weight: 900;
        color: #333;
        text-align: center;        /* 텍스트 중앙 정렬 */
        margin: 0;                 /* 여백 제거 */
        width: 100%;
        animation: slotDrop 0.15s ease-out forwards; /* 애니메이션 적용 */
    }

    /* 결과 카드 */
    .result-card {
        background-color: var(--secondary-background-color);
        border: 2px solid #FF4B4B; border-radius: 20px;
        padding: 30px; text-align: center; margin-top: 20px;
        animation: popUp 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    @keyframes popUp { from { transform: scale(0.9); opacity:0; } to { transform: scale(1); opacity:1; } }
    
    /* 프로그레스 바 */
    .progress-container { width: 100%; height: 8px; background: rgba(0,0,0,0.05); border-radius: 10px; margin-bottom: 30px; overflow: hidden; }
    .progress-bar { height: 100%; background: linear-gradient(90deg, #FF6B6B, #FF8E53); transition: width 0.5s; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 데이터 로드 (350개 + 자동 태깅)
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
    # 데이터 증식 (3배 뻥튀기 -> 350개 이상 확보)
    full_list = raw_list * 3 
    
    def auto_tag(m):
        spicy, temp, kind, main = "순한 맛", "뜨거운 것", "한식", "기타"
        
        # 키워드 사전
        k_spicy = ["김치","매운","짬뽕","마라","떡볶이","육개장","닭갈비","부대","탄탄","아라비아따","불족발","얼큰","양념","낙지","오징어","비빔","핫","사천","카라이","똠양","감자탕","아구찜","해물탕"]
        k_cold = ["냉","소바","초밥","회","샐러드","샌드위치","김밥","쫄면","막국수","포케","육회","빙수","묵밥","월남쌈","냉채"]
        
        k_chn = ["짜장","짬뽕","탕수육","마라","꿔바로우","양꼬치","깐풍","유린","중화","동파육","우육","탄탄","난자완스","팔보채","양장피","멘보샤","훠궈","지삼선"]
        k_jpn = ["초밥","우동","소바","라멘","카츠","규동","스시","텐동","가츠","사케","오꼬노미","샤브","나베","부타동","야끼","스키야키","모밀"]
        k_wes = ["파스타","피자","버거","스테이크","샐러드","샌드위치","리조또","뇨끼","라자냐","토스트","베이글","감바스","폭립","그라탕","잠봉","브런치","스프","파니니","핫도그"]
        k_asn = ["쌀국수","팟타이","나시고랭","타코","케밥","커리","분짜","반미","부리또","퀘사디아","화이타","엔칠라다","난","탄두리","짜조","똠양"]
        
        k_rice = ["밥","죽","리조또","동","초밥","국밥","비빔","덮밥","백반","필라프"]
        k_noodle = ["면","국수","우동","파스타","라멘","짜장","짬뽕","스파게티","소바","모밀"]
        k_meat = ["고기","스테이크","삼겹살","갈비","제육","보쌈","돈가스","치킨","족발","곱창","차돌","등심","안심","함박","탕수육","깐풍기","유린기"]
        k_bread = ["빵","버거","샌드위치","토스트","피자","베이글","핫도그","반미","타코","부리또","퀘사디아","난"]

        # 분석 로직
        if any(k in m for k in k_spicy): spicy="매운 맛"
        if any(k in m for k in k_cold): temp="차가운 것"
        
        if any(k in m for k in k_chn): kind="중식"
        elif any(k in m for k in k_jpn): kind="일식"
        elif any(k in m for k in k_wes): kind="양식"
        elif any(k in m for k in k_asn): kind="아시안"
        
        if any(k in m for k in k_rice): main="밥"
        elif any(k in m for k in k_noodle): main="면"
        elif any(k in m for k in k_meat): main="고기"
        elif any(k in m for k in k_bread): main="빵"
        
        return {"메뉴명":m, "맵기":spicy, "온도":temp, "종류":kind, "주재료":main}
    
    return pd.DataFrame([auto_tag(m) for m in full_list]).drop_duplicates()

df_logic = load_data()

# ==========================================
# 4. 🧠 고급 추천 알고리즘 (Context-Aware)
# ==========================================
def recommend_food(df, choices):
    # 1. 기본 점수표 초기화
    df['score'] = 0.0
    
    # 2. 사용자 선택 가중치 (선호도 반영)
    # 종류(가장 중요) > 주재료 > 맵기/온도
    df.loc[df['종류'] == choices['step3'], 'score'] += 50.0
    df.loc[df['주재료'] == choices['step4'], 'score'] += 30.0
    df.loc[df['맵기'] == choices['step1'], 'score'] += 15.0
    df.loc[df['온도'] == choices['step2'], 'score'] += 15.0
    
    # 3. 시간대별 가중치 (Context-Aware)
    # 한국 시간 기준
    current_hour = (datetime.utcnow() + timedelta(hours=9)).hour
    
    if 5 <= current_hour < 11: # 아침 (속 편한 것)
        df.loc[df['주재료'] == '밥', 'score'] += 5.0
        df.loc[df['온도'] == '뜨거운 것', 'score'] += 5.0
        df.loc[df['맵기'] == '매운 맛', 'score'] -= 5.0 # 아침부터 매운건 감점
        
    elif 11 <= current_hour < 14: # 점심 (든든하게)
        df.loc[df['주재료'].isin(['밥', '면']), 'score'] += 5.0
        
    elif 17 <= current_hour: # 저녁/밤 (맛있는 것)
        df.loc[df['주재료'] == '고기', 'score'] += 5.0
        df.loc[df['맵기'] == '매운 맛', 'score'] += 3.0
    
    # 4. 랜덤 노이즈 추가 (Tie-Breaking)
    # 점수가 같아도 매번 미세하게 순위가 바뀌도록 0~3점 사이의 난수 추가
    df['score'] += df.apply(lambda x: random.uniform(0, 3.0), axis=1)
    
    # 5. 최종 순위 산정
    top_candidates = df.sort_values(by='score', ascending=False).head(15)
    
    # 최상위권 메뉴 선정 (1등)
    final_menu = top_candidates.iloc[0]['메뉴명']
    
    # 유사 메뉴 선정 (1등과 다른 것 중 상위 2개)
    others_pool = top_candidates[top_candidates['메뉴명'] != final_menu]
    if len(others_pool) >= 2:
        similar_menus = others_pool.head(2)['메뉴명'].tolist()
    else:
        similar_menus = others_pool['메뉴명'].tolist()
        
    return final_menu, similar_menus

# 시간 타이틀
def get_time_title():
    h = (datetime.utcnow() + timedelta(hours=9)).hour
    if 5 <= h < 11: return "☀️ 아메추"
    elif 11 <= h < 17: return "🕛 점메추"
    else: return "🌙 저메추"

# ==========================================
# 5. UI 메인
# ==========================================
if 'mode' not in st.session_state: st.session_state.mode = 'logic'
if 'choices' not in st.session_state: st.session_state.choices = {'step1': None, 'step2': None, 'step3': None, 'step4': None}
if 'slot_result' not in st.session_state: st.session_state.slot_result = "777"

def set_choice(step, value):
    st.session_state.choices[step] = value

st.title(get_time_title())

col1, col2 = st.columns(2)
with col1:
    btn_type = "primary" if st.session_state.mode == 'logic' else "secondary"
    if st.button("🚀 스스로 선택", key="tab_logic", type=btn_type):
        st.session_state.mode = 'logic'; st.rerun()
with col2:
    btn_type = "primary" if st.session_state.mode == 'random' else "secondary"
    if st.button("🎰 랜덤 룰렛", key="tab_random", type=btn_type):
        st.session_state.mode = 'random'; st.rerun()

st.write("")

# ----------------------------
# MODE 1: 스스로 선택 (고급 알고리즘 적용)
# ----------------------------
if st.session_state.mode == 'logic':
    st.subheader("취향을 선택해주세요")
    
    c1, c2 = st.columns(2)
    cur = st.session_state.choices['step1']
    if c1.button("매운 맛", type="primary" if cur=="매운 맛" else "secondary"): set_choice('step1', "매운 맛"); st.rerun()
    if c2.button("순한 맛", type="primary" if cur=="순한 맛" else "secondary"): set_choice('step1', "순한 맛"); st.rerun()
    
    if st.session_state.choices['step1']:
        st.write("")
        c1, c2 = st.columns(2)
        cur = st.session_state.choices['step2']
        if c1.button("뜨거운 것", type="primary" if cur=="뜨거운 것" else "secondary"): set_choice('step2', "뜨거운 것"); st.rerun()
        if c2.button("차가운 것", type="primary" if cur=="차가운 것" else "secondary"): set_choice('step2', "차가운 것"); st.rerun()

    if st.session_state.choices['step2']:
        st.write("")
        st.subheader("종류")
        cols = st.columns(3)
        opts = ["한식", "중식", "일식", "양식", "아시안"]
        cur = st.session_state.choices['step3']
        for i, opt in enumerate(opts):
            with cols[i%3]:
                if st.button(opt, key=f"l_{opt}", type="primary" if cur==opt else "secondary"): set_choice('step3', opt); st.rerun()

    if st.session_state.choices['step3']:
        st.write("")
        st.subheader("주재료")
        cols = st.columns(3)
        opts = ["밥", "면", "고기", "빵", "기타"]
        cur = st.session_state.choices['step4']
        for i, opt in enumerate(opts):
            with cols[i%3]:
                if st.button(opt, key=f"l_{opt}", type="primary" if cur==opt else "secondary"): set_choice('step4', opt); st.rerun()

    if st.session_state.choices['step4']:
        st.markdown("---")
        
        # 🔥 고급 알고리즘 실행
        final, similar = recommend_food(df_logic, st.session_state.choices)
        
        st.markdown(f"""
        <div class="result-card">
            <p style="color:gray; font-size:14px; margin-bottom:5px;">분석 결과</p>
            <h1 style="margin:10px 0; color:#FF4B4B; font-size:3em;">{final}</h1>
            <p style="opacity:0.7;">{st.session_state.choices['step1']} · {st.session_state.choices['step2']} · {st.session_state.choices['step3']}</p>
            <p style="background:rgba(128,128,128,0.1); padding:10px; border-radius:10px; margin-top:15px; color:var(--text-color);">
                🤔 <b>다른 추천:</b> {', '.join(similar)}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        col1, col2 = st.columns(2)
        col1.link_button("N 네이버지도", f"https://map.naver.com/v5/search/내주변 {final}", use_container_width=True)
        col2.link_button("K 카카오맵", f"https://map.kakao.com/link/search/내주변 {final}", use_container_width=True)
        
        st.write("")
        if st.button("🔄 다시 하기"): 
            st.session_state.choices = {'step1':None,'step2':None,'step3':None,'step4':None}
            st.rerun()

# ----------------------------
# MODE 2: 랜덤 슬롯머신
# ----------------------------
else:
    st.subheader("🎰 운명의 룰렛")
    
    # 레이아웃 나누기
    c_screen, c_button = st.columns([6.5, 3.5])
    slot_placeholder = c_screen.empty()
    
    # [상태 1] 아직 안 돌렸을 때 (초기화면 '777')
    if st.session_state.slot_result == "777":
        slot_placeholder.markdown("""
        <div class="slot-machine-container">
            <div class="slot-viewport"><div class="slot-text">🎰 777 🎰</div></div>
        </div>
        """, unsafe_allow_html=True)

        # ----------------------------
# MODE 2: 랜덤 슬롯머신
# ----------------------------
else:
    st.subheader("🎰 운명의 룰렛")
    
    # 레이아웃: [슬롯화면 (6.5)] [레버 (3.5)]
    c_screen, c_button = st.columns([6.5, 3.5])
    slot_placeholder = c_screen.empty()
    
    # 1. 화면 (정지 상태)
    if st.session_state.slot_result == "777":
        slot_placeholder.markdown("""
        <div class="slot-machine-container">
            <div class="slot-viewport">
                <div class="slot-text" style="animation: none;">🎰 777 🎰</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # 결과 화면
        final = st.session_state.slot_result
        slot_placeholder.markdown(f"""
        <div class="slot-machine-container" style="border-color:#FF4B4B;">
            <div class="slot-viewport">
                <div class="slot-text" style="color:#FF4B4B; animation: none;">🎉 {final} 🎉</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 2. 버튼 및 애니메이션 로직 (수정된 부분)
    with c_button:
        st.markdown('<div class="arcade-box">', unsafe_allow_html=True)
        
        # 버튼 클릭
        if st.button("GO!", key="arcade_btn"):
            candidates = df_logic['메뉴명'].tolist()
            
            # 속도 조절
            delays = [0.05]*10 + [0.1]*5 + [0.2]*3 + [0.4]*2
            
            for d in delays:
                temp = random.choice(candidates)
                
                # [핵심] 랜덤 ID를 생성해 애니메이션 강제 실행
                random_id = random.randint(0, 1000000)
                
                # 'slot-drop' 클래스로 낙하 효과 적용
                slot_placeholder.markdown(f"""
                <div class="slot-machine-container">
                    <div class="slot-viewport">
                        <div id="slot-{random_id}" class="slot-text slot-drop" style="color:#555;">
                            {temp}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                time.sleep(d)
            
            # 최종 결과 저장
            st.session_state.slot_result = random.choice(candidates)
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

    # 결과 처리 (지도 버튼 등)
    if st.session_state.slot_result != "777":
        st.balloons()
        final = st.session_state.slot_result
        st.write("")
        col1, col2 = st.columns(2)
        col1.link_button("N 네이버지도", f"https://map.naver.com/v5/search/내주변 {final}", use_container_width=True)
        col2.link_button("K 카카오맵", f"https://map.kakao.com/link/search/내주변 {final}", use_container_width=True)
        st.write("")
        if st.button("🔄 리셋", type="secondary"):
            st.session_state.slot_result = "777"
            st.rerun()
