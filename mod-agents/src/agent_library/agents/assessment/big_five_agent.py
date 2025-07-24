"""
Big Five Personality Assessment Agent

Extracted from EnhancedBigFiveProcessor to provide clinical-grade Big Five personality assessment.
Implements the Five-Factor Model with 6 facets per trait and clinical linguistic integration.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import asyncio
from dataclasses import dataclass

from ...core.base_agent import BaseAgent, AgentMessage, AgentResponse, AgentCapability, AgentStatus


@dataclass
class BigFiveTrait:
    """Represents a Big Five personality trait with facets and scores"""
    name: str
    score: float
    percentile: int
    facet_scores: Dict[str, float]
    evidence: List[str]
    clinical_correlates: Dict[str, List[str]]
    interpretation: str


@dataclass
class BigFiveProfile:
    """Complete Big Five personality profile"""
    openness: BigFiveTrait
    conscientiousness: BigFiveTrait
    extraversion: BigFiveTrait
    agreeableness: BigFiveTrait
    neuroticism: BigFiveTrait
    overall_confidence: float
    clinical_insights: Dict[str, Any]
    recommendations: List[str]


class BigFiveAgent(BaseAgent):
    """
    Clinical-grade Big Five personality assessment agent.
    
    Implements the Five-Factor Model (FFM) with:
    - 6 facets per trait for comprehensive assessment
    - Clinical linguistic marker integration
    - Evidence-based scoring and interpretation
    - Therapeutic and vocational insights
    """
    
    def __init__(self, agent_id: str = "big_five_agent"):
        super().__init__(agent_id, "Big Five Personality Assessment Agent", "1.0.0")
        
        # Define capabilities following project standards
        self._capabilities = [
            AgentCapability(
                name="big_five_assessment",
                description="Comprehensive Big Five personality assessment with facet analysis",
                input_schema={
                    "text": "string",
                    "context": "dict (optional)",
                    "analysis_depth": "string (optional)"
                },
                output_schema={
                    "big_five_profile": "dict",
                    "summary": "string",
                    "clinical_insights": "dict",
                    "recommendations": "list",
                    "confidence": "float"
                },
                performance_sla={
                    "max_response_time": 5.0,
                    "min_confidence": 0.70,
                    "min_text_length": 50
                }
            ),
            AgentCapability(
                name="personality_profiling",
                description="Generate detailed personality profiles with clinical correlates",
                input_schema={"text": "string"},
                output_schema={"profile": "dict", "insights": "dict"},
                performance_sla={"max_response_time": 3.0}
            ),
            AgentCapability(
                name="facet_analysis",
                description="Detailed analysis of Big Five facets and sub-traits",
                input_schema={"text": "string", "trait_focus": "string (optional)"},
                output_schema={"facet_scores": "dict", "evidence": "list"}
            )
        ]
        
        # Comprehensive trait profiles with facets and clinical markers
        self.trait_profiles = {
            "openness": {
                "name": "Openness to Experience",
                "facets": {
                    "imagination": ["imagine", "fantasy", "dream", "creative", "visualize"],
                    "artistic_interests": ["art", "music", "poetry", "beauty", "aesthetic"],
                    "emotionality": ["feel", "emotion", "moved", "touched", "sensitive"],
                    "adventurousness": ["try", "new", "adventure", "explore", "experiment"],
                    "intellect": ["think", "analyze", "understand", "complex", "abstract"],
                    "liberalism": ["challenge", "tradition", "change", "progressive", "question"]
                },
                "high_indicators": {
                    "keywords": ["creative", "curious", "imaginative", "artistic", "unconventional"],
                    "linguistic_markers": ["what if", "imagine", "suppose", "wonder", "possibility"],
                    "complexity_threshold": 0.7
                },
                "low_indicators": {
                    "keywords": ["practical", "traditional", "routine", "conventional", "realistic"],
                    "linguistic_markers": ["always done", "proven", "standard", "normal", "usual"],
                    "complexity_threshold": 0.3
                },
                "clinical_correlates": {
                    "positive": ["creativity", "cognitive flexibility", "aesthetic sensitivity"],
                    "negative": ["fantasy proneness", "impracticality", "emotional overwhelm"]
                }
            },
            "conscientiousness": {
                "name": "Conscientiousness",
                "facets": {
                    "self_efficacy": ["capable", "competent", "handle", "manage", "accomplish"],
                    "orderliness": ["organize", "plan", "schedule", "systematic", "neat"],
                    "dutifulness": ["duty", "obligation", "responsible", "reliable", "promise"],
                    "achievement_striving": ["goal", "achieve", "succeed", "strive", "excel"],
                    "self_discipline": ["discipline", "persist", "finish", "complete", "follow through"],
                    "cautiousness": ["careful", "think before", "consider", "deliberate", "cautious"]
                },
                "high_indicators": {
                    "keywords": ["organized", "disciplined", "responsible", "thorough", "reliable"],
                    "linguistic_markers": ["plan to", "schedule", "must", "should", "deadline"],
                    "future_focus_ratio": 0.08
                },
                "low_indicators": {
                    "keywords": ["spontaneous", "flexible", "relaxed", "casual", "impulsive"],
                    "linguistic_markers": ["whatever", "go with flow", "see what happens", "wing it"],
                    "future_focus_ratio": 0.02
                },
                "clinical_correlates": {
                    "positive": ["achievement", "reliability", "health behaviors"],
                    "negative": ["perfectionism", "rigidity", "workaholism"]
                }
            },
            "extraversion": {
                "name": "Extraversion",
                "facets": {
                    "warmth": ["warm", "friendly", "close", "affectionate", "caring"],
                    "gregariousness": ["people", "social", "group", "party", "gathering"],
                    "assertiveness": ["assert", "speak up", "confident", "direct", "leadership"],
                    "activity": ["active", "energy", "busy", "fast", "vigorous"],
                    "excitement_seeking": ["excitement", "thrill", "adventure", "risk", "stimulation"],
                    "positive_emotions": ["happy", "joy", "cheerful", "optimistic", "enthusiastic"]
                },
                "high_indicators": {
                    "keywords": ["outgoing", "social", "energetic", "talkative", "assertive"],
                    "linguistic_markers": ["we", "together", "exciting", "fun", "everyone"],
                    "social_words_ratio": 0.08
                },
                "low_indicators": {
                    "keywords": ["quiet", "reserved", "solitary", "independent", "thoughtful"],
                    "linguistic_markers": ["alone", "quiet", "prefer", "myself", "peaceful"],
                    "social_words_ratio": 0.02
                },
                "clinical_correlates": {
                    "positive": ["social support", "leadership", "positive affect"],
                    "negative": ["attention seeking", "impulsivity", "burnout risk"]
                }
            },
            "agreeableness": {
                "name": "Agreeableness",
                "facets": {
                    "trust": ["trust", "believe", "faith", "honest", "sincere"],
                    "morality": ["fair", "cheat", "honest", "ethical", "principled"],
                    "altruism": ["help", "assist", "support", "care", "generous"],
                    "cooperation": ["cooperate", "work together", "compromise", "agree", "harmony"],
                    "modesty": ["humble", "modest", "simple", "unpretentious", "down to earth"],
                    "sympathy": ["concern", "sympathy", "compassion", "feel for", "empathy"]
                },
                "high_indicators": {
                    "keywords": ["kind", "cooperative", "trusting", "helpful", "compassionate"],
                    "linguistic_markers": ["understand", "appreciate", "together", "share", "support"],
                    "other_focus_ratio": 0.06
                },
                "low_indicators": {
                    "keywords": ["competitive", "skeptical", "critical", "demanding", "tough"],
                    "linguistic_markers": ["don't trust", "compete", "win", "skeptical", "prove it"],
                    "other_focus_ratio": 0.02
                },
                "clinical_correlates": {
                    "positive": ["relationship quality", "teamwork", "social harmony"],
                    "negative": ["exploitation vulnerability", "conflict avoidance", "dependency"]
                }
            },
            "neuroticism": {
                "name": "Neuroticism (Emotional Stability)",
                "facets": {
                    "anxiety": ["anxious", "worried", "nervous", "tense", "stressed"],
                    "anger": ["angry", "irritated", "frustrated", "annoyed", "mad"],
                    "depression": ["sad", "depressed", "down", "hopeless", "empty"],
                    "self_consciousness": ["embarrassed", "shy", "awkward", "self-conscious", "uncomfortable"],
                    "immoderation": ["resist", "control", "temptation", "indulge", "excess"],
                    "vulnerability": ["panic", "helpless", "overwhelmed", "break down", "fall apart"]
                },
                "high_indicators": {
                    "keywords": ["anxious", "worried", "stressed", "emotional", "sensitive"],
                    "linguistic_markers": ["can't handle", "too much", "overwhelmed", "worried about", "stressed"],
                    "negative_emotion_ratio": 0.15
                },
                "low_indicators": {
                    "keywords": ["calm", "relaxed", "stable", "composed", "unflappable"],
                    "linguistic_markers": ["no worries", "calm", "handle it", "stable", "fine"],
                    "negative_emotion_ratio": 0.03
                },
                "clinical_correlates": {
                    "positive": ["emotional sensitivity", "empathy", "self-awareness"],
                    "negative": ["anxiety disorders", "depression", "stress vulnerability"]
                }
            }
        }
    
    async def initialize(self) -> bool:
        """Initialize the Big Five personality assessment agent"""
        try:
            self.logger.info("Initializing Big Five Personality Assessment Agent...")
            # Initialize any required models or resources here
            # For now, the agent works with built-in assessment algorithms
            self.logger.info("Big Five Agent initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Big Five Agent: {str(e)}")
            self.status = AgentStatus.ERROR
            return False
    
    async def validate_input(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate input data against Big Five assessment requirements"""
        # Check for required text input
        if not data.get("text"):
            return False, "Text is required for Big Five personality assessment"
        
        text = data["text"]
        if not isinstance(text, str):
            return False, "Text must be a string"
        
        # Check minimum text length for meaningful assessment
        if len(text.strip()) < 50:
            return False, "Text must contain at least 50 characters for Big Five assessment"
        
        # Check maximum text length
        if len(text) > 10000:
            return False, "Text exceeds maximum length of 10000 characters"
        
        # Check word count for quality analysis
        word_count = len(text.split())
        if word_count < 10:
            return False, "Text must contain at least 10 words for meaningful personality assessment"
        
        # Validate optional parameters
        analysis_depth = data.get("analysis_depth")
        if analysis_depth and analysis_depth not in ["standard", "detailed", "clinical"]:
            return False, "Analysis depth must be 'standard', 'detailed', or 'clinical'"
        
        return True, None
    
    def get_capabilities(self) -> List[AgentCapability]:
        """Return list of Big Five assessment capabilities"""
        return self._capabilities
    
    async def process(self, message: AgentMessage) -> AgentResponse:
        """Process text for Big Five personality assessment"""
        try:
            text = message.content.get("text", "")
            if not text or len(text.strip()) < 50:
                return AgentResponse(
                    agent_id=self.agent_id,
                    content={"error": "Insufficient text for Big Five assessment (minimum 50 characters)"},
                    confidence=0.0
                )
            
            # Perform Big Five assessment
            profile = await self._assess_big_five(text)
            
            result = {
                "big_five_profile": self._serialize_profile(profile),
                "summary": self._generate_summary(profile),
                "clinical_insights": profile.clinical_insights,
                "recommendations": profile.recommendations
            }
            
            return AgentResponse(
                agent_id=self.agent_id,
                content=result,
                confidence=profile.overall_confidence
            )
            
        except Exception as e:
            return AgentResponse(
                agent_id=self.agent_id,
                content={"error": f"Big Five assessment failed: {str(e)}"},
                confidence=0.0
            )
    
    async def _assess_big_five(self, text: str) -> BigFiveProfile:
        """Perform comprehensive Big Five assessment"""
        text_lower = text.lower()
        words = text.split()
        
        # Extract linguistic features for assessment
        linguistic_features = await self._extract_linguistic_features(text, words)
        
        # Assess each trait
        traits = {}
        for trait_name, trait_data in self.trait_profiles.items():
            trait_assessment = await self._assess_trait(
                trait_name, trait_data, text_lower, words, linguistic_features
            )
            traits[trait_name] = trait_assessment
        
        # Generate clinical insights and recommendations
        clinical_insights = self._generate_clinical_insights(traits, linguistic_features)
        recommendations = self._generate_recommendations(traits, clinical_insights)
        
        # Calculate overall confidence
        trait_confidences = [trait.score for trait in traits.values()]
        overall_confidence = np.mean(trait_confidences) if trait_confidences else 0.0
        
        return BigFiveProfile(
            openness=traits["openness"],
            conscientiousness=traits["conscientiousness"],
            extraversion=traits["extraversion"],
            agreeableness=traits["agreeableness"],
            neuroticism=traits["neuroticism"],
            overall_confidence=min(0.95, overall_confidence),
            clinical_insights=clinical_insights,
            recommendations=recommendations
        )
    
    async def _extract_linguistic_features(self, text: str, words: List[str]) -> Dict[str, float]:
        """Extract linguistic features relevant to Big Five assessment"""
        text_lower = text.lower()
        
        # Social words ratio
        social_words = ["we", "us", "our", "together", "team", "group", "people", "everyone", "relationship"]
        social_count = sum(text_lower.count(word) for word in social_words)
        social_words_ratio = social_count / len(words) if words else 0
        
        # Future-focused language
        future_words = ["will", "plan", "goal", "future", "tomorrow", "next", "schedule", "intend"]
        future_count = sum(text_lower.count(word) for word in future_words)
        future_focus_ratio = future_count / len(words) if words else 0
        
        # Other-focused language
        other_words = ["you", "your", "they", "them", "their", "others", "someone", "people"]
        other_count = sum(text_lower.count(word) for word in other_words)
        other_focus_ratio = other_count / len(words) if words else 0
        
        # Negative emotion words
        negative_words = ["sad", "angry", "worried", "anxious", "stressed", "frustrated", "disappointed", "upset"]
        negative_count = sum(text_lower.count(word) for word in negative_words)
        negative_emotion_ratio = negative_count / len(words) if words else 0
        
        # Text complexity (simplified)
        avg_word_length = np.mean([len(word) for word in words]) if words else 0
        sentences = text.split('.')
        avg_sentence_length = len(words) / max(len(sentences), 1)
        complexity = (avg_word_length * 0.4) + (avg_sentence_length * 0.6) / 10
        
        return {
            "social_words_ratio": social_words_ratio,
            "future_focus_ratio": future_focus_ratio,
            "other_focus_ratio": other_focus_ratio,
            "negative_emotion_ratio": negative_emotion_ratio,
            "complexity": min(1.0, complexity)
        }
    
    async def _assess_trait(self, trait_name: str, trait_data: Dict[str, Any], 
                          text_lower: str, words: List[str], 
                          linguistic_features: Dict[str, float]) -> BigFiveTrait:
        """Assess a single Big Five trait with facet analysis"""
        
        # Assess facets
        facet_scores = {}
        evidence = []
        
        for facet_name, facet_keywords in trait_data["facets"].items():
            facet_score = 0.0
            facet_evidence = []
            
            # Count keyword matches
            for keyword in facet_keywords:
                if keyword in text_lower:
                    facet_score += 0.2
                    facet_evidence.append(f"Uses '{keyword}' (facet: {facet_name})")
            
            facet_scores[facet_name] = min(1.0, facet_score)
            evidence.extend(facet_evidence[:2])  # Limit evidence per facet
        
        # High indicators scoring
        high_score = 0.0
        for keyword in trait_data["high_indicators"]["keywords"]:
            if keyword in text_lower:
                high_score += 0.15
                evidence.append(f"High {trait_name}: uses '{keyword}'")
        
        for marker in trait_data["high_indicators"]["linguistic_markers"]:
            if marker in text_lower:
                high_score += 0.1
                evidence.append(f"High {trait_name}: linguistic pattern '{marker}'")
        
        # Low indicators scoring (inverse)
        low_score = 0.0
        for keyword in trait_data["low_indicators"]["keywords"]:
            if keyword in text_lower:
                low_score += 0.15
                evidence.append(f"Low {trait_name}: uses '{keyword}'")
        
        for marker in trait_data["low_indicators"]["linguistic_markers"]:
            if marker in text_lower:
                low_score += 0.1
                evidence.append(f"Low {trait_name}: linguistic pattern '{marker}'")
        
        # Linguistic feature adjustments
        linguistic_adjustment = self._apply_linguistic_adjustments(
            trait_name, trait_data, linguistic_features
        )
        
        # Calculate final score
        facet_average = np.mean(list(facet_scores.values())) if facet_scores else 0.0
        raw_score = facet_average * 0.5 + high_score * 0.3 - low_score * 0.2 + linguistic_adjustment
        
        # Normalize to 0-1 range
        final_score = max(0.0, min(1.0, raw_score))
        
        # Convert to percentile (simplified)
        percentile = int(final_score * 100)
        
        # Generate interpretation
        interpretation = self._interpret_trait_score(trait_name, final_score, facet_scores)
        
        return BigFiveTrait(
            name=trait_data["name"],
            score=final_score,
            percentile=percentile,
            facet_scores=facet_scores,
            evidence=evidence[:5],  # Limit evidence
            clinical_correlates=trait_data["clinical_correlates"],
            interpretation=interpretation
        )
    
    def _apply_linguistic_adjustments(self, trait_name: str, trait_data: Dict[str, Any], 
                                    features: Dict[str, float]) -> float:
        """Apply linguistic feature adjustments to trait scores"""
        adjustment = 0.0
        
        if trait_name == "openness":
            # High complexity indicates openness
            if features["complexity"] > trait_data["high_indicators"].get("complexity_threshold", 0.7):
                adjustment += 0.1
            elif features["complexity"] < trait_data["low_indicators"].get("complexity_threshold", 0.3):
                adjustment -= 0.1
        
        elif trait_name == "conscientiousness":
            # Future focus indicates conscientiousness
            threshold = trait_data["high_indicators"].get("future_focus_ratio", 0.08)
            if features["future_focus_ratio"] > threshold:
                adjustment += 0.15
            elif features["future_focus_ratio"] < trait_data["low_indicators"].get("future_focus_ratio", 0.02):
                adjustment -= 0.1
        
        elif trait_name == "extraversion":
            # Social language indicates extraversion
            threshold = trait_data["high_indicators"].get("social_words_ratio", 0.08)
            if features["social_words_ratio"] > threshold:
                adjustment += 0.2
            elif features["social_words_ratio"] < trait_data["low_indicators"].get("social_words_ratio", 0.02):
                adjustment -= 0.15
        
        elif trait_name == "agreeableness":
            # Other-focus indicates agreeableness
            threshold = trait_data["high_indicators"].get("other_focus_ratio", 0.06)
            if features["other_focus_ratio"] > threshold:
                adjustment += 0.1
            elif features["other_focus_ratio"] < trait_data["low_indicators"].get("other_focus_ratio", 0.02):
                adjustment -= 0.1
        
        elif trait_name == "neuroticism":
            # Negative emotion language indicates neuroticism
            threshold = trait_data["high_indicators"].get("negative_emotion_ratio", 0.15)
            if features["negative_emotion_ratio"] > threshold:
                adjustment += 0.2
            elif features["negative_emotion_ratio"] < trait_data["low_indicators"].get("negative_emotion_ratio", 0.03):
                adjustment -= 0.15
        
        return adjustment
    
    def _interpret_trait_score(self, trait_name: str, score: float, facet_scores: Dict[str, float]) -> str:
        """Generate interpretation for trait score"""
        if score >= 0.7:
            level = "High"
        elif score >= 0.4:
            level = "Moderate"
        else:
            level = "Low"
        
        # Find dominant facets
        sorted_facets = sorted(facet_scores.items(), key=lambda x: x[1], reverse=True)
        top_facets = [facet for facet, score in sorted_facets[:2] if score > 0.3]
        
        facet_text = ""
        if top_facets:
            facet_text = f" Particularly evident in {' and '.join(top_facets)}."
        
        return f"{level} {trait_name}.{facet_text}"
    
    def _generate_clinical_insights(self, traits: Dict[str, BigFiveTrait], 
                                  features: Dict[str, float]) -> Dict[str, Any]:
        """Generate clinical insights from Big Five profile"""
        insights = {
            "overall_pattern": "",
            "strengths": [],
            "potential_challenges": [],
            "interpersonal_style": "",
            "stress_vulnerability": "",
            "growth_areas": []
        }
        
        # Analyze overall pattern
        high_traits = [name for name, trait in traits.items() if trait.score >= 0.7]
        low_traits = [name for name, trait in traits.items() if trait.score <= 0.3]
        
        if len(high_traits) >= 3:
            insights["overall_pattern"] = "Multi-faceted personality with several prominent traits"
        elif len(high_traits) == 0:
            insights["overall_pattern"] = "Balanced personality profile with moderate trait expression"
        else:
            insights["overall_pattern"] = f"Personality primarily characterized by {', '.join(high_traits)}"
        
        # Identify strengths
        if traits["conscientiousness"].score >= 0.6:
            insights["strengths"].append("Strong self-discipline and reliability")
        if traits["agreeableness"].score >= 0.6:
            insights["strengths"].append("Cooperative and empathetic interpersonal style")
        if traits["openness"].score >= 0.6:
            insights["strengths"].append("Creative and intellectually curious")
        if traits["extraversion"].score >= 0.6:
            insights["strengths"].append("Socially confident and energetic")
        if traits["neuroticism"].score <= 0.4:
            insights["strengths"].append("Emotionally stable and resilient")
        
        # Identify challenges
        if traits["neuroticism"].score >= 0.7:
            insights["potential_challenges"].append("High stress sensitivity and emotional reactivity")
        if traits["conscientiousness"].score <= 0.3:
            insights["potential_challenges"].append("May struggle with organization and follow-through")
        if traits["agreeableness"].score <= 0.3:
            insights["potential_challenges"].append("May have interpersonal conflicts")
        
        # Interpersonal style
        if traits["extraversion"].score >= 0.6 and traits["agreeableness"].score >= 0.6:
            insights["interpersonal_style"] = "Warm and socially engaging"
        elif traits["extraversion"].score <= 0.4 and traits["agreeableness"].score >= 0.6:
            insights["interpersonal_style"] = "Quietly supportive and thoughtful"
        elif traits["extraversion"].score >= 0.6 and traits["agreeableness"].score <= 0.4:
            insights["interpersonal_style"] = "Assertive and competitive"
        else:
            insights["interpersonal_style"] = "Reserved and independent"
        
        # Stress vulnerability
        stress_score = traits["neuroticism"].score - traits["conscientiousness"].score * 0.3
        if stress_score >= 0.5:
            insights["stress_vulnerability"] = "High vulnerability to stress and emotional overwhelm"
        elif stress_score <= 0.2:
            insights["stress_vulnerability"] = "Good stress resilience and emotional regulation"
        else:
            insights["stress_vulnerability"] = "Moderate stress sensitivity"
        
        return insights
    
    def _generate_recommendations(self, traits: Dict[str, BigFiveTrait], 
                                insights: Dict[str, Any]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        if traits["neuroticism"].score >= 0.7:
            recommendations.append("Consider stress management techniques and mindfulness practices")
        
        if traits["conscientiousness"].score <= 0.4:
            recommendations.append("Develop organizational systems and goal-setting strategies")
        
        if traits["openness"].score >= 0.7:
            recommendations.append("Channel creativity into structured projects for best outcomes")
        
        if traits["extraversion"].score <= 0.3:
            recommendations.append("Leverage independent work strengths while building gradual social skills")
        
        if traits["agreeableness"].score <= 0.3:
            recommendations.append("Practice active listening and empathy to improve relationships")
        
        # Combination recommendations
        if traits["conscientiousness"].score >= 0.7 and traits["neuroticism"].score >= 0.6:
            recommendations.append("High standards may increase stress - practice self-compassion")
        
        if not recommendations:
            recommendations.append("Well-balanced personality profile - continue current growth trajectory")
        
        return recommendations
    
    def _serialize_profile(self, profile: BigFiveProfile) -> Dict[str, Any]:
        """Serialize BigFiveProfile for JSON response"""
        return {
            "openness": {
                "name": profile.openness.name,
                "score": profile.openness.score,
                "percentile": profile.openness.percentile,
                "facet_scores": profile.openness.facet_scores,
                "evidence": profile.openness.evidence,
                "interpretation": profile.openness.interpretation
            },
            "conscientiousness": {
                "name": profile.conscientiousness.name,
                "score": profile.conscientiousness.score,
                "percentile": profile.conscientiousness.percentile,
                "facet_scores": profile.conscientiousness.facet_scores,
                "evidence": profile.conscientiousness.evidence,
                "interpretation": profile.conscientiousness.interpretation
            },
            "extraversion": {
                "name": profile.extraversion.name,
                "score": profile.extraversion.score,
                "percentile": profile.extraversion.percentile,
                "facet_scores": profile.extraversion.facet_scores,
                "evidence": profile.extraversion.evidence,
                "interpretation": profile.extraversion.interpretation
            },
            "agreeableness": {
                "name": profile.agreeableness.name,
                "score": profile.agreeableness.score,
                "percentile": profile.agreeableness.percentile,
                "facet_scores": profile.agreeableness.facet_scores,
                "evidence": profile.agreeableness.evidence,
                "interpretation": profile.agreeableness.interpretation
            },
            "neuroticism": {
                "name": profile.neuroticism.name,
                "score": profile.neuroticism.score,
                "percentile": profile.neuroticism.percentile,
                "facet_scores": profile.neuroticism.facet_scores,
                "evidence": profile.neuroticism.evidence,
                "interpretation": profile.neuroticism.interpretation
            }
        }
    
    def _generate_summary(self, profile: BigFiveProfile) -> str:
        """Generate a concise summary of the Big Five profile"""
        trait_summaries = []
        
        for trait_name in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]:
            trait = getattr(profile, trait_name)
            if trait.score >= 0.7:
                level = "High"
            elif trait.score >= 0.4:
                level = "Moderate"
            else:
                level = "Low"
            trait_summaries.append(f"{level} {trait_name.title()}")
        
        return f"Big Five Profile: {' | '.join(trait_summaries)}"


# Helper function for external usage
async def assess_big_five(text: str, agent_id: str = "big_five_agent") -> Dict[str, Any]:
    """Convenience function for Big Five personality assessment"""
    agent = BigFiveAgent(agent_id)
    message = AgentMessage(
        message_id="big_five_assessment",
        agent_id=agent_id,
        content={"text": text}
    )
    
    response = await agent.process(message)
    return response.content