"""Base Agent Class - Foundation for all modular agents"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from enum import Enum
import asyncio
import logging
from pydantic import BaseModel, Field
import time


class AgentStatus(str, Enum):
    """Agent operational status"""
    IDLE = "idle"
    PROCESSING = "processing"
    ERROR = "error"
    UNAVAILABLE = "unavailable"


class PerformanceMetrics(BaseModel):
    """Performance tracking for agents"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0
    last_response_time: float = 0.0
    uptime_seconds: float = 0.0
    memory_usage_mb: float = 0.0
    

class AgentCapability(BaseModel):
    """Defines what an agent can do"""
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    performance_sla: Dict[str, float] = Field(default_factory=dict)


class AgentMessage(BaseModel):
    """Standard message format for inter-agent communication"""
    id: str
    source_agent: str
    target_agent: Optional[str] = None
    message_type: str = "request"
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    correlation_id: Optional[str] = None


class AgentResponse(BaseModel):
    """Standard response format from agents"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    processing_time: float
    agent_id: str
    confidence: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, agent_id: str, name: str, version: str = "1.0.0"):
        self.agent_id = agent_id
        self.name = name
        self.version = version
        self.status = AgentStatus.IDLE
        self.logger = logging.getLogger(f"agent.{agent_id}")
        self.metrics = PerformanceMetrics()
        self.start_time = time.time()
        self._capabilities: List[AgentCapability] = []
        
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize agent resources (models, connections, etc.)"""
        pass
    
    @abstractmethod
    async def process(self, message: AgentMessage) -> AgentResponse:
        """Process incoming message and return response"""
        pass
    
    @abstractmethod
    async def validate_input(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate input data against agent requirements"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[AgentCapability]:
        """Return list of agent capabilities"""
        pass
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check and return status"""
        self.metrics.uptime_seconds = time.time() - self.start_time
        
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "version": self.version,
            "status": self.status.value,
            "uptime_seconds": self.metrics.uptime_seconds,
            "metrics": self.metrics.dict(),
            "capabilities": len(self._capabilities),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def shutdown(self) -> bool:
        """Gracefully shutdown agent"""
        self.logger.info(f"Shutting down agent {self.agent_id}")
        self.status = AgentStatus.UNAVAILABLE
        return True
    
    def _track_performance(self, start_time: float, success: bool):
        """Track performance metrics"""
        response_time = time.time() - start_time
        self.metrics.total_requests += 1
        if success:
            self.metrics.successful_requests += 1
        else:
            self.metrics.failed_requests += 1
        
        self.metrics.last_response_time = response_time
        
        # Update rolling average
        if self.metrics.average_response_time == 0:
            self.metrics.average_response_time = response_time
        else:
            self.metrics.average_response_time = (
                self.metrics.average_response_time * 0.9 + response_time * 0.1
            )
    
    async def handle_message(self, message: AgentMessage) -> AgentResponse:
        """Wrapper for message processing with metrics tracking"""
        start_time = time.time()
        self.status = AgentStatus.PROCESSING
        
        try:
            # Validate input
            is_valid, error_msg = await self.validate_input(message.payload)
            if not is_valid:
                self._track_performance(start_time, False)
                return AgentResponse(
                    success=False,
                    error=f"Invalid input: {error_msg}",
                    processing_time=time.time() - start_time,
                    agent_id=self.agent_id
                )
            
            # Process message
            response = await self.process(message)
            self._track_performance(start_time, response.success)
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            self._track_performance(start_time, False)
            self.status = AgentStatus.ERROR
            
            return AgentResponse(
                success=False,
                error=str(e),
                processing_time=time.time() - start_time,
                agent_id=self.agent_id
            )
        finally:
            self.status = AgentStatus.IDLE


class ChainableAgent(BaseAgent):
    """Extended base class for agents that can be chained"""
    
    def __init__(self, agent_id: str, name: str, version: str = "1.0.0"):
        super().__init__(agent_id, name, version)
        self.input_agents: List[str] = []
        self.output_agents: List[str] = []
    
    def add_input_agent(self, agent_id: str):
        """Add an agent that provides input to this agent"""
        if agent_id not in self.input_agents:
            self.input_agents.append(agent_id)
    
    def add_output_agent(self, agent_id: str):
        """Add an agent that receives output from this agent"""
        if agent_id not in self.output_agents:
            self.output_agents.append(agent_id)
    
    async def forward_to_next(self, response: AgentResponse, original_message: AgentMessage) -> List[AgentMessage]:
        """Create messages to forward to next agents in chain"""
        messages = []
        for agent_id in self.output_agents:
            messages.append(AgentMessage(
                id=f"{original_message.id}_forward_{agent_id}",
                source_agent=self.agent_id,
                target_agent=agent_id,
                message_type="forward",
                payload=response.data or {},
                metadata={
                    **original_message.metadata,
                    "chain_depth": original_message.metadata.get("chain_depth", 0) + 1,
                    "previous_agent": self.agent_id
                },
                correlation_id=original_message.correlation_id or original_message.id
            ))
        return messages