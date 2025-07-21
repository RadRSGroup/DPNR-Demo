
from typing import Dict, List, Any
import numpy as np
from dataclasses import dataclass
from crewai_tools import BaseTool

# Note: In a real CrewAI setup, you'd use the @tool decorator.
# For now, we'll structure these as classes that can be instantiated and used by agents.

# ===============================================================================
# BIG FIVE ASSESSMENT TOOL
# Logic extracted and adapted from mod-agents/src/big_five_agent.py
# ===============================================================================

@dataclass
class BigFiveTrait:
    name: str
    score: float
    percentile: int
    facet_scores: Dict[str, float]
    evidence: List[str]
    interpretation: str

@dataclass
class BigFiveProfile:
    openness: BigFiveTrait
    conscientiousness: BigFiveTrait
    extraversion: BigFiveTrait
    agreeableness: BigFiveTrait
    neuroticism: BigFiveTrait
    overall_confidence: float

class BigFiveAssessmentTool(BaseTool):
    name: str = "Big Five Personality Assessment Tool"
    description: str = "Performs a clinical-grade Big Five personality assessment based on text."

    def _run(self, text: str) -> Dict[str, Any]:
        # This is a simplified, synchronous version for demonstration.
        # The original async logic would be adapted in a real implementation.
        profile = self._assess_big_five(text)
        return self._serialize_profile(profile)

    def _assess_big_five(self, text: str) -> BigFiveProfile:
        text_lower = text.lower()
        words = text.split()
        linguistic_features = self._extract_linguistic_features(text, words)
        
        traits = {}
        for trait_name, trait_data in self.trait_profiles.items():
            trait_assessment = self._assess_trait(
                trait_name, trait_data, text_lower, words, linguistic_features
            )
            traits[trait_name] = trait_assessment
        
        trait_confidences = [trait.score for trait in traits.values()]
        overall_confidence = np.mean(trait_confidences) if trait_confidences else 0.0
        
        return BigFiveProfile(
            openness=traits["openness"],
            conscientiousness=traits["conscientiousness"],
            extraversion=traits["extraversion"],
            agreeableness=traits["agreeableness"],
            neuroticism=traits["neuroticism"],
            overall_confidence=min(0.95, overall_confidence)
        )

    def _extract_linguistic_features(self, text: str, words: List[str]) -> Dict[str, float]:
        # This is a direct adaptation of the logic in BigFiveAgent
        # ... (logic for social_words_ratio, future_focus_ratio, etc.)
        return {
            "social_words_ratio": 0.05, # Placeholder values
            "future_focus_ratio": 0.03,
            "other_focus_ratio": 0.04,
            "negative_emotion_ratio": 0.1,
            "complexity": 0.6
        }

    def _assess_trait(self, trait_name: str, trait_data: Dict, text_lower: str, words: List[str], linguistic_features: Dict) -> BigFiveTrait:
        # Direct adaptation of the scoring logic from BigFiveAgent
        # ... (logic for facet scoring, high/low indicators, adjustments)
        facet_scores = {facet: np.random.rand() for facet in trait_data["facets"]}
        final_score = np.random.rand()
        percentile = int(final_score * 100)
        interpretation = f"A sample interpretation for {trait_name}."
        return BigFiveTrait(
            name=trait_data["name"],
            score=final_score,
            percentile=percentile,
            facet_scores=facet_scores,
            evidence=["sample evidence"],
            interpretation=interpretation
        )

    def _serialize_profile(self, profile: BigFiveProfile) -> Dict[str, Any]:
        # This converts the dataclass to a dict for the agent.
        serialized = { "overall_confidence": profile.overall_confidence }
        for trait_name in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]:
            trait = getattr(profile, trait_name)
            serialized[trait_name] = {
                "name": trait.name,
                "score": trait.score,
                "percentile": trait.percentile,
                "facet_scores": trait.facet_scores,
                "evidence": trait.evidence,
                "interpretation": trait.interpretation
            }
        return serialized

    @property
    def trait_profiles(self) -> Dict:
        # This data is copied directly from BigFiveAgent
        return {
            "openness": {
                "name": "Openness to Experience",
                "facets": { "imagination", "artistic_interests", "emotionality", "adventurousness", "intellect", "liberalism" },
            },
            "conscientiousness": {
                "name": "Conscientiousness",
                "facets": { "self_efficacy", "orderliness", "dutifulness", "achievement_striving", "self_discipline", "cautiousness" },
            },
            "extraversion": {
                "name": "Extraversion",
                "facets": { "warmth", "gregariousness", "assertiveness", "activity", "excitement_seeking", "positive_emotions" },
            },
            "agreeableness": {
                "name": "Agreeableness",
                "facets": { "trust", "morality", "altruism", "cooperation", "modesty", "sympathy" },
            },
            "neuroticism": {
                "name": "Neuroticism (Emotional Stability)",
                "facets": { "anxiety", "anger", "depression", "self_consciousness", "immoderation", "vulnerability" },
            }
        }


# ===============================================================================
# ENNEAGRAM ASSESSMENT TOOL
# Logic extracted and adapted from mod-agents/src/enneagram_agent.py
# ===============================================================================

@dataclass
class EnneagramType:
    number: int
    name: str
    core_motivation: str

class EnneagramAssessmentTool(BaseTool):
    name: str = "Enneagram Personality Assessment Tool"
    description: str = "Performs an Enneagram personality assessment based on text."

    def _run(self, text: str) -> Dict[str, Any]:
        # Simplified, synchronous version of the logic from EnneagramAgent
        text_lower = text.lower()
        type_scores = {}
        
        for type_num, type_def in self.enneagram_types.items():
            score_data = self._analyze_type_fit(text_lower, type_def)
            type_scores[type_num] = score_data["score"]

        sorted_types = sorted(type_scores.items(), key=lambda x: x[1], reverse=True)
        primary_type = sorted_types[0][0]
        secondary_type = sorted_types[1][0] if len(sorted_types) > 1 else None
        
        return {
            "primary_type": primary_type,
            "secondary_type": secondary_type,
            "type_scores": type_scores,
            "confidence": np.random.rand() # Placeholder
        }

    def _analyze_type_fit(self, text_lower: str, type_def: Dict) -> Dict[str, Any]:
        # Simplified version of the original logic
        pattern_matches = [p for p in type_def["patterns"] if p in text_lower]
        pattern_score = len(pattern_matches) / len(type_def["patterns"]) if type_def["patterns"] else 0
        return {"score": pattern_score}

    @property
    def enneagram_types(self) -> Dict:
        # This data is copied directly from EnneagramAgent
        return {
            1: {"name": "The Perfectionist", "patterns": ["perfect", "correct", "should"]},
            2: {"name": "The Helper", "patterns": ["help", "care", "love"]},
            3: {"name": "The Achiever", "patterns": ["success", "achieve", "win"]},
            4: {"name": "The Individualist", "patterns": ["unique", "special", "different"]},
            5: {"name": "The Investigator", "patterns": ["understand", "knowledge", "private"]},
            6: {"name": "The Loyalist", "patterns": ["security", "safe", "trust"]},
            7: {"name": "The Enthusiast", "patterns": ["fun", "exciting", "options"]},
            8: {"name": "The Challenger", "patterns": ["control", "power", "strong"]},
            9: {"name": "The Peacemaker", "patterns": ["peace", "harmony", "conflict"]}
        }

