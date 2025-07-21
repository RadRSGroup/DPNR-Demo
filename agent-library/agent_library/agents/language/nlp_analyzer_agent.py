"""NLP Analyzer Agent - Extracts linguistic features, sentiment, and emotions"""
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import asyncio
import logging
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import numpy as np

from agent_library.core.base_agent import (
    ChainableAgent, AgentMessage, AgentResponse, 
    AgentCapability, AgentStatus
)


class NLPAnalyzerAgent(ChainableAgent):
    """Agent specialized in natural language processing and linguistic analysis"""
    
    def __init__(self, agent_id: str = "nlp_analyzer", features: List[str] = None):
        super().__init__(agent_id, "NLP Analyzer Agent", "1.0.0")
        self.features = features or ["sentiment", "emotion", "embedding", "stats"]
        self.models = {}
        
        # Define capabilities
        self._capabilities = [
            AgentCapability(
                name="analyze_text",
                description="Comprehensive NLP analysis of text",
                input_schema={
                    "text": "string",
                    "features": "list[string] (optional)"
                },
                output_schema={
                    "sentiment": "dict",
                    "emotions": "list[dict]",
                    "embedding": "list[float]",
                    "text_stats": "dict",
                    "linguistic_features": "dict"
                },
                performance_sla={
                    "max_response_time": 1.0,  # seconds
                    "min_confidence": 0.8,
                    "max_text_length": 5000
                }
            ),
            AgentCapability(
                name="extract_keywords",
                description="Extract key terms and phrases",
                input_schema={"text": "string", "top_k": "int (optional, default=10)"},
                output_schema={"keywords": "list[dict]"},
                performance_sla={"max_response_time": 0.5}
            ),
            AgentCapability(
                name="batch_analyze",
                description="Analyze multiple texts in parallel",
                input_schema={
                    "texts": "list[string]",
                    "features": "list[string] (optional)"
                },
                output_schema={"analyses": "list[dict]"},
                performance_sla={
                    "max_response_time": 15.0,
                    "max_batch_size": 100
                }
            )
        ]
    
    async def initialize(self) -> bool:
        """Initialize NLP models"""
        try:
            self.logger.info("Initializing NLP models...")
            
            # Load sentiment analysis model
            if "sentiment" in self.features:
                self.models["sentiment"] = pipeline(
                    "sentiment-analysis",
                    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
                )
            
            # Load emotion analysis model
            if "emotion" in self.features:
                self.models["emotion"] = pipeline(
                    "text-classification",
                    model="j-hartmann/emotion-english-distilroberta-base"
                )
            
            # Load embedding model
            if "embedding" in self.features:
                self.models["embedding"] = SentenceTransformer('all-MiniLM-L6-v2')
            
            self.logger.info("NLP models initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize NLP models: {str(e)}")
            self.status = AgentStatus.ERROR
            return False
    
    async def process(self, message: AgentMessage) -> AgentResponse:
        """Process NLP analysis request"""
        start_time = datetime.utcnow()
        
        try:
            action = message.payload.get("action", "analyze_text")
            
            if action == "analyze_text":
                result = await self._analyze_text(
                    message.payload.get("text"),
                    message.payload.get("features", self.features)
                )
            elif action == "extract_keywords":
                result = await self._extract_keywords(
                    message.payload.get("text"),
                    message.payload.get("top_k", 10)
                )
            elif action == "batch_analyze":
                result = await self._batch_analyze(
                    message.payload.get("texts"),
                    message.payload.get("features", self.features)
                )
            else:
                raise ValueError(f"Unknown action: {action}")
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return AgentResponse(
                success=True,
                data=result,
                processing_time=processing_time,
                agent_id=self.agent_id,
                confidence=result.get("confidence", 0.9)
            )
            
        except Exception as e:
            self.logger.error(f"NLP analysis error: {str(e)}")
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return AgentResponse(
                success=False,
                error=str(e),
                processing_time=processing_time,
                agent_id=self.agent_id
            )
    
    async def _analyze_text(self, text: str, features: List[str]) -> Dict[str, Any]:
        """Perform comprehensive text analysis"""
        tasks = []
        results = {}
        
        # Run analyses in parallel
        if "sentiment" in features and "sentiment" in self.models:
            tasks.append(("sentiment", self._analyze_sentiment(text)))
        
        if "emotion" in features and "emotion" in self.models:
            tasks.append(("emotion", self._analyze_emotions(text)))
        
        if "embedding" in features and "embedding" in self.models:
            tasks.append(("embedding", self._generate_embedding(text)))
        
        if "stats" in features:
            tasks.append(("stats", self._extract_text_stats(text)))
        
        if "linguistic" in features:
            tasks.append(("linguistic", self._extract_linguistic_features(text)))
        
        # Execute all tasks
        if tasks:
            task_results = await asyncio.gather(*[task[1] for task in tasks])
            for i, (feature_name, _) in enumerate(tasks):
                results[feature_name] = task_results[i]
        
        # Calculate overall confidence
        confidence = self._calculate_confidence(results)
        results["confidence"] = confidence
        
        return results
    
    async def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        try:
            result = self.models["sentiment"](text)[0]
            return {
                "label": result["label"],
                "score": float(result["score"]),
                "polarity": self._map_sentiment_polarity(result["label"])
            }
        except Exception as e:
            self.logger.warning(f"Sentiment analysis failed: {str(e)}")
            return {"label": "NEUTRAL", "score": 0.5, "polarity": 0.0}
    
    async def _analyze_emotions(self, text: str) -> List[Dict[str, Any]]:
        """Analyze emotions in text"""
        try:
            results = self.models["emotion"](text)
            emotions = []
            for result in results:
                emotions.append({
                    "emotion": result["label"],
                    "score": float(result["score"]),
                    "intensity": self._categorize_intensity(result["score"])
                })
            return sorted(emotions, key=lambda x: x["score"], reverse=True)
        except Exception as e:
            self.logger.warning(f"Emotion analysis failed: {str(e)}")
            return [{"emotion": "neutral", "score": 0.5, "intensity": "moderate"}]
    
    async def _generate_embedding(self, text: str) -> List[float]:
        """Generate text embedding"""
        try:
            embedding = self.models["embedding"].encode(text)
            return embedding.tolist()
        except Exception as e:
            self.logger.warning(f"Embedding generation failed: {str(e)}")
            return [0.0] * 384  # Default embedding size
    
    async def _extract_text_stats(self, text: str) -> Dict[str, Any]:
        """Extract basic text statistics"""
        words = text.split()
        sentences = text.replace('!', '.').replace('?', '.').split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "avg_word_length": sum(len(w) for w in words) / len(words) if words else 0,
            "avg_sentence_length": len(words) / len(sentences) if sentences else 0,
            "char_count": len(text),
            "unique_words": len(set(word.lower() for word in words)),
            "lexical_diversity": len(set(word.lower() for word in words)) / len(words) if words else 0,
            "readability_score": self._calculate_readability(text, words, sentences)
        }
    
    async def _extract_linguistic_features(self, text: str) -> Dict[str, Any]:
        """Extract advanced linguistic features"""
        words = text.split()
        
        # Punctuation analysis
        punctuation_count = sum(1 for char in text if char in '.,!?;:')
        
        # Capitalization patterns
        caps_count = sum(1 for char in text if char.isupper())
        
        # Question and exclamation patterns
        questions = text.count('?')
        exclamations = text.count('!')
        
        # Word length distribution
        word_lengths = [len(word) for word in words]
        
        return {
            "punctuation_density": punctuation_count / len(text) if text else 0,
            "capitalization_ratio": caps_count / len(text) if text else 0,
            "question_density": questions / len(words) if words else 0,
            "exclamation_density": exclamations / len(words) if words else 0,
            "avg_word_length": np.mean(word_lengths) if word_lengths else 0,
            "word_length_variance": np.var(word_lengths) if word_lengths else 0,
            "long_word_ratio": sum(1 for length in word_lengths if length > 6) / len(word_lengths) if word_lengths else 0,
            "complexity_indicator": self._calculate_complexity(text, words)
        }
    
    def _map_sentiment_polarity(self, label: str) -> float:
        """Map sentiment label to numerical polarity"""
        mapping = {
            "POSITIVE": 1.0,
            "NEGATIVE": -1.0,
            "NEUTRAL": 0.0
        }
        return mapping.get(label.upper(), 0.0)
    
    def _categorize_intensity(self, score: float) -> str:
        """Categorize emotion intensity"""
        if score >= 0.8:
            return "high"
        elif score >= 0.6:
            return "moderate"
        elif score >= 0.4:
            return "low"
        else:
            return "minimal"
    
    def _calculate_readability(self, text: str, words: List[str], sentences: List[str]) -> float:
        """Calculate simplified readability score"""
        if not sentences or not words:
            return 0.0
        
        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Simplified Flesch-like score
        readability = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_word_length / 4.7)
        return max(0, min(100, readability)) / 100  # Normalize to 0-1
    
    def _calculate_complexity(self, text: str, words: List[str]) -> float:
        """Calculate text complexity indicator"""
        if not words:
            return 0.0
        
        # Factors: vocabulary diversity, sentence structure, word length
        vocab_diversity = len(set(word.lower() for word in words)) / len(words)
        avg_word_length = sum(len(word) for word in words) / len(words)
        sentence_variety = len(set(len(s.split()) for s in text.split('.') if s.strip()))
        
        complexity = (vocab_diversity * 0.4) + (min(avg_word_length / 10, 1) * 0.3) + (min(sentence_variety / 10, 1) * 0.3)
        return min(complexity, 1.0)
    
    def _calculate_confidence(self, results: Dict[str, Any]) -> float:
        """Calculate overall confidence in analysis"""
        confidences = []
        
        # Sentiment confidence
        if "sentiment" in results:
            confidences.append(results["sentiment"]["score"])
        
        # Emotion confidence (top emotion)
        if "emotion" in results and results["emotion"]:
            confidences.append(results["emotion"][0]["score"])
        
        # Text stats are always confident
        if "stats" in results:
            confidences.append(0.95)
        
        return sum(confidences) / len(confidences) if confidences else 0.8
    
    async def _extract_keywords(self, text: str, top_k: int) -> Dict[str, Any]:
        """Extract keywords from text"""
        words = text.lower().split()
        
        # Simple frequency-based keyword extraction
        word_freq = {}
        for word in words:
            if len(word) > 3 and word.isalpha():  # Filter short words and non-alphabetic
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and take top_k
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        return {
            "keywords": [
                {"word": word, "frequency": freq, "relevance": freq / len(words)}
                for word, freq in keywords
            ],
            "total_unique_words": len(word_freq)
        }
    
    async def _batch_analyze(self, texts: List[str], features: List[str]) -> Dict[str, Any]:
        """Analyze multiple texts in parallel"""
        tasks = []
        for i, text in enumerate(texts):
            tasks.append(self._analyze_text(text, features))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        analyses = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                analyses.append({
                    "index": i,
                    "error": str(result),
                    "text_preview": texts[i][:100] + "..." if len(texts[i]) > 100 else texts[i]
                })
            else:
                analyses.append({
                    "index": i,
                    **result
                })
        
        return {"analyses": analyses}
    
    async def validate_input(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate input data"""
        action = data.get("action", "analyze_text")
        
        if action == "analyze_text":
            if not data.get("text"):
                return False, "Text is required for analysis"
            if len(data["text"]) > 5000:
                return False, "Text exceeds maximum length of 5000 characters"
                
        elif action == "extract_keywords":
            if not data.get("text"):
                return False, "Text is required for keyword extraction"
            top_k = data.get("top_k", 10)
            if not isinstance(top_k, int) or top_k < 1 or top_k > 100:
                return False, "top_k must be an integer between 1 and 100"
                
        elif action == "batch_analyze":
            if not data.get("texts") or not isinstance(data["texts"], list):
                return False, "Texts list is required for batch analysis"
            if len(data["texts"]) > 100:
                return False, "Batch size exceeds maximum of 100 texts"
            if any(len(text) > 5000 for text in data["texts"]):
                return False, "One or more texts exceed maximum length of 5000 characters"
        
        return True, None
    
    def get_capabilities(self) -> List[AgentCapability]:
        """Return agent capabilities"""
        return self._capabilities