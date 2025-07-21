"""
FastAPI endpoints for IFS Agent
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime

from .ifs_agent import IFSAgent
from ...core.base_agent import AgentMessage


router = APIRouter(prefix="/api/v1/assessment/ifs", tags=["ifs"])


class IFSAnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=5000)
    user_id: str
    session_id: str
    context: Optional[Dict[str, Any]] = None


class IFSAnalyzeResponse(BaseModel):
    parts: List[Dict[str, Any]]
    confidence: float
    session_id: str


class IFSDialogueRequest(BaseModel):
    part_id: str
    message: str
    session_id: str
    session_context: Optional[Dict[str, Any]] = None


class IFSDialogueResponse(BaseModel):
    response: str
    suggested_questions: List[str]
    unburdening_readiness: float
    therapeutic_notes: Optional[str] = None


_ifs_agent = None


async def get_ifs_agent() -> IFSAgent:
    global _ifs_agent
    if _ifs_agent is None:
        _ifs_agent = IFSAgent()
        await _ifs_agent.initialize()
    return _ifs_agent


@router.post("/analyze", response_model=IFSAnalyzeResponse)
async def analyze_for_parts(
    request: IFSAnalyzeRequest,
    agent: IFSAgent = Depends(get_ifs_agent)
) -> IFSAnalyzeResponse:
    try:
        message = AgentMessage(
            id=f"api-{request.session_id}-{datetime.utcnow().timestamp()}",
            source_agent="api",
            payload={
                "action": "identify_parts",
                "data": {"text": request.text, "context": request.context}
            }
        )
        
        response = await agent.process(message)
        
        if not response.success:
            raise HTTPException(status_code=500, detail=response.error)
            
        return IFSAnalyzeResponse(
            parts=response.data.get("parts", []),
            confidence=response.confidence or 0.85,
            session_id=request.session_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dialogue", response_model=IFSDialogueResponse)
async def facilitate_parts_dialogue(
    request: IFSDialogueRequest,
    agent: IFSAgent = Depends(get_ifs_agent)
) -> IFSDialogueResponse:
    try:
        message = AgentMessage(
            id=f"api-dialogue-{request.session_id}-{datetime.utcnow().timestamp()}",
            source_agent="api",
            payload={
                "action": "facilitate_dialogue",
                "data": {
                    "part_id": request.part_id,
                    "message": request.message,
                    "session_context": request.session_context
                }
            }
        )
        
        response = await agent.process(message)
        
        if not response.success:
            raise HTTPException(status_code=500, detail=response.error)
            
        dialogue_data = response.data
        return IFSDialogueResponse(
            response=dialogue_data.get("part_response", ""),
            suggested_questions=dialogue_data.get("suggested_questions", []),
            unburdening_readiness=dialogue_data.get("unburdening_readiness", 0.0),
            therapeutic_notes=dialogue_data.get("therapeutic_notes")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check(agent: IFSAgent = Depends(get_ifs_agent)) -> Dict[str, Any]:
    health_data = await agent.health_check()
    return {
        **health_data,
        "therapeutic_framework": "Internal Family Systems",
        "capabilities": ["identify_parts", "facilitate_dialogue", "assess_readiness"]
    }
