# DPNR Platform - Deployment Guide

## Quick Production Setup

### 1. Environment Setup
```bash
# Clone repository
git clone <repository-url>
cd DPNR-Demo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
Create `.env` file:
```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (for enhanced features)
POSTGRES_URL=postgresql://user:pass@localhost/dpnr
REDIS_URL=redis://localhost:6379

# Production settings
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### 3. Run Production Server
```bash
cd agent-library
uvicorn fastapi_server:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints Overview

### Core Therapeutic Agents
- **IFS**: `/api/v1/assessment/ifs/` - Internal Family Systems
- **Shadow Work**: `/api/v1/assessment/shadow/` - Jungian shadow integration
- **Growth Tracker**: `/api/v1/growth/` - Progress monitoring
- **Digital Twin**: `/api/v1/digital-twin/` - Soul archetype evolution
- **PaRDeS**: `/api/v1/pardes/` - Multi-layer reflection
- **Narrative**: `/api/v1/assessment/narrative/` - Story reframing

### Mirror Room Orchestration
- **Start Session**: `POST /api/v1/mirror-room/session/start`
- **Continue**: `POST /api/v1/mirror-room/session/continue`
- **Safety Check**: `GET /api/v1/mirror-room/session/{id}/safety`

### Health & Monitoring
- **Health Check**: `GET /health`
- **API Docs**: `GET /docs`
- **OpenAPI**: `GET /openapi.json`

## Safety & Clinical Features

### Crisis Detection
- Automatic detection of suicidal ideation, self-harm indicators
- Immediate escalation to crisis resources (988, 911)
- Human therapist referral protocols

### Therapeutic Safety
- Session depth progression with safety gates
- Trauma-informed pacing and boundaries
- Comprehensive logging for clinical oversight

## System Architecture

### Core Components
```
agent-library/
├── agent_library/
│   ├── core/                 # Base agent framework
│   ├── agents/assessment/    # 8 therapeutic agents
│   └── orchestration/        # Mirror Room engine
├── fastapi_server.py        # Production API server
└── requirements.txt         # Dependencies
```

### Production Features
- **Async Processing**: Full async/await patterns
- **Error Handling**: Comprehensive exception management
- **Logging**: Structured logging with session tracking
- **Monitoring**: Health checks and metrics endpoints
- **Security**: Input validation, rate limiting, CORS

## Development Team Integration

### Code Quality Standards
- **Type Hints**: Required on all functions
- **Pydantic Models**: All API inputs/outputs validated
- **Async Patterns**: Non-blocking I/O throughout
- **Error Boundaries**: Graceful degradation

### Testing Integration
```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests (when available)
pytest tests/ -v

# Type checking
mypy agent_library/

# Code formatting
black agent_library/
```

### Database Integration (Optional)
For enhanced features, integrate with PostgreSQL:
```sql
-- Create database
CREATE DATABASE dpnr;

-- Install pgvector for embeddings (optional)
CREATE EXTENSION vector;

-- Tables will be created automatically by the application
```

## Security Considerations

### API Security
- Input validation on all endpoints
- Rate limiting per IP/user
- CORS configuration for web clients
- Authentication/authorization ready

### Data Privacy
- Session isolation and cleanup
- No persistent storage of sensitive data
- GDPR compliance ready
- HIPAA-ready architecture

## Monitoring & Observability

### Logging
- Structured JSON logging
- Session-based correlation IDs
- Safety event alerting
- Performance metrics

### Health Checks
```bash
# Check system health
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2025-01-21T...",
  "agents": {
    "ifs": "operational",
    "shadow_work": "operational",
    "mirror_room": "operational"
  }
}
```

## Troubleshooting

### Common Issues

1. **OpenAI API Key Missing**
   ```
   Error: OpenAI API key not configured
   Solution: Set OPENAI_API_KEY in environment
   ```

2. **Import Errors**
   ```
   Error: ModuleNotFoundError
   Solution: Ensure virtual environment is activated and requirements installed
   ```

3. **Port Already In Use**
   ```
   Error: [Errno 48] Address already in use
   Solution: Change port with --port 8001 or kill existing process
   ```

### Performance Optimization
- Use Redis for session caching (optional)
- Configure database connection pooling
- Implement horizontal scaling with load balancer
- Monitor memory usage with multiple workers

## Support & Escalation

### Crisis Protocols
- **Emergency**: Automatic escalation to crisis hotlines
- **Professional**: Human therapist referral system
- **Safety**: Continuous monitoring and intervention

### Technical Support
- Comprehensive error logging for debugging
- Session replay capability for issue investigation
- Performance metrics for optimization

---

**DPNR Platform v1.0**  
*Production-Ready AI Therapeutic System*

For technical questions, refer to README.md and API documentation at `/docs`.