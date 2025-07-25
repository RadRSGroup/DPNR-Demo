# DPNR CrewAI Therapeutic System

## Overview

A production-ready CrewAI-based psychological assessment and therapeutic intervention system. This unified platform coordinates multiple AI agents to provide comprehensive mental health support through various therapeutic modalities.

## Quick Start

### 1. Installation

```bash
cd unified_agent_system
pip install -r requirements.txt
```

### 2. Environment Setup

Copy `.env` file and configure your API keys:

```bash
# Required API Keys
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here  # Optional
COHERE_API_KEY=your_cohere_key_here  # Optional

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 3. Run the System

```bash
# Run with uvicorn
uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Or run directly
python main.py
```

### 4. Access API

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Mirror Room**: http://localhost:8000/mirror-room

## Therapeutic Agents

### Available Agents

1. **IFS Agent** - Internal Family Systems parts work and dialogue
2. **Shadow Work Agent** - Jungian unconscious pattern integration
3. **PaRDeS Reflection Agent** - 4-layer Kabbalistic interpretation
4. **Growth Tracker Agent** - Multi-domain progress monitoring  
5. **Digital Twin Agent** - Soul archetype evolution tracking

### Therapeutic Focus Options

- `IFS` - Internal Family Systems dialogue
- `Shadow Work` - Jungian shadow integration
- `PaRDeS` - Multi-layer mystical reflection
- `Growth Tracking` - Progress analysis and insights
- `Digital Twin` - Archetypal evolution tracking

## API Usage

### Mirror Room Session

```bash
curl -X POST "http://localhost:8000/mirror-room" \
  -H "Authorization: Bearer dummy_token" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I feel like there are different parts of me that want different things",
    "therapeutic_focus": "IFS"
  }'
```

### Response Format

```json
{
  "success": true,
  "therapeutic_focus": "IFS",
  "result": "Therapeutic response from CrewAI agents...",
  "error": null
}
```

## Architecture

### CrewAI Components

- **Agents** (`agents/`): Specialized therapeutic AI agents
- **Crews** (`crews/`): Orchestration logic for agent coordination
- **Tasks** (`tasks/`): Specific therapeutic task definitions
- **Tools** (`tools/`): Assessment and analysis tools
- **Prompts** (`prompts/`): Agent behavior and response guidance

### Key Features

- **Production-Ready**: Full FastAPI application with proper error handling
- **Environment Configuration**: Secure API key management
- **Multiple LLM Support**: Gemini, OpenAI, Cohere integration
- **Therapeutic Safety**: Built-in safety protocols and boundaries
- **Extensible**: Easy to add new agents and therapeutic modalities

## Development

### Project Structure

```
unified_agent_system/
   .env                    # Environment configuration
   api.py                 # FastAPI application
   config.py              # Configuration management
   main.py               # Application entry point
   requirements.txt       # Python dependencies
   agents/               # CrewAI therapeutic agents
   crews/                # Agent orchestration
   tasks/                # Therapeutic task definitions
   tools/                # Assessment and analysis tools
   prompts/              # Agent prompts and behaviors
```

### Adding New Agents

1. Define agent in `agents/therapeutic_agents.py`
2. Create tasks in `tasks/therapeutic_tasks.py`
3. Add orchestration logic in `crews/mirror_room_crew.py`
4. Update API endpoints in `api.py`

### Testing

```bash
# Check health
curl http://localhost:8000/health

# Test Mirror Room with different focuses
curl -X POST http://localhost:8000/mirror-room \
  -H "Authorization: Bearer dummy_token" \
  -H "Content-Type: application/json" \
  -d '{"text": "I had a profound realization today", "therapeutic_focus": "PaRDeS"}'
```

## Production Deployment

### Environment Variables

```bash
# Production settings
ENVIRONMENT=production
LOG_LEVEL=INFO
GEMINI_API_KEY=your_production_key
DATABASE_URL=postgresql://user:pass@db/dpnr
REDIS_URL=redis://cache:6379
```

### Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f
```

## Safety & Compliance

- **Therapeutic Boundaries**: Agents maintain appropriate therapeutic boundaries
- **Crisis Detection**: Built-in safety protocols for emergency situations
- **Data Privacy**: Secure handling of sensitive therapeutic content
- **Professional Integration**: Designed for human therapist oversight

---

**DPNR CrewAI System v1.0**  
*Production-Ready Therapeutic AI Platform*