
from crewai import Task
from .agents import AssessmentAgents

class AssessmentTasks:
    """
    A class to define all tasks related to psychological assessment.
    """
    def personality_analysis_task(self, agent: Agent, text: str) -> Task:
        """
        Defines the task for analyzing a piece of text to create a personality profile.
        The task is assigned to a specific agent and provided with the text to analyze.
        """
        return Task(
            description=f"Analyze the following text to create a comprehensive personality profile. "
                        f"Identify the user's Big Five and Enneagram types, providing detailed scores and evidence for each. "
                        f"Text to analyze: \n\n---\n{text}\n---",
            expected_output="A JSON object containing two main keys: 'big_five_profile' and 'enneagram_profile'. "
                            "Each key should contain the detailed assessment results from the respective tool, "
                            "including scores, interpretations, and evidence.",
            agent=agent,
            async_execution=True
        )
