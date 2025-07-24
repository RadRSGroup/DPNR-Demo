"""Workflow Engine - Executes agent chains with monitoring and error handling"""
import asyncio
import uuid
import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
import json
import traceback
from contextlib import asynccontextmanager

from ..core.base_agent import (
    BaseAgent, AgentMessage, AgentResponse, AgentStatus
)
from .chain_builder import (
    ChainBuilder, AgentChain, AgentNode, ChainConnection, ChainExecutionMode
)


class ExecutionStatus(str, Enum):
    """Execution status of workflows"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class NodeStatus(str, Enum):
    """Status of individual nodes in execution"""
    WAITING = "waiting"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ExecutionContext:
    """Context for workflow execution"""
    execution_id: str
    chain_id: str
    user_id: Optional[str] = None
    input_data: Dict[str, Any] = field(default_factory=dict)
    variables: Dict[str, Any] = field(default_factory=dict)
    start_time: datetime = field(default_factory=datetime.utcnow)
    timeout_seconds: int = 300  # 5 minutes default


@dataclass
class NodeExecution:
    """Execution state of a single node"""
    node_id: str
    status: NodeStatus = NodeStatus.WAITING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    agent_response: Optional[AgentResponse] = None
    retries: int = 0
    max_retries: int = 3


@dataclass
class WorkflowExecution:
    """Complete workflow execution state"""
    execution_id: str
    chain_id: str
    status: ExecutionStatus = ExecutionStatus.PENDING
    context: ExecutionContext = None
    node_executions: Dict[str, NodeExecution] = field(default_factory=dict)
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    final_result: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    execution_log: List[str] = field(default_factory=list)


class WorkflowEngine:
    """Engine for executing agent workflows"""
    
    def __init__(self, chain_builder: ChainBuilder, max_concurrent_executions: int = 50):
        self.chain_builder = chain_builder
        self.agents: Dict[str, BaseAgent] = {}
        self.executions: Dict[str, WorkflowExecution] = {}
        self.max_concurrent = max_concurrent_executions
        self.execution_semaphore = asyncio.Semaphore(max_concurrent_executions)
        self.logger = logging.getLogger(__name__)
        
        # Event hooks
        self.hooks: Dict[str, List[Callable]] = {
            "before_execution": [],
            "after_execution": [],
            "node_start": [],
            "node_complete": [],
            "node_error": []
        }
    
    def register_agent(self, agent: BaseAgent):
        """Register an agent instance for use in workflows"""
        self.agents[agent.agent_id] = agent
        self.logger.info(f"Registered agent: {agent.agent_id}")
    
    def add_hook(self, event: str, callback: Callable):
        """Add event hook"""
        if event in self.hooks:
            self.hooks[event].append(callback)
    
    async def execute_chain(self, chain_id: str, input_data: Dict[str, Any], 
                          user_id: Optional[str] = None, timeout: int = 300) -> WorkflowExecution:
        """Execute a chain workflow"""
        execution_id = str(uuid.uuid4())
        
        # Get chain definition
        if chain_id not in self.chain_builder.chains:
            raise ValueError(f"Chain {chain_id} not found")
        
        chain = self.chain_builder.chains[chain_id]
        
        # Create execution context
        context = ExecutionContext(
            execution_id=execution_id,
            chain_id=chain_id,
            user_id=user_id,
            input_data=input_data,
            timeout_seconds=timeout
        )
        
        # Initialize workflow execution
        execution = WorkflowExecution(
            execution_id=execution_id,
            chain_id=chain_id,
            context=context
        )
        
        # Initialize node executions
        for node in chain.nodes:
            execution.node_executions[node.agent_id] = NodeExecution(node_id=node.agent_id)
        
        self.executions[execution_id] = execution
        
        try:
            async with self.execution_semaphore:
                await self._execute_workflow(execution, chain)
        except Exception as e:
            execution.status = ExecutionStatus.FAILED
            execution.error = str(e)
            execution.end_time = datetime.utcnow()
            self.logger.error(f"Workflow execution failed: {str(e)}")
        
        return execution
    
    async def _execute_workflow(self, execution: WorkflowExecution, chain: AgentChain):
        """Execute the workflow"""
        execution.status = ExecutionStatus.RUNNING
        execution.execution_log.append(f"Started execution at {datetime.utcnow()}")
        
        try:
            # Execute before hooks
            await self._execute_hooks("before_execution", execution)
            
            # Build execution graph
            dependency_graph = self._build_dependency_graph(chain)
            
            # Execute with timeout
            timeout_task = asyncio.create_task(
                asyncio.sleep(execution.context.timeout_seconds)
            )
            execution_task = asyncio.create_task(
                self._execute_dependency_graph(execution, chain, dependency_graph)
            )
            
            done, pending = await asyncio.wait(
                [timeout_task, execution_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel pending tasks
            for task in pending:
                task.cancel()
            
            if timeout_task in done:
                execution.status = ExecutionStatus.TIMEOUT
                execution.error = f"Execution timed out after {execution.context.timeout_seconds} seconds"
            else:
                # Get execution result
                result = await execution_task
                execution.final_result = result
                execution.status = ExecutionStatus.COMPLETED
            
        except Exception as e:
            execution.status = ExecutionStatus.FAILED
            execution.error = str(e)
            execution.execution_log.append(f"Error: {str(e)}")
            self.logger.error(f"Workflow execution error: {traceback.format_exc()}")
        
        finally:
            execution.end_time = datetime.utcnow()
            execution.execution_log.append(f"Completed execution at {execution.end_time}")
            
            # Execute after hooks
            await self._execute_hooks("after_execution", execution)
    
    def _build_dependency_graph(self, chain: AgentChain) -> Dict[str, List[str]]:
        """Build dependency graph from chain connections"""
        dependencies = {node.agent_id: [] for node in chain.nodes}
        
        for connection in chain.connections:
            dependencies[connection.target_agent].append(connection.source_agent)
        
        return dependencies
    
    async def _execute_dependency_graph(self, execution: WorkflowExecution, 
                                      chain: AgentChain, dependencies: Dict[str, List[str]]) -> Dict[str, Any]:
        """Execute nodes respecting dependencies"""
        completed_nodes = set()
        final_results = {}
        
        # Find entry points (nodes with no dependencies)
        entry_points = [node_id for node_id, deps in dependencies.items() if not deps]
        if not entry_points and chain.entry_point:
            entry_points = [chain.entry_point]
        
        if not entry_points:
            raise ValueError("No entry points found in chain")
        
        # Execute nodes level by level
        ready_nodes = set(entry_points)
        
        while ready_nodes:
            # Get nodes by execution mode
            sequential_nodes = []
            parallel_nodes = []
            
            for node_id in ready_nodes:
                node = next(n for n in chain.nodes if n.agent_id == node_id)
                if node.execution_mode == ChainExecutionMode.PARALLEL:
                    parallel_nodes.append(node_id)
                else:
                    sequential_nodes.append(node_id)
            
            # Execute parallel nodes
            if parallel_nodes:
                parallel_tasks = [
                    self._execute_node(execution, chain, node_id)
                    for node_id in parallel_nodes
                ]
                parallel_results = await asyncio.gather(*parallel_tasks, return_exceptions=True)
                
                for i, result in enumerate(parallel_results):
                    node_id = parallel_nodes[i]
                    if isinstance(result, Exception):
                        execution.node_executions[node_id].status = NodeStatus.FAILED
                        execution.node_executions[node_id].error = str(result)
                        raise result
                    else:
                        final_results[node_id] = result
                        completed_nodes.add(node_id)
            
            # Execute sequential nodes
            for node_id in sequential_nodes:
                try:
                    result = await self._execute_node(execution, chain, node_id)
                    final_results[node_id] = result
                    completed_nodes.add(node_id)
                except Exception as e:
                    execution.node_executions[node_id].status = NodeStatus.FAILED
                    execution.node_executions[node_id].error = str(e)
                    raise e
            
            # Find next ready nodes
            ready_nodes = set()
            for node_id, deps in dependencies.items():
                if node_id not in completed_nodes and all(dep in completed_nodes for dep in deps):
                    ready_nodes.add(node_id)
        
        return final_results
    
    async def _execute_node(self, execution: WorkflowExecution, chain: AgentChain, node_id: str) -> Dict[str, Any]:
        """Execute a single node"""
        node_exec = execution.node_executions[node_id]
        node = next(n for n in chain.nodes if n.agent_id == node_id)
        
        node_exec.status = NodeStatus.RUNNING
        node_exec.start_time = datetime.utcnow()
        
        execution.execution_log.append(f"Starting node {node_id}")
        
        try:
            # Execute node start hooks
            await self._execute_hooks("node_start", execution, node_id)
            
            # Get input data for this node
            input_data = await self._prepare_node_input(execution, chain, node_id)
            node_exec.input_data = input_data
            
            # Get agent instance
            if node.agent_id not in self.agents:
                raise ValueError(f"Agent {node.agent_id} not registered")
            
            agent = self.agents[node.agent_id]
            
            # Create agent message
            message = AgentMessage(
                id=f"{execution.execution_id}_{node_id}",
                source_agent="workflow_engine",
                target_agent=node.agent_id,
                payload=input_data,
                metadata={
                    "execution_id": execution.execution_id,
                    "chain_id": execution.chain_id,
                    "node_config": node.config
                }
            )
            
            # Execute agent with retries
            response = await self._execute_with_retries(agent, message, node_exec)
            
            if not response.success:
                raise Exception(f"Agent execution failed: {response.error}")
            
            node_exec.agent_response = response
            node_exec.output_data = response.data or {}
            node_exec.status = NodeStatus.COMPLETED
            node_exec.end_time = datetime.utcnow()
            
            execution.execution_log.append(f"Completed node {node_id}")
            
            # Execute node complete hooks
            await self._execute_hooks("node_complete", execution, node_id)
            
            return node_exec.output_data
            
        except Exception as e:
            node_exec.status = NodeStatus.FAILED
            node_exec.error = str(e)
            node_exec.end_time = datetime.utcnow()
            
            execution.execution_log.append(f"Failed node {node_id}: {str(e)}")
            
            # Execute node error hooks
            await self._execute_hooks("node_error", execution, node_id, e)
            
            raise e
    
    async def _prepare_node_input(self, execution: WorkflowExecution, chain: AgentChain, node_id: str) -> Dict[str, Any]:
        """Prepare input data for a node based on connections"""
        input_data = {}
        
        # Get connections that target this node
        incoming_connections = [conn for conn in chain.connections if conn.target_agent == node_id]
        
        if not incoming_connections:
            # Entry node - use execution input
            input_data = execution.context.input_data.copy()
        else:
            # Merge data from source agents
            for connection in incoming_connections:
                source_node_exec = execution.node_executions[connection.source_agent]
                
                if source_node_exec.status != NodeStatus.COMPLETED:
                    raise ValueError(f"Source node {connection.source_agent} not completed")
                
                source_data = source_node_exec.output_data
                
                # Apply data mapping if specified
                if connection.data_mapping:
                    for source_field, target_field in connection.data_mapping.items():
                        if source_field in source_data:
                            input_data[target_field] = source_data[source_field]
                else:
                    # Direct merge
                    input_data.update(source_data)
        
        # Add execution context variables
        input_data["_context"] = {
            "execution_id": execution.execution_id,
            "chain_id": execution.chain_id,
            "user_id": execution.context.user_id,
            "variables": execution.context.variables
        }
        
        return input_data
    
    async def _execute_with_retries(self, agent: BaseAgent, message: AgentMessage, node_exec: NodeExecution) -> AgentResponse:
        """Execute agent with retry logic"""
        last_error = None
        
        for attempt in range(node_exec.max_retries + 1):
            try:
                if attempt > 0:
                    self.logger.info(f"Retrying agent {agent.agent_id}, attempt {attempt + 1}")
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                
                response = await agent.handle_message(message)
                
                if response.success:
                    return response
                else:
                    last_error = response.error
                    
            except Exception as e:
                last_error = str(e)
                self.logger.warning(f"Agent execution attempt {attempt + 1} failed: {str(e)}")
        
        node_exec.retries = node_exec.max_retries
        raise Exception(f"Agent execution failed after {node_exec.max_retries + 1} attempts. Last error: {last_error}")
    
    async def _execute_hooks(self, event: str, execution: WorkflowExecution, 
                           node_id: Optional[str] = None, error: Optional[Exception] = None):
        """Execute event hooks"""
        for hook in self.hooks.get(event, []):
            try:
                if asyncio.iscoroutinefunction(hook):
                    await hook(execution, node_id, error)
                else:
                    hook(execution, node_id, error)
            except Exception as e:
                self.logger.error(f"Hook execution failed: {str(e)}")
    
    async def get_execution_status(self, execution_id: str) -> Optional[WorkflowExecution]:
        """Get execution status"""
        return self.executions.get(execution_id)
    
    async def cancel_execution(self, execution_id: str) -> bool:
        """Cancel a running execution"""
        if execution_id in self.executions:
            execution = self.executions[execution_id]
            if execution.status == ExecutionStatus.RUNNING:
                execution.status = ExecutionStatus.CANCELLED
                execution.end_time = datetime.utcnow()
                execution.execution_log.append(f"Cancelled at {datetime.utcnow()}")
                return True
        return False
    
    async def cleanup_old_executions(self, max_age_hours: int = 24):
        """Clean up old execution records"""
        cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)
        
        to_remove = []
        for execution_id, execution in self.executions.items():
            if execution.end_time and execution.end_time < cutoff_time:
                to_remove.append(execution_id)
        
        for execution_id in to_remove:
            del self.executions[execution_id]
        
        self.logger.info(f"Cleaned up {len(to_remove)} old executions")
    
    def get_execution_metrics(self) -> Dict[str, Any]:
        """Get execution metrics"""
        total_executions = len(self.executions)
        status_counts = {}
        
        for execution in self.executions.values():
            status = execution.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "total_executions": total_executions,
            "status_distribution": status_counts,
            "registered_agents": len(self.agents),
            "active_executions": len([e for e in self.executions.values() if e.status == ExecutionStatus.RUNNING])
        }