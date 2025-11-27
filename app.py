import streamlit as st
import pandas as pd
import random

# 페이지 설정 (제일 먼저 와야 함)
st.set_page_config(page_title="점메추 AI Pro", layout="centered")

# ==========================================
# ⚡ 캐싱 적용: 데이터를 한 번만 로드하고 기억함
# ==========================================
@st.cache_data
def load_menu_data():
    # 1. 방대한 음식 이름 리스트 (400개+)
    raw_menu_list = [
        # [한식]
        "김치찌개", "참치김치찌개", "돼지김치찌개", "꽁치김치찌개", "스팸김치찌개",
        "된장찌개", "차돌된장찌개", "해물된장찌개", "우렁된장찌개", "강된장",
        "순두부찌개", "해물순두부", "들깨순두부", "햄치즈순두부", "쫄면순두부",
        "부대찌개", "청국장", "비지찌개", "동태찌개", "알탕", "대구탕", "꽃게탕", "매운탕",
        "갈비탕", "설렁탕", "곰탕", "나주곰탕", "사골국", "도가니탕", "꼬리곰탕",
        "삼계탕", "반계탕", "닭곰탕", "닭개장", "육개장", "추어탕", "장어탕",
        "콩나물국밥", "순대국", "돼지국밥", "소머리국밥", "선지해장국", "뼈해장국", "황태해장국", "올갱이국",
        "비빔밥", "돌솥비빔밥", "육회비빔밥", "꼬막비빔밥", "산채비빔밥", "멍게비빔밥",
        "김치볶음밥", "새우볶음밥", "참치마요덮밥", "스팸마요덮밥", "치킨마요덮밥", "제육덮밥", "오징어덮밥", "낙지덮밥", "쭈꾸미덮밥",
        "불고기백반", "생선구이백반", "게장백반", "보리밥", "쌈밥", "묵밥", "국밥", "미역국", "무국",
        "삼겹살", "목살", "항정살", "돼지갈비", "갈매기살", "냉동삼겹살",
        "소갈비", "차돌박이", "등심", "안심", "육회", "육사시미",
        "닭갈비", "숯불닭갈비", "찜닭", "안동찜닭", "로제찜닭", "닭볶음탕", "닭한마리",
        "제육볶음", "두부김치", "오징어볶음", "낙지볶음", "쭈꾸미볶음", "코다리조림", "갈치조림", "고등어조림",
        "보쌈", "마늘보쌈", "족발", "불족발", "냉채족발",
        "곱창", "대창", "막창", "양대창", "곱창전골",
        "감자탕", "등뼈찜", "아구찜", "해물찜", "꽃게찜",
        "파전", "김치전", "해물파전", "감자전", "육전", "모둠전", "빈대떡",
        "떡볶이", "라볶이", "즉석떡볶이", "로제떡볶이", "짜장떡볶이", "궁중떡볶이", "기름떡볶이",
        "튀김", "순대", "김밥", "참치김밥", "치즈김밥", "돈가스김밥", "충무김밥",
        "라면", "치즈라면", "만두라면", "해물라면", "틈새라면",
        "칼국수", "바지락칼국수", "닭칼국수", "장칼국수", "비빔칼국수", "들깨칼국수",
        "수제비", "들깨수제비", "잔치국수", "비빔국수", "열무국수", "콩국수",
        "냉면", "물냉면", "비빔냉면", "회냉면", "평양냉면", "함흥냉면",
        "막국수", "쫄면", "만두국", "떡만두국", "떡국", "비빔만두",
        
        # [중식]
        "짜장면", "간짜장", "삼선짜장", "쟁반짜장", "유니짜장", "사천짜장",
        "짬뽕", "삼선짬뽕", "백짬뽕", "고기짬뽕", "차돌짬뽕", "굴짬뽕", "홍합짬뽕", "볶음짬뽕", "냉짬뽕",
        "볶음밥", "새우볶음밥", "삼선볶음밥", "잡채밥", "마파두부밥", "유산슬밥", "잡탕밥", "고추잡채밥",
        "탕수육", "찹쌀탕수육", "사천탕수육", "꿔바로우",
        "깐풍기", "유린기", "라조기", "난자완스", "팔보채", "양장피", "유산슬", "고추잡채",
        "군만두", "물만두", "꽃빵", "멘보샤",
        "마라탕", "마라샹궈", "훠궈", "양꼬치", "양갈비", "우육면", "탄탄면", "동파육", "크림새우", "칠리새우",
        
        # [일식]
        "초밥", "모듬초밥", "연어초밥", "광어초밥", "새우초밥", "참치초밥", "소고기초밥", "유부초밥",
        "회덮밥", "사케동", "규동", "가츠동", "에비동", "오야코동", "부타동", "차슈동", "장어덮밥", "텐동", "카이센동",
        "우동", "튀김우동", "유부우동", "김치우동", "냉우동", "붓카케우동", "카레우동",
        "소바", "냉모밀", "판모밀", "온모밀", "마제소바",
        "라멘", "돈코츠라멘", "미소라멘", "소유라멘", "시오라멘", "카라이라멘", "탄탄멘",
        "돈가스", "등심돈가스", "안심돈가스", "치즈돈가스", "고구마치즈돈가스", "카레돈가스", "돈가스나베", "김치나베",
        "카레라이스", "하이라이스", "오꼬노미야끼", "타코야끼", "야끼소바", "스키야키", "샤브샤브",
        
        # [양식]
        "토마토파스타", "크림파스타", "로제파스타", "알리오올리오", "봉골레", "까르보나라", "볼로네제", "빠네파스타", "명란파스타",
        "라자냐", "뇨끼", "리조또", "크림리조또", "토마토리조또", "오징어먹물리조또",
        "피자", "고르곤졸라", "페퍼로니피자", "포테이토피자", "불고기피자", "시카고피자", "하와이안피자",
        "스테이크", "티본스테이크", "찹스테이크", "함박스테이크", "돈마호크", "폭립",
        "햄버거", "치즈버거", "수제버거", "치킨버거", "새우버거",
        "샌드위치", "클럽샌드위치", "서브웨이", "에그드랍", "이삭토스트", "프렌치토스트", "베이글", "파니니", "핫도그",
        "샐러드", "닭가슴살샐러드", "리코타치즈샐러드", "연어샐러드", "콥샐러드", "포케",
        "스프", "감바스", "에그인헬",
        
        # [아시안/기타]
        "쌀국수", "매운쌀국수", "분짜", "반미", "월남쌈", "짜조",
        "팟타이", "나시고랭", "미시고랭", "푸팟퐁커리", "똠양꿍",
        "타코", "부리또", "퀘사디아", "화이타", "케밥",
        "마라탕", "인도커리", "난", "탄두리치킨"
    ]

    # 2. 분석 로직 (내부 함수)
    def auto_tagging(menu):
        spicy, temp, kind, main = "순한 맛", "뜨거운 것", "한식", "기타"
        
        # 맵기
        spicy_keywords = ["김치", "매운", "육개장", "짬뽕", "마라", "떡볶이", "비빔", "양념", "낙지", "쭈꾸미", "닭갈비", "얼큰", "핫", "사천", "불족발", "카라이", "탄탄", "똠양", "감자탕", "해물탕", "매운탕"]
        if any(k in menu for k in spicy_keywords): spicy = "매운 맛"
        
        # 온도
        cold_keywords = ["냉면", "소바", "모밀", "초밥", "회", "냉", "샌드위치", "샐러드", "육회", "김밥", "빙수", "묵밥", "포케", "월남쌈"]
        if any(k in menu for k in cold_keywords): temp = "차가운 것"
        
        # 종류
        chinese = ["짜장", "짬뽕", "탕수육", "마라", "꿔바로우", "유린기", "동파육", "우육", "탄탄", "양꼬치", "훠궈", "멘보샤", "깐풍", "라조기", "난자완스", "팔보채"]
        japanese = ["초밥", "우동", "소바", "라멘", "카츠", "가츠", "규동", "사케동", "오꼬노미", "스시", "나베", "텐동", "부타동", "야끼", "스키야키", "샤브샤브"]
        western = ["파스타", "피자", "버거", "스테이크", "샐러드", "샌드위치", "리조또", "스프", "라자냐", "뇨끼", "토스트", "베이글", "감바스", "파니니"]
        asian = ["쌀국수", "팟타이", "나시고랭", "미시고랭", "분짜", "타코", "부리또", "커리", "반미", "퀘사디아", "케밥", "화이타", "똠양", "난"]
        
        if any(k in menu for k in chinese): kind = "중식"
        elif any(k in menu for k in japanese): kind = "일식"
        elif any(k in menu for k in western): kind = "양식"
        elif any(k in menu for k in asian): kind = "아시안"
        
        # 주재료
        rice = ["밥", "죽", "리조또", "동", "초밥", "필라프", "포케"]
        noodle = ["면", "국수", "우동", "소바", "파스타", "라멘", "짜장", "짬뽕", "팟타이", "잡채"]
        meat = ["고기", "스테이크", "삼겹살", "갈비", "제육", "보쌈", "족발", "탕수육", "돈가스", "치킨", "육회", "찜닭", "곱창", "대창"]
        bread = ["빵", "버거", "샌드위치", "토스트", "피자", "베이글", "핫도그"]
        
        if any(k in menu for k in rice): main = "밥"
        elif any(k in menu for k in noodle): main = "면"
        elif any(k in menu for k in meat): main = "고기"
        elif any(k in menu for k in bread): main = "빵"
            
        return {"메뉴명": menu, "맵기": spicy, "온도": temp, "종류": kind, "주재료": main}

    # 데이터 생성
    return pd.DataFrame([auto_tagging(m) for m in raw_menu_list])

# 🚀 여기서 한 번만 실행됨!
df_logic = load_menu_data()

# ==========================================
# 3. 스타일 및 UI
# ==========================================
st.markdown("""
<style>
    :root { --primary: #FF4B4B; }
    .stButton > button {
        width: 100%; height: 65px; border-radius: 12px; font-size: 19px !important; font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: all 0.2s;
    }
    .stButton > button:hover { transform: translateY(-2px); }
    .result-card {
        border: 3px solid var(--primary); border-radius: 20px;
        padding: 30px; text-align: center; background-color: #fff;
        margin-top: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .menu-badge {
        background-color: #f0f2f6; padding: 5px 12px; border-radius: 15px;
        font-size: 0.9em; margin: 3px; display: inline-block; font-weight: 500;
        border: 1px solid #ddd;
    }
    a { text-decoration: none; color: #FF4B4B; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 4. 상태 관리
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

st.title("🚀 점메추 AI Pro")
st.caption(f"⚡ 캐싱 적용 완료: {len(df_logic)}개의 메뉴가 준비되었습니다.")

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
    
    # 조건에 맞는 메뉴 필터링
    result_df = df_logic[
        (df_logic['맵기']==c1) & 
        (df_logic['온도']==c2) & 
        (df_logic['종류']==c3) & 
        (df_logic['주재료']==c4)
    ]
    
    if not result_df.empty:
        # 랜덤 하나 추천
        pick = result_df.sample(1).iloc[0]
        final_menu = pick['메뉴명']
        
        # 네이버 지도 검색 링크
        search_url = f"https://map.naver.com/v5/search/근처 {final_menu}"
        
        st.markdown(f"""
        <div class="result-card">
            <h3 style="color:#888;">AI 분석 결과</h3>
            <h1 style="color:#FF4B4B; font-size:3.5rem; margin:15px 0;">{final_menu}</h1>
            <div style="margin-bottom:20px;">
                <span class="menu-badge">{pick['종류']}</span>
                <span class="menu-badge">{pick['맵기']}</span>
                <span class="menu-badge">{pick['온도']}</span>
                <span class="menu-badge">{pick['주재료']}</span>
            </div>
            <p style="font-size:1.2rem;"><a href="{search_url}" target="_blank">🗺️ 근처 '{final_menu}' 맛집 찾기 (Click)</a></p>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
        
        # 다른 후보 (최대 5개까지)
        others = result_df['메뉴명'].tolist()
        if len(others) > 1:
            others = [x for x in others if x != final_menu]
            random.shuffle(others)
            others_txt = ", ".join(others[:5])
            if len(others) > 5: others_txt += " 등..."
            st.info(f"💡 그 외 추천: {others_txt}")
            
    else:
        st.warning("이런! 조건이 너무 까다로워서 메뉴를 못 찾았어요. 😭")
        # 차선책 (종류만 같은 거)
        backup = df_logic[df_logic['종류']==c3].sample(1).iloc[0]['메뉴명']
        st.success(f"대신 **{backup}** 어떠세요?")

    st.write("")
    if st.button("🔄 처음부터 다시 하기"):
        for k in st.session_state.choices: st.session_state.choices[k] = None
        st.rerun()
