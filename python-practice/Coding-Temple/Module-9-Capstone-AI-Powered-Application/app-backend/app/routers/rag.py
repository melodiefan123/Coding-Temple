# app/routers/rag.py
import shutil
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from app.schemas.rag import QueryRequest, QueryResponse
from app.services.rag_service import index_document, query_rag
from app.utils.security import get_current_user

router = APIRouter(prefix="/rag", tags=["RAG & Search"])

TEMP_DIR = Path("uploads/rag_temp")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/index", status_code=status.HTTP_200_OK)
def index_file(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    """Uploads and indexes a receipt, invoice, or PDF into RAG."""
    file_ext = Path(file.filename).suffix
    temp_path = TEMP_DIR / f"{uuid.uuid4()}{file_ext}"
    
    with temp_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        chunks_indexed = index_document(temp_path, current_user.id)
        return {
            "message": "Document successfully indexed!",
            "filename": file.filename,
            "chunks": chunks_indexed
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process and index document: {str(e)}"
        )
    finally:
        if temp_path.exists():
            temp_path.unlink()  # Clean up temp file

@router.post("/query", response_model=QueryResponse)
def ask_question(
    payload: QueryRequest,
    current_user=Depends(get_current_user)
):
    """Queries the user's indexed financial data using RAG."""
    try:
        answer = query_rag(payload.question, current_user.id)
        return QueryResponse(question=payload.question, answer=answer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"RAG query failed: {str(e)}"
        )