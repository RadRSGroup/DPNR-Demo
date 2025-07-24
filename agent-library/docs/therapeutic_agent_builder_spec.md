# TherapeuticAgentBuilder Specification

## Overview
The TherapeuticAgentBuilder is a meta-agent that autonomously creates other therapeutic agents for the DPNR platform. It generates production-ready Python code that extends the existing BaseAgent architecture.

## Core Capabilities

### 1. Agent Generation
- Analyzes therapeutic framework requirements from specifications
- Generates complete Python agent implementations
- Creates comprehensive test suites with 85%+ coverage
- Produces API endpoint implementations for FastAPI integration

### 2. Therapeutic Frameworks Supported
- **IFS (Internal Family Systems)**: Parts identification, dialogue facilitation, unburdening assessment
- **Shadow Work**: Jungian pattern detection, projection analysis, integration guidance
- **Narrative Therapy**: Story analysis, reframing, value alignment
- **Somatic Experiencing**: Body awareness, trauma processing, nervous system regulation
- **Attachment Style**: Relationship pattern analysis, attachment classification
- **PaRDeS Reflection**: 4-layer depth analysis (Pshat, Remez, Drash, Sod)

## Input/Output Specifications

### Input Schema
```python
class AgentGenerationRequest(BaseModel):
    agent_type: Literal["ifs", "shadow", "narrative", "somatic", "attachment", "pardes"]
    framework_description: str  # Detailed therapeutic framework requirements
    api_endpoints: List[Dict[str, Any]]  # API endpoint specifications
    quality_requirements: Dict[str, float] = {
        "therapeutic_accuracy": 0.85,
        "test_coverage": 0.85,
        "confidence_threshold": 0.75
    }
    integration_points: List[str]  # Existing agents to integrate with
```

### Output Schema
```python
class GeneratedAgent(BaseModel):
    agent_code: str  # Complete Python implementation
    test_code: str  # Comprehensive test suite
    api_code: str  # FastAPI endpoint implementations
    documentation: str  # Usage examples and docstrings
    validation_report: Dict[str, Any]  # Quality metrics and validation results
```

## Quality Gates

### 1. Code Quality Standards
- **Type Safety**: All functions must have complete type hints
- **Async Support**: I/O operations must use async/await patterns
- **Error Handling**: Comprehensive exception handling with specific error types
- **Logging**: Structured logging with appropriate levels (DEBUG, INFO, WARNING, ERROR)

### 2. Therapeutic Accuracy
- Minimum 85% accuracy on therapeutic framework principles
- Clinical validation checkpoints for high-risk assessments
- Confidence scoring on all therapeutic outputs
- Human-in-the-loop triggers for low-confidence scenarios

### 3. Testing Requirements
- Unit tests for all public methods
- Integration tests for API endpoints
- Mock therapeutic scenarios for validation
- Performance benchmarks for response times

### 4. Documentation Standards
- Comprehensive docstrings following Google style
- Usage examples for each therapeutic method
- API documentation with request/response examples
- Clinical considerations and limitations

## Integration Requirements

### 1. BaseAgent Extension
```python
class TherapeuticAgent(BaseAgent):
    """All generated agents must inherit from BaseAgent"""
    
    async def process_message(self, message: Message) -> Response:
        """Core processing method required by BaseAgent"""
        pass
    
    async def get_health_status(self) -> HealthStatus:
        """Health check implementation"""
        pass
```

### 2. Database Schema Extensions
- PostgreSQL schemas for therapeutic session data
- Vector embeddings for pattern matching
- Session history with privacy considerations
- Audit trails for clinical compliance

### 3. API Integration Pattern
```python
@router.post("/api/v1/assessment/{agent_type}/analyze")
async def analyze(
    request: TherapeuticRequest,
    agent: TherapeuticAgent = Depends(get_agent)
) -> TherapeuticResponse:
    """Standard API endpoint pattern for all therapeutic agents"""
    pass
```

## Therapeutic Agent Templates

### IFS Agent Template
```python
class IFSAgent(BaseAgent):
    """Internal Family Systems therapy agent"""
    
    async def identify_parts(self, text: str) -> List[IFSPart]:
        """Identify manager, firefighter, and exile parts"""
        pass
    
    async def facilitate_dialogue(self, part_id: str, message: str) -> DialogueResponse:
        """Facilitate conversation with identified part"""
        pass
    
    async def assess_unburdening_readiness(self, part: IFSPart) -> float:
        """Determine if part is ready for unburdening process"""
        pass
```

### Shadow Work Agent Template
```python
class ShadowWorkAgent(BaseAgent):
    """Jungian shadow work therapy agent"""
    
    async def detect_shadow_patterns(self, text: str, history: List[str]) -> List[ShadowPattern]:
        """Identify unconscious patterns and projections"""
        pass
    
    async def analyze_projections(self, pattern: ShadowPattern) -> ProjectionAnalysis:
        """Analyze psychological projections"""
        pass
    
    async def generate_integration_guidance(self, pattern: ShadowPattern) -> IntegrationPlan:
        """Create plan for shadow integration"""
        pass
```

## Validation Process

### 1. Automated Validation
- Syntax validation using AST parsing
- Import verification for dependencies
- Type checking with mypy
- Test execution with pytest

### 2. Therapeutic Validation
- Framework adherence scoring
- Clinical accuracy assessment
- Safety checks for harmful content
- Ethical considerations review

### 3. Integration Testing
- API endpoint functionality
- Database schema compatibility
- Performance benchmarks
- Error handling scenarios

## Error Handling

### 1. Generation Errors
```python
class AgentGenerationError(Exception):
    """Base exception for agent generation failures"""
    pass

class TherapeuticValidationError(AgentGenerationError):
    """Therapeutic accuracy below threshold"""
    pass

class CodeQualityError(AgentGenerationError):
    """Generated code fails quality standards"""
    pass
```

### 2. Recovery Mechanisms
- Automatic retry with refined prompts
- Fallback to simpler implementations
- Human escalation for complex failures
- Detailed error reporting for debugging

## Performance Specifications

### Generation Metrics
- Agent generation time: < 5 minutes
- Test suite generation: < 3 minutes
- Validation completion: < 2 minutes
- Total pipeline: < 10 minutes per agent

### Runtime Performance
- API response time: < 200ms (p95)
- Concurrent session support: 1000+
- Memory footprint: < 100MB per agent
- CPU utilization: < 25% under normal load

## Security Considerations

### 1. Code Injection Prevention
- Sanitized code generation
- AST validation before execution
- Sandboxed testing environment
- No dynamic code execution in production

### 2. Data Privacy
- No PII in generated code
- Encrypted session storage
- GDPR-compliant data handling
- Audit trails for all operations

## Usage Example

```python
# Initialize the builder
builder = TherapeuticAgentBuilder()

# Generate IFS Agent
request = AgentGenerationRequest(
    agent_type="ifs",
    framework_description="Internal Family Systems therapy focusing on parts work",
    api_endpoints=[
        {
            "path": "/api/v1/assessment/ifs/analyze",
            "method": "POST",
            "description": "Analyze text for IFS parts"
        }
    ]
)

# Generate the agent
result = await builder.generate_agent(request)

# Validate and deploy
if result.validation_report["therapeutic_accuracy"] >= 0.85:
    await deploy_agent(result.agent_code)
```

## Success Criteria

The TherapeuticAgentBuilder will be considered successful when it can:
1. Generate fully functional therapeutic agents with 85%+ accuracy
2. Create comprehensive test suites with 85%+ coverage
3. Produce API implementations that integrate seamlessly
4. Maintain consistent code quality across all generated agents
5. Complete the generation pipeline in under 10 minutes