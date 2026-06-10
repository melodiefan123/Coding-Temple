import os
# Create a config.py with a Settings class that reads from environment variables with sensible defaults
# Include at least these settings: OLLAMA_URL, MODEL_NAME, CHROMA_PATH, MAX_RESULTS, CONFIDENCE_THRESHOLD, DEBUG
# Create a .env file with Docker Compose values
# Create a .env.example (without secrets) for documentation
# Add .env to both .gitignore and .dockerignore
# Update your docker-compose.yml to use env_file: .env
# Verify: change MODEL_NAME in .env, restart, and confirm the change takes effect

class Settings:
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama3.2:8b")
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