
from crewai import Task, Agent
from typing import Dict, Any

class AssessmentTasks:
    """
    Comprehensive class managing all psychological assessment tasks for 5 frameworks:
    - Big Five personality traits
    - Enneagram personality types  
    - Values assessment (Schwartz)
    - Emotional Intelligence (4-domain model)
    - Cognitive Style dimensions
    """
    
    def comprehensive_personality_analysis_task(self, agent: Agent, text: str) -> Task:
        """
        Master task for comprehensive personality assessment across all 5 frameworks.
        """
        return Task(
            description=(
                f"Conduct a comprehensive personality assessment using ALL five psychological frameworks:\n\n"
                f"1. **Big Five Personality Traits**: Assess Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism\n"
                f"2. **Enneagram Types**: Identify core type, motivations, fears, and behavioral patterns\n"
                f"3. **Values Assessment**: Evaluate Schwartz's 10 universal values and priorities\n"
                f"4. **Emotional Intelligence**: Assess 4-domain EI model (perceiving, using, understanding, managing emotions)\n"
                f"5. **Cognitive Style**: Analyze thinking patterns and information processing preferences\n\n"
                f"**Text to analyze:**\n\n---\n{text}\n---\n\n"
                f"**Instructions:**\n"
                f"- Use ALL available assessment tools\n"
                f"- Provide detailed evidence and confidence scores\n"
                f"- Generate integrated insights across frameworks\n"
                f"- Include therapeutic and development recommendations\n"
                f"- Ensure clinical-grade accuracy and depth"
            ),
            expected_output=(
                "A comprehensive JSON object with the following structure:\n"
                "```json\n"
                "{\n"
                "  'assessment_summary': 'Overall personality profile summary',\n"
                "  'big_five_profile': { detailed Big Five results },\n"
                "  'enneagram_profile': { detailed Enneagram results },\n"
                "  'values_profile': { detailed Values assessment },\n"
                "  'emotional_intelligence_profile': { detailed EI assessment },\n"
                "  'cognitive_style_profile': { detailed Cognitive Style results },\n"
                "  'integrated_insights': [ cross-framework themes and patterns ],\n"
                "  'development_recommendations': [ personalized growth suggestions ],\n"
                "  'overall_confidence': float,\n"
                "  'assessment_metadata': { processing details and quality metrics }\n"
                "}\n"
                "```"
            ),
            agent=agent,
            async_execution=True,
            memory=True
        )
    
    def big_five_analysis_task(self, agent: Agent, text: str, analysis_depth: str = "standard") -> Task:
        """
        Specialized task for Big Five personality assessment.
        """
        return Task(
            description=(
                f"Conduct comprehensive Big Five personality assessment with {analysis_depth} depth:\n\n"
                f"**Assessment Requirements:**\n"
                f"- Analyze all 5 traits: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism\n"
                f"- Provide facet-level analysis (6 facets per trait)\n"
                f"- Include percentile scores and clinical interpretations\n"
                f"- Identify linguistic markers and behavioral evidence\n"
                f"- Generate therapeutic implications and recommendations\n\n"
                f"**Text to analyze:**\n\n---\n{text}\n---"
            ),
            expected_output=(
                "Detailed Big Five assessment JSON containing:\n"
                "- Trait scores and percentiles\n"
                "- Facet-level breakdowns\n"
                "- Evidence and linguistic markers\n"
                "- Clinical interpretations\n"
                "- Personality summary and recommendations"
            ),
            agent=agent,
            async_execution=True
        )
    
    def enneagram_analysis_task(self, agent: Agent, text: str, include_wings: bool = True) -> Task:
        """
        Specialized task for Enneagram personality assessment.
        """
        return Task(
            description=(
                f"Conduct detailed Enneagram personality type assessment:\n\n"
                f"**Assessment Requirements:**\n"
                f"- Identify primary Enneagram type (1-9)\n"
                f"- Analyze core motivations, fears, and desires\n"
                f"- Examine behavioral patterns and stress/growth directions\n"
                f"- {'Include wing analysis (adjacent types)' if include_wings else 'Focus on core type only'}\n"
                f"- Provide growth recommendations and integration opportunities\n\n"
                f"**Text to analyze:**\n\n---\n{text}\n---"
            ),
            expected_output=(
                "Comprehensive Enneagram assessment JSON containing:\n"
                "- Primary and secondary type identification\n"
                "- Core motivations and behavioral evidence\n"
                "- Stress and security patterns\n"
                "- Wing influences (if requested)\n"
                "- Development recommendations and growth paths"
            ),
            agent=agent,
            async_execution=True
        )
    
    def values_analysis_task(self, agent: Agent, text: str, cultural_context: str = None) -> Task:
        """
        Specialized task for Schwartz values assessment.
        """
        cultural_note = f" with consideration for {cultural_context} cultural context" if cultural_context else ""
        
        return Task(
            description=(
                f"Conduct comprehensive values assessment using Schwartz's 10 universal values{cultural_note}:\n\n"
                f"**Assessment Requirements:**\n"
                f"- Assess all 10 values: Self-Direction, Stimulation, Hedonism, Achievement, Power, Security, Conformity, Tradition, Benevolence, Universalism\n"
                f"- Identify value priorities and hierarchies\n"
                f"- Analyze 4 higher-order dimensions (Openness vs Conservation, Self-Enhancement vs Self-Transcendence)\n"
                f"- Detect value conflicts and integration opportunities\n"
                f"- Generate motivational insights and life choice implications\n\n"
                f"**Text to analyze:**\n\n---\n{text}\n---"
            ),
            expected_output=(
                "Comprehensive values assessment JSON containing:\n"
                "- Individual value scores and importance levels\n"
                "- Value priority rankings\n"
                "- Higher-order dimension analysis\n"
                "- Value conflicts and tensions\n"
                "- Motivational insights and recommendations"
            ),
            agent=agent,
            async_execution=True
        )
    
    def emotional_intelligence_analysis_task(self, agent: Agent, text: str, focus_domains: list = None) -> Task:
        """
        Specialized task for Emotional Intelligence assessment.
        """
        domain_focus = f" with emphasis on {', '.join(focus_domains)}" if focus_domains else ""
        
        return Task(
            description=(
                f"Conduct comprehensive Emotional Intelligence assessment using the Four-Domain Model{domain_focus}:\n\n"
                f"**Assessment Requirements:**\n"
                f"- Assess all 4 domains: Perceiving, Using, Understanding, and Managing Emotions\n"
                f"- Analyze emotional vocabulary richness and complexity\n"
                f"- Evaluate emotion regulation strategies and patterns\n"
                f"- Assess interpersonal emotional competencies\n"
                f"- Generate leadership and relationship insights\n\n"
                f"**Text to analyze:**\n\n---\n{text}\n---"
            ),
            expected_output=(
                "Detailed EI assessment JSON containing:\n"
                "- Domain scores and competency levels\n"
                "- Emotional profile and regulation style\n"
                "- Strengths and development priorities\n"
                "- Interpersonal and leadership implications\n"
                "- EI development recommendations"
            ),
            agent=agent,
            async_execution=True
        )
    
    def cognitive_style_analysis_task(self, agent: Agent, text: str, dimensions: list = None) -> Task:
        """
        Specialized task for Cognitive Style assessment.
        """
        dimension_focus = f" focusing on {', '.join(dimensions)}" if dimensions else ""
        
        return Task(
            description=(
                f"Conduct comprehensive Cognitive Style assessment{dimension_focus}:\n\n"
                f"**Assessment Requirements:**\n"
                f"- Analyze 6 cognitive dimensions: Analytical-Intuitive, Detail-Big Picture, Sequential-Random, Concrete-Abstract, Convergent-Divergent, Field Independent-Dependent\n"
                f"- Identify thinking patterns and information processing preferences\n"
                f"- Assess decision-making and problem-solving styles\n"
                f"- Determine optimal learning and work environments\n"
                f"- Generate cognitive strengths and development suggestions\n\n"
                f"**Text to analyze:**\n\n---\n{text}\n---"
            ),
            expected_output=(
                "Comprehensive cognitive style assessment JSON containing:\n"
                "- Dimensional scores and style categories\n"
                "- Thinking pattern analysis and implications\n"
                "- Cognitive strengths and potential blind spots\n"
                "- Optimal environments and collaboration insights\n"
                "- Development suggestions for cognitive flexibility"
            ),
            agent=agent,
            async_execution=True
        )
    
    def integration_synthesis_task(self, agent: Agent, assessment_results: Dict[str, Any]) -> Task:
        """
        Specialized task for integrating insights across all assessment frameworks.
        """
        return Task(
            description=(
                f"Synthesize and integrate findings from all personality assessment frameworks:\n\n"
                f"**Integration Requirements:**\n"
                f"- Identify convergent themes across Big Five, Enneagram, Values, EI, and Cognitive Style\n"
                f"- Analyze framework interactions and reinforcing patterns\n"
                f"- Generate holistic personality synthesis\n"
                f"- Create integrated development roadmap\n"
                f"- Provide practical applications for career, relationships, and growth\n\n"
                f"**Assessment Results to Integrate:**\n"
                f"{assessment_results}"
            ),
            expected_output=(
                "Integrated personality analysis JSON containing:\n"
                "- Convergent themes across frameworks\n"
                "- Framework interaction insights\n"
                "- Holistic personality synthesis\n"
                "- Integrated development opportunities\n"
                "- Practical applications and recommendations"
            ),
            agent=agent,
            async_execution=True,
            memory=True
        )
    
    def quality_validation_task(self, agent: Agent, assessment_results: Dict[str, Any], 
                               original_text: str, confidence_threshold: float = 0.75) -> Task:
        """
        Task for validating assessment quality and consistency.
        """
        return Task(
            description=(
                f"Validate assessment results for quality, consistency, and confidence:\n\n"
                f"**Validation Requirements:**\n"
                f"- Check confidence scores against threshold ({confidence_threshold})\n"
                f"- Verify consistency across frameworks\n"
                f"- Identify contradictions or low-confidence assessments\n"
                f"- Flag assessments requiring recursive analysis\n"
                f"- Ensure evidence quality and assessment depth\n\n"
                f"**Assessment Results:**\n{assessment_results}\n\n"
                f"**Original Text:**\n---\n{original_text}\n---"
            ),
            expected_output=(
                "Quality validation report JSON containing:\n"
                "- Overall quality score and confidence metrics\n"
                "- Consistency analysis across frameworks\n"
                "- Identified issues or low-confidence areas\n"
                "- Recommendations for improvement or re-analysis\n"
                "- Final validation status (approved/requires_revision)"
            ),
            agent=agent,
            async_execution=True
        )
    
    def therapeutic_insights_task(self, agent: Agent, assessment_results: Dict[str, Any]) -> Task:
        """
        Task for generating therapeutic insights and growth recommendations.
        """
        return Task(
            description=(
                f"Generate therapeutic insights and growth-oriented recommendations:\n\n"
                f"**Therapeutic Analysis Requirements:**\n"
                f"- Identify therapeutic leverage points for growth\n"
                f"- Detect potential areas of psychological stuckness\n"
                f"- Recommend therapeutic modalities and approaches\n"
                f"- Generate relationship and interpersonal insights\n"
                f"- Create actionable personal development strategies\n\n"
                f"**Assessment Results:**\n{assessment_results}"
            ),
            expected_output=(
                "Therapeutic insights JSON containing:\n"
                "- Key therapeutic leverage points\n"
                "- Growth opportunities and challenges\n"
                "- Recommended therapeutic approaches\n"
                "- Relationship and interpersonal patterns\n"
                "- Actionable development strategies"
            ),
            agent=agent,
            async_execution=True
        )
    
    # Legacy method for backward compatibility
    def personality_analysis_task(self, agent: Agent, text: str) -> Task:
        """
        Legacy method - redirects to comprehensive analysis.
        """
        return self.comprehensive_personality_analysis_task(agent, text)
