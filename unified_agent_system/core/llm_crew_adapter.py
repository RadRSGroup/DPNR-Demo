"""
CrewAI LLM Adapter Integration
Bridges the new LLM adapter with CrewAI agents
"""

from typing import Optional, Dict, Any
from crewai import Agent
from crewai.llm import LLM
from .llm_adapter import LLMOrchestrator, LLMProvider, create_llm_orchestrator
from ..config import config
import logging

logger = logging.getLogger(__name__)

class CrewAILLMAdapter(LLM):
    """
    Custom LLM adapter that integrates our multi-provider LLM orchestrator
    with CrewAI's LLM interface
    """
    
    def __init__(
        self,
        orchestrator: LLMOrchestrator,
        preferred_provider: Optional[LLMProvider] = None,
        assessment_type: Optional[str] = None
    ):
        self.orchestrator = orchestrator
        self.preferred_provider = preferred_provider
        self.assessment_type = assessment_type
        super().__init__()
    
    async def _call(self, prompt: str, **kwargs) -> str:
        """
        CrewAI LLM interface implementation
        Routes to our multi-provider orchestrator
        """
        try:
            # Extract system prompt if provided
            system_prompt = kwargs.get("system_prompt")
            
            response = await self.orchestrator.generate_with_fallback(
                prompt=prompt,
                system_prompt=system_prompt,
                preferred_provider=self.preferred_provider,
                assessment_type=self.assessment_type
            )
            
            return response.content
            
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise

class EnhancedAssessmentAgent:
    """
    Enhanced assessment agent factory that creates agents with:
    - Multi-provider LLM support
    - Assessment-specific routing
    - Clinical model integration
    """
    
    def __init__(self):
        # Initialize LLM orchestrator
        self.llm_orchestrator = create_llm_orchestrator(
            openai_key=config.openai_api_key,
            anthropic_key=config.anthropic_api_key,
            gemini_key=config.gemini_api_key
        )
    
    def create_agent(
        self,
        role: str,
        goal: str,
        backstory: str,
        tools: list = None,
        assessment_type: str = None,
        preferred_provider: Optional[LLMProvider] = None
    ) -> Agent:
        """
        Create enhanced agent with multi-provider LLM support
        
        Args:
            role: Agent role description
            goal: Agent goal
            backstory: Agent backstory
            tools: List of tools for the agent
            assessment_type: Type of assessment for LLM routing
            preferred_provider: Preferred LLM provider
        """
        
        # Create custom LLM adapter
        llm_adapter = CrewAILLMAdapter(
            orchestrator=self.llm_orchestrator,
            preferred_provider=preferred_provider,
            assessment_type=assessment_type
        )
        
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools or [],
            llm=llm_adapter,
            allow_delegation=True,
            verbose=True,
            memory=True
        )
    
    def clinical_assessor(self) -> Agent:
        """
        Clinical assessor agent optimized for clinical frameworks
        Uses OpenAI GPT-4 for analytical precision
        """
        return self.create_agent(
            role="Clinical Psychological Assessor",
            goal="Conduct clinical-grade psychological assessments using evidence-based frameworks and scientific rigor.",
            backstory=(
                "You are a licensed clinical psychologist with expertise in psychometric assessment. "
                "You use validated psychological instruments and evidence-based frameworks including "
                "Big Five, emotional intelligence, and cognitive style assessment. Your analyses are "
                "precise, clinically informed, and backed by peer-reviewed research."
            ),
            assessment_type="clinical",
            preferred_provider=LLMProvider.OPENAI
        )
    
    def soul_level_assessor(self) -> Agent:
        """
        Soul-level assessor agent optimized for mystical frameworks
        Uses Anthropic Claude for nuanced understanding
        """
        return self.create_agent(
            role="Soul-Level Consciousness Assessor",
            goal="Conduct deep soul-level assessments using mystical and spiritual frameworks to reveal hidden patterns.",
            backstory=(
                "You are a master of consciousness studies and mystical psychology with deep understanding "
                "of Kabbalistic Sefirot, Jungian shadow work, Internal Family Systems, and PaRDeS interpretation. "
                "You perceive subtle energetic patterns and soul-level dynamics that reveal the deeper "
                "structure of human consciousness and spiritual development."
            ),
            assessment_type="soul_level",
            preferred_provider=LLMProvider.ANTHROPIC
        )
    
    def hybrid_assessor(self) -> Agent:
        """
        Hybrid assessor that combines clinical and soul-level insights
        Uses Gemini for balanced integration
        """
        return self.create_agent(
            role="Integrative Personality Assessor",
            goal="Integrate clinical psychological frameworks with soul-level insights for comprehensive understanding.",
            backstory=(
                "You are a pioneering psychologist who bridges scientific psychology with transpersonal "
                "and spiritual frameworks. You seamlessly integrate Big Five, Enneagram, values assessment "
                "with deeper soul-level patterns from Sefirot, shadow work, and consciousness studies. "
                "Your assessments honor both empirical rigor and spiritual wisdom."
            ),
            assessment_type="hybrid",
            preferred_provider=LLMProvider.GEMINI
        )
    
    def therapeutic_insights_specialist(self) -> Agent:
        """
        Specialist for generating therapeutic insights and recommendations
        """
        return self.create_agent(
            role="Therapeutic Insights Specialist",
            goal="Generate actionable therapeutic insights and personalized growth recommendations from assessment data.",
            backstory=(
                "You are a master therapist with 25+ years of experience across multiple modalities. "
                "You excel at translating assessment results into practical therapeutic interventions, "
                "growth strategies, and healing pathways. Your recommendations are compassionate, "
                "evidence-based, and tailored to each individual's unique journey."
            ),
            assessment_type="therapeutic",
            preferred_provider=LLMProvider.ANTHROPIC
        )
    
    def quality_validator(self) -> Agent:
        """
        Quality validation agent for assessment accuracy
        """
        return self.create_agent(
            role="Assessment Quality Validator",
            goal="Validate assessment quality, consistency, and clinical accuracy across all frameworks.",
            backstory=(
                "You are a psychometric expert and research methodologist with deep expertise in "
                "assessment validity and reliability. You ensure all assessments meet clinical "
                "standards, identify inconsistencies, and flag results requiring recursive analysis. "
                "Your validation process maintains the highest standards of psychological assessment."
            ),
            assessment_type="validation",
            preferred_provider=LLMProvider.OPENAI
        )
    
    def assessment_coordinator(self) -> Agent:
        """
        Coordinator agent for managing complex assessment workflows
        """
        return self.create_agent(
            role="Assessment Workflow Coordinator",
            goal="Coordinate complex multi-framework assessments and ensure optimal processing flow.",
            backstory=(
                "You are an expert in psychological assessment workflows and process optimization. "
                "You coordinate between clinical and soul-level assessors, manage quality validation, "
                "and ensure comprehensive integration of all assessment frameworks. Your leadership "
                "ensures efficient, thorough, and accurate assessment processes."
            ),
            assessment_type="coordination",
            preferred_provider=LLMProvider.GEMINI
        )

# Factory function to create enhanced agents
def create_enhanced_agents() -> EnhancedAssessmentAgent:
    """Create enhanced assessment agent factory"""
    return EnhancedAssessmentAgent()

# Backward compatibility - update existing AssessmentAgents class
class UpdatedAssessmentAgents:
    """
    Updated assessment agents class that uses the new LLM adapter
    while maintaining backward compatibility
    """
    
    def __init__(self):
        self.enhanced_factory = create_enhanced_agents()
        
        # Import original tools
        from ..tools.assessment_tools import (
            BigFiveAssessmentTool, 
            EnneagramAssessmentTool,
            ValuesAssessmentTool,
            EmotionalIntelligenceAssessmentTool,
            CognitiveStyleAssessmentTool,
            IntegrationAssessmentTool
        )
        
        self.tools = {
            'big_five': BigFiveAssessmentTool(),
            'enneagram': EnneagramAssessmentTool(),
            'values': ValuesAssessmentTool(),
            'ei': EmotionalIntelligenceAssessmentTool(),
            'cognitive_style': CognitiveStyleAssessmentTool(),
            'integration': IntegrationAssessmentTool()
        }
    
    def psychological_assessor(self) -> Agent:
        """Comprehensive psychological assessor with multi-provider LLM"""
        return self.enhanced_factory.create_agent(
            role="Master Psychological Assessor",
            goal="Conduct comprehensive personality assessment using all frameworks to provide complete psychological profile.",
            backstory=(
                "You are a world-class psychological analyst with 20+ years of clinical experience. "
                "You have mastery of Big Five, Enneagram, Schwartz values, emotional intelligence, "
                "and cognitive style frameworks. Your assessments are comprehensive, evidence-based, "
                "and therapeutically insightful."
            ),
            tools=list(self.tools.values()),
            assessment_type="comprehensive",
            preferred_provider=LLMProvider.OPENAI
        )
    
    def big_five_specialist(self) -> Agent:
        """Big Five specialist with clinical LLM routing"""
        return self.enhanced_factory.create_agent(
            role="Big Five Personality Specialist",
            goal="Conduct comprehensive Big Five assessment with detailed facet analysis.",
            backstory=(
                "You are a clinical psychologist specialized in the Five-Factor Model with deep "
                "expertise in trait psychology. You assess all traits with clinical precision "
                "and provide detailed percentile rankings and therapeutic implications."
            ),
            tools=[self.tools['big_five']],
            assessment_type="big_five",
            preferred_provider=LLMProvider.OPENAI
        )
    
    def enneagram_specialist(self) -> Agent:
        """Enneagram specialist with hybrid LLM routing"""
        return self.enhanced_factory.create_agent(
            role="Enneagram Personality Expert",
            goal="Identify Enneagram type with detailed analysis of core motivations and patterns.",
            backstory=(
                "You are a certified Enneagram master with expertise in the 9 types system. "
                "You understand deep psychological motivations, core fears, and growth patterns. "
                "Your analysis includes wings, stress/security patterns, and development recommendations."
            ),
            tools=[self.tools['enneagram']],
            assessment_type="enneagram",
            preferred_provider=LLMProvider.GEMINI
        )
    
    def values_specialist(self) -> Agent:
        """Values specialist with hybrid LLM routing"""
        return self.enhanced_factory.create_agent(
            role="Human Values Assessment Expert",
            goal="Assess values priorities using Schwartz framework with cultural sensitivity.",
            backstory=(
                "You are an expert in Schwartz's Theory of Basic Human Values with deep understanding "
                "of 10 universal values and their organization. You identify value priorities, conflicts, "
                "and motivational drivers that guide human behavior and life choices."
            ),
            tools=[self.tools['values']],
            assessment_type="values",
            preferred_provider=LLMProvider.GEMINI
        )
    
    def emotional_intelligence_specialist(self) -> Agent:
        """EI specialist with clinical LLM routing"""
        return self.enhanced_factory.create_agent(
            role="Emotional Intelligence Assessment Specialist",
            goal="Assess emotional intelligence using Four-Domain Model.",
            backstory=(
                "You are an expert in emotional intelligence based on Mayer-Salovey Four-Domain Model. "
                "You evaluate perceiving, using, understanding, and managing emotions. Your assessments "
                "provide insights into interpersonal effectiveness and emotional regulation strategies."
            ),
            tools=[self.tools['ei']],
            assessment_type="emotional_intelligence",
            preferred_provider=LLMProvider.OPENAI
        )
    
    def cognitive_style_specialist(self) -> Agent:
        """Cognitive style specialist with clinical LLM routing"""
        return self.enhanced_factory.create_agent(
            role="Cognitive Style Assessment Expert",
            goal="Analyze cognitive style dimensions and thinking patterns.",
            backstory=(
                "You are a cognitive psychology expert specializing in individual differences in thinking. "
                "You assess 6 key dimensions and reveal how individuals process information, solve problems, "
                "and make decisions, providing insights for optimal learning and collaboration."
            ),
            tools=[self.tools['cognitive_style']],
            assessment_type="cognitive_style",
            preferred_provider=LLMProvider.OPENAI
        )
    
    def integration_specialist(self) -> Agent:
        """Integration specialist with hybrid LLM routing"""
        return self.enhanced_factory.integration_specialist()
    
    def therapeutic_insights_specialist(self) -> Agent:
        """Therapeutic insights specialist"""
        return self.enhanced_factory.therapeutic_insights_specialist()
    
    def quality_validator(self) -> Agent:
        """Quality validator"""
        return self.enhanced_factory.quality_validator()
    
    def assessment_coordinator(self) -> Agent:
        """Assessment coordinator"""
        return self.enhanced_factory.assessment_coordinator()