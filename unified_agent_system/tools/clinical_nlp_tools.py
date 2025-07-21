
import asyncio
from typing import Dict, List, Any
from transformers import pipeline
from sentence_transformers import SentenceTransformer

class NLPPipeline:
    """
    A tool for performing various NLP analyses on text.
    This includes sentiment analysis, emotion detection, and embedding generation.
    """
    def __init__(self):
        # These models are loaded once when the class is instantiated.
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
        self.emotion_analyzer = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base"
        )
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    async def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Performs a comprehensive NLP analysis of the input text.
        """
        # Run different analyses concurrently for efficiency.
        sentiment_task = asyncio.create_task(self._analyze_sentiment(text))
        emotion_task = asyncio.create_task(self._analyze_emotions(text))
        embedding_task = asyncio.create_task(self._generate_embedding(text))
        
        sentiment, emotions, embedding = await asyncio.gather(
            sentiment_task, emotion_task, embedding_task
        )
        
        return {
            "sentiment": sentiment,
            "emotions": emotions,
            "embedding": embedding,
            "text_stats": self._extract_text_stats(text)
        }
    
    async def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        result = self.sentiment_analyzer(text)[0]
        return {"label": result["label"], "score": result["score"]}
    
    async def _analyze_emotions(self, text: str) -> List[Dict[str, float]]:
        results = self.emotion_analyzer(text)
        return [{"emotion": r["label"], "score": r["score"]} for r in results]
    
    async def _generate_embedding(self, text: str) -> List[float]:
        embedding = self.embedding_model.encode(text)
        return embedding.tolist()
    
    def _extract_text_stats(self, text: str) -> Dict[str, Any]:
        words = text.split()
        word_count = len(words)
        return {
            "word_count": word_count,
            "avg_word_length": sum(len(w) for w in words) / word_count if word_count > 0 else 0,
            "sentence_count": text.count('.') + text.count('!') + text.count('?'),
            "complexity_score": len(set(words)) / word_count if word_count > 0 else 0
        }
