"""
Cognitive Style Assessment Agent

Assesses individual differences in thinking patterns, information processing,
and decision-making styles based on established cognitive psychology research.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import asyncio
from dataclasses import dataclass
import re

from agent_library.core.base_agent import BaseAgent, AgentMessage, AgentResponse, AgentCapability, AgentStatus


@dataclass
class CognitiveDimension:
    """Represents a cognitive style dimension with score and interpretation"""
    name: str
    description: str
    dimension_pair: Tuple[str, str]  # (low_end, high_end)
    score: float  # 0.0 = strongly low_end, 1.0 = strongly high_end
    percentile: int
    style_category: str
    evidence: List[str]
    implications: List[str]


@dataclass
class ThinkingProfile:
    """Overall thinking and processing profile"""
    dominant_styles: List[str]
    thinking_complexity: float
    decision_making_approach: str
    information_processing_preference: str
    problem_solving_style: str
    learning_style_indicators: List[str]


@dataclass
class CognitiveAssessment:
    """Complete cognitive style assessment"""
    dimensions: Dict[str, CognitiveDimension]
    thinking_profile: ThinkingProfile
    cognitive_strengths: List[str]
    potential_blind_spots: List[str]
    optimal_environments: List[str]
    collaboration_insights: List[str]
    development_suggestions: List[str]
    overall_confidence: float


class CognitiveStyleAgent(BaseAgent):
    """
    Cognitive Style Assessment Agent
    
    Assesses key dimensions of cognitive style:
    1. Analytical vs Intuitive thinking
    2. Detail-oriented vs Big Picture focus  
    3. Sequential vs Random processing
    4. Concrete vs Abstract thinking
    5. Convergent vs Divergent thinking
    6. Field Independent vs Field Dependent
    """
    
    def __init__(self, agent_id: str = "cognitive_style_agent"):
        super().__init__(agent_id, "Cognitive Style Assessment Agent", "1.0.0")
        self.capabilities = [
            "cognitive_style_assessment",
            "thinking_pattern_analysis",
            "decision_making_style",
            "information_processing_preferences",
            "learning_style_indicators",
            "cognitive_strengths_identification"
        ]
        
        # Cognitive Style Dimensions
        self.cognitive_dimensions = {
            "analytical_intuitive": {
                "name": "Analytical-Intuitive Thinking",
                "description": "Preference for systematic analysis vs holistic intuition",
                "dimension_pair": ("Analytical", "Intuitive"),
                "analytical_indicators": {
                    "keywords": ["analyze", "logical", "systematic", "step by step", "methodical",
                               "rational", "evidence", "data", "facts", "proof", "reason"],
                    "phrases": ["step by step", "break down", "analyze this", "logical approach",
                              "systematic way", "evidence shows", "data indicates"],
                    "patterns": ["because", "therefore", "consequently", "as a result", "given that"]
                },
                "intuitive_indicators": {
                    "keywords": ["feel", "sense", "intuition", "gut", "instinct", "hunch",
                               "impression", "vibe", "overall", "holistic", "naturally"],
                    "phrases": ["gut feeling", "sense that", "feels right", "instinctively",
                              "naturally drawn", "overall impression", "intuitively"],
                    "patterns": ["something tells me", "I have a feeling", "it seems", "appears to be"]
                }
            },
            "detail_big_picture": {
                "name": "Detail-Big Picture Orientation",
                "description": "Focus on specifics and details vs overall patterns and concepts",
                "dimension_pair": ("Detail-Oriented", "Big Picture"),
                "detail_indicators": {
                    "keywords": ["detail", "specific", "precise", "exact", "particular", "accurate",
                               "careful", "thorough", "meticulous", "fine-tuned"],
                    "phrases": ["pay attention to", "focus on details", "specifically", "in particular",
                              "precisely", "exactly", "carefully consider"],
                    "patterns": ["first", "second", "third", "next", "then", "finally"]
                },
                "big_picture_indicators": {
                    "keywords": ["overall", "general", "concept", "idea", "vision", "strategy",
                               "broad", "perspective", "framework", "pattern", "theme"],
                    "phrases": ["big picture", "overall view", "general idea", "broad perspective",
                              "main concept", "strategic view", "larger context"],
                    "patterns": ["in general", "overall", "fundamentally", "essentially", "basically"]
                }
            },
            "sequential_random": {
                "name": "Sequential-Random Processing",
                "description": "Preference for linear, ordered thinking vs non-linear, flexible processing",
                "dimension_pair": ("Sequential", "Random"),
                "sequential_indicators": {
                    "keywords": ["order", "sequence", "plan", "organize", "structure", "schedule",
                               "systematic", "methodical", "linear", "step", "process"],
                    "phrases": ["in order", "step by step", "one by one", "systematically",
                              "organized approach", "planned way", "structured process"],
                    "patterns": ["first", "then", "next", "after that", "finally", "in conclusion"]
                },
                "random_indicators": {
                    "keywords": ["spontaneous", "flexible", "adaptable", "creative", "innovative",
                               "jump", "shift", "change", "variety", "different"],
                    "phrases": ["change direction", "different approach", "mix things up",
                              "spontaneously", "as it comes", "go with flow"],
                    "patterns": ["suddenly", "meanwhile", "by the way", "speaking of", "that reminds me"]
                }
            },
            "concrete_abstract": {
                "name": "Concrete-Abstract Thinking",
                "description": "Preference for tangible, practical concepts vs theoretical, conceptual ideas",
                "dimension_pair": ("Concrete", "Abstract"),
                "concrete_indicators": {
                    "keywords": ["practical", "real", "actual", "tangible", "hands-on", "specific",
                               "example", "experience", "physical", "concrete", "application"],
                    "phrases": ["real world", "practical application", "hands-on experience",
                              "concrete example", "actual situation", "tangible results"],
                    "patterns": ["for example", "such as", "like when", "in practice", "actually"]
                },
                "abstract_indicators": {
                    "keywords": ["theoretical", "conceptual", "philosophical", "idea", "principle",
                               "theory", "concept", "model", "framework", "notion"],
                    "phrases": ["in theory", "conceptually speaking", "philosophical perspective",
                              "abstract idea", "theoretical framework", "underlying principle"],
                    "patterns": ["what if", "suppose", "imagine", "theoretically", "conceptually"]
                }
            },
            "convergent_divergent": {
                "name": "Convergent-Divergent Thinking",
                "description": "Preference for finding single correct answers vs generating multiple possibilities",
                "dimension_pair": ("Convergent", "Divergent"),
                "convergent_indicators": {
                    "keywords": ["solution", "answer", "correct", "right", "best", "optimal",
                               "efficient", "focused", "targeted", "precise", "definitive"],
                    "phrases": ["right answer", "best solution", "correct approach", "most efficient",
                              "focused on", "zero in on", "pinpoint"],
                    "patterns": ["the answer is", "the solution", "the best way", "clearly", "obviously"]
                },
                "divergent_indicators": {
                    "keywords": ["possibilities", "alternatives", "options", "creative", "innovative",
                               "multiple", "various", "different", "explore", "brainstorm"],
                    "phrases": ["multiple ways", "different approaches", "various options",
                              "creative solutions", "alternative methods", "explore possibilities"],
                    "patterns": ["or", "alternatively", "another way", "what about", "could also"]
                }
            },
            "field_independent_dependent": {
                "name": "Field Independence-Dependence",
                "description": "Ability to separate information from context vs reliance on environmental cues",
                "dimension_pair": ("Field Independent", "Field Dependent"),
                "independent_indicators": {
                    "keywords": ["independent", "separate", "isolate", "extract", "individual",
                               "standalone", "objective", "detached", "analytical"],
                    "phrases": ["on its own", "separate from", "independent of", "isolated from",
                              "objectively speaking", "detached analysis"],
                    "patterns": ["regardless of", "independent of", "separate from", "in isolation"]
                },
                "dependent_indicators": {
                    "keywords": ["context", "environment", "situation", "surrounding", "connected",
                               "related", "influenced", "dependent", "holistic"],
                    "phrases": ["in context", "depends on", "influenced by", "connected to",
                              "considering the situation", "given the environment"],
                    "patterns": ["depending on", "in relation to", "considering", "given that"]
                }
            }
        }
        
        # Decision-making style indicators
        self.decision_styles = {
            "systematic": ["plan", "analyze", "consider", "evaluate", "compare", "systematic"],
            "intuitive": ["feel", "sense", "gut", "instinct", "naturally", "spontaneous"],
            "collaborative": ["discuss", "consult", "ask others", "team", "together", "input"],
            "independent": ["decide myself", "own decision", "independently", "alone", "personal"]
        }
        
        # Problem-solving approaches
        self.problem_solving_styles = {
            "methodical": ["step by step", "systematic", "methodical", "organized", "structured"],
            "creative": ["creative", "innovative", "think outside", "brainstorm", "imagine"],
            "practical": ["practical", "realistic", "feasible", "workable", "doable"],
            "experimental": ["try", "test", "experiment", "trial", "explore"]
        }
    
    async def process(self, message: AgentMessage) -> AgentResponse:
        """Process text for cognitive style assessment"""
        try:
            text = message.content.get("text", "")
            if not text or len(text.strip()) < 50:
                return AgentResponse(
                    agent_id=self.agent_id,
                    content={"error": "Insufficient text for cognitive style assessment (minimum 50 characters)"},
                    confidence=0.0
                )
            
            # Perform cognitive style assessment
            assessment = await self._assess_cognitive_style(text)
            
            result = {
                "cognitive_profile": self._serialize_assessment(assessment),
                "thinking_style_summary": self._generate_style_summary(assessment),
                "strengths": assessment.cognitive_strengths,
                "development_suggestions": assessment.development_suggestions,
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
                content={"error": f"Cognitive style assessment failed: {str(e)}"},
                confidence=0.0
            )
    
    async def _assess_cognitive_style(self, text: str) -> CognitiveAssessment:
        """Perform comprehensive cognitive style assessment"""
        text_lower = text.lower()
        words = text.split()
        
        # Assess each cognitive dimension
        dimensions = {}
        for dimension_key, dimension_data in self.cognitive_dimensions.items():
            dimension_assessment = await self._assess_cognitive_dimension(
                dimension_key, dimension_data, text_lower, words
            )
            dimensions[dimension_key] = dimension_assessment
        
        # Analyze thinking profile
        thinking_profile = self._analyze_thinking_profile(text_lower, words, dimensions)
        
        # Generate insights and recommendations
        cognitive_strengths = self._identify_cognitive_strengths(dimensions, thinking_profile)
        potential_blind_spots = self._identify_blind_spots(dimensions)
        optimal_environments = self._suggest_optimal_environments(dimensions, thinking_profile)
        collaboration_insights = self._generate_collaboration_insights(dimensions)
        development_suggestions = self._generate_development_suggestions(dimensions, potential_blind_spots)
        
        # Calculate overall confidence
        dimension_scores = [abs(d.score - 0.5) * 2 for d in dimensions.values()]  # Distance from neutral
        text_complexity = self._assess_text_complexity(text_lower, words)
        overall_confidence = min(0.95, np.mean(dimension_scores) * 0.7 + text_complexity * 0.3)
        
        return CognitiveAssessment(
            dimensions=dimensions,
            thinking_profile=thinking_profile,
            cognitive_strengths=cognitive_strengths,
            potential_blind_spots=potential_blind_spots,
            optimal_environments=optimal_environments,
            collaboration_insights=collaboration_insights,
            development_suggestions=development_suggestions,
            overall_confidence=overall_confidence
        )
    
    async def _assess_cognitive_dimension(self, dimension_key: str, dimension_data: Dict[str, Any],
                                        text_lower: str, words: List[str]) -> CognitiveDimension:
        """Assess a single cognitive dimension"""
        
        # Get the two ends of the dimension
        if dimension_key == "analytical_intuitive":
            low_end_key, high_end_key = "analytical_indicators", "intuitive_indicators"
        elif dimension_key == "detail_big_picture":
            low_end_key, high_end_key = "detail_indicators", "big_picture_indicators"
        elif dimension_key == "sequential_random":
            low_end_key, high_end_key = "sequential_indicators", "random_indicators"
        elif dimension_key == "concrete_abstract":
            low_end_key, high_end_key = "concrete_indicators", "abstract_indicators"
        elif dimension_key == "convergent_divergent":
            low_end_key, high_end_key = "convergent_indicators", "divergent_indicators"
        elif dimension_key == "field_independent_dependent":
            low_end_key, high_end_key = "independent_indicators", "dependent_indicators"
        
        # Score both ends
        low_score = self._score_cognitive_indicators(dimension_data[low_end_key], text_lower, words)
        high_score = self._score_cognitive_indicators(dimension_data[high_end_key], text_lower, words)
        
        # Calculate dimension score (0.0 = strongly low end, 1.0 = strongly high end)
        total_score = low_score + high_score
        if total_score > 0:
            dimension_score = high_score / total_score
        else:
            dimension_score = 0.5  # Neutral if no indicators found
        
        # Collect evidence
        evidence = []
        if low_score > 0:
            evidence.extend(self._get_evidence(dimension_data[low_end_key], text_lower, 
                                             dimension_data["dimension_pair"][0]))
        if high_score > 0:
            evidence.extend(self._get_evidence(dimension_data[high_end_key], text_lower,
                                             dimension_data["dimension_pair"][1]))
        
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
        
        # Generate implications
        implications = self._generate_dimension_implications(dimension_key, dimension_score, style_category)
        
        return CognitiveDimension(
            name=dimension_data["name"],
            description=dimension_data["description"],
            dimension_pair=dimension_data["dimension_pair"],
            score=dimension_score,
            percentile=int(dimension_score * 100),
            style_category=style_category,
            evidence=evidence[:3],  # Limit evidence
            implications=implications
        )
    
    def _score_cognitive_indicators(self, indicators: Dict[str, List[str]], 
                                  text_lower: str, words: List[str]) -> float:
        """Score cognitive indicators for one end of a dimension"""
        score = 0.0
        
        # Keyword matching
        for keyword in indicators.get("keywords", []):
            if keyword in text_lower:
                score += 0.1
        
        # Phrase matching (higher weight)
        for phrase in indicators.get("phrases", []):
            if phrase in text_lower:
                score += 0.15
        
        # Pattern matching (linguistic patterns)
        for pattern in indicators.get("patterns", []):
            if pattern in text_lower:
                score += 0.1
        
        return score
    
    def _get_evidence(self, indicators: Dict[str, List[str]], text_lower: str, style_name: str) -> List[str]:
        """Get evidence for cognitive style indicators"""
        evidence = []
        
        # Check keywords
        for keyword in indicators.get("keywords", []):
            if keyword in text_lower and len(evidence) < 2:
                evidence.append(f"{style_name} style: uses '{keyword}'")
        
        # Check phrases
        for phrase in indicators.get("phrases", []):
            if phrase in text_lower and len(evidence) < 2:
                evidence.append(f"{style_name} style: expresses '{phrase}'")
        
        return evidence
    
    def _analyze_thinking_profile(self, text_lower: str, words: List[str], 
                                dimensions: Dict[str, CognitiveDimension]) -> ThinkingProfile:
        """Analyze overall thinking profile"""
        
        # Identify dominant styles
        dominant_styles = []
        for dimension in dimensions.values():
            if "Strong" in dimension.style_category:
                dominant_styles.append(dimension.style_category)
        
        # Calculate thinking complexity
        complexity_indicators = [
            "complex", "complicated", "nuanced", "multifaceted", "sophisticated",
            "intricate", "elaborate", "detailed", "comprehensive"
        ]
        complexity_count = sum(1 for indicator in complexity_indicators if indicator in text_lower)
        thinking_complexity = min(1.0, complexity_count * 0.2)
        
        # Determine decision-making approach
        decision_scores = {}
        for style, keywords in self.decision_styles.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                decision_scores[style] = score
        
        if decision_scores:
            decision_making_approach = max(decision_scores.keys(), key=decision_scores.get)
        else:
            decision_making_approach = "unclear"
        
        # Determine information processing preference
        if dimensions["detail_big_picture"].score <= 0.4:
            processing_preference = "detail-focused"
        elif dimensions["detail_big_picture"].score >= 0.6:
            processing_preference = "pattern-focused"
        else:
            processing_preference = "balanced"
        
        # Determine problem-solving style
        solving_scores = {}
        for style, keywords in self.problem_solving_styles.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                solving_scores[style] = score
        
        if solving_scores:
            problem_solving_style = max(solving_scores.keys(), key=solving_scores.get)
        else:
            problem_solving_style = "adaptive"
        
        # Learning style indicators
        learning_indicators = []
        if dimensions["sequential_random"].score <= 0.4:
            learning_indicators.append("structured learning")
        if dimensions["concrete_abstract"].score <= 0.4:
            learning_indicators.append("practical application")
        if dimensions["analytical_intuitive"].score <= 0.4:
            learning_indicators.append("logical progression")
        if dimensions["convergent_divergent"].score >= 0.6:
            learning_indicators.append("exploratory learning")
        
        return ThinkingProfile(
            dominant_styles=dominant_styles,
            thinking_complexity=thinking_complexity,
            decision_making_approach=decision_making_approach,
            information_processing_preference=processing_preference,
            problem_solving_style=problem_solving_style,
            learning_style_indicators=learning_indicators
        )
    
    def _generate_dimension_implications(self, dimension_key: str, score: float, style_category: str) -> List[str]:
        """Generate implications for each cognitive dimension"""
        implications = []
        
        if dimension_key == "analytical_intuitive":
            if score <= 0.4:  # Analytical
                implications.extend([
                    "Prefers systematic analysis and logical reasoning",
                    "Values evidence-based decision making"
                ])
            elif score >= 0.6:  # Intuitive
                implications.extend([
                    "Relies on holistic understanding and gut feelings",
                    "Quick to see patterns and connections"
                ])
        
        elif dimension_key == "detail_big_picture":
            if score <= 0.4:  # Detail-oriented
                implications.extend([
                    "Excels at careful, thorough analysis",
                    "May need help seeing broader implications"
                ])
            elif score >= 0.6:  # Big picture
                implications.extend([
                    "Strong strategic and conceptual thinking",
                    "May overlook important details"
                ])
        
        elif dimension_key == "sequential_random":
            if score <= 0.4:  # Sequential
                implications.extend([
                    "Works best with structured, organized approaches",
                    "Prefers step-by-step processes"
                ])
            elif score >= 0.6:  # Random
                implications.extend([
                    "Thrives with flexibility and variety",
                    "May struggle with rigid structures"
                ])
        
        elif dimension_key == "concrete_abstract":
            if score <= 0.4:  # Concrete
                implications.extend([
                    "Prefers practical, real-world applications",
                    "Values tangible examples and experiences"
                ])
            elif score >= 0.6:  # Abstract
                implications.extend([
                    "Comfortable with theoretical concepts",
                    "Enjoys exploring ideas and possibilities"
                ])
        
        elif dimension_key == "convergent_divergent":
            if score <= 0.4:  # Convergent
                implications.extend([
                    "Focused on finding optimal solutions",
                    "Efficient at narrowing down options"
                ])
            elif score >= 0.6:  # Divergent
                implications.extend([
                    "Generates multiple creative alternatives",
                    "Excels at brainstorming and innovation"
                ])
        
        elif dimension_key == "field_independent_dependent":
            if score <= 0.4:  # Independent
                implications.extend([
                    "Can analyze information objectively",
                    "Less influenced by contextual factors"
                ])
            elif score >= 0.6:  # Dependent
                implications.extend([
                    "Considers context and environmental factors",
                    "Values holistic understanding"
                ])
        
        return implications
    
    def _assess_text_complexity(self, text_lower: str, words: List[str]) -> float:
        """Assess complexity of the text content"""
        if not words:
            return 0.0
        
        # Sentence complexity
        sentences = text_lower.split('.')
        avg_words_per_sentence = len(words) / max(len(sentences), 1)
        
        # Vocabulary complexity
        long_words = sum(1 for word in words if len(word) > 6)
        long_word_ratio = long_words / len(words)
        
        # Logical connectors
        connectors = ["however", "therefore", "consequently", "furthermore", "moreover", "nevertheless"]
        connector_count = sum(1 for connector in connectors if connector in text_lower)
        
        complexity = (avg_words_per_sentence / 20) * 0.4 + long_word_ratio * 0.4 + (connector_count / 10) * 0.2
        return min(1.0, complexity)
    
    def _identify_cognitive_strengths(self, dimensions: Dict[str, CognitiveDimension], 
                                    thinking_profile: ThinkingProfile) -> List[str]:
        """Identify cognitive strengths based on dimensions and profile"""
        strengths = []
        
        # Dimension-based strengths
        for dimension in dimensions.values():
            if "Strong" in dimension.style_category:
                if dimension.score <= 0.3:  # Strong low end
                    strengths.append(f"Strong {dimension.dimension_pair[0].lower()} thinking")
                elif dimension.score >= 0.7:  # Strong high end
                    strengths.append(f"Strong {dimension.dimension_pair[1].lower()} thinking")
        
        # Profile-based strengths
        if thinking_profile.thinking_complexity >= 0.6:
            strengths.append("Handles complex, nuanced thinking well")
        
        if thinking_profile.decision_making_approach == "systematic":
            strengths.append("Makes well-reasoned, systematic decisions")
        elif thinking_profile.decision_making_approach == "collaborative":
            strengths.append("Values input and collaborative decision-making")
        
        return strengths[:4]  # Limit strengths
    
    def _identify_blind_spots(self, dimensions: Dict[str, CognitiveDimension]) -> List[str]:
        """Identify potential cognitive blind spots"""
        blind_spots = []
        
        # Extreme scores may indicate blind spots
        for dimension in dimensions.values():
            if dimension.score <= 0.2:  # Very low
                opposite_style = dimension.dimension_pair[1]
                blind_spots.append(f"May undervalue {opposite_style.lower()} approaches")
            elif dimension.score >= 0.8:  # Very high
                opposite_style = dimension.dimension_pair[0]
                blind_spots.append(f"May overlook {opposite_style.lower()} considerations")
        
        return blind_spots[:3]  # Limit blind spots
    
    def _suggest_optimal_environments(self, dimensions: Dict[str, CognitiveDimension], 
                                    thinking_profile: ThinkingProfile) -> List[str]:
        """Suggest optimal work/learning environments"""
        environments = []
        
        # Based on sequential vs random
        if dimensions["sequential_random"].score <= 0.4:
            environments.append("Structured, organized environments with clear processes")
        elif dimensions["sequential_random"].score >= 0.6:
            environments.append("Flexible environments that allow for variety and spontaneity")
        
        # Based on detail vs big picture
        if dimensions["detail_big_picture"].score <= 0.4:
            environments.append("Roles requiring attention to detail and precision")
        elif dimensions["detail_big_picture"].score >= 0.6:
            environments.append("Strategic roles focusing on vision and conceptual work")
        
        # Based on decision-making style
        if thinking_profile.decision_making_approach == "collaborative":
            environments.append("Team-oriented environments with opportunities for input")
        elif thinking_profile.decision_making_approach == "independent":
            environments.append("Autonomous environments with independent decision-making")
        
        return environments
    
    def _generate_collaboration_insights(self, dimensions: Dict[str, CognitiveDimension]) -> List[str]:
        """Generate insights about collaboration style"""
        insights = []
        
        # Analytical vs Intuitive collaboration
        analytical_score = 1 - dimensions["analytical_intuitive"].score
        if analytical_score >= 0.6:
            insights.append("Brings logical analysis and systematic thinking to teams")
        elif dimensions["analytical_intuitive"].score >= 0.6:
            insights.append("Contributes intuitive insights and pattern recognition")
        
        # Convergent vs Divergent collaboration
        if dimensions["convergent_divergent"].score <= 0.4:
            insights.append("Helps teams focus and find optimal solutions")
        elif dimensions["convergent_divergent"].score >= 0.6:
            insights.append("Generates creative alternatives and innovative ideas")
        
        # Detail vs Big Picture collaboration
        if dimensions["detail_big_picture"].score <= 0.4:
            insights.append("Ensures thoroughness and attention to important details")
        elif dimensions["detail_big_picture"].score >= 0.6:
            insights.append("Provides strategic perspective and conceptual framework")
        
        return insights[:3]  # Limit insights
    
    def _generate_development_suggestions(self, dimensions: Dict[str, CognitiveDimension], 
                                        blind_spots: List[str]) -> List[str]:
        """Generate cognitive development suggestions"""
        suggestions = []
        
        # Address extreme scores
        for dimension in dimensions.values():
            if dimension.score <= 0.2:
                opposite_style = dimension.dimension_pair[1]
                suggestions.append(f"Practice {opposite_style.lower()} thinking approaches")
            elif dimension.score >= 0.8:
                opposite_style = dimension.dimension_pair[0]
                suggestions.append(f"Develop {opposite_style.lower()} skills for balance")
        
        # General development suggestions
        if len(blind_spots) > 2:
            suggestions.append("Seek diverse perspectives to challenge thinking patterns")
        
        suggestions.append("Practice metacognition - reflect on your thinking processes")
        
        return suggestions[:4]  # Limit suggestions
    
    async def initialize(self) -> bool:
        """Initialize the Cognitive Style Assessment agent"""
        try:
            # No external models needed for basic assessment
            return True
        except Exception as e:
            return False
    
    async def validate_input(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate input data for cognitive style assessment"""
        text = data.get("text", "")
        if not text or not isinstance(text, str):
            return False, "Text input is required and must be a string"
        if len(text.strip()) < 50:
            return False, "Text must be at least 50 characters for meaningful cognitive style assessment"
        if len(text) > 10000:
            return False, "Text exceeds maximum length of 10,000 characters"
        return True, None
    
    def get_capabilities(self) -> List[AgentCapability]:
        """Return list of agent capabilities"""
        from ...core.base_agent import AgentCapability
        return [AgentCapability(name=cap, description=f"Cognitive style: {cap}") for cap in self.capabilities]
    
    def _serialize_assessment(self, assessment: CognitiveAssessment) -> Dict[str, Any]:
        """Serialize cognitive assessment for JSON response"""
        return {
            "dimensions": {
                key: {
                    "name": dimension.name,
                    "description": dimension.description,
                    "dimension_pair": dimension.dimension_pair,
                    "score": dimension.score,
                    "percentile": dimension.percentile,
                    "style_category": dimension.style_category,
                    "evidence": dimension.evidence,
                    "implications": dimension.implications
                }
                for key, dimension in assessment.dimensions.items()
            },
            "thinking_profile": {
                "dominant_styles": assessment.thinking_profile.dominant_styles,
                "thinking_complexity": assessment.thinking_profile.thinking_complexity,
                "decision_making_approach": assessment.thinking_profile.decision_making_approach,
                "information_processing_preference": assessment.thinking_profile.information_processing_preference,
                "problem_solving_style": assessment.thinking_profile.problem_solving_style,
                "learning_style_indicators": assessment.thinking_profile.learning_style_indicators
            },
            "optimal_environments": assessment.optimal_environments,
            "collaboration_insights": assessment.collaboration_insights,
            "potential_blind_spots": assessment.potential_blind_spots
        }
    
    def _generate_style_summary(self, assessment: CognitiveAssessment) -> Dict[str, str]:
        """Generate a summary of cognitive styles"""
        return {
            dimension_key: dimension.style_category
            for dimension_key, dimension in assessment.dimensions.items()
        }
    
    def _generate_summary(self, assessment: CognitiveAssessment) -> str:
        """Generate concise summary of cognitive style"""
        dominant_styles = assessment.thinking_profile.dominant_styles
        
        if dominant_styles:
            style_text = ", ".join(dominant_styles[:2])  # Top 2 styles
        else:
            style_text = "Balanced cognitive approach"
        
        complexity_level = "High" if assessment.thinking_profile.thinking_complexity >= 0.6 else "Moderate"
        
        return f"Cognitive Style: {style_text} | Complexity: {complexity_level} | Decision Style: {assessment.thinking_profile.decision_making_approach.title()}"


# Helper function for external usage
async def assess_cognitive_style(text: str, agent_id: str = "cognitive_style_agent") -> Dict[str, Any]:
    """Convenience function for cognitive style assessment"""
    agent = CognitiveStyleAgent(agent_id)
    message = AgentMessage(
        message_id="cognitive_style_assessment",
        agent_id=agent_id,
        content={"text": text}
    )
    
    response = await agent.process(message)
    return response.content