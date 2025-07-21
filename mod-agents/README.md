# ModAgents - AI Assessment System

A production-ready AI agent system for multi-model psychological assessment, built with CrewAI and FastAPI.

## 🚀 Quick Deploy on Render

### 1. One-Click Deploy
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/RadRSGroup/DPNR-Demo/tree/ModAgents)

### 2. Manual Setup

1. **Fork/Clone** this repository
2. **Connect to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Select the `ModAgents` branch
   - Set root directory: `mod-agents`

3. **Add Environment Variables** (in Render dashboard):
   ```
   OPENAI_API_KEY=your_openai_key_here
   COHERE_API_KEY=your_cohere_key_here
   ```

4. **Deploy** - Render will automatically build and deploy!

## 🏗️ Architecture

```
mod-agents/
├── render.yaml          # Render deployment config
├── Dockerfile           # Container configuration
├── docker-compose.yml   # Local development
├── requirements.txt     # Python dependencies
└── src/                 # Source code
    ├── agent_library/   # Core agent framework
    └── frontend_api_server.py  # Main API server
```

## 🔧 Local Development

```bash
# Clone and run locally
git clone https://github.com/RadRSGroup/DPNR-Demo.git
cd DPNR-Demo
git checkout ModAgents
cd mod-agents

# Start with Docker Compose
docker-compose up

# Or run directly
pip install -r requirements.txt
uvicorn src.frontend_api_server:app --reload
```

## 📊 Available Assessments

- **Enneagram Types** - 9 personality types focused on core motivations
- **Big Five Traits** - Five-factor model with personality dimensions  
- **Personal Values** - Schwartz's 10 universal human values
- **Emotional Intelligence** - Four-domain EQ assessment
- **Cognitive Style** - Thinking patterns and information processing
- **Clinical Language Analysis** - Psycholinguistic markers and risk assessment

## 🛠️ API Endpoints

- `GET /health` - Health check and available assessments
- `POST /assess` - Run psychological assessments
- `GET /docs` - Interactive API documentation
- `GET /` - Web interface for testing

## 🔐 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for GPT models |
| `COHERE_API_KEY` | No | Cohere API key for embeddings |
| `REDIS_URL` | Auto | Redis connection (auto-set by Render) |
| `LOG_LEVEL` | No | Logging level (default: INFO) |
| `CONFIDENCE_THRESHOLD` | No | Min confidence for assessments (default: 0.75) |

## 🚦 Monitoring

- Health endpoint: `https://your-app.onrender.com/health`
- Logs: Available in Render dashboard
- Metrics: Built-in FastAPI metrics

## 🔄 Updates

The system auto-deploys on pushes to the `ModAgents` branch. To update:

```bash
git push origin ModAgents
```

## 🆘 Troubleshooting

- **Build fails**: Check requirements.txt and Dockerfile
- **Redis connection**: Ensure Redis service is running in Render
- **API errors**: Check environment variables are set
- **Port issues**: Render auto-assigns PORT variable

## 📞 Support

For issues or questions, check the [GitHub repository](https://github.com/RadRSGroup/DPNR-Demo/tree/ModAgents).