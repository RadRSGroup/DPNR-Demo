from crewai import Task
from unified_agent_system.prompts.reporting_prompts import ReportingPrompts

class ReportingTasks:
    def weekly_summary_task(self, agent, context) -> Task:
        return Task(
            description=ReportingPrompts.weekly_summary_description(),
            expected_output=ReportingPrompts.weekly_summary_expected_output(),
            agent=agent,
            context=context
        )