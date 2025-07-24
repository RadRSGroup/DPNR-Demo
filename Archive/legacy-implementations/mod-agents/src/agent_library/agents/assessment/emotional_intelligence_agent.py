"""
Emotional Intelligence Assessment Agent

Implements the Four-Domain Model of Emotional Intelligence (Mayer & Salovey).
Assesses ability to perceive, use, understand, and manage emotions effectively.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import asyncio
from dataclasses import dataclass
import re

from ...core.base_agent import BaseAgent, AgentMessage, AgentResponse, AgentCapability, AgentStatus


@dataclass
class EQDomain:
    """Represents one of the four EQ domains"""
    name: str
    description: str
    score: float
    percentile: int
    competency_level: str
    evidence: List[str]
    development_areas: List[str]
    strengths: List[str]


@dataclass
class EmotionalProfile:
    """Emotional vocabulary and expression analysis"""
    emotion_vocabulary_size: int
    emotion_complexity: float
    emotional_granularity: str  # broad, moderate, specific
    dominant_emotions: List[str]
    emotion_regulation_style: str
    emotional_awareness_level: str


@dataclass
class EQAssessment:
    """Complete Emotional Intelligence assessment"""
    domains: Dict[str, EQDomain]
    overall_eq_score: float
    overall_percentile: int
    emotional_profile: EmotionalProfile
    eq_strengths: List[str]
    development_priorities: List[str]
    interpersonal_insights: List[str]
    leadership_implications: List[str]
    recommendations: List[str]
    overall_confidence: float


class EmotionalIntelligenceAgent(BaseAgent):
    """
    Four-Domain Emotional Intelligence Assessment Agent
    
    Assesses the four core EQ domains:
    1. Perceiving Emotions - Identifying emotions in self and others
    2. Using Emotions - Harnessing emotions to facilitate thinking
    3. Understanding Emotions - Comprehending emotional development and progression
    4. Managing Emotions - Regulating emotions in self and others
    """
    
    def __init__(self, agent_id: str = "emotional_intelligence_agent"):
        super().__init__(agent_id, "Emotional Intelligence Assessment Agent", "1.0.0")
        self.capabilities = [
            "emotional_intelligence_assessment",
            "eq_domain_analysis", 
            "emotional_vocabulary_analysis",
            "emotion_regulation_assessment",
            "interpersonal_eq_insights",
            "leadership_eq_profiling"
        ]
        
        # Four-Domain EQ Framework
        self.eq_domains = {
            "perceiving_emotions": {
                "name": "Perceiving Emotions",
                "description": "Ability to identify emotions in oneself and others",
                "keywords": {
                    "self_awareness": ["feel", "sense", "notice", "aware", "recognize", "realize", 
                                     "understand myself", "know when", "pick up on"],
                    "other_awareness": ["see that", "notice others", "pick up", "sense when", 
                                      "read people", "tell when", "observe"],
                    "emotional_cues": ["facial", "body language", "tone", "voice", "expression", 
                                     "gesture", "mood", "vibe", "energy"],
                    "intuition": ["gut feeling", "instinct", "intuition", "sense that", 
                                "something tells me", "feeling is"]
                },
                "phrases": [
                    "I can tell when", "I sense that", "I notice when people", 
                    "I pick up on", "I'm aware of", "I realize that",
                    "body language tells me", "tone of voice", "facial expression"
                ],
                "competencies": [
                    "Emotional self-awareness", "Accurate self-assessment", 
                    "Self-confidence", "Empathy", "Organizational awareness"
                ]
            },
            "using_emotions": {
                "name": "Using Emotions",
                "description": "Ability to harness emotions to facilitate thinking and problem-solving",
                "keywords": {
                    "motivation": ["motivated", "passionate", "driven", "excited", "energized",
                                 "inspired", "enthusiasm", "determination"],
                    "emotional_leverage": ["channel", "use my", "harness", "draw on", "fuel",
                                         "emotional energy", "passion drives"],
                    "mood_influence": ["when I'm happy", "when excited", "feeling good", 
                                     "positive mood", "emotional state"],
                    "emotional_thinking": ["feel strongly", "emotionally invested", "gut tells me",
                                         "heart says", "passionate about"]
                },
                "phrases": [
                    "channel my emotions", "use my passion", "emotional energy helps",
                    "when I feel", "passion drives me", "emotions guide",
                    "harness my", "emotional fuel", "feeling motivates"
                ],
                "competencies": [
                    "Emotional self-control", "Achievement orientation", 
                    "Positive outlook", "Adaptability"
                ]
            },
            "understanding_emotions": {
                "name": "Understanding Emotions",
                "description": "Ability to comprehend emotional language and progression",
                "keywords": {
                    "emotional_complexity": ["complex", "mixed feelings", "conflicted", "torn",
                                           "ambivalent", "nuanced", "layered"],
                    "emotion_causes": ["because", "due to", "triggered by", "stems from",
                                     "reason for", "makes me feel", "causes"],
                    "emotion_progression": ["leads to", "escalates", "builds up", "develops into",
                                          "turns into", "eventually", "progression"],
                    "emotional_vocabulary": ["frustrated", "disappointed", "overwhelmed", "anxious",
                                           "optimistic", "content", "irritated", "elated"]
                },
                "phrases": [
                    "understand why", "makes sense that", "emotional pattern", 
                    "leads to feeling", "because of", "resulting in",
                    "complex emotions", "mixed feelings", "understand the connection"
                ],
                "competencies": [
                    "Emotional literacy", "Systems thinking", "Pattern recognition",
                    "Cognitive empathy", "Emotional awareness"
                ]
            },
            "managing_emotions": {
                "name": "Managing Emotions",
                "description": "Ability to regulate emotions in self and influence others",
                "keywords": {
                    "self_regulation": ["calm down", "control", "manage", "regulate", "cope",
                                      "handle", "deal with", "work through"],
                    "influence_others": ["help others", "calm them", "encourage", "support",
                                       "guide", "reassure", "comfort"],
                    "emotional_strategies": ["take a breath", "step back", "perspective", "reframe",
                                           "think differently", "strategy", "approach"],
                    "recovery": ["bounce back", "recover", "resilient", "overcome", "move on",
                               "get through", "persevere"]
                },
                "phrases": [
                    "calm myself down", "help others feel", "manage my emotions",
                    "regulate my", "cope with", "work through",
                    "emotional control", "stay composed", "influence mood"
                ],
                "competencies": [
                    "Emotional self-control", "Stress tolerance", "Conflict management",
                    "Inspirational leadership", "Coach and mentor", "Influence"
                ]
            }
        }
        
        # Emotional vocabulary categories
        self.emotion_categories = {
            "basic_emotions": ["happy", "sad", "angry", "afraid", "surprised", "disgusted"],
            "complex_emotions": [
                "frustrated", "disappointed", "overwhelmed", "anxious", "optimistic", 
                "content", "irritated", "elated", "melancholy", "euphoric", "apprehensive",
                "contemplative", "exhilarated", "despondent", "serene", "agitated"
            ],
            "emotional_nuances": [
                "bittersweet", "ambivalent", "conflicted", "torn", "mixed feelings",
                "emotional rollercoaster", "complex emotions", "nuanced feelings"
            ]
        }
        
        # Emotion regulation strategies
        self.regulation_strategies = {
            "cognitive": ["reframe", "perspective", "think differently", "rationalize", "analyze"],
            "behavioral": ["take action", "do something", "physical activity", "routine", "structure"],
            "social": ["talk to", "seek support", "share with", "connect", "reach out"],
            "somatic": ["breathe", "relax", "meditate", "calm", "center myself"]
        }
    
    async def process(self, message: AgentMessage) -> AgentResponse:
        """Process text for emotional intelligence assessment"""
        try:
            text = message.content.get("text", "")
            if not text or len(text.strip()) < 40:
                return AgentResponse(
                    agent_id=self.agent_id,
                    content={"error": "Insufficient text for EQ assessment (minimum 40 characters)"},
                    confidence=0.0
                )
            
            # Perform EQ assessment
            assessment = await self._assess_emotional_intelligence(text)
            
            result = {
                "eq_profile": self._serialize_assessment(assessment),
                "overall_score": assessment.overall_eq_score,
                "strengths": assessment.eq_strengths,
                "development_priorities": assessment.development_priorities,
                "recommendations": assessment.recommendations,
                "summary": self._generate_summary(assessment)
            }
            
            return AgentResponse(
                agent_id=self.agent_id,
                content=result,
                confidence=assessment.overall_confidence
            )
            
        except Exception as e:
            return AgentResponse(
                agent_id=self.agent_id,
                content={"error": f"EQ assessment failed: {str(e)}"},
                confidence=0.0
            )
    
    async def _assess_emotional_intelligence(self, text: str) -> EQAssessment:
        """Perform comprehensive emotional intelligence assessment"""
        text_lower = text.lower()
        words = text.split()
        
        # Assess each EQ domain
        domains = {}
        for domain_key, domain_data in self.eq_domains.items():
            domain_assessment = await self._assess_eq_domain(
                domain_key, domain_data, text_lower, words
            )
            domains[domain_key] = domain_assessment
        
        # Analyze emotional profile
        emotional_profile = self._analyze_emotional_profile(text_lower, words)
        
        # Calculate overall EQ score
        domain_scores = [domain.score for domain in domains.values()]
        overall_eq_score = np.mean(domain_scores)
        overall_percentile = int(overall_eq_score * 100)
        
        # Generate insights and recommendations
        eq_strengths = self._identify_eq_strengths(domains, emotional_profile)
        development_priorities = self._identify_development_priorities(domains)
        interpersonal_insights = self._generate_interpersonal_insights(domains, emotional_profile)
        leadership_implications = self._generate_leadership_implications(domains)
        recommendations = self._generate_recommendations(domains, development_priorities)
        
        # Calculate confidence
        text_length_factor = min(0.3, len(text) / 1000)
        emotional_content_factor = self._calculate_emotional_content_richness(text_lower)
        overall_confidence = min(0.95, overall_eq_score * 0.7 + text_length_factor + emotional_content_factor)
        
        return EQAssessment(
            domains=domains,
            overall_eq_score=overall_eq_score,
            overall_percentile=overall_percentile,
            emotional_profile=emotional_profile,
            eq_strengths=eq_strengths,
            development_priorities=development_priorities,
            interpersonal_insights=interpersonal_insights,
            leadership_implications=leadership_implications,
            recommendations=recommendations,
            overall_confidence=overall_confidence
        )
    
    async def _assess_eq_domain(self, domain_key: str, domain_data: Dict[str, Any],
                              text_lower: str, words: List[str]) -> EQDomain:
        """Assess a single EQ domain"""
        score = 0.0
        evidence = []
        
        # Assess keyword categories
        for category, keywords in domain_data["keywords"].items():
            category_score = 0.0
            for keyword in keywords:
                if keyword in text_lower:
                    category_score += 0.1
                    evidence.append(f"Shows {category.replace('_', ' ')}: uses '{keyword}'")
            
            # Weight categories differently based on domain
            if domain_key == "perceiving_emotions" and category in ["self_awareness", "other_awareness"]:
                score += category_score * 1.2
            elif domain_key == "using_emotions" and category in ["motivation", "emotional_leverage"]:
                score += category_score * 1.2
            elif domain_key == "understanding_emotions" and category in ["emotional_complexity", "emotion_causes"]:
                score += category_score * 1.2
            elif domain_key == "managing_emotions" and category in ["self_regulation", "influence_others"]:
                score += category_score * 1.2
            else:
                score += category_score
        
        # Assess phrases (higher weight)
        for phrase in domain_data["phrases"]:
            if phrase in text_lower:
                score += 0.15
                evidence.append(f"Demonstrates {domain_data['name']}: '{phrase}'")
        
        # Domain-specific analysis
        domain_bonus = self._analyze_domain_specific_patterns(domain_key, text_lower, words)
        score += domain_bonus
        
        # Normalize score
        final_score = min(1.0, max(0.0, score))
        
        # Determine competency level
        if final_score >= 0.8:
            competency_level = "Advanced"
        elif final_score >= 0.6:
            competency_level = "Proficient"
        elif final_score >= 0.4:
            competency_level = "Developing"
        else:
            competency_level = "Emerging"
        
        # Generate development areas and strengths
        strengths, development_areas = self._analyze_domain_competencies(
            domain_data, final_score, evidence
        )
        
        return EQDomain(
            name=domain_data["name"],
            description=domain_data["description"],
            score=final_score,
            percentile=int(final_score * 100),
            competency_level=competency_level,
            evidence=evidence[:4],  # Limit evidence
            development_areas=development_areas,
            strengths=strengths
        )
    
    def _analyze_domain_specific_patterns(self, domain_key: str, text_lower: str, words: List[str]) -> float:
        """Analyze domain-specific patterns for bonus scoring"""
        bonus = 0.0
        
        if domain_key == "perceiving_emotions":
            # Look for emotional observation language
            observation_words = ["notice", "observe", "see", "watch", "detect"]
            emotion_words = ["feel", "emotion", "mood", "upset", "happy", "sad"]
            
            for obs_word in observation_words:
                for emo_word in emotion_words:
                    if obs_word in text_lower and emo_word in text_lower:
                        bonus += 0.05
                        break
        
        elif domain_key == "using_emotions":
            # Look for emotional motivation patterns
            if "passion" in text_lower and any(word in text_lower for word in ["drive", "motivate", "fuel"]):
                bonus += 0.1
            
        elif domain_key == "understanding_emotions":
            # Look for causal emotional reasoning
            causal_patterns = ["because I feel", "feeling leads to", "when I'm", "makes me feel"]
            for pattern in causal_patterns:
                if pattern in text_lower:
                    bonus += 0.05
        
        elif domain_key == "managing_emotions":
            # Look for emotional regulation strategies
            for strategy_type, strategies in self.regulation_strategies.items():
                strategy_count = sum(1 for strategy in strategies if strategy in text_lower)
                if strategy_count > 0:
                    bonus += 0.03 * strategy_count
        
        return min(0.2, bonus)  # Cap bonus
    
    def _analyze_emotional_profile(self, text_lower: str, words: List[str]) -> EmotionalProfile:
        """Analyze emotional vocabulary and expression patterns"""
        
        # Count emotional vocabulary
        basic_emotion_count = sum(1 for emotion in self.emotion_categories["basic_emotions"] 
                                if emotion in text_lower)
        complex_emotion_count = sum(1 for emotion in self.emotion_categories["complex_emotions"] 
                                  if emotion in text_lower)
        nuance_count = sum(1 for nuance in self.emotion_categories["emotional_nuances"] 
                         if nuance in text_lower)
        
        emotion_vocabulary_size = basic_emotion_count + complex_emotion_count + nuance_count
        
        # Calculate emotional complexity
        if nuance_count > 0 or complex_emotion_count > 2:
            emotion_complexity = 0.8 + (nuance_count * 0.1)
        elif complex_emotion_count > 0:
            emotion_complexity = 0.5 + (complex_emotion_count * 0.1)
        else:
            emotion_complexity = 0.2 + (basic_emotion_count * 0.1)
        
        emotion_complexity = min(1.0, emotion_complexity)
        
        # Determine emotional granularity
        if nuance_count > 0 and complex_emotion_count > 1:
            emotional_granularity = "specific"
        elif complex_emotion_count > 0 or basic_emotion_count > 2:
            emotional_granularity = "moderate"
        else:
            emotional_granularity = "broad"
        
        # Identify dominant emotions mentioned
        dominant_emotions = []
        for emotion in self.emotion_categories["basic_emotions"] + self.emotion_categories["complex_emotions"][:10]:
            if emotion in text_lower:
                dominant_emotions.append(emotion)
        
        # Analyze emotion regulation style
        regulation_mentions = {}
        for style, strategies in self.regulation_strategies.items():
            count = sum(1 for strategy in strategies if strategy in text_lower)
            if count > 0:
                regulation_mentions[style] = count
        
        if regulation_mentions:
            emotion_regulation_style = max(regulation_mentions.keys(), key=regulation_mentions.get)
        else:
            emotion_regulation_style = "unclear"
        
        # Determine emotional awareness level
        awareness_indicators = ["feel", "emotion", "aware", "notice", "sense"]
        awareness_count = sum(1 for indicator in awareness_indicators if indicator in text_lower)
        
        if awareness_count > 3 and emotion_vocabulary_size > 3:
            emotional_awareness_level = "high"
        elif awareness_count > 1 and emotion_vocabulary_size > 1:
            emotional_awareness_level = "moderate"
        else:
            emotional_awareness_level = "developing"
        
        return EmotionalProfile(
            emotion_vocabulary_size=emotion_vocabulary_size,
            emotion_complexity=emotion_complexity,
            emotional_granularity=emotional_granularity,
            dominant_emotions=dominant_emotions[:5],  # Limit to top 5
            emotion_regulation_style=emotion_regulation_style,
            emotional_awareness_level=emotional_awareness_level
        )
    
    def _calculate_emotional_content_richness(self, text_lower: str) -> float:
        """Calculate how emotionally rich the text content is"""
        emotional_words = (self.emotion_categories["basic_emotions"] + 
                         self.emotion_categories["complex_emotions"] + 
                         self.emotion_categories["emotional_nuances"])
        
        emotion_mentions = sum(1 for word in emotional_words if word in text_lower)
        word_count = len(text_lower.split())
        
        if word_count > 0:
            emotional_density = emotion_mentions / word_count
            return min(0.2, emotional_density * 5)  # Scale and cap
        return 0.0
    
    def _analyze_domain_competencies(self, domain_data: Dict[str, Any], score: float, 
                                   evidence: List[str]) -> Tuple[List[str], List[str]]:
        """Analyze strengths and development areas for domain"""
        strengths = []
        development_areas = []
        
        competencies = domain_data.get("competencies", [])
        
        if score >= 0.7:
            strengths.extend(competencies[:2])  # Top competencies as strengths
        elif score >= 0.4:
            if competencies:
                strengths.append(competencies[0])  # One strength
                development_areas.extend(competencies[1:3])  # Areas to develop
        else:
            development_areas.extend(competencies[:3])  # Focus areas
        
        return strengths, development_areas
    
    def _identify_eq_strengths(self, domains: Dict[str, EQDomain], 
                             emotional_profile: EmotionalProfile) -> List[str]:
        """Identify overall EQ strengths"""
        strengths = []
        
        # Domain-based strengths
        strong_domains = [domain for domain in domains.values() if domain.score >= 0.7]
        for domain in strong_domains:
            strengths.append(f"Strong {domain.name.lower()} abilities")
        
        # Emotional profile strengths
        if emotional_profile.emotional_awareness_level == "high":
            strengths.append("High emotional self-awareness")
        
        if emotional_profile.emotion_complexity >= 0.7:
            strengths.append("Sophisticated understanding of emotional complexity")
        
        if emotional_profile.emotion_vocabulary_size >= 5:
            strengths.append("Rich emotional vocabulary and expression")
        
        return strengths[:4]  # Limit strengths
    
    def _identify_development_priorities(self, domains: Dict[str, EQDomain]) -> List[str]:
        """Identify priority areas for EQ development"""
        priorities = []
        
        # Find domains with lowest scores
        sorted_domains = sorted(domains.values(), key=lambda d: d.score)
        
        for domain in sorted_domains:
            if domain.score < 0.5:
                priorities.append(f"Develop {domain.name.lower()} skills")
        
        # Specific developmental focuses
        if domains["managing_emotions"].score < 0.6:
            priorities.append("Focus on emotional self-regulation strategies")
        
        if domains["perceiving_emotions"].score < 0.6:
            priorities.append("Enhance emotional awareness and recognition")
        
        return priorities[:3]  # Limit priorities
    
    def _generate_interpersonal_insights(self, domains: Dict[str, EQDomain], 
                                       emotional_profile: EmotionalProfile) -> List[str]:
        """Generate insights about interpersonal emotional intelligence"""
        insights = []
        
        perceiving = domains["perceiving_emotions"].score
        managing = domains["managing_emotions"].score
        
        if perceiving >= 0.7 and managing >= 0.7:
            insights.append("Strong interpersonal skills - can read others and influence emotions positively")
        elif perceiving >= 0.6:
            insights.append("Good at reading emotional cues but may need to develop influence skills")
        elif managing >= 0.6:
            insights.append("Can manage emotions well but may miss subtle emotional signals from others")
        
        if emotional_profile.emotion_regulation_style == "social":
            insights.append("Tends to seek social support for emotional regulation")
        
        return insights
    
    def _generate_leadership_implications(self, domains: Dict[str, EQDomain]) -> List[str]:
        """Generate leadership-related EQ implications"""
        implications = []
        
        managing_score = domains["managing_emotions"].score
        using_score = domains["using_emotions"].score
        perceiving_score = domains["perceiving_emotions"].score
        
        if managing_score >= 0.7 and using_score >= 0.7:
            implications.append("Strong leadership potential - can inspire and manage team emotions")
        
        if perceiving_score >= 0.7:
            implications.append("Likely effective at reading team dynamics and morale")
        
        if all(domain.score >= 0.6 for domain in domains.values()):
            implications.append("Well-rounded emotional leadership capabilities")
        elif managing_score < 0.5:
            implications.append("May struggle with team emotional regulation and conflict resolution")
        
        return implications
    
    def _generate_recommendations(self, domains: Dict[str, EQDomain], 
                                development_priorities: List[str]) -> List[str]:
        """Generate personalized EQ development recommendations"""
        recommendations = []
        
        # Domain-specific recommendations
        if domains["perceiving_emotions"].score < 0.6:
            recommendations.append("Practice mindfulness and emotional check-ins to increase awareness")
        
        if domains["using_emotions"].score < 0.6:
            recommendations.append("Learn to channel emotions productively for motivation and decision-making")
        
        if domains["understanding_emotions"].score < 0.6:
            recommendations.append("Study emotional patterns and develop emotional vocabulary")
        
        if domains["managing_emotions"].score < 0.6:
            recommendations.append("Develop specific emotion regulation strategies and stress management techniques")
        
        # General recommendations
        if len(development_priorities) > 2:
            recommendations.append("Consider EQ coaching or training to accelerate development")
        
        recommendations.append("Practice active listening and empathy in daily interactions")
        
        return recommendations[:5]  # Limit recommendations
    
    async def initialize(self) -> bool:
        """Initialize the Emotional Intelligence Assessment agent"""
        try:
            # No external models needed for basic assessment
            return True
        except Exception as e:
            return False
    
    async def validate_input(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate input data for emotional intelligence assessment"""
        text = data.get("text", "")
        if not text or not isinstance(text, str):
            return False, "Text input is required and must be a string"
        if len(text.strip()) < 40:
            return False, "Text must be at least 40 characters for meaningful EQ assessment"
        if len(text) > 10000:
            return False, "Text exceeds maximum length of 10,000 characters"
        return True, None
    
    def get_capabilities(self) -> List[AgentCapability]:
        """Return list of agent capabilities"""
        from ...core.base_agent import AgentCapability
        return [AgentCapability(name=cap, description=f"Emotional intelligence: {cap}") for cap in self.capabilities]
    
    def _serialize_assessment(self, assessment: EQAssessment) -> Dict[str, Any]:
        """Serialize EQ assessment for JSON response"""
        return {
            "domains": {
                key: {
                    "name": domain.name,
                    "description": domain.description,
                    "score": domain.score,
                    "percentile": domain.percentile,
                    "competency_level": domain.competency_level,
                    "evidence": domain.evidence,
                    "strengths": domain.strengths,
                    "development_areas": domain.development_areas
                }
                for key, domain in assessment.domains.items()
            },
            "emotional_profile": {
                "emotion_vocabulary_size": assessment.emotional_profile.emotion_vocabulary_size,
                "emotion_complexity": assessment.emotional_profile.emotion_complexity,
                "emotional_granularity": assessment.emotional_profile.emotional_granularity,
                "dominant_emotions": assessment.emotional_profile.dominant_emotions,
                "emotion_regulation_style": assessment.emotional_profile.emotion_regulation_style,
                "emotional_awareness_level": assessment.emotional_profile.emotional_awareness_level
            },
            "interpersonal_insights": assessment.interpersonal_insights,
            "leadership_implications": assessment.leadership_implications
        }
    
    def _generate_summary(self, assessment: EQAssessment) -> str:
        """Generate concise summary of EQ assessment"""
        overall_level = ""
        if assessment.overall_eq_score >= 0.8:
            overall_level = "High EQ"
        elif assessment.overall_eq_score >= 0.6:
            overall_level = "Moderate-High EQ"
        elif assessment.overall_eq_score >= 0.4:
            overall_level = "Moderate EQ"
        else:
            overall_level = "Developing EQ"
        
        top_domain = max(assessment.domains.values(), key=lambda d: d.score)
        
        return f"{overall_level} (Score: {assessment.overall_eq_score:.2f}) | Strongest: {top_domain.name}"


# Helper function for external usage
async def assess_emotional_intelligence(text: str, agent_id: str = "emotional_intelligence_agent") -> Dict[str, Any]:
    """Convenience function for emotional intelligence assessment"""
    agent = EmotionalIntelligenceAgent(agent_id)
    message = AgentMessage(
        message_id="eq_assessment",
        agent_id=agent_id,
        content={"text": text}
    )
    
    response = await agent.process(message)
    return response.content