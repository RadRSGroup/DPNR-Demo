"""
FastAPI endpoints for Digital Twin Agent
Implements DPNR Digital Twin API contracts
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum

from .digital_twin_agent import (
    DigitalTwinAgent,
    SoulArchetype,
    SoulLevel,
    TwinAspect,
    EvolutionTrigger
)
from ...core.base_agent import AgentMessage


router = APIRouter(prefix="/api/v1/digital-twin", tags=["digital-twin"])


class GenerateTwinRequest(BaseModel):
    """Request to generate digital twin"""
    user_id: str = Field(..., min_length=5, max_length=50)
    assessment_data: Dict[str, Any] = Field(..., description="User assessment and growth data")
    
    @validator('assessment_data')
    def validate_assessment_data(cls, v):
        # Ensure basic required fields
        if not isinstance(v, dict):
            raise ValueError("Assessment data must be a dictionary")
        return v


class GenerateTwinResponse(BaseModel):
    """Response from twin generation"""
    twin_id: str
    archetype: str
    soul_level: str
    visual_representation: Dict[str, Any]
    development_metrics: Dict[str, float]
    aspect_levels: Dict[str, float]
    created_at: str


class EvolveTwinRequest(BaseModel):
    """Request to evolve digital twin"""
    twin_id: str = Field(..., min_length=1)
    trigger: str = Field(..., description="Evolution trigger type")
    trigger_data: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('trigger')
    def validate_trigger(cls, v):
        try:
            EvolutionTrigger(v)
        except ValueError:
            valid_triggers = [t.value for t in EvolutionTrigger]
            raise ValueError(f"Invalid trigger. Must be one of: {valid_triggers}")
        return v


class EvolveTwinResponse(BaseModel):
    """Response from twin evolution"""
    evolution_id: str
    twin_id: str
    trigger: str
    changes: Dict[str, Any]
    new_archetype: str
    new_level: str
    significance: float
    description: str
    metaphor: Optional[str] = None
    visual_changes: Dict[str, Any]
    evolved_at: str


class TwinInsightsRequest(BaseModel):
    """Request for twin insights"""
    twin_id: str = Field(..., min_length=1)
    focus_areas: Optional[List[str]] = Field(default=None, max_items=5)


class TwinInsightsResponse(BaseModel):
    """Response with twin insights"""
    twin_id: str
    insights: List[Dict[str, Any]]
    insight_count: int
    current_archetype: str
    development_stage: str
    generated_at: str


class EvolutionTimelineRequest(BaseModel):
    """Request for evolution timeline"""
    twin_id: str = Field(..., min_length=1)
    timeframe: str = Field("all", regex="^(week|month|quarter|all)$")


class EvolutionTimelineResponse(BaseModel):
    """Response with evolution timeline"""
    twin_id: str
    timeframe: str
    timeline: Dict[str, Any]
    current_state: Dict[str, Any]


class TwinStateResponse(BaseModel):
    """Response with current twin state"""
    twin_id: str
    user_id: str
    archetype: str
    soul_level: str
    development_stage: str
    visual_representation: Dict[str, Any]
    development_metrics: Dict[str, float]
    aspect_levels: Dict[str, float]
    last_updated: str
    evolution_count: int
    breakthrough_count: int


# Global Digital Twin agent instance
_digital_twin_agent = None


async def get_digital_twin_agent() -> DigitalTwinAgent:
    """Get or create Digital Twin agent instance"""
    global _digital_twin_agent
    if _digital_twin_agent is None:
        _digital_twin_agent = DigitalTwinAgent()
        await _digital_twin_agent.initialize()
    return _digital_twin_agent


@router.post("/generate", response_model=GenerateTwinResponse)
async def generate_digital_twin(
    request: GenerateTwinRequest,
    background_tasks: BackgroundTasks,
    agent: DigitalTwinAgent = Depends(get_digital_twin_agent)
) -> GenerateTwinResponse:
    """
    Generate digital twin from user assessment data
    
    Creates a symbolic representation of the user's inner development
    including soul archetype, visual attributes, and development metrics.
    """
    try:
        message = AgentMessage(
            id=f"generate-{request.user_id}-{datetime.utcnow().timestamp()}",
            source_agent="api",
            payload={
                "action": "generate_twin",
                "data": {
                    "user_id": request.user_id,
                    "assessment_data": request.assessment_data
                }
            }
        )
        
        response = await agent.process(message)
        
        if not response.success:
            raise HTTPException(status_code=500, detail=response.error)
        
        data = response.data
        
        # Schedule background processing
        background_tasks.add_task(
            _process_twin_creation_analytics, 
            request.user_id, 
            data.get("twin_id"),
            data.get("archetype")
        )
        
        return GenerateTwinResponse(
            twin_id=data.get("twin_id"),
            archetype=data.get("archetype"),
            soul_level=data.get("soul_level"),
            visual_representation=data.get("visual_representation", {}),
            development_metrics=data.get("development_metrics", {}),
            aspect_levels=data.get("aspect_levels", {}),
            created_at=data.get("created_at")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate twin: {str(e)}")


@router.post("/evolve", response_model=EvolveTwinResponse)
async def evolve_digital_twin(
    request: EvolveTwinRequest,
    background_tasks: BackgroundTasks,
    agent: DigitalTwinAgent = Depends(get_digital_twin_agent)
) -> EvolveTwinResponse:
    """
    Evolve digital twin based on growth and therapeutic progress
    
    Triggers twin evolution based on breakthroughs, integration,
    growth milestones, and other significant development events.
    """
    try:
        message = AgentMessage(
            id=f"evolve-{request.twin_id}-{datetime.utcnow().timestamp()}",
            source_agent="api",
            payload={
                "action": "evolve_twin",
                "data": {
                    "twin_id": request.twin_id,
                    "trigger": request.trigger,
                    "trigger_data": request.trigger_data
                }
            }
        )
        
        response = await agent.process(message)
        
        if not response.success:
            if "not found" in response.error.lower():
                raise HTTPException(status_code=404, detail=response.error)
            raise HTTPException(status_code=500, detail=response.error)
        
        data = response.data
        
        # Schedule background processing for significant evolutions
        if data.get("significance", 0) >= 0.7:
            background_tasks.add_task(
                _process_twin_evolution_celebration,
                data.get("twin_id"),
                data.get("evolution_id"),
                data.get("description")
            )
        
        return EvolveTwinResponse(
            evolution_id=data.get("evolution_id"),
            twin_id=data.get("twin_id"),
            trigger=data.get("trigger"),
            changes=data.get("changes", {}),
            new_archetype=data.get("new_archetype"),
            new_level=data.get("new_level"),
            significance=data.get("significance", 0.5),
            description=data.get("description", ""),
            metaphor=data.get("metaphor"),
            visual_changes=data.get("visual_changes", {}),
            evolved_at=data.get("evolved_at")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to evolve twin: {str(e)}")


@router.get("/{twin_id}/evolution", response_model=EvolutionTimelineResponse)
async def get_twin_evolution_timeline(
    twin_id: str,
    timeframe: str = "all",
    agent: DigitalTwinAgent = Depends(get_digital_twin_agent)
) -> EvolutionTimelineResponse:
    """
    Get twin's evolution timeline
    
    Returns comprehensive timeline of twin's development including
    evolution events, breakthrough moments, and progression summary.
    """
    try:
        # Validate timeframe
        if timeframe not in ["week", "month", "quarter", "all"]:
            raise HTTPException(status_code=400, detail="Invalid timeframe. Must be 'week', 'month', 'quarter', or 'all'")
        
        message = AgentMessage(
            id=f"timeline-{twin_id}-{datetime.utcnow().timestamp()}",
            source_agent="api",
            payload={
                "action": "get_evolution_timeline",
                "data": {
                    "twin_id": twin_id,
                    "timeframe": timeframe
                }
            }
        )
        
        response = await agent.process(message)
        
        if not response.success:
            if "not found" in response.error.lower():
                raise HTTPException(status_code=404, detail=response.error)
            raise HTTPException(status_code=500, detail=response.error)
        
        data = response.data
        
        return EvolutionTimelineResponse(
            twin_id=data.get("twin_id"),
            timeframe=data.get("timeframe"),
            timeline=data.get("timeline", {}),
            current_state=data.get("current_state", {})
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get timeline: {str(e)}")


@router.post("/{twin_id}/insights", response_model=TwinInsightsResponse)
async def get_twin_insights(
    twin_id: str,
    request: TwinInsightsRequest = None,
    agent: DigitalTwinAgent = Depends(get_digital_twin_agent)
) -> TwinInsightsResponse:
    """
    Generate insights from twin analysis
    
    Provides personalized insights about archetype development,
    integration opportunities, and evolution readiness.
    """
    try:
        # Handle both path parameter and request body
        if request is None:
            request = TwinInsightsRequest(twin_id=twin_id)
        elif request.twin_id != twin_id:
            request.twin_id = twin_id
        
        message = AgentMessage(
            id=f"insights-{twin_id}-{datetime.utcnow().timestamp()}",
            source_agent="api",
            payload={
                "action": "get_twin_insights",
                "data": {
                    "twin_id": request.twin_id,
                    "focus_areas": request.focus_areas or []
                }
            }
        )
        
        response = await agent.process(message)
        
        if not response.success:
            if "not found" in response.error.lower():
                raise HTTPException(status_code=404, detail=response.error)
            raise HTTPException(status_code=500, detail=response.error)
        
        data = response.data
        
        return TwinInsightsResponse(
            twin_id=data.get("twin_id"),
            insights=data.get("insights", []),
            insight_count=data.get("insight_count", 0),
            current_archetype=data.get("current_archetype"),
            development_stage=data.get("development_stage"),
            generated_at=data.get("generated_at")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate insights: {str(e)}")


@router.get("/{twin_id}", response_model=TwinStateResponse)
async def get_twin_state(
    twin_id: str,
    agent: DigitalTwinAgent = Depends(get_digital_twin_agent)
) -> TwinStateResponse:
    """
    Get current twin state and summary
    
    Returns comprehensive view of twin's current development state,
    visual representation, and key metrics.
    """
    try:
        # Get twin data from agent's active twins
        if twin_id not in agent.active_twins:
            raise HTTPException(status_code=404, detail=f"Twin {twin_id} not found")
        
        twin = agent.active_twins[twin_id]
        
        return TwinStateResponse(
            twin_id=twin.twin_id,
            user_id=twin.user_id,
            archetype=twin.soul_archetype.value,
            soul_level=twin.soul_level.value,
            development_stage=twin.development_stage,
            visual_representation={
                "attributes": twin.visual_attributes,
                "colors": twin.color_palette,
                "symbols": twin.symbolic_elements
            },
            development_metrics={
                "integration_score": twin.integration_score,
                "wisdom_level": twin.wisdom_level,
                "compassion_depth": twin.compassion_depth,
                "authenticity_strength": twin.authenticity_strength
            },
            aspect_levels=twin.aspect_levels,
            last_updated=twin.last_updated.isoformat(),
            evolution_count=len(twin.evolution_events),
            breakthrough_count=len(twin.breakthrough_moments)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get twin state: {str(e)}")


@router.get("/archetypes")
async def get_soul_archetypes() -> Dict[str, Any]:
    """
    Get available soul archetypes
    
    Returns all supported soul archetypes with descriptions
    and typical characteristics for each stage.
    """
    archetypes = {
        archetype.value: {
            "name": archetype.value.replace('_', ' ').title(),
            "description": _get_archetype_description(archetype),
            "characteristics": _get_archetype_characteristics(archetype),
            "typical_stage": _get_archetype_stage(archetype)
        }
        for archetype in SoulArchetype
    }
    
    return {
        "archetypes": archetypes,
        "total_archetypes": len(archetypes),
        "progression_order": [a.value for a in SoulArchetype]
    }


@router.get("/soul-levels")
async def get_soul_levels() -> Dict[str, Any]:
    """
    Get available soul levels
    
    Returns Kabbalistic soul levels (Nefesh to Yechida) with
    descriptions and development characteristics.
    """
    levels = {
        level.value: {
            "name": level.value.title(),
            "description": _get_soul_level_description(level),
            "development_focus": _get_soul_level_focus(level),
            "typical_experiences": _get_soul_level_experiences(level)
        }
        for level in SoulLevel
    }
    
    return {
        "soul_levels": levels,
        "total_levels": len(levels),
        "development_order": [l.value for l in SoulLevel]
    }


@router.get("/triggers")
async def get_evolution_triggers() -> Dict[str, Any]:
    """
    Get available evolution triggers
    
    Returns all supported evolution triggers that can
    catalyze twin development and transformation.
    """
    triggers = {
        trigger.value: {
            "name": trigger.value.replace('_', ' ').title(),
            "description": _get_trigger_description(trigger),
            "typical_effects": _get_trigger_effects(trigger),
            "significance_range": _get_trigger_significance(trigger)
        }
        for trigger in EvolutionTrigger
    }
    
    return {
        "evolution_triggers": triggers,
        "total_triggers": len(triggers)
    }


@router.get("/health")
async def health_check(
    agent: DigitalTwinAgent = Depends(get_digital_twin_agent)
) -> Dict[str, Any]:
    """Check Digital Twin agent health status"""
    health_data = await agent.health_check()
    return {
        **health_data,
        "framework": "DPNR Digital Twin System",
        "capabilities": [
            "Soul archetype determination and evolution",
            "Visual representation generation",
            "Development milestone tracking",
            "Breakthrough celebration and integration",
            "Symbolic meaning interpretation"
        ],
        "supported_archetypes": health_data.get("supported_archetypes", 0),
        "supported_soul_levels": health_data.get("supported_soul_levels", 0)
    }


# Helper functions for descriptions

def _get_archetype_description(archetype: SoulArchetype) -> str:
    """Get description for soul archetype"""
    descriptions = {
        SoulArchetype.SEEKER: "Beginning spiritual exploration with curiosity and openness",
        SoulArchetype.EXPLORER: "Active inner work and adventurous self-discovery",
        SoulArchetype.HEALER: "Self-healing journey and emerging therapeutic presence",
        SoulArchetype.GUIDE: "Mentoring and teaching others from integrated wisdom",
        SoulArchetype.MYSTIC: "Deep spiritual realization and transcendent awareness",
        SoulArchetype.SAGE: "Unified consciousness serving with compassionate wisdom"
    }
    return descriptions.get(archetype, "Spiritual development archetype")


def _get_archetype_characteristics(archetype: SoulArchetype) -> List[str]:
    """Get characteristics for archetype"""
    characteristics = {
        SoulArchetype.SEEKER: ["Curious", "Open-minded", "Questioning", "Learning-oriented"],
        SoulArchetype.EXPLORER: ["Adventurous", "Brave", "Experimental", "Growth-focused"],
        SoulArchetype.HEALER: ["Compassionate", "Intuitive", "Transformative", "Service-oriented"],
        SoulArchetype.GUIDE: ["Wise", "Supportive", "Teaching", "Mentoring"],
        SoulArchetype.MYSTIC: ["Transcendent", "Unified", "Insightful", "Contemplative"],
        SoulArchetype.SAGE: ["Integrated", "Compassionate", "Serving", "Enlightened"]
    }
    return characteristics.get(archetype, ["Developing", "Growing", "Evolving"])


def _get_archetype_stage(archetype: SoulArchetype) -> str:
    """Get typical stage for archetype"""
    stages = {
        SoulArchetype.SEEKER: "Beginning inner work",
        SoulArchetype.EXPLORER: "Active development",
        SoulArchetype.HEALER: "Integration phase", 
        SoulArchetype.GUIDE: "Service emergence",
        SoulArchetype.MYSTIC: "Transcendent realization",
        SoulArchetype.SAGE: "Unified consciousness"
    }
    return stages.get(archetype, "Spiritual development")


def _get_soul_level_description(level: SoulLevel) -> str:
    """Get description for soul level"""
    descriptions = {
        SoulLevel.NEFESH: "Physical/instinctual soul - basic life force and survival instincts",
        SoulLevel.RUACH: "Emotional soul - feelings, desires, and emotional intelligence", 
        SoulLevel.NESHAMAH: "Intellectual/spiritual soul - higher reasoning and spiritual insight",
        SoulLevel.CHAYAH: "Soul of life - transcendent awareness and unity consciousness",
        SoulLevel.YECHIDA: "Soul of absolute unity - complete oneness with divine essence"
    }
    return descriptions.get(level, "Soul development level")


def _get_soul_level_focus(level: SoulLevel) -> str:
    """Get development focus for soul level"""
    focus_areas = {
        SoulLevel.NEFESH: "Physical wellbeing and basic emotional regulation",
        SoulLevel.RUACH: "Emotional mastery and interpersonal relationships",
        SoulLevel.NESHAMAH: "Intellectual understanding and spiritual practice",
        SoulLevel.CHAYAH: "Transcendent experiences and unity awareness", 
        SoulLevel.YECHIDA: "Complete self-realization and service from oneness"
    }
    return focus_areas.get(level, "Soul development")


def _get_soul_level_experiences(level: SoulLevel) -> List[str]:
    """Get typical experiences for soul level"""
    experiences = {
        SoulLevel.NEFESH: ["Body awareness", "Basic emotions", "Survival instincts"],
        SoulLevel.RUACH: ["Emotional depth", "Relationship skills", "Creative expression"],
        SoulLevel.NESHAMAH: ["Spiritual insights", "Higher reasoning", "Meaningful purpose"],
        SoulLevel.CHAYAH: ["Unity experiences", "Transcendent awareness", "Mystical states"],
        SoulLevel.YECHIDA: ["Oneness consciousness", "Divine union", "Selfless service"]
    }
    return experiences.get(level, ["Spiritual development"])


def _get_trigger_description(trigger: EvolutionTrigger) -> str:
    """Get description for evolution trigger"""
    descriptions = {
        EvolutionTrigger.BREAKTHROUGH: "Major therapeutic breakthrough or realization",
        EvolutionTrigger.INTEGRATION: "Successful parts or shadow integration",
        EvolutionTrigger.GROWTH_MILESTONE: "Significant progress in growth metrics",
        EvolutionTrigger.SPIRITUAL_AWAKENING: "Deep spiritual insight or awakening",
        EvolutionTrigger.RELATIONSHIP_HEALING: "Healing breakthrough in relationships",
        EvolutionTrigger.CREATIVE_EMERGENCE: "Emergence of authentic creative expression"
    }
    return descriptions.get(trigger, "Development catalyst event")


def _get_trigger_effects(trigger: EvolutionTrigger) -> List[str]:
    """Get typical effects of trigger"""
    effects = {
        EvolutionTrigger.BREAKTHROUGH: ["Archetype advancement", "Increased luminosity", "Expanded awareness"],
        EvolutionTrigger.INTEGRATION: ["Greater wholeness", "Reduced inner conflict", "Enhanced authenticity"],
        EvolutionTrigger.GROWTH_MILESTONE: ["Steady development", "Skill advancement", "Confidence increase"],
        EvolutionTrigger.SPIRITUAL_AWAKENING: ["Elevated consciousness", "Divine connection", "Transcendent insight"],
        EvolutionTrigger.RELATIONSHIP_HEALING: ["Heart opening", "Trust building", "Compassion expansion"],
        EvolutionTrigger.CREATIVE_EMERGENCE: ["Creative flow", "Authentic expression", "Joyful manifestation"]
    }
    return effects.get(trigger, ["Positive development"])


def _get_trigger_significance(trigger: EvolutionTrigger) -> str:
    """Get significance range for trigger"""
    significance = {
        EvolutionTrigger.BREAKTHROUGH: "High (0.8-1.0)",
        EvolutionTrigger.INTEGRATION: "Medium-High (0.6-0.8)",
        EvolutionTrigger.GROWTH_MILESTONE: "Medium (0.4-0.7)",
        EvolutionTrigger.SPIRITUAL_AWAKENING: "Very High (0.9-1.0)",
        EvolutionTrigger.RELATIONSHIP_HEALING: "Medium-High (0.6-0.8)",
        EvolutionTrigger.CREATIVE_EMERGENCE: "Medium (0.5-0.7)"
    }
    return significance.get(trigger, "Variable")


# Background task functions

async def _process_twin_creation_analytics(user_id: str, twin_id: str, archetype: str):
    """Background task to process twin creation analytics"""
    # In production, this would:
    # - Update user journey analytics
    # - Trigger welcome sequence for new archetype
    # - Generate personalized development recommendations
    # - Send twin creation notification
    
    print(f"Processing twin creation analytics: User {user_id}, Twin {twin_id}, Archetype {archetype}")


async def _process_twin_evolution_celebration(twin_id: str, evolution_id: str, description: str):
    """Background task to process significant twin evolution"""
    # In production, this would:
    # - Trigger celebration sequence
    # - Generate evolution achievement badges
    # - Update user progress milestones
    # - Send evolution notification with metaphor
    
    print(f"Processing significant twin evolution: {twin_id} - {description}")