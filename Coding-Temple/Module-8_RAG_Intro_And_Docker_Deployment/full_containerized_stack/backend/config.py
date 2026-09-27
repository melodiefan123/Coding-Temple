import os

class Settings:
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://ollama:11434")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama3.2:1b")
    CHROMA_PATH: str = os.getenv("CHROMA_PATH", "/app/chroma_data")
    MAX_RESULTS: int = int(os.getenv("MAX_RESULTS", "5"))
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()

if settings.DEBUG:
    print("=== Configuration ===")
    print(f"  Ollama URL: {settings.OLLAMA_URL}")
    print(f"  Model: {settings.MODEL_NAME}")
    print(f"  ChromaDB: {settings.CHROMA_PATH}")
    print(f"  Max Results: {settings.MAX_RESULTS}")
    print(f"  Threshold: {settings.CONFIDENCE_THRESHOLD}")
    print(f"  Debug: {settings.DEBUG}")