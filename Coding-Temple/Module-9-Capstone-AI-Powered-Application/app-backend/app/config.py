import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")  # Default value for development
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))