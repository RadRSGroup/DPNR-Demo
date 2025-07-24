"""Translation Agent - Handles language translation with focus on Hebrew"""
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import asyncio
import os
from transformers import MarianMTModel, MarianTokenizer, M2M100ForConditionalGeneration, M2M100Tokenizer
import torch
from langdetect import detect
import logging

from ...core.base_agent import (
    ChainableAgent, AgentMessage, AgentResponse, 
    AgentCapability, AgentStatus
)


class TranslationAgent(ChainableAgent):
    """Agent specialized in translation, with optimized support for Hebrew"""
    
    def __init__(self, agent_id: str = "translation_agent", supported_languages: List[str] = None):
        super().__init__(agent_id, "Translation Agent", "1.0.0")
        self.supported_languages = supported_languages or ["en", "he", "es", "fr", "de", "ar", "ru"]
        self.models = {}
        self.tokenizers = {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Define capabilities
        self._capabilities = [
            AgentCapability(
                name="translate",
                description="Translate text between supported languages",
                input_schema={
                    "text": "string",
                    "source_language": "string (optional, auto-detected if not provided)",
                    "target_language": "string (required)"
                },
                output_schema={
                    "translated_text": "string",
                    "source_language": "string",
                    "target_language": "string",
                    "confidence": "float"
                },
                performance_sla={
                    "max_response_time": 2.0,  # seconds
                    "min_confidence": 0.8,
                    "max_text_length": 5000
                }
            ),
            AgentCapability(
                name="detect_language",
                description="Detect the language of input text",
                input_schema={"text": "string"},
                output_schema={"detected_language": "string", "confidence": "float"},
                performance_sla={"max_response_time": 0.5}
            ),
            AgentCapability(
                name="batch_translate",
                description="Translate multiple texts in parallel",
                input_schema={
                    "texts": "list[string]",
                    "source_language": "string (optional)",
                    "target_language": "string"
                },
                output_schema={
                    "translations": "list[dict]"
                },
                performance_sla={
                    "max_response_time": 10.0,
                    "max_batch_size": 100
                }
            )
        ]
        
        # Model configurations for different language pairs
        self.model_configs = {
            "en-he": "Helsinki-NLP/opus-mt-en-he",
            "he-en": "Helsinki-NLP/opus-mt-he-en",
            "multi": "facebook/m2m100_418M"  # Multilingual fallback
        }
    
    async def initialize(self) -> bool:
        """Initialize translation models"""
        try:
            self.logger.info("Initializing translation models...")
            
            # Load Hebrew-specific models for better performance
            if "he" in self.supported_languages:
                await self._load_model("en-he")
                await self._load_model("he-en")
            
            # Load multilingual model for other languages
            await self._load_model("multi")
            
            self.logger.info("Translation models initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize translation models: {str(e)}")
            self.status = AgentStatus.ERROR
            return False
    
    async def _load_model(self, model_key: str):
        """Load a specific translation model"""
        model_name = self.model_configs[model_key]
        
        if model_key == "multi":
            self.tokenizers[model_key] = M2M100Tokenizer.from_pretrained(model_name)
            self.models[model_key] = M2M100ForConditionalGeneration.from_pretrained(model_name).to(self.device)
        else:
            self.tokenizers[model_key] = MarianTokenizer.from_pretrained(model_name)
            self.models[model_key] = MarianMTModel.from_pretrained(model_name).to(self.device)
    
    async def process(self, message: AgentMessage) -> AgentResponse:
        """Process translation request"""
        start_time = datetime.utcnow()
        
        try:
            action = message.payload.get("action", "translate")
            
            if action == "translate":
                result = await self._translate(
                    message.payload.get("text"),
                    message.payload.get("source_language"),
                    message.payload.get("target_language")
                )
            elif action == "detect_language":
                result = await self._detect_language(message.payload.get("text"))
            elif action == "batch_translate":
                result = await self._batch_translate(
                    message.payload.get("texts"),
                    message.payload.get("source_language"),
                    message.payload.get("target_language")
                )
            else:
                raise ValueError(f"Unknown action: {action}")
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return AgentResponse(
                success=True,
                data=result,
                processing_time=processing_time,
                agent_id=self.agent_id,
                confidence=result.get("confidence", 1.0)
            )
            
        except Exception as e:
            self.logger.error(f"Translation error: {str(e)}")
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return AgentResponse(
                success=False,
                error=str(e),
                processing_time=processing_time,
                agent_id=self.agent_id
            )
    
    async def _translate(self, text: str, source_lang: Optional[str], target_lang: str) -> Dict[str, Any]:
        """Translate text from source to target language"""
        if not source_lang:
            source_lang = await self._detect_language(text)
            source_lang = source_lang["detected_language"]
        
        # Validate languages
        if source_lang not in self.supported_languages:
            raise ValueError(f"Source language '{source_lang}' not supported")
        if target_lang not in self.supported_languages:
            raise ValueError(f"Target language '{target_lang}' not supported")
        
        # Skip if same language
        if source_lang == target_lang:
            return {
                "translated_text": text,
                "source_language": source_lang,
                "target_language": target_lang,
                "confidence": 1.0
            }
        
        # Select appropriate model
        model_key = f"{source_lang}-{target_lang}"
        if model_key not in self.models:
            model_key = "multi"  # Use multilingual model
        
        # Perform translation
        translated_text, confidence = await self._run_translation(text, source_lang, target_lang, model_key)
        
        return {
            "translated_text": translated_text,
            "source_language": source_lang,
            "target_language": target_lang,
            "confidence": confidence
        }
    
    async def _run_translation(self, text: str, source_lang: str, target_lang: str, model_key: str) -> Tuple[str, float]:
        """Run the actual translation using the model"""
        model = self.models[model_key]
        tokenizer = self.tokenizers[model_key]
        
        # For multilingual model, set source and target languages
        if model_key == "multi":
            tokenizer.src_lang = source_lang
            encoded = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            encoded = encoded.to(self.device)
            
            forced_bos_token_id = tokenizer.get_lang_id(target_lang)
            generated_tokens = model.generate(**encoded, forced_bos_token_id=forced_bos_token_id)
        else:
            encoded = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            encoded = encoded.to(self.device)
            generated_tokens = model.generate(**encoded)
        
        translated_text = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
        
        # Calculate confidence based on model outputs
        with torch.no_grad():
            outputs = model(**encoded, labels=generated_tokens)
            confidence = float(torch.exp(-outputs.loss).item())
        
        return translated_text, min(confidence, 1.0)
    
    async def _detect_language(self, text: str) -> Dict[str, Any]:
        """Detect the language of the input text"""
        try:
            detected_lang = detect(text)
            
            # Map common language codes
            lang_map = {
                "iw": "he",  # Hebrew old code to new
                "in": "id",  # Indonesian old code to new
            }
            detected_lang = lang_map.get(detected_lang, detected_lang)
            
            return {
                "detected_language": detected_lang,
                "confidence": 0.95  # langdetect doesn't provide confidence scores
            }
        except Exception as e:
            self.logger.warning(f"Language detection failed: {str(e)}")
            return {
                "detected_language": "en",  # Default to English
                "confidence": 0.5
            }
    
    async def _batch_translate(self, texts: List[str], source_lang: Optional[str], target_lang: str) -> Dict[str, Any]:
        """Translate multiple texts in parallel"""
        tasks = []
        for text in texts:
            tasks.append(self._translate(text, source_lang, target_lang))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        translations = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                translations.append({
                    "index": i,
                    "error": str(result),
                    "original_text": texts[i]
                })
            else:
                translations.append({
                    "index": i,
                    **result
                })
        
        return {"translations": translations}
    
    async def validate_input(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate input data"""
        action = data.get("action", "translate")
        
        if action == "translate":
            if not data.get("text"):
                return False, "Text is required for translation"
            if not data.get("target_language"):
                return False, "Target language is required"
            if len(data["text"]) > 5000:
                return False, "Text exceeds maximum length of 5000 characters"
                
        elif action == "detect_language":
            if not data.get("text"):
                return False, "Text is required for language detection"
                
        elif action == "batch_translate":
            if not data.get("texts") or not isinstance(data["texts"], list):
                return False, "Texts list is required for batch translation"
            if not data.get("target_language"):
                return False, "Target language is required"
            if len(data["texts"]) > 100:
                return False, "Batch size exceeds maximum of 100 texts"
        
        return True, None
    
    def get_capabilities(self) -> List[AgentCapability]:
        """Return agent capabilities"""
        return self._capabilities