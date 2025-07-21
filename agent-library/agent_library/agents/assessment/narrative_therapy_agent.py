"""
Narrative Therapy Agent for DPNR Platform
Story reframing and identity reconstruction framework
Built using PaRDeS architectural template
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


class StoryType(str, Enum):
    """Types of narratives in narrative therapy"""
    DOMINANT = "dominant"          # Main life story
    PROBLEM = "problem"            # Problem-saturated story
    PREFERRED = "preferred"        # Alternative/preferred story
    UNIQUE_OUTCOME = "unique_outcome"  # Exception to problem story


class NarrativeTheme(str, Enum):
    """Common narrative therapy themes"""
    IDENTITY = "identity"
    RELATIONSHIPS = "relationships"
    ACHIEVEMENT = "achievement"
    BELONGING = "belonging"
    PURPOSE = "purpose"
    RESILIENCE = "resilience"
    AGENCY = "agency"
    VALUES = "values"


class NarrativeAnalysis(BaseModel):
    """Complete narrative therapy analysis"""
    analysis_id: str
    user_id: str
    original_text: str
    dominant_story: str
    problem_story: Optional[str]
    externalized_problem: Optional[str]
    unique_outcomes: List[str]
    alternative_story: Optional[str]
    themes: List[NarrativeTheme]
    values_alignment: Dict[str, float]
    confidence: float = Field(ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    @validator('unique_outcomes')
    def validate_outcomes(cls, v):
        return [outcome for outcome in v if outcome and len(outcome) > 10]


class StoryReframe(BaseModel):
    """Reframed story structure"""
    original_narrative: str
    reframed_narrative: str
    reframing_technique: str
    therapeutic_intent: str
    empowerment_level: float = Field(ge=0.0, le=1.0)


class UniqueOutcome(BaseModel):
    """Exception to problem story"""
    outcome_id: str
    description: str
    significance: str
    theme: NarrativeTheme
    strength_revealed: str


class NarrativeContext(BaseModel):
    """Context for narrative analysis"""
    user_id: str
    session_history: Optional[List[str]] = []
    identified_values: Optional[Dict[str, float]] = {}
    therapeutic_goals: Optional[List[str]] = []
    cultural_context: Optional[str] = None
    growth_level: float = Field(default=5.0, ge=0.0, le=10.0)


class NarrativeTherapyAgent(BaseAgent):
    """
    Narrative Therapy Agent implementing story analysis and reframing
    Based on Michael White and David Epston's narrative therapy approach
    """
    
    def __init__(self):
        super().__init__(
            agent_id="narrative-therapy-agent",
            name="Narrative Therapy Agent",
            version="1.0.0"
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize OpenAI client for AI-powered analysis
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and OPENAI_AVAILABLE:
            self.openai_client = AsyncOpenAI(api_key=api_key)
            self.ai_enabled = True
            self.logger.info("OpenAI client initialized for narrative analysis")
        else:
            self.openai_client = None
            self.ai_enabled = False
            self.logger.warning("No OpenAI API key - using rule-based narrative analysis")
        
        # Problem externalization templates
        self.externalization_templates = self._load_externalization_templates()
        
        # Story reframing strategies
        self.reframing_strategies = self._load_reframing_strategies()
        
    async def initialize(self) -> bool:
        """Initialize narrative therapy agent"""
        try:
            self.logger.info("Initializing narrative therapy agent")
            
            # Define capabilities
            self._capabilities = [
                AgentCapability(
                    name="analyze_narrative",
                    description="Analyze dominant and problem stories",
                    input_schema={"text": "string", "context": "object"},
                    output_schema={"analysis": "object"}
                ),
                AgentCapability(
                    name="reframe_story",
                    description="Generate alternative narratives",
                    input_schema={"story": "string", "technique": "string"},
                    output_schema={"reframe": "object"}
                ),
                AgentCapability(
                    name="find_unique_outcomes",
                    description="Identify exceptions to problem stories",
                    input_schema={"text": "string", "problem": "string"},
                    output_schema={"outcomes": "array"}
                ),
                AgentCapability(
                    name="externalize_problem",
                    description="Separate person from problem",
                    input_schema={"text": "string", "problem": "string"},
                    output_schema={"externalization": "string"}
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
        valid_actions = ["analyze_narrative", "reframe_story", "find_unique_outcomes", "externalize_problem"]
        if action not in valid_actions:
            return False, f"Unknown action: {action}. Valid: {valid_actions}"
            
        return True, None
    
    async def process(self, message: AgentMessage) -> AgentResponse:
        """Process narrative therapy request"""
        start_time = datetime.now(timezone.utc)
        
        try:
            action = message.payload.get("action")
            data = message.payload.get("data", {})
            
            if action == "analyze_narrative":
                analysis = await self.analyze_narrative(
                    data.get("text", ""),
                    NarrativeContext(**data.get("context", {}))
                )
                result = {"analysis": analysis.dict()}
                
            elif action == "reframe_story":
                reframe = await self.reframe_story(
                    data.get("story", ""),
                    data.get("problem_story", ""),
                    data.get("values", {}),
                    data.get("technique", "strengths_based")
                )
                result = {"reframe": reframe.dict()}
                
            elif action == "find_unique_outcomes":
                outcomes = await self.find_unique_outcomes(
                    data.get("text", ""),
                    data.get("problem_story", "")
                )
                result = {"outcomes": [o.dict() for o in outcomes]}
                
            elif action == "externalize_problem":
                externalization = await self.externalize_problem(
                    data.get("text", ""),
                    data.get("problem_identification", "")
                )
                result = {"externalization": externalization}
                
            else:
                raise ValueError(f"Unknown action: {action}")
            
            # Calculate processing confidence
            processing_confidence = 0.85
            if action == "analyze_narrative" and isinstance(result.get('analysis'), dict):
                processing_confidence = result['analysis'].get('confidence', 0.85)
            
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
    
    async def analyze_narrative(self, text: str, context: NarrativeContext) -> NarrativeAnalysis:
        """Analyze narrative to identify dominant and problem stories"""
        
        analysis_id = str(uuid.uuid4())[:8]
        
        # Identify dominant story
        dominant_story = await self._identify_dominant_story(text, context)
        
        # Identify problem story
        problem_story = await self._identify_problem_story(text, dominant_story)
        
        # Externalize the problem
        externalized_problem = None
        if problem_story:
            externalized_problem = await self.externalize_problem(text, problem_story)
        
        # Find unique outcomes
        unique_outcomes = await self.find_unique_outcomes(text, problem_story or dominant_story)
        
        # Generate alternative story
        alternative_story = await self._generate_alternative_story(
            dominant_story, 
            problem_story,
            [o.description for o in unique_outcomes],
            context
        )
        
        # Identify themes
        themes = await self._identify_narrative_themes(text, dominant_story, alternative_story)
        
        # Assess values alignment
        values_alignment = await self._assess_values_alignment(
            alternative_story or dominant_story,
            context.identified_values or {}
        )
        
        # Calculate confidence
        confidence = await self._calculate_analysis_confidence(
            dominant_story,
            problem_story,
            unique_outcomes,
            alternative_story
        )
        
        return NarrativeAnalysis(
            analysis_id=analysis_id,
            user_id=context.user_id,
            original_text=text,
            dominant_story=dominant_story,
            problem_story=problem_story,
            externalized_problem=externalized_problem,
            unique_outcomes=[o.description for o in unique_outcomes],
            alternative_story=alternative_story,
            themes=themes,
            values_alignment=values_alignment,
            confidence=confidence
        )
    
    async def _identify_dominant_story(self, text: str, context: NarrativeContext) -> str:
        """Identify the dominant narrative in the text"""
        
        if self.ai_enabled:
            try:
                prompt = f"""
                Analyze this text to identify the dominant life story or narrative the person is telling about themselves.
                
                Text: "{text}"
                
                Context:
                - Growth level: {context.growth_level}/10
                - Therapeutic goals: {context.therapeutic_goals or 'Not specified'}
                
                Guidelines:
                - Identify the main story they tell about who they are
                - Look for repeated themes, identity statements, and self-descriptions
                - Notice totalizing statements ("I always...", "I never...", "I am...")
                - Focus on the overarching narrative, not just individual events
                - Keep it concise (2-3 sentences)
                
                Example: "The dominant story is one of being a perpetual failure who can't maintain relationships. The narrative centers on inadequacy and the belief that they inevitably disappoint others."
                """
                
                response = await self._make_ai_request(prompt, max_tokens=150)
                return response.strip()
                
            except Exception as e:
                self.logger.error(f"AI dominant story identification failed: {e}")
                return await self._identify_dominant_story_fallback(text)
        else:
            return await self._identify_dominant_story_fallback(text)
    
    async def _identify_problem_story(self, text: str, dominant_story: str) -> Optional[str]:
        """Identify problem-saturated narrative"""
        
        if self.ai_enabled:
            try:
                prompt = f"""
                Based on this text and dominant story, identify the problem-saturated narrative if present.
                
                Text: "{text}"
                Dominant Story: "{dominant_story}"
                
                Guidelines:
                - Look for narratives focused on problems, deficits, or limitations
                - Identify stories where problems define the person's identity
                - Notice language that makes problems seem permanent or unchangeable
                - Focus on totalizing problem descriptions
                - Return None if no clear problem story exists
                - Keep it concise (1-2 sentences)
                
                Example: "The problem story portrays anxiety as controlling their life, making them believe they are 'an anxious person' rather than someone experiencing anxiety."
                """
                
                response = await self._make_ai_request(prompt, max_tokens=120)
                return response.strip() if response.strip().lower() != "none" else None
                
            except Exception as e:
                self.logger.error(f"AI problem story identification failed: {e}")
                return await self._identify_problem_story_fallback(text)
        else:
            return await self._identify_problem_story_fallback(text)
    
    async def find_unique_outcomes(self, text: str, problem_story: str) -> List[UniqueOutcome]:
        """Find exceptions to the problem story"""
        
        unique_outcomes = []
        
        if self.ai_enabled and problem_story:
            try:
                prompt = f"""
                Identify unique outcomes - times when the problem story didn't dominate or the person acted outside their problem narrative.
                
                Text: "{text}"
                Problem Story: "{problem_story}"
                
                Guidelines:
                - Look for exceptions, contradictions to the problem story
                - Find moments of agency, strength, or different choices
                - Identify times the problem was less influential
                - Notice skills, knowledge, or values that contradict the problem story
                - Find up to 3 unique outcomes
                
                Format each outcome as:
                Description: [What happened]
                Significance: [Why this matters]
                Strength: [What ability or value this reveals]
                """
                
                response = await self._make_ai_request(prompt, max_tokens=300)
                
                # Parse response into unique outcomes
                outcomes_text = response.strip().split('\n\n')
                for i, outcome_text in enumerate(outcomes_text[:3]):
                    if outcome_text:
                        unique_outcomes.append(await self._parse_unique_outcome(outcome_text, i))
                        
            except Exception as e:
                self.logger.error(f"AI unique outcomes detection failed: {e}")
                unique_outcomes = await self._find_unique_outcomes_fallback(text, problem_story)
        else:
            unique_outcomes = await self._find_unique_outcomes_fallback(text, problem_story)
        
        return unique_outcomes
    
    async def externalize_problem(self, text: str, problem_identification: str) -> str:
        """Externalize the problem - separate person from problem"""
        
        if self.ai_enabled:
            try:
                prompt = f"""
                Create an externalization of this problem, separating the person from the problem using narrative therapy techniques.
                
                Text: "{text}"
                Problem: "{problem_identification}"
                
                Guidelines:
                - Give the problem a name or metaphor (e.g., "The Worry Monster", "The Critical Voice")
                - Describe how the problem operates on/influences the person
                - Use language that positions the person as separate from the problem
                - Make it relatable but not minimizing
                - Keep it therapeutic and empowering
                
                Example: "The Inner Critic has been visiting you frequently, whispering stories of inadequacy and trying to convince you that its voice is your truth."
                """
                
                response = await self._make_ai_request(prompt, max_tokens=120)
                return response.strip()
                
            except Exception as e:
                self.logger.error(f"AI externalization failed: {e}")
                return await self._externalize_problem_fallback(problem_identification)
        else:
            return await self._externalize_problem_fallback(problem_identification)
    
    async def reframe_story(self, story: str, problem_story: str, 
                           values: Dict[str, float], technique: str = "strengths_based") -> StoryReframe:
        """Reframe narrative using specified technique"""
        
        reframing_prompt = self.reframing_strategies.get(technique, self.reframing_strategies["strengths_based"])
        
        if self.ai_enabled:
            try:
                prompt = f"""
                Reframe this narrative using {technique} narrative therapy technique.
                
                Original Story: "{story}"
                Problem Story: "{problem_story}"
                Person's Values: {json.dumps(values) if values else "Not specified"}
                
                Reframing Approach: {reframing_prompt}
                
                Guidelines:
                - Honor the person's experience while offering new perspective
                - Highlight agency, choice, and capability
                - Connect to the person's values and preferred identity
                - Use empowering, non-pathologizing language
                - Make it authentic and resonant
                - 2-3 sentences maximum
                """
                
                response = await self._make_ai_request(prompt, max_tokens=150)
                reframed = response.strip()
                
            except Exception as e:
                self.logger.error(f"AI reframing failed: {e}")
                reframed = await self._reframe_story_fallback(story, technique)
        else:
            reframed = await self._reframe_story_fallback(story, technique)
        
        empowerment = await self._calculate_empowerment_level(story, reframed)
        
        return StoryReframe(
            original_narrative=story,
            reframed_narrative=reframed,
            reframing_technique=technique,
            therapeutic_intent=reframing_prompt,
            empowerment_level=empowerment
        )
    
    async def _generate_alternative_story(self, dominant_story: str, problem_story: Optional[str],
                                        unique_outcomes: List[str], context: NarrativeContext) -> Optional[str]:
        """Generate alternative/preferred story"""
        
        if not unique_outcomes:
            return None
            
        if self.ai_enabled:
            try:
                prompt = f"""
                Create an alternative story that incorporates these unique outcomes and contradicts the problem narrative.
                
                Dominant Story: "{dominant_story}"
                Problem Story: "{problem_story or 'Not identified'}"
                Unique Outcomes: {json.dumps(unique_outcomes)}
                Values: {json.dumps(context.identified_values) if context.identified_values else "Not specified"}
                
                Guidelines:
                - Build on the unique outcomes as evidence of alternative identity
                - Create a richer, more empowering narrative
                - Include the person's values, skills, and knowledge
                - Make it specific and grounded in their experiences
                - Maintain authenticity while expanding possibilities
                - 2-4 sentences
                
                Example: "You are someone who has faced The Worry Monster and found ways to quiet its voice. Your courage in seeking support and your determination to grow show a person committed to living according to their values of authenticity and connection."
                """
                
                response = await self._make_ai_request(prompt, max_tokens=200)
                return response.strip()
                
            except Exception as e:
                self.logger.error(f"AI alternative story generation failed: {e}")
                return await self._generate_alternative_story_fallback(unique_outcomes)
        else:
            return await self._generate_alternative_story_fallback(unique_outcomes)
    
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
    async def _identify_dominant_story_fallback(self, text: str) -> str:
        """Rule-based dominant story identification"""
        
        text_lower = text.lower()
        
        # Look for identity statements
        identity_markers = ["i am", "i'm", "i always", "i never", "people say i"]
        dominant_themes = []
        
        for marker in identity_markers:
            if marker in text_lower:
                # Extract text after marker
                start = text_lower.find(marker) + len(marker)
                end = text_lower.find('.', start)
                if end == -1:
                    end = min(start + 50, len(text_lower))
                theme = text[start:end].strip()
                if theme:
                    dominant_themes.append(theme)
        
        if dominant_themes:
            return f"The person describes themselves as {', '.join(dominant_themes[:2])}"
        else:
            return "The dominant story reflects someone navigating life challenges and seeking understanding"
    
    async def _identify_problem_story_fallback(self, text: str) -> Optional[str]:
        """Rule-based problem story identification"""
        
        problem_indicators = [
            "problem", "struggle", "can't", "never able", "always fail",
            "broken", "damaged", "worthless", "hopeless"
        ]
        
        text_lower = text.lower()
        problems_found = []
        
        for indicator in problem_indicators:
            if indicator in text_lower:
                problems_found.append(indicator)
        
        if len(problems_found) >= 2:
            return f"The problem story focuses on feelings of {' and '.join(problems_found[:2])}"
        
        return None
    
    async def _find_unique_outcomes_fallback(self, text: str, problem_story: str) -> List[UniqueOutcome]:
        """Rule-based unique outcomes detection"""
        
        outcomes = []
        outcome_indicators = [
            "but sometimes", "except when", "although", "there was a time",
            "i managed to", "i was able to", "successfully", "overcame"
        ]
        
        text_lower = text.lower()
        
        for i, indicator in enumerate(outcome_indicators[:3]):
            if indicator in text_lower:
                outcomes.append(UniqueOutcome(
                    outcome_id=str(uuid.uuid4())[:8],
                    description=f"A time when they {indicator} handle things differently",
                    significance="Shows capacity for change and resilience",
                    theme=NarrativeTheme.RESILIENCE,
                    strength_revealed="Adaptability and inner strength"
                ))
        
        return outcomes
    
    async def _externalize_problem_fallback(self, problem: str) -> str:
        """Rule-based problem externalization"""
        
        problem_lower = problem.lower()
        
        if "anxiety" in problem_lower:
            return "The Anxiety seems to visit you frequently, trying to convince you that danger lurks everywhere"
        elif "depression" in problem_lower:
            return "The Heavy Cloud has been following you, dimming the colors of your world"
        elif "anger" in problem_lower:
            return "The Fury shows up uninvited, trying to take control of your words and actions"
        elif "fear" in problem_lower:
            return "The Fear whispers stories of what might go wrong, keeping you from taking steps forward"
        else:
            return f"This Problem has been influencing your story, but it is not who you are"
    
    async def _reframe_story_fallback(self, story: str, technique: str) -> str:
        """Rule-based story reframing"""
        
        if technique == "strengths_based":
            return f"Your journey through {story} reveals your courage and determination to seek growth and understanding"
        elif technique == "values_focused":
            return f"Even in difficult times, you continue to honor what matters most to you"
        elif technique == "agency_highlighting":
            return f"You have been making choices to navigate these challenges, showing your capacity to influence your own story"
        else:
            return f"Your story shows someone actively working to create the life they want to live"
    
    async def _generate_alternative_story_fallback(self, unique_outcomes: List[str]) -> str:
        """Rule-based alternative story generation"""
        
        if unique_outcomes:
            return f"You are someone who has shown {unique_outcomes[0]}. This reveals a person with hidden strengths and the ability to write new chapters in their story"
        else:
            return "You are in the process of discovering new aspects of yourself and exploring different ways of being in the world"
    
    # Helper Methods
    async def _parse_unique_outcome(self, outcome_text: str, index: int) -> UniqueOutcome:
        """Parse unique outcome from text"""
        
        lines = outcome_text.strip().split('\n')
        description = ""
        significance = ""
        strength = ""
        
        for line in lines:
            if line.startswith("Description:"):
                description = line.replace("Description:", "").strip()
            elif line.startswith("Significance:"):
                significance = line.replace("Significance:", "").strip()
            elif line.startswith("Strength:"):
                strength = line.replace("Strength:", "").strip()
        
        return UniqueOutcome(
            outcome_id=str(uuid.uuid4())[:8],
            description=description or "Unnamed unique outcome",
            significance=significance or "Shows potential for change",
            theme=NarrativeTheme.RESILIENCE,
            strength_revealed=strength or "Hidden strength"
        )
    
    async def _identify_narrative_themes(self, text: str, dominant_story: str, 
                                       alternative_story: Optional[str]) -> List[NarrativeTheme]:
        """Identify key themes in narratives"""
        
        themes = []
        all_text = f"{text} {dominant_story} {alternative_story or ''}".lower()
        
        theme_keywords = {
            NarrativeTheme.IDENTITY: ["who i am", "identity", "self", "authentic"],
            NarrativeTheme.RELATIONSHIPS: ["relationship", "connection", "family", "friends", "loved ones"],
            NarrativeTheme.ACHIEVEMENT: ["success", "accomplish", "achieve", "goal"],
            NarrativeTheme.BELONGING: ["belong", "fit in", "community", "accepted"],
            NarrativeTheme.PURPOSE: ["purpose", "meaning", "why", "mission"],
            NarrativeTheme.RESILIENCE: ["overcome", "strength", "survive", "bounce back"],
            NarrativeTheme.AGENCY: ["choice", "control", "decide", "power"],
            NarrativeTheme.VALUES: ["values", "believe", "important", "matters"]
        }
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                themes.append(theme)
        
        return themes[:4]  # Return top 4 themes
    
    async def _assess_values_alignment(self, story: str, identified_values: Dict[str, float]) -> Dict[str, float]:
        """Assess how well the story aligns with identified values"""
        
        if not identified_values:
            return {"authenticity": 0.7, "growth": 0.8, "connection": 0.6}
        
        alignment = {}
        story_lower = story.lower()
        
        for value, importance in identified_values.items():
            # Simple keyword matching for alignment
            value_present = value.lower() in story_lower
            alignment[value] = min(1.0, importance * (0.8 if value_present else 0.4))
        
        return alignment
    
    async def _calculate_analysis_confidence(self, dominant_story: str, problem_story: Optional[str],
                                           unique_outcomes: List[UniqueOutcome], 
                                           alternative_story: Optional[str]) -> float:
        """Calculate confidence in narrative analysis"""
        
        base_confidence = 0.7
        
        # Factors that increase confidence
        if len(dominant_story) > 50:
            base_confidence += 0.1
        if problem_story and len(problem_story) > 30:
            base_confidence += 0.05
        if len(unique_outcomes) >= 2:
            base_confidence += 0.1
        if alternative_story and len(alternative_story) > 50:
            base_confidence += 0.05
        
        # AI vs fallback factor
        if self.ai_enabled:
            base_confidence += 0.1
        
        return min(0.95, base_confidence)
    
    async def _calculate_empowerment_level(self, original: str, reframed: str) -> float:
        """Calculate empowerment level of reframed story"""
        
        empowerment_keywords = [
            "strength", "capable", "choice", "power", "agency",
            "overcome", "resilient", "courageous", "determined"
        ]
        
        reframed_lower = reframed.lower()
        empowerment_score = sum(1 for keyword in empowerment_keywords if keyword in reframed_lower)
        
        return min(1.0, 0.5 + (empowerment_score * 0.1))
    
    def _load_externalization_templates(self) -> Dict[str, str]:
        """Load problem externalization templates"""
        
        return {
            "anxiety": "The Worry Voice that tries to predict disasters",
            "depression": "The Gray Fog that obscures your view",
            "anger": "The Fire that burns without your permission",
            "shame": "The Harsh Judge that never rests",
            "perfectionism": "The Impossible Standard that moves its goalposts",
            "fear": "The Alarm Bell that rings too often"
        }
    
    def _load_reframing_strategies(self) -> Dict[str, str]:
        """Load story reframing strategies"""
        
        return {
            "strengths_based": "Focus on hidden strengths, skills, and knowledge demonstrated in the story",
            "values_focused": "Highlight how the person's actions connect to their deep values",
            "agency_highlighting": "Emphasize choices made and influence exercised",
            "exception_finding": "Build on unique outcomes and exceptions to the problem story",
            "future_oriented": "Create a bridge from current story to preferred future",
            "resource_identifying": "Identify internal and external resources available"
        }