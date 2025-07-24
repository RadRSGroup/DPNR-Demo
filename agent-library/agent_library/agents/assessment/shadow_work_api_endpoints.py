"""
FastAPI endpoints for Shadow Work Agent
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime

from .shadow_work_agent import ShadowWorkAgent, ShadowPattern
from ...core.base_agent import AgentMessage


router = APIRouter(prefix="/api/v1/assessment/shadow", tags=["shadow"])


class ShadowAnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=5000)
    user_id: str
    session_id: str
    history: Optional[List[str]] = []


class ShadowAnalyzeResponse(BaseModel):
    patterns: List[Dict[str, Any]]
    confidence: float
    session_id: str


class IntegrationRequest(BaseModel):
    pattern: Dict[str, Any]
    readiness: float = Field(ge=0.0, le=1.0)
    session_id: str


class IntegrationResponse(BaseModel):
    guidance: Dict[str, Any]
    timeline: str
    warning_signs: List[str]


_shadow_agent = None


async def get_shadow_agent() -> ShadowWorkAgent:
    global _shadow_agent
    if _shadow_agent is None:
        _shadow_agent = ShadowWorkAgent()
        await _shadow_agent.initialize()
    return _shadow_agent


@router.post("/analyze", response_model=ShadowAnalyzeResponse)
async def analyze_shadow_patterns(
    request: ShadowAnalyzeRequest,
    agent: ShadowWorkAgent = Depends(get_shadow_agent)
) -> ShadowAnalyzeResponse:
    """Analyze text for shadow patterns and projections"""
    try:
        message = AgentMessage(
            id=f"shadow-{request.session_id}-{datetime.utcnow().timestamp()}",
            source_agent="api",
            payload={
                "action": "detect_shadow_patterns",
                "data": {
                    "text": request.text,
                    "history": request.history
                }
            }
        )
        
        response = await agent.process(message)
        
        if not response.success:
            raise HTTPException(status_code=500, detail=response.error)
            
        return ShadowAnalyzeResponse(
            patterns=response.data.get("patterns", []),
            confidence=response.confidence or 0.85,
            session_id=request.session_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/integrate", response_model=IntegrationResponse)
async def generate_integration_guidance(
    request: IntegrationRequest,
    agent: ShadowWorkAgent = Depends(get_shadow_agent)
) -> IntegrationResponse:
    """Generate guidance for shadow integration work"""
    try:
        message = AgentMessage(
            id=f"shadow-integrate-{request.session_id}-{datetime.utcnow().timestamp()}",
            source_agent="api",
            payload={
                "action": "generate_integration_guidance",
                "data": {
                    "pattern": request.pattern,
                    "readiness": request.readiness
                }
            }
        )
        
        response = await agent.process(message)
        
        if not response.success:
            raise HTTPException(status_code=500, detail=response.error)
            
        guidance_data = response.data.get("guidance", {})
        return IntegrationResponse(
            guidance=guidance_data,
            timeline=guidance_data.get("integration_timeline", "Unknown"),
            warning_signs=guidance_data.get("warning_signs", [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check(agent: ShadowWorkAgent = Depends(get_shadow_agent)) -> Dict[str, Any]:
    health_data = await agent.health_check()
    return {
        **health_data,
        "therapeutic_framework": "Jungian Shadow Work",
        "capabilities": ["detect_shadow_patterns", "analyze_projections", "generate_integration_guidance"]
    }
