
from crewai import Task
from .agents import TherapeuticAgents

class ReportingTasks:
    """
    A class to define all tasks related to reporting and summarizing user progress.
    """
    def weekly_summary_task(self, agent: Agent, user_id: str) -> Task:
        """
        Defines the task for generating a weekly summary for a specific user.
        This task would require a tool to fetch the user's data from the database.
        """
        return Task(
            description=f"Generate a weekly soul summary for user '{user_id}'. "
                        f"Fetch all of the user's assessment results, mirror room insights, and growth tracker data from the past 7 days. "
                        f"Synthesize this information into a compassionate and insightful narrative. "
                        f"Highlight key achievements, identify recurring themes or challenges, and offer a prompt for reflection for the week ahead.",
            expected_output="A JSON object containing the weekly summary, including 'achievements', 'challenges', 'key_insights', and a 'reflection_prompt'.",
            agent=agent,
            # In a real scenario, this task would be equipped with a tool to fetch user data.
            # tools=[DatabaseTool(user_id=user_id)]
        )
