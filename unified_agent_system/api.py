
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
from typing import List, Optional, Dict, Any
import time
import logging
from contextlib import asynccontextmanager

# Import from the new unified architecture
from .config import config
from .crews.assessment_crew import AssessmentCrew
from .tools.database_tools import DatabaseManager # Assuming DB logic moves here
from pydantic import BaseModel, Field

# ===============================================================================
# SETUP AND LIFESPAN MANAGEMENT
# ===============================================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global instances for our application
db_manager: Optional[DatabaseManager] = None
assessment_crew: Optional[AssessmentCrew] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """
    global db_manager, assessment_crew
    
    # Initialize database
    db_manager = DatabaseManager(config.database_url)
    await db_manager.initialize()
    
    # Initialize the primary assessment crew
    assessment_crew = AssessmentCrew(db_manager)
    
    logger.info("Unified Agent System initialized successfully")
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

class AssessmentRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=5000, description="Text to analyze")
    assessment_types: List[AssessmentType] = Field(
        default=[AssessmentType.BIG_FIVE], 
        description="Types of assessments to perform"
    )

class AssessmentResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict] = None

class HealthCheckResponse(BaseModel):
    status: str
    database_connected: bool

# ===============================================================================
# CORE API ENDPOINTS
# ===============================================================================

@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """
    Provides a health check of the API and its critical dependencies.
    """
    db_ok = await db_manager.is_connected()
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
        
        # The API's job is to translate the request into inputs for the crew
        # and kick off the process.
        inputs = {
            'user_id': user_id,
            'text': request.text,
            'assessment_types': [t.value for t in request.assessment_types]
        }
        
        # Kick off the crew's work in the background
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
        result=status.get('result')
    )

# ===============================================================================
# MAIN RUN LOGIC (for standalone execution)
# ===============================================================================

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
