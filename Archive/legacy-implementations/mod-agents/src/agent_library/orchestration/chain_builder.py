"""Chain Builder - Create and configure agent chains"""
from typing import List, Dict, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import yaml
from pathlib import Path

from ..core.base_agent import AgentMessage, ChainableAgent


class ChainExecutionMode(str, Enum):
    """How agents in a chain should be executed"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    LOOP = "loop"


@dataclass
class AgentNode:
    """Represents an agent in the chain"""
    agent_id: str
    agent_class: str
    config: Dict[str, Any] = field(default_factory=dict)
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    execution_mode: ChainExecutionMode = ChainExecutionMode.SEQUENTIAL
    condition: Optional[str] = None  # For conditional execution
    max_iterations: int = 1  # For loop execution


@dataclass
class ChainConnection:
    """Represents a connection between agents"""
    source_agent: str
    target_agent: str
    data_mapping: Dict[str, str] = field(default_factory=dict)  # source_field: target_field
    transform: Optional[str] = None  # Optional transformation function


@dataclass
class AgentChain:
    """Represents a complete agent chain"""
    chain_id: str
    name: str
    description: str
    nodes: List[AgentNode] = field(default_factory=list)
    connections: List[ChainConnection] = field(default_factory=list)
    entry_point: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ChainBuilder:
    """Builder for creating agent chains"""
    
    def __init__(self):
        self.chains: Dict[str, AgentChain] = {}
        self.agent_registry: Dict[str, type] = {}
    
    def register_agent(self, agent_class: type, agent_type: str = None):
        """Register an agent class for use in chains"""
        agent_type = agent_type or agent_class.__name__
        self.agent_registry[agent_type] = agent_class
    
    def create_chain(self, chain_id: str, name: str, description: str = "") -> AgentChain:
        """Create a new agent chain"""
        chain = AgentChain(
            chain_id=chain_id,
            name=name,
            description=description
        )
        self.chains[chain_id] = chain
        return chain
    
    def add_agent(self, chain_id: str, agent_id: str, agent_class: str, 
                  config: Dict[str, Any] = None, execution_mode: ChainExecutionMode = ChainExecutionMode.SEQUENTIAL) -> AgentNode:
        """Add an agent to a chain"""
        if chain_id not in self.chains:
            raise ValueError(f"Chain {chain_id} not found")
        
        node = AgentNode(
            agent_id=agent_id,
            agent_class=agent_class,
            config=config or {},
            execution_mode=execution_mode
        )
        
        chain = self.chains[chain_id]
        chain.nodes.append(node)
        
        # Set entry point if this is the first node
        if not chain.entry_point:
            chain.entry_point = agent_id
        
        return node
    
    def connect_agents(self, chain_id: str, source_agent: str, target_agent: str,
                      data_mapping: Dict[str, str] = None, transform: str = None):
        """Connect two agents in a chain"""
        if chain_id not in self.chains:
            raise ValueError(f"Chain {chain_id} not found")
        
        chain = self.chains[chain_id]
        
        # Verify agents exist
        agent_ids = {node.agent_id for node in chain.nodes}
        if source_agent not in agent_ids:
            raise ValueError(f"Source agent {source_agent} not found in chain")
        if target_agent not in agent_ids:
            raise ValueError(f"Target agent {target_agent} not found in chain")
        
        connection = ChainConnection(
            source_agent=source_agent,
            target_agent=target_agent,
            data_mapping=data_mapping or {},
            transform=transform
        )
        
        chain.connections.append(connection)
        
        # Update agent inputs/outputs
        for node in chain.nodes:
            if node.agent_id == source_agent:
                if target_agent not in node.outputs:
                    node.outputs.append(target_agent)
            elif node.agent_id == target_agent:
                if source_agent not in node.inputs:
                    node.inputs.append(source_agent)
    
    def create_sequential_chain(self, chain_id: str, name: str, agent_sequence: List[Tuple[str, str, Dict]]) -> AgentChain:
        """Create a simple sequential chain"""
        chain = self.create_chain(chain_id, name, f"Sequential chain: {name}")
        
        prev_agent = None
        for agent_id, agent_class, config in agent_sequence:
            self.add_agent(chain_id, agent_id, agent_class, config)
            
            if prev_agent:
                self.connect_agents(chain_id, prev_agent, agent_id)
            
            prev_agent = agent_id
        
        return chain
    
    def create_parallel_chain(self, chain_id: str, name: str, 
                            input_agent: Tuple[str, str, Dict],
                            parallel_agents: List[Tuple[str, str, Dict]],
                            output_agent: Tuple[str, str, Dict]) -> AgentChain:
        """Create a chain with parallel execution"""
        chain = self.create_chain(chain_id, name, f"Parallel chain: {name}")
        
        # Add input agent
        input_id, input_class, input_config = input_agent
        self.add_agent(chain_id, input_id, input_class, input_config)
        
        # Add parallel agents
        for agent_id, agent_class, config in parallel_agents:
            self.add_agent(chain_id, agent_id, agent_class, config, ChainExecutionMode.PARALLEL)
            self.connect_agents(chain_id, input_id, agent_id)
        
        # Add output agent
        output_id, output_class, output_config = output_agent
        self.add_agent(chain_id, output_id, output_class, output_config)
        
        # Connect all parallel agents to output
        for agent_id, _, _ in parallel_agents:
            self.connect_agents(chain_id, agent_id, output_id)
        
        return chain
    
    def validate_chain(self, chain_id: str) -> Tuple[bool, List[str]]:
        """Validate a chain configuration"""
        if chain_id not in self.chains:
            return False, ["Chain not found"]
        
        chain = self.chains[chain_id]
        errors = []
        
        # Check entry point
        if not chain.entry_point:
            errors.append("No entry point defined")
        elif chain.entry_point not in {node.agent_id for node in chain.nodes}:
            errors.append(f"Entry point {chain.entry_point} not found in nodes")
        
        # Check all agents in connections exist
        agent_ids = {node.agent_id for node in chain.nodes}
        for conn in chain.connections:
            if conn.source_agent not in agent_ids:
                errors.append(f"Source agent {conn.source_agent} in connection not found")
            if conn.target_agent not in agent_ids:
                errors.append(f"Target agent {conn.target_agent} in connection not found")
        
        # Check for orphaned agents (no inputs or outputs except entry/exit)
        for node in chain.nodes:
            if node.agent_id != chain.entry_point and not node.inputs:
                errors.append(f"Agent {node.agent_id} has no inputs")
        
        # Check agent classes are registered
        for node in chain.nodes:
            if node.agent_class not in self.agent_registry:
                errors.append(f"Agent class {node.agent_class} not registered")
        
        return len(errors) == 0, errors
    
    def export_chain(self, chain_id: str, format: str = "json") -> str:
        """Export chain configuration"""
        if chain_id not in self.chains:
            raise ValueError(f"Chain {chain_id} not found")
        
        chain = self.chains[chain_id]
        
        data = {
            "chain_id": chain.chain_id,
            "name": chain.name,
            "description": chain.description,
            "entry_point": chain.entry_point,
            "nodes": [
                {
                    "agent_id": node.agent_id,
                    "agent_class": node.agent_class,
                    "config": node.config,
                    "execution_mode": node.execution_mode.value,
                    "inputs": node.inputs,
                    "outputs": node.outputs
                }
                for node in chain.nodes
            ],
            "connections": [
                {
                    "source": conn.source_agent,
                    "target": conn.target_agent,
                    "mapping": conn.data_mapping,
                    "transform": conn.transform
                }
                for conn in chain.connections
            ],
            "metadata": chain.metadata
        }
        
        if format == "json":
            return json.dumps(data, indent=2)
        elif format == "yaml":
            return yaml.dump(data, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def import_chain(self, data: Union[str, Dict], format: str = "json") -> AgentChain:
        """Import chain configuration"""
        if isinstance(data, str):
            if format == "json":
                data = json.loads(data)
            elif format == "yaml":
                data = yaml.safe_load(data)
            else:
                raise ValueError(f"Unsupported format: {format}")
        
        chain = AgentChain(
            chain_id=data["chain_id"],
            name=data["name"],
            description=data.get("description", ""),
            entry_point=data.get("entry_point"),
            metadata=data.get("metadata", {})
        )
        
        # Import nodes
        for node_data in data["nodes"]:
            node = AgentNode(
                agent_id=node_data["agent_id"],
                agent_class=node_data["agent_class"],
                config=node_data.get("config", {}),
                execution_mode=ChainExecutionMode(node_data.get("execution_mode", "sequential")),
                inputs=node_data.get("inputs", []),
                outputs=node_data.get("outputs", [])
            )
            chain.nodes.append(node)
        
        # Import connections
        for conn_data in data["connections"]:
            conn = ChainConnection(
                source_agent=conn_data["source"],
                target_agent=conn_data["target"],
                data_mapping=conn_data.get("mapping", {}),
                transform=conn_data.get("transform")
            )
            chain.connections.append(conn)
        
        self.chains[chain.chain_id] = chain
        return chain
    
    def visualize_chain(self, chain_id: str) -> str:
        """Generate a simple text visualization of the chain"""
        if chain_id not in self.chains:
            raise ValueError(f"Chain {chain_id} not found")
        
        chain = self.chains[chain_id]
        lines = []
        
        lines.append(f"Chain: {chain.name}")
        lines.append(f"ID: {chain.chain_id}")
        lines.append(f"Entry: {chain.entry_point}")
        lines.append("")
        lines.append("Nodes:")
        
        for node in chain.nodes:
            mode = f" [{node.execution_mode.value}]" if node.execution_mode != ChainExecutionMode.SEQUENTIAL else ""
            lines.append(f"  - {node.agent_id} ({node.agent_class}){mode}")
        
        lines.append("")
        lines.append("Connections:")
        
        for conn in chain.connections:
            mapping = f" {conn.data_mapping}" if conn.data_mapping else ""
            lines.append(f"  - {conn.source_agent} -> {conn.target_agent}{mapping}")
        
        return "\n".join(lines)