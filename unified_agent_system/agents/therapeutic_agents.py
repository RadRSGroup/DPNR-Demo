from crewai import Agent
import sys
import os

# Add prompts directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import prompts for each therapeutic modality
from prompts import ifs_prompts
from prompts import shadow_work_prompts  
from prompts import pardes_prompts
from prompts import growth_tracker_prompts
from prompts import digital_twin_prompts

class TherapeuticAgents:
    """
    A class to define agents focused on therapeutic modalities and spiritual frameworks.
    """
    def ifs_agent(self) -> Agent:
        """
        Agent specializing in Internal Family Systems (IFS). 
        Identifies parts (Managers, Firefighters, Exiles) and facilitates dialogue.
        """
        return Agent(
            role="Internal Family Systems (IFS) Facilitator",
            goal="To help the user identify and understand their internal parts (Managers, Firefighters, Exiles) and foster a compassionate inner dialogue.",
            backstory=ifs_prompts.SYSTEM_PROMPT,
            # tools=[IFSTool()], # To be created later
            allow_delegation=False,
            verbose=True
        )

    def shadow_work_agent(self) -> Agent:
        """
        Agent specializing in Jungian Shadow Work.
        Helps users identify and integrate their shadow aspects.
        """
        return Agent(
            role="Jungian Shadow Work Guide",
            goal="To help the user uncover and integrate their shadow self, transforming hidden patterns into sources of strength and wholeness.",
            backstory=shadow_work_prompts.SYSTEM_PROMPT,
            # tools=[ShadowPatternTool()], # To be created later
            allow_delegation=False,
            verbose=True
        )

    def pardes_reflection_agent(self) -> Agent:
        """
        Agent specializing in the PaRDeS multi-level reflection framework.
        Provides reflections at four different depths: Pshat, Remez, Drash, and Sod.
        """
        return Agent(
            role="Mystical Reflection Guide (PaRDeS Framework)",
            goal="To provide the user with multi-layered reflections on their experiences, moving from the literal to the metaphorical, the allegorical, and finally to the soul-level essence (Sod).",
            backstory=pardes_prompts.SYSTEM_PROMPT,
            # tools=[SodLayerTool()], # To be created later
            verbose=True
        )

    def reporting_agent(self) -> Agent:
        """
        Agent specializing in summarizing and reporting on user progress.
        """
        return Agent(
            role="Insightful Progress Reporter",
            goal="To synthesize the user's weekly progress, insights, and challenges into a clear, compassionate, and encouraging summary.",
            backstory="You are a data-driven storyteller with a heart. You can see the patterns in a user's journey and weave them into a narrative that is both informative and inspiring. You highlight wins, gently point out challenges, and always focus on the path of growth.",
            verbose=True
        )
    
    def growth_tracker_agent(self) -> Agent:
        """
        Agent specializing in tracking growth and progress across multiple domains.
        """
        return Agent(
            role="Growth Tracker Specialist",
            goal="To monitor, analyze, and provide insights on user's growth across psychological, emotional, and spiritual domains.",
            backstory=growth_tracker_prompts.SYSTEM_PROMPT,
            verbose=True
        )
    
    def digital_twin_agent(self) -> Agent:
        """
        Agent specializing in creating and evolving digital representations of user's soul archetype.
        """
        return Agent(
            role="Digital Twin Creator",
            goal="To create and evolve a comprehensive digital representation of the user's soul archetype and spiritual development.",
            backstory=digital_twin_prompts.SYSTEM_PROMPT,
            verbose=True
        )