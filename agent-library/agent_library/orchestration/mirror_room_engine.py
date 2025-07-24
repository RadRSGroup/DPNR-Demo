"""
Mirror Room Orchestration Engine for DPNR Platform
Coordinates IFS and Shadow Work agents for reflective therapeutic dialogue

This engine represents the core DPNR therapeutic experience, managing
multi-agent sessions with depth progression and safety protocols.
"""
import asyncio
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from pydantic import BaseModel, Field, validator
from enum import Enum

from ..core.base_agent import BaseAgent, AgentMessage, AgentResponse
from ..agents.assessment.ifs_agent import IFSAgent, IFSPart, DialogueResponse
from ..agents.assessment.shadow_work_agent import ShadowWorkAgent, ShadowPattern, IntegrationGuidance
from ..agents.assessment.pardes_reflection_agent import PaRDeSReflectionAgent, PaRDeSReflection, ReflectionContext


class SessionDepth(str, Enum):
    """Mirror Room session depth levels"""
    SURFACE = "surface"        # Initial exploration, building safety
    MODERATE = "moderate"      # Deeper patterns, gentle integration  
    PROFOUND = "profound"      # Core wounds, transformational work
    INTEGRATION = "integration" # Synthesis and embodiment


class TherapeuticFocus(str, Enum):
    """Primary therapeutic focus for session"""
    PARTS_WORK = "parts_work"           # IFS parts dialogue
    SHADOW_INTEGRATION = "shadow_integration"  # Shadow pattern work
    PARDES_REFLECTION = "pardes_reflection"     # PaRDeS multi-layer reflection
    NARRATIVE_THERAPY = "narrative_therapy"    # Story reframing work
    INTEGRATED = "integrated"           # All frameworks together
    ASSESSMENT = "assessment"           # Initial exploration


class SafetyLevel(str, Enum):
    """Therapeutic safety assessment"""
    SAFE = "safe"               # Continue with current approach
    CAUTION = "caution"         # Slow down, increase support
    ESCALATE = "escalate"       # Human therapist involvement needed
    EMERGENCY = "emergency"     # Immediate intervention required


class MirrorRoomSession(BaseModel):
    """Represents an active Mirror Room session"""
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    start_time: datetime = Field(default_factory=datetime.utcnow)
    current_depth: SessionDepth = SessionDepth.SURFACE
    therapeutic_focus: TherapeuticFocus = TherapeuticFocus.ASSESSMENT
    session_history: List[Dict[str, Any]] = Field(default_factory=list)
    identified_parts: List[Dict[str, Any]] = Field(default_factory=list)
    identified_patterns: List[Dict[str, Any]] = Field(default_factory=list)
    safety_level: SafetyLevel = SafetyLevel.SAFE
    confidence_scores: List[float] = Field(default_factory=list)
    integration_readiness: float = 0.0
    last_activity: datetime = Field(default_factory=datetime.utcnow)


class MirrorRoomResponse(BaseModel):
    """Response from Mirror Room session"""
    session_id: str
    response_text: str
    therapeutic_insights: List[Dict[str, Any]]
    suggested_questions: List[str]
    depth_progression: float = Field(ge=0.0, le=1.0)
    safety_assessment: SafetyLevel
    session_recommendations: List[str]
    integration_opportunities: List[str]


class MirrorRoomEngine(BaseAgent):
    """
    Mirror Room Orchestration Engine
    
    Coordinates IFS and Shadow Work agents to create DPNR's signature
    therapeutic experience with depth progression and safety protocols.
    """
    
    def __init__(self):
        super().__init__(
            agent_id="mirror-room-engine",
            name="Mirror Room Orchestration Engine",
            version="1.0.0"
        )
        self.logger = logging.getLogger(__name__)
        self.active_sessions: Dict[str, MirrorRoomSession] = {}
        
        # Initialize therapeutic agents
        self.ifs_agent: Optional[IFSAgent] = None
        self.shadow_agent: Optional[ShadowWorkAgent] = None
        self.pardes_agent: Optional[PaRDeSReflectionAgent] = None
        
        # Session configuration
        self.max_session_duration = timedelta(hours=2)
        self.depth_progression_threshold = 0.75
        self.safety_check_interval = 5  # Check safety every 5 interactions
        
    async def initialize(self) -> bool:
        """Initialize Mirror Room engine and therapeutic agents"""
        try:
            self.logger.info("Initializing Mirror Room Engine")
            
            # Initialize therapeutic agents
            self.ifs_agent = IFSAgent()
            await self.ifs_agent.initialize()
            
            self.shadow_agent = ShadowWorkAgent()
            await self.shadow_agent.initialize()
            
            self.pardes_agent = PaRDeSReflectionAgent()
            await self.pardes_agent.initialize()
            
            self.narrative_agent = NarrativeTherapyAgent()
            await self.narrative_agent.initialize()
            
            self.logger.info("Mirror Room Engine initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Mirror Room Engine: {e}")
            return False
    
    def get_capabilities(self) -> List:
        """Return Mirror Room capabilities"""
        return [
            {
                "name": "start_session",
                "description": "Start new Mirror Room therapeutic session",
                "input_schema": {"user_id": "string", "initial_context": "string"},
                "output_schema": {"session": "object"}
            },
            {
                "name": "continue_session",
                "description": "Continue existing Mirror Room session",
                "input_schema": {"session_id": "string", "user_input": "string"},
                "output_schema": {"response": "object"}
            },
            {
                "name": "assess_safety",
                "description": "Assess therapeutic safety of session",
                "input_schema": {"session_id": "string"},
                "output_schema": {"safety_assessment": "object"}
            }
        ]
    
    async def validate_input(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate Mirror Room input"""
        action = data.get("action")
        if action not in ["start_session", "continue_session", "assess_safety", "end_session"]:
            return False, f"Unknown action: {action}"
        
        if action == "start_session" and not data.get("data", {}).get("user_id"):
            return False, "user_id required for start_session"
        
        if action in ["continue_session", "assess_safety", "end_session"] and not data.get("data", {}).get("session_id"):
            return False, "session_id required for this action"
            
        return True, None
    
    async def process(self, message: AgentMessage) -> AgentResponse:
        """Process Mirror Room requests"""
        start_time = datetime.utcnow()
        
        try:
            action = message.payload.get("action")
            data = message.payload.get("data", {})
            
            if action == "start_session":
                session = await self.start_session(
                    data.get("user_id"),
                    data.get("initial_context", ""),
                    data.get("depth_level", SessionDepth.SURFACE)
                )
                result = {"session": session.dict()}
                
            elif action == "continue_session":
                response = await self.continue_session(
                    data.get("session_id"),
                    data.get("user_input", "")
                )
                result = {"response": response.dict()}
                
            elif action == "assess_safety":
                safety_assessment = await self.assess_session_safety(
                    data.get("session_id")
                )
                result = {"safety_assessment": safety_assessment}
                
            elif action == "end_session":
                summary = await self.end_session(
                    data.get("session_id")
                )
                result = {"session_summary": summary}
                
            else:
                raise ValueError(f"Unknown action: {action}")
            
            return AgentResponse(
                success=True,
                data=result,
                processing_time=(datetime.utcnow() - start_time).total_seconds(),
                agent_id=self.agent_id,
                confidence=self._calculate_overall_confidence(data.get("session_id"))
            )
            
        except Exception as e:
            self.logger.error(f"Mirror Room processing failed: {e}")
            return AgentResponse(
                success=False,
                error=str(e),
                processing_time=(datetime.utcnow() - start_time).total_seconds(),
                agent_id=self.agent_id
            )
    
    async def start_session(self, user_id: str, initial_context: str, 
                          depth_level: SessionDepth = SessionDepth.SURFACE) -> MirrorRoomSession:
        """Start a new Mirror Room session"""
        
        session = MirrorRoomSession(
            user_id=user_id,
            current_depth=depth_level,
            therapeutic_focus=TherapeuticFocus.ASSESSMENT
        )
        
        # Store session
        self.active_sessions[session.session_id] = session
        
        # Initial assessment using both agents
        await self._conduct_initial_assessment(session, initial_context)
        
        self.logger.info(f"Started Mirror Room session {session.session_id} for user {user_id}")
        return session
    
    async def continue_session(self, session_id: str, user_input: str) -> MirrorRoomResponse:
        """Continue an existing Mirror Room session"""
        
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        
        # Update last activity
        session.last_activity = datetime.utcnow()
        
        # Check session safety
        safety_level = await self._assess_safety(session, user_input)
        session.safety_level = safety_level
        
        if safety_level == SafetyLevel.EMERGENCY:
            return await self._handle_emergency(session)
        elif safety_level == SafetyLevel.ESCALATE:
            return await self._handle_escalation(session)
        
        # Determine therapeutic approach
        therapeutic_approach = await self._determine_therapeutic_approach(session, user_input)
        
        # Coordinate agents based on approach
        response = await self._coordinate_therapeutic_response(
            session, user_input, therapeutic_approach
        )
        
        # Update session history
        session.session_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "user_input": user_input,
            "response": response.response_text,
            "therapeutic_focus": therapeutic_approach,
            "depth": session.current_depth,
            "safety_level": safety_level
        })
        
        # Check for depth progression
        await self._evaluate_depth_progression(session, response)
        
        return response
    
    async def _conduct_initial_assessment(self, session: MirrorRoomSession, initial_context: str):
        """Conduct initial assessment using both IFS and Shadow Work agents"""
        
        # IFS parts identification
        ifs_message = AgentMessage(
            id=f"ifs-assessment-{session.session_id}",
            source_agent=self.agent_id,
            payload={
                "action": "identify_parts",
                "data": {"text": initial_context}
            }
        )
        
        ifs_response = await self.ifs_agent.process(ifs_message)
        if ifs_response.success:
            session.identified_parts = ifs_response.data.get("parts", [])
        
        # Shadow pattern detection
        shadow_message = AgentMessage(
            id=f"shadow-assessment-{session.session_id}",
            source_agent=self.agent_id,
            payload={
                "action": "detect_shadow_patterns",
                "data": {"text": initial_context, "history": []}
            }
        )
        
        shadow_response = await self.shadow_agent.process(shadow_message)
        if shadow_response.success:
            session.identified_patterns = shadow_response.data.get("patterns", [])
        
        # Determine initial therapeutic focus
        if session.identified_parts and session.identified_patterns:
            session.therapeutic_focus = TherapeuticFocus.INTEGRATED
        elif session.identified_parts:
            session.therapeutic_focus = TherapeuticFocus.PARTS_WORK
        elif session.identified_patterns:
            session.therapeutic_focus = TherapeuticFocus.SHADOW_INTEGRATION
        
        self.logger.info(f"Initial assessment complete for session {session.session_id}")
    
    async def _determine_therapeutic_approach(self, session: MirrorRoomSession, 
                                           user_input: str) -> TherapeuticFocus:
        """Determine the best therapeutic approach for current interaction"""
        
        # Analyze user input for therapeutic indicators
        parts_indicators = ["part of me", "inner critic", "scared", "angry part", "protective"]
        shadow_indicators = ["they always", "people are", "i hate", "disgusts me", "i never"]
        pardes_indicators = ["insight", "realize", "understand", "meaning", "deeper", "wisdom"]
        narrative_indicators = ["story", "narrative", "identity", "problem", "always been", "never been", "who i am"]
        
        user_input_lower = user_input.lower()
        
        parts_score = sum(1 for indicator in parts_indicators if indicator in user_input_lower)
        shadow_score = sum(1 for indicator in shadow_indicators if indicator in user_input_lower)
        pardes_score = sum(1 for indicator in pardes_indicators if indicator in user_input_lower)
        narrative_score = sum(1 for indicator in narrative_indicators if indicator in user_input_lower)
        
        # Narrative therapy is helpful for identity and story work
        if narrative_score >= 2 or "my story" in user_input_lower or "who i am" in user_input_lower:
            return TherapeuticFocus.NARRATIVE_THERAPY
        
        # PaRDeS is especially suitable for integration phases and profound insights
        if (session.current_depth in [SessionDepth.PROFOUND, SessionDepth.INTEGRATION] and 
            pardes_score > 0):
            return TherapeuticFocus.PARDES_REFLECTION
        
        # Consider session history and current focus
        if parts_score > shadow_score and parts_score > pardes_score and session.identified_parts:
            return TherapeuticFocus.PARTS_WORK
        elif shadow_score > parts_score and shadow_score > pardes_score and session.identified_patterns:
            return TherapeuticFocus.SHADOW_INTEGRATION
        elif pardes_score > 0 and session.current_depth != SessionDepth.SURFACE:
            return TherapeuticFocus.PARDES_REFLECTION
        elif narrative_score > 0 and session.current_depth != SessionDepth.SURFACE:
            return TherapeuticFocus.NARRATIVE_THERAPY
        elif session.current_depth in [SessionDepth.PROFOUND, SessionDepth.INTEGRATION]:
            return TherapeuticFocus.INTEGRATED
        else:
            return session.therapeutic_focus  # Continue current focus
    
    async def _coordinate_therapeutic_response(self, session: MirrorRoomSession, 
                                             user_input: str, approach: TherapeuticFocus) -> MirrorRoomResponse:
        """Coordinate response from appropriate therapeutic agent(s)"""
        
        insights = []
        suggestions = []
        integration_opportunities = []
        
        if approach == TherapeuticFocus.PARTS_WORK:
            # Use IFS agent for parts work
            response_text, ifs_insights, ifs_suggestions = await self._get_ifs_response(
                session, user_input
            )
            insights.extend(ifs_insights)
            suggestions.extend(ifs_suggestions)
            
        elif approach == TherapeuticFocus.SHADOW_INTEGRATION:
            # Use Shadow Work agent
            response_text, shadow_insights, shadow_suggestions = await self._get_shadow_response(
                session, user_input
            )
            insights.extend(shadow_insights)
            suggestions.extend(shadow_suggestions)
            
        elif approach == TherapeuticFocus.PARDES_REFLECTION:
            # Use PaRDeS Reflection agent
            response_text, pardes_insights, pardes_suggestions = await self._get_pardes_response(
                session, user_input
            )
            insights.extend(pardes_insights)
            suggestions.extend(pardes_suggestions)
            
        elif approach == TherapeuticFocus.NARRATIVE_THERAPY:
            # Use Narrative Therapy agent
            response_text, narrative_insights, narrative_suggestions = await self._get_narrative_response(
                session, user_input
            )
            insights.extend(narrative_insights)
            suggestions.extend(narrative_suggestions)
            
        elif approach == TherapeuticFocus.INTEGRATED:
            # Coordinate both agents
            ifs_text, ifs_insights, ifs_suggestions = await self._get_ifs_response(session, user_input)
            shadow_text, shadow_insights, shadow_suggestions = await self._get_shadow_response(session, user_input)
            
            # Integrate responses
            response_text = await self._integrate_therapeutic_responses(ifs_text, shadow_text)
            insights.extend(ifs_insights + shadow_insights)
            suggestions.extend(ifs_suggestions + shadow_suggestions)
            integration_opportunities = await self._identify_integration_opportunities(session)
            
        else:
            # Assessment mode
            response_text = "I'm here to understand what's present for you today. What would you like to explore?"
            suggestions = [
                "What part of your experience feels most important right now?",
                "What patterns do you notice in your relationships or reactions?",
                "What would you like to understand better about yourself?"
            ]
        
        # Calculate depth progression
        depth_progression = self._calculate_depth_progression(session)
        
        return MirrorRoomResponse(
            session_id=session.session_id,
            response_text=response_text,
            therapeutic_insights=insights,
            suggested_questions=suggestions,
            depth_progression=depth_progression,
            safety_assessment=session.safety_level,
            session_recommendations=self._generate_session_recommendations(session),
            integration_opportunities=integration_opportunities
        )
    
    async def _get_ifs_response(self, session: MirrorRoomSession, user_input: str) -> Tuple[str, List[Dict], List[str]]:
        """Get response from IFS agent"""
        
        # Determine most relevant part for dialogue
        relevant_part = None
        if session.identified_parts:
            # Simple relevance scoring based on user input
            for part_data in session.identified_parts:
                part_emotions = part_data.get("emotions", [])
                if any(emotion in user_input.lower() for emotion in part_emotions):
                    relevant_part = part_data
                    break
            
            if not relevant_part:
                relevant_part = session.identified_parts[0]  # Use first identified part
        
        if relevant_part:
            # Facilitate dialogue with identified part
            dialogue_message = AgentMessage(
                id=f"ifs-dialogue-{session.session_id}",
                source_agent=self.agent_id,
                payload={
                    "action": "facilitate_dialogue",
                    "data": {
                        "part_id": relevant_part.get("part_id"),
                        "message": user_input,
                        "session_context": {
                            "part_type": relevant_part.get("part_type"),
                            "depth": session.current_depth
                        }
                    }
                }
            )
            
            ifs_response = await self.ifs_agent.process(dialogue_message)
            
            if ifs_response.success:
                response_data = ifs_response.data
                return (
                    response_data.get("part_response", ""),
                    [{"type": "ifs_insight", "part": relevant_part, "dialogue_quality": ifs_response.confidence}],
                    response_data.get("suggested_questions", [])
                )
        
        # Fallback to general IFS response
        return (
            "I notice there might be different parts of you present. Which part would like to be heard right now?",
            [{"type": "ifs_general", "observation": "Parts may be present but not yet clearly identified"}],
            [
                "What part of you is speaking right now?",
                "How long has this part been trying to protect you?",
                "What does this part most need you to know?"
            ]
        )
    
    async def _get_shadow_response(self, session: MirrorRoomSession, user_input: str) -> Tuple[str, List[Dict], List[str]]:
        """Get response from Shadow Work agent"""
        
        # Look for relevant shadow pattern
        relevant_pattern = None
        if session.identified_patterns:
            for pattern_data in session.identified_patterns:
                pattern_type = pattern_data.get("pattern_type")
                if pattern_type == "projection" and ("they" in user_input.lower() or "people" in user_input.lower()):
                    relevant_pattern = pattern_data
                    break
                elif pattern_type == "repression" and ("never" in user_input.lower() or "not me" in user_input.lower()):
                    relevant_pattern = pattern_data
                    break
        
        if relevant_pattern:
            # Generate integration guidance
            guidance_message = AgentMessage(
                id=f"shadow-guidance-{session.session_id}",
                source_agent=self.agent_id,
                payload={
                    "action": "generate_integration_guidance",
                    "data": {
                        "pattern": relevant_pattern,
                        "readiness": session.integration_readiness
                    }
                }
            )
            
            shadow_response = await self.shadow_agent.process(guidance_message)
            
            if shadow_response.success:
                guidance_data = shadow_response.data.get("guidance", {})
                steps = guidance_data.get("integration_steps", [])
                questions = guidance_data.get("reflection_questions", [])
                
                response_text = f"I notice a pattern that might be worth exploring gently. {steps[0] if steps else 'What do you make of this pattern you have described?'}"
                
                return (
                    response_text,
                    [{"type": "shadow_insight", "pattern": relevant_pattern, "guidance_quality": shadow_response.confidence}],
                    questions[:3]  # Limit to 3 questions
                )
        
        # Fallback to general shadow work response
        return (
            "I'm curious about what might be happening unconsciously. What aspects of this situation feel familiar?",
            [{"type": "shadow_general", "observation": "Shadow patterns may be present but require gentle exploration"}],
            [
                "What about this reminds you of other situations?",
                "What would you never want to be like?",
                "What do you find yourself judging in others?"
            ]
        )
    
    async def _get_pardes_response(self, session: MirrorRoomSession, user_input: str) -> Tuple[str, List[Dict], List[str]]:
        """Get response from PaRDeS Reflection agent"""
        
        # Build reflection context from session data
        context = ReflectionContext(
            soul_archetype=session.session_history[-1].get("soul_archetype", "seeker") if session.session_history else "seeker",
            growth_level=session.integration_readiness * 10.0,  # Convert to 0-10 scale
            spiritual_readiness=8.0 if session.current_depth == SessionDepth.PROFOUND else 6.0,
            therapeutic_history=[h.get("user_input", "") for h in session.session_history[-5:]],  # Last 5 interactions
            current_challenges=[]  # Would be populated from safety assessments
        )
        
        # Determine appropriate depth based on session depth
        depth_map = {
            SessionDepth.SURFACE: "surface",
            SessionDepth.MODERATE: "moderate", 
            SessionDepth.PROFOUND: "deep",
            SessionDepth.INTEGRATION: "profound"
        }
        depth_requested = depth_map.get(session.current_depth, "moderate")
        
        # Generate PaRDeS reflection
        pardes_message = AgentMessage(
            id=f"pardes-{session.session_id}",
            source_agent=self.agent_id,
            payload={
                "action": "generate_reflection",
                "data": {
                    "insight": user_input,
                    "context": context.dict(),
                    "depth_requested": depth_requested
                }
            }
        )
        
        pardes_response = await self.pardes_agent.process(pardes_message)
        
        if pardes_response.success:
            reflection_data = pardes_response.data
            layers = reflection_data.get("layers", {})
            metaphors = reflection_data.get("metaphors", [])
            integration_guidance = reflection_data.get("integration_guidance", [])
            
            # Create integrated response text from layers
            response_parts = []
            if "pshat" in layers and layers["pshat"]:
                response_parts.append(f"At the surface level: {layers['pshat']}")
            if "remez" in layers and layers["remez"]:
                response_parts.append(f"The emotional pattern I notice: {layers['remez']}")
            if "drash" in layers and layers["drash"]:
                response_parts.append(f"From a growth perspective: {layers['drash']}")
            if "sod" in layers and layers["sod"]:
                response_parts.append(f"At the soul level: {layers['sod']}")
            
            response_text = " | ".join(response_parts) if response_parts else "I sense deeper layers of meaning in what you've shared."
            
            # Add a metaphor if available
            if metaphors:
                response_text += f" | {metaphors[0]}"
            
            insights = [{
                "type": "pardes_reflection",
                "layers": layers,
                "metaphors": metaphors,
                "depth": depth_requested,
                "reflection_id": reflection_data.get("reflection_id"),
                "therapeutic_potency": reflection_data.get("therapeutic_potency", 0.85)
            }]
            
            # Convert integration guidance to suggested questions
            suggestions = integration_guidance[:3] if integration_guidance else [
                "How does this deeper understanding change your relationship to the situation?",
                "What layer of meaning resonates most strongly with you?",
                "How might you integrate this insight into your daily life?"
            ]
            
            return (response_text, insights, suggestions)
        
        # Fallback response if PaRDeS fails
        return (
            "I sense there are deeper layers of meaning in what you've shared. Let's explore this together.",
            [{"type": "pardes_fallback", "observation": "Multi-layer reflection requested but could not be generated"}],
            [
                "What feels most significant about this realization?",
                "How might this connect to larger patterns in your life?",
                "What wisdom is trying to emerge here?"
            ]
        )
    
    async def _get_narrative_response(self, session: MirrorRoomSession, user_input: str) -> Tuple[str, List[Dict], List[str]]:
        """Get response from Narrative Therapy agent"""
        
        # Build narrative context from session
        narrative_context = NarrativeContext(
            user_id=session.user_id,
            session_history=[h.get("user_input", "") for h in session.session_history[-5:]],
            identified_values={"authenticity": 0.8, "growth": 0.9, "connection": 0.7},  # Could be derived from session
            therapeutic_goals=["identity clarity", "story reframing"],
            growth_level=session.integration_readiness * 10.0
        )
        
        # Create analysis message
        narrative_message = AgentMessage(
            id=f"narrative-{session.session_id}",
            type="assessment_request",
            content={"text": user_input, "context": narrative_context.dict()},
            sender_id=self.agent_id,
            recipient_id=self.narrative_agent.agent_id,
            timestamp=datetime.utcnow()
        )
        
        # Process with narrative agent
        narrative_response = await self.narrative_agent.process({
            "action": "analyze_narrative",
            "data": {"text": user_input, "context": narrative_context.dict()}
        })
        
        if narrative_response.success:
            analysis = narrative_response.data.get("analysis", {})
            
            # Build response based on narrative analysis
            dominant_story = analysis.get("dominant_story", "")
            problem_story = analysis.get("problem_story", "")
            unique_outcomes = analysis.get("unique_outcomes", [])
            alternative_story = analysis.get("alternative_story", "")
            
            insights = []
            
            # Add narrative insights
            if dominant_story:
                insights.append({
                    "type": "narrative_dominant_story",
                    "story": dominant_story,
                    "significance": "This is the main story you tell about yourself"
                })
            
            if problem_story:
                insights.append({
                    "type": "narrative_problem_story",
                    "story": problem_story,
                    "externalization": analysis.get("externalized_problem", "")
                })
            
            if unique_outcomes:
                insights.append({
                    "type": "narrative_unique_outcomes",
                    "outcomes": unique_outcomes,
                    "potential": "These exceptions show your capacity for change"
                })
            
            # Craft therapeutic response
            if alternative_story:
                response_text = f"I'm hearing your story, and I'm also noticing something else. {alternative_story} What does this alternative narrative bring up for you?"
            elif unique_outcomes:
                response_text = f"While you've shared about {dominant_story}, I'm also curious about times when this wasn't the whole story. {unique_outcomes[0] if unique_outcomes else 'Can you think of any exceptions?'}"
            else:
                response_text = f"The story you're telling about yourself seems to be: {dominant_story}. I wonder what other stories might also be true?"
            
            # Generate narrative-focused questions
            suggestions = [
                "What would your preferred story about yourself sound like?",
                "Who would notice first if you started living this new story?",
                "What values are most important in the story you want to live?"
            ]
            
            return (response_text, insights, suggestions)
        
        # Fallback if narrative analysis fails
        return (
            "I'm interested in the story you're telling about yourself and your life. What narrative feels most true right now?",
            [{"type": "narrative_fallback", "observation": "Story analysis requested but could not be completed"}],
            [
                "What story have you been telling yourself about this situation?",
                "Are there times when a different story was possible?",
                "What would you prefer your story to be?"
            ]
        )
    
    async def _integrate_therapeutic_responses(self, ifs_response: str, shadow_response: str) -> str:
        """Integrate IFS and Shadow Work responses into coherent reflection"""
        
        # Simple integration - in production, this could use an LLM for more sophisticated synthesis
        if "part" in ifs_response.lower() and "pattern" in shadow_response.lower():
            return f"I'm noticing both an internal part that's present and a pattern that might be worth exploring. {ifs_response} At the same time, {shadow_response.lower()}"
        elif len(ifs_response) > len(shadow_response):
            return f"{ifs_response} I'm also curious about any patterns this brings up for you."
        else:
            return f"{shadow_response} And I wonder what parts of you are responding to this pattern."
    
    async def _identify_integration_opportunities(self, session: MirrorRoomSession) -> List[str]:
        """Identify opportunities for integrating IFS and Shadow Work insights"""
        
        opportunities = []
        
        # Check for parts holding shadow content
        if session.identified_parts and session.identified_patterns:
            for part in session.identified_parts:
                part_type = part.get("part_type")
                if part_type == "exile" and any(p.get("pattern_type") == "repression" for p in session.identified_patterns):
                    opportunities.append("Exile part may be holding repressed shadow content - gentle integration possible")
                elif part_type == "manager" and any(p.get("pattern_type") == "projection" for p in session.identified_patterns):
                    opportunities.append("Manager part may be projecting control needs - awareness opportunity")
        
        # Check for depth readiness
        if session.current_depth in [SessionDepth.MODERATE, SessionDepth.PROFOUND]:
            opportunities.append("Session depth supports deeper integration work")
        
        return opportunities
    
    def _calculate_depth_progression(self, session: MirrorRoomSession) -> float:
        """Calculate how ready the session is to progress to deeper levels"""
        
        factors = {
            "trust_built": len(session.session_history) >= 3,
            "parts_identified": len(session.identified_parts) > 0,
            "patterns_recognized": len(session.identified_patterns) > 0,
            "safety_maintained": session.safety_level in [SafetyLevel.SAFE, SafetyLevel.CAUTION],
            "confidence_stable": len(session.confidence_scores) >= 3 and min(session.confidence_scores[-3:]) > 0.7
        }
        
        progression_score = sum(factors.values()) / len(factors)
        return progression_score
    
    async def _evaluate_depth_progression(self, session: MirrorRoomSession, response: MirrorRoomResponse):
        """Evaluate whether session is ready to progress to deeper level"""
        
        if response.depth_progression >= self.depth_progression_threshold:
            current_depth = session.current_depth
            
            if current_depth == SessionDepth.SURFACE and response.depth_progression >= 0.75:
                session.current_depth = SessionDepth.MODERATE
                self.logger.info(f"Session {session.session_id} progressed to MODERATE depth")
                
            elif current_depth == SessionDepth.MODERATE and response.depth_progression >= 0.85:
                session.current_depth = SessionDepth.PROFOUND
                self.logger.info(f"Session {session.session_id} progressed to PROFOUND depth")
                
            elif current_depth == SessionDepth.PROFOUND and response.depth_progression >= 0.90:
                session.current_depth = SessionDepth.INTEGRATION
                self.logger.info(f"Session {session.session_id} progressed to INTEGRATION depth")
    
    async def _assess_safety(self, session: MirrorRoomSession, user_input: str) -> SafetyLevel:
        """Assess therapeutic safety of current session"""
        
        # Emergency indicators
        emergency_indicators = [
            "kill myself", "end it all", "not worth living", "suicide",
            "hurt myself", "self harm", "overdose"
        ]
        
        # Escalation indicators  
        escalation_indicators = [
            "can't handle", "too much", "overwhelmed", "breaking down",
            "losing control", "dissociat", "panic attack"
        ]
        
        user_input_lower = user_input.lower()
        
        # Check for emergency indicators
        if any(indicator in user_input_lower for indicator in emergency_indicators):
            return SafetyLevel.EMERGENCY
        
        # Check for escalation indicators
        if any(indicator in user_input_lower for indicator in escalation_indicators):
            return SafetyLevel.ESCALATE
        
        # Check session factors
        session_duration = datetime.utcnow() - session.start_time
        if session_duration > self.max_session_duration:
            return SafetyLevel.CAUTION
        
        # Check confidence scores
        if (len(session.confidence_scores) >= 3 and 
            max(session.confidence_scores[-3:]) < 0.5):
            return SafetyLevel.CAUTION
        
        return SafetyLevel.SAFE
    
    async def _handle_emergency(self, session: MirrorRoomSession) -> MirrorRoomResponse:
        """Handle emergency situation"""
        
        self.logger.critical(f"EMERGENCY detected in session {session.session_id}")
        
        return MirrorRoomResponse(
            session_id=session.session_id,
            response_text="I'm concerned about your safety. Please reach out to a crisis hotline, emergency services, or a trusted person immediately. National Suicide Prevention Lifeline: 988",
            therapeutic_insights=[{
                "type": "emergency_response",
                "priority": "immediate_intervention",
                "resources": ["988 Suicide Prevention Lifeline", "911 Emergency Services"]
            }],
            suggested_questions=[],
            depth_progression=0.0,
            safety_assessment=SafetyLevel.EMERGENCY,
            session_recommendations=["END_SESSION_IMMEDIATELY", "ESCALATE_TO_HUMAN", "PROVIDE_CRISIS_RESOURCES"],
            integration_opportunities=[]
        )
    
    async def _handle_escalation(self, session: MirrorRoomSession) -> MirrorRoomResponse:
        """Handle therapeutic escalation"""
        
        self.logger.warning(f"Escalation needed for session {session.session_id}")
        
        return MirrorRoomResponse(
            session_id=session.session_id,
            response_text="I notice you're experiencing something intense right now. This seems like important work that would benefit from a human therapist's support. Would you like help finding resources?",
            therapeutic_insights=[{
                "type": "escalation_recommended",
                "reason": "Intensity beyond AI therapeutic scope",
                "next_steps": "Human therapist consultation recommended"
            }],
            suggested_questions=[
                "Would you like me to help you find a therapist?",
                "What support do you have available right now?",
                "How can we help you feel safer in this moment?"
            ],
            depth_progression=0.0,
            safety_assessment=SafetyLevel.ESCALATE,
            session_recommendations=["CONNECT_WITH_HUMAN_THERAPIST", "PROVIDE_SUPPORT_RESOURCES", "SLOW_DOWN_PACE"],
            integration_opportunities=[]
        )
    
    def _generate_session_recommendations(self, session: MirrorRoomSession) -> List[str]:
        """Generate recommendations for session continuation"""
        
        recommendations = []
        
        # Depth-based recommendations
        if session.current_depth == SessionDepth.SURFACE:
            recommendations.append("Continue building trust and safety")
            recommendations.append("Explore presenting concerns gently")
            
        elif session.current_depth == SessionDepth.MODERATE:
            recommendations.append("Begin deeper pattern exploration")
            recommendations.append("Introduce parts dialogue if appropriate")
            
        elif session.current_depth == SessionDepth.PROFOUND:
            recommendations.append("Support core healing work")
            recommendations.append("Maintain therapeutic boundaries")
            
        elif session.current_depth == SessionDepth.INTEGRATION:
            recommendations.append("Focus on synthesis and embodiment")
            recommendations.append("Plan practical integration steps")
        
        # Safety-based recommendations
        if session.safety_level == SafetyLevel.CAUTION:
            recommendations.append("Monitor safety indicators closely")
            recommendations.append("Consider slowing therapeutic pace")
        
        return recommendations
    
    def _calculate_overall_confidence(self, session_id: str) -> float:
        """Calculate overall confidence for current session"""
        
        if not session_id or session_id not in self.active_sessions:
            return 0.7  # Default confidence
        
        session = self.active_sessions[session_id]
        
        if not session.confidence_scores:
            return 0.7
        
        # Return average of recent confidence scores
        recent_scores = session.confidence_scores[-5:]  # Last 5 interactions
        return sum(recent_scores) / len(recent_scores)
    
    async def assess_session_safety(self, session_id: str) -> Dict[str, Any]:
        """Public method to assess session safety"""
        
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        safety_level = await self._assess_safety(session, "")
        
        return {
            "session_id": session_id,
            "safety_level": safety_level,
            "session_duration": (datetime.utcnow() - session.start_time).total_seconds(),
            "interaction_count": len(session.session_history),
            "current_depth": session.current_depth,
            "recommendations": self._generate_session_recommendations(session)
        }
    
    async def end_session(self, session_id: str) -> Dict[str, Any]:
        """End Mirror Room session and provide summary"""
        
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        
        summary = {
            "session_id": session_id,
            "user_id": session.user_id,
            "duration": (datetime.utcnow() - session.start_time).total_seconds(),
            "interactions": len(session.session_history),
            "max_depth_reached": session.current_depth,
            "parts_identified": len(session.identified_parts),
            "patterns_identified": len(session.identified_patterns),
            "final_safety_level": session.safety_level,
            "integration_opportunities": len(await self._identify_integration_opportunities(session)),
            "therapeutic_insights": self._generate_session_insights(session)
        }
        
        # Clean up session
        del self.active_sessions[session_id]
        
        self.logger.info(f"Ended Mirror Room session {session_id}")
        return summary
    
    def _generate_session_insights(self, session: MirrorRoomSession) -> List[str]:
        """Generate insights from completed session"""
        
        insights = []
        
        if session.identified_parts:
            parts_summary = ", ".join([p.get("part_type", "unknown") for p in session.identified_parts])
            insights.append(f"Parts identified: {parts_summary}")
        
        if session.identified_patterns:
            patterns_summary = ", ".join([p.get("pattern_type", "unknown") for p in session.identified_patterns])
            insights.append(f"Shadow patterns explored: {patterns_summary}")
        
        if session.current_depth != SessionDepth.SURFACE:
            insights.append(f"Therapeutic depth reached: {session.current_depth}")
        
        if session.safety_level == SafetyLevel.SAFE:
            insights.append("Session maintained therapeutic safety throughout")
        
        return insights