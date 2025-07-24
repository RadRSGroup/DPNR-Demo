"""
FastAPI endpoints for Growth Tracker Agent
Implements DPNR Growth Tracking API
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum

from .growth_tracker_agent import (
    GrowthTrackerAgent, 
    LifeDomain, 
    GrowthMetricType,
    TrendDirection,
    GrowthReport
)
from ...core.base_agent import AgentMessage


router = APIRouter(prefix="/api/v1/growth", tags=["growth-tracker"])


class TrackGrowthRequest(BaseModel):
    """Request to track growth metric"""
    user_id: str = Field(..., min_length=5, max_length=50)
    domain: str  # LifeDomain
    metric: str  # GrowthMetricType
    value: float = Field(..., ge=0.0, le=10.0)
    context: Optional[str] = Field(None, max_length=500)
    session_id: Optional[str] = None
    
    @validator('domain')
    def validate_domain(cls, v):
        try:
            LifeDomain(v)
        except ValueError:
            valid_domains = [d.value for d in LifeDomain]
            raise ValueError(f"Invalid domain. Must be one of: {valid_domains}")
        return v
    
    @validator('metric')
    def validate_metric(cls, v):
        try:
            GrowthMetricType(v)
        except ValueError:
            valid_metrics = [m.value for m in GrowthMetricType]
            raise ValueError(f"Invalid metric. Must be one of: {valid_metrics}")
        return v


class TrackGrowthResponse(BaseModel):
    """Response from tracking growth"""
    recorded: bool
    trend: str
    insights: List[str]
    entry_id: str
    current_value: float
    total_entries: int


class GrowthReportRequest(BaseModel):
    """Request for growth report"""
    user_id: str = Field(..., min_length=5, max_length=50)
    period: str = Field("month", regex="^(week|month|quarter)$")
    domains: Optional[List[str]] = None
    
    @validator('domains')
    def validate_domains(cls, v):
        if v is not None:
            try:
                [LifeDomain(d) for d in v]
            except ValueError:
                valid_domains = [d.value for d in LifeDomain]
                raise ValueError(f"Invalid domain. Must be from: {valid_domains}")
        return v


class GrowthReportResponse(BaseModel):
    """Growth report response"""
    user_id: str
    report_period: str
    start_date: datetime
    end_date: datetime
    overall_growth_score: float
    domain_scores: Dict[str, float]
    trends: List[Dict[str, Any]]
    insights: List[Dict[str, Any]]
    achievements: List[str]
    recommendations: List[str]
    next_focus_areas: List[str]


class TrendAnalysisRequest(BaseModel):
    """Request for trend analysis"""
    user_id: str = Field(..., min_length=5, max_length=50)
    domains: Optional[List[str]] = None
    timeframe_days: int = Field(30, ge=7, le=365)
    
    @validator('domains')
    def validate_domains(cls, v):
        if v is not None:
            try:
                [LifeDomain(d) for d in v]
            except ValueError:
                valid_domains = [d.value for d in LifeDomain]
                raise ValueError(f"Invalid domain. Must be from: {valid_domains}")
        return v


class TrendAnalysisResponse(BaseModel):
    """Response from trend analysis"""
    trends: List[Dict[str, Any]]
    timeframe_days: int
    analysis_date: str


class InsightsRequest(BaseModel):
    """Request for growth insights"""
    user_id: str = Field(..., min_length=5, max_length=50)
    focus_areas: Optional[List[str]] = None
    
    @validator('focus_areas')
    def validate_focus_areas(cls, v):
        if v is not None:
            try:
                [LifeDomain(d) for d in v]
            except ValueError:
                valid_domains = [d.value for d in LifeDomain]
                raise ValueError(f"Invalid focus area. Must be from: {valid_domains}")
        return v


class InsightsResponse(BaseModel):
    """Response with growth insights"""
    insights: List[Dict[str, Any]]
    insight_count: int
    generated_at: str


# Global Growth Tracker agent instance
_growth_tracker_agent = None


async def get_growth_tracker_agent() -> GrowthTrackerAgent:
    """Get or create Growth Tracker agent instance"""
    global _growth_tracker_agent
    if _growth_tracker_agent is None:
        _growth_tracker_agent = GrowthTrackerAgent()
        await _growth_tracker_agent.initialize()
    return _growth_tracker_agent


@router.post("/track", response_model=TrackGrowthResponse)
async def track_growth_metric(
    request: TrackGrowthRequest,
    background_tasks: BackgroundTasks,
    agent: GrowthTrackerAgent = Depends(get_growth_tracker_agent)
) -> TrackGrowthResponse:
    """
    Track growth metric for user
    
    Records a growth measurement across life domains and provides 
    immediate trend analysis and breakthrough insights.
    """
    try:
        message = AgentMessage(
            id=f"track-{request.user_id}-{datetime.utcnow().timestamp()}",
            source_agent="api",
            payload={
                "action": "track_growth",
                "data": {
                    "user_id": request.user_id,
                    "domain": request.domain,
                    "metric": request.metric,
                    "value": request.value,
                    "context": request.context,
                    "session_id": request.session_id
                }
            }
        )
        
        response = await agent.process(message)
        
        if not response.success:
            raise HTTPException(status_code=500, detail=response.error)
        
        data = response.data
        
        # Schedule background analytics processing
        background_tasks.add_task(_process_growth_analytics, request.user_id, data)
        
        return TrackGrowthResponse(
            recorded=data.get("recorded", False),
            trend=data.get("trend", "stable"),
            insights=data.get("insights", []),
            entry_id=data.get("entry_id", ""),
            current_value=data.get("current_value", 0.0),
            total_entries=data.get("total_entries", 0)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to track growth: {str(e)}")


@router.get("/report/{user_id}", response_model=GrowthReportResponse)
async def get_growth_report(
    user_id: str,
    period: str = "month",
    domains: Optional[str] = None,  # Comma-separated domains
    agent: GrowthTrackerAgent = Depends(get_growth_tracker_agent)
) -> GrowthReportResponse:
    """
    Generate comprehensive growth report
    
    Provides detailed analysis of user's progress across life domains
    with insights, achievements, and personalized recommendations.
    """
    try:
        # Parse domains parameter
        domain_list = None
        if domains:
            domain_list = [d.strip() for d in domains.split(",")]
        
        # Validate inputs
        if period not in ["week", "month", "quarter"]:
            raise HTTPException(status_code=400, detail="Period must be 'week', 'month', or 'quarter'")
        
        if domain_list:
            try:
                [LifeDomain(d) for d in domain_list]
            except ValueError:
                valid_domains = [d.value for d in LifeDomain]
                raise HTTPException(status_code=400, detail=f"Invalid domain. Must be from: {valid_domains}")
        
        message = AgentMessage(
            id=f"report-{user_id}-{datetime.utcnow().timestamp()}",
            source_agent="api",
            payload={
                "action": "generate_report",
                "data": {
                    "user_id": user_id,
                    "period": period,
                    "domains": domain_list
                }
            }
        )
        
        response = await agent.process(message)
        
        if not response.success:
            if "No growth data found" in response.error:
                raise HTTPException(status_code=404, detail=response.error)
            raise HTTPException(status_code=500, detail=response.error)
        
        report_data = response.data
        
        return GrowthReportResponse(
            user_id=report_data.get("user_id"),
            report_period=report_data.get("report_period"),
            start_date=datetime.fromisoformat(report_data.get("start_date")) if report_data.get("start_date") else datetime.utcnow(),
            end_date=datetime.fromisoformat(report_data.get("end_date")) if report_data.get("end_date") else datetime.utcnow(),
            overall_growth_score=report_data.get("overall_growth_score", 0.0),
            domain_scores=report_data.get("domain_scores", {}),
            trends=report_data.get("trends", []),
            insights=report_data.get("insights", []),
            achievements=report_data.get("achievements", []),
            recommendations=report_data.get("recommendations", []),
            next_focus_areas=report_data.get("next_focus_areas", [])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")


@router.post("/trends", response_model=TrendAnalysisResponse)
async def analyze_growth_trends(
    request: TrendAnalysisRequest,
    agent: GrowthTrackerAgent = Depends(get_growth_tracker_agent)
) -> TrendAnalysisResponse:
    """
    Analyze growth trends for user
    
    Provides detailed trend analysis across specified domains and timeframes
    with breakthrough detection and pattern recognition.
    """
    try:
        message = AgentMessage(
            id=f"trends-{request.user_id}-{datetime.utcnow().timestamp()}",
            source_agent="api",
            payload={
                "action": "analyze_trends",
                "data": {
                    "user_id": request.user_id,
                    "domains": request.domains,
                    "timeframe": request.timeframe_days
                }
            }
        )
        
        response = await agent.process(message)
        
        if not response.success:
            if "No growth data found" in response.error:
                raise HTTPException(status_code=404, detail=response.error)
            raise HTTPException(status_code=500, detail=response.error)
        
        data = response.data
        
        return TrendAnalysisResponse(
            trends=data.get("trends", []),
            timeframe_days=data.get("timeframe_days", request.timeframe_days),
            analysis_date=data.get("analysis_date", datetime.utcnow().isoformat())
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze trends: {str(e)}")


@router.post("/insights", response_model=InsightsResponse)
async def get_growth_insights(
    request: InsightsRequest,
    agent: GrowthTrackerAgent = Depends(get_growth_tracker_agent)
) -> InsightsResponse:
    """
    Generate growth insights and recommendations
    
    Provides personalized insights based on growth patterns, 
    breakthrough indicators, and integration opportunities.
    """
    try:
        message = AgentMessage(
            id=f"insights-{request.user_id}-{datetime.utcnow().timestamp()}",
            source_agent="api",
            payload={
                "action": "get_insights",
                "data": {
                    "user_id": request.user_id,
                    "focus_areas": request.focus_areas
                }
            }
        )
        
        response = await agent.process(message)
        
        if not response.success:
            if "No growth data found" in response.error:
                raise HTTPException(status_code=404, detail=response.error)
            raise HTTPException(status_code=500, detail=response.error)
        
        data = response.data
        
        return InsightsResponse(
            insights=data.get("insights", []),
            insight_count=data.get("insight_count", 0),
            generated_at=data.get("generated_at", datetime.utcnow().isoformat())
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate insights: {str(e)}")


@router.get("/domains")
async def get_life_domains() -> Dict[str, Any]:
    """
    Get available life domains for growth tracking
    
    Returns all supported life domains with descriptions.
    """
    domains = {
        domain.value: {
            "name": domain.value.replace('_', ' ').title(),
            "description": _get_domain_description(domain)
        }
        for domain in LifeDomain
    }
    
    return {
        "domains": domains,
        "total_domains": len(domains)
    }


@router.get("/metrics")
async def get_growth_metrics() -> Dict[str, Any]:
    """
    Get available growth metrics for tracking
    
    Returns all supported growth metrics with descriptions.
    """
    metrics = {
        metric.value: {
            "name": metric.value.replace('_', ' ').title(),
            "description": _get_metric_description(metric)
        }
        for metric in GrowthMetricType
    }
    
    return {
        "metrics": metrics,
        "total_metrics": len(metrics)
    }


@router.get("/health")
async def health_check(
    agent: GrowthTrackerAgent = Depends(get_growth_tracker_agent)
) -> Dict[str, Any]:
    """Check Growth Tracker agent health status"""
    health_data = await agent.health_check()
    return {
        **health_data,
        "framework": "DPNR Growth Tracking System",
        "capabilities": [
            "Life domain progress tracking",
            "Trend analysis and breakthrough detection", 
            "Personalized growth insights",
            "Cross-domain pattern recognition"
        ],
        "supported_domains": len(LifeDomain),
        "supported_metrics": len(GrowthMetricType)
    }


# Helper functions

def _get_domain_description(domain: LifeDomain) -> str:
    """Get description for life domain"""
    descriptions = {
        LifeDomain.RELATIONSHIPS: "Quality and depth of personal relationships",
        LifeDomain.CAREER_PURPOSE: "Professional fulfillment and life purpose alignment",
        LifeDomain.EMOTIONAL_WELLBEING: "Emotional health, regulation, and resilience",
        LifeDomain.SPIRITUAL_GROWTH: "Connection to meaning, transcendence, and sacred",
        LifeDomain.PHYSICAL_HEALTH: "Physical vitality, energy, and body wellness",
        LifeDomain.CREATIVITY_EXPRESSION: "Creative outlets and authentic self-expression",
        LifeDomain.PERSONAL_DEVELOPMENT: "Self-growth, learning, and consciousness expansion",
        LifeDomain.FAMILY_COMMUNITY: "Family bonds and community connection"
    }
    return descriptions.get(domain, "Personal growth in this life area")


def _get_metric_description(metric: GrowthMetricType) -> str:
    """Get description for growth metric"""
    descriptions = {
        GrowthMetricType.EMOTIONAL_REGULATION: "Ability to manage emotions skillfully",
        GrowthMetricType.SELF_AWARENESS: "Understanding of inner patterns and motivations",
        GrowthMetricType.RELATIONSHIP_QUALITY: "Depth and health of connections with others",
        GrowthMetricType.PURPOSE_CLARITY: "Clarity about life direction and meaning",
        GrowthMetricType.STRESS_MANAGEMENT: "Capacity to handle stress and pressure",
        GrowthMetricType.AUTHENTICITY: "Alignment between true self and outer expression",
        GrowthMetricType.RESILIENCE: "Ability to bounce back from challenges",
        GrowthMetricType.COMPASSION: "Kindness and understanding toward self and others",
        GrowthMetricType.BOUNDARIES: "Healthy limits and self-protection",
        GrowthMetricType.SPIRITUAL_CONNECTION: "Connection to transcendent meaning and purpose"
    }
    return descriptions.get(metric, "Growth measurement in this area")


async def _process_growth_analytics(user_id: str, growth_data: Dict[str, Any]):
    """Background task to process growth analytics"""
    # In production, this would:
    # - Update user progress dashboards
    # - Trigger milestone celebrations  
    # - Update Digital Twin evolution
    # - Generate personalized growth recommendations
    # - Send progress notifications
    
    print(f"Processing growth analytics for user {user_id}: {growth_data.get('trend', 'stable')} trend")