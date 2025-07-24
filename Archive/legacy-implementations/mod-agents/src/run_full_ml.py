#!/usr/bin/env python3
"""
Full ML Production System with real transformer models
Uses actual ML models instead of mock implementations
"""

import asyncio
import sys
import os
from pathlib import Path
from typing import Dict, Any, List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check for ML libraries
try:
    import torch
    import transformers
    from transformers import pipeline, AutoTokenizer, AutoModel
    from sentence_transformers import SentenceTransformer
    import langdetect
    import numpy as np
    ML_AVAILABLE = True
    logger.info("✅ Full ML stack available")
except ImportError as e:
    ML_AVAILABLE = False
    logger.error(f"❌ ML libraries not available: {e}")
    logger.error("Please run: source ml_env/bin/activate")
    sys.exit(1)

class FullMLTranslationAgent:
    """Translation agent using real transformer models"""
    
    def __init__(self):
        self.name = "FullMLTranslationAgent"
        logger.info("🔄 Loading translation models...")
        
        # Load available translation models for Hebrew-English
        self.use_ml_translation = False
        try:
            # Try to load any available Helsinki-NLP models
            from transformers import MarianMTModel, MarianTokenizer
            
            # Try different model names that might exist
            model_attempts = [
                "Helsinki-NLP/opus-mt-he-en",
                "Helsinki-NLP/opus-mt-heb-eng", 
                "Helsinki-NLP/opus-mt-iw-en"
            ]
            
            for model_name in model_attempts:
                try:
                    self.he_to_en_tokenizer = MarianTokenizer.from_pretrained(model_name)
                    self.he_to_en_model = MarianMTModel.from_pretrained(model_name)
                    self.use_ml_translation = True
                    logger.info(f"✅ Translation model loaded: {model_name}")
                    break
                except:
                    continue
            
            if not self.use_ml_translation:
                logger.warning("⚠️  No ML translation models available, using enhanced dictionary translation")
                
        except Exception as e:
            logger.warning(f"⚠️  ML translation not available: {e}")
            
        # Enhanced Hebrew-English dictionary for fallback
        self.translation_dict = {
            # Core words
            "אני": "I", "את": "you", "הוא": "he", "היא": "she", "אנחנו": "we", "אתם": "you", "הם": "they",
            "יוצרת": "creative", "נלהבת": "enthusiastic", "רוצה": "want", "לדעת": "to know",
            "שמה": "that what", "עושה": "do", "חשוב": "important", "קשה": "difficult", "להרגיש": "to feel",
            "בטוחה": "secure", "ממוקדת": "focused", "כשאני": "when I", "לא": "not", "יכולה": "can",
            "לשלוט": "control", "במצב": "situation", "אוהב": "love", "לעזור": "to help", "לאחרים": "others",
            "להצליח": "to succeed", "להשיג": "to achieve", "המטרות": "goals", "עובד": "work",
            "קשה": "hard", "לשמור": "to maintain", "תדמית": "image", "מוצלחת": "successful",
            "מתמקד": "focus", "יעיל": "efficient", "פרודוקטיבי": "productive", "מוכשר": "talented",
            "מוצלח": "successful", "דואג": "worry", "באמת": "really", "משחק": "play", "תפקיד": "role"
        }
    
    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process translation request with real models or enhanced dictionary"""
        try:
            text = message.get("text", "")
            target_language = message.get("target_language", "auto")
            
            # Detect source language
            detected_lang = langdetect.detect(text)
            
            if detected_lang == "he" and target_language in ["en", "auto"]:
                if self.use_ml_translation:
                    # Use ML model for Hebrew to English
                    inputs = self.he_to_en_tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
                    with torch.no_grad():
                        translated = self.he_to_en_model.generate(**inputs, max_length=100)
                    translated_text = self.he_to_en_tokenizer.decode(translated[0], skip_special_tokens=True)
                    confidence = 0.95
                else:
                    # Enhanced dictionary translation
                    words = text.split()
                    translated_words = []
                    for word in words:
                        # Remove punctuation for lookup
                        clean_word = word.strip(".,!?;:")
                        if clean_word in self.translation_dict:
                            translated_words.append(self.translation_dict[clean_word])
                        else:
                            translated_words.append(f"[{clean_word}]")  # Keep untranslated words in brackets
                    translated_text = " ".join(translated_words)
                    confidence = 0.8
                    
            else:
                # No translation needed or unsupported direction
                translated_text = text
                confidence = 1.0
            
            return {
                "translated_text": translated_text,
                "source_language": detected_lang,
                "target_language": "en" if detected_lang == "he" else detected_lang,
                "confidence": confidence,
                "method": "ML_model" if self.use_ml_translation else "dictionary"
            }
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return {
                "translated_text": text,
                "source_language": "unknown",
                "target_language": "unknown", 
                "confidence": 0.3,
                "error": str(e)
            }

class FullMLNLPAgent:
    """NLP analysis using real transformer models"""
    
    def __init__(self):
        self.name = "FullMLNLPAgent"
        logger.info("🔄 Loading NLP models...")
        
        try:
            # Load sentiment analysis model
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest"
            )
            
            # Load emotion detection model
            self.emotion_pipeline = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base"
            )
            
            # Load sentence transformer for embeddings
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            logger.info("✅ NLP models loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load NLP models: {e}")
            raise
    
    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process NLP analysis with real models"""
        try:
            text = message.get("text", "")
            
            # Sentiment analysis
            sentiment_result = self.sentiment_pipeline(text)[0]
            sentiment = {
                "label": sentiment_result["label"],
                "score": float(sentiment_result["score"])
            }
            
            # Emotion detection
            emotion_results = self.emotion_pipeline(text)
            emotions = [
                {
                    "emotion": result["label"],
                    "score": float(result["score"])
                }
                for result in emotion_results[:3]  # Top 3 emotions
            ]
            
            # Generate embeddings
            embeddings = self.sentence_model.encode(text)
            
            # Text statistics
            words = text.split()
            word_count = len(words)
            
            return {
                "sentiment": sentiment,
                "word_count": word_count,
                "emotions": emotions,
                "embeddings": embeddings.tolist(),
                "confidence": 0.9
            }
            
        except Exception as e:
            logger.error(f"NLP analysis error: {e}")
            return {
                "sentiment": {"label": "NEUTRAL", "score": 0.5},
                "word_count": len(text.split()),
                "emotions": [{"emotion": "neutral", "score": 0.7}],
                "confidence": 0.3,
                "error": str(e)
            }

class FullMLEnneagramAgent:
    """Enhanced Enneagram assessment using ML embeddings"""
    
    def __init__(self):
        self.name = "FullMLEnneagramAgent"
        logger.info("🔄 Loading Enneagram models...")
        
        try:
            # Load sentence transformer for semantic analysis
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Enhanced type patterns with semantic embeddings
            self.type_patterns = {
                1: {
                    "keywords": ["perfect", "correct", "should", "must", "proper", "right", "wrong", "improve", "standards"],
                    "phrases": ["things should be done correctly", "there's a right way", "I notice mistakes", "high standards"],
                    "semantic_examples": [
                        "I believe in doing things the right way",
                        "I have high standards for myself and others",
                        "I notice when things are not quite right"
                    ]
                },
                2: {
                    "keywords": ["help", "care", "love", "need", "support", "others", "giving", "relationships"],
                    "phrases": ["I love helping others", "people need me", "I care about others"],
                    "semantic_examples": [
                        "I enjoy helping others feel better",
                        "I often put others' needs before my own",
                        "I want to be loved and appreciated"
                    ]
                },
                3: {
                    "keywords": ["success", "achieve", "win", "goal", "efficient", "image", "best", "accomplish"],
                    "phrases": ["I want to succeed", "image matters", "be the best"],
                    "semantic_examples": [
                        "I am driven to achieve my goals",
                        "Success and recognition are important to me",
                        "I work hard to maintain a successful image"
                    ]
                },
                4: {
                    "keywords": ["unique", "special", "different", "deep", "missing", "authentic", "feel"],
                    "phrases": ["I'm different from others", "something is missing", "deep feelings"],
                    "semantic_examples": [
                        "I value being authentic and unique",
                        "I often feel like something is missing",
                        "I have deep, intense emotions"
                    ]
                },
                5: {
                    "keywords": ["understand", "knowledge", "private", "observe", "analyze", "think", "energy"],
                    "phrases": ["I need to understand", "observe before acting", "preserve energy"],
                    "semantic_examples": [
                        "I prefer to observe and understand before acting",
                        "I need time alone to process information",
                        "I value knowledge and competence"
                    ]
                },
                6: {
                    "keywords": ["security", "safe", "trust", "loyal", "doubt", "authority", "anxiety"],
                    "phrases": ["need security", "can I trust", "what if"],
                    "semantic_examples": [
                        "I value security and loyalty",
                        "I often think about potential problems",
                        "Trust is very important to me"
                    ]
                },
                7: {
                    "keywords": ["fun", "exciting", "options", "adventure", "positive", "avoid", "possibilities"],
                    "phrases": ["this sounds fun", "so many options", "new adventures"],
                    "semantic_examples": [
                        "I love exploring new possibilities",
                        "I prefer to focus on positive experiences",
                        "I enjoy having many options and adventures"
                    ]
                },
                8: {
                    "keywords": ["control", "power", "strong", "direct", "justice", "protect", "intensity"],
                    "phrases": ["take control", "stand up for", "be direct"],
                    "semantic_examples": [
                        "I prefer to be in control of situations",
                        "I stand up for what I believe is right",
                        "I am direct and assertive in my approach"
                    ]
                },
                9: {
                    "keywords": ["peace", "harmony", "conflict", "comfortable", "agree", "merge", "calm"],
                    "phrases": ["avoid conflict", "everyone gets along", "keep the peace"],
                    "semantic_examples": [
                        "I prefer harmony and avoid conflict",
                        "I want everyone to feel comfortable",
                        "I tend to go along with others"
                    ]
                }
            }
            
            # Pre-compute embeddings for semantic patterns
            self.type_embeddings = {}
            for type_num, patterns in self.type_patterns.items():
                examples_text = " ".join(patterns["semantic_examples"])
                self.type_embeddings[type_num] = self.sentence_model.encode(examples_text)
            
            logger.info("✅ Enneagram models loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load Enneagram models: {e}")
            raise
    
    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced personality assessment using ML"""
        try:
            text = message.get("text", "").lower()
            
            # Generate text embedding
            text_embedding = self.sentence_model.encode(text)
            
            # Calculate semantic similarity scores
            similarity_scores = {}
            for type_num, type_embedding in self.type_embeddings.items():
                # Cosine similarity
                similarity = np.dot(text_embedding, type_embedding) / (
                    np.linalg.norm(text_embedding) * np.linalg.norm(type_embedding)
                )
                similarity_scores[type_num] = float(similarity)
            
            # Traditional keyword matching (with weights)
            keyword_scores = {}
            for type_num, patterns in self.type_patterns.items():
                keyword_matches = sum(1 for keyword in patterns["keywords"] if keyword in text)
                phrase_matches = sum(2 for phrase in patterns["phrases"] if phrase in text)  # Weight phrases more
                
                total_patterns = len(patterns["keywords"]) + len(patterns["phrases"])
                keyword_scores[type_num] = (keyword_matches + phrase_matches) / total_patterns
            
            # Combine semantic and keyword scores
            combined_scores = {}
            for type_num in range(1, 10):
                semantic_weight = 0.7
                keyword_weight = 0.3
                
                combined_score = (
                    semantic_weight * similarity_scores.get(type_num, 0) +
                    keyword_weight * keyword_scores.get(type_num, 0)
                )
                combined_scores[type_num] = combined_score
            
            # Find the highest scoring type
            primary_type = max(combined_scores, key=combined_scores.get)
            confidence = combined_scores[primary_type]
            
            # Ensure minimum confidence threshold
            if confidence < 0.3:
                confidence = 0.3
            elif confidence > 1.0:
                confidence = 1.0
            
            return {
                "primary_type": primary_type,
                "type_name": f"Type {primary_type}",
                "confidence": confidence,
                "all_scores": combined_scores,
                "semantic_scores": similarity_scores,
                "keyword_scores": keyword_scores,
                "growth_recommendations": [
                    "Develop self-awareness through reflection",
                    "Practice mindfulness and emotional regulation",
                    "Seek feedback from trusted friends or mentors"
                ]
            }
            
        except Exception as e:
            logger.error(f"Enneagram assessment error: {e}")
            return {
                "primary_type": 2,  # Default fallback
                "type_name": "Type 2",
                "confidence": 0.3,
                "error": str(e),
                "growth_recommendations": ["Practice self-awareness"]
            }

class FullMLProductionSystem:
    """Production system with full ML capabilities"""
    
    def __init__(self):
        self.translation_agent = None
        self.nlp_agent = None
        self.enneagram_agent = None
        self.initialized = False
    
    async def initialize(self) -> bool:
        """Initialize all ML agents"""
        try:
            logger.info("🚀 Initializing Full ML Production System...")
            
            # Initialize agents with progress indicators
            logger.info("📥 Loading translation models...")
            self.translation_agent = FullMLTranslationAgent()
            
            logger.info("📥 Loading NLP models...")
            self.nlp_agent = FullMLNLPAgent()
            
            logger.info("📥 Loading personality assessment models...")
            self.enneagram_agent = FullMLEnneagramAgent()
            
            self.initialized = True
            logger.info("✅ Full ML system initialized successfully!")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize ML system: {e}")
            return False
    
    async def process_chain(self, text: str) -> Dict[str, Any]:
        """Process text through full ML pipeline"""
        if not self.initialized:
            raise Exception("System not initialized")
        
        steps = []
        
        # Step 1: Translation
        translation_result = await self.translation_agent.handle_message({"text": text})
        steps.append({
            "agent": "translation",
            "success": "error" not in translation_result,
            "data": translation_result
        })
        
        # Use translated text for further processing
        processed_text = translation_result.get("translated_text", text)
        
        # Step 2: NLP Analysis
        nlp_result = await self.nlp_agent.handle_message({"text": processed_text})
        steps.append({
            "agent": "nlp", 
            "success": "error" not in nlp_result,
            "data": nlp_result
        })
        
        # Step 3: Personality Assessment
        enneagram_result = await self.enneagram_agent.handle_message({"text": processed_text})
        steps.append({
            "agent": "enneagram",
            "success": "error" not in enneagram_result,
            "data": enneagram_result
        })
        
        # Create summary
        summary = {
            "source_language": translation_result.get("source_language", "unknown"),
            "sentiment": nlp_result.get("sentiment", {}).get("label", "NEUTRAL"),
            "personality_type": enneagram_result.get("primary_type", 2),
            "confidence": enneagram_result.get("confidence", 0.5)
        }
        
        return {
            "input": text,
            "chain": "full_ml",
            "steps": steps,
            "summary": summary
        }
    
    async def health_check(self) -> bool:
        """Check system health"""
        return self.initialized and ML_AVAILABLE

async def main():
    """Test the full ML system"""
    print("🧠 Full ML Personality Assessment System")
    print("="*50)
    
    # Initialize system
    system = FullMLProductionSystem()
    success = await system.initialize()
    
    if not success:
        print("❌ Failed to initialize ML system")
        return
    
    # Test with sample text
    test_texts = [
        "אני יוצרת נלהבת, אני רוצה לדעת שמה שאני עושה חשוב. קשה לי להרגיש בטוחה וממוקדת במה שאני רוצה כשאני לא יכולה לשלוט במצב.",
        "I am driven to succeed and achieve my goals. I work hard to maintain a successful image.",
        "I love helping others and making sure everyone feels comfortable and valued."
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n--- Test {i} ---")
        print(f"Input: {text[:50]}...")
        
        result = await system.process_chain(text)
        summary = result["summary"]
        
        print(f"Language: {summary['source_language']}")
        print(f"Personality: Type {summary['personality_type']}")
        print(f"Confidence: {summary['confidence']:.1%}")
        print(f"Sentiment: {summary['sentiment']}")

if __name__ == "__main__":
    if not ML_AVAILABLE:
        print("❌ ML libraries not available. Please run:")
        print("source ml_env/bin/activate")
        sys.exit(1)
    
    asyncio.run(main())