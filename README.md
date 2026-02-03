# 🏥 실비-헬퍼 (Silbi-Helper): AI 실손 보험금 분석 비서

> **Upstage AI**를 활용하여 복잡한 병원 영수증을 분석하고 보험 약관에 기반한 환급 가이드를 제공하는 AI 에이전트입니다.

---
## 🔴 구조
```
silbi-helper-agent
├── app
│   ├── main.py              
│   ├── upstage_utils.py    
│   └── prompt_template.py   
├── data
│   ├── image.png            # 시험용 이미지
│   └── policy.txt           # 보험 약관 데이터 
├── .env                     # API 키
├── .gitignore   
├── README.md               
└── requirements.txt         
```

## ✨ 주요 기능
- **문서 레이아웃 분석**: Upstage Document Parse를 통해 복잡한 영수증 표 구조를 마크다운으로 완벽 변환
- **지능형 약관 검색 (RAG)**: 사용자의 영수증 항목과 가장 관련 있는 보험 약관 조항을 벡터 DB에서 자동 검색
- **맞춤형 분석 리포트**: Solar-Pro LLM을 활용하여 환급 예상 금액 및 청구 시 주의사항 안내

## 🛠 핵심 기술 (Core Technology)
- **LLM**: Upstage `solar-pro`
- **Document Parse**: Upstage `document-parse`
- **Embeddings**: Upstage `solar-embedding-1-large`
- **Vector DB**: FAISS
- **Framework**: LangChain, Streamlit

## 📊 Benchmark
오픈소스 OCR(EasyOCR)과 Upstage Layout Analysis의 성능을 비교한 결과입니다.
- **오픈소스**: 텍스트가 줄글로 나열되어 금액 매칭이 불가능함.
> 국민건강보협 요양급여의 기군데 관한 규칙 [별지 제6호서식] <개절 201421) 1외래 [비입원 ( 1퇴원[ ]중간) 진료비 계산서 영수증 환지등록번호 환자 성명 진료기간 야간(공휴일)진료 야간 공류 부터 까지 진료과국 질병aDRG)번호 방실 환자구분 영수공번호(연입-일런번 급여 비금여 금액산정내용 함목 인부 본인부담 신턱 신택진료료 진료비 승액 본인부담금 공단부담급 본인부담 진료료 이외
- **Upstage**: 표 구조를 완벽히 유지하여 AI가 정확한 수치를 계산할 수 있음.
> | ■ 국민건강보험 요양급여의 기준에 관한 규칙 [별지 제6호서식] <개정 2014.9.1.> [ ]외래 [✓]입원 ([ ]퇴원[ ]중간) 진료비 계산서 · 영수증 | ■ 국민건강보험 요양급여의 기준에 관한 규칙 [별지 제6호서식] <개정 2014.9.1.> [ ]외래 [✓]입원 ([ ]퇴원[ ]중간) 진료비 계산서 · 영수증 | ■ 국민건강보험 요양급여의 기준에 관한 규칙 [별지 제6호서식] <개정 2014.9.1.> [ ]외래 [✓]입원 ([ ]퇴원[ ]중간) 진료비 계산서 · 영수증 | ■ 국민건강보험 요양급여의 기준에 관한 규칙 [별지 제6호서식] <개정 2014.9.1.> [ ]외래 [✓]입원 ([ ]퇴원[ ]중간) 진료비 계산서 · 영수증 |
| --- | --- | --- | --- |
| 환자등록번호 | 환자 성명 | 진료기간 | 야간(공휴일)진료 |
|  |  | .부터 .까지 | [ ] 야간 [ ] 공휴 일 |
| 진료과목 | 질병군(DRG)번호 | 병실 | 환자구분 | 영수증번호(연월-일련번 호) |
| --- | --- | --- | --- | --- |
| 항목 | 항목 | 항목 | 급여 | 급여 | 급여 | 비급여 | 비급여 | 금액산정내용 | 금액산정내용 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 항목 | 항목 | 항목 | 일부 본인부담 | 일부 본인부담 | 전액 본인부담 | 선택 진료료 | 선택진료료 이외 | ⑦ 진료비 총액 (1+2+3+4+5) | 5,960,000 |


## 🚀 시작하기

### 1. 환경 변수 설정
프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 발급받은 API Key를 입력합니다.
`UPSTAGE_API_KEY=your_api_key_here`

### 2. 라이브러리 설치
```bash
pip install -r requirements.txt
```

### 3. 실행
```bash
streamlit run app/main.py
```

## 🛠 트러블슈팅: 라이브러리 임포트 오류 해결
최신 langchain-upstage 라이브러리 업데이트에 따라 UpstageLayoutAnalysisLoader 대신 **UpstageDocumentParseLoader**를 사용하여 임포트 에러를 해결하고 파싱 안정성을 확보했습니다.
```python
from langchain_upstage.document_parse import UpstageDocumentParseLoader

loader = UpstageDocumentParseLoader(file_path, split="element")
```

---
Powered by Upstage
