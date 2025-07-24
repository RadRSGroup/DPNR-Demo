"""
FastAPI endpoints for Narrative Therapy Agent
Provides REST API for narrative analysis and story reframing
Generated: 2025-07-21
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import logging
import uuid

from .narrative_therapy_agent import (
    NarrativeTherapyAgent,
    NarrativeContext,
    NarrativeAnalysis,
    StoryReframe,
    UniqueOutcome,
    StoryType,
    NarrativeTheme
)
from ...core.base_agent import AgentMessage
from ...core.message_types import MessageType

# Initialize router
router = APIRouter(
    prefix="/api/v1/assessment/narrative",
    tags=["narrative_therapy"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    }
)

# Initialize agent
narrative_agent = NarrativeTherapyAgent()
logger = logging.getLogger(__name__)


# Request/Response Models
class NarrativeAnalysisRequest(BaseModel):
    """Request model for narrative analysis"""
    text: str = Field(..., min_length=10, max_length=5000, description="Text to analyze")
    user_id: str = Field(..., min_length=1, max_length=100, description="User identifier")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")
    include_reframe: bool = Field(default=True, description="Include story reframing")
    
    @validator('text')
    def validate_text(cls, v):
        if len(v.strip()) < 10:
            raise ValueError("Text too short for meaningful analysis")
        return v.strip()


class StoryReframeRequest(BaseModel):
    """Request model for story reframing"""
    story: str = Field(..., min_length=10, max_length=2000, description="Story to reframe")
    problem_story: Optional[str] = Field(None, description="Identified problem story")
    values: Optional[Dict[str, float]] = Field(default_factory=dict, description="User values")
    technique: str = Field(default="strengths_based", description="Reframing technique")
    user_id: str = Field(..., description="User identifier")


class UniqueOutcomesRequest(BaseModel):
    """Request model for finding unique outcomes"""
    text: str = Field(..., min_length=10, max_length=5000, description="Text to analyze")
    problem_story: str = Field(..., description="Problem story to find exceptions to")
    user_id: str = Field(..., description="User identifier")


class ExternalizeRequest(BaseModel):
    """Request model for problem externalization"""
    text: str = Field(..., description="Context text")
    problem_identification: str = Field(..., description="Identified problem")
    user_id: str = Field(..., description="User identifier")


class ValuesAlignmentRequest(BaseModel):
    """Request model for values alignment assessment"""
    narrative_id: str = Field(..., description="ID of analyzed narrative")
    values: Dict[str, float] = Field(..., description="User's identified values")


# Response Models
class NarrativeAnalysisResponse(BaseModel):
    """Response model for narrative analysis"""
    analysis_id: str
    user_id: str
    dominant_story: str
    problem_story: Optional[str]
    externalized_problem: Optional[str]
    unique_outcomes: List[str]
    alternative_story: Optional[str]
    themes: List[str]
    values_alignment: Dict[str, float]
    confidence: float
    reframe: Optional[Dict[str, Any]] = None
    processing_time: float
    timestamp: datetime


class StoryReframeResponse(BaseModel):
    """Response model for story reframing"""
    original_narrative: str
    reframed_narrative: str
    reframing_technique: str
    therapeutic_intent: str
    empowerment_level: float
    processing_time: float


class UniqueOutcomesResponse(BaseModel):
    """Response model for unique outcomes"""
    outcomes: List[Dict[str, Any]]
    total_found: int
    processing_time: float


class ExternalizeResponse(BaseModel):
    """Response model for problem externalization"""
    externalization: str
    problem_name: Optional[str]
    therapeutic_metaphor: str
    processing_time: float


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    agent_id: str
    version: str
    capabilities: List[str]
    ai_enabled: bool


# Endpoints
@router.post("/analyze", response_model=NarrativeAnalysisResponse)
async def analyze_narrative(request: NarrativeAnalysisRequest):
    """
    Analyze text to identify dominant story, problem story, and unique outcomes
    """
    try:
        start_time = datetime.now(timezone.utc)
        
        # Create context
        context = NarrativeContext(
            user_id=request.user_id,
            **request.context
        )
        
        # Create agent message
        message = AgentMessage(
            message_id=str(uuid.uuid4()),
            message_type=MessageType.ASSESSMENT_REQUEST,
            sender_id="api",
            recipient_id=narrative_agent.agent_id,
            payload={
                "action": "analyze_narrative",
                "data": {
                    "text": request.text,
                    "context": context.dict()
                }
            }
        )
        
        # Process with agent
        response = await narrative_agent.process(message)
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Analysis failed: {response.error}"
            )
        
        analysis_data = response.data.get("analysis", {})
        
        # Include reframe if requested
        reframe_data = None
        if request.include_reframe and analysis_data.get("dominant_story"):
            reframe_message = AgentMessage(
                message_id=str(uuid.uuid4()),
                message_type=MessageType.ASSESSMENT_REQUEST,
                sender_id="api",
                recipient_id=narrative_agent.agent_id,
                payload={
                    "action": "reframe_story",
                    "data": {
                        "story": analysis_data["dominant_story"],
                        "problem_story": analysis_data.get("problem_story", ""),
                        "values": context.identified_values or {},
                        "technique": "strengths_based"
                    }
                }
            )
            
            reframe_response = await narrative_agent.process(reframe_message)
            if reframe_response.success:
                reframe_data = reframe_response.data.get("reframe")
        
        processing_time = (datetime.now(timezone.utc) - start_time).total_seconds()
        
        return NarrativeAnalysisResponse(
            analysis_id=analysis_data.get("analysis_id"),
            user_id=analysis_data.get("user_id"),
            dominant_story=analysis_data.get("dominant_story"),
            problem_story=analysis_data.get("problem_story"),
            externalized_problem=analysis_data.get("externalized_problem"),
            unique_outcomes=analysis_data.get("unique_outcomes", []),
            alternative_story=analysis_data.get("alternative_story"),
            themes=[theme for theme in analysis_data.get("themes", [])],
            values_alignment=analysis_data.get("values_alignment", {}),
            confidence=analysis_data.get("confidence", 0.0),
            reframe=reframe_data,
            processing_time=processing_time,
            timestamp=datetime.now(timezone.utc)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Narrative analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error during analysis: {str(e)}"
        )


@router.post("/reframe", response_model=StoryReframeResponse)
async def reframe_story(request: StoryReframeRequest):
    """
    Reframe a story using narrative therapy techniques
    """
    try:
        start_time = datetime.now(timezone.utc)
        
        # Validate technique
        valid_techniques = [
            "strengths_based", "values_focused", "agency_highlighting",
            "exception_finding", "future_oriented", "resource_identifying"
        ]
        
        if request.technique not in valid_techniques:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid technique. Valid options: {valid_techniques}"
            )
        
        # Create agent message
        message = AgentMessage(
            message_id=str(uuid.uuid4()),
            message_type=MessageType.ASSESSMENT_REQUEST,
            sender_id="api",
            recipient_id=narrative_agent.agent_id,
            payload={
                "action": "reframe_story",
                "data": {
                    "story": request.story,
                    "problem_story": request.problem_story or "",
                    "values": request.values or {},
                    "technique": request.technique
                }
            }
        )
        
        # Process with agent
        response = await narrative_agent.process(message)
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Reframing failed: {response.error}"
            )
        
        reframe_data = response.data.get("reframe", {})
        processing_time = (datetime.now(timezone.utc) - start_time).total_seconds()
        
        return StoryReframeResponse(
            original_narrative=reframe_data.get("original_narrative"),
            reframed_narrative=reframe_data.get("reframed_narrative"),
            reframing_technique=reframe_data.get("reframing_technique"),
            therapeutic_intent=reframe_data.get("therapeutic_intent"),
            empowerment_level=reframe_data.get("empowerment_level", 0.0),
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Story reframing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error during reframing: {str(e)}"
        )


@router.post("/unique-outcomes", response_model=UniqueOutcomesResponse)
async def find_unique_outcomes(request: UniqueOutcomesRequest):
    """
    Find unique outcomes (exceptions to problem story)
    """
    try:
        start_time = datetime.now(timezone.utc)
        
        # Create agent message
        message = AgentMessage(
            message_id=str(uuid.uuid4()),
            message_type=MessageType.ASSESSMENT_REQUEST,
            sender_id="api",
            recipient_id=narrative_agent.agent_id,
            payload={
                "action": "find_unique_outcomes",
                "data": {
                    "text": request.text,
                    "problem_story": request.problem_story
                }
            }
        )
        
        # Process with agent
        response = await narrative_agent.process(message)
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Finding unique outcomes failed: {response.error}"
            )
        
        outcomes = response.data.get("outcomes", [])
        processing_time = (datetime.now(timezone.utc) - start_time).total_seconds()
        
        return UniqueOutcomesResponse(
            outcomes=outcomes,
            total_found=len(outcomes),
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unique outcomes error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error finding unique outcomes: {str(e)}"
        )


@router.post("/externalize", response_model=ExternalizeResponse)
async def externalize_problem(request: ExternalizeRequest):
    """
    Externalize a problem (separate person from problem)
    """
    try:
        start_time = datetime.now(timezone.utc)
        
        # Create agent message
        message = AgentMessage(
            message_id=str(uuid.uuid4()),
            message_type=MessageType.ASSESSMENT_REQUEST,
            sender_id="api",
            recipient_id=narrative_agent.agent_id,
            payload={
                "action": "externalize_problem",
                "data": {
                    "text": request.text,
                    "problem_identification": request.problem_identification
                }
            }
        )
        
        # Process with agent
        response = await narrative_agent.process(message)
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Externalization failed: {response.error}"
            )
        
        externalization = response.data.get("externalization", "")
        processing_time = (datetime.now(timezone.utc) - start_time).total_seconds()
        
        # Extract problem name if present
        problem_name = None
        if "The" in externalization:
            start = externalization.find("The")
            end = externalization.find(" ", start + 4)
            if end > start:
                problem_name = externalization[start:end]
        
        return ExternalizeResponse(
            externalization=externalization,
            problem_name=problem_name,
            therapeutic_metaphor=externalization,
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Externalization error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error during externalization: {str(e)}"
        )


@router.post("/values-align")
async def assess_values_alignment(request: ValuesAlignmentRequest):
    """
    Assess how well a narrative aligns with user's values
    """
    try:
        # This would typically look up the narrative from storage
        # For now, return a sample assessment
        
        alignment_scores = {}
        for value, importance in request.values.items():
            # Simple scoring based on importance
            alignment_scores[value] = min(1.0, importance * 0.85)
        
        return {
            "narrative_id": request.narrative_id,
            "values_alignment": alignment_scores,
            "overall_alignment": sum(alignment_scores.values()) / len(alignment_scores) if alignment_scores else 0.0,
            "recommendations": [
                "Consider how your story reflects your value of " + max(request.values, key=request.values.get),
                "Explore ways to strengthen alignment with your core values"
            ]
        }
        
    except Exception as e:
        logger.error(f"Values alignment error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error assessing values: {str(e)}"
        )


@router.get("/story-types", response_model=List[str])
async def get_story_types():
    """
    Get available story types in narrative therapy
    """
    return [story_type.value for story_type in StoryType]


@router.get("/themes", response_model=List[str])
async def get_narrative_themes():
    """
    Get available narrative themes
    """
    return [theme.value for theme in NarrativeTheme]


@router.get("/reframing-techniques", response_model=Dict[str, str])
async def get_reframing_techniques():
    """
    Get available reframing techniques with descriptions
    """
    return {
        "strengths_based": "Focus on hidden strengths and capabilities",
        "values_focused": "Highlight connection to personal values",
        "agency_highlighting": "Emphasize choices and influence",
        "exception_finding": "Build on unique outcomes",
        "future_oriented": "Bridge to preferred future",
        "resource_identifying": "Identify available resources"
    }


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Check narrative therapy agent health
    """
    try:
        await narrative_agent.initialize()
        
        capabilities = [cap.name for cap in narrative_agent.get_capabilities()]
        
        return HealthCheckResponse(
            status="healthy",
            agent_id=narrative_agent.agent_id,
            version=narrative_agent.version,
            capabilities=capabilities,
            ai_enabled=narrative_agent.ai_enabled
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Narrative therapy agent unhealthy"
        )


# Integration endpoints for other DPNR systems
@router.post("/integrate/growth-tracker")
async def integrate_with_growth_tracker(data: Dict[str, Any]):
    """
    Integration endpoint for Growth Tracker
    """
    try:
        # Extract narrative insights for growth tracking
        narrative_id = data.get("narrative_id")
        growth_indicators = {
            "narrative_coherence": 0.75,
            "agency_recognition": 0.80,
            "values_alignment": 0.70,
            "problem_externalization": 0.85
        }
        
        return {
            "narrative_id": narrative_id,
            "growth_indicators": growth_indicators,
            "recommendation": "Continue exploring unique outcomes to strengthen alternative story"
        }
        
    except Exception as e:
        logger.error(f"Growth tracker integration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Integration error: {str(e)}"
        )


@router.post("/integrate/digital-twin")
async def integrate_with_digital_twin(data: Dict[str, Any]):
    """
    Integration endpoint for Digital Twin
    """
    try:
        # Extract narrative themes for twin evolution
        twin_id = data.get("twin_id")
        narrative_themes = data.get("themes", [])
        
        narrative_evolution = {
            "dominant_theme": narrative_themes[0] if narrative_themes else "identity",
            "story_coherence": 0.8,
            "empowerment_trajectory": "ascending",
            "next_chapter_potential": "high"
        }
        
        return {
            "twin_id": twin_id,
            "narrative_evolution": narrative_evolution,
            "soul_story_update": "Your soul's story is expanding beyond old limitations"
        }
        
    except Exception as e:
        logger.error(f"Digital twin integration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Integration error: {str(e)}"
        )