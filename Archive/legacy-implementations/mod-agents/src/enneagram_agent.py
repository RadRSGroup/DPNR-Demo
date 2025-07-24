"""Enneagram Assessment Agent - Specialized in 9-type personality assessment"""
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import asyncio
import logging
import re
from dataclasses import dataclass

from agent_library.core.base_agent import (
    ChainableAgent, AgentMessage, AgentResponse, 
    AgentCapability, AgentStatus
)


@dataclass
class EnneagramType:
    """Enneagram type definition with patterns and characteristics"""
    number: int
    name: str
    core_motivation: str
    basic_fear: str
    basic_desire: str
    patterns: List[str]
    behavioral_indicators: List[str]
    stress_patterns: List[str]
    growth_patterns: List[str]


@dataclass 
class PersonalityScore:
    """Personality trait score with evidence"""
    trait: str
    score: float
    confidence: float
    evidence: List[str]
    behavioral_indicators: List[str] = None


class EnneagramAgent(ChainableAgent):
    """Agent specialized in Enneagram personality assessment"""
    
    def __init__(self, agent_id: str = "enneagram_agent", confidence_threshold: float = 0.75):
        super().__init__(agent_id, "Enneagram Assessment Agent", "1.0.0")
        self.confidence_threshold = confidence_threshold
        
        # Initialize Enneagram type definitions
        self._init_enneagram_types()
        
        # Define capabilities
        self._capabilities = [
            AgentCapability(
                name="assess_enneagram",
                description="Assess Enneagram personality type from text",
                input_schema={
                    "text": "string",
                    "context": "dict (optional)",
                    "nlp_features": "dict (optional)"
                },
                output_schema={
                    "primary_type": "int",
                    "secondary_type": "int",
                    "type_scores": "dict",
                    "confidence": "float",
                    "behavioral_evidence": "list",
                    "growth_recommendations": "list"
                },
                performance_sla={
                    "max_response_time": 3.0,  # seconds
                    "min_confidence": 0.75,
                    "max_text_length": 5000
                }
            ),
            AgentCapability(
                name="detailed_analysis",
                description="Detailed Enneagram analysis with facets",
                input_schema={
                    "text": "string",
                    "include_wings": "bool (optional, default=true)",
                    "include_instincts": "bool (optional, default=false)"
                },
                output_schema={
                    "detailed_assessment": "dict",
                    "wing_analysis": "dict",
                    "stress_security_patterns": "dict"
                },
                performance_sla={"max_response_time": 5.0}
            ),
            AgentCapability(
                name="compare_types",
                description="Compare likelihood of multiple types",
                input_schema={
                    "text": "string",
                    "candidate_types": "list[int] (optional)"
                },
                output_schema={"type_comparison": "dict"},
                performance_sla={"max_response_time": 2.0}
            )
        ]
    
    def _init_enneagram_types(self):
        """Initialize Enneagram type definitions"""
        self.enneagram_types = {
            1: EnneagramType(
                number=1,
                name="The Perfectionist",
                core_motivation="To be good, right, perfect, and improve everything",
                basic_fear="Being corrupt, defective, or wrong",
                basic_desire="To be good, perfect, and improve everything",
                patterns=["perfect", "correct", "should", "must", "proper", "right", "wrong", "improve", "better", "ideal"],
                behavioral_indicators=["critical", "detailed", "systematic", "principled", "responsible"],
                stress_patterns=["angry", "critical", "impatient", "resentful"],
                growth_patterns=["accepting", "serene", "wise", "objective"]
            ),
            2: EnneagramType(
                number=2,
                name="The Helper",
                core_motivation="To feel loved and needed",
                basic_fear="Being unloved or unwanted",
                basic_desire="To feel loved",
                patterns=["help", "care", "love", "need", "support", "others", "giving", "serve", "assist"],
                behavioral_indicators=["empathetic", "generous", "people-pleasing", "supportive"],
                stress_patterns=["manipulative", "possessive", "martyrdom"],
                growth_patterns=["self-caring", "emotionally honest", "unconditionally loving"]
            ),
            3: EnneagramType(
                number=3,
                name="The Achiever",
                core_motivation="To feel valuable and worthwhile",
                basic_fear="Being worthless without achievement",
                basic_desire="To feel valuable and worthwhile",
                patterns=["success", "achieve", "win", "goal", "efficient", "image", "best", "performance", "accomplish"],
                behavioral_indicators=["ambitious", "adaptable", "driven", "image-conscious"],
                stress_patterns=["deceptive", "narcissistic", "hostile"],
                growth_patterns=["authentic", "self-accepting", "charitable"]
            ),
            4: EnneagramType(
                number=4,
                name="The Individualist",
                core_motivation="To find themselves and their significance",
                basic_fear="Having no identity or personal significance",
                basic_desire="To find themselves and their significance",
                patterns=["unique", "special", "different", "deep", "missing", "authentic", "identity", "meaning"],
                behavioral_indicators=["expressive", "dramatic", "self-absorbed", "temperamental"],
                stress_patterns=["depressed", "alienated", "self-indulgent"],
                growth_patterns=["inspired", "creative", "able to renew self"]
            ),
            5: EnneagramType(
                number=5,
                name="The Investigator",
                core_motivation="To be capable and competent",
                basic_fear="Being useless, helpless, or incapable",
                basic_desire="To be competent and understanding",
                patterns=["understand", "knowledge", "private", "observe", "analyze", "think", "study", "research"],
                behavioral_indicators=["intense", "cerebral", "perceptive", "innovative", "secretive"],
                stress_patterns=["hyperactive", "scattered", "anxious"],
                growth_patterns=["visionary", "pioneering", "confident"]
            ),
            6: EnneagramType(
                number=6,
                name="The Loyalist",
                core_motivation="To have security and support",
                basic_fear="Being without support or guidance",
                basic_desire="To have security and support",
                patterns=["security", "safe", "trust", "loyal", "doubt", "authority", "responsible", "reliable"],
                behavioral_indicators=["engaging", "responsible", "anxious", "suspicious"],
                stress_patterns=["unpredictable", "defiant", "reactive"],
                growth_patterns=["self-reliant", "courageous", "positive"]
            ),
            7: EnneagramType(
                number=7,
                name="The Enthusiast",
                core_motivation="To maintain happiness and avoid pain",
                basic_fear="Being trapped in pain or deprivation",
                basic_desire="To be satisfied and content",
                patterns=["fun", "exciting", "options", "adventure", "positive", "avoid", "variety", "experience"],
                behavioral_indicators=["spontaneous", "versatile", "distractible", "scattered"],
                stress_patterns=["perfectionist", "critical", "impatient"],
                growth_patterns=["focused", "fascinated", "joyous"]
            ),
            8: EnneagramType(
                number=8,
                name="The Challenger",
                core_motivation="To be self-reliant and in control",
                basic_fear="Being controlled or vulnerable",
                basic_desire="To protect themselves and control their environment",
                patterns=["control", "power", "strong", "direct", "justice", "protect", "intensity", "challenge"],
                behavioral_indicators=["self-confident", "decisive", "confrontational"],
                stress_patterns=["secretive", "fearful", "withdrawn"],
                growth_patterns=["caring", "protective", "heroic"]
            ),
            9: EnneagramType(
                number=9,
                name="The Peacemaker",
                core_motivation="To maintain inner and outer peace",
                basic_fear="Loss of connection and fragmentation",
                basic_desire="To have inner and outer peace",
                patterns=["peace", "harmony", "conflict", "comfortable", "agree", "merge", "calm", "steady"],
                behavioral_indicators=["accepting", "trusting", "stable", "creative", "optimistic"],
                stress_patterns=["anxious", "worried", "scattered"],
                growth_patterns=["dynamic", "self-developing", "energetic"]
            )
        }
    
    async def initialize(self) -> bool:
        """Initialize the Enneagram assessment agent"""
        try:
            self.logger.info("Initializing Enneagram assessment agent...")
            # No external models needed for basic assessment
            self.logger.info("Enneagram agent initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Enneagram agent: {str(e)}")
            self.status = AgentStatus.ERROR
            return False
    
    async def process(self, message: AgentMessage) -> AgentResponse:
        """Process Enneagram assessment request"""
        start_time = datetime.utcnow()
        
        try:
            action = message.payload.get("action", "assess_enneagram")
            
            if action == "assess_enneagram":
                result = await self._assess_enneagram(
                    message.payload.get("text"),
                    message.payload.get("context", {}),
                    message.payload.get("nlp_features", {})
                )
            elif action == "detailed_analysis":
                result = await self._detailed_analysis(
                    message.payload.get("text"),
                    message.payload.get("include_wings", True),
                    message.payload.get("include_instincts", False)
                )
            elif action == "compare_types":
                result = await self._compare_types(
                    message.payload.get("text"),
                    message.payload.get("candidate_types", list(range(1, 10)))
                )
            else:
                raise ValueError(f"Unknown action: {action}")
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return AgentResponse(
                success=True,
                data=result,
                processing_time=processing_time,
                agent_id=self.agent_id,
                confidence=result.get("confidence", 0.8)
            )
            
        except Exception as e:
            self.logger.error(f"Enneagram assessment error: {str(e)}")
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return AgentResponse(
                success=False,
                error=str(e),
                processing_time=processing_time,
                agent_id=self.agent_id
            )
    
    async def _assess_enneagram(self, text: str, context: Dict[str, Any], nlp_features: Dict[str, Any]) -> Dict[str, Any]:
        """Perform Enneagram personality assessment"""
        text_lower = text.lower()
        type_scores = {}
        behavioral_evidence = {}
        
        # Analyze each Enneagram type
        for type_num, type_def in self.enneagram_types.items():
            score_data = await self._analyze_type_fit(text_lower, type_def, nlp_features)
            type_scores[type_num] = score_data
            
            if score_data["evidence"]:
                behavioral_evidence[type_num] = {
                    "patterns": score_data["evidence"],
                    "behavioral_indicators": score_data["behavioral_matches"],
                    "confidence": score_data["confidence"]
                }
        
        # Determine primary and secondary types
        sorted_types = sorted(type_scores.items(), key=lambda x: x[1]["score"], reverse=True)
        primary_type = sorted_types[0][0]
        secondary_type = sorted_types[1][0] if len(sorted_types) > 1 else None
        
        # Calculate overall confidence
        overall_confidence = self._calculate_overall_confidence(type_scores, text)
        
        # Generate growth recommendations
        growth_recommendations = self._generate_growth_recommendations(primary_type, secondary_type)
        
        return {
            "primary_type": primary_type,
            "secondary_type": secondary_type,
            "type_scores": {k: v["score"] for k, v in type_scores.items()},
            "detailed_scores": type_scores,
            "confidence": overall_confidence,
            "behavioral_evidence": behavioral_evidence,
            "growth_recommendations": growth_recommendations,
            "type_description": {
                "primary": {
                    "number": primary_type,
                    "name": self.enneagram_types[primary_type].name,
                    "core_motivation": self.enneagram_types[primary_type].core_motivation
                },
                "secondary": {
                    "number": secondary_type,
                    "name": self.enneagram_types[secondary_type].name if secondary_type else None,
                    "core_motivation": self.enneagram_types[secondary_type].core_motivation if secondary_type else None
                } if secondary_type else None
            }
        }
    
    async def _analyze_type_fit(self, text_lower: str, type_def: EnneagramType, nlp_features: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze how well text fits a specific Enneagram type"""
        # Pattern matching
        pattern_matches = []
        for pattern in type_def.patterns:
            if pattern in text_lower:
                pattern_matches.append(pattern)
        
        pattern_score = len(pattern_matches) / len(type_def.patterns) if type_def.patterns else 0
        
        # Behavioral indicator matching
        behavioral_matches = []
        for indicator in type_def.behavioral_indicators:
            if indicator in text_lower:
                behavioral_matches.append(indicator)
        
        behavioral_score = len(behavioral_matches) / len(type_def.behavioral_indicators) if type_def.behavioral_indicators else 0
        
        # Sentiment and emotion adjustment
        sentiment_adjustment = 0
        emotion_adjustment = 0
        
        if nlp_features:
            sentiment = nlp_features.get("sentiment", {})
            emotions = nlp_features.get("emotions", [])
            
            # Type-specific sentiment patterns
            if type_def.number == 7 and sentiment.get("polarity", 0) > 0.5:  # Enthusiast likes positive
                sentiment_adjustment = 0.1
            elif type_def.number == 4 and sentiment.get("polarity", 0) < -0.3:  # Individualist may express melancholy
                sentiment_adjustment = 0.1
            elif type_def.number == 6 and any(e.get("emotion") == "fear" for e in emotions):  # Loyalist may express anxiety
                emotion_adjustment = 0.1
        
        # Calculate composite score
        base_score = (pattern_score * 0.6) + (behavioral_score * 0.4)
        adjusted_score = min(base_score + sentiment_adjustment + emotion_adjustment, 1.0)
        
        # Calculate confidence based on evidence strength
        evidence_strength = len(pattern_matches) + len(behavioral_matches)
        confidence = min(evidence_strength / 10, 1.0)  # Scale based on total evidence
        
        return {
            "score": adjusted_score,
            "confidence": confidence,
            "evidence": pattern_matches,
            "behavioral_matches": behavioral_matches,
            "pattern_score": pattern_score,
            "behavioral_score": behavioral_score
        }
    
    def _calculate_overall_confidence(self, type_scores: Dict[int, Dict], text: str) -> float:
        """Calculate overall assessment confidence"""
        # Factors affecting confidence:
        # 1. Clarity of top type (difference between 1st and 2nd)
        # 2. Amount of evidence
        # 3. Text length and quality
        
        scores = [data["score"] for data in type_scores.values()]
        scores.sort(reverse=True)
        
        # Clear distinction between top types
        distinction = scores[0] - scores[1] if len(scores) > 1 else scores[0]
        
        # Amount of evidence
        total_evidence = sum(len(data["evidence"]) + len(data["behavioral_matches"]) 
                           for data in type_scores.values())
        evidence_factor = min(total_evidence / 20, 1.0)
        
        # Text quality (length and variety)
        words = text.split()
        text_quality = min(len(words) / 100, 1.0) * min(len(set(words)) / len(words), 1.0) if words else 0
        
        # Combine factors
        confidence = (distinction * 0.4) + (evidence_factor * 0.35) + (text_quality * 0.25)
        return min(confidence, 1.0)
    
    def _generate_growth_recommendations(self, primary_type: int, secondary_type: Optional[int]) -> List[str]:
        """Generate personalized growth recommendations"""
        recommendations = []
        
        primary_def = self.enneagram_types[primary_type]
        
        # Primary type recommendations
        recommendations.extend([
            f"Focus on developing: {', '.join(primary_def.growth_patterns[:2])}",
            f"Be aware of stress patterns: {', '.join(primary_def.stress_patterns[:2])}",
            f"Core growth area: {primary_def.basic_desire}"
        ])
        
        # Secondary type recommendations
        if secondary_type:
            secondary_def = self.enneagram_types[secondary_type]
            recommendations.append(f"Integrate positive aspects of Type {secondary_type}: {', '.join(secondary_def.growth_patterns[:1])}")
        
        return recommendations
    
    async def _detailed_analysis(self, text: str, include_wings: bool, include_instincts: bool) -> Dict[str, Any]:
        """Perform detailed Enneagram analysis with wings and instincts"""
        basic_assessment = await self._assess_enneagram(text, {}, {})
        primary_type = basic_assessment["primary_type"]
        
        result = {
            "basic_assessment": basic_assessment,
            "detailed_breakdown": await self._analyze_facets(text, primary_type)
        }
        
        if include_wings:
            result["wing_analysis"] = await self._analyze_wings(text, primary_type)
        
        if include_instincts:
            result["instinctual_variants"] = await self._analyze_instincts(text)
        
        return result
    
    async def _analyze_facets(self, text: str, primary_type: int) -> Dict[str, Any]:
        """Analyze specific facets of the primary type"""
        type_def = self.enneagram_types[primary_type]
        text_lower = text.lower()
        
        return {
            "core_motivation_evidence": [p for p in type_def.patterns if p in text_lower],
            "stress_indicators": [p for p in type_def.stress_patterns if p in text_lower],
            "growth_indicators": [p for p in type_def.growth_patterns if p in text_lower],
            "behavioral_strength": len([b for b in type_def.behavioral_indicators if b in text_lower]) / len(type_def.behavioral_indicators)
        }
    
    async def _analyze_wings(self, text: str, primary_type: int) -> Dict[str, Any]:
        """Analyze wing influences (adjacent types)"""
        # Wings are adjacent types (e.g., Type 5 has wings 4 and 6)
        wing1 = primary_type - 1 if primary_type > 1 else 9
        wing2 = primary_type + 1 if primary_type < 9 else 1
        
        wing1_score = await self._analyze_type_fit(text.lower(), self.enneagram_types[wing1], {})
        wing2_score = await self._analyze_type_fit(text.lower(), self.enneagram_types[wing2], {})
        
        return {
            f"wing_{wing1}": {
                "score": wing1_score["score"],
                "influence": "primary" if wing1_score["score"] > wing2_score["score"] else "secondary",
                "evidence": wing1_score["evidence"]
            },
            f"wing_{wing2}": {
                "score": wing2_score["score"],
                "influence": "primary" if wing2_score["score"] > wing1_score["score"] else "secondary",
                "evidence": wing2_score["evidence"]
            }
        }
    
    async def _analyze_instincts(self, text: str) -> Dict[str, Any]:
        """Analyze instinctual variants (self-preservation, social, sexual)"""
        text_lower = text.lower()
        
        instinct_patterns = {
            "self_preservation": ["safe", "secure", "comfort", "health", "resources", "survival"],
            "social": ["group", "community", "belonging", "status", "hierarchy", "network"],
            "sexual": ["intense", "connection", "attraction", "chemistry", "one-on-one", "energy"]
        }
        
        instinct_scores = {}
        for instinct, patterns in instinct_patterns.items():
            matches = [p for p in patterns if p in text_lower]
            score = len(matches) / len(patterns)
            instinct_scores[instinct] = {
                "score": score,
                "evidence": matches
            }
        
        return instinct_scores
    
    async def _compare_types(self, text: str, candidate_types: List[int]) -> Dict[str, Any]:
        """Compare likelihood of specified types"""
        text_lower = text.lower()
        comparisons = {}
        
        for type_num in candidate_types:
            if type_num in self.enneagram_types:
                score_data = await self._analyze_type_fit(text_lower, self.enneagram_types[type_num], {})
                comparisons[type_num] = {
                    "name": self.enneagram_types[type_num].name,
                    "score": score_data["score"],
                    "confidence": score_data["confidence"],
                    "evidence_count": len(score_data["evidence"]) + len(score_data["behavioral_matches"]),
                    "key_evidence": score_data["evidence"][:3]  # Top 3 pieces of evidence
                }
        
        # Rank by score
        ranked_types = sorted(comparisons.items(), key=lambda x: x[1]["score"], reverse=True)
        
        return {
            "type_comparison": comparisons,
            "ranked_likelihood": [(type_num, data["score"]) for type_num, data in ranked_types],
            "most_likely": ranked_types[0][0] if ranked_types else None,
            "confidence_differential": ranked_types[0][1]["score"] - ranked_types[1][1]["score"] if len(ranked_types) > 1 else 1.0
        }
    
    async def validate_input(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate input data"""
        action = data.get("action", "assess_enneagram")
        
        if action in ["assess_enneagram", "detailed_analysis", "compare_types"]:
            if not data.get("text"):
                return False, "Text is required for Enneagram assessment"
            if len(data["text"]) > 5000:
                return False, "Text exceeds maximum length of 5000 characters"
            if len(data["text"].split()) < 10:
                return False, "Text must contain at least 10 words for meaningful assessment"
        
        if action == "compare_types":
            candidate_types = data.get("candidate_types", [])
            if candidate_types and not all(isinstance(t, int) and 1 <= t <= 9 for t in candidate_types):
                return False, "Candidate types must be integers between 1 and 9"
        
        return True, None
    
    def get_capabilities(self) -> List[AgentCapability]:
        """Return agent capabilities"""
        return self._capabilities