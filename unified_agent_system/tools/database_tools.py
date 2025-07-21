
import asyncpg
import logging
import json
from typing import List, Dict, Any

# Import from the new unified architecture
from .config import config
# We will need to define or import these Pydantic models. For now, let's assume they exist.
# In a future step, we will create a central models.py file.
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Placeholder for the actual AssessmentResult model
class AssessmentResult(BaseModel):
    user_id: str
    assessment_type: str
    scores: List[Dict]
    overall_confidence: float
    embedding: List[float]
    requires_followup: bool
    followup_questions: List[str]
    processing_time_ms: int

class DatabaseManager:
    """
    Manages all interactions with the PostgreSQL database.
    """
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None
    
    async def initialize(self):
        """Creates the connection pool and ensures tables exist."""
        try:
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=5,
                max_size=20,
                command_timeout=30
            )
            await self._create_tables()
            logger.info("DatabaseManager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize DatabaseManager: {e}")
            self.pool = None
    
    async def is_connected(self) -> bool:
        """Health check method to verify database connectivity."""
        if not self.pool:
            return False
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("SELECT 1")
            return True
        except Exception:
            return False

    async def _create_tables(self):
        """Creates the necessary tables and extensions if they don't exist."""
        async with self.pool.acquire() as conn:
            await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id VARCHAR(50) UNIQUE NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    metadata JSONB DEFAULT '{}',
                    gdpr_consent BOOLEAN DEFAULT FALSE,
                    data_retention_end TIMESTAMPTZ
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS assessments (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id VARCHAR(50) NOT NULL, -- Removed REFERENCES for loose coupling
                    assessment_type VARCHAR(50) NOT NULL,
                    input_text TEXT NOT NULL,
                    scores JSONB NOT NULL,
                    confidence FLOAT NOT NULL,
                    embedding VECTOR(1536),
                    requires_followup BOOLEAN DEFAULT FALSE,
                    followup_questions JSONB DEFAULT '[]',
                    processing_time_ms INTEGER,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)
            
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_assessments_user_type ON assessments(user_id, assessment_type)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_assessments_embedding ON assessments USING hnsw (embedding vector_l2_ops)")
    
    async def save_assessment(self, result: AssessmentResult, embedding: List[float], input_text: str):
        """Saves a completed assessment result to the database."""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO assessments (
                    user_id, assessment_type, input_text, scores, confidence,
                    embedding, requires_followup, followup_questions, processing_time_ms
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            """, 
                result.user_id,
                result.assessment_type,
                input_text,
                json.dumps(result.scores),
                result.overall_confidence,
                embedding,
                result.requires_followup,
                json.dumps(result.followup_questions),
                result.processing_time_ms
            )
    
    async def find_similar_profiles(self, embedding: List[float], assessment_type: str, limit: int = 5):
        """Finds similar profiles using vector similarity search."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT user_id, scores, confidence,
                       1 - (embedding <=> $1) as similarity
                FROM assessments 
                WHERE assessment_type = $2
                ORDER BY embedding <=> $1 
                LIMIT $3
            """, embedding, assessment_type, limit)
            return [dict(row) for row in rows]
