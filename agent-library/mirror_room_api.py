"""
FastAPI endpoints for Mirror Room Orchestration Engine
DPNR Platform - Signature Therapeutic Experience
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

from agent_library.orchestration.mirror_room_engine import (
    MirrorRoomEngine, 
    SessionDepth, 
    TherapeuticFocus,
    SafetyLevel,
    MirrorRoomSession,
    MirrorRoomResponse
)
from agent_library.core.base_agent import AgentMessage


router = APIRouter(prefix="/api/v1/mirror-room", tags=["mirror-room"])


class StartSessionRequest(BaseModel):
    """Request to start Mirror Room session"""
    user_id: str = Field(..., min_length=1, max_length=50)
    initial_context: str = Field(..., min_length=10, max_length=2000)
    depth_level: Optional[SessionDepth] = SessionDepth.SURFACE


class ContinueSessionRequest(BaseModel):
    """Request to continue Mirror Room session"""
    session_id: str
    user_input: str = Field(..., min_length=1, max_length=1000)


class StartSessionResponse(BaseModel):
    """Response from starting Mirror Room session"""
    session_id: str
    current_depth: SessionDepth
    therapeutic_focus: TherapeuticFocus
    initial_insights: List[Dict[str, Any]]
    safety_level: SafetyLevel
    welcome_message: str


class ContinueSessionResponse(BaseModel):
    """Response from continuing Mirror Room session"""
    session_id: str
    response_text: str
    therapeutic_insights: List[Dict[str, Any]]
    suggested_questions: List[str]
    current_depth: SessionDepth
    depth_progression: float
    safety_assessment: SafetyLevel
    session_recommendations: List[str]
    integration_opportunities: List[str]


class SafetyAssessmentResponse(BaseModel):
    """Response from safety assessment"""
    session_id: str
    safety_level: SafetyLevel
    session_duration: float
    interaction_count: int
    current_depth: SessionDepth
    recommendations: List[str]


class SessionSummaryResponse(BaseModel):
    """Response from ending session"""
    session_id: str
    user_id: str
    duration: float
    interactions: int
    max_depth_reached: SessionDepth
    parts_identified: int
    patterns_identified: int
    therapeutic_insights: List[str]
    integration_opportunities: int


# Global Mirror Room engine instance
_mirror_room_engine = None


async def get_mirror_room_engine() -> MirrorRoomEngine:
    """Get or create Mirror Room engine instance"""
    global _mirror_room_engine
    if _mirror_room_engine is None:
        _mirror_room_engine = MirrorRoomEngine()
        await _mirror_room_engine.initialize()
    return _mirror_room_engine


@router.post("/session/start", response_model=StartSessionResponse)
async def start_mirror_room_session(
    request: StartSessionRequest,
    engine: MirrorRoomEngine = Depends(get_mirror_room_engine)
) -> StartSessionResponse:
    """
    Start a new Mirror Room therapeutic session
    
    The Mirror Room is DPNR's signature therapeutic experience,
    coordinating IFS and Shadow Work agents for deep reflective dialogue.
    """
    try:
        # Create agent message
        message = AgentMessage(
            id=f"mirror-room-start-{datetime.utcnow().timestamp()}",
            source_agent="api",
            payload={
                "action": "start_session",
                "data": {
                    "user_id": request.user_id,
                    "initial_context": request.initial_context,
                    "depth_level": request.depth_level
                }
            }
        )
        
        # Start session
        response = await engine.process(message)
        
        if not response.success:
            raise HTTPException(status_code=500, detail=response.error)
        
        session_data = response.data.get("session", {})
        
        # Generate welcome message based on initial assessment
        welcome_message = _generate_welcome_message(session_data)
        
        return StartSessionResponse(
            session_id=session_data.get("session_id"),
            current_depth=SessionDepth(session_data.get("current_depth", "surface")),
            therapeutic_focus=TherapeuticFocus(session_data.get("therapeutic_focus", "assessment")),
            initial_insights=_extract_initial_insights(session_data),
            safety_level=SafetyLevel(session_data.get("safety_level", "safe")),
            welcome_message=welcome_message
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start session: {str(e)}")


@router.post("/session/continue", response_model=ContinueSessionResponse)
async def continue_mirror_room_session(
    request: ContinueSessionRequest,
    engine: MirrorRoomEngine = Depends(get_mirror_room_engine)
) -> ContinueSessionResponse:
    """
    Continue an existing Mirror Room session
    
    Coordinates therapeutic dialogue between IFS and Shadow Work agents
    with depth progression and safety monitoring.
    """
    try:
        # Create agent message
        message = AgentMessage(
            id=f"mirror-room-continue-{request.session_id}-{datetime.utcnow().timestamp()}",
            source_agent="api",
            payload={
                "action": "continue_session",
                "data": {
                    "session_id": request.session_id,
                    "user_input": request.user_input
                }
            }
        )
        
        # Continue session
        response = await engine.process(message)
        
        if not response.success:
            raise HTTPException(status_code=500, detail=response.error)
        
        response_data = response.data.get("response", {})
        
        return ContinueSessionResponse(
            session_id=response_data.get("session_id"),
            response_text=response_data.get("response_text", ""),
            therapeutic_insights=response_data.get("therapeutic_insights", []),
            suggested_questions=response_data.get("suggested_questions", []),
            current_depth=SessionDepth(response_data.get("current_depth", "surface")),
            depth_progression=response_data.get("depth_progression", 0.0),
            safety_assessment=SafetyLevel(response_data.get("safety_assessment", "safe")),
            session_recommendations=response_data.get("session_recommendations", []),
            integration_opportunities=response_data.get("integration_opportunities", [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to continue session: {str(e)}")


@router.get("/session/{session_id}/safety", response_model=SafetyAssessmentResponse)
async def assess_session_safety(
    session_id: str,
    engine: MirrorRoomEngine = Depends(get_mirror_room_engine)
) -> SafetyAssessmentResponse:
    """
    Assess therapeutic safety of current session
    
    Provides real-time safety monitoring with recommendations
    for session management and potential escalation.
    """
    try:
        safety_data = await engine.assess_session_safety(session_id)
        
        if "error" in safety_data:
            raise HTTPException(status_code=404, detail=safety_data["error"])
        
        return SafetyAssessmentResponse(
            session_id=safety_data.get("session_id"),
            safety_level=SafetyLevel(safety_data.get("safety_level", "safe")),
            session_duration=safety_data.get("session_duration", 0.0),
            interaction_count=safety_data.get("interaction_count", 0),
            current_depth=SessionDepth(safety_data.get("current_depth", "surface")),
            recommendations=safety_data.get("recommendations", [])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to assess safety: {str(e)}")


@router.post("/session/{session_id}/end", response_model=SessionSummaryResponse)
async def end_mirror_room_session(
    session_id: str,
    background_tasks: BackgroundTasks,
    engine: MirrorRoomEngine = Depends(get_mirror_room_engine)
) -> SessionSummaryResponse:
    """
    End Mirror Room session and provide therapeutic summary
    
    Generates comprehensive session summary with insights,
    progress, and recommendations for continued growth.
    """
    try:
        # Create agent message
        message = AgentMessage(
            id=f"mirror-room-end-{session_id}-{datetime.utcnow().timestamp()}",
            source_agent="api",
            payload={
                "action": "end_session",
                "data": {"session_id": session_id}
            }
        )
        
        response = await engine.process(message)
        
        if not response.success:
            raise HTTPException(status_code=500, detail=response.error)
        
        summary_data = response.data.get("session_summary", {})
        
        if "error" in summary_data:
            raise HTTPException(status_code=404, detail=summary_data["error"])
        
        # Schedule background analytics processing
        background_tasks.add_task(_process_session_analytics, summary_data)
        
        return SessionSummaryResponse(
            session_id=summary_data.get("session_id"),
            user_id=summary_data.get("user_id"),
            duration=summary_data.get("duration", 0.0),
            interactions=summary_data.get("interactions", 0),
            max_depth_reached=SessionDepth(summary_data.get("max_depth_reached", "surface")),
            parts_identified=summary_data.get("parts_identified", 0),
            patterns_identified=summary_data.get("patterns_identified", 0),
            therapeutic_insights=summary_data.get("therapeutic_insights", []),
            integration_opportunities=summary_data.get("integration_opportunities", 0)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to end session: {str(e)}")


@router.get("/health")
async def health_check(engine: MirrorRoomEngine = Depends(get_mirror_room_engine)) -> Dict[str, Any]:
    """Check Mirror Room engine health status"""
    health_data = await engine.health_check()
    return {
        **health_data,
        "therapeutic_framework": "IFS + Shadow Work Integration",
        "session_management": "Active session monitoring and safety protocols",
        "capabilities": [
            "Multi-agent therapeutic coordination",
            "Session depth progression",
            "Real-time safety assessment",
            "Integration opportunity detection"
        ],
        "active_sessions": len(engine.active_sessions) if hasattr(engine, 'active_sessions') else 0
    }


# Helper functions

def _generate_welcome_message(session_data: Dict[str, Any]) -> str:
    """Generate personalized welcome message based on initial assessment"""
    
    parts_count = len(session_data.get("identified_parts", []))
    patterns_count = len(session_data.get("identified_patterns", []))
    therapeutic_focus = session_data.get("therapeutic_focus", "assessment")
    
    if therapeutic_focus == "integrated":
        return "Welcome to your Mirror Room session. I notice both internal parts and patterns that may be worth exploring together. This is a space for deep reflection and integration."
    
    elif therapeutic_focus == "parts_work" and parts_count > 0:
        return f"Welcome to your Mirror Room session. I sense {parts_count} distinct part{'s' if parts_count > 1 else ''} of you present. This is a safe space to listen to what these parts have to say."
    
    elif therapeutic_focus == "shadow_integration" and patterns_count > 0:
        return f"Welcome to your Mirror Room session. I notice {patterns_count} pattern{'s' if patterns_count > 1 else ''} that might offer insights into your unconscious processes. Let's explore this with curiosity and compassion."
    
    else:
        return "Welcome to your Mirror Room session. This is a space for deep reflection and self-discovery. I'm here to accompany you as we explore what's present for you today."


def _extract_initial_insights(session_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract initial therapeutic insights from session data"""
    
    insights = []
    
    parts = session_data.get("identified_parts", [])
    patterns = session_data.get("identified_patterns", [])
    
    for part in parts[:2]:  # Limit to first 2 parts for initial response
        insights.append({
            "type": "ifs_part_identified",
            "part_type": part.get("part_type"),
            "role": part.get("role"),
            "confidence": part.get("confidence", 0.0)
        })
    
    for pattern in patterns[:2]:  # Limit to first 2 patterns
        insights.append({
            "type": "shadow_pattern_detected",
            "pattern_type": pattern.get("pattern_type"),
            "emotional_charge": pattern.get("emotional_charge", 0.0),
            "confidence": pattern.get("confidence", 0.0)
        })
    
    return insights


async def _process_session_analytics(summary_data: Dict[str, Any]):
    """Background task to process session analytics"""
    # In production, this would:
    # - Store session data for analytics
    # - Generate insights for user progress tracking
    # - Update therapeutic effectiveness metrics
    # - Prepare integration recommendations
    
    print(f"Processing analytics for session {summary_data.get('session_id')}")
    # Placeholder for analytics processing