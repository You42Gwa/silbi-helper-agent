import streamlit as st
import os
from upstage_utils import get_parsed_receipt, create_vector_db, analyze_with_rag
from easyocr_utils import get_easyocr_result

# 페이지 설정
st.set_page_config(page_title="실비-헬퍼 AI", layout="wide", page_icon="🏥")

st.title("🏥 실비-헬퍼: AI 실손 보험금 분석 비서")
st.markdown("""
Upstage AI를 활용하여 복잡한 대학병원 영수증을 분석하고, 
보험 약관에 기반한 환급 가이드를 제공합니다.
""")

# DB 생성
if "vector_db" not in st.session_state:
    with st.spinner("보험 약관 데이터베이스를 구축 중입니다..."):
        # data/policy.txt 파일 존재해야함
        if os.path.exists("data/policy.txt"):
            st.session_state.vector_db = create_vector_db("data/policy.txt")
            st.success("약관 DB 구축 완료!")
        else:
            st.error("data/policy.txt 파일을 먼저 생성해주세요.")

# 사이드바: 파일 업로드
st.sidebar.header("📁 서류 업로드")
uploaded_file = st.sidebar.file_uploader("병원 영수증 이미지를 업로드하세요.", type=["jpg", "png", "jpeg", "pdf"])

# 메인 화면 구성
col1, col2 = st.columns(2)

if uploaded_file is not None:
    # 이미지 미리보기
    with col1:
        st.subheader("📸 업로드된 서류")
        st.image(uploaded_file, use_container_width=True)
        
    with col2:
        st.subheader("🔍 AI 분석 결과")
        
        # 임시 파일 저장
        temp_path = f"data/temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 분석 실행
        with st.status("AI 에이전트가 서류를 분석 중입니다...", expanded=True) as status:
            st.write("1. Upstage Document Parse로 표 구조 분석 중...")
            parsed_text = get_parsed_receipt(temp_path)
            
            st.write("2. RAG 기반 관련 약관 검색 중...")
            # 분석 및 결과 생성
            final_report = analyze_with_rag(parsed_text, st.session_state.vector_db)
            
            status.update(label="분석 완료!", state="complete", expanded=False)
        
        # 결과 탭 구성
        tab1, tab2, tab3 = st.tabs(["💡 AI 해석 리포트", "📄 파싱 원본(Markdown)", "📄 EasyOCR 결과"])
        
        with tab1:
            st.markdown(final_report)
            
        with tab2:
            st.code(parsed_text, language="markdown")
            
        with tab3:
            st.code(get_easyocr_result(temp_path), language="markdown")
            
    # 분석 후 임시 파일 삭제
    os.remove(temp_path)

else:
    st.info("왼쪽 사이드바에서 분석할 영수증 파일을 업로드해주세요.")

st.divider()
st.caption("Solar LLM, Document Parse, Embeddings를 활용하였습니다.")