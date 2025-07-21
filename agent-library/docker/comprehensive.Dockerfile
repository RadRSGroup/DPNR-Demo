# Comprehensive Assessment System Docker Image
FROM agent-library-base:latest

# Set working directory
WORKDIR /app

# Copy comprehensive assessment system files
COPY comprehensive_assessment_system.py .
COPY frontend_api_server.py .

# Verify all ML libraries are available and working
RUN python -c "\
import torch; \
import transformers; \
import sentence_transformers; \
import langdetect; \
import numpy; \
import pandas; \
print('✅ PyTorch version:', torch.__version__); \
print('✅ Transformers version:', transformers.__version__); \
print('✅ Sentence-transformers version:', sentence_transformers.__version__); \
print('✅ Language detection available'); \
print('✅ All ML libraries verified successfully!')"

# Note: Import tests will be done at runtime to avoid build complexity

# Create directories for model caching and temporary files
RUN mkdir -p /app/models /app/cache /app/logs

# Set comprehensive assessment system environment variables
ENV COMPREHENSIVE_ASSESSMENT=true
ENV ENABLE_TRANSLATION=true
ENV ENABLE_INTERACTIVE_SESSIONS=true
ENV LOG_LEVEL=INFO
ENV MAX_CONCURRENT_ASSESSMENTS=10
ENV CONFIDENCE_THRESHOLD=0.75

# Expose the frontend API port
EXPOSE 8000

# Health check specific to comprehensive system
HEALTHCHECK --interval=30s --timeout=15s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the comprehensive frontend API server
CMD ["python", "frontend_api_server.py"]