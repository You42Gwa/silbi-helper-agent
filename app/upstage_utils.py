import os
from dotenv import load_dotenv
from langchain_upstage import UpstageEmbeddings, ChatUpstage
from langchain_upstage.document_parse import UpstageDocumentParseLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from prompt_template import INSURANCE_ANALYSIS_TEMPLATE

load_dotenv()

#영수증 파싱
def get_parsed_receipt(file_path):
    loader = UpstageDocumentParseLoader(
        file_path, 
        output_format="markdown",
        ocr="force"             
    )
    docs = loader.load()
    
    full_content = "\n\n".join([doc.page_content for doc in docs])
    
    return full_content

#약관 데이터 기반 Vector DB 생성
def create_vector_db(policy_text_path):
    with open(policy_text_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    #텍스트 분할
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.create_documents([content])
    
    #FAISS DB 구축
    embeddings = UpstageEmbeddings(model="solar-embedding-1-large")
    vector_db = FAISS.from_documents(splits, embeddings)
    return vector_db

#RAG 기반 분석 수행
def analyze_with_rag(receipt_text, vector_db):
    #Retrieval
    retriever = vector_db.as_retriever(search_kwargs={"k": 2})
    relevant_docs = retriever.invoke(receipt_text)
    context = "\n".join([doc.page_content for doc in relevant_docs])
    
    #Generation
    llm = ChatUpstage(model="solar-pro")
    
    prompt = ChatPromptTemplate.from_template(INSURANCE_ANALYSIS_TEMPLATE)
    
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"receipt_text": receipt_text, "context": context})