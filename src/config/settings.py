"""Application settings and configuration"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Anthropic Claude API
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Pinecone Vector Database
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "")
    pinecone_environment: str = os.getenv("PINECONE_ENVIRONMENT", "us-east-1-aws")
    pinecone_index_name: str = os.getenv("PINECONE_INDEX_NAME", "college-major-rag")
    
    # FastAPI Settings
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", 8000))
    
    # Application Settings
    app_name: str = "College Major RAG System"
    app_version: str = "0.1.0"
    embedding_model: str = "all-MiniLM-L6-v2"  # Local sentence-transformers model (no API key needed)
    max_tokens: int = 2048
    temperature: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
