from crewai import Crew
from unified_agent_system.agents.therapeutic_agents import TherapeuticAgents
from unified_agent_system.tasks.reporting_tasks import ReportingTasks

class ReportingCrew:
    def __init__(self):
        self.therapeutic_agents = TherapeuticAgents()
        self.reporting_tasks = ReportingTasks()

    def create_weekly_soul_summary_crew(self, context):
        reporting_agent = self.therapeutic_agents.reporting_agent()
        weekly_summary_task = self.reporting_tasks.weekly_summary_task(reporting_agent, context)

        crew = Crew(
            agents=[reporting_agent],
            tasks=[weekly_summary_task],
            verbose=True
        )
        return crew

    def get_status(self, task_id: str) -> dict:
        """
        Retrieves the status of a reporting task.
        This is a placeholder. In a real application, you would query a database
        or a task queue to get the actual status and result of the task.
        """
        # For demonstration, we'll return a dummy status
        # In a real system, you'd have a mechanism to store and retrieve task results
        # For now, assume success if task_id exists (which it will if kickoff was called)
        if task_id:
            return {"status": "completed", "result": {"summary": "This is a dummy weekly soul summary for task_id: " + task_id}}
        return {"status": "not_found"}