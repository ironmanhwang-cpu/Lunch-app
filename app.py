import streamlit as st
import pandas as pd
import random

# 1. 페이지 설정 (가장 윗줄에 있어야 함)
st.set_page_config(page_title="점메추 GPS", layout="centered")

# 2. 데이터 로드 (캐싱 적용)
@st.cache_data
def load_data():
    # 메뉴 데이터 리스트
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
    
    # 자동 분류 로직
    def auto_tag(m):
        spicy, temp, kind, main = "순한 맛", "뜨거운 것", "한식", "기타"
        
        # 맵기
        if any(k in m for k in ["김치","매운","짬뽕","마라","떡볶이","육개장","비빔","낙지","얼큰","닭갈비","부대","탄탄","타코"]): spicy="매운 맛"
        # 온도
        if any(k in m for k in ["냉","소바","초밥","회","샐러드","샌드위치","김밥","빙수","쫄면","막국수","포케","월남쌈"]): temp="차가운 것"
        # 종류
        if any(k in m for k in ["짜장","짬뽕","탕수육","마라","꿔바로우","유린기","양꼬치","훠궈","깐풍"]): kind="중식"
        elif any(k in m for k in ["초밥","우동","소바","라멘","카츠","가츠","규동","텐동","오꼬노미","스시","샤브"]): kind="일식"
        elif any(k in m for k in ["파스타","피자","버거","스테이크","샐러드","샌드위치","리조또","스프","브런치"]): kind="양식"
        elif any(k in m for k in ["쌀국수","팟타이","나시고랭","분짜","타코","부리또","반미","커리"]): kind="아시안"
        # 주재료
        if any(k in m for k in ["밥","죽","리조또","동","초밥","필라프","포케","국밥","백반"]): main="밥"
        elif any(k in m for k in ["면","국수","우동","파스타","라멘","짜장","짬뽕","팟타이","잡채"]): main="면"
        elif any(k in m for k in ["고기","스테이크","삼겹살","갈비","제육","보쌈","족발","탕수육","돈가스","치킨","찜닭","곱창"]): main="고기"
        elif any(k in m for k in ["빵","버거","샌드위치","토스트","피자","베이글","타코"]): main="빵"
        
        return {"메뉴명":m, "맵기":spicy, "온도":temp, "종류":kind, "주재료":main}
    
    return pd.DataFrame([auto_tag(m) for m in raw_list])

df_logic = load_data()

# 3. 상태 관리
if 'choices' not in st.session_state:
    st.session_state.choices = {'step1': None, 'step2': None, 'step3': None, 'step4': None}

def set_choice(step, value):
    st.session_state.choices[step] = value

# 4. 메인 화면
st.title("📍 점메추 GPS")
st.write("내 주변 맛집을 바로 찾아드립니다.")
st.markdown("---")

# 단계별 선택 (안전한 UI 사용)
# Step 1
st.subheader("1. 맵기 선택")
c1, c2 = st.columns(2)
if c1.button("🌶️ 매운 맛", type="primary" if st.session_state.choices['step1']=="매운 맛" else "secondary"):
    set_choice('step1', "매운 맛")
    st.rerun()
if c2.button("😌 순한 맛", type="primary" if st.session_state.choices['step1']=="순한 맛" else "secondary"):
    set_choice('step1', "순한 맛")
    st.rerun()

# Step 2
if st.session_state.choices['step1']:
    st.write("")
    st.subheader("2. 온도 선택")
    c1, c2 = st.columns(2)
    if c1.button("🔥 뜨거운 것", type="primary" if st.session_state.choices['step2']=="뜨거운 것" else "secondary"):
        set_choice('step2', "뜨거운 것")
        st.rerun()
    if c2.button("❄️ 차가운 것", type="primary" if st.session_state.choices['step2']=="차가운 것" else "secondary"):
        set_choice('step2', "차가운 것")
        st.rerun()

# Step 3
if st.session_state.choices['step2']:
    st.write("")
    st.subheader("3. 종류 선택")
    col_list = st.columns(3)
    options = ["한식", "중식", "일식", "양식", "아시안"]
    for i, opt in enumerate(options):
        # 3열로 배치
        with col_list[i % 3]:
            if st.button(opt, key=f"s3_{opt}", type="primary" if st.session_state.choices['step3']==opt else "secondary"):
                set_choice('step3', opt)
                st.rerun()

# Step 4
if st.session_state.choices['step3']:
    st.write("")
    st.subheader("4. 재료 선택")
    col_list = st.columns(3)
    options = ["밥", "면", "고기", "빵", "기타"]
    for i, opt in enumerate(options):
        with col_list[i % 3]:
            if st.button(opt, key=f"s4_{opt}", type="primary" if st.session_state.choices['step4']==opt else "secondary"):
                set_choice('step4', opt)
                st.rerun()

# 최종 결과
if st.session_state.choices['step4']:
    st.markdown("---")
    
    # 선택값 가져오기
    c1 = st.session_state.choices['step1']
    c2 = st.session_state.choices['step2']
    c3 = st.session_state.choices['step3']
    c4 = st.session_state.choices['step4']
    
    # 필터링
    result_df = df_logic[
        (df_logic['맵기']==c1) & (df_logic['온도']==c2) & 
        (df_logic['종류']==c3) & (df_logic['주재료']==c4)
    ]
    
    if not result_df.empty:
        final_menu = result_df.sample(1).iloc[0]['메뉴명']
        
        # 디자인 박스 (안전한 HTML)
        st.markdown(f"""
        <div style="
            background-color: #f0f2f6; 
            padding: 20px; 
            border-radius: 15px; 
            border: 2px solid #ff4b4b;
            text-align: center;">
            <h3 style="margin:0; color:gray;">오늘의 메뉴</h3>
            <h1 style="margin:10px 0; color:#ff4b4b; font-size:3em;">{final_menu}</h1>
            <p>({c1}, {c2}, {c3}, {c4})</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.success("👇 아래 버튼을 누르면 내 주변 식당을 찾습니다!")
        
        # 지도 버튼 (스트림릿 네이티브 링크 버튼 사용 - 오류 없음)
        col1, col2 = st.columns(2)
        with col1:
            st.link_button(f"N 네이버지도 검색", f"https://map.naver.com/v5/search/내주변 {final_menu}", use_container_width=True)
        with col2:
            st.link_button(f"K 카카오맵 검색", f"https://map.kakao.com/link/search/내주변 {final_menu}", use_container_width=True)
            
    else:
        st.warning("조건에 맞는 메뉴가 없어요 😭")
        backup = df_logic[df_logic['종류']==c3].sample(1).iloc[0]['메뉴명']
        st.info(f"대신 **{backup}** 어때요?")
        st.link_button(f"N {backup} 맛집 찾기", f"https://map.naver.com/v5/search/내주변 {backup}", use_container_width=True)

    st.write("")
    if st.button("🔄 처음부터 다시 하기", type="secondary", use_container_width=True):
        for k in st.session_state.choices: st.session_state.choices[k] = None
        st.rerun()
