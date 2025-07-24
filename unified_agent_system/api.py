
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
from typing import List, Optional, Dict, Any
from enum import Enum
import time
import logging
from contextlib import asynccontextmanager

# Import from the new unified architecture
from .config import config
from .crews.assessment_crew import AssessmentCrew
from .crews.reporting_crew import ReportingCrew
from .crews.mirror_room_crew import MirrorRoomCrew
# from .tools.database_tools import DatabaseManager # Will be implemented later
from pydantic import BaseModel, Field

# ===============================================================================
# SETUP AND LIFESPAN MANAGEMENT
# ===============================================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global instances for our application
# db_manager: Optional[DatabaseManager] = None
assessment_crew: Optional[AssessmentCrew] = None
reporting_crew: Optional[ReportingCrew] = None
mirror_room_crew: Optional[MirrorRoomCrew] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """
    global assessment_crew, reporting_crew, mirror_room_crew
    
    # Initialize database (placeholder for now)
    # db_manager = DatabaseManager(config.database_url)
    # await db_manager.initialize()
    
    # Initialize crews
    assessment_crew = AssessmentCrew(db_manager=None)  # Will add db_manager later
    reporting_crew = ReportingCrew()
    mirror_room_crew = MirrorRoomCrew()
    
    logger.info("Unified Agent System initialized successfully")
    logger.info(f"Gemini API Key configured: {'Yes' if config.gemini_api_key else 'No'}")
    yield
    logger.info("Shutting down system")

app = FastAPI(
    title="Unified Psychological Assessment API",
    description="A single, unified API for the multi-model psychological assessment system powered by CrewAI.",
    version="2.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================================================================
# SECURITY (Placeholder)
# ===============================================================================

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Placeholder for authentication logic.
    """
    if not credentials.credentials:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    # In a real app, you would validate the token and fetch user details
    return {"user_id": "authenticated_user_placeholder"}

# ===============================================================================
# API MODELS (Pydantic Schemas)
# ===============================================================================

class AssessmentType(str, Enum):
    ENNEAGRAM = "enneagram"
    BIG_FIVE = "big_five"
    EMOTIONAL_INTELLIGENCE = "emotional_intelligence"
    VALUES = "values"
    COGNITIVE_STYLE = "cognitive_style"

class AssessmentMode(str, Enum):
    COMPREHENSIVE = "comprehensive"  # Single agent with all frameworks
    PARALLEL = "parallel"           # Parallel specialists with integration
    SINGLE_FRAMEWORK = "single_framework"  # One specific framework
    LEGACY = "legacy"               # Backward compatibility

class AssessmentRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=5000, description="Text to analyze")
    assessment_types: List[AssessmentType] = Field(
        default=[AssessmentType.BIG_FIVE], 
        description="Types of assessments to perform (used in legacy mode)"
    )
    assessment_mode: AssessmentMode = Field(
        default=AssessmentMode.COMPREHENSIVE,
        description="Assessment processing mode"
    )
    framework: Optional[AssessmentType] = Field(
        default=None,
        description="Specific framework for single_framework mode"
    )
    analysis_depth: str = Field(
        default="standard",
        description="Analysis depth: standard, detailed, clinical"
    )
    include_therapeutic_insights: bool = Field(
        default=True,
        description="Include therapeutic insights and recommendations"
    )
    confidence_threshold: float = Field(
        default=0.75,
        ge=0.0, le=1.0,
        description="Minimum confidence threshold for assessments"
    )

class AssessmentResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict] = None
    assessment_mode: Optional[str] = None
    frameworks_processed: Optional[int] = None
    overall_confidence: Optional[float] = None
    processing_metadata: Optional[Dict] = None
    error: Optional[str] = None

class HealthCheckResponse(BaseModel):
    status: str
    database_connected: bool

class WeeklySummaryRequest(BaseModel):
    user_id: str = Field(..., description="The ID of the user for whom to generate the summary.")
    context_data: Dict[str, Any] = Field(..., description="Contextual data for the summary, e.g., recent interactions, assessment results.")

class ReportingResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict] = None

class MirrorRoomRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=2000, description="Text for therapeutic analysis")
    therapeutic_focus: str = Field(..., description="Focus area: IFS, Shadow Work, PaRDeS, Growth Tracking, Digital Twin")

class MirrorRoomResponse(BaseModel):
    success: bool
    therapeutic_focus: str
    result: Optional[Dict] = None
    error: Optional[str] = None

# ===============================================================================
# CORE API ENDPOINTS
# ===============================================================================

@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """
    Provides a health check of the API and its critical dependencies.
    """
    # Placeholder for database check
    db_ok = True  # Will implement database check later
    api_status = "healthy" if db_ok else "degraded"
    return HealthCheckResponse(status=api_status, database_connected=db_ok)

@app.post("/assess", response_model=AssessmentResponse, status_code=202, tags=["Assessment"])
async def create_assessment(
    request: AssessmentRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """
    Accepts an assessment request and kicks off the CrewAI workflow in the background.
    """
    try:
        user_id = current_user["user_id"]
        
        # Translate API request to crew inputs
        inputs = {
            'user_id': user_id,
            'text': request.text,
            'assessment_types': [t.value for t in request.assessment_types],
            'assessment_type': request.assessment_mode.value,
            'framework': request.framework.value if request.framework else None,
            'analysis_depth': request.analysis_depth,
            'include_therapeutic_insights': request.include_therapeutic_insights,
            'confidence_threshold': request.confidence_threshold
        }
        
        # Kick off the enhanced crew workflow
        task_id = assessment_crew.kickoff(inputs=inputs)
        
        return AssessmentResponse(
            task_id=task_id,
            status="accepted"
        )
        
    except Exception as e:
        logger.error(f"Failed to kick off assessment: {e}")
        raise HTTPException(status_code=500, detail="Failed to start assessment process.")

@app.get("/assess/{task_id}", response_model=AssessmentResponse, tags=["Assessment"])
async def get_assessment_result(task_id: str, current_user: dict = Depends(get_current_user)):
    """
    Retrieves the status and result of a previously started assessment task.
    """
    status = assessment_crew.get_status(task_id)
    
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
        
    return AssessmentResponse(
        task_id=task_id,
        status=status['status'],
        result=status.get('result'),
        assessment_mode=status.get('result', {}).get('assessment_type'),
        frameworks_processed=status.get('result', {}).get('processing_metadata', {}).get('frameworks_processed'),
        overall_confidence=status.get('result', {}).get('overall_confidence'),
        processing_metadata=status.get('result', {}).get('processing_metadata'),
        error=status.get('error')
    )

@app.post("/report/weekly-summary", response_model=ReportingResponse, status_code=202, tags=["Reporting"])
async def create_weekly_summary(
    request: WeeklySummaryRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """
    Accepts a request to generate a weekly soul summary and kicks off the CrewAI workflow in the background.
    """
    try:
        user_id = current_user["user_id"] # Or use request.user_id if it's part of the request body
        
        # The API's job is to translate the request into inputs for the crew
        inputs = {
            'user_id': user_id,
            'context_data': request.context_data
        }
        
        # Kick off the reporting crew's work in the background
        task_id = reporting_crew.create_weekly_soul_summary_crew(context=inputs).kickoff()
        
        return ReportingResponse(
            task_id=task_id,
            status="accepted"
        )
        
    except Exception as e:
        logger.error(f"Failed to kick off weekly summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to start weekly summary process.")

@app.get("/report/{task_id}", response_model=ReportingResponse, tags=["Reporting"])
async def get_reporting_result(task_id: str, current_user: dict = Depends(get_current_user)):
    """
    Retrieves the status and result of a previously started reporting task.
    """
    status = reporting_crew.get_status(task_id)
    
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
        
    return ReportingResponse(
        task_id=task_id,
        status=status['status'],
        result=status.get('result')
    )

@app.post("/assess/parallel", response_model=AssessmentResponse, status_code=202, tags=["Assessment"])
async def create_parallel_assessment(
    text: str = Field(..., min_length=10, max_length=5000),
    confidence_threshold: float = Field(default=0.75, ge=0.0, le=1.0),
    current_user: dict = Depends(get_current_user)
):
    """
    Run parallel assessment across all 5 frameworks with integration.
    """
    try:
        inputs = {
            'user_id': current_user["user_id"],
            'text': text,
            'assessment_type': 'parallel',
            'confidence_threshold': confidence_threshold
        }
        
        task_id = assessment_crew.kickoff(inputs=inputs)
        
        return AssessmentResponse(
            task_id=task_id,
            status="accepted",
            assessment_mode="parallel"
        )
        
    except Exception as e:
        logger.error(f"Failed to start parallel assessment: {e}")
        raise HTTPException(status_code=500, detail="Failed to start parallel assessment.")

@app.post("/assess/{framework}", response_model=AssessmentResponse, status_code=202, tags=["Assessment"])
async def create_single_framework_assessment(
    framework: AssessmentType,
    text: str = Field(..., min_length=10, max_length=5000),
    analysis_depth: str = Field(default="standard", regex="^(standard|detailed|clinical)$"),
    current_user: dict = Depends(get_current_user)
):
    """
    Run assessment for a single specified framework.
    """
    try:
        inputs = {
            'user_id': current_user["user_id"],
            'text': text,
            'assessment_type': 'single_framework',
            'framework': framework.value,
            'analysis_depth': analysis_depth
        }
        
        task_id = assessment_crew.kickoff(inputs=inputs)
        
        return AssessmentResponse(
            task_id=task_id,
            status="accepted",
            assessment_mode="single_framework",
            frameworks_processed=1
        )
        
    except Exception as e:
        logger.error(f"Failed to start {framework.value} assessment: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start {framework.value} assessment.")

@app.post("/assess/{task_id}/therapeutic-insights", response_model=Dict, tags=["Assessment"])
async def generate_therapeutic_insights(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Generate therapeutic insights from completed assessment results.
    """
    try:
        insights = assessment_crew.generate_therapeutic_insights(task_id)
        return {"task_id": task_id, "therapeutic_insights": insights}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to generate therapeutic insights: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate therapeutic insights.")

@app.get("/assess/tasks", response_model=List[Dict], tags=["Assessment"])
async def list_assessment_tasks(current_user: dict = Depends(get_current_user)):
    """
    List all assessment tasks for monitoring and management.
    """
    return assessment_crew.list_all_tasks()

@app.delete("/assess/cleanup", tags=["Assessment"])
async def cleanup_completed_tasks(
    keep_recent: int = Field(default=10, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """
    Clean up old completed assessment tasks.
    """
    cleaned_count = assessment_crew.cleanup_completed_tasks(keep_recent)
    return {"message": f"Cleaned up {cleaned_count} completed tasks"}

@app.post("/mirror-room", response_model=MirrorRoomResponse, tags=["Mirror Room"])
async def mirror_room_session(
    request: MirrorRoomRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Run a therapeutic session in the Mirror Room with the specified focus.
    """
    try:
        result = mirror_room_crew.run_session(
            initial_text=request.text,
            therapeutic_focus=request.therapeutic_focus
        )
        
        return MirrorRoomResponse(
            success=result.get("success", True),
            therapeutic_focus=request.therapeutic_focus,
            result=result.get("result"),
            error=result.get("error")
        )
        
    except Exception as e:
        logger.error(f"Mirror Room session failed: {e}")
        return MirrorRoomResponse(
            success=False,
            therapeutic_focus=request.therapeutic_focus,
            error=str(e)
        )

# ===============================================================================
# MAIN RUN LOGIC (for standalone execution)
# ===============================================================================

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
