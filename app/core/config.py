from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    # API Configuration
    PROJECT_NAME: str = "DocMind"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str
    
    # External Services
    GOOGLE_API_KEY: str
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]
    
    # Document Processing
    UPLOAD_FOLDER: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Vector Store
    VECTOR_STORE_PATH: str = "./chroma_db"
    
    # Model Configuration
    TEMPERATURE: float = 0.3
    MAX_TOKENS: int = 2048
    TOP_K: int = 4
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()