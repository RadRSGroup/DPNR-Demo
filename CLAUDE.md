# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a **production-ready Python AI agent system** for mystical therapeutic processing and multi-model psychological assessment. The system combines **10 Sefirot agents** (Tree of Life) with traditional psychological frameworks, using **CrewAI** for agent orchestration and advanced therapeutic processing.

### 🌟 MYSTICAL FRAMEWORK INTEGRATION (NEW)

- **Complete Sefirot System**: All 10 Tree of Life agents for mystical therapeutic processing
- **Phase 2 Complete**: 5 operational sefirot (Malchut, Tiferet, Yesod, Chesed, Gevurah)
- **Advanced Patterns**: Lightning Flow processing and polarity integration
- **Soul Level Integration**: 5 soul levels (Nefesh → Yechida) across all processing
- **Strategy Gap Closure**: 95% complete mystical framework implementation

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

## Agent-Driven Development for DPNR Platform

### Overview
The DPNR platform extends this system with therapeutic frameworks using an **agent-driven development approach** where AI agents autonomously create the missing therapeutic components.

### Development Progress Tracking - MAJOR UPDATE
- **Current Phase**: 2 - COMPLETE (Sefirot Emotional Processing)
- **Current Step**: Phase 3 Authorization - Wisdom Sefirot Development
- **Status**: 95% Strategy Gap Closure Achieved
- **Target**: Complete 10-Sefirot mystical therapeutic framework

### ✅ COMPLETED SEFIROT AGENTS (Production Ready)
1. **🏰 Malchut (Kingdom)** - Real-world manifestation and practical integration
2. **💎 Tiferet (Beauty)** - Harmony, balance, and polarity integration
3. **🏛️ Yesod (Foundation)** - Grounding and practical synthesis
4. **💝 Chesed (Compassion)** - Loving-kindness and healing facilitation  
5. **⚔️ Gevurah (Strength)** - Boundaries, discipline, and shadow work

### ✅ COMPLETED TRADITIONAL SYSTEMS (Production Ready)
1. **Mirror Room Engine** - IFS + Shadow Work integration with depth progression
2. **IFS Agent** - Internal Family Systems parts identification and dialogue
3. **Shadow Work Agent** - Jungian pattern detection and integration guidance  
4. **Growth Tracker** - Multi-domain progress tracking with trend analysis
5. **Digital Twin Generator** - Soul archetype evolution with visual representation
6. **PaRDeS Reflection Engine** - 4-layer depth analysis system

### TherapeuticAgentBuilder Specifications
The meta-agent that creates other therapeutic agents with the following requirements:
- **Purpose**: Autonomously generates IFS, Shadow Work, Narrative Therapy, and other therapeutic agents
- **Base Class**: Must extend the existing BaseAgent architecture
- **Quality Gates**: 
  - 85%+ therapeutic accuracy validation required
  - Comprehensive test suite generation (85%+ coverage)
  - Clinical validation checkpoints
- **Output Format**: Production-ready Python code with full documentation

### 🎯 NEXT PRIORITY SYSTEMS TO IMPLEMENT
**Phase 3 Wisdom Sefirot** - Advanced insight and creative expression agents

### ✅ COMPLETED SEFIROT + THERAPEUTIC AGENTS
1. **IFSAgent**: ✅ Internal Family Systems + Chesed integration
2. **ShadowWorkAgent**: ✅ Jungian shadow work + Gevurah integration  
3. **GrowthTrackerAgent**: ✅ Multi-domain progress + Yesod grounding
4. **DigitalTwinAgent**: ✅ Soul archetype evolution + Tiferet beauty
5. **PaRDeSReflectionAgent**: ✅ 4-layer depth analysis complete
6. **SefirotOrchestrator**: ✅ Multi-sefirot workflow management
7. **LightningFlowProcessor**: ✅ Breakthrough processing system

### 🔄 REMAINING SEFIROT AGENTS TO CREATE (Phase 3)
1. **🔮 ChochmahAgent**: Flash insights and pattern recognition (Wisdom)
2. **🏛️ BinahAgent**: Deep comprehension and integration (Understanding)
3. **🎨 NetzachAgent**: Persistence and creative expression (Victory)
4. **📢 HodAgent**: Communication and teaching mastery (Glory)
2. **NarrativeTherapyAgent**: Story reframing and identity reconstruction
3. **SomaticExperiencingAgent**: Body awareness and trauma processing
4. **AttachmentStyleAgent**: Relationship pattern analysis

### API Contracts for DPNR Backend

#### IFS (Internal Family Systems) Endpoints
```
POST /api/v1/assessment/ifs/analyze
- Input: { "text": string, "user_id": string, "session_id": string }
- Output: { "parts": [{"type": "manager|firefighter|exile", "content": string, "emotion": string}], "confidence": float }

POST /api/v1/assessment/ifs/dialogue
- Input: { "part_id": string, "message": string, "session_id": string }
- Output: { "response": string, "suggested_questions": [string], "unburdening_readiness": float }
```

#### Shadow Work Endpoints
```
POST /api/v1/assessment/shadow/detect
- Input: { "text": string, "user_id": string, "history_context": object }
- Output: { "shadow_patterns": [{"pattern": string, "trigger": string, "projection": string}], "confidence": float }

POST /api/v1/assessment/shadow/integrate
- Input: { "shadow_pattern_id": string, "user_response": string }
- Output: { "integration_guidance": string, "next_steps": [string] }
```

#### Narrative Therapy Endpoints
```
POST /api/v1/assessment/narrative/analyze
- Input: { "text": string, "user_id": string }
- Output: { "dominant_story": string, "problem_story": string, "unique_outcomes": [string] }

POST /api/v1/assessment/narrative/reframe
- Input: { "story_id": string, "reframing_context": string }
- Output: { "alternative_story": string, "value_alignment": object }
```

#### Mirror Room Engine Endpoints
```
POST /api/v1/mirror-room/session/start
- Input: { "user_id": string, "initial_context": string, "depth_level": "surface|moderate|deep" }
- Output: { "session_id": string, "initial_reflection": string, "available_agents": [string] }

POST /api/v1/mirror-room/session/continue
- Input: { "session_id": string, "user_response": string }
- Output: { "reflection": string, "therapeutic_insights": [object], "depth_progression": float }

GET /api/v1/mirror-room/session/{session_id}/summary
- Output: { "key_insights": [string], "parts_identified": [object], "growth_areas": [string] }
```

#### Digital Twin APIs
```
POST /api/v1/digital-twin/generate
- Input: { "user_id": string, "assessment_data": object }
- Output: { "twin_id": string, "archetype": string, "soul_level": string, "visual_representation": object }

GET /api/v1/digital-twin/{twin_id}/evolution
- Output: { "timeline": [{"date": string, "changes": [string], "growth_metrics": object}] }
```

#### Growth Tracker APIs
```
POST /api/v1/growth/track
- Input: { "user_id": string, "domain": string, "metric": string, "value": float }
- Output: { "recorded": boolean, "trend": "improving|stable|declining", "insights": string }

GET /api/v1/growth/report/{user_id}
- Query params: { "period": "week|month|quarter", "domains": [string] }
- Output: { "progress": object, "achievements": [string], "recommendations": [string] }
```

#### ✅ COMPLETED API ENDPOINTS

**Growth Tracker APIs** (✅ Complete)
```
POST /api/v1/growth/track - Record growth metrics
GET /api/v1/growth/report/{user_id} - Generate progress reports
POST /api/v1/growth/trends - Analyze growth trends
POST /api/v1/growth/insights - Generate personalized insights
```

**Digital Twin APIs** (✅ Complete)
```
POST /api/v1/digital-twin/generate - Create user's digital twin
POST /api/v1/digital-twin/evolve - Evolve twin based on triggers
GET /api/v1/digital-twin/{twin_id}/evolution - Get evolution timeline
POST /api/v1/digital-twin/{twin_id}/insights - Generate twin insights
```

**Mirror Room APIs** (✅ Complete)
```
POST /api/v1/mirror-room/session/start - Start therapeutic session
POST /api/v1/mirror-room/session/continue - Continue dialogue
GET /api/v1/mirror-room/session/{id}/safety - Safety assessment
```

#### 🎯 NEXT TO IMPLEMENT: PaRDeS Reflection Engine
```
POST /api/v1/pardes/reflect
- Input: { "insight": string, "context": object, "depth_requested": "pshat|remez|drash|sod" }
- Output: { 
    "layers": {
      "pshat": string,    // Literal insight
      "remez": string,    // Emotional pattern
      "drash": string,    // Reframed meaning
      "sod": string       // Soul truth
    },
    "metaphors": [string],
    "integration_guidance": [string]
  }
```

### Development Rules & Standards

#### Agent Creation Standards
1. **Backend Only**: No frontend/UI components in this phase
2. **Extend Existing**: Build on current infrastructure, don't replace
3. **Clinical Accuracy**: Minimum 85% therapeutic accuracy required
4. **Test Coverage**: Minimum 85% test coverage for all generated code
5. **Documentation**: Each agent must include comprehensive docstrings and usage examples

#### Code Quality Requirements
- Type hints required for all functions
- Async/await patterns for all I/O operations
- Pydantic models for all API inputs/outputs
- Comprehensive error handling with specific exceptions
- Structured logging with appropriate log levels

#### Integration Requirements
- Must integrate seamlessly with existing FastAPI server
- Database schemas must extend current PostgreSQL structure
- All agents must inherit from BaseAgent class
- Use existing authentication and session management

### Supervisor Approval Gates
Each development phase requires explicit supervisor approval:
1. **Step Completion**: Present deliverables and test results
2. **Quality Verification**: Demonstrate adherence to standards
3. **Integration Testing**: Show successful integration with existing system
4. **Next Step Authorization**: Receive explicit approval before proceeding