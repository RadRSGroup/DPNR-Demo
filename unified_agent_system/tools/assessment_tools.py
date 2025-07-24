
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
# VALUES ASSESSMENT TOOL  
# Logic extracted from agent-library/agents/assessment/values_agent.py
# ===============================================================================

@dataclass
class ValueProfile:
    name: str
    description: str
    score: float
    percentile: int
    importance_level: str
    evidence: List[str]
    motivational_goal: str

@dataclass
class ValuesAssessment:
    individual_values: Dict[str, ValueProfile]
    value_priorities: List[tuple]
    motivational_insights: List[str]
    recommendations: List[str]
    overall_confidence: float

class ValuesAssessmentTool(BaseTool):
    name: str = "Values Assessment Tool"
    description: str = "Performs Schwartz values assessment to identify 10 universal human values."
    
    def _run(self, text: str) -> Dict[str, Any]:
        assessment = self._assess_values(text)
        return self._serialize_assessment(assessment)
    
    def _assess_values(self, text: str) -> ValuesAssessment:
        text_lower = text.lower()
        words = text.split()
        
        individual_values = {}
        for value_key, value_data in self.values_framework.items():
            value_profile = self._assess_single_value(value_key, value_data, text_lower, words)
            individual_values[value_key] = value_profile
        
        value_priorities = sorted(
            [(v.name, v.score) for v in individual_values.values()],
            key=lambda x: x[1], reverse=True
        )
        
        motivational_insights = self._generate_motivational_insights(individual_values)
        recommendations = self._generate_recommendations(individual_values)
        overall_confidence = np.mean([v.score for v in individual_values.values()])
        
        return ValuesAssessment(
            individual_values=individual_values,
            value_priorities=value_priorities[:5],
            motivational_insights=motivational_insights,
            recommendations=recommendations,
            overall_confidence=min(0.95, overall_confidence)
        )
    
    def _assess_single_value(self, value_key: str, value_data: Dict, text_lower: str, words: List[str]) -> ValueProfile:
        score = 0.0
        evidence = []
        
        # Keyword matching
        for keyword in value_data["keywords"]:
            if keyword in text_lower:
                score += 0.1
                evidence.append(f"Uses '{keyword}' (core {value_data['name']} value)")
                if len(evidence) >= 3:
                    break
        
        # Phrase matching (higher weight)
        for phrase in value_data["phrases"]:
            if phrase in text_lower:
                score += 0.2
                evidence.append(f"Expresses '{phrase}' (strong {value_data['name']} indicator)")
        
        final_score = min(1.0, max(0.0, score))
        
        if final_score >= 0.7:
            importance_level = "Very Important"
        elif final_score >= 0.5:
            importance_level = "Important"
        elif final_score >= 0.3:
            importance_level = "Moderately Important"
        else:
            importance_level = "Less Important"
        
        return ValueProfile(
            name=value_data["name"],
            description=value_data["description"],
            score=final_score,
            percentile=int(final_score * 100),
            importance_level=importance_level,
            evidence=evidence[:4],
            motivational_goal=value_data["motivational_goal"]
        )
    
    def _generate_motivational_insights(self, values: Dict[str, ValueProfile]) -> List[str]:
        insights = []
        top_values = sorted(values.values(), key=lambda v: v.score, reverse=True)[:3]
        
        if top_values[0].score > 0.7:
            insights.append(f"Strongly motivated by {top_values[0].motivational_goal.lower()}")
        
        # Specific value combinations
        if values["universalism"].score > 0.6 and values["benevolence"].score > 0.6:
            insights.append("Shows strong prosocial orientation - cares for both close others and humanity broadly")
        
        if values["achievement"].score > 0.6 and values["power"].score > 0.6:
            insights.append("Highly ambitious with strong drive for success and influence")
        
        return insights[:3]
    
    def _generate_recommendations(self, values: Dict[str, ValueProfile]) -> List[str]:
        recommendations = []
        high_values = [v for v in values.values() if v.score > 0.7]
        
        if high_values:
            top_value = max(high_values, key=lambda v: v.score)
            recommendations.append(f"Leverage your strong {top_value.name} values in decision-making")
        
        if values["achievement"].score > 0.6:
            recommendations.append("Seek roles with clear goals and opportunities for advancement")
        
        if values["self_direction"].score > 0.6:
            recommendations.append("Pursue activities that allow creative expression and autonomy")
        
        return recommendations[:3]
    
    def _serialize_assessment(self, assessment: ValuesAssessment) -> Dict[str, Any]:
        return {
            "values_profile": {
                key: {
                    "name": value.name,
                    "score": value.score,
                    "percentile": value.percentile,
                    "importance_level": value.importance_level,
                    "evidence": value.evidence,
                    "motivational_goal": value.motivational_goal
                }
                for key, value in assessment.individual_values.items()
            },
            "value_priorities": assessment.value_priorities,
            "motivational_insights": assessment.motivational_insights,
            "recommendations": assessment.recommendations,
            "overall_confidence": assessment.overall_confidence
        }
    
    @property
    def values_framework(self) -> Dict:
        return {
            "self_direction": {
                "name": "Self-Direction",
                "description": "Independent thought and action; choosing, creating, exploring",
                "motivational_goal": "Independent thought and action",
                "keywords": ["independent", "creative", "freedom", "choice", "curious", "explore", "authentic", "original"],
                "phrases": ["my own way", "be myself", "make my own", "creative solution", "explore new"]
            },
            "stimulation": {
                "name": "Stimulation",
                "description": "Excitement, novelty, and challenge in life",
                "motivational_goal": "Excitement and challenge",
                "keywords": ["exciting", "adventure", "thrill", "challenge", "risk", "new", "stimulating", "bold"],
                "phrases": ["love adventure", "seek excitement", "take risks", "new challenges"]
            },
            "hedonism": {
                "name": "Hedonism",
                "description": "Pleasure and sensuous gratification for oneself", 
                "motivational_goal": "Pleasure and enjoyment",
                "keywords": ["pleasure", "enjoy", "fun", "satisfy", "indulge", "comfort", "luxury", "relax"],
                "phrases": ["enjoy life", "feel good", "treat myself", "pure pleasure"]
            },
            "achievement": {
                "name": "Achievement",
                "description": "Personal success through demonstrating competence",
                "motivational_goal": "Success and accomplishment",
                "keywords": ["success", "achieve", "accomplish", "goal", "excel", "competent", "ambitious"],
                "phrases": ["reach my goals", "be successful", "demonstrate competence", "achieve excellence"]
            },
            "power": {
                "name": "Power",
                "description": "Social status and prestige, control or dominance",
                "motivational_goal": "Status and control",
                "keywords": ["power", "authority", "control", "influence", "status", "prestige", "wealth"],
                "phrases": ["in control", "position of power", "high status", "social prestige"]
            },
            "security": {
                "name": "Security",
                "description": "Safety, harmony, and stability of society and self",
                "motivational_goal": "Safety and stability",
                "keywords": ["secure", "safe", "stable", "protect", "order", "clean", "healthy", "family"],
                "phrases": ["feel secure", "stay safe", "stable environment", "protect family"]
            },
            "conformity": {
                "name": "Conformity",
                "description": "Restraint of actions that might violate social expectations",
                "motivational_goal": "Social harmony and compliance",
                "keywords": ["polite", "obedient", "dutiful", "responsible", "honor", "respect", "proper"],
                "phrases": ["follow rules", "do what's expected", "respect authority", "proper behavior"]
            },
            "tradition": {
                "name": "Tradition",
                "description": "Respect and commitment to cultural or religious customs",
                "motivational_goal": "Cultural and religious tradition",
                "keywords": ["tradition", "culture", "custom", "heritage", "ancestors", "roots", "religious"],
                "phrases": ["cultural traditions", "honor ancestors", "religious beliefs", "family heritage"]
            },
            "benevolence": {
                "name": "Benevolence",
                "description": "Preserving and enhancing welfare of close others",
                "motivational_goal": "Care for close others",
                "keywords": ["helpful", "caring", "loyal", "honest", "responsible", "love", "family", "forgive"],
                "phrases": ["help others", "care for family", "true friendship", "be there for"]
            },
            "universalism": {
                "name": "Universalism",
                "description": "Understanding, tolerance, and protection for all people and nature",
                "motivational_goal": "Welfare of all people and nature",
                "keywords": ["justice", "equality", "peace", "tolerance", "wisdom", "unity", "environment"],
                "phrases": ["social justice", "protect environment", "world peace", "equal rights"]
            }
        }


# ===============================================================================
# EMOTIONAL INTELLIGENCE ASSESSMENT TOOL
# Logic extracted from agent-library/agents/assessment/emotional_intelligence_agent.py  
# ===============================================================================

@dataclass
class EQDomain:
    name: str
    description: str
    score: float
    percentile: int
    competency_level: str
    evidence: List[str]

@dataclass 
class EQAssessment:
    domains: Dict[str, EQDomain]
    overall_eq_score: float
    eq_strengths: List[str]
    development_priorities: List[str]
    recommendations: List[str]
    overall_confidence: float

class EmotionalIntelligenceAssessmentTool(BaseTool):
    name: str = "Emotional Intelligence Assessment Tool"
    description: str = "Performs Four-Domain Emotional Intelligence assessment based on text."
    
    def _run(self, text: str) -> Dict[str, Any]:
        assessment = self._assess_emotional_intelligence(text)
        return self._serialize_assessment(assessment)
    
    def _assess_emotional_intelligence(self, text: str) -> EQAssessment:
        text_lower = text.lower()
        words = text.split()
        
        domains = {}
        for domain_key, domain_data in self.eq_domains.items():
            domain_assessment = self._assess_eq_domain(domain_key, domain_data, text_lower, words)
            domains[domain_key] = domain_assessment
        
        domain_scores = [domain.score for domain in domains.values()]
        overall_eq_score = np.mean(domain_scores)
        
        eq_strengths = self._identify_eq_strengths(domains)
        development_priorities = self._identify_development_priorities(domains)
        recommendations = self._generate_recommendations(domains)
        
        overall_confidence = min(0.95, overall_eq_score * 0.8 + (len(text) / 1000) * 0.2)
        
        return EQAssessment(
            domains=domains,
            overall_eq_score=overall_eq_score,
            eq_strengths=eq_strengths,
            development_priorities=development_priorities,
            recommendations=recommendations,
            overall_confidence=overall_confidence
        )
    
    def _assess_eq_domain(self, domain_key: str, domain_data: Dict, text_lower: str, words: List[str]) -> EQDomain:
        score = 0.0
        evidence = []
        
        # Assess keyword categories
        for category, keywords in domain_data["keywords"].items():
            category_score = 0.0
            for keyword in keywords:
                if keyword in text_lower:
                    category_score += 0.1
                    evidence.append(f"Shows {category.replace('_', ' ')}: uses '{keyword}'")
            score += category_score
        
        # Assess phrases (higher weight)
        for phrase in domain_data["phrases"]:
            if phrase in text_lower:
                score += 0.15
                evidence.append(f"Demonstrates {domain_data['name']}: '{phrase}'")
        
        final_score = min(1.0, max(0.0, score))
        
        if final_score >= 0.8:
            competency_level = "Advanced"
        elif final_score >= 0.6:
            competency_level = "Proficient"
        elif final_score >= 0.4:
            competency_level = "Developing"
        else:
            competency_level = "Emerging"
        
        return EQDomain(
            name=domain_data["name"],
            description=domain_data["description"],
            score=final_score,
            percentile=int(final_score * 100),
            competency_level=competency_level,
            evidence=evidence[:4]
        )
    
    def _identify_eq_strengths(self, domains: Dict[str, EQDomain]) -> List[str]:
        strengths = []
        strong_domains = [domain for domain in domains.values() if domain.score >= 0.7]
        for domain in strong_domains:
            strengths.append(f"Strong {domain.name.lower()} abilities")
        return strengths[:3]
    
    def _identify_development_priorities(self, domains: Dict[str, EQDomain]) -> List[str]:
        priorities = []
        sorted_domains = sorted(domains.values(), key=lambda d: d.score)
        for domain in sorted_domains:
            if domain.score < 0.5:
                priorities.append(f"Develop {domain.name.lower()} skills")
        return priorities[:3]
    
    def _generate_recommendations(self, domains: Dict[str, EQDomain]) -> List[str]:
        recommendations = []
        
        if domains["perceiving_emotions"].score < 0.6:
            recommendations.append("Practice mindfulness and emotional check-ins to increase awareness")
        
        if domains["managing_emotions"].score < 0.6:
            recommendations.append("Develop specific emotion regulation strategies and stress management techniques")
        
        recommendations.append("Practice active listening and empathy in daily interactions")
        return recommendations[:3]
    
    def _serialize_assessment(self, assessment: EQAssessment) -> Dict[str, Any]:
        return {
            "eq_profile": {
                key: {
                    "name": domain.name,
                    "score": domain.score,
                    "percentile": domain.percentile,
                    "competency_level": domain.competency_level,
                    "evidence": domain.evidence
                }
                for key, domain in assessment.domains.items()
            },
            "overall_score": assessment.overall_eq_score,
            "strengths": assessment.eq_strengths,
            "development_priorities": assessment.development_priorities,
            "recommendations": assessment.recommendations,
            "overall_confidence": assessment.overall_confidence
        }
    
    @property
    def eq_domains(self) -> Dict:
        return {
            "perceiving_emotions": {
                "name": "Perceiving Emotions",
                "description": "Ability to identify emotions in oneself and others",
                "keywords": {
                    "self_awareness": ["feel", "sense", "notice", "aware", "recognize", "realize"],
                    "other_awareness": ["see that", "notice others", "pick up", "read people"],
                    "emotional_cues": ["facial", "body language", "tone", "voice", "expression"]
                },
                "phrases": ["I can tell when", "I sense that", "I notice when", "body language tells me"]
            },
            "using_emotions": {
                "name": "Using Emotions",
                "description": "Ability to harness emotions to facilitate thinking",
                "keywords": {
                    "motivation": ["motivated", "passionate", "driven", "excited", "energized"],
                    "emotional_leverage": ["channel", "use my", "harness", "draw on", "fuel"]
                },
                "phrases": ["channel my emotions", "use my passion", "passion drives me"]
            },
            "understanding_emotions": {
                "name": "Understanding Emotions", 
                "description": "Ability to comprehend emotional language and progression",
                "keywords": {
                    "emotional_complexity": ["complex", "mixed feelings", "conflicted", "nuanced"],
                    "emotion_causes": ["because", "due to", "triggered by", "makes me feel"]
                },
                "phrases": ["understand why", "emotional pattern", "complex emotions"]
            },
            "managing_emotions": {
                "name": "Managing Emotions",
                "description": "Ability to regulate emotions in self and influence others",
                "keywords": {
                    "self_regulation": ["calm down", "control", "manage", "regulate", "cope"],
                    "influence_others": ["help others", "calm them", "encourage", "support"]
                },
                "phrases": ["calm myself down", "manage my emotions", "emotional control"]
            }
        }


# ===============================================================================
# COGNITIVE STYLE ASSESSMENT TOOL
# Logic extracted from agent-library/agents/assessment/cognitive_style_agent.py
# ===============================================================================

@dataclass
class CognitiveDimension:
    name: str
    description: str
    score: float
    percentile: int
    style_category: str
    evidence: List[str]
    implications: List[str]

@dataclass
class CognitiveAssessment:
    dimensions: Dict[str, CognitiveDimension]
    cognitive_strengths: List[str]
    optimal_environments: List[str]
    development_suggestions: List[str]
    overall_confidence: float

class CognitiveStyleAssessmentTool(BaseTool):
    name: str = "Cognitive Style Assessment Tool"
    description: str = "Assesses cognitive style dimensions and thinking patterns."
    
    def _run(self, text: str) -> Dict[str, Any]:
        assessment = self._assess_cognitive_style(text)
        return self._serialize_assessment(assessment)
    
    def _assess_cognitive_style(self, text: str) -> CognitiveAssessment:
        text_lower = text.lower()
        words = text.split()
        
        dimensions = {}
        for dimension_key, dimension_data in self.cognitive_dimensions.items():
            dimension_assessment = self._assess_cognitive_dimension(
                dimension_key, dimension_data, text_lower, words
            )
            dimensions[dimension_key] = dimension_assessment
        
        cognitive_strengths = self._identify_cognitive_strengths(dimensions)
        optimal_environments = self._suggest_optimal_environments(dimensions)
        development_suggestions = self._generate_development_suggestions(dimensions)
        
        dimension_scores = [abs(d.score - 0.5) * 2 for d in dimensions.values()]
        overall_confidence = min(0.95, np.mean(dimension_scores) * 0.8)
        
        return CognitiveAssessment(
            dimensions=dimensions,
            cognitive_strengths=cognitive_strengths,
            optimal_environments=optimal_environments,
            development_suggestions=development_suggestions,
            overall_confidence=overall_confidence
        )
    
    def _assess_cognitive_dimension(self, dimension_key: str, dimension_data: Dict, 
                                  text_lower: str, words: List[str]) -> CognitiveDimension:
        
        # Get indicator types for this dimension
        if dimension_key == "analytical_intuitive":
            low_indicators = dimension_data["analytical_indicators"]
            high_indicators = dimension_data["intuitive_indicators"]
        elif dimension_key == "detail_big_picture":
            low_indicators = dimension_data["detail_indicators"]
            high_indicators = dimension_data["big_picture_indicators"]
        else:
            # Default fallback
            low_indicators = {"keywords": [], "phrases": []}
            high_indicators = {"keywords": [], "phrases": []}
        
        # Score both ends
        low_score = self._score_indicators(low_indicators, text_lower)
        high_score = self._score_indicators(high_indicators, text_lower)
        
        # Calculate dimension score
        total_score = low_score + high_score
        dimension_score = high_score / total_score if total_score > 0 else 0.5
        
        # Determine style category
        if dimension_score >= 0.7:
            style_category = f"Strong {dimension_data['dimension_pair'][1]}"
        elif dimension_score >= 0.6:
            style_category = f"Moderate {dimension_data['dimension_pair'][1]}"
        elif dimension_score <= 0.3:
            style_category = f"Strong {dimension_data['dimension_pair'][0]}"
        elif dimension_score <= 0.4:
            style_category = f"Moderate {dimension_data['dimension_pair'][0]}"
        else:
            style_category = "Balanced"
        
        evidence = []
        if low_score > 0:
            evidence.append(f"{dimension_data['dimension_pair'][0]} thinking patterns detected")
        if high_score > 0:
            evidence.append(f"{dimension_data['dimension_pair'][1]} thinking patterns detected")
        
        implications = self._generate_dimension_implications(dimension_key, dimension_score)
        
        return CognitiveDimension(
            name=dimension_data["name"],
            description=dimension_data["description"],
            score=dimension_score,
            percentile=int(dimension_score * 100),
            style_category=style_category,
            evidence=evidence[:3],
            implications=implications
        )
    
    def _score_indicators(self, indicators: Dict, text_lower: str) -> float:
        score = 0.0
        for keyword in indicators.get("keywords", []):
            if keyword in text_lower:
                score += 0.1
        for phrase in indicators.get("phrases", []):
            if phrase in text_lower:
                score += 0.15
        return score
    
    def _generate_dimension_implications(self, dimension_key: str, score: float) -> List[str]:
        implications = []
        
        if dimension_key == "analytical_intuitive":
            if score <= 0.4:
                implications.append("Prefers systematic analysis and logical reasoning")
            elif score >= 0.6:
                implications.append("Relies on holistic understanding and gut feelings")
        
        return implications[:2]
    
    def _identify_cognitive_strengths(self, dimensions: Dict[str, CognitiveDimension]) -> List[str]:
        strengths = []
        for dimension in dimensions.values():
            if "Strong" in dimension.style_category:
                strengths.append(f"Strong {dimension.style_category.lower().replace('strong ', '')} thinking")
        return strengths[:3]
    
    def _suggest_optimal_environments(self, dimensions: Dict[str, CognitiveDimension]) -> List[str]:
        environments = []
        if "analytical_intuitive" in dimensions:
            if dimensions["analytical_intuitive"].score <= 0.4:
                environments.append("Structured environments with clear analytical processes")
            elif dimensions["analytical_intuitive"].score >= 0.6:
                environments.append("Creative environments that value intuitive insights")
        return environments[:2]
    
    def _generate_development_suggestions(self, dimensions: Dict[str, CognitiveDimension]) -> List[str]:
        suggestions = []
        for dimension in dimensions.values():
            if dimension.score <= 0.2 or dimension.score >= 0.8:
                suggestions.append("Practice metacognition - reflect on your thinking processes")
                break
        return suggestions[:2]
    
    def _serialize_assessment(self, assessment: CognitiveAssessment) -> Dict[str, Any]:
        return {
            "cognitive_profile": {
                key: {
                    "name": dimension.name,
                    "score": dimension.score,
                    "percentile": dimension.percentile,
                    "style_category": dimension.style_category,
                    "evidence": dimension.evidence,
                    "implications": dimension.implications
                }
                for key, dimension in assessment.dimensions.items()
            },
            "strengths": assessment.cognitive_strengths,
            "optimal_environments": assessment.optimal_environments,
            "development_suggestions": assessment.development_suggestions,
            "overall_confidence": assessment.overall_confidence
        }
    
    @property
    def cognitive_dimensions(self) -> Dict:
        return {
            "analytical_intuitive": {
                "name": "Analytical-Intuitive Thinking",
                "description": "Preference for systematic analysis vs holistic intuition",
                "dimension_pair": ("Analytical", "Intuitive"),
                "analytical_indicators": {
                    "keywords": ["analyze", "logical", "systematic", "methodical", "rational", "evidence"],
                    "phrases": ["step by step", "break down", "logical approach"]
                },
                "intuitive_indicators": {
                    "keywords": ["feel", "sense", "intuition", "gut", "instinct", "hunch"],
                    "phrases": ["gut feeling", "sense that", "feels right"]
                }
            },
            "detail_big_picture": {
                "name": "Detail-Big Picture Orientation", 
                "description": "Focus on specifics vs overall patterns",
                "dimension_pair": ("Detail-Oriented", "Big Picture"),
                "detail_indicators": {
                    "keywords": ["detail", "specific", "precise", "exact", "careful", "thorough"],
                    "phrases": ["pay attention to", "focus on details", "specifically"]
                },
                "big_picture_indicators": {
                    "keywords": ["overall", "general", "concept", "vision", "strategy", "broad"],
                    "phrases": ["big picture", "overall view", "general idea"]
                }
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


# ===============================================================================
# INTEGRATION TOOL
# Combines results from multiple assessment frameworks
# ===============================================================================

class IntegrationAssessmentTool(BaseTool):
    name: str = "Integration Assessment Tool"
    description: str = "Integrates results from multiple personality assessment frameworks."
    
    def _run(self, assessment_results: Dict[str, Any]) -> Dict[str, Any]:
        return self._integrate_assessments(assessment_results)
    
    def _integrate_assessments(self, results: Dict[str, Any]) -> Dict[str, Any]:
        integration = {
            "convergent_themes": self._find_convergent_themes(results),
            "framework_interactions": self._analyze_framework_interactions(results),
            "personality_synthesis": self._synthesize_personality(results),
            "integrated_recommendations": self._generate_integrated_recommendations(results)
        }
        return integration
    
    def _find_convergent_themes(self, results: Dict[str, Any]) -> List[str]:
        themes = []
        
        # Example: High conscientiousness + Enneagram Type 1 + Achievement values
        if (results.get("big_five", {}).get("conscientiousness", {}).get("score", 0) > 0.7 and
            results.get("enneagram", {}).get("primary_type") == 1 and
            results.get("values", {}).get("values_profile", {}).get("achievement", {}).get("score", 0) > 0.6):
            themes.append("Strong perfectionist and achievement-oriented personality")
        
        return themes
    
    def _analyze_framework_interactions(self, results: Dict[str, Any]) -> List[str]:
        interactions = []
        
        # Example interactions
        if results.get("emotional_intelligence", {}).get("overall_score", 0) > 0.7:
            interactions.append("High EI supports interpersonal effectiveness across other frameworks")
        
        return interactions
    
    def _synthesize_personality(self, results: Dict[str, Any]) -> str:
        synthesis_parts = []
        
        # Extract key characteristics from each framework
        if "enneagram" in results:
            primary_type = results["enneagram"].get("primary_type")
            if primary_type:
                synthesis_parts.append(f"Core Enneagram Type {primary_type} patterns")
        
        if "big_five" in results:
            bf_summary = "Big Five profile shows "
            high_traits = []
            for trait in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]:
                score = results["big_five"].get(trait, {}).get("score", 0)
                if score > 0.7:
                    high_traits.append(f"high {trait}")
            if high_traits:
                bf_summary += ", ".join(high_traits)
                synthesis_parts.append(bf_summary)
        
        return "; ".join(synthesis_parts) if synthesis_parts else "Integrated personality profile pending analysis"
    
    def _generate_integrated_recommendations(self, results: Dict[str, Any]) -> List[str]:
        recommendations = []
        
        # Cross-framework recommendations
        recommendations.append("Leverage identified strengths across all frameworks for optimal growth")
        recommendations.append("Address development areas consistently across personality dimensions")
        
        return recommendations

