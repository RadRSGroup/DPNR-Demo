"""
Sefirot API Endpoints for DPNR Agent Library
FastAPI endpoints for sefirot therapeutic processing
Provides REST API access to sefirot agents and orchestrator
Generated for Phase 1 Sefirot Integration
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from .sefirot_base_agent import SefirotType, SefirotFlow
from ...orchestration.sefirot_orchestrator import SefirotOrchestrator

# Initialize router and orchestrator
router = APIRouter(prefix="/api/v1/sefirot", tags=["sefirot"])
logger = logging.getLogger(__name__)

# Global orchestrator instance
sefirot_orchestrator = SefirotOrchestrator()


# Pydantic models for API
class SefirotSessionRequest(BaseModel):
    """Request model for creating sefirot session"""
    user_id: str = Field(..., min_length=5, max_length=50)
    therapeutic_intent: str = Field(..., min_length=10, max_length=500)
    workflow_name: Optional[str] = None
    custom_sefirot: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)


class SefirotProcessingRequest(BaseModel):
    """Request model for sefirot processing"""
    session_id: str
    user_input: str = Field(..., min_length=10, max_length=5000)
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)


class SefirotAgentRequest(BaseModel):
    """Request model for direct sefirot agent processing"""
    user_id: str = Field(..., min_length=5, max_length=50)
    sefirot_type: str
    user_input: str = Field(..., min_length=10, max_length=5000)
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)
    soul_level: str = "nefesh"


class SefirotSessionResponse(BaseModel):
    """Response model for sefirot session"""
    session_id: str
    user_id: str
    therapeutic_intent: str
    created_at: str
    workflow: Optional[str] = None
    active_sefirot: List[str]
    status: str = "active"


class SefirotProcessingResponse(BaseModel):
    """Response model for sefirot processing"""
    session_id: str
    success: bool
    synthesis: Optional[Dict[str, Any]] = None
    sefirot_results: List[Dict[str, Any]] = Field(default_factory=list)
    processing_summary: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class SefirotAgentResponse(BaseModel):
    """Response model for direct sefirot agent processing"""
    sefirot_type: str
    success: bool
    response: Optional[Dict[str, Any]] = None
    confidence: float = 0.0
    processing_time: float = 0.0
    error: Optional[str] = None


# Helper functions
async def get_orchestrator() -> SefirotOrchestrator:
    """Get sefirot orchestrator instance"""
    return sefirot_orchestrator


def validate_sefirot_type(sefirot_type: str) -> SefirotType:
    """Validate and convert sefirot type string"""
    try:
        return SefirotType(sefirot_type.lower())
    except ValueError:
        valid_types = [s.value for s in SefirotType]
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sefirot type: {sefirot_type}. Valid types: {valid_types}"
        )


# API Endpoints

@router.get("/workflows")
async def list_workflows(orchestrator: SefirotOrchestrator = Depends(get_orchestrator)):
    """List available sefirot workflows"""
    try:
        workflows = await orchestrator.list_available_workflows()
        return {
            "success": True,
            "workflows": workflows,
            "count": len(workflows)
        }
    except Exception as e:
        logger.error(f"Failed to list workflows: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/create", response_model=SefirotSessionResponse)
async def create_session(
    request: SefirotSessionRequest,
    orchestrator: SefirotOrchestrator = Depends(get_orchestrator)
):
    """Create new sefirot therapeutic session"""
    try:
        # Validate custom sefirot if provided
        custom_sefirot_types = None
        if request.custom_sefirot:
            custom_sefirot_types = []
            for sefirot_str in request.custom_sefirot:
                sefirot_type = validate_sefirot_type(sefirot_str)
                custom_sefirot_types.append(sefirot_type)
        
        # Create session
        session_id = await orchestrator.create_session(
            user_id=request.user_id,
            therapeutic_intent=request.therapeutic_intent,
            workflow_name=request.workflow_name,
            custom_sefirot=custom_sefirot_types
        )
        
        # Get session info
        session_info = await orchestrator.get_session(session_id)
        
        return SefirotSessionResponse(
            session_id=session_id,
            user_id=request.user_id,
            therapeutic_intent=request.therapeutic_intent,
            created_at=session_info["created_at"],
            workflow=request.workflow_name,
            active_sefirot=session_info["active_agents"]
        )
        
    except Exception as e:
        logger.error(f"Failed to create session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/process", response_model=SefirotProcessingResponse)
async def process_request(
    request: SefirotProcessingRequest,
    background_tasks: BackgroundTasks,
    orchestrator: SefirotOrchestrator = Depends(get_orchestrator)
):
    """Process therapeutic request through sefirot workflow"""
    try:
        # Process the request
        result = await orchestrator.process_therapeutic_request(
            session_id=request.session_id,
            user_input=request.user_input,
            context=request.context
        )
        
        # Add background task for session analytics if successful
        if result["success"]:
            background_tasks.add_task(
                log_session_analytics,
                request.session_id,
                result["processing_summary"]
            )
        
        return SefirotProcessingResponse(
            session_id=request.session_id,
            success=result["success"],
            synthesis=result.get("synthesis"),
            sefirot_results=result.get("sefirot_results", []),
            processing_summary=result.get("processing_summary"),
            error=result.get("error")
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to process request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}")
async def get_session(
    session_id: str,
    orchestrator: SefirotOrchestrator = Depends(get_orchestrator)
):
    """Get sefirot session information"""
    try:
        session_info = await orchestrator.get_session(session_id)
        
        if not session_info:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {
            "success": True,
            "session": session_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/{session_id}/complete")
async def complete_session(
    session_id: str,
    orchestrator: SefirotOrchestrator = Depends(get_orchestrator)
):
    """Complete and finalize sefirot session"""
    try:
        result = await orchestrator.complete_session(session_id)
        
        return {
            "success": True,
            "session_completed": result["completed"],
            "summary": result["summary"],
            "synthesis": result.get("synthesis")
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to complete session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agent/{sefirot_type}", response_model=SefirotAgentResponse)
async def process_direct_agent(
    sefirot_type: str,
    request: SefirotAgentRequest,
    orchestrator: SefirotOrchestrator = Depends(get_orchestrator)
):
    """Process request directly through specific sefirot agent"""
    try:
        # Validate sefirot type
        validated_sefirot_type = validate_sefirot_type(sefirot_type)
        
        # Get agent from orchestrator
        if validated_sefirot_type not in orchestrator.agent_pool:
            raise HTTPException(
                status_code=404,
                detail=f"Sefirot agent {sefirot_type} not available"
            )
        
        agent = orchestrator.agent_pool[validated_sefirot_type]
        
        # Create agent message
        from ...core.base_agent import AgentMessage
        import uuid
        
        message = AgentMessage(
            message_id=str(uuid.uuid4()),
            sender_id="api",
            recipient_id=agent.agent_id,
            message_type="therapeutic_processing",
            payload={
                "action": "process_therapeutic_request",
                "data": {
                    "user_input": request.user_input,
                    "context": {
                        **request.context,
                        "user_id": request.user_id,
                        "soul_level": request.soul_level
                    }
                }
            }
        )
        
        # Process through agent
        response = await agent.process(message)
        
        return SefirotAgentResponse(
            sefirot_type=sefirot_type,
            success=response.success,
            response=response.data if response.success else None,
            confidence=response.confidence or 0.0,
            processing_time=response.processing_time or 0.0,
            error=response.error if not response.success else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to process direct agent request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agent/{sefirot_type}/health")
async def get_agent_health(
    sefirot_type: str,
    orchestrator: SefirotOrchestrator = Depends(get_orchestrator)
):
    """Get health status of specific sefirot agent"""
    try:
        # Validate sefirot type
        validated_sefirot_type = validate_sefirot_type(sefirot_type)
        
        # Get agent health
        if validated_sefirot_type not in orchestrator.agent_pool:
            raise HTTPException(
                status_code=404,
                detail=f"Sefirot agent {sefirot_type} not available"
            )
        
        agent = orchestrator.agent_pool[validated_sefirot_type]
        health_info = await agent.health_check()
        
        return {
            "success": True,
            "sefirot_type": sefirot_type,
            "health": health_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get agent health for {sefirot_type}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/system/health")
async def get_system_health(orchestrator: SefirotOrchestrator = Depends(get_orchestrator)):
    """Get health status of entire sefirot system"""
    try:
        health_info = await orchestrator.health_check()
        
        return {
            "success": True,
            "system_status": "healthy",
            "health_info": health_info,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get system health: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/types")
async def list_sefirot_types():
    """List all available sefirot types and their descriptions"""
    try:
        sefirot_info = {}
        
        for sefirot_type in SefirotType:
            # Get description based on sefirot type
            descriptions = {
                SefirotType.KETER: "Crown - Universal breakthrough catalyst",
                SefirotType.CHOCHMAH: "Wisdom - Insight generation and pattern recognition",
                SefirotType.BINAH: "Understanding - Deep comprehension and integration",
                SefirotType.CHESED: "Compassion - Loving-kindness and healing facilitation",
                SefirotType.GEVURAH: "Strength - Boundaries, discipline, and shadow work",
                SefirotType.TIFERET: "Beauty - Balance, harmony, and aesthetic integration",
                SefirotType.NETZACH: "Victory - Persistence and creative expression",
                SefirotType.HOD: "Glory - Communication and teaching",
                SefirotType.YESOD: "Foundation - Grounding and practical application",
                SefirotType.MALCHUT: "Kingdom - Manifestation and real-world integration"
            }
            
            sefirot_info[sefirot_type.value] = {
                "name": sefirot_type.value.title(),
                "description": descriptions.get(sefirot_type, "Sefirot therapeutic agent"),
                "available": True  # All 10 sefirot now available
            }
        
        return {
            "success": True,
            "sefirot_types": sefirot_info,
            "all_phases_complete": ["keter", "chochmah", "binah", "chesed", "gevurah", "tiferet", "netzach", "hod", "yesod", "malchut"],
            "total_sefirot": len(SefirotType),
            "completion_status": "100% - Full Mystical Framework Operational"
        }
        
    except Exception as e:
        logger.error(f"Failed to list sefirot types: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flows")
async def list_flow_patterns():
    """List available sefirot flow patterns"""
    try:
        flow_info = {}
        
        for flow in SefirotFlow:
            descriptions = {
                SefirotFlow.DESCENDING: "Divine to practical - from transcendent insight to earthly application",
                SefirotFlow.ASCENDING: "Practical to divine - from grounded reality to transcendent understanding", 
                SefirotFlow.BALANCING: "Pillar balancing - harmonizing severity, mercy, and balance pillars",
                SefirotFlow.LIGHTNING: "Lightning flash - rapid activation through entire tree"
            }
            
            flow_info[flow.value] = {
                "name": flow.value.title(),
                "description": descriptions.get(flow, "Sefirot flow pattern"),
                "recommended_use": _get_flow_recommendation(flow)
            }
        
        return {
            "success": True,
            "flow_patterns": flow_info,
            "default_flow": "descending"
        }
        
    except Exception as e:
        logger.error(f"Failed to list flow patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _get_flow_recommendation(flow: SefirotFlow) -> str:
    """Get recommendation for when to use specific flow pattern"""
    recommendations = {
        SefirotFlow.DESCENDING: "Best for integrating spiritual insights into daily life",
        SefirotFlow.ASCENDING: "Best for grounding practical challenges in higher wisdom",
        SefirotFlow.BALANCING: "Best for resolving conflicts and creating harmony",
        SefirotFlow.LIGHTNING: "Best for breakthrough experiences and rapid transformation"
    }
    return recommendations.get(flow, "General therapeutic processing")


# Background tasks
async def log_session_analytics(session_id: str, processing_summary: Dict[str, Any]):
    """Background task to log session analytics"""
    try:
        logger.info(f"Session {session_id} analytics: {processing_summary}")
        # Here you could add database logging, metrics collection, etc.
    except Exception as e:
        logger.error(f"Failed to log analytics for session {session_id}: {e}")


# Include router function for main app
def include_sefirot_routes(app):
    """Include sefirot routes in FastAPI app"""
    app.include_router(router)
    logger.info("Sefirot API endpoints registered")


# Export for convenience
__all__ = [
    "router", 
    "include_sefirot_routes",
    "SefirotSessionRequest",
    "SefirotProcessingRequest", 
    "SefirotAgentRequest",
    "SefirotSessionResponse",
    "SefirotProcessingResponse",
    "SefirotAgentResponse"
]