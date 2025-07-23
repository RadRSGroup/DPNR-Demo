
from typing import Dict, Any
from crewai import Crew, Process

# Import from the new unified architecture
from ..agents.therapeutic_agents import TherapeuticAgents
from ..prompts.therapeutic_prompts import TherapeuticPrompts
from ..tasks.therapeutic_tasks import TherapeuticTasks

class MirrorRoomCrew:
    """
    Orchestrates a therapeutic session in the Mirror Room.
    This crew manages the interaction between different therapeutic agents.
    """
    def __init__(self):
        self.agents = TherapeuticAgents()
        self.prompts = TherapeuticPrompts()
        self.tasks = TherapeuticTasks()

    def run_session(self, initial_text: str, therapeutic_focus: str) -> Dict[str, Any]:
        """
        Runs a full therapeutic session based on the user's focus.
        """
        if therapeutic_focus == "IFS":
            agent = self.agents.ifs_agent()
            task = self.tasks.ifs_dialogue_task(agent, initial_text)
        elif therapeutic_focus == "Shadow Work":
            agent = self.agents.shadow_work_agent()
            task = self.tasks.shadow_integration_task(agent, initial_text)
        elif therapeutic_focus == "PaRDeS":
            agent = self.agents.pardes_reflection_agent()
            task = self.tasks.pardes_reflection_task(agent, initial_text)
        elif therapeutic_focus == "Growth Tracking":
            agent = self.agents.growth_tracker_agent()
            task = self.tasks.growth_tracking_task(agent, {"text": initial_text})
        elif therapeutic_focus == "Digital Twin":
            agent = self.agents.digital_twin_agent()
            task = self.tasks.digital_twin_evolution_task(agent, initial_text, {})
        else:
            raise ValueError(f"Unknown therapeutic focus: {therapeutic_focus}")

        # Assemble and run the crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=2
        )

        # Execute the crew and return results
        try:
            result = crew.kickoff()
            return {
                "success": True,
                "therapeutic_focus": therapeutic_focus,
                "result": result,
                "initial_text": initial_text
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "therapeutic_focus": therapeutic_focus,
                "initial_text": initial_text
            }
