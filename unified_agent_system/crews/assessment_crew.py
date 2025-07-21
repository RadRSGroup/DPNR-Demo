import uuid
from typing import Dict, Any
from crewai import Crew, Process

# Import from the new unified architecture
from ..tools.database_tools import DatabaseManager
from ..agents.assessment_agents import AssessmentAgents
from ..tasks.assessment_tasks import AssessmentTasks

class AssessmentCrew:
    """
    Orchestrates the entire psychological assessment process using a CrewAI crew.
    """
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.tasks = {}
        self.agents = AssessmentAgents()
        self.tasks_definition = AssessmentTasks()

    def kickoff(self, inputs: Dict[str, Any]) -> str:
        """
        Starts a new assessment task by assembling and running a CrewAI crew.
        """
        task_id = str(uuid.uuid4())
        text_to_analyze = inputs.get("text", "")

        # 1. Create the Agent
        assessor_agent = self.agents.psychological_assessor()

        # 2. Create the Task
        analysis_task = self.tasks_definition.personality_analysis_task(assessor_agent, text_to_analyze)

        # 3. Assemble the Crew
        crew = Crew(
            agents=[assessor_agent],
            tasks=[analysis_task],
            process=Process.sequential,
            verbose=2
        )

        # 4. Kick off the crew asynchronously
        # Note: CrewAI's kickoff is synchronous, but the task itself is marked for async execution.
        # In a real production scenario, you would run this in a separate thread or process
        # to avoid blocking the API.
        try:
            result = crew.kickoff(inputs=inputs)
            self.tasks[task_id] = {"status": "completed", "result": result}
        except Exception as e:
            self.tasks[task_id] = {"status": "failed", "result": str(e)}
        
        return task_id

    def get_status(self, task_id: str) -> Dict[str, Any]:
        """
        Retrieves the status and result of a given task.
        """
        return self.tasks.get(task_id)