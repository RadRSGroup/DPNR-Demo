# FastAPI REST API Server for Psychological Assessment System
# Production-ready REST endpoints with comprehensive error handling

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import asyncio
import uvicorn
from typing import List, Optional, Dict, Any
import time
import logging
from contextlib import asynccontextmanager

# Import our core system
from psychological_assessment_system import (
    PsychologicalAssessmentSystem, 
    UserInput, 
    AssessmentResult, 
    AssessmentType,
    Config
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global system instance
system: Optional[PsychologicalAssessmentSystem] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global system
    config = Config(
        openai_api_key="your-openai-key",
        cohere_api_key="your-cohere-key",
        database_url="postgresql://user:pass@localhost/psych_db",
        redis_url="redis://localhost:6379"
    )
    
    system = PsychologicalAssessmentSystem(config)
    await system.initialize()
    logger.info("System initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down system")

app = FastAPI(
    title="Psychological Assessment API",
    description="Multi-model psychological assessment system with real-time processing",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Implement your authentication logic here
    # For now, we'll just validate the token exists
    if not credentials.credentials:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return {"user_id": "authenticated_user"}

# ===============================================================================
# REQUEST/RESPONSE MODELS
# ===============================================================================

class AssessmentRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=5000, description="Text to analyze")
    assessment_types: List[AssessmentType] = Field(
        default=[AssessmentType.BIG_FIVE], 
        description="Types of assessments to perform"
    )
    context: Optional[Dict[str, Any]] = Field(
        default_factory=dict, 
        description="Additional context for assessment"
    )

class AssessmentResponse(BaseModel):
    assessment_id: str
    user_id: str
    results: AssessmentResult
    processing_time_ms: int
    status: str

class BatchAssessmentRequest(BaseModel):
    assessments: List[AssessmentRequest] = Field(..., max_items=10)
    
class HealthCheckResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    database_connected: bool
    redis_connected: bool

class SimilarProfilesRequest(BaseModel):
    text: str
    assessment_type: AssessmentType
    limit: int = Field(default=5, ge=1, le=20)

# ===============================================================================
# API ENDPOINTS
# ===============================================================================

@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Test database connection
        db_connected = await test_database_connection()
        redis_connected = await test_redis_connection()
        
        return HealthCheckResponse(
            status="healthy" if db_connected and redis_connected else "degraded",
            timestamp=datetime.utcnow().isoformat(),
            version="1.0.0",
            database_connected=db_connected,
            redis_connected=redis_connected
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.post("/assess", response_model=AssessmentResponse, tags=["Assessment"])
async def single_assessment(
    request: AssessmentRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Perform a single psychological assessment."""
    start_time = time.time()
    
    try:
        user_input = UserInput(
            user_id=current_user["user_id"],
            text=request.text,
            assessment_types=request.assessment_types,
            context=request.context
        )
        
        result = await system.process_single_assessment(user_input)
        
        # Log assessment for analytics (background task)
        background_tasks.add_task(log_assessment_analytics, result)
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return AssessmentResponse(
            assessment_id=result.assessment_id,
            user_id=result.user_id,
            results=result,
            processing_time_ms=processing_time,
            status="completed"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Assessment error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/assess/batch", tags=["Assessment"])
async def batch_assessment(
    request: BatchAssessmentRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Process multiple assessments in batch."""
    if len(request.assessments) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 assessments per batch")
    
    start_time = time.time()
    results = []
    
    try:
        # Process assessments concurrently
        tasks = []
        for i, assessment_req in enumerate(request.assessments):
            user_input = UserInput(
                user_id=f"{current_user['user_id']}_batch_{i}",
                text=assessment_req.text,
                assessment_types=assessment_req.assessment_types,
                context=assessment_req.context
            )
            tasks.append(system.process_single_assessment(user_input))
        
        assessment_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, result in enumerate(assessment_results):
            if isinstance(result, Exception):
                logger.error(f"Batch assessment {i} failed: {result}")
                results.append({
                    "assessment_id": f"failed_{i}",
                    "status": "failed",
                    "error": str(result)
                })
            else:
                results.append({
                    "assessment_id": result.assessment_id,
                    "user_id": result.user_id,
                    "results": result,
                    "status": "completed"
                })
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Log batch analytics
        background_tasks.add_task(log_batch_analytics, len(request.assessments), processing_time)
        
        return {
            "batch_id": str(uuid.uuid4()),
            "total_assessments": len(request.assessments),
            "successful": sum(1 for r in results if r["status"] == "completed"),
            "failed": sum(1 for r in results if r["status"] == "failed"),
            "processing_time_ms": processing_time,
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Batch assessment error: {e}")
        raise HTTPException(status_code=500, detail="Batch processing failed")

@app.post("/similar-profiles", tags=["Analysis"])
async def find_similar_profiles(
    request: SimilarProfilesRequest,
    current_user: dict = Depends(get_current_user)
):
    """Find similar personality profiles based on text input."""
    try:
        # Generate embedding for input text
        nlp_analysis = await system.nlp_pipeline.analyze_text(request.text)
        
        # Find similar profiles
        similar_profiles = await system.db_manager.find_similar_profiles(
            nlp_analysis["embedding"],
            request.assessment_type.value,
            request.limit
        )
        
        return {
            "input_text_stats": nlp_analysis["text_stats"],
            "similar_profiles": similar_profiles,
            "total_found": len(similar_profiles)
        }
        
    except Exception as e:
        logger.error(f"Similar profiles error: {e}")
        raise HTTPException(status_code=500, detail="Failed to find similar profiles")

@app.get("/user/{user_id}/assessments", tags=["User Data"])
async def get_user_assessments(
    user_id: str,
    limit: int = 10,
    offset: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """Get assessment history for a user."""
    # Verify user can access this data
    if current_user["user_id"] != user_id and not is_admin_user(current_user):
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    try:
        assessments = await get_user_assessment_history(user_id, limit, offset)
        return {
            "user_id": user_id,
            "assessments": assessments,
            "total": len(assessments)
        }
    except Exception as e:
        logger.error(f"Error fetching user assessments: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch assessments")

@app.delete("/user/{user_id}/data", tags=["Privacy"])
async def delete_user_data(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete all user data (GDPR compliance)."""
    # Verify user can delete this data
    if current_user["user_id"] != user_id and not is_admin_user(current_user):
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    try:
        deleted_count = await delete_user_data_from_db(user_id)
        logger.info(f"Deleted {deleted_count} records for user {user_id}")
        
        return {
            "message": "User data deleted successfully",
            "user_id": user_id,
            "records_deleted": deleted_count
        }
    except Exception as e:
        logger.error(f"Error deleting user data: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete user data")

@app.get("/analytics/stats", tags=["Analytics"])
async def get_analytics_stats(current_user: dict = Depends(get_current_user)):
    """Get system analytics and usage statistics."""
    if not is_admin_user(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        stats = await get_system_analytics()
        return stats
    except Exception as e:
        logger.error(f"Error fetching analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch analytics")

# ===============================================================================
# WEBSOCKET ENDPOINT
# ===============================================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time assessment."""
    await websocket.accept()
    
    try:
        await system.websocket_handler.handle_connection(websocket, "/ws")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()

# ===============================================================================
# UTILITY FUNCTIONS
# ===============================================================================

async def test_database_connection() -> bool:
    """Test database connectivity."""
    try:
        async with system.db_manager.pool.acquire() as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception:
        return False

async def test_redis_connection() -> bool:
    """Test Redis connectivity."""
    try:
        redis_client = await redis.from_url(system.config.redis_url)
        await redis_client.ping()
        await redis_client.close()
        return True
    except Exception:
        return False

async def log_assessment_analytics(result: AssessmentResult):
    """Log assessment for analytics (background task)."""
    try:
        # Implement your analytics logging here
        logger.info(f"Assessment completed: {result.assessment_id}, confidence: {result.overall_confidence}")
    except Exception as e:
        logger.error(f"Analytics logging error: {e}")

async def log_batch_analytics(count: int, processing_time: int):
    """Log batch processing analytics."""
    try:
        logger.info(f"Batch processed: {count} assessments in {processing_time}ms")
    except Exception as e:
        logger.error(f"Batch analytics error: {e}")

def is_admin_user(user: dict) -> bool:
    """Check if user has admin privileges."""
    # Implement your admin check logic
    return user.get("role") == "admin"

async def get_user_assessment_history(user_id: str, limit: int, offset: int) -> List[dict]:
    """Fetch user assessment history from database."""
    async with system.db_manager.pool.acquire() as conn:
        rows = await conn.fet