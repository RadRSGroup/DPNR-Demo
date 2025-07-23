from crewai import Task
from typing import Dict, Any
import sys
import os

# Add prompts directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import prompts
from prompts import ifs_prompts
from prompts import shadow_work_prompts
from prompts import pardes_prompts
from prompts import growth_tracker_prompts
from prompts import digital_twin_prompts

class TherapeuticTasks:
    """
    Task definitions for therapeutic CrewAI workflows.
    """
    
    def ifs_dialogue_task(self, agent, initial_text: str) -> Task:
        """
        Task for facilitating IFS dialogue with identified parts.
        """
        # Detect potential part type from initial text
        text_lower = initial_text.lower()
        part_type = "manager"  # Default
        
        if any(word in text_lower for word in ["hurt", "scared", "alone", "shame"]):
            part_type = "exile"
        elif any(word in text_lower for word in ["escape", "avoid", "numb", "angry"]):
            part_type = "firefighter"
            
        dialogue_template = ifs_prompts.PART_DIALOGUE_TEMPLATES.get(part_type)
        
        return Task(
            description=f"""
            Facilitate an Internal Family Systems dialogue session.
            
            Initial user input: {initial_text}
            
            Guidelines from IFS Framework:
            {ifs_prompts.SYSTEM_PROMPT}
            
            Dialogue approach for this part:
            - Greeting: {dialogue_template['greeting']}
            - Core validation: {dialogue_template['validation']}
            - Gentle inquiry: {dialogue_template['gentle_inquiry']}
            
            Suggested questions to explore:
            {chr(10).join(f"- {q}" for q in dialogue_template['questions'][:3])}
            
            Remember to maintain curiosity, compassion, and support Self-leadership emergence.
            """,
            agent=agent,
            expected_output="A therapeutic response that includes part identification, compassionate dialogue, and follow-up questions that deepen understanding."
        )
    
    def shadow_integration_task(self, agent, initial_text: str) -> Task:
        """
        Task for shadow work pattern detection and integration guidance.
        """
        # Detect shadow pattern type
        text_lower = initial_text.lower()
        pattern_type = "projection"  # Default
        
        if any(phrase in text_lower for phrase in ["i would never", "not me", "i'm not"]):
            pattern_type = "repression"
        elif any(phrase in text_lower for phrase in ["perfect", "always good", "never bad"]):
            pattern_type = "compensation"
            
        pattern_template = shadow_work_prompts.SHADOW_PATTERN_TEMPLATES.get(pattern_type)
        
        return Task(
            description=f"""
            Conduct Jungian Shadow Work analysis and integration.
            
            User input to analyze: {initial_text}
            
            Shadow Work Framework:
            {shadow_work_prompts.SYSTEM_PROMPT}
            
            Detected pattern type: {pattern_type}
            
            Integration approach:
            {pattern_template['integration_prompt']}
            
            Key exploration areas:
            - Gift finding: {pattern_template.get('gift_finding', '')}
            - Acceptance support: {pattern_template.get('acceptance_support', '')}
            
            Integration process guidance:
            {shadow_work_prompts.INTEGRATION_PROCESS_PROMPTS['gift_extraction']}
            
            Remember: Shadow contains both poison and medicine. Help the user find the gold.
            """,
            agent=agent,
            expected_output="Shadow pattern analysis with compassionate integration guidance, focusing on the gifts within the shadow and practical steps for conscious integration."
        )
    
    def pardes_reflection_task(self, agent, initial_text: str) -> Task:
        """
        Task for multi-layer PaRDeS reflection framework.
        """
        return Task(
            description=f"""
            Provide a PaRDeS multi-layer reflection on the user's insight.
            
            User insight to reflect upon: {initial_text}
            
            PaRDeS Framework:
            {pardes_prompts.SYSTEM_PROMPT}
            
            Layer-by-layer guidance:
            
            1. PSHAT (Literal):
            {pardes_prompts.get_pshat_prompt(initial_text)}
            
            2. REMEZ (Emotional Pattern):
            {pardes_prompts.get_remez_prompt(initial_text)}
            
            3. DRASH (Life Lesson):
            {pardes_prompts.get_drash_prompt(initial_text)}
            
            4. SOD (Soul Truth):
            {pardes_prompts.get_sod_prompt(initial_text)}
            
            Metaphor creation guidance:
            {pardes_prompts.METAPHOR_GENERATION_PROMPTS['nature_metaphors']}
            
            Integration support:
            {pardes_prompts.INTEGRATION_GUIDANCE_TEMPLATES['bridging_levels']}
            
            Remember: Guide from surface understanding to soul-level truth with reverence.
            """,
            agent=agent,
            expected_output="A four-layer PaRDeS reflection that takes the user from literal understanding through emotional patterns and life lessons to soul-level truth, with metaphors and integration guidance."
        )
    
    def growth_tracking_task(self, agent, user_data: Dict[str, Any]) -> Task:
        """
        Task for analyzing growth patterns and providing insights.
        """
        return Task(
            description=f"""
            Analyze user growth patterns and provide personalized insights.
            
            User data: {user_data}
            
            Your task:
            1. Identify growth trends across psychological, emotional, and spiritual domains
            2. Detect breakthrough moments and significant developments
            3. Analyze progress against user's stated goals
            4. Provide encouraging feedback on achievements
            5. Suggest areas for continued focus and development
            6. Generate personalized growth recommendations
            
            Create a compassionate and motivating growth analysis.
            """,
            agent=agent,
            expected_output="Comprehensive growth analysis with trends, insights, and personalized recommendations."
        )
    
    def digital_twin_evolution_task(self, agent, trigger_event: str, current_twin: Dict[str, Any]) -> Task:
        """
        Task for evolving the user's digital twin based on new insights.
        """
        return Task(
            description=f"""
            Evolve the user's digital twin based on a significant life event or insight.
            
            Trigger event: {trigger_event}
            Current twin state: {current_twin}
            
            Your task:
            1. Analyze how the trigger event impacts the user's soul archetype
            2. Identify areas of archetypal evolution and growth
            3. Update the digital twin's characteristics and representation
            4. Generate new symbolic representations if needed
            5. Document the evolution timeline and significance
            6. Provide insights on the spiritual development represented
            
            Create a meaningful evolution that honors the user's growth journey.
            """,
            agent=agent,
            expected_output="Updated digital twin with evolution details, new characteristics, and spiritual insights."
        )