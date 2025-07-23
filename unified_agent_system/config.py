import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    openai_api_key: str
    cohere_api_key: str
    gemini_api_key: str
    database_url: str
    redis_url: str
    embedding_model: str = "text-embedding-3-large"
    max_concurrent_assessments: int = 100
    confidence_threshold: float = 0.75
    recursive_max_depth: int = 3
    environment: str = "development"
    log_level: str = "INFO"

config = Config(
    openai_api_key=os.getenv("OPENAI_API_KEY", ""),
    cohere_api_key=os.getenv("COHERE_API_KEY", ""),
    gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
    database_url=os.getenv("DATABASE_URL", "sqlite:///./dpnr.db"),
    redis_url=os.getenv("REDIS_URL", "redis://localhost:6379"),
    environment=os.getenv("ENVIRONMENT", "development"),
    log_level=os.getenv("LOG_LEVEL", "INFO")
)
