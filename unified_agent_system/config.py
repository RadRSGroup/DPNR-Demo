from dataclasses import dataclass

@dataclass
class Config:
    openai_api_key: str
    cohere_api_key: str
    database_url: str
    redis_url: str
    embedding_model: str = "text-embedding-3-large"
    max_concurrent_assessments: int = 100
    confidence_threshold: float = 0.75
    recursive_max_depth: int = 3

config = Config(
    openai_api_key="your-openai-key",
    cohere_api_key="your-cohere-key", 
    database_url="postgresql://user:pass@localhost/psych_db",
    redis_url="redis://localhost:6379"
)
