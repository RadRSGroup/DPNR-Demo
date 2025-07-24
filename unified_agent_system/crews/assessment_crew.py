import uuid
import asyncio
from typing import Dict, Any, List, Optional
from crewai import Crew, Process
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import from the new unified architecture
from ..tools.database_tools import DatabaseManager
from ..agents.assessment_agents import AssessmentAgents
from ..tasks.assessment_tasks import AssessmentTasks

class AssessmentCrew:
    """
    Advanced orchestration engine for comprehensive psychological assessment.
    Manages parallel processing across 5 frameworks with integration and quality validation.
    """
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.tasks = {}
        self.agents = AssessmentAgents()
        self.tasks_definition = AssessmentTasks()
        self.confidence_threshold = 0.75
        self.max_concurrent_assessments = 5

    def kickoff(self, inputs: Dict[str, Any]) -> str:
        """
        Starts comprehensive psychological assessment with parallel processing.
        """
        task_id = str(uuid.uuid4())
        text_to_analyze = inputs.get("text", "")
        assessment_type = inputs.get("assessment_type", "comprehensive")
        
        self.tasks[task_id] = {"status": "processing", "result": None}
        
        try:
            if assessment_type == "comprehensive":
                result = self._run_comprehensive_assessment(text_to_analyze, inputs)
            elif assessment_type == "parallel":
                result = self._run_parallel_assessment(text_to_analyze, inputs)
            elif assessment_type == "single_framework":
                framework = inputs.get("framework", "big_five")
                result = self._run_single_framework_assessment(text_to_analyze, framework, inputs)
            else:
                result = self._run_legacy_assessment(text_to_analyze, inputs)
            
            self.tasks[task_id] = {"status": "completed", "result": result}
        except Exception as e:
            self.tasks[task_id] = {"status": "failed", "result": str(e), "error": str(e)}
        
        return task_id
    
    def _run_comprehensive_assessment(self, text: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run comprehensive assessment using the master psychological assessor.
        """
        # Create comprehensive assessment crew
        assessor_agent = self.agents.psychological_assessor()
        coordinator_agent = self.agents.assessment_coordinator()
        validator_agent = self.agents.quality_validator()
        
        # Create tasks
        analysis_task = self.tasks_definition.comprehensive_personality_analysis_task(assessor_agent, text)
        
        # Assemble crew with hierarchical process
        crew = Crew(
            agents=[assessor_agent, coordinator_agent, validator_agent],
            tasks=[analysis_task],
            process=Process.hierarchical,
            manager_agent=coordinator_agent,
            verbose=2,
            memory=True
        )
        
        result = crew.kickoff(inputs=inputs)
        return self._process_comprehensive_result(result)
    
    def _run_parallel_assessment(self, text: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run parallel assessment across all 5 frameworks with integration.
        """
        # Create specialized agents for each framework
        big_five_agent = self.agents.big_five_specialist()
        enneagram_agent = self.agents.enneagram_specialist()
        values_agent = self.agents.values_specialist()
        ei_agent = self.agents.emotional_intelligence_specialist()
        cognitive_agent = self.agents.cognitive_style_specialist()
        integration_agent = self.agents.integration_specialist()
        validator_agent = self.agents.quality_validator()
        
        # Create specialized tasks
        big_five_task = self.tasks_definition.big_five_analysis_task(big_five_agent, text)
        enneagram_task = self.tasks_definition.enneagram_analysis_task(enneagram_agent, text)
        values_task = self.tasks_definition.values_analysis_task(values_agent, text)
        ei_task = self.tasks_definition.emotional_intelligence_analysis_task(ei_agent, text)
        cognitive_task = self.tasks_definition.cognitive_style_analysis_task(cognitive_agent, text)
        
        # Run parallel assessment crews
        parallel_results = self._execute_parallel_crews([
            (big_five_agent, big_five_task, "big_five"),
            (enneagram_agent, enneagram_task, "enneagram"),
            (values_agent, values_task, "values"),
            (ei_agent, ei_task, "emotional_intelligence"),
            (cognitive_agent, cognitive_task, "cognitive_style")
        ], inputs)
        
        # Integration phase
        integration_task = self.tasks_definition.integration_synthesis_task(integration_agent, parallel_results)
        integration_crew = Crew(
            agents=[integration_agent],
            tasks=[integration_task],
            process=Process.sequential,
            verbose=1
        )
        
        integrated_result = integration_crew.kickoff(inputs={"assessment_results": parallel_results})
        
        # Quality validation phase
        validation_task = self.tasks_definition.quality_validation_task(
            validator_agent, parallel_results, text, self.confidence_threshold
        )
        validation_crew = Crew(
            agents=[validator_agent],
            tasks=[validation_task],
            process=Process.sequential,
            verbose=1
        )
        
        validation_result = validation_crew.kickoff(inputs={
            "assessment_results": parallel_results,
            "original_text": text
        })
        
        return {
            "assessment_type": "parallel",
            "framework_results": parallel_results,
            "integrated_analysis": integrated_result,
            "quality_validation": validation_result,
            "overall_confidence": self._calculate_overall_confidence(parallel_results),
            "processing_metadata": {
                "frameworks_processed": 5,
                "parallel_execution": True,
                "integration_performed": True,
                "quality_validated": True
            }
        }
    
    def _execute_parallel_crews(self, crew_configs: List[tuple], inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute multiple assessment crews in parallel using ThreadPoolExecutor.
        """
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_concurrent_assessments) as executor:
            # Submit all crew executions
            future_to_framework = {}
            
            for agent, task, framework_name in crew_configs:
                crew = Crew(
                    agents=[agent],
                    tasks=[task],
                    process=Process.sequential,
                    verbose=1
                )
                future = executor.submit(crew.kickoff, inputs)
                future_to_framework[future] = framework_name
            
            # Collect results as they complete
            for future in as_completed(future_to_framework):
                framework_name = future_to_framework[future]
                try:
                    result = future.result()
                    results[framework_name] = result
                except Exception as e:
                    results[framework_name] = {
                        "error": str(e),
                        "status": "failed",
                        "framework": framework_name
                    }
        
        return results
    
    def _run_single_framework_assessment(self, text: str, framework: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run assessment for a single specified framework.
        """
        framework_agents = {
            "big_five": self.agents.big_five_specialist,
            "enneagram": self.agents.enneagram_specialist,
            "values": self.agents.values_specialist,
            "emotional_intelligence": self.agents.emotional_intelligence_specialist,
            "cognitive_style": self.agents.cognitive_style_specialist
        }
        
        framework_tasks = {
            "big_five": self.tasks_definition.big_five_analysis_task,
            "enneagram": self.tasks_definition.enneagram_analysis_task,
            "values": self.tasks_definition.values_analysis_task,
            "emotional_intelligence": self.tasks_definition.emotional_intelligence_analysis_task,
            "cognitive_style": self.tasks_definition.cognitive_style_analysis_task
        }
        
        if framework not in framework_agents:
            raise ValueError(f"Unknown framework: {framework}")
        
        agent = framework_agents[framework]()
        task = framework_tasks[framework](agent, text)
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=2
        )
        
        result = crew.kickoff(inputs=inputs)
        return {
            "assessment_type": "single_framework",
            "framework": framework,
            "result": result
        }
    
    def _run_legacy_assessment(self, text: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Legacy assessment method for backward compatibility.
        """
        assessor_agent = self.agents.psychological_assessor()
        analysis_task = self.tasks_definition.personality_analysis_task(assessor_agent, text)
        
        crew = Crew(
            agents=[assessor_agent],
            tasks=[analysis_task],
            process=Process.sequential,
            verbose=2
        )
        
        result = crew.kickoff(inputs=inputs)
        return {
            "assessment_type": "legacy",
            "result": result
        }
    
    def _process_comprehensive_result(self, result: Any) -> Dict[str, Any]:
        """
        Process and structure comprehensive assessment results.
        """
        return {
            "assessment_type": "comprehensive",
            "result": result,
            "processing_metadata": {
                "method": "comprehensive_single_agent",
                "frameworks_included": 5
            }
        }
    
    def _calculate_overall_confidence(self, results: Dict[str, Any]) -> float:
        """
        Calculate overall confidence score across all framework results.
        """
        confidence_scores = []
        
        for framework_result in results.values():
            if isinstance(framework_result, dict) and "overall_confidence" in framework_result:
                confidence_scores.append(framework_result["overall_confidence"])
            elif isinstance(framework_result, dict) and "confidence" in framework_result:
                confidence_scores.append(framework_result["confidence"])
        
        return sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
    
    def run_recursive_analysis(self, task_id: str, low_confidence_frameworks: List[str]) -> str:
        """
        Run recursive analysis for frameworks with low confidence scores.
        """
        original_task = self.tasks.get(task_id)
        if not original_task:
            raise ValueError(f"Task {task_id} not found")
        
        recursive_task_id = f"{task_id}_recursive"
        
        # Implementation for recursive analysis would go here
        # This would re-run specific frameworks with enhanced prompts
        
        return recursive_task_id
    
    def generate_therapeutic_insights(self, task_id: str) -> Dict[str, Any]:
        """
        Generate therapeutic insights from completed assessment results.
        """
        task_result = self.tasks.get(task_id)
        if not task_result or task_result["status"] != "completed":
            raise ValueError(f"Task {task_id} not completed or not found")
        
        therapeutic_agent = self.agents.therapeutic_insights_specialist()
        insights_task = self.tasks_definition.therapeutic_insights_task(therapeutic_agent, task_result["result"])
        
        crew = Crew(
            agents=[therapeutic_agent],
            tasks=[insights_task],
            process=Process.sequential,
            verbose=1
        )
        
        insights_result = crew.kickoff(inputs={"assessment_results": task_result["result"]})
        return insights_result

    def get_status(self, task_id: str) -> Dict[str, Any]:
        """
        Retrieves the status and result of a given task with enhanced metadata.
        """
        task = self.tasks.get(task_id)
        if not task:
            return {"status": "not_found", "error": "Task not found"}
        
        return {
            "task_id": task_id,
            "status": task["status"],
            "result": task.get("result"),
            "error": task.get("error"),
            "metadata": {
                "has_result": "result" in task and task["result"] is not None,
                "has_error": "error" in task,
                "processing_complete": task["status"] in ["completed", "failed"]
            }
        }
    
    def list_all_tasks(self) -> List[Dict[str, Any]]:
        """
        List all tasks with their current status.
        """
        return [
            {
                "task_id": task_id,
                "status": task_data["status"],
                "has_result": "result" in task_data and task_data["result"] is not None
            }
            for task_id, task_data in self.tasks.items()
        ]
    
    def cleanup_completed_tasks(self, keep_recent: int = 10) -> int:
        """
        Clean up old completed tasks, keeping only the most recent ones.
        """
        completed_tasks = [
            (task_id, task_data) for task_id, task_data in self.tasks.items() 
            if task_data["status"] in ["completed", "failed"]
        ]
        
        if len(completed_tasks) <= keep_recent:
            return 0
        
        # Sort by task_id (which includes timestamp) and remove oldest
        completed_tasks.sort(key=lambda x: x[0])
        tasks_to_remove = completed_tasks[:-keep_recent]
        
        for task_id, _ in tasks_to_remove:
            del self.tasks[task_id]
        
        return len(tasks_to_remove)