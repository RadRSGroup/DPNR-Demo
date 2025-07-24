# 🧪 Agent Library - Testing Team Deployment Guide

## 📋 **Quick Start for Testing Teams**

This guide provides multiple deployment options for testing the Agent Library psychological assessment system.

---

## 🐳 **Option 1: Docker Deployment (Recommended)**

### Prerequisites
- Docker installed on your system
- Port 8000 available

### Quick Run
```bash
# 1. Clone/download the agent-library folder
cd agent-library

# 2. Build the Docker image
docker build -t agent-library .

# 3. Run the container
docker run -p 8000:8000 agent-library
```

### Access the System
- **Web Interface**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **Assessment API**: POST to http://localhost:8000/assess

### Test Cases
1. **English Assessment**:
   ```
   "I am a very organized person who likes to plan everything carefully. I value achievement and success, and I work hard to reach my goals."
   ```

2. **Hebrew Assessment**:
   ```
   "אני אדם יצירתי שאוהב לחקור דברים חדשים. חשוב לי להיות עצמאי ולעשות דברים בדרך שלי."
   ```

---

## 🐍 **Option 2: Python Direct Run**

### Prerequisites
- Python 3.9+
- pip package manager

### Quick Setup
```bash
# 1. Navigate to agent-library directory
cd agent-library

# 2. Install minimal dependencies
pip install langdetect orjson

# 3. Run the simple server
python3 simple_docker_server.py
```

### Access
- Same as Docker option: http://localhost:8000

---

## 📊 **Option 3: Full Feature Testing**

### For Complete System Testing

```bash
# 1. Install all dependencies
pip install -r requirements.txt

# 2. Run comprehensive system
python3 frontend_api_server.py
```

### Features Available
- ✅ All 6 psychological frameworks
- ✅ Hebrew-English translation
- ✅ Interactive sessions
- ✅ Cross-framework insights
- ✅ Clinical analysis

---

## 🧪 **Testing Scenarios**

### Scenario 1: Basic Functionality
1. Open http://localhost:8000
2. Enter test text (English or Hebrew)
3. Click "Run Assessment"
4. Verify personality type result

### Scenario 2: API Testing
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test assessment endpoint
curl -X POST http://localhost:8000/assess \\
  -H "Content-Type: application/json" \\
  -d '{"text": "I am very creative and love exploring new ideas."}'
```

### Scenario 3: Multi-language Support
1. Input Hebrew text: "אני אדם יצירתי ונלהב"
2. Verify language detection
3. Check assessment results

### Scenario 4: Error Handling
1. Test with insufficient text (< 10 characters)
2. Test with invalid API requests
3. Verify appropriate error messages

---

## 📈 **Expected Results**

### Successful Assessment Response
```json
{
  "assessment_type": "Enneagram",
  "result": "Type 7 - The Enthusiast",
  "confidence": 0.85,
  "detected_language": "en",
  "patterns_found": 3,
  "message": "Assessment complete! Based on your text, you align most with Type 7 - The Enthusiast.",
  "timestamp": "2024-01-20T10:30:00Z"
}
```

### Health Check Response
```json
{
  "status": "healthy",
  "message": "Agent Library Docker Container Running",
  "version": "1.0.0",
  "features": [
    "Enneagram Assessment",
    "Big Five Personality",
    "Values Assessment",
    "Emotional Intelligence",
    "Cognitive Style",
    "Clinical Language Analysis",
    "Hebrew-English Translation"
  ]
}
```

---

## 🐛 **Troubleshooting**

### Common Issues

#### Port Already in Use
```bash
# Use different port
docker run -p 8001:8000 agent-library
# Access: http://localhost:8001
```

#### Docker Build Fails
```bash
# Clean build
docker system prune -f
docker build --no-cache -t agent-library .
```

#### Python Dependencies Missing
```bash
# Install minimal requirements
pip install langdetect orjson

# Or full requirements
pip install -r requirements.txt
```

### Quick Validation
```bash
# Test if system is running
curl http://localhost:8000/health

# Expected: HTTP 200 with JSON response
```

---

## 📋 **Test Plan Template**

### ✅ **Functional Tests**
- [ ] Container starts successfully
- [ ] Web interface loads (http://localhost:8000)
- [ ] Health endpoint responds (http://localhost:8000/health)
- [ ] Assessment processes English text
- [ ] Assessment processes Hebrew text
- [ ] Results include personality type and confidence
- [ ] Error handling for invalid input

### ✅ **Performance Tests**
- [ ] Response time < 3 seconds for typical assessment
- [ ] System handles 10 concurrent requests
- [ ] Memory usage remains stable
- [ ] No memory leaks after 100 assessments

### ✅ **API Tests**
- [ ] POST /assess with valid input returns 200
- [ ] POST /assess with invalid input returns 400
- [ ] GET /health returns 200
- [ ] CORS headers present for web access

### ✅ **Language Tests**
- [ ] English text assessed correctly
- [ ] Hebrew text detected and processed
- [ ] Mixed language text handled gracefully
- [ ] Special characters don't break system

---

## 🚀 **Production Deployment Notes**

### Docker Compose (for scaled testing)
```yaml
version: '3.8'
services:
  agent-library:
    image: agent-library
    ports:
      - "8000:8000"
    environment:
      - LOG_LEVEL=INFO
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Environment Variables
```bash
# Optional configuration
export LOG_LEVEL=DEBUG
export ASSESSMENT_TIMEOUT=30
export MAX_TEXT_LENGTH=5000
```

---

## 📞 **Support & Feedback**

### For Testing Teams:
1. **Log Issues**: Document any errors with request/response examples
2. **Performance**: Note response times and resource usage
3. **Usability**: Test the web interface across browsers
4. **Edge Cases**: Try unusual inputs, long text, special characters

### Success Criteria:
- ✅ System starts in < 30 seconds
- ✅ Assessments complete in < 5 seconds
- ✅ All test scenarios pass
- ✅ No critical errors in logs
- ✅ Web interface is responsive and functional

---

**Ready for comprehensive psychological assessment testing! 🧠✨**