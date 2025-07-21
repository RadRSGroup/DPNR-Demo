# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a **production-ready Python AI agent system** for multi-model psychological assessment. The system uses **CrewAI** for agent orchestration, combining multiple psychological frameworks (Enneagram, Big Five, Emotional Intelligence, Values, Cognitive Style) with advanced NLP processing.

### Core Components

- **CrewAI Agents**: Role-based AI agents for specialized assessment tasks
- **FastAPI Server**: REST API with comprehensive error handling (`fastapi_server.py`)
- **Psychological Assessment System**: Main orchestration engine (`psychological_assessment_system.py`)
- **Clinical Framework Processors**: Advanced linguistic analysis and clinical-grade models (`clin_framework_processors.py`)
- **WebSocket Support**: Real-time assessment processing
- **Vector Storage**: PostgreSQL + pgvector for semantic similarity matching

### Key Technologies

- **Agent Framework**: CrewAI for role-based agent orchestration
- **Database**: PostgreSQL with pgvector extension for vector embeddings
- **Caching**: Redis for session management and result caching
- **ML Models**: Transformers, sentence-transformers, clinical-grade RoBERTa models
- **APIs**: OpenAI GPT models, Cohere for embeddings

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start database and Redis (development)
docker-compose up postgres redis -d

# Run main application
python psychological_assessment_system.py

# Run FastAPI server
uvicorn fastapi_server:app --reload --host 0.0.0.0 --port 8000
```

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/test_processors.py -v
pytest tests/test_integration.py -v
pytest tests/test_performance.py -v

# Run with coverage
pytest --cov=psychological_assessment_system tests/
```

### Production Deployment
```bash
# Docker deployment
make up           # Start all services
make logs         # View logs  
make test         # Run tests
make deploy-prod  # Production deployment

# Access services
# API: http://localhost:8000
# WebSocket: ws://localhost:8765
# Grafana: http://localhost:3000
# Prometheus: http://localhost:9090
```

## Code Architecture Patterns

### Multi-Model Assessment Flow
The system processes text through multiple psychological frameworks simultaneously:
1. **Input Validation**: Pydantic models with clinical validation
2. **NLP Pipeline**: Clinical-grade linguistic analysis
3. **Agent Processing**: CrewAI agents for specialized assessment
4. **Confidence Scoring**: Recursive prompting when confidence < threshold
5. **Result Aggregation**: Cross-framework consistency checking

### Async Processing Pattern
All major operations use asyncio for high-performance concurrent processing:
- Batch assessments processed with semaphore-controlled concurrency
- Database operations use asyncpg connection pools
- WebSocket connections handled with async generators

### Configuration Management
Environment-based configuration through `Config` dataclass:
- API keys for OpenAI, Cohere
- Database URLs (PostgreSQL with pgvector)
- Performance tuning parameters (max_concurrent_assessments, confidence_threshold)

### Error Handling & Resilience
- Circuit breaker patterns for API failures
- Exponential backoff for rate limiting
- Human-in-the-loop escalation for low-confidence assessments
- Comprehensive logging with structured logging

## Data Models & Validation

### Core Assessment Types
```python
class AssessmentType(str, Enum):
    ENNEAGRAM = "enneagram"
    BIG_FIVE = "big_five" 
    EMOTIONAL_INTELLIGENCE = "emotional_intelligence"
    VALUES = "values"
    COGNITIVE_STYLE = "cognitive_style"
```

### Input Validation
- Text input: 10-5000 characters with meaningful content validation
- User IDs: 5-50 characters for proper identification
- Assessment types: Multiple frameworks can be processed simultaneously

### Confidence & Quality Assurance
- Confidence scores (0.0-1.0) for each trait assessment
- Recursive prompting system when confidence < 0.75
- Cross-model validation for consistency checking

## Clinical Features & Compliance

### Clinical-Grade Processing
- Mental health RoBERTa models for risk assessment
- LIWC-style psycholinguistic feature extraction
- Therapy sentiment analysis for emotional state detection
- Temporal orientation analysis for cognitive assessment

### Privacy & Compliance
- GDPR compliance with right to erasure endpoints
- HIPAA-ready deployment with encryption at rest
- Audit trails for all assessment activities
- Pseudonymization for research data protection

## Performance Characteristics

- **Concurrent Processing**: 10,000+ assessments/minute
- **Response Time**: Sub-second for simple assessments  
- **Memory Usage**: <100MB increase under sustained load
- **Confidence Accuracy**: 85-95% correlation with expert assessments
- **Cost Reduction**: 60-70% vs specialized vector databases

## Extension Points

### Adding New Assessment Models
Extend `BaseProcessor` class in clinical framework processors:
```python
class CustomProcessor(BaseProcessor):
    async def process(self, text: str, context: Dict[str, Any]) -> Tuple[List[PersonalityScore], float]:
        # Custom processing logic
        return scores, confidence
```

### Custom Recursive Prompts
Add to prompt generator for specialized questioning:
```python
custom_prompts = {
    "assessment_type": {
        "trait": "Follow-up question for trait assessment"
    }
}
```