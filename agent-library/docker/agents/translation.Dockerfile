# Translation Agent Docker Image
FROM agent-library-base:latest

# Install translation-specific dependencies
RUN pip install --no-cache-dir \
    sentencepiece>=0.1.99 \
    sacremoses>=0.0.53 \
    protobuf>=4.25.0

# Download and cache Hebrew translation models
RUN python -c "
from transformers import MarianMTModel, MarianTokenizer, M2M100ForConditionalGeneration, M2M100Tokenizer
import torch

print('Downloading Hebrew translation models...')
# Hebrew models
tokenizer_en_he = MarianTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-he')
model_en_he = MarianMTModel.from_pretrained('Helsinki-NLP/opus-mt-en-he')

tokenizer_he_en = MarianTokenizer.from_pretrained('Helsinki-NLP/opus-mt-he-en')
model_he_en = MarianMTModel.from_pretrained('Helsinki-NLP/opus-mt-he-en')

# Multilingual fallback
tokenizer_multi = M2M100Tokenizer.from_pretrained('facebook/m2m100_418M')
model_multi = M2M100ForConditionalGeneration.from_pretrained('facebook/m2m100_418M')

print('Models downloaded and cached successfully')
"

# Copy translation agent code
COPY agents/language/translation_agent.py ./agent_library/agents/language/

# Create config directory
RUN mkdir -p /app/config

# Agent configuration
ENV AGENT_TYPE=translation
ENV AGENT_ID=translation_agent_1
ENV SUPPORTED_LANGUAGES=en,he,ar,es,fr,de,ru
ENV MAX_TEXT_LENGTH=5000
ENV CONFIDENCE_THRESHOLD=0.75

# Expose agent port
EXPOSE 8001

# Health check for translation agent
HEALTHCHECK --interval=30s --timeout=15s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Start the translation agent
CMD ["python", "-m", "agent_library.agents.language.translation_agent", "--port", "8001"]