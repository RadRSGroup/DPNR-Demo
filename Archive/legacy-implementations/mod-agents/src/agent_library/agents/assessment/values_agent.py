"""
Values Assessment Agent

Implements Schwartz's Theory of Basic Human Values for personality assessment.
Assesses 10 universal values organized into 4 higher-order dimensions.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import asyncio
from dataclasses import dataclass

from ...core.base_agent import BaseAgent, AgentMessage, AgentResponse, AgentCapability, AgentStatus


@dataclass
class ValueProfile:
    """Represents a single value with score and evidence"""
    name: str
    description: str
    score: float
    percentile: int
    importance_level: str
    evidence: List[str]
    motivational_goal: str


@dataclass
class ValuesDimension:
    """Higher-order value dimension grouping related values"""
    name: str
    description: str
    values: List[str]
    dimension_score: float
    dominant_value: str


@dataclass
class ValuesAssessment:
    """Complete values assessment profile"""
    individual_values: Dict[str, ValueProfile]
    dimensions: Dict[str, ValuesDimension]
    value_priorities: List[Tuple[str, float]]
    value_conflicts: List[Tuple[str, str, str]]  # value1, value2, explanation
    cultural_adaptation: Dict[str, Any]
    motivational_insights: List[str]
    recommendations: List[str]
    overall_confidence: float


class ValuesAgent(BaseAgent):
    """
    Schwartz Values Assessment Agent
    
    Assesses 10 universal human values:
    - Self-Direction, Stimulation, Hedonism, Achievement, Power
    - Security, Conformity, Tradition, Benevolence, Universalism
    
    Organized into 4 higher-order dimensions:
    - Openness to Change vs Conservation
    - Self-Enhancement vs Self-Transcendence
    """
    
    def __init__(self, agent_id: str = "values_agent"):
        super().__init__(agent_id, "Values Assessment Agent", "1.0.0")
        self.capabilities = [
            "values_assessment",
            "motivational_analysis",
            "value_priority_ranking",
            "cultural_adaptation",
            "life_goal_insights"
        ]
        
        # Schwartz's 10 Universal Values
        self.values_framework = {
            "self_direction": {
                "name": "Self-Direction",
                "description": "Independent thought and action; choosing, creating, exploring",
                "motivational_goal": "Independent thought and action",
                "keywords": [
                    "independent", "creative", "freedom", "choice", "curious", "explore",
                    "authentic", "original", "self-reliant", "innovative", "autonomous",
                    "unique", "individual", "personal", "own way", "decide for myself"
                ],
                "phrases": [
                    "my own way", "be myself", "make my own", "creative solution",
                    "explore new", "independent thinking", "personal choice"
                ],
                "dimension": "openness_to_change"
            },
            "stimulation": {
                "name": "Stimulation",
                "description": "Excitement, novelty, and challenge in life",
                "motivational_goal": "Excitement and challenge",
                "keywords": [
                    "exciting", "adventure", "thrill", "challenge", "risk", "new",
                    "stimulating", "bold", "daring", "variety", "change", "novel",
                    "intense", "dynamic", "unexpected", "spontaneous"
                ],
                "phrases": [
                    "love adventure", "seek excitement", "take risks", "new challenges",
                    "never boring", "something different", "push limits"
                ],
                "dimension": "openness_to_change"
            },
            "hedonism": {
                "name": "Hedonism",
                "description": "Pleasure and sensuous gratification for oneself",
                "motivational_goal": "Pleasure and enjoyment",
                "keywords": [
                    "pleasure", "enjoy", "fun", "satisfy", "indulge", "comfort",
                    "luxury", "relax", "treat myself", "happiness", "gratification",
                    "feel good", "wonderful", "delightful", "pleasurable"
                ],
                "phrases": [
                    "enjoy life", "feel good", "treat myself", "pure pleasure",
                    "love luxury", "savor the moment", "good things in life"
                ],
                "dimension": "openness_to_change"
            },
            "achievement": {
                "name": "Achievement",
                "description": "Personal success through demonstrating competence",
                "motivational_goal": "Success and accomplishment",
                "keywords": [
                    "success", "achieve", "accomplish", "goal", "excel", "competent",
                    "ambitious", "capable", "effective", "influential", "successful",
                    "perform", "attain", "reach", "master", "expert"
                ],
                "phrases": [
                    "reach my goals", "be successful", "demonstrate competence",
                    "achieve excellence", "show what I can do", "prove myself"
                ],
                "dimension": "self_enhancement"
            },
            "power": {
                "name": "Power",
                "description": "Social status and prestige, control or dominance",
                "motivational_goal": "Status and control",
                "keywords": [
                    "power", "authority", "control", "influence", "status", "prestige",
                    "wealth", "dominance", "command", "leadership", "important",
                    "respect", "recognition", "position", "privilege"
                ],
                "phrases": [
                    "in control", "position of power", "high status", "social prestige",
                    "influential person", "command respect", "important position"
                ],
                "dimension": "self_enhancement"
            },
            "security": {
                "name": "Security",
                "description": "Safety, harmony, and stability of society and self",
                "motivational_goal": "Safety and stability",
                "keywords": [
                    "secure", "safe", "stable", "protect", "order", "clean",
                    "healthy", "family", "belong", "social order", "reliable",
                    "predictable", "consistent", "dependable", "certain"
                ],
                "phrases": [
                    "feel secure", "stay safe", "stable environment", "protect family",
                    "maintain order", "sense of belonging", "reliable support"
                ],
                "dimension": "conservation"
            },
            "conformity": {
                "name": "Conformity",
                "description": "Restraint of actions that might violate social expectations",
                "motivational_goal": "Social harmony and compliance",
                "keywords": [
                    "polite", "obedient", "dutiful", "responsible", "honor", "respect",
                    "traditional", "proper", "appropriate", "follow", "rules",
                    "expectations", "comply", "conform", "well-behaved"
                ],
                "phrases": [
                    "follow rules", "do what's expected", "respect authority",
                    "proper behavior", "social expectations", "honor traditions"
                ],
                "dimension": "conservation"
            },
            "tradition": {
                "name": "Tradition",
                "description": "Respect and commitment to cultural or religious customs",
                "motivational_goal": "Cultural and religious tradition",
                "keywords": [
                    "tradition", "culture", "custom", "heritage", "ancestors", "roots",
                    "religious", "spiritual", "ritual", "ceremony", "values",
                    "beliefs", "legacy", "history", "sacred", "reverence"
                ],
                "phrases": [
                    "cultural traditions", "honor ancestors", "religious beliefs",
                    "family heritage", "respect customs", "spiritual values"
                ],
                "dimension": "conservation"
            },
            "benevolence": {
                "name": "Benevolence",
                "description": "Preserving and enhancing welfare of close others",
                "motivational_goal": "Care for close others",
                "keywords": [
                    "helpful", "caring", "loyal", "honest", "responsible", "true",
                    "friendship", "love", "family", "forgive", "support", "kind",
                    "compassionate", "devoted", "trustworthy", "reliable friend"
                ],
                "phrases": [
                    "help others", "care for family", "true friendship", "be there for",
                    "support loved ones", "loyal to friends", "help those close to me"
                ],
                "dimension": "self_transcendence"
            },
            "universalism": {
                "name": "Universalism",
                "description": "Understanding, tolerance, and protection for all people and nature",
                "motivational_goal": "Welfare of all people and nature",
                "keywords": [
                    "justice", "equality", "peace", "tolerance", "wisdom", "unity",
                    "environment", "nature", "protect", "world", "humanity",
                    "social justice", "broad-minded", "understanding", "universal"
                ],
                "phrases": [
                    "social justice", "protect environment", "world peace",
                    "equal rights", "care for nature", "help humanity", "understand others"
                ],
                "dimension": "self_transcendence"
            }
        }
        
        # Higher-order dimensions
        self.dimensions = {
            "openness_to_change": {
                "name": "Openness to Change",
                "description": "Values emphasizing independence of thought and action, readiness for change",
                "values": ["self_direction", "stimulation", "hedonism"],
                "opposite": "conservation"
            },
            "conservation": {
                "name": "Conservation",
                "description": "Values emphasizing order, self-restriction, resistance to change",
                "values": ["security", "conformity", "tradition"],
                "opposite": "openness_to_change"
            },
            "self_enhancement": {
                "name": "Self-Enhancement", 
                "description": "Values emphasizing pursuit of own interests and success",
                "values": ["achievement", "power"],
                "opposite": "self_transcendence"
            },
            "self_transcendence": {
                "name": "Self-Transcendence",
                "description": "Values emphasizing acceptance of others and concern for their welfare",
                "values": ["benevolence", "universalism"],
                "opposite": "self_enhancement"
            }
        }
    
    async def process(self, message: AgentMessage) -> AgentResponse:
        """Process text for values assessment"""
        try:
            text = message.content.get("text", "")
            if not text or len(text.strip()) < 30:
                return AgentResponse(
                    agent_id=self.agent_id,
                    content={"error": "Insufficient text for values assessment (minimum 30 characters)"},
                    confidence=0.0
                )
            
            # Perform values assessment
            assessment = await self._assess_values(text)
            
            result = {
                "values_profile": self._serialize_assessment(assessment),
                "value_priorities": assessment.value_priorities,
                "motivational_insights": assessment.motivational_insights,
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
                content={"error": f"Values assessment failed: {str(e)}"},
                confidence=0.0
            )
    
    async def _assess_values(self, text: str) -> ValuesAssessment:
        """Perform comprehensive values assessment"""
        text_lower = text.lower()
        words = text.split()
        
        # Assess individual values
        individual_values = {}
        for value_key, value_data in self.values_framework.items():
            value_profile = await self._assess_single_value(value_key, value_data, text_lower, words)
            individual_values[value_key] = value_profile
        
        # Calculate dimension scores
        dimensions = self._calculate_dimensions(individual_values)
        
        # Rank value priorities
        value_priorities = self._rank_value_priorities(individual_values)
        
        # Identify value conflicts
        value_conflicts = self._identify_value_conflicts(individual_values, dimensions)
        
        # Generate insights and recommendations
        motivational_insights = self._generate_motivational_insights(individual_values, dimensions)
        recommendations = self._generate_recommendations(individual_values, value_conflicts)
        
        # Calculate overall confidence
        value_scores = [v.score for v in individual_values.values()]
        overall_confidence = min(0.95, np.mean(value_scores) + (len(text) / 2000) * 0.2)
        
        return ValuesAssessment(
            individual_values=individual_values,
            dimensions=dimensions,
            value_priorities=value_priorities,
            value_conflicts=value_conflicts,
            cultural_adaptation={},  # Could be expanded
            motivational_insights=motivational_insights,
            recommendations=recommendations,
            overall_confidence=overall_confidence
        )
    
    async def _assess_single_value(self, value_key: str, value_data: Dict[str, Any], 
                                 text_lower: str, words: List[str]) -> ValueProfile:
        """Assess a single value from text"""
        score = 0.0
        evidence = []
        
        # Keyword matching
        for keyword in value_data["keywords"]:
            if keyword in text_lower:
                score += 0.1
                evidence.append(f"Uses '{keyword}' (core {value_data['name']} value)")
                if len(evidence) >= 3:  # Limit keyword evidence
                    break
        
        # Phrase matching (higher weight)
        for phrase in value_data["phrases"]:
            if phrase in text_lower:
                score += 0.2
                evidence.append(f"Expresses '{phrase}' (strong {value_data['name']} indicator)")
        
        # Contextual analysis
        contextual_score = self._analyze_value_context(value_key, text_lower, words)
        score += contextual_score
        
        # Normalize score
        final_score = min(1.0, max(0.0, score))
        
        # Determine importance level
        if final_score >= 0.7:
            importance_level = "Very Important"
        elif final_score >= 0.5:
            importance_level = "Important"
        elif final_score >= 0.3:
            importance_level = "Moderately Important"
        else:
            importance_level = "Less Important"
        
        # Convert to percentile
        percentile = int(final_score * 100)
        
        return ValueProfile(
            name=value_data["name"],
            description=value_data["description"],
            score=final_score,
            percentile=percentile,
            importance_level=importance_level,
            evidence=evidence[:4],  # Limit evidence
            motivational_goal=value_data["motivational_goal"]
        )
    
    def _analyze_value_context(self, value_key: str, text_lower: str, words: List[str]) -> float:
        """Analyze contextual indicators for specific values"""
        contextual_score = 0.0
        
        if value_key == "self_direction":
            # Look for autonomy and creativity indicators
            if any(phrase in text_lower for phrase in ["my own", "independent", "creative approach"]):
                contextual_score += 0.15
            if "because" in text_lower:  # Self-justification
                contextual_score += 0.05
        
        elif value_key == "achievement":
            # Look for goal and success language
            goal_words = ["goal", "target", "objective", "aim", "strive"]
            goal_count = sum(text_lower.count(word) for word in goal_words)
            contextual_score += min(0.2, goal_count * 0.05)
        
        elif value_key == "benevolence":
            # Look for relationship and care language
            care_words = ["family", "friend", "help", "support", "care"]
            care_count = sum(text_lower.count(word) for word in care_words)
            contextual_score += min(0.15, care_count * 0.03)
        
        elif value_key == "universalism":
            # Look for broader concern indicators
            universal_words = ["everyone", "world", "humanity", "all people", "society"]
            universal_count = sum(text_lower.count(word) for word in universal_words)
            contextual_score += min(0.2, universal_count * 0.05)
        
        elif value_key == "security":
            # Look for safety and stability language
            security_words = ["safe", "secure", "stable", "protect", "certain"]
            security_count = sum(text_lower.count(word) for word in security_words)
            contextual_score += min(0.15, security_count * 0.03)
        
        elif value_key == "power":
            # Look for influence and status language
            power_words = ["lead", "control", "manage", "influence", "authority"]
            power_count = sum(text_lower.count(word) for word in power_words)
            contextual_score += min(0.15, power_count * 0.03)
        
        return contextual_score
    
    def _calculate_dimensions(self, individual_values: Dict[str, ValueProfile]) -> Dict[str, ValuesDimension]:
        """Calculate higher-order dimension scores"""
        dimensions = {}
        
        for dim_key, dim_data in self.dimensions.items():
            # Calculate average score for values in this dimension
            value_scores = [individual_values[value_key].score for value_key in dim_data["values"]]
            dimension_score = np.mean(value_scores)
            
            # Find dominant value in dimension
            dominant_value_key = max(dim_data["values"], 
                                   key=lambda v: individual_values[v].score)
            dominant_value = individual_values[dominant_value_key].name
            
            dimensions[dim_key] = ValuesDimension(
                name=dim_data["name"],
                description=dim_data["description"],
                values=dim_data["values"],
                dimension_score=dimension_score,
                dominant_value=dominant_value
            )
        
        return dimensions
    
    def _rank_value_priorities(self, individual_values: Dict[str, ValueProfile]) -> List[Tuple[str, float]]:
        """Rank values by importance/score"""
        return sorted(
            [(value.name, value.score) for value in individual_values.values()],
            key=lambda x: x[1],
            reverse=True
        )
    
    def _identify_value_conflicts(self, individual_values: Dict[str, ValueProfile], 
                                dimensions: Dict[str, ValuesDimension]) -> List[Tuple[str, str, str]]:
        """Identify potential value conflicts"""
        conflicts = []
        
        # Check opposing dimensions
        openness_score = dimensions["openness_to_change"].dimension_score
        conservation_score = dimensions["conservation"].dimension_score
        
        if abs(openness_score - conservation_score) < 0.2:
            conflicts.append((
                "Openness to Change",
                "Conservation", 
                "May experience tension between desire for change and need for stability"
            ))
        
        enhancement_score = dimensions["self_enhancement"].dimension_score
        transcendence_score = dimensions["self_transcendence"].dimension_score
        
        if abs(enhancement_score - transcendence_score) < 0.2:
            conflicts.append((
                "Self-Enhancement",
                "Self-Transcendence",
                "May struggle between personal success and concern for others"
            ))
        
        # Check specific value conflicts
        if (individual_values["achievement"].score > 0.6 and 
            individual_values["benevolence"].score > 0.6):
            conflicts.append((
                "Achievement",
                "Benevolence", 
                "May face challenges balancing personal success with helping others"
            ))
        
        if (individual_values["stimulation"].score > 0.6 and 
            individual_values["security"].score > 0.6):
            conflicts.append((
                "Stimulation",
                "Security",
                "May experience tension between desire for excitement and need for safety"
            ))
        
        return conflicts
    
    def _generate_motivational_insights(self, individual_values: Dict[str, ValueProfile], 
                                      dimensions: Dict[str, ValuesDimension]) -> List[str]:
        """Generate insights about motivational drivers"""
        insights = []
        
        # Top values insights
        top_values = sorted(individual_values.values(), key=lambda v: v.score, reverse=True)[:3]
        
        if top_values[0].score > 0.7:
            insights.append(f"Strongly motivated by {top_values[0].motivational_goal.lower()}")
        
        # Dimension insights
        dominant_dimension = max(dimensions.values(), key=lambda d: d.dimension_score)
        if dominant_dimension.dimension_score > 0.6:
            insights.append(f"Value orientation is primarily focused on {dominant_dimension.name.lower()}")
        
        # Specific patterns
        if individual_values["universalism"].score > 0.6 and individual_values["benevolence"].score > 0.6:
            insights.append("Shows strong prosocial orientation - cares for both close others and humanity broadly")
        
        if individual_values["achievement"].score > 0.6 and individual_values["power"].score > 0.6:
            insights.append("Highly ambitious with strong drive for success and influence")
        
        if individual_values["self_direction"].score > 0.6 and individual_values["stimulation"].score > 0.6:
            insights.append("Values autonomy and seeks novel, challenging experiences")
        
        return insights
    
    def _generate_recommendations(self, individual_values: Dict[str, ValueProfile], 
                                value_conflicts: List[Tuple[str, str, str]]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Conflict resolution recommendations
        for conflict in value_conflicts:
            recommendations.append(f"Consider strategies to balance {conflict[0]} and {conflict[1]} values")
        
        # Value development recommendations
        low_values = [v for v in individual_values.values() if v.score < 0.3]
        
        if any(v.name in ["Benevolence", "Universalism"] for v in low_values):
            recommendations.append("Consider developing empathy and concern for others' welfare")
        
        if any(v.name in ["Security", "Conformity"] for v in low_values):
            recommendations.append("Reflect on the importance of stability and social harmony")
        
        # Strength utilization
        high_values = [v for v in individual_values.values() if v.score > 0.7]
        
        if high_values:
            top_value = max(high_values, key=lambda v: v.score)
            recommendations.append(f"Leverage your strong {top_value.name} values in decision-making")
        
        # Career/life recommendations
        if individual_values["achievement"].score > 0.6:
            recommendations.append("Seek roles with clear goals and opportunities for advancement")
        
        if individual_values["self_direction"].score > 0.6:
            recommendations.append("Pursue activities that allow creative expression and autonomy")
        
        if individual_values["universalism"].score > 0.6:
            recommendations.append("Consider involvement in social causes or environmental protection")
        
        return recommendations[:5]  # Limit recommendations
    
    async def initialize(self) -> bool:
        """Initialize the Values Assessment agent"""
        try:
            # No external models needed for basic assessment
            return True
        except Exception as e:
            return False
    
    async def validate_input(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate input data for values assessment"""
        text = data.get("text", "")
        if not text or not isinstance(text, str):
            return False, "Text input is required and must be a string"
        if len(text.strip()) < 30:
            return False, "Text must be at least 30 characters for meaningful values assessment"
        if len(text) > 10000:
            return False, "Text exceeds maximum length of 10,000 characters"
        return True, None
    
    def get_capabilities(self) -> List[AgentCapability]:
        """Return list of agent capabilities"""
        from ...core.base_agent import AgentCapability
        return [AgentCapability(name=cap, description=f"Values assessment: {cap}") for cap in self.capabilities]
    
    def _serialize_assessment(self, assessment: ValuesAssessment) -> Dict[str, Any]:
        """Serialize assessment for JSON response"""
        return {
            "individual_values": {
                key: {
                    "name": value.name,
                    "description": value.description,
                    "score": value.score,
                    "percentile": value.percentile,
                    "importance_level": value.importance_level,
                    "evidence": value.evidence,
                    "motivational_goal": value.motivational_goal
                }
                for key, value in assessment.individual_values.items()
            },
            "dimensions": {
                key: {
                    "name": dim.name,
                    "description": dim.description,
                    "dimension_score": dim.dimension_score,
                    "dominant_value": dim.dominant_value,
                    "values_included": dim.values
                }
                for key, dim in assessment.dimensions.items()
            },
            "value_conflicts": [
                {"value1": c[0], "value2": c[1], "explanation": c[2]}
                for c in assessment.value_conflicts
            ]
        }
    
    def _generate_summary(self, assessment: ValuesAssessment) -> str:
        """Generate concise summary of values profile"""
        top_3_values = assessment.value_priorities[:3]
        top_dimension = max(assessment.dimensions.values(), key=lambda d: d.dimension_score)
        
        values_text = ", ".join([f"{name} ({score:.1f})" for name, score in top_3_values])
        
        return f"Top Values: {values_text} | Primary Orientation: {top_dimension.name}"


# Helper function for external usage
async def assess_values(text: str, agent_id: str = "values_agent") -> Dict[str, Any]:
    """Convenience function for values assessment"""
    agent = ValuesAgent(agent_id)
    message = AgentMessage(
        message_id="values_assessment",
        agent_id=agent_id,
        content={"text": text}
    )
    
    response = await agent.process(message)
    return response.content