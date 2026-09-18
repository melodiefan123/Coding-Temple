import os
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

VECTOR_DB_DIR = Path("vector_db")
VECTOR_DB_DIR.mkdir(exist_ok=True)

def get_user_vectorstore(user_id: int) -> Chroma:
    """Returns or creates a user-specific Chroma vector collection."""
    embeddings = OpenAIEmbeddings()  # Initialized on demand
    user_db_path = str(VECTOR_DB_DIR / f"user_{user_id}")
    return Chroma(
        collection_name=f"user_{user_id}_docs",
        embedding_function=embeddings,
        persist_directory=user_db_path,
    )

def index_document(file_path: Path, user_id: int) -> int:
    """Loads a document, chunks it, and indexes it into ChromaDB."""
    ext = file_path.suffix.lower()
    
    loader = PyPDFLoader(str(file_path)) if ext == ".pdf" else TextLoader(str(file_path))
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)
    
    vectorstore = get_user_vectorstore(user_id)
    vectorstore.add_documents(splits)
    return len(splits)

def query_rag(question: str, user_id: int) -> str:
    """Queries user vector store and answers with context."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # Initialized on demand
    vectorstore = get_user_vectorstore(user_id)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI assistant for financial tracking, receipts, and invoices.\n"
                   "Use the following retrieved context to answer the question.\n"
                   "If context is missing or insufficient, state that clearly.\n\n"
                   "Context:\n{context}"),
        ("human", "{question}"),
    ])

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain.invoke(question)