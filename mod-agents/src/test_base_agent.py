"""Unit tests for BaseAgent and ChainableAgent"""
import pytest
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import time

from agent_library.core.base_agent import (
    BaseAgent, ChainableAgent, AgentMessage, AgentResponse,
    AgentCapability, AgentStatus, PerformanceMetrics
)


class MockAgent(BaseAgent):
    """Mock implementation for testing"""
    
    def __init__(self, agent_id: str = "mock_agent"):
        super().__init__(agent_id, "Mock Agent", "1.0.0")
        self.initialized = False
        self.process_delay = 0.1
        self.should_fail = False
        
    async def initialize(self) -> bool:
        self.initialized = True
        return True
    
    async def process(self, message: AgentMessage) -> AgentResponse:
        if self.should_fail:
            raise Exception("Mock processing error")
            
        await asyncio.sleep(self.process_delay)
        
        return AgentResponse(
            success=True,
            data={"echo": message.payload},
            processing_time=self.process_delay,
            agent_id=self.agent_id,
            confidence=0.95
        )
    
    async def validate_input(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        if "invalid" in data:
            return False, "Invalid input detected"
        return True, None
    
    def get_capabilities(self) -> List[AgentCapability]:
        return [
            AgentCapability(
                name="echo",
                description="Echo back the input",
                input_schema={"message": "string"},
                output_schema={"echo": "object"},
                performance_sla={"max_response_time": 1.0}
            )
        ]


class MockChainableAgent(ChainableAgent):
    """Mock chainable agent for testing"""
    
    async def initialize(self) -> bool:
        return True
    
    async def process(self, message: AgentMessage) -> AgentResponse:
        # Transform the input
        transformed = {"transformed": message.payload.get("data", ""), "agent": self.agent_id}
        
        return AgentResponse(
            success=True,
            data=transformed,
            processing_time=0.05,
            agent_id=self.agent_id
        )
    
    async def validate_input(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        return True, None
    
    def get_capabilities(self) -> List[AgentCapability]:
        return []


class TestBaseAgent:
    """Test BaseAgent functionality"""
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self):
        """Test agent initialization"""
        agent = MockAgent("test_agent")
        
        assert agent.agent_id == "test_agent"
        assert agent.name == "Mock Agent"
        assert agent.version == "1.0.0"
        assert agent.status == AgentStatus.IDLE
        assert not agent.initialized
        
        result = await agent.initialize()
        assert result is True
        assert agent.initialized
    
    @pytest.mark.asyncio
    async def test_message_processing(self):
        """Test successful message processing"""
        agent = MockAgent()
        await agent.initialize()
        
        message = AgentMessage(
            id="test_msg_1",
            source_agent="test_source",
            payload={"data": "test data"},
            message_type="request"
        )
        
        response = await agent.handle_message(message)
        
        assert response.success is True
        assert response.agent_id == "mock_agent"
        assert response.data["echo"]["data"] == "test data"
        assert response.processing_time >= 0.1
        assert response.confidence == 0.95
    
    @pytest.mark.asyncio
    async def test_input_validation(self):
        """Test input validation"""
        agent = MockAgent()
        await agent.initialize()
        
        # Valid input
        valid_message = AgentMessage(
            id="valid_msg",
            source_agent="test",
            payload={"data": "valid"}
        )
        response = await agent.handle_message(valid_message)
        assert response.success is True
        
        # Invalid input
        invalid_message = AgentMessage(
            id="invalid_msg",
            source_agent="test",
            payload={"invalid": True}
        )
        response = await agent.handle_message(invalid_message)
        assert response.success is False
        assert "Invalid input detected" in response.error
    
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling during processing"""
        agent = MockAgent()
        await agent.initialize()
        agent.should_fail = True
        
        message = AgentMessage(
            id="error_msg",
            source_agent="test",
            payload={"data": "test"}
        )
        
        response = await agent.handle_message(message)
        
        assert response.success is False
        assert response.error == "Mock processing error"
        assert agent.status == AgentStatus.ERROR
    
    @pytest.mark.asyncio
    async def test_performance_tracking(self):
        """Test performance metrics tracking"""
        agent = MockAgent()
        await agent.initialize()
        
        # Process multiple messages
        for i in range(5):
            message = AgentMessage(
                id=f"perf_msg_{i}",
                source_agent="test",
                payload={"data": f"test_{i}"}
            )
            await agent.handle_message(message)
        
        metrics = agent.metrics
        assert metrics.total_requests == 5
        assert metrics.successful_requests == 5
        assert metrics.failed_requests == 0
        assert metrics.average_response_time > 0
        assert metrics.last_response_time >= 0.1
    
    @pytest.mark.asyncio
    async def test_health_check(self):
        """Test health check functionality"""
        agent = MockAgent()
        await agent.initialize()
        
        health = await agent.health_check()
        
        assert health["agent_id"] == "mock_agent"
        assert health["status"] == AgentStatus.IDLE.value
        assert health["uptime_seconds"] > 0
        assert "metrics" in health
        assert health["capabilities"] == 1
    
    @pytest.mark.asyncio
    async def test_shutdown(self):
        """Test agent shutdown"""
        agent = MockAgent()
        await agent.initialize()
        
        result = await agent.shutdown()
        assert result is True
        assert agent.status == AgentStatus.UNAVAILABLE


class TestChainableAgent:
    """Test ChainableAgent functionality"""
    
    @pytest.mark.asyncio
    async def test_agent_chaining(self):
        """Test adding input/output agents"""
        agent = MockChainableAgent("chain_agent_1", "Chain Agent 1")
        
        agent.add_input_agent("input_agent_1")
        agent.add_input_agent("input_agent_2")
        agent.add_output_agent("output_agent_1")
        
        assert len(agent.input_agents) == 2
        assert len(agent.output_agents) == 1
        assert "input_agent_1" in agent.input_agents
        assert "output_agent_1" in agent.output_agents
        
        # Test duplicate prevention
        agent.add_input_agent("input_agent_1")
        assert len(agent.input_agents) == 2
    
    @pytest.mark.asyncio
    async def test_forward_messages(self):
        """Test message forwarding to next agents"""
        agent = MockChainableAgent("chain_agent", "Chain Agent")
        agent.add_output_agent("next_agent_1")
        agent.add_output_agent("next_agent_2")
        
        original_message = AgentMessage(
            id="original_msg",
            source_agent="source",
            payload={"data": "test"},
            correlation_id="corr_123"
        )
        
        response = AgentResponse(
            success=True,
            data={"transformed": "data"},
            processing_time=0.1,
            agent_id="chain_agent"
        )
        
        forwarded_messages = await agent.forward_to_next(response, original_message)
        
        assert len(forwarded_messages) == 2
        
        for msg in forwarded_messages:
            assert msg.source_agent == "chain_agent"
            assert msg.message_type == "forward"
            assert msg.payload == {"transformed": "data"}
            assert msg.correlation_id == "corr_123"
            assert msg.metadata["chain_depth"] == 1
            assert msg.metadata["previous_agent"] == "chain_agent"


class TestPerformanceRequirements:
    """Test performance requirements are met"""
    
    @pytest.mark.asyncio
    async def test_response_time_sla(self):
        """Test that response times meet SLA"""
        agent = MockAgent()
        agent.process_delay = 0.05  # 50ms
        await agent.initialize()
        
        response_times = []
        
        for i in range(10):
            message = AgentMessage(
                id=f"perf_test_{i}",
                source_agent="test",
                payload={"data": f"test_{i}"}
            )
            
            start = time.time()
            response = await agent.handle_message(message)
            elapsed = time.time() - start
            
            response_times.append(elapsed)
            assert response.success is True
        
        avg_response_time = sum(response_times) / len(response_times)
        assert avg_response_time < 0.1  # Under 100ms average
        assert max(response_times) < 0.2  # No response over 200ms
    
    @pytest.mark.asyncio
    async def test_concurrent_processing(self):
        """Test concurrent message processing"""
        agent = MockAgent()
        agent.process_delay = 0.05
        await agent.initialize()
        
        # Create multiple messages
        messages = [
            AgentMessage(
                id=f"concurrent_{i}",
                source_agent="test",
                payload={"data": f"concurrent_test_{i}"}
            )
            for i in range(20)
        ]
        
        # Process concurrently
        start = time.time()
        tasks = [agent.handle_message(msg) for msg in messages]
        responses = await asyncio.gather(*tasks)
        elapsed = time.time() - start
        
        # All should succeed
        assert all(r.success for r in responses)
        assert len(responses) == 20
        
        # Should be faster than sequential (20 * 0.05 = 1s)
        # With concurrency, should be much less
        assert elapsed < 0.5
    
    @pytest.mark.asyncio
    async def test_memory_efficiency(self):
        """Test memory efficiency under load"""
        agent = MockAgent()
        agent.process_delay = 0.001  # Very fast processing
        await agent.initialize()
        
        # Process many messages
        for i in range(1000):
            message = AgentMessage(
                id=f"memory_test_{i}",
                source_agent="test",
                payload={"data": f"test_{i}" * 100}  # Larger payload
            )
            await agent.handle_message(message)
        
        # Check metrics are tracked correctly
        assert agent.metrics.total_requests == 1000
        assert agent.metrics.successful_requests == 1000
        
        # Agent should still be responsive
        health = await agent.health_check()
        assert health["status"] == AgentStatus.IDLE.value


if __name__ == "__main__":
    pytest.main([__file__, "-v"])