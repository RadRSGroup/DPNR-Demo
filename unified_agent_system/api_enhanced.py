"""
Enhanced API with GDPR Authentication, Multi-Provider LLM, and Scalability Features
Production-ready backend for psychological assessment system
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
from typing import List, Optional, Dict, Any, Set
from enum import Enum
import time
import logging
from contextlib import asynccontextmanager
import json
import asyncio
from datetime import datetime

# Import enhanced components  
from .config import config
from .core.auth_gdpr import GDPRCompliantAuth, UserConsent
from .core.scalability_config import ConnectionManager
from .core.assessment_router import AssessmentRouter
from .core.llm_adapter import create_llm_orchestrator
from .core.llm_crew_adapter import UpdatedAssessmentAgents

# Import existing components
from .crews.assessment_crew import AssessmentCrew
from .crews.reporting_crew import ReportingCrew
from .crews.mirror_room_crew import MirrorRoomCrew
from pydantic import BaseModel, Field

# ===============================================================================
# SETUP AND LIFESPAN MANAGEMENT
# ===============================================================================

logging.basicConfig(level=getattr(logging, config.log_level))
logger = logging.getLogger(__name__)

# Global instances
auth_system: Optional[GDPRCompliantAuth] = None
connection_manager: Optional[ConnectionManager] = None
assessment_router: Optional[AssessmentRouter] = None
llm_orchestrator = None
assessment_crew: Optional[AssessmentCrew] = None
reporting_crew: Optional[ReportingCrew] = None
mirror_room_crew: Optional[MirrorRoomCrew] = None

# WebSocket connection manager
class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"WebSocket connected for user {user_id}")
    
    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"WebSocket disconnected for user {user_id}")
    
    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_text(message)
    
    async def broadcast_status(self, message: str):
        for websocket in self.active_connections.values():
            await websocket.send_text(message)

websocket_manager = WebSocketManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Enhanced lifespan management with all production components"""
    global auth_system, connection_manager, assessment_router, llm_orchestrator
    global assessment_crew, reporting_crew, mirror_room_crew
    
    try:
        logger.info("Initializing production backend components...")
        
        # Initialize connection manager
        connection_manager = ConnectionManager()
        await connection_manager.initialize(
            database_url=config.database_url,
            redis_url=config.redis_url,
            read_replica_url=config.read_replica_url
        )
        
        # Initialize GDPR auth system
        auth_system = GDPRCompliantAuth(
            secret_key=config.jwt_secret_key,
            database_url=config.database_url,
            token_expiry_minutes=config.token_expiry_minutes,
            refresh_token_expiry_days=config.refresh_token_expiry_days
        )
        
        # Initialize LLM orchestrator
        llm_orchestrator = create_llm_orchestrator(
            openai_key=config.openai_api_key,
            anthropic_key=config.anthropic_api_key,
            gemini_key=config.gemini_api_key
        )
        
        # Initialize assessment router
        assessment_router = AssessmentRouter(llm_orchestrator)
        
        # Initialize crews with enhanced agents
        enhanced_agents = UpdatedAssessmentAgents()
        assessment_crew = AssessmentCrew(db_manager=connection_manager.db_pool)
        reporting_crew = ReportingCrew()
        mirror_room_crew = MirrorRoomCrew()
        
        logger.info("✅ All production components initialized successfully")
        logger.info(f"✅ Database pool: {config.db_max_connections} max connections")
        logger.info(f"✅ Redis cache: {config.redis_max_connections} max connections")
        logger.info(f"✅ LLM providers: OpenAI, Anthropic, Gemini")
        logger.info(f"✅ Clinical models: {'Enabled' if config.clinical_models_enabled else 'Disabled'}")
        
        yield
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize components: {e}")
        raise
    finally:
        logger.info("Shutting down production backend...")
        if connection_manager:
            await connection_manager.close()

app = FastAPI(
    title="DPNR Psychological Assessment API",
    description="Production-ready multi-provider psychological assessment system with GDPR compliance",
    version="3.0.0",
    lifespan=lifespan
)

# Enhanced CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"] if config.environment == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# ===============================================================================
# PYDANTIC MODELS
# ===============================================================================

class UserRegistrationRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=255, regex=r'^[^@]+@[^@]+\.[^@]+$')
    password: str = Field(..., min_length=8, max_length=128)
    consent: Dict[str, Any] = Field(..., description="GDPR consent object")
    ip_address: str = Field(..., description="User IP address for consent tracking")

class LoginRequest(BaseModel):
    email: str
    password: str

class AssessmentType(str, Enum):
    ENNEAGRAM = "enneagram"
    BIG_FIVE = "big_five"
    EMOTIONAL_INTELLIGENCE = "emotional_intelligence"
    VALUES = "values"
    COGNITIVE_STYLE = "cognitive_style"
    SEFIROT = "sefirot"
    SHADOW_WORK = "shadow_work"
    IFS = "ifs"
    PARDES = "pardes"

class EnhancedAssessmentRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=5000)
    assessment_types: List[AssessmentType] = Field(default=[AssessmentType.BIG_FIVE])
    use_clinical_models: bool = Field(default=True, description="Use clinical transformer models")
    analysis_depth: str = Field(default="standard", regex="^(standard|detailed|clinical)$")
    include_therapeutic_insights: bool = Field(default=True)
    confidence_threshold: float = Field(default=0.75, ge=0.0, le=1.0)

class AssessmentResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict] = None
    clinical_insights: Optional[Dict] = None
    soul_level_insights: Optional[Dict] = None
    overall_confidence: Optional[float] = None
    processing_metadata: Optional[Dict] = None
    error: Optional[str] = None

# ===============================================================================
# AUTHENTICATION ENDPOINTS
# ===============================================================================

@app.post("/auth/register", tags=["Authentication"])
async def register_user(request: UserRegistrationRequest):
    """Register new user with GDPR consent tracking"""
    try:
        # Create consent object
        consent = UserConsent(
            data_processing=request.consent.get("data_processing", False),
            marketing_emails=request.consent.get("marketing_emails", False),
            analytics_tracking=request.consent.get("analytics_tracking", False),
            consent_timestamp=datetime.utcnow(),
            ip_address=request.ip_address
        )
        
        # Create user
        async with connection_manager.db_pool.acquire_write() as db_pool:
            result = await auth_system.create_user(
                email=request.email,
                password=request.password,
                consent=consent,
                db_pool=db_pool
            )
        
        return {
            "status": "success",
            "message": "User created successfully",
            "user_id": result["user_id"],
            "gdpr_compliant": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User registration failed: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@app.post("/auth/login", tags=["Authentication"])
async def login_user(request: LoginRequest):
    """Authenticate user and return JWT tokens"""
    try:
        async with connection_manager.db_pool.acquire_read() as db_pool:
            auth_token = await auth_system.authenticate(
                email=request.email,
                password=request.password,
                db_pool=db_pool
            )
        
        return {
            "access_token": auth_token.access_token,
            "refresh_token": auth_token.refresh_token,
            "token_type": auth_token.token_type,
            "expires_in": auth_token.expires_in,
            "consent_status": auth_token.consent_status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        raise HTTPException(status_code=500, detail="Authentication failed")

@app.post("/auth/refresh", tags=["Authentication"])
async def refresh_token(refresh_token: str):
    """Refresh access token using refresh token"""
    try:
        async with connection_manager.db_pool.acquire_read() as db_pool:
            new_token = await auth_system.refresh_access_token(
                refresh_token=refresh_token,
                db_pool=db_pool
            )
        
        return {
            "access_token": new_token.access_token,
            "token_type": new_token.token_type,
            "expires_in": new_token.expires_in
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh failed: {e}")
        raise HTTPException(status_code=500, detail="Token refresh failed")

# ===============================================================================
# AUTHENTICATION DEPENDENCY
# ===============================================================================

security = HTTPBearer()

async def get_authenticated_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Enhanced authentication with rate limiting and GDPR compliance"""
    try:
        # Verify JWT token
        async with connection_manager.db_pool.acquire_read() as db_pool:
            user_info = await auth_system.verify_token(credentials, db_pool)
        
        # Check rate limit
        rate_allowed = await connection_manager.rate_limiter.check_rate_limit(
            user_info["user_id"]
        )
        
        if not rate_allowed:
            remaining = await connection_manager.rate_limiter.get_remaining_requests(
                user_info["user_id"]
            )
            raise HTTPException(
                status_code=429, 
                detail=f"Rate limit exceeded. {remaining} requests remaining."
            )
        
        return user_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")

# ===============================================================================
# ENHANCED ASSESSMENT ENDPOINTS
# ===============================================================================

@app.post("/assess/enhanced", response_model=AssessmentResponse, status_code=202, tags=["Assessment"])
async def create_enhanced_assessment(
    request: EnhancedAssessmentRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_authenticated_user)
):
    """
    Enhanced assessment with clinical models and multi-provider LLM routing
    """
    try:
        user_id = current_user["user_id"]
        
        # Process each assessment type
        assessment_results = {}
        
        for assessment_type in request.assessment_types:
            # Route to appropriate models and LLMs
            if request.use_clinical_models and config.clinical_models_enabled:
                result = await assessment_router.route_assessment(
                    text=request.text,
                    assessment_type=assessment_type.value,
                    additional_context={
                        "analysis_depth": request.analysis_depth,
                        "user_id": user_id
                    }
                )
                assessment_results[assessment_type.value] = result
            else:
                # Fallback to LLM-only assessment
                llm_response = await llm_orchestrator.generate_with_fallback(
                    prompt=f"Conduct {assessment_type.value} assessment on: {request.text}",
                    assessment_type=assessment_type.value
                )
                assessment_results[assessment_type.value] = {
                    "insights": {"llm_analysis": llm_response.content},
                    "confidence": 0.75
                }
        
        # Generate task ID and store results
        task_id = f"enhanced_{int(time.time())}_{user_id[:8]}"
        
        # Cache results
        await connection_manager.redis_cache.set(
            f"assessment:{task_id}",
            json.dumps({
                "status": "completed",
                "results": assessment_results,
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }),
            ttl=3600
        )
        
        # Send WebSocket update
        await websocket_manager.send_personal_message(
            json.dumps({
                "type": "assessment_completed",
                "task_id": task_id,
                "assessment_types": [t.value for t in request.assessment_types]
            }),
            user_id
        )
        
        return AssessmentResponse(
            task_id=task_id,
            status="completed",
            result=assessment_results,
            clinical_insights=assessment_results.get("clinical"),
            soul_level_insights=assessment_results.get("soul_analysis"),
            overall_confidence=sum(r.get("confidence", 0) for r in assessment_results.values()) / len(assessment_results),
            processing_metadata={
                "clinical_models_used": request.use_clinical_models and config.clinical_models_enabled,
                "assessment_types_processed": len(request.assessment_types),
                "analysis_depth": request.analysis_depth
            }
        )
        
    except Exception as e:
        logger.error(f"Enhanced assessment failed: {e}")
        raise HTTPException(status_code=500, detail="Assessment processing failed")

@app.get("/assess/{task_id}", response_model=AssessmentResponse, tags=["Assessment"])
async def get_assessment_result(
    task_id: str, 
    current_user: dict = Depends(get_authenticated_user)
):
    """Retrieve assessment results with caching"""
    try:
        # Try cache first
        cached_result = await connection_manager.redis_cache.get(f"assessment:{task_id}")
        
        if cached_result:
            result_data = json.loads(cached_result)
            
            # Verify user ownership
            if result_data.get("user_id") != current_user["user_id"]:
                raise HTTPException(status_code=403, detail="Access denied")
            
            return AssessmentResponse(
                task_id=task_id,
                status=result_data["status"],
                result=result_data.get("results"),
                overall_confidence=result_data.get("overall_confidence")
            )
        
        # Fallback to original crew system
        if assessment_crew:
            status = assessment_crew.get_status(task_id)
            if status:
                return AssessmentResponse(
                    task_id=task_id,
                    status=status["status"],
                    result=status.get("result"),
                    error=status.get("error")
                )
        
        raise HTTPException(status_code=404, detail="Assessment not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve assessment: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve assessment")

# ===============================================================================
# GDPR COMPLIANCE ENDPOINTS
# ===============================================================================

@app.get("/gdpr/export", tags=["GDPR"])
async def export_user_data(current_user: dict = Depends(get_authenticated_user)):
    """Export all user data (GDPR Right to Data Portability)"""
    try:
        user_id = current_user["user_id"]
        
        async with connection_manager.db_pool.acquire_read() as db_pool:
            export_data = await auth_system.export_user_data(user_id, db_pool)
        
        return {
            "status": "success",
            "export_data": export_data,
            "gdpr_compliant": True
        }
        
    except Exception as e:
        logger.error(f"Data export failed: {e}")
        raise HTTPException(status_code=500, detail="Data export failed")

@app.delete("/gdpr/delete", tags=["GDPR"])
async def delete_user_data(current_user: dict = Depends(get_authenticated_user)):
    """Delete all user data (GDPR Right to Erasure)"""
    try:
        user_id = current_user["user_id"]
        
        async with connection_manager.db_pool.acquire_write() as db_pool:
            deletion_result = await auth_system.delete_user_data(user_id, db_pool)
        
        return {
            "status": "success",
            "message": "All user data has been anonymized",
            "deletion_timestamp": deletion_result["deletion_timestamp"],
            "gdpr_compliant": True
        }
        
    except Exception as e:
        logger.error(f"Data deletion failed: {e}")
        raise HTTPException(status_code=500, detail="Data deletion failed")

# ===============================================================================
# WEBSOCKET ENDPOINTS
# ===============================================================================

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time assessment updates"""
    try:
        await websocket_manager.connect(websocket, user_id)
        
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            
            # Echo heartbeat
            if data == "ping":
                await websocket.send_text("pong")
            
    except WebSocketDisconnect:
        websocket_manager.disconnect(user_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        websocket_manager.disconnect(user_id)

# ===============================================================================
# HEALTH AND MONITORING
# ===============================================================================

@app.get("/health", tags=["Health"])
async def enhanced_health_check():
    """Comprehensive health check"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {}
    }
    
    try:
        # Check database
        async with connection_manager.db_pool.acquire_read() as conn:
            await conn.fetchval("SELECT 1")
        health_status["components"]["database"] = "healthy"
    except Exception as e:
        health_status["components"]["database"] = f"unhealthy: {e}"
        health_status["status"] = "degraded"
    
    try:
        # Check Redis
        await connection_manager.redis_cache.get("health_check")
        health_status["components"]["redis"] = "healthy"
    except Exception as e:
        health_status["components"]["redis"] = f"unhealthy: {e}"
        health_status["status"] = "degraded"
    
    # Check LLM providers
    available_models = llm_orchestrator.get_available_models()
    health_status["components"]["llm_providers"] = {
        provider.value: len(models) for provider, models in available_models.items()
    }
    
    return health_status

@app.get("/metrics", tags=["Monitoring"])
async def get_metrics(current_user: dict = Depends(get_authenticated_user)):
    """System metrics for monitoring"""
    return {
        "active_websockets": len(websocket_manager.active_connections),
        "db_pool_size": connection_manager.config.db_max_connections,
        "redis_pool_size": connection_manager.config.redis_max_connections,
        "assessment_types_supported": len(AssessmentType),
        "clinical_models_enabled": config.clinical_models_enabled
    }

# ===============================================================================
# MAIN ENTRY POINT
# ===============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "api_enhanced:app",
        host="0.0.0.0",
        port=8000,
        workers=1 if config.debug else 4,
        reload=config.debug,
        log_level=config.log_level.lower()
    )