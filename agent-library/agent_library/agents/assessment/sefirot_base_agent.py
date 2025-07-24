"""
Sefirot Base Agent for DPNR Platform
Foundation class for implementing the 10 Sefirot as therapeutic agents
Bridges mystical framework with multi-agent therapeutic logic
Generated for Phase 1 Sefirot Integration
"""
import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from pydantic import BaseModel, Field, validator
from enum import Enum
import uuid

from ...core.base_agent import BaseAgent, AgentMessage, AgentResponse, AgentCapability
from ...core.message_types import MessageType, PersonalityScore


class SefirotType(str, Enum):
    """10 Sefirot mapped to therapeutic agent specializations"""
    # Upper Triad - Divine Intelligence
    KETER = "keter"           # Crown - Universal breakthrough catalyst
    CHOCHMAH = "chochmah"     # Wisdom - Insight generation/pattern recognition
    BINAH = "binah"           # Understanding - Deep comprehension/integration
    
    # Middle Triad - Emotional Processing  
    CHESED = "chesed"         # Compassion - Loving-kindness/healing facilitation
    GEVURAH = "gevurah"       # Strength - Boundaries/discipline/shadow work
    TIFERET = "tiferet"       # Beauty - Balance/harmony/aesthetic integration
    
    # Lower Triad - Practical Implementation
    NETZACH = "netzach"       # Victory - Persistence/creative expression
    HOD = "hod"               # Glory - Communication/teaching/sharing
    YESOD = "yesod"           # Foundation - Grounding/practical application
    MALCHUT = "malchut"       # Kingdom - Manifestation/real-world integration


class SefirotFlow(str, Enum):
    """Sefirot energy flow directions in therapeutic processing"""
    DESCENDING = "descending"  # From Keter down to Malchut (divine to practical)
    ASCENDING = "ascending"    # From Malchut up to Keter (practical to divine)
    BALANCING = "balancing"    # Between pillars (severity/mercy/balance)
    LIGHTNING = "lightning"    # Lightning flash pattern (full tree activation)


class SefirotAttribute(BaseModel):
    """Attributes associated with each Sefirot"""
    sefirot_type: SefirotType
    pillar: str  # "severity", "mercy", "balance"
    level: str   # "supernal", "emotional", "practical"
    divine_name: str  # Hebrew divine name associated
    therapeutic_focus: str  # Primary therapeutic function
    soul_level_affinity: List[str]  # Which soul levels it serves best
    integration_patterns: List[str]  # How it integrates with other sefirot


class SefirotActivation(BaseModel):
    """Represents activation of a Sefirot in therapeutic process"""
    activation_id: str
    sefirot_type: SefirotType
    user_id: str
    session_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    trigger_context: Dict[str, Any]  # What triggered this sefirot
    activation_intensity: float = Field(ge=0.0, le=1.0)  # How strongly activated
    therapeutic_intent: str  # Intended therapeutic outcome
    
    connected_sefirot: List[SefirotType] = Field(default_factory=list)  # Other activated sefirot
    flow_pattern: SefirotFlow = SefirotFlow.DESCENDING
    
    processing_duration: Optional[float] = None
    therapeutic_outcome: Optional[Dict[str, Any]] = None


class SefirotResponse(BaseModel):
    """Response from Sefirot agent processing"""
    sefirot_type: SefirotType
    response_content: str
    therapeutic_insights: List[str]
    integration_guidance: List[str]
    
    confidence: float = Field(ge=0.0, le=1.0)
    depth_level: str  # "surface", "intermediate", "deep", "mystical"
    
    next_sefirot_recommendations: List[SefirotType] = Field(default_factory=list)
    soul_level_resonance: Optional[str] = None
    
    metaphors: List[str] = Field(default_factory=list)
    symbols: List[str] = Field(default_factory=list)


class SefirotAgent(BaseAgent):
    """
    Base class for all Sefirot agents
    Provides common sefirot functionality and therapeutic integration patterns
    """
    
    def __init__(self, sefirot_type: SefirotType, agent_id: str = None, name: str = None):
        if not agent_id:
            agent_id = f"{sefirot_type.value}-agent"
        if not name:
            name = f"{sefirot_type.value.title()} Sefirot Agent"
            
        super().__init__(
            agent_id=agent_id,
            name=name,
            version="1.0.0"
        )
        
        self.sefirot_type = sefirot_type
        self.sefirot_attributes = self._initialize_sefirot_attributes()
        self.logger = logging.getLogger(__name__)
        self.active_activations: Dict[str, SefirotActivation] = {}
        
    def _initialize_sefirot_attributes(self) -> SefirotAttribute:
        """Initialize attributes for this sefirot type"""
        sefirot_config = {
            SefirotType.KETER: {
                "pillar": "balance", "level": "supernal",
                "divine_name": "Ehyeh", "therapeutic_focus": "Universal breakthrough catalyst",
                "soul_level_affinity": ["yechida", "chayah"], 
                "integration_patterns": ["crown_activation", "unity_consciousness"]
            },
            SefirotType.CHOCHMAH: {
                "pillar": "mercy", "level": "supernal", 
                "divine_name": "Yah", "therapeutic_focus": "Insight generation and pattern recognition",
                "soul_level_affinity": ["chayah", "neshamah"],
                "integration_patterns": ["wisdom_flash", "intuitive_knowing"]
            },
            SefirotType.BINAH: {
                "pillar": "severity", "level": "supernal",
                "divine_name": "YHVH Elohim", "therapeutic_focus": "Deep comprehension and integration", 
                "soul_level_affinity": ["neshamah", "ruach"],
                "integration_patterns": ["understanding_depth", "analytical_processing"]
            },
            SefirotType.CHESED: {
                "pillar": "mercy", "level": "emotional",
                "divine_name": "El", "therapeutic_focus": "Loving-kindness and healing facilitation",
                "soul_level_affinity": ["ruach", "neshamah"],
                "integration_patterns": ["compassionate_flow", "healing_embrace"]
            },
            SefirotType.GEVURAH: {
                "pillar": "severity", "level": "emotional", 
                "divine_name": "Elohim", "therapeutic_focus": "Boundaries, discipline, and shadow work",
                "soul_level_affinity": ["ruach", "nefesh"],
                "integration_patterns": ["protective_boundary", "shadow_integration"]
            },
            SefirotType.TIFERET: {
                "pillar": "balance", "level": "emotional",
                "divine_name": "YHVH", "therapeutic_focus": "Balance, harmony, and aesthetic integration",
                "soul_level_affinity": ["ruach", "neshamah", "nefesh"],
                "integration_patterns": ["harmonic_balance", "beauty_synthesis"]
            },
            SefirotType.NETZACH: {
                "pillar": "mercy", "level": "practical",
                "divine_name": "YHVH Tzevaot", "therapeutic_focus": "Persistence and creative expression", 
                "soul_level_affinity": ["nefesh", "ruach"],
                "integration_patterns": ["creative_victory", "persistent_flow"]
            },
            SefirotType.HOD: {
                "pillar": "severity", "level": "practical",
                "divine_name": "Elohim Tzevaot", "therapeutic_focus": "Communication and teaching",
                "soul_level_affinity": ["nefesh", "ruach"], 
                "integration_patterns": ["structured_glory", "communicative_precision"]
            },
            SefirotType.YESOD: {
                "pillar": "balance", "level": "practical",
                "divine_name": "Shaddai El Chai", "therapeutic_focus": "Grounding and practical application",
                "soul_level_affinity": ["nefesh", "ruach"],
                "integration_patterns": ["foundation_grounding", "practical_synthesis"]
            },
            SefirotType.MALCHUT: {
                "pillar": "balance", "level": "practical", 
                "divine_name": "Adonai", "therapeutic_focus": "Manifestation and real-world integration",
                "soul_level_affinity": ["nefesh"],
                "integration_patterns": ["worldly_manifestation", "practical_kingdom"]
            }
        }
        
        config = sefirot_config.get(self.sefirot_type, sefirot_config[SefirotType.MALCHUT])
        
        return SefirotAttribute(
            sefirot_type=self.sefirot_type,
            pillar=config["pillar"],
            level=config["level"], 
            divine_name=config["divine_name"],
            therapeutic_focus=config["therapeutic_focus"],
            soul_level_affinity=config["soul_level_affinity"],
            integration_patterns=config["integration_patterns"]
        )
    
    async def initialize(self) -> bool:
        """Initialize Sefirot agent with base capabilities"""
        try:
            self.logger.info(f"Initializing {self.sefirot_type.value} Sefirot Agent")
            
            self._capabilities = [
                AgentCapability(
                    name="activate_sefirot",
                    description=f"Activate {self.sefirot_type.value} sefirot for therapeutic processing",
                    input_schema={"context": "object", "intensity": "float", "soul_level": "string"},
                    output_schema={"activation": "object", "response": "object"}
                ),
                AgentCapability(
                    name="process_therapeutic_request",
                    description=f"Process therapeutic request through {self.sefirot_type.value} lens",
                    input_schema={"user_input": "string", "context": "object"},
                    output_schema={"response": "object", "insights": "array"}
                ),
                AgentCapability(
                    name="integrate_with_sefirot",
                    description=f"Integrate {self.sefirot_type.value} with other sefirot",
                    input_schema={"connected_sefirot": "array", "flow_pattern": "string"},
                    output_schema={"integration": "object"}
                ),
                AgentCapability(
                    name="generate_sefirot_insights",
                    description=f"Generate therapeutic insights from {self.sefirot_type.value} perspective",
                    input_schema={"context": "object", "depth_level": "string"},
                    output_schema={"insights": "array", "guidance": "array"}
                )
            ]
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize {self.sefirot_type.value} agent: {e}")
            return False
    
    def get_capabilities(self) -> List[AgentCapability]:
        """Return sefirot agent capabilities"""
        return self._capabilities
    
    async def validate_input(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate input data for sefirot processing"""
        required_fields = {"action", "data"}
        if not all(field in data for field in required_fields):
            return False, f"Missing required fields: {required_fields}"
        
        action = data.get("action")
        valid_actions = ["activate_sefirot", "process_therapeutic_request", 
                        "integrate_with_sefirot", "generate_sefirot_insights"]
        if action not in valid_actions:
            return False, f"Unknown action: {action}. Valid actions: {valid_actions}"
            
        return True, None
    
    async def process(self, message: AgentMessage) -> AgentResponse:
        """Process sefirot therapeutic request"""
        start_time = datetime.utcnow()
        
        try:
            action = message.payload.get("action")
            data = message.payload.get("data", {})
            
            if action == "activate_sefirot":
                result = await self.activate_sefirot(
                    context=data.get("context", {}),
                    intensity=data.get("intensity", 0.7),
                    soul_level=data.get("soul_level", "nefesh")
                )
                
            elif action == "process_therapeutic_request":
                result = await self.process_therapeutic_request(
                    user_input=data.get("user_input", ""),
                    context=data.get("context", {})
                )
                
            elif action == "integrate_with_sefirot":
                result = await self.integrate_with_sefirot(
                    connected_sefirot=data.get("connected_sefirot", []),
                    flow_pattern=data.get("flow_pattern", "descending")
                )
                
            elif action == "generate_sefirot_insights":
                result = await self.generate_sefirot_insights(
                    context=data.get("context", {}),
                    depth_level=data.get("depth_level", "intermediate")
                )
                
            else:
                raise ValueError(f"Unknown action: {action}")
            
            confidence = self._calculate_confidence(result)
            
            return AgentResponse(
                success=True,
                data=result,
                processing_time=(datetime.utcnow() - start_time).total_seconds(),
                agent_id=self.agent_id,
                confidence=confidence
            )
            
        except Exception as e:
            self.logger.error(f"Sefirot processing failed: {e}")
            return AgentResponse(
                success=False,
                error=str(e),
                processing_time=(datetime.utcnow() - start_time).total_seconds(),
                agent_id=self.agent_id
            )
    
    async def activate_sefirot(self, context: Dict[str, Any], intensity: float = 0.7, 
                             soul_level: str = "nefesh") -> Dict[str, Any]:
        """Activate this sefirot for therapeutic processing"""
        
        activation_id = str(uuid.uuid4())
        user_id = context.get("user_id", "unknown")
        session_id = context.get("session_id")
        
        # Create activation record
        activation = SefirotActivation(
            activation_id=activation_id,
            sefirot_type=self.sefirot_type,
            user_id=user_id,
            session_id=session_id,
            trigger_context=context,
            activation_intensity=intensity,
            therapeutic_intent=await self._determine_therapeutic_intent(context, soul_level),
            flow_pattern=await self._determine_flow_pattern(context)
        )
        
        # Store activation
        self.active_activations[activation_id] = activation
        
        # Generate sefirot response
        response = await self._generate_sefirot_response(activation, context, soul_level)
        
        self.logger.info(f"Activated {self.sefirot_type.value} sefirot: {activation.therapeutic_intent}")
        
        return {
            "activation_id": activation_id,
            "sefirot_type": self.sefirot_type.value,
            "intensity": intensity,
            "therapeutic_intent": activation.therapeutic_intent,
            "response": response.dict(),
            "activated_at": activation.timestamp.isoformat()
        }
    
    async def process_therapeutic_request(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process therapeutic request through sefirot lens"""
        
        # Activate sefirot for processing
        soul_level = context.get("soul_level", "nefesh")
        activation_result = await self.activate_sefirot(context, intensity=0.8, soul_level=soul_level)
        
        # Generate therapeutic processing
        processing_result = await self._process_through_sefirot_lens(user_input, context)
        
        # Create integrated response
        return {
            "sefirot_type": self.sefirot_type.value,
            "user_input_processed": user_input,
            "therapeutic_response": processing_result["response"],
            "insights": processing_result["insights"], 
            "integration_guidance": processing_result["guidance"],
            "activation": activation_result,
            "processing_depth": processing_result.get("depth_level", "intermediate"),
            "confidence": processing_result.get("confidence", 0.8)
        }
    
    async def integrate_with_sefirot(self, connected_sefirot: List[str], 
                                   flow_pattern: str = "descending") -> Dict[str, Any]:
        """Integrate this sefirot with other sefirot in the tree"""
        
        try:
            flow = SefirotFlow(flow_pattern)
        except ValueError:
            flow = SefirotFlow.DESCENDING
        
        # Convert string sefirot to SefirotType
        connected_types = []
        for sefirot_str in connected_sefirot:
            try:
                connected_types.append(SefirotType(sefirot_str))
            except ValueError:
                continue
        
        # Generate integration patterns
        integration_patterns = await self._generate_integration_patterns(connected_types, flow)
        
        return {
            "source_sefirot": self.sefirot_type.value,
            "connected_sefirot": [s.value for s in connected_types],
            "flow_pattern": flow.value,
            "integration_patterns": integration_patterns,
            "therapeutic_synergies": await self._identify_therapeutic_synergies(connected_types),
            "recommended_sequence": await self._recommend_activation_sequence(connected_types, flow)
        }
    
    async def generate_sefirot_insights(self, context: Dict[str, Any], 
                                      depth_level: str = "intermediate") -> Dict[str, Any]:
        """Generate therapeutic insights from sefirot perspective"""
        
        insights = await self._generate_therapeutic_insights(context, depth_level)
        metaphors = await self._generate_sefirot_metaphors(context, depth_level)
        symbols = await self._generate_sefirot_symbols(context)
        
        return {
            "sefirot_type": self.sefirot_type.value,
            "therapeutic_focus": self.sefirot_attributes.therapeutic_focus,
            "insights": insights,
            "metaphors": metaphors,
            "symbols": symbols,
            "depth_level": depth_level,
            "soul_level_resonance": await self._determine_soul_level_resonance(context),
            "integration_opportunities": await self._identify_integration_opportunities(context),
            "generated_at": datetime.utcnow().isoformat()
        }
    
    # Abstract methods to be implemented by specific sefirot agents
    
    async def _determine_therapeutic_intent(self, context: Dict[str, Any], soul_level: str) -> str:
        """Determine therapeutic intent based on sefirot specialization"""
        # Base implementation - override in specific sefirot agents
        return f"{self.sefirot_attributes.therapeutic_focus} for {soul_level} level"
    
    async def _determine_flow_pattern(self, context: Dict[str, Any]) -> SefirotFlow:
        """Determine appropriate flow pattern for context"""
        # Base implementation - can be overridden
        return SefirotFlow.DESCENDING
    
    async def _generate_sefirot_response(self, activation: SefirotActivation, 
                                       context: Dict[str, Any], soul_level: str) -> SefirotResponse:
        """Generate sefirot-specific therapeutic response"""
        # Base implementation - override in specific sefirot agents
        return SefirotResponse(
            sefirot_type=self.sefirot_type,
            response_content=f"Activated {self.sefirot_type.value} for therapeutic processing",
            therapeutic_insights=[f"Insights from {self.sefirot_type.value} perspective"],
            integration_guidance=[f"Guidance for integrating {self.sefirot_type.value} energy"],
            confidence=0.7,
            depth_level=soul_level
        )
    
    async def _process_through_sefirot_lens(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process user input through this sefirot's therapeutic lens"""
        # Base implementation - override in specific sefirot agents  
        return {
            "response": f"Processed through {self.sefirot_type.value} lens: {user_input[:100]}...",
            "insights": [f"Insight from {self.sefirot_type.value} perspective"],
            "guidance": [f"Guidance from {self.sefirot_type.value}"],
            "depth_level": "intermediate",
            "confidence": 0.7
        }
    
    # Helper methods
    
    async def _generate_integration_patterns(self, connected_sefirot: List[SefirotType], 
                                           flow: SefirotFlow) -> List[str]:
        """Generate integration patterns with other sefirot"""
        patterns = []
        for sefirot in connected_sefirot:
            pattern = f"{self.sefirot_type.value}-{sefirot.value}-{flow.value}"
            patterns.append(pattern)
        return patterns
    
    async def _identify_therapeutic_synergies(self, connected_sefirot: List[SefirotType]) -> List[str]:
        """Identify therapeutic synergies with connected sefirot"""
        synergies = []
        for sefirot in connected_sefirot:
            synergy = f"Synergy between {self.sefirot_type.value} and {sefirot.value}"
            synergies.append(synergy)
        return synergies
    
    async def _recommend_activation_sequence(self, connected_sefirot: List[SefirotType], 
                                           flow: SefirotFlow) -> List[str]:
        """Recommend activation sequence for connected sefirot"""
        if flow == SefirotFlow.DESCENDING:
            # Order from top to bottom of tree
            sequence = sorted([self.sefirot_type] + connected_sefirot, 
                            key=lambda s: list(SefirotType).index(s))
        else:
            # Reverse order for ascending
            sequence = sorted([self.sefirot_type] + connected_sefirot, 
                            key=lambda s: list(SefirotType).index(s), reverse=True)
        
        return [s.value for s in sequence]
    
    async def _generate_therapeutic_insights(self, context: Dict[str, Any], depth_level: str) -> List[str]:
        """Generate therapeutic insights for this sefirot"""
        # Base implementation - override in specific agents
        return [
            f"Insight from {self.sefirot_type.value}: {self.sefirot_attributes.therapeutic_focus}",
            f"Focus area: {self.sefirot_attributes.pillar} pillar energy",
            f"Operating at {self.sefirot_attributes.level} level"
        ]
    
    async def _generate_sefirot_metaphors(self, context: Dict[str, Any], depth_level: str) -> List[str]:
        """Generate metaphors appropriate for this sefirot"""
        # Base metaphor system - can be overridden
        metaphor_base = {
            SefirotType.KETER: ["crown of consciousness", "divine spark", "unity source"],
            SefirotType.CHOCHMAH: ["flash of wisdom", "lightning insight", "primordial point"],
            SefirotType.BINAH: ["womb of understanding", "palace of comprehension", "structured wisdom"],
            SefirotType.CHESED: ["flowing river of compassion", "open heart embrace", "boundless love"],
            SefirotType.GEVURAH: ["protective boundary", "disciplined strength", "refined fire"],
            SefirotType.TIFERET: ["golden harmony", "balanced beauty", "heart center radiance"],
            SefirotType.NETZACH: ["persistent flame", "creative victory", "enduring flow"],
            SefirotType.HOD: ["structured communication", "precise expression", "organized glory"],
            SefirotType.YESOD: ["solid foundation", "grounding root", "practical synthesis"],
            SefirotType.MALCHUT: ["earthly kingdom", "manifested reality", "practical vessel"]
        }
        
        return metaphor_base.get(self.sefirot_type, ["spiritual energy", "divine attribute"])
    
    async def _generate_sefirot_symbols(self, context: Dict[str, Any]) -> List[str]:
        """Generate symbols associated with this sefirot"""
        # Base symbol system
        symbol_base = {
            SefirotType.KETER: ["crown", "point", "unity_circle"],
            SefirotType.CHOCHMAH: ["lightning", "spark", "wisdom_eye"],
            SefirotType.BINAH: ["palace", "womb", "understanding_cup"],
            SefirotType.CHESED: ["water", "cup_overflowing", "open_arms"],
            SefirotType.GEVURAH: ["sword", "fire", "protective_shield"],
            SefirotType.TIFERET: ["sun", "heart", "golden_ratio"],
            SefirotType.NETZACH: ["pillar", "victory_laurel", "eternal_flame"],
            SefirotType.HOD: ["mountain", "structured_crystal", "communication_tower"],
            SefirotType.YESOD: ["foundation_stone", "moon", "connecting_bridge"],
            SefirotType.MALCHUT: ["earth", "kingdom_crown", "practical_tools"]
        }
        
        return symbol_base.get(self.sefirot_type, ["divine_symbol"])
    
    async def _determine_soul_level_resonance(self, context: Dict[str, Any]) -> Optional[str]:
        """Determine which soul level this sefirot resonates with for this context"""
        user_soul_level = context.get("soul_level")
        if user_soul_level in self.sefirot_attributes.soul_level_affinity:
            return user_soul_level
        
        # Return closest affinity
        if self.sefirot_attributes.soul_level_affinity:
            return self.sefirot_attributes.soul_level_affinity[0]
        
        return None
    
    async def _identify_integration_opportunities(self, context: Dict[str, Any]) -> List[str]:
        """Identify opportunities for integrating this sefirot"""
        opportunities = []
        
        # Add integration patterns from attributes
        for pattern in self.sefirot_attributes.integration_patterns:
            opportunities.append(f"Opportunity for {pattern} integration")
        
        # Add context-specific opportunities
        if context.get("therapeutic_focus"):
            opportunities.append(f"Integration with {context['therapeutic_focus']} work")
        
        return opportunities
    
    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """Calculate confidence score for sefirot processing"""
        if "error" in result:
            return 0.3
        
        base_confidence = 0.75
        
        # Increase confidence with more complete results
        if "therapeutic_response" in result:
            base_confidence += 0.05
        if "insights" in result and len(result["insights"]) > 0:
            base_confidence += 0.05
        if "activation" in result:
            base_confidence += 0.05
        if result.get("processing_depth") == "deep":
            base_confidence += 0.1
        
        return min(1.0, base_confidence)
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for sefirot agent"""
        return {
            "agent_id": self.agent_id,
            "sefirot_type": self.sefirot_type.value,
            "status": "healthy",
            "active_activations": len(self.active_activations),
            "therapeutic_focus": self.sefirot_attributes.therapeutic_focus,
            "pillar": self.sefirot_attributes.pillar,
            "level": self.sefirot_attributes.level,
            "capabilities": len(self._capabilities)
        }