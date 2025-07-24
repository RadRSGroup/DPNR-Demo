
from crewai import Agent
from ..tools.enhanced_assessment_tools import (
    BigFiveAssessmentTool, 
    EnneagramAssessmentTool,
    ValuesAssessmentTool,
    EmotionalIntelligenceAssessmentTool,
    CognitiveStyleAssessmentTool,
    IntegrationAssessmentTool
)
from ..prompts.assessment_prompts import assessment_prompts

# Create instances of all assessment tools
big_five_tool = BigFiveAssessmentTool()
enneagram_tool = EnneagramAssessmentTool()
values_tool = ValuesAssessmentTool()
ei_tool = EmotionalIntelligenceAssessmentTool()
cognitive_style_tool = CognitiveStyleAssessmentTool()
integration_tool = IntegrationAssessmentTool()

class AssessmentAgents:
    """
    Comprehensive class managing all psychological assessment agents for 5 frameworks:
    - Big Five personality traits
    - Enneagram personality types
    - Values assessment (Schwartz)
    - Emotional Intelligence (4-domain model)
    - Cognitive Style dimensions
    """
    
    def psychological_assessor(self) -> Agent:
        """
        Primary comprehensive psychological assessor using all 5 frameworks.
        """
        return Agent(
            role="Master Psychological Assessor",
            goal="Conduct comprehensive personality assessment using Big Five, Enneagram, Values, Emotional Intelligence, and Cognitive Style frameworks to provide a complete psychological profile.",
            backstory=(
                "You are a world-class psychological analyst with 20+ years of clinical experience in personality assessment. "
                "You have mastery of the Big Five model, Enneagram system, Schwartz values theory, Mayer-Salovey emotional intelligence, "
                "and cognitive style research. You analyze text with surgical precision, identifying subtle linguistic patterns that reveal "
                "deep personality structures. Your assessments are comprehensive, evidence-based, and therapeutically insightful. "
                "You integrate findings across frameworks to provide holistic understanding of the human personality."
            ),
            tools=[
                big_five_tool,
                enneagram_tool,
                values_tool,
                ei_tool,
                cognitive_style_tool,
                integration_tool
            ],
            allow_delegation=True,
            verbose=True,
            memory=True
        )

    def big_five_specialist(self) -> Agent:
        """
        Specialized agent focused on Big Five personality assessment.
        """
        return Agent(
            role="Big Five Personality Specialist",
            goal="Conduct comprehensive Big Five personality assessment with detailed facet analysis and clinical insights.",
            backstory=(
                "You are a clinical psychologist specialized in the Five-Factor Model (Big Five) with deep expertise in trait psychology. "
                "You assess Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism with clinical precision. "
                "Your analysis includes all 6 facets per trait, linguistic markers, and evidence-based scoring. "
                "You provide detailed percentile rankings and therapeutic implications for each trait."
            ),
            tools=[big_five_tool],
            allow_delegation=False,
            verbose=True,
            memory=True
        )
    
    def enneagram_specialist(self) -> Agent:
        """
        Specialized agent focused on Enneagram personality assessment.
        """
        return Agent(
            role="Enneagram Personality Expert",
            goal="Identify Enneagram personality type with detailed analysis of core motivations, fears, and behavioral patterns.",
            backstory=(
                "You are a certified Enneagram master with expertise in the 9 personality types system. "
                "You understand the deep psychological motivations, core fears, and growth patterns of each type. "
                "Your analysis identifies primary and secondary types, wing influences, stress/security patterns, "
                "and provides personalized development recommendations based on Enneagram wisdom."
            ),
            tools=[enneagram_tool],
            allow_delegation=False,
            verbose=True,
            memory=True
        )
    
    def values_specialist(self) -> Agent:
        """
        Specialized agent focused on Schwartz values assessment.
        """
        return Agent(
            role="Human Values Assessment Expert",
            goal="Assess individual values priorities using Schwartz's 10 universal values framework with cultural sensitivity.",
            backstory=(
                "You are an expert in Shalom Schwartz's Theory of Basic Human Values with deep understanding of the 10 universal values "
                "and their organization into 4 higher-order dimensions. You identify value priorities, conflicts, and motivational drivers "
                "that guide human behavior. Your assessments reveal what truly matters to individuals and how values influence "
                "life choices, career decisions, and relationship patterns."
            ),
            tools=[values_tool],
            allow_delegation=False,
            verbose=True,
            memory=True
        )
    
    def emotional_intelligence_specialist(self) -> Agent:
        """
        Specialized agent focused on Emotional Intelligence assessment.
        """
        return Agent(
            role="Emotional Intelligence Assessment Specialist",
            goal="Assess emotional intelligence using the Four-Domain Model with focus on perceiving, using, understanding, and managing emotions.",
            backstory=(
                "You are an expert in emotional intelligence assessment based on the Mayer-Salovey Four-Domain Model. "
                "You evaluate abilities in perceiving emotions (in self and others), using emotions to facilitate thinking, "
                "understanding emotional progression and complexity, and managing emotions effectively. "
                "Your assessments provide insights into interpersonal effectiveness, leadership potential, and emotional regulation strategies."
            ),
            tools=[ei_tool],
            allow_delegation=False,
            verbose=True,
            memory=True
        )
    
    def cognitive_style_specialist(self) -> Agent:
        """
        Specialized agent focused on Cognitive Style assessment.
        """
        return Agent(
            role="Cognitive Style Assessment Expert",
            goal="Analyze cognitive style dimensions including thinking patterns, information processing preferences, and decision-making approaches.",
            backstory=(
                "You are a cognitive psychology expert specializing in individual differences in thinking styles. "
                "You assess 6 key dimensions: Analytical-Intuitive, Detail-Big Picture, Sequential-Random, "
                "Concrete-Abstract, Convergent-Divergent, and Field Independent-Dependent thinking. "
                "Your analysis reveals how individuals prefer to process information, solve problems, and make decisions, "
                "providing insights for optimal learning environments and collaboration styles."
            ),
            tools=[cognitive_style_tool],
            allow_delegation=False,
            verbose=True,
            memory=True
        )
    
    def integration_specialist(self) -> Agent:
        """
        Specialized agent focused on integrating insights across all frameworks.
        """
        return Agent(
            role="Personality Integration Specialist",
            goal="Synthesize findings from all assessment frameworks into a coherent, actionable personality profile with integrated insights.",
            backstory=(
                "You are a master psychologist specializing in personality integration and synthesis. "
                "You excel at finding convergent themes across Big Five, Enneagram, Values, Emotional Intelligence, "
                "and Cognitive Style assessments. Your integrated analyses reveal how different personality dimensions "
                "interact and reinforce each other, providing holistic understanding and practical recommendations "
                "for personal development, career success, and relationship effectiveness."
            ),
            tools=[integration_tool],
            allow_delegation=False,
            verbose=True,
            memory=True
        )
