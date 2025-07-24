"""
Clinical Language Analysis Agent

Extracted from NLPAnalyzerAgent to provide specialized clinical and psycholinguistic analysis.
Focuses on linguistic markers relevant to psychological assessment and clinical evaluation.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import asyncio
from dataclasses import dataclass

from agent_library.core.base_agent import BaseAgent, AgentMessage, AgentResponse, AgentCapability, AgentStatus


@dataclass
class ClinicalLinguisticFeatures:
    """Structured clinical linguistic features"""
    # Punctuation patterns
    punctuation_density: float
    question_density: float
    exclamation_density: float
    
    # Capitalization and emphasis
    capitalization_ratio: float
    emphasis_patterns: Dict[str, float]
    
    # Word structure analysis
    avg_word_length: float
    word_length_variance: float
    long_word_ratio: float
    
    # Complexity and readability
    complexity_indicator: float
    readability_score: float
    
    # Clinical markers
    emotional_intensity: str
    linguistic_risk_factors: List[str]
    communication_style: str


class ClinicalLanguageAgent(BaseAgent):
    """
    Specialized agent for clinical linguistic analysis and psycholinguistic feature extraction.
    
    Provides clinical-grade analysis of text patterns that may be relevant for:
    - Psychological assessment
    - Communication style analysis
    - Risk factor identification
    - Therapeutic progress monitoring
    """
    
    def __init__(self, agent_id: str = "clinical_language_agent"):
        super().__init__(agent_id, "Clinical Language Analysis Agent", "1.0.0")
        
        # Define capabilities following project standards
        self._capabilities = [
            AgentCapability(
                name="clinical_linguistic_analysis",
                description="Perform clinical-grade linguistic analysis of text patterns",
                input_schema={
                    "text": "string",
                    "context": "dict (optional)",
                    "analysis_type": "string (optional)"
                },
                output_schema={
                    "clinical_features": "dict",
                    "risk_assessment": "dict", 
                    "communication_style": "string",
                    "recommendations": "list",
                    "confidence": "float"
                },
                performance_sla={
                    "max_response_time": 3.0,
                    "min_confidence": 0.60,
                    "max_text_length": 5000
                }
            ),
            AgentCapability(
                name="psycholinguistic_features",
                description="Extract psycholinguistic markers and patterns",
                input_schema={
                    "text": "string",
                    "include_markers": "list (optional)"
                },
                output_schema={
                    "linguistic_features": "dict",
                    "emotional_intensity": "string",
                    "risk_factors": "list"
                },
                performance_sla={"max_response_time": 2.0}
            )
        ]
        
        # Clinical thresholds (based on research literature)
        self.thresholds = {
            "high_punctuation": 0.08,  # >8% punctuation may indicate anxiety
            "high_caps": 0.15,         # >15% caps may indicate emotional intensity
            "high_questions": 0.2,     # >20% questions may indicate uncertainty
            "complex_language": 15.0,  # Complex language patterns
            "fragmented_text": 3.0     # Very short sentences may indicate distress
        }
    
    async def initialize(self) -> bool:
        """Initialize the clinical language analysis agent"""
        try:
            self.logger.info("Initializing Clinical Language Analysis Agent...")
            # Initialize any required clinical models or resources here
            # For now, the agent works with built-in linguistic analysis
            self.logger.info("Clinical Language Agent initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Clinical Language Agent: {str(e)}")
            self.status = AgentStatus.ERROR
            return False
    
    async def validate_input(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate input data against clinical language analysis requirements"""
        # Check for required text input
        if not data.get("text"):
            return False, "Text is required for clinical linguistic analysis"
        
        text = data["text"]
        if not isinstance(text, str):
            return False, "Text must be a string"
        
        # Check minimum text length for meaningful analysis
        if len(text.strip()) < 10:
            return False, "Text must contain at least 10 characters for clinical analysis"
        
        # Check maximum text length
        if len(text) > 5000:
            return False, "Text exceeds maximum length of 5000 characters"
        
        # Check word count for quality analysis
        word_count = len(text.split())
        if word_count < 5:
            return False, "Text must contain at least 5 words for meaningful clinical assessment"
        
        # Validate optional parameters
        analysis_type = data.get("analysis_type")
        if analysis_type and analysis_type not in ["standard", "detailed", "risk_focused"]:
            return False, "Analysis type must be 'standard', 'detailed', or 'risk_focused'"
        
        return True, None
    
    def get_capabilities(self) -> List[AgentCapability]:
        """Return list of clinical language analysis capabilities"""
        return self._capabilities
    
    async def process(self, message: AgentMessage) -> AgentResponse:
        """Process text for clinical linguistic analysis"""
        try:
            text = message.content.get("text", "")
            if not text or len(text.strip()) < 10:
                return AgentResponse(
                    agent_id=self.agent_id,
                    content={"error": "Insufficient text for clinical analysis"},
                    confidence=0.0
                )
            
            # Perform clinical linguistic analysis
            features = await self._extract_clinical_features(text)
            risk_assessment = self._assess_linguistic_risks(features)
            communication_style = self._analyze_communication_style(features)
            
            result = {
                "clinical_features": features.__dict__,
                "risk_assessment": risk_assessment,
                "communication_style": communication_style,
                "recommendations": self._generate_recommendations(features, risk_assessment)
            }
            
            # Calculate confidence based on text length and feature completeness
            confidence = min(0.95, 0.6 + (len(text) / 1000) * 0.3)
            
            return AgentResponse(
                agent_id=self.agent_id,
                content=result,
                confidence=confidence
            )
            
        except Exception as e:
            return AgentResponse(
                agent_id=self.agent_id,
                content={"error": f"Clinical analysis failed: {str(e)}"},
                confidence=0.0
            )
    
    async def _extract_clinical_features(self, text: str) -> ClinicalLinguisticFeatures:
        """Extract clinical-relevant linguistic features"""
        words = text.split()
        sentences = text.split('.')
        
        # Basic linguistic metrics
        punctuation_count = sum(1 for char in text if char in '.,!?;:')
        caps_count = sum(1 for char in text if char.isupper())
        questions = text.count('?')
        exclamations = text.count('!')
        
        # Word analysis
        word_lengths = [len(word.strip('.,!?;:')) for word in words if word.strip()]
        
        # Clinical emphasis patterns
        emphasis_patterns = {
            "repetition": self._detect_repetition(words),
            "intensifiers": self._count_intensifiers(text),
            "absolutism": self._detect_absolutist_language(text),
            "self_reference": self._count_self_references(text)
        }
        
        # Calculate core metrics
        punctuation_density = punctuation_count / len(text) if text else 0
        capitalization_ratio = caps_count / len(text) if text else 0
        question_density = questions / len(words) if words else 0
        exclamation_density = exclamations / len(words) if words else 0
        
        avg_word_length = np.mean(word_lengths) if word_lengths else 0
        word_length_variance = np.var(word_lengths) if word_lengths else 0
        long_word_ratio = sum(1 for length in word_lengths if length > 6) / len(word_lengths) if word_lengths else 0
        
        complexity_indicator = self._calculate_complexity(text, words, sentences)
        readability_score = self._calculate_readability(text, words, sentences)
        
        # Clinical assessment
        emotional_intensity = self._assess_emotional_intensity(
            punctuation_density, capitalization_ratio, exclamation_density
        )
        
        linguistic_risk_factors = self._identify_risk_factors(
            punctuation_density, capitalization_ratio, question_density, 
            complexity_indicator, emphasis_patterns
        )
        
        communication_style = self._determine_communication_style(
            question_density, avg_word_length, complexity_indicator, emphasis_patterns
        )
        
        return ClinicalLinguisticFeatures(
            punctuation_density=punctuation_density,
            question_density=question_density,
            exclamation_density=exclamation_density,
            capitalization_ratio=capitalization_ratio,
            emphasis_patterns=emphasis_patterns,
            avg_word_length=avg_word_length,
            word_length_variance=word_length_variance,
            long_word_ratio=long_word_ratio,
            complexity_indicator=complexity_indicator,
            readability_score=readability_score,
            emotional_intensity=emotional_intensity,
            linguistic_risk_factors=linguistic_risk_factors,
            communication_style=communication_style
        )
    
    def _detect_repetition(self, words: List[str]) -> float:
        """Detect repetitive language patterns"""
        if len(words) < 3:
            return 0.0
        
        word_counts = {}
        for word in words:
            word_lower = word.lower().strip('.,!?;:')
            if len(word_lower) > 2:  # Ignore very short words
                word_counts[word_lower] = word_counts.get(word_lower, 0) + 1
        
        repeated_words = sum(1 for count in word_counts.values() if count > 1)
        return repeated_words / len(word_counts) if word_counts else 0.0
    
    def _count_intensifiers(self, text: str) -> float:
        """Count linguistic intensifiers that may indicate emotional state"""
        intensifiers = [
            'very', 'extremely', 'absolutely', 'completely', 'totally',
            'really', 'quite', 'rather', 'incredibly', 'tremendously',
            'enormously', 'exceptionally', 'remarkably', 'particularly'
        ]
        
        text_lower = text.lower()
        count = sum(text_lower.count(word) for word in intensifiers)
        words = len(text.split())
        
        return count / words if words > 0 else 0.0
    
    def _detect_absolutist_language(self, text: str) -> float:
        """Detect absolutist thinking patterns"""
        absolutist_words = [
            'always', 'never', 'everyone', 'nobody', 'everything', 'nothing',
            'all', 'none', 'every', 'no one', 'everywhere', 'nowhere',
            'forever', 'impossible', 'perfect', 'terrible', 'awful', 'amazing'
        ]
        
        text_lower = text.lower()
        count = sum(text_lower.count(word) for word in absolutist_words)
        words = len(text.split())
        
        return count / words if words > 0 else 0.0
    
    def _count_self_references(self, text: str) -> float:
        """Count self-referential language"""
        self_words = ['i', 'me', 'my', 'myself', 'mine']
        text_lower = text.lower()
        
        count = sum(text_lower.count(' ' + word + ' ') for word in self_words)
        # Also count at beginning of text
        count += sum(1 for word in self_words if text_lower.startswith(word + ' '))
        
        words = len(text.split())
        return count / words if words > 0 else 0.0
    
    def _calculate_complexity(self, text: str, words: List[str], sentences: List[str]) -> float:
        """Calculate linguistic complexity indicator"""
        if not words:
            return 0.0
        
        # Average words per sentence
        avg_sentence_length = len(words) / max(len(sentences), 1)
        
        # Syllable estimation (simplified)
        estimated_syllables = sum(max(1, len([c for c in word if c.lower() in 'aeiou'])) for word in words)
        avg_syllables = estimated_syllables / len(words)
        
        # Combine metrics
        complexity = (avg_sentence_length * 0.6) + (avg_syllables * 0.4)
        return min(complexity, 30.0)  # Cap at reasonable maximum
    
    def _calculate_readability(self, text: str, words: List[str], sentences: List[str]) -> float:
        """Calculate simplified readability score"""
        if not words or not sentences:
            return 0.0
        
        avg_sentence_length = len(words) / max(len(sentences), 1)
        avg_word_length = np.mean([len(word) for word in words])
        
        # Simplified Flesch-like formula
        readability = 206.835 - (1.015 * avg_sentence_length) - (84.6 * (avg_word_length / 4.7))
        return max(0.0, min(100.0, readability))
    
    def _assess_emotional_intensity(self, punct_density: float, caps_ratio: float, excl_density: float) -> str:
        """Assess emotional intensity from linguistic patterns"""
        intensity_score = (punct_density * 2) + (caps_ratio * 3) + (excl_density * 4)
        
        if intensity_score > 0.5:
            return "high"
        elif intensity_score > 0.25:
            return "moderate"
        elif intensity_score > 0.1:
            return "low"
        else:
            return "minimal"
    
    def _identify_risk_factors(self, punct_density: float, caps_ratio: float, 
                             question_density: float, complexity: float, 
                             emphasis_patterns: Dict[str, float]) -> List[str]:
        """Identify potential linguistic risk factors"""
        risk_factors = []
        
        if punct_density > self.thresholds["high_punctuation"]:
            risk_factors.append("excessive_punctuation")
        
        if caps_ratio > self.thresholds["high_caps"]:
            risk_factors.append("excessive_capitalization")
        
        if question_density > self.thresholds["high_questions"]:
            risk_factors.append("high_uncertainty")
        
        if complexity > self.thresholds["complex_language"]:
            risk_factors.append("overly_complex_language")
        elif complexity < self.thresholds["fragmented_text"]:
            risk_factors.append("fragmented_communication")
        
        if emphasis_patterns["repetition"] > 0.3:
            risk_factors.append("repetitive_patterns")
        
        if emphasis_patterns["absolutism"] > 0.1:
            risk_factors.append("absolutist_thinking")
        
        if emphasis_patterns["self_reference"] > 0.25:
            risk_factors.append("excessive_self_focus")
        
        return risk_factors
    
    def _determine_communication_style(self, question_density: float, avg_word_length: float,
                                     complexity: float, emphasis_patterns: Dict[str, float]) -> str:
        """Determine overall communication style"""
        if question_density > 0.15:
            return "questioning"
        elif complexity > 12.0 and avg_word_length > 5.5:
            return "formal"
        elif emphasis_patterns["intensifiers"] > 0.15:
            return "emphatic"
        elif complexity < 8.0 and avg_word_length < 4.5:
            return "simple"
        elif emphasis_patterns["self_reference"] > 0.2:
            return "introspective"
        else:
            return "balanced"
    
    def _assess_linguistic_risks(self, features: ClinicalLinguisticFeatures) -> Dict[str, Any]:
        """Assess overall linguistic risk profile"""
        risk_score = len(features.linguistic_risk_factors) / 8.0  # Normalize to 0-1
        
        risk_level = "low"
        if risk_score > 0.6:
            risk_level = "high"
        elif risk_score > 0.3:
            risk_level = "moderate"
        
        return {
            "overall_risk_level": risk_level,
            "risk_score": risk_score,
            "identified_factors": features.linguistic_risk_factors,
            "emotional_indicators": {
                "intensity": features.emotional_intensity,
                "punctuation_pattern": "elevated" if features.punctuation_density > 0.06 else "normal",
                "capitalization_pattern": "elevated" if features.capitalization_ratio > 0.1 else "normal"
            }
        }
    
    def _analyze_communication_style(self, features: ClinicalLinguisticFeatures) -> Dict[str, Any]:
        """Analyze communication style and patterns"""
        return {
            "primary_style": features.communication_style,
            "complexity_level": "high" if features.complexity_indicator > 12 else "moderate" if features.complexity_indicator > 8 else "low",
            "readability": "easy" if features.readability_score > 70 else "moderate" if features.readability_score > 40 else "difficult",
            "emphasis_patterns": features.emphasis_patterns,
            "linguistic_traits": {
                "uses_questions": features.question_density > 0.1,
                "uses_emphasis": features.exclamation_density > 0.05,
                "formal_language": features.avg_word_length > 5.0,
                "repetitive": features.emphasis_patterns["repetition"] > 0.2
            }
        }
    
    def _generate_recommendations(self, features: ClinicalLinguisticFeatures, 
                                risk_assessment: Dict[str, Any]) -> List[str]:
        """Generate clinical recommendations based on linguistic analysis"""
        recommendations = []
        
        if risk_assessment["overall_risk_level"] == "high":
            recommendations.append("Consider follow-up clinical assessment")
        
        if "excessive_punctuation" in features.linguistic_risk_factors:
            recommendations.append("Monitor for signs of anxiety or emotional dysregulation")
        
        if "high_uncertainty" in features.linguistic_risk_factors:
            recommendations.append("Explore confidence and decision-making patterns")
        
        if "absolutist_thinking" in features.linguistic_risk_factors:
            recommendations.append("Consider cognitive flexibility interventions")
        
        if "fragmented_communication" in features.linguistic_risk_factors:
            recommendations.append("Assess for attention or processing difficulties")
        
        if features.communication_style == "introspective" and features.emphasis_patterns["self_reference"] > 0.3:
            recommendations.append("Monitor for excessive rumination patterns")
        
        if not recommendations:
            recommendations.append("No significant linguistic risk factors identified")
        
        return recommendations


# Helper function for external usage
async def analyze_clinical_language(text: str, agent_id: str = "clinical_language_agent") -> Dict[str, Any]:
    """Convenience function for clinical language analysis"""
    agent = ClinicalLanguageAgent(agent_id)
    message = AgentMessage(
        message_id="clinical_analysis",
        agent_id=agent_id,
        content={"text": text}
    )
    
    response = await agent.process(message)
    return response.content