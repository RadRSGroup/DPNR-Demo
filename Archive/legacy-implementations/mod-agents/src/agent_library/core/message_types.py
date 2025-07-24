"""
Message Types for Agent Communication

Simplified message format for psychological assessment agents.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class AgentMessage:
    """Simple message format for agent communication"""
    message_id: str
    agent_id: str
    content: Dict[str, Any]
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass 
class AgentResponse:
    """Simple response format from agents"""
    agent_id: str
    content: Dict[str, Any]
    confidence: float
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()