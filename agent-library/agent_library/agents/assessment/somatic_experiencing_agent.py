"""
Somatic Experiencing Agent for DPNR Platform
Body-based trauma processing and nervous system regulation
Based on Peter Levine's Somatic Experiencing methodology
Generated: 2025-07-21
"""
import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any
from pydantic import BaseModel, Field, validator
from enum import Enum
import uuid
import json
import os
try:
    import openai
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None
    AsyncOpenAI = None

from ...core.base_agent import BaseAgent, AgentMessage, AgentResponse, AgentCapability
from ...core.message_types import MessageType, PersonalityScore


class NervousSystemState(str, Enum):
    """Nervous system activation states"""
    REGULATED = "regulated"           # Optimal arousal zone
    HYPERAROUSAL = "hyperarousal"     # Fight/flight activation
    HYPOAROUSAL = "hypoarousal"       # Freeze/collapse state
    MIXED = "mixed"                   # Complex activation patterns
    UNKNOWN = "unknown"               # Cannot determine state


class BodyRegion(str, Enum):
    """Body regions for sensation mapping"""
    HEAD = "head"
    NECK_THROAT = "neck_throat"
    CHEST = "chest"
    HEART = "heart"
    STOMACH = "stomach"
    PELVIS = "pelvis"
    ARMS = "arms"
    HANDS = "hands"
    LEGS = "legs"
    FEET = "feet"
    BACK = "back"
    WHOLE_BODY = "whole_body"


class SensationType(str, Enum):
    """Types of body sensations"""
    TENSION = "tension"
    RELAXATION = "relaxation"
    WARMTH = "warmth"
    COOLNESS = "coolness"
    TINGLING = "tingling"
    NUMBNESS = "numbness"
    PAIN = "pain"
    PLEASURE = "pleasure"
    VIBRATION = "vibration"
    HEAVINESS = "heaviness"
    LIGHTNESS = "lightness"
    EXPANSION = "expansion"
    CONTRACTION = "contraction"
    FLOW = "flow"
    STUCK = "stuck"


class TraumaResponse(str, Enum):
    """Trauma response patterns"""
    FIGHT = "fight"                   # Aggressive mobilization
    FLIGHT = "flight"                 # Escape mobilization  
    FREEZE = "freeze"                 # Immobilization with fear
    FAWN = "fawn"                     # Appeasement response
    COLLAPSE = "collapse"             # Immobilization with shutdown
    DISSOCIATION = "dissociation"     # Disconnection from body/self


class RegulationTechnique(str, Enum):
    """Somatic regulation techniques"""
    GROUNDING = "grounding"           # Connection to present/earth
    BREATHING = "breathing"           # Breath awareness/regulation
    MOVEMENT = "movement"             # Gentle body movement
    ORIENTATION = "orientation"       # Spatial awareness
    RESOURCING = "resourcing"         # Positive body memories
    TITRATION = "titration"           # Small doses of activation
    PENDULATION = "pendulation"       # Movement between states
    VOCALIZING = "vocalizing"         # Sound and vibration


class BodySensation(BaseModel):
    """Individual body sensation"""
    sensation_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    region: BodyRegion
    sensation_type: SensationType
    intensity: float = Field(ge=0.0, le=10.0)
    quality: Optional[str] = None
    duration: Optional[str] = None
    movement: Optional[str] = None
    
    @validator('intensity')
    def validate_intensity(cls, v):
        return max(0.0, min(10.0, v))


class NervousSystemAssessment(BaseModel):
    """Comprehensive nervous system assessment"""
    assessment_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    user_id: str
    current_state: NervousSystemState
    activation_level: float = Field(ge=0.0, le=10.0)
    body_sensations: List[BodySensation]
    trauma_responses: List[TraumaResponse]
    regulation_capacity: float = Field(ge=0.0, le=10.0)
    window_of_tolerance: Dict[str, float]  # optimal arousal range
    recommended_interventions: List[RegulationTechnique]
    safety_level: float = Field(ge=0.0, le=10.0)
    confidence: float = Field(ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RegulationGuidance(BaseModel):
    """Somatic regulation guidance"""
    guidance_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    technique: RegulationTechnique
    instructions: str
    duration_minutes: int = Field(ge=1, le=30)
    precautions: List[str]
    expected_outcome: str
    contraindications: List[str]


class SomaticContext(BaseModel):
    """Context for somatic processing"""
    user_id: str
    trauma_history: Optional[bool] = None
    current_safety: float = Field(default=7.0, ge=0.0, le=10.0)
    therapeutic_relationship: float = Field(default=7.0, ge=0.0, le=10.0)
    body_awareness_level: float = Field(default=5.0, ge=0.0, le=10.0)
    recent_triggers: Optional[List[str]] = []
    medication_effects: Optional[List[str]] = []
    session_history: Optional[List[str]] = []


class SomaticExperiencingAgent(BaseAgent):
    """
    Somatic Experiencing Agent implementing body-based trauma processing
    Based on Peter Levine's methodology focusing on nervous system regulation
    """
    
    def __init__(self):
        super().__init__(
            agent_id="somatic-experiencing-agent",
            name="Somatic Experiencing Agent", 
            version="1.0.0"
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize OpenAI client for AI-powered analysis
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and OPENAI_AVAILABLE:
            self.openai_client = AsyncOpenAI(api_key=api_key)
            self.ai_enabled = True
            self.logger.info("OpenAI client initialized for somatic analysis")
        else:
            self.openai_client = None
            self.ai_enabled = False
            self.logger.warning("No OpenAI API key - using rule-based somatic analysis")
        
        # Load somatic resources
        self.body_sensation_indicators = self._load_sensation_indicators()
        self.regulation_techniques = self._load_regulation_techniques()
        self.trauma_response_patterns = self._load_trauma_patterns()
        
    async def initialize(self) -> bool:
        """Initialize somatic experiencing agent"""
        try:
            self.logger.info("Initializing somatic experiencing agent")
            
            # Define capabilities
            self._capabilities = [
                AgentCapability(
                    name="assess_nervous_system",
                    description="Assess current nervous system state and activation",
                    input_schema={"text": "string", "context": "object"},
                    output_schema={"assessment": "object"}
                ),
                AgentCapability(
                    name="map_body_sensations",
                    description="Identify and map body sensations",
                    input_schema={"description": "string", "regions": "array"},
                    output_schema={"sensations": "array"}
                ),
                AgentCapability(
                    name="detect_trauma_responses",
                    description="Identify trauma response patterns",
                    input_schema={"text": "string", "behavioral_cues": "array"},
                    output_schema={"responses": "array"}
                ),
                AgentCapability(
                    name="generate_regulation_guidance",
                    description="Provide nervous system regulation techniques",
                    input_schema={"state": "string", "context": "object"},
                    output_schema={"guidance": "object"}
                )
            ]
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize: {e}")
            return False
    
    def get_capabilities(self) -> List[AgentCapability]:
        """Return agent capabilities"""
        return self._capabilities
    
    async def validate_input(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate input data"""
        required_fields = {"action", "data"}
        if not all(field in data for field in required_fields):
            return False, f"Missing required fields: {required_fields}"
        
        action = data.get("action")
        valid_actions = [
            "assess_nervous_system", "map_body_sensations", 
            "detect_trauma_responses", "generate_regulation_guidance"
        ]
        if action not in valid_actions:
            return False, f"Unknown action: {action}. Valid: {valid_actions}"
            
        return True, None
    
    async def process(self, message: AgentMessage) -> AgentResponse:
        """Process somatic experiencing request"""
        start_time = datetime.now(timezone.utc)
        
        try:
            action = message.payload.get("action")
            data = message.payload.get("data", {})
            
            if action == "assess_nervous_system":
                assessment = await self.assess_nervous_system(
                    data.get("text", ""),
                    SomaticContext(**data.get("context", {}))
                )
                result = {"assessment": assessment.dict()}
                
            elif action == "map_body_sensations":
                sensations = await self.map_body_sensations(
                    data.get("description", ""),
                    data.get("regions", [])
                )
                result = {"sensations": [s.dict() for s in sensations]}
                
            elif action == "detect_trauma_responses":
                responses = await self.detect_trauma_responses(
                    data.get("text", ""),
                    data.get("behavioral_cues", [])
                )
                result = {"responses": responses}
                
            elif action == "generate_regulation_guidance":
                guidance = await self.generate_regulation_guidance(
                    data.get("state", "unknown"),
                    SomaticContext(**data.get("context", {}))
                )
                result = {"guidance": guidance.dict()}
                
            else:
                raise ValueError(f"Unknown action: {action}")
            
            # Calculate processing confidence
            processing_confidence = 0.85
            if action == "assess_nervous_system" and isinstance(result.get('assessment'), dict):
                processing_confidence = result['assessment'].get('confidence', 0.85)
            
            return AgentResponse(
                success=True,
                data=result,
                processing_time=(datetime.now(timezone.utc) - start_time).total_seconds(),
                agent_id=self.agent_id,
                confidence=processing_confidence
            )
            
        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            return AgentResponse(
                success=False,
                error=str(e),
                processing_time=(datetime.now(timezone.utc) - start_time).total_seconds(),
                agent_id=self.agent_id
            )
    
    async def assess_nervous_system(self, text: str, context: SomaticContext) -> NervousSystemAssessment:
        """Comprehensive nervous system state assessment"""
        
        assessment_id = str(uuid.uuid4())[:8]
        
        # Detect current state
        current_state = await self._detect_nervous_system_state(text, context)
        
        # Calculate activation level
        activation_level = await self._calculate_activation_level(text, current_state)
        
        # Map body sensations
        body_sensations = await self.map_body_sensations(text, [])
        
        # Detect trauma responses
        trauma_responses = await self._detect_trauma_response_patterns(text, context)
        
        # Assess regulation capacity
        regulation_capacity = await self._assess_regulation_capacity(text, context)
        
        # Determine window of tolerance
        window_of_tolerance = await self._calculate_window_of_tolerance(
            activation_level, regulation_capacity, context
        )
        
        # Recommend interventions
        recommended_interventions = await self._recommend_interventions(
            current_state, activation_level, context
        )
        
        # Calculate safety level
        safety_level = await self._assess_somatic_safety(text, context, trauma_responses)
        
        # Calculate confidence
        confidence = await self._calculate_assessment_confidence(
            current_state, body_sensations, context
        )
        
        return NervousSystemAssessment(
            assessment_id=assessment_id,
            user_id=context.user_id,
            current_state=current_state,
            activation_level=activation_level,
            body_sensations=body_sensations,
            trauma_responses=trauma_responses,
            regulation_capacity=regulation_capacity,
            window_of_tolerance=window_of_tolerance,
            recommended_interventions=recommended_interventions,
            safety_level=safety_level,
            confidence=confidence
        )
    
    async def map_body_sensations(self, description: str, regions: List[str] = None) -> List[BodySensation]:
        """Identify and map body sensations from description"""
        
        sensations = []
        
        if self.ai_enabled:
            try:
                prompt = f"""
                Identify specific body sensations from this description. Map each sensation to body regions and types.
                
                Description: "{description}"
                Focus regions: {regions if regions else "All body regions"}
                
                For each sensation identified, provide:
                - Body region (head, chest, stomach, arms, legs, etc.)
                - Sensation type (tension, warmth, tingling, pain, etc.) 
                - Intensity (0-10 scale)
                - Quality description (sharp, dull, pulsing, etc.)
                
                Example format:
                Region: chest | Type: tension | Intensity: 7 | Quality: tight, constricted
                Region: stomach | Type: butterflies | Intensity: 5 | Quality: fluttery, nervous
                """
                
                response = await self._make_ai_request(prompt, max_tokens=200)
                sensations = await self._parse_sensation_response(response)
                
            except Exception as e:
                self.logger.error(f"AI sensation mapping failed: {e}")
                sensations = await self._map_sensations_fallback(description)
        else:
            sensations = await self._map_sensations_fallback(description)
        
        return sensations
    
    async def detect_trauma_responses(self, text: str, behavioral_cues: List[str] = None) -> List[TraumaResponse]:
        """Detect trauma response patterns"""
        
        responses = []
        
        if self.ai_enabled:
            try:
                prompt = f"""
                Identify trauma response patterns from this text and behavioral cues.
                
                Text: "{text}"
                Behavioral cues: {behavioral_cues if behavioral_cues else "None provided"}
                
                Look for indicators of:
                - Fight: Aggression, anger, confrontational language
                - Flight: Avoidance, escape impulses, restlessness  
                - Freeze: Paralysis, inability to act, feeling stuck
                - Fawn: People-pleasing, over-compliance, self-abandonment
                - Collapse: Shutdown, exhaustion, giving up
                - Dissociation: Detachment, feeling unreal, spacing out
                
                Return only the trauma responses that are clearly indicated.
                """
                
                response = await self._make_ai_request(prompt, max_tokens=150)
                responses = await self._parse_trauma_responses(response)
                
            except Exception as e:
                self.logger.error(f"AI trauma response detection failed: {e}")
                responses = await self._detect_trauma_responses_fallback(text)
        else:
            responses = await self._detect_trauma_responses_fallback(text)
        
        return responses
    
    async def generate_regulation_guidance(self, state: str, context: SomaticContext) -> RegulationGuidance:
        """Generate nervous system regulation guidance"""
        
        # Determine appropriate technique based on state
        technique = await self._select_regulation_technique(state, context)
        
        # Generate specific instructions
        instructions = await self._generate_technique_instructions(technique, state, context)
        
        # Determine duration
        duration = await self._calculate_technique_duration(technique, context)
        
        # Safety precautions
        precautions = await self._generate_safety_precautions(technique, context)
        
        # Expected outcomes
        expected_outcome = await self._describe_expected_outcome(technique, state)
        
        # Contraindications
        contraindications = await self._identify_contraindications(technique, context)
        
        return RegulationGuidance(
            technique=technique,
            instructions=instructions,
            duration_minutes=duration,
            precautions=precautions,
            expected_outcome=expected_outcome,
            contraindications=contraindications
        )
    
    # Core Analysis Methods
    async def _detect_nervous_system_state(self, text: str, context: SomaticContext) -> NervousSystemState:
        """Detect current nervous system activation state"""
        
        if self.ai_enabled:
            try:
                prompt = f"""
                Analyze this text to determine the person's nervous system state.
                
                Text: "{text}"
                Safety level: {context.current_safety}/10
                Body awareness: {context.body_awareness_level}/10
                
                States:
                - REGULATED: Calm, centered, able to think clearly
                - HYPERAROUSAL: Anxious, agitated, fight/flight activation
                - HYPOAROUSAL: Numb, shut down, collapsed, frozen
                - MIXED: Combination of high/low activation
                
                Look for indicators like:
                - Energy level, alertness
                - Emotional regulation
                - Cognitive clarity
                - Body language/sensations
                
                Return only the state name.
                """
                
                response = await self._make_ai_request(prompt, max_tokens=50)
                state_name = response.strip().upper()
                
                # Validate response
                try:
                    return NervousSystemState(state_name.lower())
                except ValueError:
                    return await self._detect_state_fallback(text)
                    
            except Exception as e:
                self.logger.error(f"AI state detection failed: {e}")
                return await self._detect_state_fallback(text)
        else:
            return await self._detect_state_fallback(text)
    
    async def _calculate_activation_level(self, text: str, state: NervousSystemState) -> float:
        """Calculate 0-10 activation level"""
        
        base_levels = {
            NervousSystemState.REGULATED: 5.0,
            NervousSystemState.HYPERAROUSAL: 8.0,
            NervousSystemState.HYPOAROUSAL: 2.0,
            NervousSystemState.MIXED: 6.5,
            NervousSystemState.UNKNOWN: 5.0
        }
        
        base_level = base_levels[state]
        
        # Adjust based on text intensity
        activation_words = ["panic", "racing", "can't stop", "overwhelmed", "spinning"]
        shutdown_words = ["numb", "empty", "nothing", "gone", "dead inside"]
        
        text_lower = text.lower()
        activation_count = sum(1 for word in activation_words if word in text_lower)
        shutdown_count = sum(1 for word in shutdown_words if word in text_lower)
        
        if activation_count > shutdown_count:
            base_level = min(10.0, base_level + activation_count * 0.5)
        elif shutdown_count > activation_count:
            base_level = max(0.0, base_level - shutdown_count * 0.5)
        
        return base_level
    
    # AI Helper Methods
    async def _make_ai_request(self, prompt: str, max_tokens: int = 150) -> str:
        """Make AI request with error handling"""
        if not self.ai_enabled or not self.openai_client:
            raise Exception("OpenAI client not available")
            
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            raise
    
    # Fallback Methods
    async def _detect_state_fallback(self, text: str) -> NervousSystemState:
        """Rule-based nervous system state detection"""
        
        text_lower = text.lower()
        
        hyperarousal_indicators = [
            "anxious", "panic", "racing", "can't sit still", "on edge",
            "overwhelmed", "spinning", "hypervigilant", "jumpy"
        ]
        
        hypoarousal_indicators = [
            "numb", "empty", "shut down", "disconnected", "frozen",
            "exhausted", "can't feel", "dead inside", "collapsed"
        ]
        
        regulated_indicators = [
            "calm", "centered", "grounded", "peaceful", "stable",
            "clear", "present", "balanced", "steady"
        ]
        
        hyper_score = sum(1 for indicator in hyperarousal_indicators if indicator in text_lower)
        hypo_score = sum(1 for indicator in hypoarousal_indicators if indicator in text_lower)
        regulated_score = sum(1 for indicator in regulated_indicators if indicator in text_lower)
        
        if regulated_score > max(hyper_score, hypo_score):
            return NervousSystemState.REGULATED
        elif hyper_score > hypo_score and hyper_score > 0:
            return NervousSystemState.HYPERAROUSAL
        elif hypo_score > 0:
            return NervousSystemState.HYPOAROUSAL
        elif hyper_score > 0 and hypo_score > 0:
            return NervousSystemState.MIXED
        else:
            return NervousSystemState.UNKNOWN
    
    async def _map_sensations_fallback(self, description: str) -> List[BodySensation]:
        """Rule-based body sensation mapping"""
        
        sensations = []
        desc_lower = description.lower()
        
        # Common sensation patterns
        sensation_patterns = {
            "chest": {
                "tight": (SensationType.TENSION, 6.0),
                "heavy": (SensationType.HEAVINESS, 7.0),
                "warm": (SensationType.WARMTH, 5.0),
                "flutter": (SensationType.VIBRATION, 4.0)
            },
            "stomach": {
                "butterflies": (SensationType.VIBRATION, 5.0),
                "knot": (SensationType.TENSION, 6.0),
                "sick": (SensationType.PAIN, 5.0),
                "empty": (SensationType.NUMBNESS, 4.0)
            },
            "shoulders": {
                "tense": (SensationType.TENSION, 7.0),
                "tight": (SensationType.TENSION, 6.0),
                "heavy": (SensationType.HEAVINESS, 6.0)
            }
        }
        
        for region, patterns in sensation_patterns.items():
            if region in desc_lower:
                for pattern, (sensation_type, intensity) in patterns.items():
                    if pattern in desc_lower:
                        sensations.append(BodySensation(
                            region=BodyRegion(region if region in [r.value for r in BodyRegion] else "whole_body"),
                            sensation_type=sensation_type,
                            intensity=intensity,
                            quality=pattern
                        ))
        
        # If no specific sensations found, create generic one
        if not sensations:
            sensations.append(BodySensation(
                region=BodyRegion.WHOLE_BODY,
                sensation_type=SensationType.TENSION,
                intensity=5.0,
                quality="general awareness"
            ))
        
        return sensations
    
    async def _detect_trauma_responses_fallback(self, text: str) -> List[TraumaResponse]:
        """Rule-based trauma response detection"""
        
        responses = []
        text_lower = text.lower()
        
        response_indicators = {
            TraumaResponse.FIGHT: ["angry", "rage", "want to hit", "aggressive", "confrontational"],
            TraumaResponse.FLIGHT: ["want to run", "escape", "get away", "avoid", "restless"],
            TraumaResponse.FREEZE: ["frozen", "can't move", "paralyzed", "stuck", "immobilized"],
            TraumaResponse.FAWN: ["please everyone", "say yes", "avoid conflict", "agreeable"],
            TraumaResponse.COLLAPSE: ["give up", "exhausted", "can't go on", "defeated"],
            TraumaResponse.DISSOCIATION: ["space out", "not real", "watching myself", "disconnected"]
        }
        
        for response_type, indicators in response_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                responses.append(response_type)
        
        return responses
    
    # Resource Loading Methods
    def _load_sensation_indicators(self) -> Dict[str, List[str]]:
        """Load body sensation indicator words"""
        return {
            "tension": ["tight", "tense", "constricted", "clenched", "rigid"],
            "warmth": ["warm", "hot", "burning", "heated", "flushed"],
            "tingling": ["tingling", "buzzing", "electric", "pins and needles"],
            "heaviness": ["heavy", "weighted", "sinking", "dense"],
            "lightness": ["light", "floating", "airy", "weightless"]
        }
    
    def _load_regulation_techniques(self) -> Dict[RegulationTechnique, Dict[str, Any]]:
        """Load regulation technique details"""
        return {
            RegulationTechnique.GROUNDING: {
                "description": "Connection to present moment and earth",
                "duration_range": (3, 10),
                "safety_level": "high"
            },
            RegulationTechnique.BREATHING: {
                "description": "Conscious breath awareness and regulation",
                "duration_range": (2, 15),
                "safety_level": "high"
            },
            RegulationTechnique.MOVEMENT: {
                "description": "Gentle, mindful body movement",
                "duration_range": (5, 20),
                "safety_level": "medium"
            },
            RegulationTechnique.RESOURCING: {
                "description": "Accessing positive body memories",
                "duration_range": (3, 10),
                "safety_level": "high"
            }
        }
    
    def _load_trauma_patterns(self) -> Dict[str, List[str]]:
        """Load trauma response pattern indicators"""
        return {
            "hypervigilance": ["scanning", "alert", "danger", "threat"],
            "numbness": ["can't feel", "disconnected", "empty", "void"],
            "overwhelm": ["too much", "can't handle", "drowning", "flood"]
        }
    
    # Helper Methods for Guidance Generation
    async def _select_regulation_technique(self, state: str, context: SomaticContext) -> RegulationTechnique:
        """Select most appropriate regulation technique"""
        
        state_techniques = {
            "hyperarousal": RegulationTechnique.GROUNDING,
            "hypoarousal": RegulationTechnique.MOVEMENT,
            "regulated": RegulationTechnique.RESOURCING,
            "mixed": RegulationTechnique.BREATHING,
            "unknown": RegulationTechnique.BREATHING
        }
        
        return state_techniques.get(state.lower(), RegulationTechnique.GROUNDING)
    
    async def _generate_technique_instructions(self, technique: RegulationTechnique, 
                                             state: str, context: SomaticContext) -> str:
        """Generate specific technique instructions"""
        
        instruction_templates = {
            RegulationTechnique.GROUNDING: "Notice your feet on the ground. Feel the support beneath you. Take a moment to look around and name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste.",
            
            RegulationTechnique.BREATHING: "Place one hand on your chest, one on your belly. Breathe naturally and notice which hand moves more. Gently extend your exhale to be slightly longer than your inhale.",
            
            RegulationTechnique.MOVEMENT: "Stand and gently shake out your arms and hands. Roll your shoulders slowly. Sway side to side like a tree in the breeze. Move only as feels comfortable.",
            
            RegulationTechnique.RESOURCING: "Bring to mind a time when you felt completely safe and at peace. Notice what that feels like in your body. Allow those sensations to expand gently."
        }
        
        return instruction_templates.get(technique, "Focus on your breath and present moment awareness.")
    
    async def _calculate_technique_duration(self, technique: RegulationTechnique, context: SomaticContext) -> int:
        """Calculate appropriate technique duration"""
        
        base_durations = {
            RegulationTechnique.GROUNDING: 5,
            RegulationTechnique.BREATHING: 10,
            RegulationTechnique.MOVEMENT: 8,
            RegulationTechnique.RESOURCING: 7
        }
        
        base = base_durations.get(technique, 5)
        
        # Adjust for body awareness level
        if context.body_awareness_level > 7.0:
            base += 3
        elif context.body_awareness_level < 3.0:
            base = max(3, base - 2)
        
        return min(15, max(3, base))
    
    async def _generate_safety_precautions(self, technique: RegulationTechnique, 
                                         context: SomaticContext) -> List[str]:
        """Generate safety precautions for technique"""
        
        base_precautions = ["Stop if you feel overwhelmed", "Go slowly", "Honor your body's signals"]
        
        if context.trauma_history:
            base_precautions.extend([
                "Have support person nearby if needed",
                "Remember you can stop anytime",
                "Notice if anything feels triggering"
            ])
        
        if context.current_safety < 6.0:
            base_precautions.extend([
                "Stay in current location",
                "Keep eyes open if preferred",
                "Focus on external awareness"
            ])
        
        return base_precautions[:4]  # Limit to 4 most relevant
    
    async def _describe_expected_outcome(self, technique: RegulationTechnique, state: str) -> str:
        """Describe expected outcome of technique"""
        
        outcomes = {
            RegulationTechnique.GROUNDING: "Increased sense of stability and present-moment awareness",
            RegulationTechnique.BREATHING: "Calmer nervous system and improved emotional regulation",
            RegulationTechnique.MOVEMENT: "Released tension and restored natural body flow",
            RegulationTechnique.RESOURCING: "Access to inner strength and positive body memories"
        }
        
        return outcomes.get(technique, "Improved nervous system regulation and body awareness")
    
    async def _identify_contraindications(self, technique: RegulationTechnique, 
                                        context: SomaticContext) -> List[str]:
        """Identify contraindications for technique"""
        
        contraindications = []
        
        if technique == RegulationTechnique.BREATHING and "respiratory" in str(context.medication_effects):
            contraindications.append("Avoid if respiratory medication effects present")
        
        if technique == RegulationTechnique.MOVEMENT and context.current_safety < 5.0:
            contraindications.append("Use caution with movement if feeling unsafe")
        
        if context.trauma_history and technique == RegulationTechnique.RESOURCING:
            contraindications.append("Go slowly with positive memories if trauma history present")
        
        return contraindications
    
    # Assessment Helper Methods
    async def _assess_regulation_capacity(self, text: str, context: SomaticContext) -> float:
        """Assess person's capacity for self-regulation"""
        
        base_capacity = 5.0
        
        # Adjust based on awareness level
        base_capacity += (context.body_awareness_level - 5.0) * 0.5
        
        # Adjust based on safety
        base_capacity += (context.current_safety - 5.0) * 0.3
        
        # Look for regulation indicators in text
        regulation_indicators = ["breathe", "calm down", "center myself", "ground", "pause"]
        text_lower = text.lower()
        
        for indicator in regulation_indicators:
            if indicator in text_lower:
                base_capacity += 0.5
        
        return max(0.0, min(10.0, base_capacity))
    
    async def _calculate_window_of_tolerance(self, activation: float, capacity: float, 
                                           context: SomaticContext) -> Dict[str, float]:
        """Calculate optimal arousal window"""
        
        # Base window is narrower with lower regulation capacity
        window_width = capacity * 0.8
        
        optimal_center = 5.0
        
        return {
            "lower_bound": max(0.0, optimal_center - window_width / 2),
            "upper_bound": min(10.0, optimal_center + window_width / 2),
            "current_position": activation,
            "in_window": abs(activation - optimal_center) <= window_width / 2
        }
    
    async def _recommend_interventions(self, state: NervousSystemState, 
                                     activation: float, context: SomaticContext) -> List[RegulationTechnique]:
        """Recommend appropriate interventions"""
        
        interventions = []
        
        if state == NervousSystemState.HYPERAROUSAL:
            interventions = [RegulationTechnique.GROUNDING, RegulationTechnique.BREATHING]
        elif state == NervousSystemState.HYPOAROUSAL:
            interventions = [RegulationTechnique.MOVEMENT, RegulationTechnique.ORIENTATION]
        elif state == NervousSystemState.MIXED:
            interventions = [RegulationTechnique.PENDULATION, RegulationTechnique.BREATHING]
        else:
            interventions = [RegulationTechnique.RESOURCING, RegulationTechnique.BREATHING]
        
        return interventions[:3]  # Limit to top 3
    
    async def _assess_somatic_safety(self, text: str, context: SomaticContext, 
                                   trauma_responses: List[TraumaResponse]) -> float:
        """Assess safety for somatic work"""
        
        base_safety = context.current_safety
        
        # Reduce safety if trauma responses present
        trauma_impact = len(trauma_responses) * 0.5
        base_safety = max(0.0, base_safety - trauma_impact)
        
        # Check for crisis indicators
        crisis_words = ["hurt myself", "can't go on", "end it", "suicide"]
        text_lower = text.lower()
        
        if any(word in text_lower for word in crisis_words):
            base_safety = min(2.0, base_safety)
        
        return base_safety
    
    async def _calculate_assessment_confidence(self, state: NervousSystemState, 
                                             sensations: List[BodySensation], 
                                             context: SomaticContext) -> float:
        """Calculate confidence in assessment"""
        
        base_confidence = 0.75
        
        # Increase confidence with more body awareness
        base_confidence += (context.body_awareness_level - 5.0) * 0.03
        
        # Increase confidence with clear state detection
        if state != NervousSystemState.UNKNOWN:
            base_confidence += 0.1
        
        # Increase confidence with sensation mapping
        if len(sensations) > 0:
            base_confidence += min(0.1, len(sensations) * 0.02)
        
        # AI vs fallback
        if self.ai_enabled:
            base_confidence += 0.05
        
        return max(0.5, min(0.95, base_confidence))
    
    async def _parse_sensation_response(self, response: str) -> List[BodySensation]:
        """Parse AI response into BodySensation objects"""
        
        sensations = []
        lines = response.strip().split('\n')
        
        for line in lines:
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:
                    try:
                        region_str = parts[0].replace('Region:', '').strip()
                        type_str = parts[1].replace('Type:', '').strip()
                        intensity_str = parts[2].replace('Intensity:', '').strip()
                        
                        # Map to enums
                        region = self._map_to_body_region(region_str)
                        sensation_type = self._map_to_sensation_type(type_str)
                        intensity = float(intensity_str) if intensity_str.replace('.', '').isdigit() else 5.0
                        
                        quality = parts[3].replace('Quality:', '').strip() if len(parts) > 3 else None
                        
                        sensations.append(BodySensation(
                            region=region,
                            sensation_type=sensation_type,
                            intensity=intensity,
                            quality=quality
                        ))
                        
                    except (ValueError, IndexError) as e:
                        self.logger.warning(f"Failed to parse sensation line: {line}, error: {e}")
                        continue
        
        return sensations if sensations else await self._map_sensations_fallback("general body awareness")
    
    async def _parse_trauma_responses(self, response: str) -> List[TraumaResponse]:
        """Parse AI response into TraumaResponse list"""
        
        responses = []
        response_lower = response.lower()
        
        response_mappings = {
            "fight": TraumaResponse.FIGHT,
            "flight": TraumaResponse.FLIGHT,
            "freeze": TraumaResponse.FREEZE,
            "fawn": TraumaResponse.FAWN,
            "collapse": TraumaResponse.COLLAPSE,
            "dissociation": TraumaResponse.DISSOCIATION
        }
        
        for keyword, trauma_response in response_mappings.items():
            if keyword in response_lower:
                responses.append(trauma_response)
        
        return responses
    
    def _map_to_body_region(self, region_str: str) -> BodyRegion:
        """Map string to BodyRegion enum"""
        region_mappings = {
            "chest": BodyRegion.CHEST,
            "stomach": BodyRegion.STOMACH,
            "belly": BodyRegion.STOMACH,
            "head": BodyRegion.HEAD,
            "neck": BodyRegion.NECK_THROAT,
            "throat": BodyRegion.NECK_THROAT,
            "arms": BodyRegion.ARMS,
            "hands": BodyRegion.HANDS,
            "legs": BodyRegion.LEGS,
            "feet": BodyRegion.FEET,
            "back": BodyRegion.BACK,
            "heart": BodyRegion.HEART,
            "pelvis": BodyRegion.PELVIS
        }
        
        region_lower = region_str.lower()
        return region_mappings.get(region_lower, BodyRegion.WHOLE_BODY)
    
    def _map_to_sensation_type(self, type_str: str) -> SensationType:
        """Map string to SensationType enum"""
        type_mappings = {
            "tension": SensationType.TENSION,
            "tight": SensationType.TENSION,
            "tense": SensationType.TENSION,
            "warm": SensationType.WARMTH,
            "warmth": SensationType.WARMTH,
            "hot": SensationType.WARMTH,
            "cool": SensationType.COOLNESS,
            "cold": SensationType.COOLNESS,
            "tingling": SensationType.TINGLING,
            "buzzing": SensationType.TINGLING,
            "numb": SensationType.NUMBNESS,
            "numbness": SensationType.NUMBNESS,
            "pain": SensationType.PAIN,
            "ache": SensationType.PAIN,
            "heavy": SensationType.HEAVINESS,
            "light": SensationType.LIGHTNESS,
            "flutter": SensationType.VIBRATION,
            "butterflies": SensationType.VIBRATION
        }
        
        type_lower = type_str.lower()
        return type_mappings.get(type_lower, SensationType.TENSION)