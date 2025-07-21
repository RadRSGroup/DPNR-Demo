"""
Attachment Style Agent for DPNR Platform  
Relationship pattern analysis and attachment style assessment
Based on Bowlby/Ainsworth attachment theory
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


class AttachmentStyle(str, Enum):
    """Four primary attachment styles"""
    SECURE = "secure"                      # Comfortable with intimacy and autonomy
    ANXIOUS_PREOCCUPIED = "anxious_preoccupied"  # Seeks intimacy but fears abandonment
    DISMISSIVE_AVOIDANT = "dismissive_avoidant"  # Values independence, avoids closeness
    FEARFUL_AVOIDANT = "fearful_avoidant"        # Wants close relationships but fears hurt


class RelationshipPattern(str, Enum):
    """Common relationship patterns"""
    PURSUIT_DISTANCE = "pursuit_distance"  # One pursues, other distances
    CONFLICT_AVOIDANCE = "conflict_avoidance"  # Avoiding difficult conversations
    CARETAKING = "caretaking"             # Over-functioning for others
    BOUNDARY_ISSUES = "boundary_issues"    # Difficulty setting/maintaining boundaries
    EMOTIONAL_FUSION = "emotional_fusion"  # Loss of individual identity in relationships
    ISOLATION = "isolation"                # Tendency to withdraw from relationships
    PEOPLE_PLEASING = "people_pleasing"    # Sacrificing self for others' approval
    CONTROL_DYNAMICS = "control_dynamics"  # Power struggles in relationships


class ActivatingStrategy(str, Enum):
    """Strategies to maintain closeness (anxious attachment)"""
    PROTEST_BEHAVIOR = "protest_behavior"  # Acting out to get attention
    EXCESSIVE_REASSURANCE = "excessive_reassurance"  # Constant need for validation
    HYPERVIGILANCE = "hypervigilance"     # Over-monitoring relationship threats
    CLINGING = "clinging"                  # Difficulty with separation
    EMOTIONAL_INTENSITY = "emotional_intensity"  # Heightened emotional expressions


class DeactivatingStrategy(str, Enum):
    """Strategies to maintain distance (avoidant attachment)"""
    EMOTIONAL_SHUTDOWN = "emotional_shutdown"  # Suppressing feelings
    DISTANCING = "distancing"              # Creating physical/emotional space
    INTELLECTUALIZATION = "intellectualization"  # Focusing on logic over emotion
    SELF_RELIANCE = "self_reliance"        # Refusing to depend on others
    MINIMIZATION = "minimization"          # Downplaying relationship importance


class AttachmentWound(BaseModel):
    """Early attachment injury or trauma"""
    wound_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    developmental_stage: str  # infancy, early childhood, adolescence, etc.
    wound_type: str          # abandonment, engulfment, betrayal, etc.
    impact_description: str
    current_manifestation: str
    healing_potential: float = Field(ge=0.0, le=10.0)


class RelationshipDynamics(BaseModel):
    """Analysis of relationship patterns"""
    dynamics_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    user_id: str
    primary_patterns: List[RelationshipPattern]
    activating_strategies: List[ActivatingStrategy]
    deactivating_strategies: List[DeactivatingStrategy]
    attachment_wounds: List[AttachmentWound]
    relationship_strengths: List[str]
    growth_edges: List[str]
    earned_security_potential: float = Field(ge=0.0, le=10.0)


class AttachmentAssessment(BaseModel):
    """Comprehensive attachment style assessment"""
    assessment_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    user_id: str
    primary_attachment_style: AttachmentStyle
    secondary_style: Optional[AttachmentStyle] = None
    style_certainty: float = Field(ge=0.0, le=1.0)
    relationship_dynamics: RelationshipDynamics
    attachment_history: Dict[str, Any]
    current_relationship_patterns: List[str]
    healing_recommendations: List[str]
    earned_security_pathway: List[str]
    confidence: float = Field(ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AttachmentContext(BaseModel):
    """Context for attachment analysis"""
    user_id: str
    relationship_status: Optional[str] = None
    family_history: Optional[Dict[str, Any]] = {}
    previous_relationships: Optional[List[str]] = []
    current_challenges: Optional[List[str]] = []
    therapy_history: Optional[bool] = None
    age_range: Optional[str] = None
    cultural_background: Optional[str] = None


class AttachmentStyleAgent(BaseAgent):
    """
    Attachment Style Agent implementing relationship pattern analysis
    Based on Bowlby/Ainsworth attachment theory with focus on earned security
    """
    
    def __init__(self):
        super().__init__(
            agent_id="attachment-style-agent",
            name="Attachment Style Agent",
            version="1.0.0"
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize OpenAI client for AI-powered analysis
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and OPENAI_AVAILABLE:
            self.openai_client = AsyncOpenAI(api_key=api_key)
            self.ai_enabled = True
            self.logger.info("OpenAI client initialized for attachment analysis")
        else:
            self.openai_client = None
            self.ai_enabled = False
            self.logger.warning("No OpenAI API key - using rule-based attachment analysis")
        
        # Load attachment resources
        self.attachment_indicators = self._load_attachment_indicators()
        self.healing_interventions = self._load_healing_interventions()
        self.earned_security_practices = self._load_earned_security_practices()
        
    async def initialize(self) -> bool:
        """Initialize attachment style agent"""
        try:
            self.logger.info("Initializing attachment style agent")
            
            # Define capabilities
            self._capabilities = [
                AgentCapability(
                    name="assess_attachment_style",
                    description="Assess primary attachment style and patterns",
                    input_schema={"text": "string", "context": "object"},
                    output_schema={"assessment": "object"}
                ),
                AgentCapability(
                    name="analyze_relationship_patterns",
                    description="Identify recurring relationship dynamics",
                    input_schema={"relationship_description": "string"},
                    output_schema={"dynamics": "object"}
                ),
                AgentCapability(
                    name="identify_attachment_wounds",
                    description="Detect early attachment injuries",
                    input_schema={"history": "string", "patterns": "array"},
                    output_schema={"wounds": "array"}
                ),
                AgentCapability(
                    name="design_earned_security_path",
                    description="Create pathway toward secure attachment",
                    input_schema={"assessment": "object", "goals": "array"},
                    output_schema={"pathway": "object"}
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
            "assess_attachment_style", "analyze_relationship_patterns", 
            "identify_attachment_wounds", "design_earned_security_path"
        ]
        if action not in valid_actions:
            return False, f"Unknown action: {action}. Valid: {valid_actions}"
            
        return True, None
    
    async def process(self, message: AgentMessage) -> AgentResponse:
        """Process attachment style assessment request"""
        start_time = datetime.now(timezone.utc)
        
        try:
            action = message.payload.get("action")
            data = message.payload.get("data", {})
            
            if action == "assess_attachment_style":
                assessment = await self.assess_attachment_style(
                    data.get("text", ""),
                    AttachmentContext(**data.get("context", {}))
                )
                result = {"assessment": assessment.dict()}
                
            elif action == "analyze_relationship_patterns":
                dynamics = await self.analyze_relationship_patterns(
                    data.get("relationship_description", ""),
                    data.get("user_id", "unknown")
                )
                result = {"dynamics": dynamics.dict()}
                
            elif action == "identify_attachment_wounds":
                wounds = await self.identify_attachment_wounds(
                    data.get("history", ""),
                    data.get("patterns", [])
                )
                result = {"wounds": [w.dict() for w in wounds]}
                
            elif action == "design_earned_security_path":
                pathway = await self.design_earned_security_path(
                    data.get("assessment", {}),
                    data.get("goals", [])
                )
                result = {"pathway": pathway}
                
            else:
                raise ValueError(f"Unknown action: {action}")
            
            # Calculate processing confidence
            processing_confidence = 0.85
            if action == "assess_attachment_style" and isinstance(result.get('assessment'), dict):
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
    
    async def assess_attachment_style(self, text: str, context: AttachmentContext) -> AttachmentAssessment:
        """Comprehensive attachment style assessment"""
        
        assessment_id = str(uuid.uuid4())[:8]
        
        # Determine primary attachment style
        primary_style, style_certainty = await self._determine_attachment_style(text, context)
        
        # Identify secondary style if mixed patterns
        secondary_style = await self._identify_secondary_style(text, primary_style, context)
        
        # Analyze relationship dynamics
        dynamics = await self.analyze_relationship_patterns(text, context.user_id)
        
        # Construct attachment history
        attachment_history = await self._construct_attachment_history(text, context)
        
        # Identify current patterns
        current_patterns = await self._identify_current_patterns(text, primary_style)
        
        # Generate healing recommendations
        healing_recommendations = await self._generate_healing_recommendations(
            primary_style, dynamics, context
        )
        
        # Design earned security pathway
        earned_security_pathway = await self._design_earned_security_pathway(
            primary_style, dynamics, context
        )
        
        # Calculate confidence
        confidence = await self._calculate_assessment_confidence(
            primary_style, style_certainty, dynamics, context
        )
        
        return AttachmentAssessment(
            assessment_id=assessment_id,
            user_id=context.user_id,
            primary_attachment_style=primary_style,
            secondary_style=secondary_style,
            style_certainty=style_certainty,
            relationship_dynamics=dynamics,
            attachment_history=attachment_history,
            current_relationship_patterns=current_patterns,
            healing_recommendations=healing_recommendations,
            earned_security_pathway=earned_security_pathway,
            confidence=confidence
        )
    
    async def analyze_relationship_patterns(self, relationship_description: str, user_id: str) -> RelationshipDynamics:
        """Analyze recurring relationship dynamics and patterns"""
        
        dynamics_id = str(uuid.uuid4())[:8]
        
        # Identify primary patterns
        primary_patterns = await self._identify_relationship_patterns(relationship_description)
        
        # Detect activating strategies (anxious behaviors)
        activating_strategies = await self._detect_activating_strategies(relationship_description)
        
        # Detect deactivating strategies (avoidant behaviors)
        deactivating_strategies = await self._detect_deactivating_strategies(relationship_description)
        
        # Identify attachment wounds
        attachment_wounds = await self.identify_attachment_wounds(
            relationship_description, primary_patterns
        )
        
        # Identify relationship strengths
        strengths = await self._identify_relationship_strengths(relationship_description)
        
        # Identify growth edges
        growth_edges = await self._identify_growth_edges(
            primary_patterns, activating_strategies, deactivating_strategies
        )
        
        # Calculate earned security potential
        earned_security_potential = await self._calculate_earned_security_potential(
            strengths, growth_edges, attachment_wounds
        )
        
        return RelationshipDynamics(
            dynamics_id=dynamics_id,
            user_id=user_id,
            primary_patterns=primary_patterns,
            activating_strategies=activating_strategies,
            deactivating_strategies=deactivating_strategies,
            attachment_wounds=attachment_wounds,
            relationship_strengths=strengths,
            growth_edges=growth_edges,
            earned_security_potential=earned_security_potential
        )
    
    async def identify_attachment_wounds(self, history: str, patterns: List[Any]) -> List[AttachmentWound]:
        """Identify early attachment injuries from history and patterns"""
        
        wounds = []
        
        if self.ai_enabled:
            try:
                prompt = f"""
                Identify potential early attachment wounds from this history and relationship patterns.
                
                History: "{history}"
                Patterns: {[str(p) for p in patterns]}
                
                Look for indicators of:
                - Abandonment: Early loss, inconsistent caregiving, emotional unavailability
                - Engulfment: Intrusive parenting, loss of autonomy, enmeshment
                - Betrayal: Abuse, broken trust, emotional manipulation
                - Rejection: Criticism, conditional love, not being seen/valued
                - Neglect: Emotional unavailability, unmet basic needs
                
                For each wound identified, provide:
                - Developmental stage (infancy, early childhood, school age, adolescence)
                - Wound type (abandonment, engulfment, betrayal, rejection, neglect)
                - Brief description of the wound
                - How it shows up currently
                
                Format:
                Stage: [stage] | Type: [type] | Description: [description] | Current: [manifestation]
                """
                
                response = await self._make_ai_request(prompt, max_tokens=300)
                wounds = await self._parse_wounds_response(response)
                
            except Exception as e:
                self.logger.error(f"AI wound identification failed: {e}")
                wounds = await self._identify_wounds_fallback(history, patterns)
        else:
            wounds = await self._identify_wounds_fallback(history, patterns)
        
        return wounds
    
    async def design_earned_security_path(self, assessment: Dict[str, Any], goals: List[str]) -> Dict[str, Any]:
        """Design pathway toward earned security"""
        
        # Extract key information
        primary_style = assessment.get("primary_attachment_style", "secure")
        dynamics = assessment.get("relationship_dynamics", {})
        patterns = dynamics.get("primary_patterns", [])
        
        # Generate phase-based pathway
        pathway = {
            "assessment_summary": {
                "primary_style": primary_style,
                "key_patterns": patterns[:3],
                "healing_potential": dynamics.get("earned_security_potential", 5.0)
            },
            
            "phase_1_awareness": {
                "title": "Developing Awareness",
                "duration_weeks": 4,
                "objectives": [
                    "Recognize attachment patterns",
                    "Understand triggers and responses",
                    "Build emotional vocabulary"
                ],
                "practices": await self._generate_awareness_practices(primary_style)
            },
            
            "phase_2_regulation": {
                "title": "Emotional Regulation",
                "duration_weeks": 6,
                "objectives": [
                    "Develop self-soothing skills",
                    "Learn to tolerate uncomfortable emotions",
                    "Practice mindful response vs reaction"
                ],
                "practices": await self._generate_regulation_practices(primary_style)
            },
            
            "phase_3_connection": {
                "title": "Secure Connection",
                "duration_weeks": 8,
                "objectives": [
                    "Practice vulnerable communication",
                    "Set healthy boundaries",
                    "Experience earned security in relationships"
                ],
                "practices": await self._generate_connection_practices(primary_style, patterns)
            },
            
            "integration_practices": await self._generate_integration_practices(goals),
            
            "progress_markers": await self._generate_progress_markers(primary_style),
            
            "resources": {
                "books": ["Attached by Amir Levine", "Hold Me Tight by Sue Johnson"],
                "therapeutic_approaches": ["EFT", "AEDP", "Somatic Experiencing"],
                "daily_practices": ["Mindfulness", "Journaling", "Self-compassion"]
            }
        }
        
        return pathway
    
    # Core Analysis Methods
    async def _determine_attachment_style(self, text: str, context: AttachmentContext) -> Tuple[AttachmentStyle, float]:
        """Determine primary attachment style with certainty score"""
        
        if self.ai_enabled:
            try:
                prompt = f"""
                Determine the primary attachment style from this text and context.
                
                Text: "{text}"
                Relationship Status: {context.relationship_status or "Not specified"}
                Current Challenges: {context.current_challenges or "Not specified"}
                
                Attachment Styles:
                - SECURE: Comfortable with intimacy and independence, trusting, effective communication
                - ANXIOUS_PREOCCUPIED: Seeks closeness but fears abandonment, needs reassurance, relationship-focused
                - DISMISSIVE_AVOIDANT: Values independence, uncomfortable with closeness, self-reliant
                - FEARFUL_AVOIDANT: Wants relationships but fears being hurt, approach-avoidance patterns
                
                Look for indicators like:
                - How they describe relationships
                - Fears and anxieties about connection
                - Patterns of behavior in relationships
                - Attitudes toward independence vs closeness
                
                Respond with: [STYLE]|[CERTAINTY 0.0-1.0]
                Example: ANXIOUS_PREOCCUPIED|0.8
                """
                
                response = await self._make_ai_request(prompt, max_tokens=100)
                return await self._parse_style_response(response)
                
            except Exception as e:
                self.logger.error(f"AI attachment style detection failed: {e}")
                return await self._determine_style_fallback(text, context)
        else:
            return await self._determine_style_fallback(text, context)
    
    async def _identify_relationship_patterns(self, description: str) -> List[RelationshipPattern]:
        """Identify primary relationship patterns"""
        
        patterns = []
        desc_lower = description.lower()
        
        # Pattern indicators
        pattern_indicators = {
            RelationshipPattern.PURSUIT_DISTANCE: ["chase", "pull away", "pursue", "distance", "comes close then leaves"],
            RelationshipPattern.CONFLICT_AVOIDANCE: ["avoid fights", "don't argue", "sweep under rug", "peace at any cost"],
            RelationshipPattern.CARETAKING: ["take care of", "fix them", "their problems", "help everyone"],
            RelationshipPattern.BOUNDARY_ISSUES: ["can't say no", "boundaries", "too much", "overwhelmed by others"],
            RelationshipPattern.PEOPLE_PLEASING: ["please everyone", "approval", "make happy", "afraid to disappoint"],
            RelationshipPattern.ISOLATION: ["withdraw", "pull back", "alone", "don't need anyone"],
            RelationshipPattern.CONTROL_DYNAMICS: ["control", "power struggle", "my way", "have to be right"]
        }
        
        for pattern, indicators in pattern_indicators.items():
            if any(indicator in desc_lower for indicator in indicators):
                patterns.append(pattern)
        
        return patterns[:4]  # Limit to top 4 patterns
    
    async def _detect_activating_strategies(self, description: str) -> List[ActivatingStrategy]:
        """Detect anxious attachment activating strategies"""
        
        strategies = []
        desc_lower = description.lower()
        
        strategy_indicators = {
            ActivatingStrategy.PROTEST_BEHAVIOR: ["acting out", "drama", "get attention", "tantrum"],
            ActivatingStrategy.EXCESSIVE_REASSURANCE: ["need to know", "ask over and over", "constant validation"],
            ActivatingStrategy.HYPERVIGILANCE: ["watch for signs", "analyze everything", "read into"],
            ActivatingStrategy.CLINGING: ["can't be apart", "need them close", "separation anxiety"],
            ActivatingStrategy.EMOTIONAL_INTENSITY: ["extreme emotions", "over-react", "dramatic feelings"]
        }
        
        for strategy, indicators in strategy_indicators.items():
            if any(indicator in desc_lower for indicator in indicators):
                strategies.append(strategy)
        
        return strategies
    
    async def _detect_deactivating_strategies(self, description: str) -> List[DeactivatingStrategy]:
        """Detect avoidant attachment deactivating strategies"""
        
        strategies = []
        desc_lower = description.lower()
        
        strategy_indicators = {
            DeactivatingStrategy.EMOTIONAL_SHUTDOWN: ["shut down", "numb out", "turn off feelings"],
            DeactivatingStrategy.DISTANCING: ["pull away", "create space", "need distance"],
            DeactivatingStrategy.INTELLECTUALIZATION: ["think not feel", "logical", "analyze rather than feel"],
            DeactivatingStrategy.SELF_RELIANCE: ["don't need anyone", "independent", "do it myself"],
            DeactivatingStrategy.MINIMIZATION: ["not important", "doesn't matter", "no big deal"]
        }
        
        for strategy, indicators in strategy_indicators.items():
            if any(indicator in desc_lower for indicator in indicators):
                strategies.append(strategy)
        
        return strategies
    
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
    async def _determine_style_fallback(self, text: str, context: AttachmentContext) -> Tuple[AttachmentStyle, float]:
        """Rule-based attachment style determination"""
        
        text_lower = text.lower()
        
        # Style indicators
        secure_indicators = ["trust", "comfortable", "balanced", "communicate well", "healthy boundaries"]
        anxious_indicators = ["fear abandonment", "need reassurance", "clingy", "jealous", "worry about"]
        avoidant_indicators = ["independent", "don't need", "uncomfortable with closeness", "pull away"]
        fearful_indicators = ["want close but", "afraid of hurt", "push pull", "confusing feelings"]
        
        # Count indicators
        secure_score = sum(1 for ind in secure_indicators if ind in text_lower)
        anxious_score = sum(1 for ind in anxious_indicators if ind in text_lower)
        avoidant_score = sum(1 for ind in avoidant_indicators if ind in text_lower)
        fearful_score = sum(1 for ind in fearful_indicators if ind in text_lower)
        
        # Determine primary style
        scores = [
            (AttachmentStyle.SECURE, secure_score),
            (AttachmentStyle.ANXIOUS_PREOCCUPIED, anxious_score),
            (AttachmentStyle.DISMISSIVE_AVOIDANT, avoidant_score),
            (AttachmentStyle.FEARFUL_AVOIDANT, fearful_score)
        ]
        
        primary_style, max_score = max(scores, key=lambda x: x[1])
        
        # Calculate certainty
        total_score = sum(score for _, score in scores)
        certainty = (max_score / total_score) if total_score > 0 else 0.5
        
        return primary_style, min(0.9, max(0.3, certainty))
    
    async def _identify_wounds_fallback(self, history: str, patterns: List[Any]) -> List[AttachmentWound]:
        """Rule-based attachment wound identification"""
        
        wounds = []
        history_lower = history.lower()
        
        # Common wound indicators
        wound_indicators = {
            "abandonment": ["left me", "went away", "never came back", "disappeared"],
            "rejection": ["not good enough", "criticized", "pushed away", "didn't want me"],
            "engulfment": ["smothered", "no space", "controlled", "couldn't breathe"],
            "betrayal": ["lied to", "betrayed", "broken trust", "couldn't count on"],
            "neglect": ["ignored", "not there", "didn't care", "on my own"]
        }
        
        for wound_type, indicators in wound_indicators.items():
            if any(indicator in history_lower for indicator in indicators):
                wounds.append(AttachmentWound(
                    developmental_stage="childhood",  # Default
                    wound_type=wound_type,
                    impact_description=f"Early {wound_type} experiences shaped relationship patterns",
                    current_manifestation=f"Shows up as {wound_type} fears in current relationships",
                    healing_potential=7.0  # Default healing potential
                ))
        
        return wounds[:3]  # Limit to 3 most significant wounds
    
    # Response Parsing Methods
    async def _parse_style_response(self, response: str) -> Tuple[AttachmentStyle, float]:
        """Parse AI attachment style response"""
        
        try:
            if '|' in response:
                style_str, certainty_str = response.split('|')
                style_str = style_str.strip().upper()
                certainty = float(certainty_str.strip())
                
                # Map to enum
                style_mapping = {
                    "SECURE": AttachmentStyle.SECURE,
                    "ANXIOUS_PREOCCUPIED": AttachmentStyle.ANXIOUS_PREOCCUPIED,
                    "DISMISSIVE_AVOIDANT": AttachmentStyle.DISMISSIVE_AVOIDANT,
                    "FEARFUL_AVOIDANT": AttachmentStyle.FEARFUL_AVOIDANT
                }
                
                style = style_mapping.get(style_str, AttachmentStyle.SECURE)
                return style, max(0.3, min(0.95, certainty))
                
        except (ValueError, IndexError):
            pass
        
        # Fallback parsing
        response_lower = response.lower()
        if "anxious" in response_lower:
            return AttachmentStyle.ANXIOUS_PREOCCUPIED, 0.7
        elif "avoidant" in response_lower and "fearful" in response_lower:
            return AttachmentStyle.FEARFUL_AVOIDANT, 0.7
        elif "avoidant" in response_lower:
            return AttachmentStyle.DISMISSIVE_AVOIDANT, 0.7
        else:
            return AttachmentStyle.SECURE, 0.6
    
    async def _parse_wounds_response(self, response: str) -> List[AttachmentWound]:
        """Parse AI wounds response"""
        
        wounds = []
        lines = response.strip().split('\n')
        
        for line in lines:
            if '|' in line:
                try:
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 4:
                        stage = parts[0].replace('Stage:', '').strip()
                        wound_type = parts[1].replace('Type:', '').strip().lower()
                        description = parts[2].replace('Description:', '').strip()
                        current = parts[3].replace('Current:', '').strip()
                        
                        wounds.append(AttachmentWound(
                            developmental_stage=stage,
                            wound_type=wound_type,
                            impact_description=description,
                            current_manifestation=current,
                            healing_potential=7.0  # Default
                        ))
                        
                except (ValueError, IndexError):
                    continue
        
        return wounds[:3]  # Limit to 3 wounds
    
    # Helper Methods for Assessment
    async def _identify_secondary_style(self, text: str, primary: AttachmentStyle, 
                                       context: AttachmentContext) -> Optional[AttachmentStyle]:
        """Identify secondary attachment style if mixed patterns present"""
        
        # Look for contradictory patterns
        text_lower = text.lower()
        
        # If primary is secure, unlikely to have strong secondary
        if primary == AttachmentStyle.SECURE:
            return None
        
        # Common mixed patterns
        if primary == AttachmentStyle.ANXIOUS_PREOCCUPIED:
            avoidant_indicators = ["need space", "pull away", "overwhelmed by closeness"]
            if any(ind in text_lower for ind in avoidant_indicators):
                return AttachmentStyle.FEARFUL_AVOIDANT
                
        elif primary == AttachmentStyle.DISMISSIVE_AVOIDANT:
            anxious_indicators = ["but want closeness", "lonely", "miss connection"]
            if any(ind in text_lower for ind in anxious_indicators):
                return AttachmentStyle.FEARFUL_AVOIDANT
        
        return None
    
    async def _construct_attachment_history(self, text: str, context: AttachmentContext) -> Dict[str, Any]:
        """Construct attachment history from available information"""
        
        return {
            "early_caregiving": "Information not provided" if not context.family_history else context.family_history.get("caregiving", "Unknown"),
            "family_dynamics": context.family_history.get("dynamics", "Not specified") if context.family_history else "Not specified",
            "significant_relationships": context.previous_relationships or [],
            "therapeutic_history": context.therapy_history or False,
            "cultural_influences": context.cultural_background or "Not specified"
        }
    
    async def _identify_current_patterns(self, text: str, style: AttachmentStyle) -> List[str]:
        """Identify current relationship patterns based on style"""
        
        style_patterns = {
            AttachmentStyle.SECURE: [
                "Communicates needs clearly",
                "Comfortable with interdependence", 
                "Handles conflict constructively"
            ],
            AttachmentStyle.ANXIOUS_PREOCCUPIED: [
                "Seeks frequent reassurance",
                "Fear of abandonment influences decisions",
                "Tends to over-analyze relationship dynamics"
            ],
            AttachmentStyle.DISMISSIVE_AVOIDANT: [
                "Maintains emotional distance",
                "Prioritizes independence over connection",
                "Difficulty with vulnerability"
            ],
            AttachmentStyle.FEARFUL_AVOIDANT: [
                "Approach-avoidance patterns in relationships",
                "Wants closeness but fears being hurt",
                "Inconsistent relationship behavior"
            ]
        }
        
        return style_patterns.get(style, ["General relationship patterns present"])
    
    async def _generate_healing_recommendations(self, style: AttachmentStyle, 
                                              dynamics: RelationshipDynamics, 
                                              context: AttachmentContext) -> List[str]:
        """Generate specific healing recommendations"""
        
        recommendations = []
        
        # Style-specific recommendations
        style_recommendations = {
            AttachmentStyle.ANXIOUS_PREOCCUPIED: [
                "Practice self-soothing techniques for anxiety",
                "Develop secure self-relationship",
                "Learn to tolerate uncertainty in relationships"
            ],
            AttachmentStyle.DISMISSIVE_AVOIDANT: [
                "Practice emotional awareness and expression",
                "Gradually increase vulnerability with trusted others",
                "Explore fears of intimacy and dependence"
            ],
            AttachmentStyle.FEARFUL_AVOIDANT: [
                "Work on emotional regulation skills",
                "Address trauma underlying fear patterns",
                "Practice staying present during relationship triggers"
            ],
            AttachmentStyle.SECURE: [
                "Continue developing healthy communication skills",
                "Support others in their attachment healing",
                "Maintain secure practices during stress"
            ]
        }
        
        recommendations.extend(style_recommendations.get(style, []))
        
        # Add wound-specific recommendations
        for wound in dynamics.attachment_wounds:
            if wound.wound_type == "abandonment":
                recommendations.append("Address abandonment fears through secure relationships")
            elif wound.wound_type == "rejection":
                recommendations.append("Practice self-acceptance and worthiness work")
        
        return recommendations[:5]  # Limit to top 5
    
    async def _design_earned_security_pathway(self, style: AttachmentStyle, 
                                            dynamics: RelationshipDynamics,
                                            context: AttachmentContext) -> List[str]:
        """Design pathway toward earned security"""
        
        pathway = [
            "Develop awareness of attachment patterns and triggers",
            "Practice emotional regulation and self-soothing",
            "Build capacity for healthy vulnerability",
            "Cultivate secure relationships and support systems",
            "Integrate new secure behaviors into daily life"
        ]
        
        # Customize based on style
        if style == AttachmentStyle.ANXIOUS_PREOCCUPIED:
            pathway.insert(1, "Learn to self-validate rather than seeking external reassurance")
        elif style == AttachmentStyle.DISMISSIVE_AVOIDANT:
            pathway.insert(2, "Gradually increase comfort with emotional intimacy")
        elif style == AttachmentStyle.FEARFUL_AVOIDANT:
            pathway.insert(1, "Address underlying trauma that drives fear patterns")
        
        return pathway
    
    # Progress and Practice Generation Methods
    async def _generate_awareness_practices(self, style: AttachmentStyle) -> List[str]:
        """Generate awareness-building practices"""
        
        base_practices = [
            "Daily attachment pattern journaling",
            "Trigger identification exercises",
            "Mindfulness of relationship emotions"
        ]
        
        if style == AttachmentStyle.ANXIOUS_PREOCCUPIED:
            base_practices.append("Notice when seeking reassurance vs self-soothing")
        elif style == AttachmentStyle.DISMISSIVE_AVOIDANT:
            base_practices.append("Track moments of emotional shutdown or distancing")
        
        return base_practices
    
    async def _generate_regulation_practices(self, style: AttachmentStyle) -> List[str]:
        """Generate emotional regulation practices"""
        
        base_practices = [
            "Breathing exercises for emotional activation",
            "Self-compassion practices",
            "Progressive muscle relaxation"
        ]
        
        if style == AttachmentStyle.ANXIOUS_PREOCCUPIED:
            base_practices.extend([
                "Anxiety tolerance exercises",
                "Self-soothing toolkit development"
            ])
        elif style == AttachmentStyle.DISMISSIVE_AVOIDANT:
            base_practices.extend([
                "Emotional awareness meditation",
                "Gradual vulnerability exercises"
            ])
        
        return base_practices
    
    async def _generate_connection_practices(self, style: AttachmentStyle, 
                                           patterns: List[RelationshipPattern]) -> List[str]:
        """Generate secure connection practices"""
        
        base_practices = [
            "Vulnerable communication exercises",
            "Healthy boundary setting practice",
            "Conflict resolution skill building"
        ]
        
        # Add pattern-specific practices
        if RelationshipPattern.PEOPLE_PLEASING in patterns:
            base_practices.append("Practice saying no with kindness")
        if RelationshipPattern.CONFLICT_AVOIDANCE in patterns:
            base_practices.append("Gentle conflict engagement exercises")
        
        return base_practices
    
    async def _generate_integration_practices(self, goals: List[str]) -> List[str]:
        """Generate integration practices based on goals"""
        
        practices = [
            "Weekly relationship check-ins with self",
            "Monthly progress reflection",
            "Secure relationship modeling"
        ]
        
        # Customize based on goals
        if "improve communication" in str(goals).lower():
            practices.append("Daily conscious communication practice")
        if "build trust" in str(goals).lower():
            practices.append("Trust-building exercises with safe people")
        
        return practices
    
    async def _generate_progress_markers(self, style: AttachmentStyle) -> List[str]:
        """Generate progress markers for earned security"""
        
        universal_markers = [
            "Increased emotional regulation during relationship stress",
            "Clearer communication of needs and boundaries",
            "Greater comfort with interdependence",
            "Reduced activation of old attachment patterns"
        ]
        
        # Add style-specific markers
        if style == AttachmentStyle.ANXIOUS_PREOCCUPIED:
            universal_markers.append("Decreased need for constant reassurance")
        elif style == AttachmentStyle.DISMISSIVE_AVOIDANT:
            universal_markers.append("Increased comfort with emotional intimacy")
        elif style == AttachmentStyle.FEARFUL_AVOIDANT:
            universal_markers.append("More consistent relationship behavior")
        
        return universal_markers
    
    # Assessment Helper Methods
    async def _identify_relationship_strengths(self, description: str) -> List[str]:
        """Identify relationship strengths and positive patterns"""
        
        desc_lower = description.lower()
        
        strength_indicators = {
            "communication": ["talk openly", "express feelings", "listen well"],
            "trust": ["trust", "reliable", "count on"],
            "support": ["support", "there for", "help each other"],
            "respect": ["respect", "boundaries", "space"],
            "growth": ["learn", "grow together", "work on"]
        }
        
        strengths = []
        for strength, indicators in strength_indicators.items():
            if any(indicator in desc_lower for indicator in indicators):
                strengths.append(f"Shows capacity for {strength}")
        
        return strengths if strengths else ["Basic relationship engagement present"]
    
    async def _identify_growth_edges(self, patterns: List[RelationshipPattern],
                                   activating: List[ActivatingStrategy],
                                   deactivating: List[DeactivatingStrategy]) -> List[str]:
        """Identify areas for growth and development"""
        
        growth_edges = []
        
        # Pattern-based growth edges
        pattern_growth = {
            RelationshipPattern.CONFLICT_AVOIDANCE: "Learning healthy conflict engagement",
            RelationshipPattern.PEOPLE_PLEASING: "Developing authentic self-expression",
            RelationshipPattern.BOUNDARY_ISSUES: "Strengthening personal boundaries",
            RelationshipPattern.ISOLATION: "Building capacity for connection"
        }
        
        for pattern in patterns:
            if pattern in pattern_growth:
                growth_edges.append(pattern_growth[pattern])
        
        # Strategy-based growth edges
        if activating:
            growth_edges.append("Developing self-soothing capacity")
        if deactivating:
            growth_edges.append("Increasing emotional availability")
        
        return growth_edges[:4]  # Limit to top 4
    
    async def _calculate_earned_security_potential(self, strengths: List[str], 
                                                 growth_edges: List[str],
                                                 wounds: List[AttachmentWound]) -> float:
        """Calculate potential for developing earned security"""
        
        base_potential = 7.0  # Base assumption of human capacity for growth
        
        # Increase potential based on strengths
        base_potential += len(strengths) * 0.3
        
        # Consider wound healing potential
        if wounds:
            avg_wound_healing = sum(w.healing_potential for w in wounds) / len(wounds)
            base_potential += (avg_wound_healing - 5.0) * 0.2
        
        # Growth edges indicate areas for development
        base_potential += len(growth_edges) * 0.1
        
        return max(3.0, min(10.0, base_potential))
    
    async def _calculate_assessment_confidence(self, style: AttachmentStyle, 
                                             style_certainty: float,
                                             dynamics: RelationshipDynamics, 
                                             context: AttachmentContext) -> float:
        """Calculate confidence in attachment assessment"""
        
        base_confidence = 0.75
        
        # Style certainty contributes
        base_confidence += (style_certainty - 0.5) * 0.2
        
        # More information increases confidence
        if context.relationship_status:
            base_confidence += 0.05
        if context.family_history:
            base_confidence += 0.05
        if context.previous_relationships:
            base_confidence += 0.05
        
        # Pattern identification increases confidence
        base_confidence += len(dynamics.primary_patterns) * 0.02
        
        # AI vs fallback
        if self.ai_enabled:
            base_confidence += 0.05
        
        return max(0.5, min(0.95, base_confidence))
    
    # Resource Loading Methods
    def _load_attachment_indicators(self) -> Dict[str, List[str]]:
        """Load attachment style indicators"""
        return {
            "secure": ["trust", "comfortable", "communicate", "balanced", "interdependent"],
            "anxious": ["fear abandonment", "need reassurance", "preoccupied", "clingy"],
            "avoidant": ["independent", "uncomfortable closeness", "self-reliant", "distant"],
            "fearful": ["want but fear", "push-pull", "inconsistent", "confused about love"]
        }
    
    def _load_healing_interventions(self) -> Dict[str, List[str]]:
        """Load healing interventions by attachment style"""
        return {
            "anxious": ["Self-soothing", "Emotional regulation", "Secure self-relationship"],
            "avoidant": ["Emotional awareness", "Vulnerability practice", "Intimacy tolerance"],
            "fearful": ["Trauma healing", "Safety building", "Consistent self-care"],
            "secure": ["Maintain practices", "Support others", "Deepen connections"]
        }
    
    def _load_earned_security_practices(self) -> List[str]:
        """Load earned security development practices"""
        return [
            "Mindfulness meditation for relationship awareness",
            "Journaling relationship patterns and triggers",
            "Gradual vulnerability exercises with safe people",
            "Emotional regulation skill development",
            "Secure relationship modeling and practice",
            "Self-compassion and worthiness work",
            "Healthy boundary setting and maintenance"
        ]