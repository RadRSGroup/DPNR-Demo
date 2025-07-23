"""
Assessment Router for Clinical vs Soul-Level Insights
Routes assessments to appropriate models and frameworks
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import asyncio
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import logging

from .llm_adapter import LLMOrchestrator, LLMProvider

logger = logging.getLogger(__name__)

class AssessmentCategory(Enum):
    CLINICAL = "clinical"
    SOUL_LEVEL = "soul_level"
    HYBRID = "hybrid"

@dataclass
class AssessmentRoute:
    category: AssessmentCategory
    primary_model: str
    llm_provider: LLMProvider
    confidence_threshold: float
    specialized_tools: List[str]

class ClinicalModelHub:
    """Hub for clinical-grade transformer models"""
    
    def __init__(self):
        self.models = {}
        self.tokenizers = {}
        self._initialize_models()
    
    def _initialize_models(self):
        """Load clinical models lazily"""
        self.model_configs = {
            "mental_health": {
                "model_name": "mental/mental-roberta-base",
                "task": "text-classification"
            },
            "emotion": {
                "model_name": "j-hartmann/emotion-english-distilroberta-base",
                "task": "text-classification"
            },
            "clinical_bert": {
                "model_name": "emilyalsentzer/Bio_ClinicalBERT",
                "task": "feature-extraction"
            },
            "psycholinguistic": {
                "model_name": "bert-base-uncased",  # Will use custom head
                "task": "feature-extraction"
            }
        }
    
    async def get_clinical_insights(self, text: str, model_type: str) -> Dict[str, Any]:
        """Get insights from clinical models"""
        
        if model_type not in self.models:
            await self._load_model(model_type)
        
        model = self.models[model_type]
        
        if model_type == "mental_health":
            return await self._analyze_mental_health(text, model)
        elif model_type == "emotion":
            return await self._analyze_emotions(text, model)
        elif model_type == "clinical_bert":
            return await self._extract_clinical_features(text, model)
        elif model_type == "psycholinguistic":
            return await self._analyze_psycholinguistics(text, model)
    
    async def _load_model(self, model_type: str):
        """Lazy load transformer models"""
        config = self.model_configs[model_type]
        
        loop = asyncio.get_event_loop()
        
        # Load in thread pool to avoid blocking
        def load():
            if config["task"] == "text-classification":
                return pipeline(config["task"], model=config["model_name"])
            else:
                tokenizer = AutoTokenizer.from_pretrained(config["model_name"])
                model = AutoModelForSequenceClassification.from_pretrained(config["model_name"])
                return {"tokenizer": tokenizer, "model": model}
        
        self.models[model_type] = await loop.run_in_executor(None, load)
    
    async def _analyze_mental_health(self, text: str, model) -> Dict[str, Any]:
        """Analyze mental health indicators"""
        loop = asyncio.get_event_loop()
        
        def analyze():
            results = model(text)
            return {
                "risk_indicators": {
                    label["label"]: label["score"] 
                    for label in results[:3]
                },
                "primary_concern": results[0]["label"] if results else None,
                "confidence": results[0]["score"] if results else 0.0
            }
        
        return await loop.run_in_executor(None, analyze)
    
    async def _analyze_emotions(self, text: str, model) -> Dict[str, Any]:
        """Analyze emotional content"""
        loop = asyncio.get_event_loop()
        
        def analyze():
            results = model(text)
            emotions = {r["label"]: r["score"] for r in results}
            
            # Categorize emotions
            positive = ["joy", "love", "optimism", "surprise"]
            negative = ["anger", "fear", "sadness", "disgust"]
            
            pos_score = sum(emotions.get(e, 0) for e in positive)
            neg_score = sum(emotions.get(e, 0) for e in negative)
            
            return {
                "emotions": emotions,
                "valence": "positive" if pos_score > neg_score else "negative",
                "emotional_intensity": max(emotions.values()) if emotions else 0.0,
                "emotional_complexity": len([e for e in emotions.values() if e > 0.1])
            }
        
        return await loop.run_in_executor(None, analyze)
    
    async def _extract_clinical_features(self, text: str, model_dict) -> Dict[str, Any]:
        """Extract clinical features using BioClinicalBERT"""
        loop = asyncio.get_event_loop()
        
        def extract():
            tokenizer = model_dict["tokenizer"]
            model = model_dict["model"]
            
            inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            
            with torch.no_grad():
                outputs = model(**inputs)
                embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
            
            # Extract key features from embeddings
            feature_vector = embeddings[0]
            
            return {
                "clinical_embedding": feature_vector.tolist()[:10],  # First 10 dims for demo
                "text_complexity": len(text.split()) / len(text.split(".")),
                "clinical_relevance_score": float(np.mean(np.abs(feature_vector)))
            }
        
        return await loop.run_in_executor(None, extract)
    
    async def _analyze_psycholinguistics(self, text: str, model_dict) -> Dict[str, Any]:
        """Analyze psycholinguistic features"""
        
        # LIWC-style categories
        word_categories = {
            "cognitive_process": ["think", "know", "consider", "understand", "realize"],
            "perceptual": ["see", "hear", "feel", "sense", "notice"],
            "biological": ["eat", "sleep", "pain", "health", "sick"],
            "drives": ["achieve", "power", "risk", "focus", "want"],
            "time_focus": {
                "past": ["was", "were", "had", "did", "used to"],
                "present": ["is", "are", "am", "now", "today"],
                "future": ["will", "going to", "plan", "hope", "tomorrow"]
            },
            "personal_concerns": ["work", "leisure", "home", "money", "religion"],
            "informal_speech": ["like", "you know", "I mean", "uh", "um"]
        }
        
        text_lower = text.lower()
        words = text_lower.split()
        word_count = len(words)
        
        features = {}
        
        # Calculate category percentages
        for category, keywords in word_categories.items():
            if category == "time_focus":
                time_scores = {}
                for tense, tense_words in keywords.items():
                    count = sum(1 for w in words if w in tense_words)
                    time_scores[tense] = count / word_count if word_count > 0 else 0
                features[category] = time_scores
            else:
                count = sum(1 for w in words if w in keywords)
                features[f"{category}_ratio"] = count / word_count if word_count > 0 else 0
        
        # Additional linguistic features
        features.update({
            "word_count": word_count,
            "avg_word_length": np.mean([len(w) for w in words]) if words else 0,
            "sentence_count": len(text.split(".")),
            "question_ratio": text.count("?") / len(text.split(".")) if text.split(".") else 0,
            "exclamation_ratio": text.count("!") / len(text.split(".")) if text.split(".") else 0,
            "first_person_usage": sum(1 for w in words if w in ["i", "me", "my", "myself"]) / word_count if word_count > 0 else 0
        })
        
        return features

class AssessmentRouter:
    """
    Routes assessments to appropriate models and frameworks
    based on assessment type and requirements
    """
    
    def __init__(self, llm_orchestrator: LLMOrchestrator):
        self.llm_orchestrator = llm_orchestrator
        self.clinical_hub = ClinicalModelHub()
        self.routes = self._initialize_routes()
    
    def _initialize_routes(self) -> Dict[str, AssessmentRoute]:
        """Define routing rules for different assessment types"""
        
        return {
            # Clinical assessments using transformer models
            "big_five": AssessmentRoute(
                category=AssessmentCategory.CLINICAL,
                primary_model="clinical_bert",
                llm_provider=LLMProvider.OPENAI,
                confidence_threshold=0.85,
                specialized_tools=["psycholinguistic", "emotion"]
            ),
            "emotional_intelligence": AssessmentRoute(
                category=AssessmentCategory.CLINICAL,
                primary_model="emotion",
                llm_provider=LLMProvider.OPENAI,
                confidence_threshold=0.80,
                specialized_tools=["mental_health"]
            ),
            "cognitive_style": AssessmentRoute(
                category=AssessmentCategory.CLINICAL,
                primary_model="psycholinguistic",
                llm_provider=LLMProvider.OPENAI,
                confidence_threshold=0.75,
                specialized_tools=["clinical_bert"]
            ),
            
            # Soul-level assessments using LLMs
            "sefirot": AssessmentRoute(
                category=AssessmentCategory.SOUL_LEVEL,
                primary_model="llm_only",
                llm_provider=LLMProvider.ANTHROPIC,
                confidence_threshold=0.70,
                specialized_tools=[]
            ),
            "shadow_work": AssessmentRoute(
                category=AssessmentCategory.SOUL_LEVEL,
                primary_model="llm_only",
                llm_provider=LLMProvider.ANTHROPIC,
                confidence_threshold=0.70,
                specialized_tools=[]
            ),
            "ifs": AssessmentRoute(
                category=AssessmentCategory.SOUL_LEVEL,
                primary_model="llm_only",
                llm_provider=LLMProvider.ANTHROPIC,
                confidence_threshold=0.75,
                specialized_tools=[]
            ),
            "pardes": AssessmentRoute(
                category=AssessmentCategory.SOUL_LEVEL,
                primary_model="llm_only",
                llm_provider=LLMProvider.ANTHROPIC,
                confidence_threshold=0.70,
                specialized_tools=[]
            ),
            
            # Hybrid assessments using both
            "enneagram": AssessmentRoute(
                category=AssessmentCategory.HYBRID,
                primary_model="psycholinguistic",
                llm_provider=LLMProvider.GEMINI,
                confidence_threshold=0.80,
                specialized_tools=["emotion"]
            ),
            "values": AssessmentRoute(
                category=AssessmentCategory.HYBRID,
                primary_model="psycholinguistic",
                llm_provider=LLMProvider.GEMINI,
                confidence_threshold=0.75,
                specialized_tools=[]
            )
        }
    
    async def route_assessment(
        self,
        text: str,
        assessment_type: str,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Route assessment to appropriate models based on type
        
        Returns:
            Dict containing insights from specialized models and LLM
        """
        
        if assessment_type not in self.routes:
            # Default routing
            route = AssessmentRoute(
                category=AssessmentCategory.HYBRID,
                primary_model="psycholinguistic",
                llm_provider=LLMProvider.OPENAI,
                confidence_threshold=0.75,
                specialized_tools=[]
            )
        else:
            route = self.routes[assessment_type]
        
        results = {
            "assessment_type": assessment_type,
            "category": route.category.value,
            "insights": {}
        }
        
        # Process based on category
        if route.category == AssessmentCategory.CLINICAL:
            # Use clinical models first
            clinical_insights = await self._process_clinical(text, route)
            results["insights"]["clinical"] = clinical_insights
            
            # Enhance with LLM
            llm_insights = await self._enhance_with_llm(
                text, assessment_type, clinical_insights, route
            )
            results["insights"]["llm_enhancement"] = llm_insights
            
        elif route.category == AssessmentCategory.SOUL_LEVEL:
            # Use LLM primarily
            llm_insights = await self._process_soul_level(
                text, assessment_type, route
            )
            results["insights"]["soul_analysis"] = llm_insights
            
        else:  # HYBRID
            # Use both clinical and LLM
            clinical_task = self._process_clinical(text, route)
            llm_task = self._process_soul_level(text, assessment_type, route)
            
            clinical_insights, llm_insights = await asyncio.gather(
                clinical_task, llm_task
            )
            
            results["insights"]["clinical"] = clinical_insights
            results["insights"]["soul_analysis"] = llm_insights
            results["insights"]["integrated"] = self._integrate_insights(
                clinical_insights, llm_insights
            )
        
        # Calculate overall confidence
        results["confidence"] = self._calculate_confidence(results["insights"])
        
        return results
    
    async def _process_clinical(
        self,
        text: str,
        route: AssessmentRoute
    ) -> Dict[str, Any]:
        """Process using clinical transformer models"""
        
        insights = {}
        
        # Primary model analysis
        if route.primary_model != "llm_only":
            primary_insights = await self.clinical_hub.get_clinical_insights(
                text, route.primary_model
            )
            insights["primary_analysis"] = primary_insights
        
        # Additional specialized tools
        for tool in route.specialized_tools:
            tool_insights = await self.clinical_hub.get_clinical_insights(
                text, tool
            )
            insights[f"{tool}_analysis"] = tool_insights
        
        return insights
    
    async def _process_soul_level(
        self,
        text: str,
        assessment_type: str,
        route: AssessmentRoute
    ) -> Dict[str, Any]:
        """Process using LLM for soul-level insights"""
        
        # Craft specialized prompt based on assessment type
        prompts = {
            "sefirot": self._create_sefirot_prompt(text),
            "shadow_work": self._create_shadow_work_prompt(text),
            "ifs": self._create_ifs_prompt(text),
            "pardes": self._create_pardes_prompt(text)
        }
        
        prompt = prompts.get(assessment_type, self._create_generic_prompt(text))
        
        response = await self.llm_orchestrator.generate_with_fallback(
            prompt=prompt["user"],
            system_prompt=prompt["system"],
            preferred_provider=route.llm_provider,
            assessment_type=assessment_type
        )
        
        return {
            "analysis": response.content,
            "model_used": response.model,
            "provider": response.provider.value,
            "latency_ms": response.latency_ms
        }
    
    async def _enhance_with_llm(
        self,
        text: str,
        assessment_type: str,
        clinical_insights: Dict[str, Any],
        route: AssessmentRoute
    ) -> Dict[str, Any]:
        """Enhance clinical insights with LLM interpretation"""
        
        prompt = f"""
        Based on the following clinical analysis insights, provide a comprehensive 
        {assessment_type} assessment:
        
        Clinical Insights:
        {clinical_insights}
        
        Original Text:
        {text}
        
        Please integrate these clinical findings into a coherent personality assessment.
        """
        
        response = await self.llm_orchestrator.generate_with_fallback(
            prompt=prompt,
            system_prompt=f"You are an expert in {assessment_type} assessment.",
            preferred_provider=route.llm_provider,
            assessment_type=assessment_type
        )
        
        return {
            "enhanced_analysis": response.content,
            "model_used": response.model
        }
    
    def _integrate_insights(
        self,
        clinical: Dict[str, Any],
        soul_level: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Integrate clinical and soul-level insights"""
        
        return {
            "synthesis": "Integrated analysis combining clinical and soul-level insights",
            "clinical_summary": clinical.get("primary_analysis", {}),
            "soul_summary": soul_level.get("analysis", "")[:200] + "...",
            "convergent_themes": self._find_convergent_themes(clinical, soul_level)
        }
    
    def _find_convergent_themes(
        self,
        clinical: Dict[str, Any],
        soul_level: Dict[str, Any]
    ) -> List[str]:
        """Find themes that appear in both clinical and soul-level analysis"""
        
        themes = []
        
        # Extract emotions from clinical
        clinical_emotions = clinical.get("emotion_analysis", {}).get("emotions", {})
        
        # Simple keyword matching for demo
        if "sadness" in clinical_emotions and clinical_emotions["sadness"] > 0.5:
            if "shadow" in str(soul_level).lower():
                themes.append("Unprocessed grief or loss requiring shadow work")
        
        return themes
    
    def _calculate_confidence(self, insights: Dict[str, Any]) -> float:
        """Calculate overall confidence score"""
        
        confidence_scores = []
        
        # Extract confidence from various sources
        for key, value in insights.items():
            if isinstance(value, dict):
                if "confidence" in value:
                    confidence_scores.append(value["confidence"])
                elif "primary_analysis" in value:
                    if "confidence" in value["primary_analysis"]:
                        confidence_scores.append(value["primary_analysis"]["confidence"])
        
        return np.mean(confidence_scores) if confidence_scores else 0.5
    
    # Prompt creation methods
    def _create_sefirot_prompt(self, text: str) -> Dict[str, str]:
        return {
            "system": """You are an expert in Kabbalistic psychology and the Tree of Life (Sefirot) framework. 
            Analyze the text through the lens of the 10 Sefirot and identify which energies are most present.""",
            "user": f"""Analyze this text through the Sefirot framework:
            
            {text}
            
            Identify:
            1. Primary Sefirot energies present
            2. Balance between giving (Chesed) and restraint (Gevurah)
            3. Integration level (Tiferet)
            4. Manifestation patterns (Malchut)
            5. Soul level insights"""
        }
    
    def _create_shadow_work_prompt(self, text: str) -> Dict[str, str]:
        return {
            "system": """You are a Jungian analyst specializing in shadow work and unconscious patterns.""",
            "user": f"""Perform a shadow work analysis on this text:
            
            {text}
            
            Identify:
            1. Potential shadow aspects or projections
            2. Repressed or denied qualities
            3. Integration opportunities
            4. Unconscious patterns
            5. Recommendations for shadow work"""
        }
    
    def _create_ifs_prompt(self, text: str) -> Dict[str, str]:
        return {
            "system": """You are an Internal Family Systems (IFS) therapist identifying parts and their roles.""",
            "user": f"""Analyze this text using the IFS framework:
            
            {text}
            
            Identify:
            1. Manager parts and their protective strategies
            2. Firefighter parts and their coping mechanisms
            3. Potential exiled parts and their burdens
            4. Self-leadership qualities present
            5. Parts that need attention or unburdening"""
        }
    
    def _create_pardes_prompt(self, text: str) -> Dict[str, str]:
        return {
            "system": """You are an expert in PaRDeS four-level interpretation system.""",
            "user": f"""Apply the PaRDeS framework to analyze this text:
            
            {text}
            
            Provide insights at each level:
            1. Pshat (Simple/Literal) - Surface meaning
            2. Remez (Hint/Allegory) - Symbolic patterns  
            3. Drash (Interpret/Seek) - Personal meaning
            4. Sod (Secret/Mystical) - Hidden soul truth"""
        }
    
    def _create_generic_prompt(self, text: str) -> Dict[str, str]:
        return {
            "system": "You are an expert psychological assessor.",
            "user": f"Analyze this text and provide psychological insights: {text}"
        }