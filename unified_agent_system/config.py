import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    # API Keys
    openai_api_key: str
    anthropic_api_key: str
    cohere_api_key: str
    gemini_api_key: str
    
    # Database & Cache
    database_url: str
    redis_url: str
    read_replica_url: str = None
    
    # LLM Configuration
    embedding_model: str = "text-embedding-3-large"
    default_llm_provider: str = "openai"
    llm_timeout: int = 30
    llm_max_retries: int = 3
    
    # Assessment Configuration
    max_concurrent_assessments: int = 500
    confidence_threshold: float = 0.75
    recursive_max_depth: int = 3
    clinical_models_enabled: bool = True
    
    # Authentication & Security
    jwt_secret_key: str
    token_expiry_minutes: int = 60
    refresh_token_expiry_days: int = 30
    
    # Scalability
    db_min_connections: int = 20
    db_max_connections: int = 100
    redis_max_connections: int = 200
    requests_per_minute_per_user: int = 60
    max_websocket_connections: int = 5000
    
    # System
    environment: str = "development"
    log_level: str = "INFO"
    debug: bool = False

config = Config(
    # API Keys
    openai_api_key=os.getenv("OPENAI_API_KEY", ""),
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
    cohere_api_key=os.getenv("COHERE_API_KEY", ""),
    gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
    
    # Database & Cache
    database_url=os.getenv("DATABASE_URL", "postgresql://localhost:5432/dpnr"),
    redis_url=os.getenv("REDIS_URL", "redis://localhost:6379"),
    read_replica_url=os.getenv("READ_REPLICA_URL"),
    
    # LLM Configuration
    default_llm_provider=os.getenv("DEFAULT_LLM_PROVIDER", "openai"),
    llm_timeout=int(os.getenv("LLM_TIMEOUT", "30")),
    clinical_models_enabled=os.getenv("CLINICAL_MODELS_ENABLED", "true").lower() == "true",
    
    # Authentication & Security
    jwt_secret_key=os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production"),
    token_expiry_minutes=int(os.getenv("TOKEN_EXPIRY_MINUTES", "60")),
    refresh_token_expiry_days=int(os.getenv("REFRESH_TOKEN_EXPIRY_DAYS", "30")),
    
    # Scalability
    max_concurrent_assessments=int(os.getenv("MAX_CONCURRENT_ASSESSMENTS", "500")),
    db_max_connections=int(os.getenv("DB_MAX_CONNECTIONS", "100")),
    redis_max_connections=int(os.getenv("REDIS_MAX_CONNECTIONS", "200")),
    requests_per_minute_per_user=int(os.getenv("REQUESTS_PER_MINUTE_PER_USER", "60")),
    max_websocket_connections=int(os.getenv("MAX_WEBSOCKET_CONNECTIONS", "5000")),
    
    # System
    environment=os.getenv("ENVIRONMENT", "development"),
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    debug=os.getenv("DEBUG", "false").lower() == "true"
)
