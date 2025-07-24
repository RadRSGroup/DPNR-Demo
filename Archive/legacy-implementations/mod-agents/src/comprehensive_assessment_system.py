"""
Comprehensive Assessment System

Integrates all psychological assessment agents into unified workflows
with frontend integration and multi-language support.
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass

# Import all assessment agents
from agent_library.agents.assessment.enneagram_agent import EnneagramAgent
from agent_library.agents.assessment.big_five_agent import BigFiveAgent
from agent_library.agents.assessment.values_agent import ValuesAgent
from agent_library.agents.assessment.emotional_intelligence_agent import EmotionalIntelligenceAgent
from agent_library.agents.assessment.cognitive_style_agent import CognitiveStyleAgent
from agent_library.agents.language.clinical_language_agent import ClinicalLanguageAgent
from agent_library.agents.language.translation_agent import TranslationAgent

# Import orchestration components
from agent_library.orchestration.chain_builder import ChainBuilder, ChainExecutionMode
from agent_library.orchestration.workflow_engine import WorkflowEngine, ExecutionContext

# Import core components
from agent_library.core.base_agent import AgentMessage, AgentResponse


@dataclass
class AssessmentResult:
    """Complete assessment results from all agents"""
    assessment_id: str
    user_input: str
    detected_language: str
    translated_text: Optional[str]
    
    # Assessment results
    enneagram_result: Dict[str, Any]
    big_five_result: Dict[str, Any]
    values_result: Dict[str, Any]
    emotional_intelligence_result: Dict[str, Any]
    cognitive_style_result: Dict[str, Any]
    clinical_language_result: Dict[str, Any]
    
    # Integrated insights
    cross_framework_insights: List[str]
    personality_summary: str
    development_recommendations: List[str]
    
    # Metadata
    overall_confidence: float
    processing_time_seconds: float
    timestamp: datetime


class ComprehensiveAssessmentSystem:
    """
    Unified system for complete psychological assessment using all agent frameworks.
    
    Provides:
    - Multi-language support (Hebrew-English translation)
    - All 6 psychological assessment frameworks
    - Clinical linguistic analysis
    - Cross-framework integration and insights
    - Frontend API integration
    - Session management for interactive assessments
    """
    
    def __init__(self, enable_translation: bool = True):
        # Initialize all agents
        self.translation_agent = TranslationAgent() if enable_translation else None
        self.clinical_language_agent = ClinicalLanguageAgent()
        self.enneagram_agent = EnneagramAgent()
        self.big_five_agent = BigFiveAgent()
        self.values_agent = ValuesAgent()
        self.emotional_intelligence_agent = EmotionalIntelligenceAgent()
        self.cognitive_style_agent = CognitiveStyleAgent()
        
        # Initialize orchestration
        self.chain_builder = ChainBuilder()
        self.workflow_engine = WorkflowEngine(self.chain_builder)
        
        # Register all agents
        self._register_agents()
        
        # Create assessment workflows
        self._create_assessment_workflows()
        
        # Session management
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
    
    def _register_agents(self):
        """Register all agents with the chain builder"""
        self.chain_builder.register_agent(TranslationAgent, "TranslationAgent")
        self.chain_builder.register_agent(ClinicalLanguageAgent, "ClinicalLanguageAgent")
        self.chain_builder.register_agent(EnneagramAgent, "EnneagramAgent")
        self.chain_builder.register_agent(BigFiveAgent, "BigFiveAgent")
        self.chain_builder.register_agent(ValuesAgent, "ValuesAgent")
        self.chain_builder.register_agent(EmotionalIntelligenceAgent, "EmotionalIntelligenceAgent")
        self.chain_builder.register_agent(CognitiveStyleAgent, "CognitiveStyleAgent")
    
    def _create_assessment_workflows(self):
        """Create pre-defined assessment workflows"""
        
        # 1. Complete Assessment Chain (all frameworks)
        self.chain_builder.create_chain(
            "complete_assessment",
            "Complete Psychological Assessment",
            "Full assessment using all psychological frameworks"
        )
        
        # Add agents in parallel for efficiency
        self.chain_builder.add_agent("complete_assessment", "translator", "TranslationAgent")
        self.chain_builder.add_agent("complete_assessment", "clinical", "ClinicalLanguageAgent", 
                                   execution_mode=ChainExecutionMode.PARALLEL)
        self.chain_builder.add_agent("complete_assessment", "enneagram", "EnneagramAgent",
                                   execution_mode=ChainExecutionMode.PARALLEL)
        self.chain_builder.add_agent("complete_assessment", "big_five", "BigFiveAgent",
                                   execution_mode=ChainExecutionMode.PARALLEL)
        self.chain_builder.add_agent("complete_assessment", "values", "ValuesAgent",
                                   execution_mode=ChainExecutionMode.PARALLEL)
        self.chain_builder.add_agent("complete_assessment", "emotional_iq", "EmotionalIntelligenceAgent",
                                   execution_mode=ChainExecutionMode.PARALLEL)
        self.chain_builder.add_agent("complete_assessment", "cognitive", "CognitiveStyleAgent",
                                   execution_mode=ChainExecutionMode.PARALLEL)
        
        # Connect translation to all assessment agents
        for agent_id in ["clinical", "enneagram", "big_five", "values", "emotional_iq", "cognitive"]:
            self.chain_builder.connect_agents("complete_assessment", "translator", agent_id,
                                            {"translated_text": "text"})
        
        # 2. Quick Assessment Chain (core frameworks only)
        self.chain_builder.create_chain(
            "quick_assessment", 
            "Quick Personality Assessment",
            "Core personality assessment with Enneagram and Big Five"
        )
        
        self.chain_builder.add_agent("quick_assessment", "translator", "TranslationAgent")
        self.chain_builder.add_agent("quick_assessment", "enneagram", "EnneagramAgent",
                                   execution_mode=ChainExecutionMode.PARALLEL)
        self.chain_builder.add_agent("quick_assessment", "big_five", "BigFiveAgent",
                                   execution_mode=ChainExecutionMode.PARALLEL)
        
        self.chain_builder.connect_agents("quick_assessment", "translator", "enneagram",
                                        {"translated_text": "text"})
        self.chain_builder.connect_agents("quick_assessment", "translator", "big_five",
                                        {"translated_text": "text"})
        
        # 3. Clinical Assessment Chain (clinical focus)
        self.chain_builder.create_chain(
            "clinical_assessment",
            "Clinical Psychological Assessment", 
            "Clinical-focused assessment with linguistic analysis"
        )
        
        self.chain_builder.add_agent("clinical_assessment", "translator", "TranslationAgent")
        self.chain_builder.add_agent("clinical_assessment", "clinical", "ClinicalLanguageAgent",
                                   execution_mode=ChainExecutionMode.PARALLEL)
        self.chain_builder.add_agent("clinical_assessment", "emotional_iq", "EmotionalIntelligenceAgent",
                                   execution_mode=ChainExecutionMode.PARALLEL)
        self.chain_builder.add_agent("clinical_assessment", "big_five", "BigFiveAgent",
                                   execution_mode=ChainExecutionMode.PARALLEL)
        
        for agent_id in ["clinical", "emotional_iq", "big_five"]:
            self.chain_builder.connect_agents("clinical_assessment", "translator", agent_id,
                                            {"translated_text": "text"})
    
    async def assess_complete(self, text: str, user_id: Optional[str] = None) -> AssessmentResult:
        """Perform complete psychological assessment"""
        start_time = datetime.utcnow()
        assessment_id = f"assessment_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Detect language and translate if needed
        detected_language = await self._detect_language(text)
        translated_text = None
        
        if detected_language != "en" and self.translation_agent:
            translation_response = await self.translation_agent.process(
                AgentMessage(
                    message_id=f"{assessment_id}_translation",
                    agent_id="translation_agent",
                    content={"text": text, "target_language": "en"}
                )
            )
            if translation_response.confidence > 0.5:
                translated_text = translation_response.content.get("translated_text", text)
            else:
                translated_text = text
        else:
            translated_text = text
        
        # Run all assessments in parallel
        assessment_text = translated_text or text
        
        tasks = [
            self._run_agent_assessment(self.clinical_language_agent, assessment_text, f"{assessment_id}_clinical"),
            self._run_agent_assessment(self.enneagram_agent, assessment_text, f"{assessment_id}_enneagram"),
            self._run_agent_assessment(self.big_five_agent, assessment_text, f"{assessment_id}_big_five"),
            self._run_agent_assessment(self.values_agent, assessment_text, f"{assessment_id}_values"),
            self._run_agent_assessment(self.emotional_intelligence_agent, assessment_text, f"{assessment_id}_eq"),
            self._run_agent_assessment(self.cognitive_style_agent, assessment_text, f"{assessment_id}_cognitive")
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Extract results (handle any exceptions)
        clinical_result = results[0] if not isinstance(results[0], Exception) else {"error": str(results[0])}
        enneagram_result = results[1] if not isinstance(results[1], Exception) else {"error": str(results[1])}
        big_five_result = results[2] if not isinstance(results[2], Exception) else {"error": str(results[2])}
        values_result = results[3] if not isinstance(results[3], Exception) else {"error": str(results[3])}
        eq_result = results[4] if not isinstance(results[4], Exception) else {"error": str(results[4])}
        cognitive_result = results[5] if not isinstance(results[5], Exception) else {"error": str(results[5])}
        
        # Generate cross-framework insights
        cross_insights = self._generate_cross_framework_insights({
            "enneagram": enneagram_result,
            "big_five": big_five_result,
            "values": values_result,
            "emotional_intelligence": eq_result,
            "cognitive_style": cognitive_result,
            "clinical": clinical_result
        })
        
        # Generate overall summary and recommendations
        personality_summary = self._generate_personality_summary({
            "enneagram": enneagram_result,
            "big_five": big_five_result,
            "values": values_result
        })
        
        development_recommendations = self._generate_development_recommendations({
            "enneagram": enneagram_result,
            "big_five": big_five_result,
            "emotional_intelligence": eq_result,
            "clinical": clinical_result
        })
        
        # Calculate overall confidence
        confidences = []
        for result in [clinical_result, enneagram_result, big_five_result, values_result, eq_result, cognitive_result]:
            if isinstance(result, dict) and "error" not in result:
                # Try to extract confidence from various result formats
                if "confidence" in result:
                    confidences.append(result["confidence"])
                elif "overall_confidence" in result:
                    confidences.append(result["overall_confidence"])
        
        overall_confidence = sum(confidences) / len(confidences) if confidences else 0.5
        
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        return AssessmentResult(
            assessment_id=assessment_id,
            user_input=text,
            detected_language=detected_language,
            translated_text=translated_text,
            enneagram_result=enneagram_result,
            big_five_result=big_five_result,
            values_result=values_result,
            emotional_intelligence_result=eq_result,
            cognitive_style_result=cognitive_result,
            clinical_language_result=clinical_result,
            cross_framework_insights=cross_insights,
            personality_summary=personality_summary,
            development_recommendations=development_recommendations,
            overall_confidence=overall_confidence,
            processing_time_seconds=processing_time,
            timestamp=datetime.utcnow()
        )
    
    async def assess_quick(self, text: str) -> Dict[str, Any]:
        """Quick assessment with core frameworks only"""
        detected_language = await self._detect_language(text)
        assessment_text = await self._translate_if_needed(text, detected_language)
        
        # Run core assessments
        tasks = [
            self._run_agent_assessment(self.enneagram_agent, assessment_text, "quick_enneagram"),
            self._run_agent_assessment(self.big_five_agent, assessment_text, "quick_big_five")
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            "enneagram": results[0] if not isinstance(results[0], Exception) else {"error": str(results[0])},
            "big_five": results[1] if not isinstance(results[1], Exception) else {"error": str(results[1])},
            "detected_language": detected_language,
            "assessment_type": "quick"
        }
    
    async def start_interactive_session(self, user_id: str, initial_text: str) -> Dict[str, Any]:
        """Start an interactive assessment session"""
        session_id = f"session_{user_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize session
        self.active_sessions[session_id] = {
            "user_id": user_id,
            "responses": [initial_text],
            "partial_results": {},
            "confidence_scores": {},
            "follow_up_questions": [],
            "created_at": datetime.utcnow()
        }
        
        # Process initial input
        initial_result = await self.assess_quick(initial_text)
        self.active_sessions[session_id]["partial_results"] = initial_result
        
        # Generate follow-up questions based on low confidence areas
        follow_up_questions = self._generate_follow_up_questions(initial_result)
        self.active_sessions[session_id]["follow_up_questions"] = follow_up_questions
        
        return {
            "session_id": session_id,
            "initial_assessment": initial_result,
            "next_question": follow_up_questions[0] if follow_up_questions else None,
            "progress": "1/5"  # Assuming 5 total questions
        }
    
    async def continue_interactive_session(self, session_id: str, response: str) -> Dict[str, Any]:
        """Continue an interactive assessment session"""
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        session["responses"].append(response)
        
        # Combine all responses for assessment
        combined_text = " ".join(session["responses"])
        
        # Update assessment with new information
        updated_result = await self.assess_quick(combined_text)
        session["partial_results"] = updated_result
        
        # Check if we have enough information (confidence thresholds)
        questions_answered = len(session["responses"])
        
        if questions_answered >= 5:  # Max questions reached
            final_result = await self.assess_complete(combined_text, session["user_id"])
            return {
                "session_id": session_id,
                "status": "completed",
                "final_assessment": self._serialize_assessment_result(final_result)
            }
        else:
            # Generate next question
            next_questions = self._generate_follow_up_questions(updated_result)
            next_question = next_questions[0] if next_questions else "Tell me more about yourself."
            
            return {
                "session_id": session_id,
                "status": "continuing",
                "current_assessment": updated_result,
                "next_question": next_question,
                "progress": f"{questions_answered + 1}/5"
            }
    
    async def _detect_language(self, text: str) -> str:
        """Detect language of input text"""
        if self.translation_agent:
            try:
                detection_response = await self.translation_agent.process(
                    AgentMessage(
                        message_id="language_detection",
                        agent_id="translation_agent",
                        content={"text": text, "action": "detect"}
                    )
                )
                return detection_response.content.get("detected_language", "en")
            except:
                return "en"
        return "en"
    
    async def _translate_if_needed(self, text: str, detected_language: str) -> str:
        """Translate text to English if needed"""
        if detected_language != "en" and self.translation_agent:
            try:
                translation_response = await self.translation_agent.process(
                    AgentMessage(
                        message_id="translation",
                        agent_id="translation_agent",
                        content={"text": text, "target_language": "en"}
                    )
                )
                return translation_response.content.get("translated_text", text)
            except:
                return text
        return text
    
    async def _run_agent_assessment(self, agent, text: str, message_id: str) -> Dict[str, Any]:
        """Run assessment on a single agent"""
        message = AgentMessage(
            message_id=message_id,
            agent_id=agent.agent_id,
            content={"text": text}
        )
        
        response = await agent.process(message)
        result = response.content.copy()
        result["confidence"] = response.confidence
        return result
    
    def _generate_cross_framework_insights(self, results: Dict[str, Dict[str, Any]]) -> List[str]:
        """Generate insights by comparing across assessment frameworks"""
        insights = []
        
        # Compare Enneagram and Big Five
        if "enneagram" in results and "big_five" in results:
            enneagram_data = results["enneagram"]
            big_five_data = results["big_five"]
            
            if ("assessment" in enneagram_data and "big_five_profile" in big_five_data and
                "error" not in enneagram_data and "error" not in big_five_data):
                
                enneagram_type = enneagram_data["assessment"]["top_type"]
                
                # Find correlations
                if "Type 1" in enneagram_type and "conscientiousness" in big_five_data["big_five_profile"]:
                    cons_score = big_five_data["big_five_profile"]["conscientiousness"]["score"]
                    if cons_score > 0.7:
                        insights.append("Strong consistency between Enneagram Type 1 and high Conscientiousness - indicates perfectionist tendencies")
                
                if "Type 7" in enneagram_type and "openness" in big_five_data["big_five_profile"]:
                    openness_score = big_five_data["big_five_profile"]["openness"]["score"]
                    if openness_score > 0.7:
                        insights.append("Enneagram Type 7 aligns with high Openness - suggests enthusiastic, variety-seeking personality")
        
        # Compare Values and Big Five
        if "values" in results and "big_five" in results:
            values_data = results["values"]
            big_five_data = results["big_five"]
            
            if ("values_profile" in values_data and "big_five_profile" in big_five_data and
                "error" not in values_data and "error" not in big_five_data):
                
                # Look for value-trait alignments
                if ("achievement" in values_data["values_profile"]["individual_values"] and
                    "conscientiousness" in big_five_data["big_five_profile"]):
                    
                    achievement_score = values_data["values_profile"]["individual_values"]["achievement"]["score"]
                    cons_score = big_five_data["big_five_profile"]["conscientiousness"]["score"]
                    
                    if achievement_score > 0.6 and cons_score > 0.6:
                        insights.append("High Achievement values coupled with high Conscientiousness suggests strong goal-oriented behavior")
        
        # Compare Emotional Intelligence with other frameworks
        if "emotional_intelligence" in results and "clinical" in results:
            eq_data = results["emotional_intelligence"]
            clinical_data = results["clinical"]
            
            if ("eq_profile" in eq_data and "clinical_features" in clinical_data and
                "error" not in eq_data and "error" not in clinical_data):
                
                eq_score = eq_data.get("overall_score", 0)
                clinical_risk = clinical_data.get("risk_assessment", {}).get("overall_risk_level", "low")
                
                if eq_score < 0.5 and clinical_risk == "high":
                    insights.append("Lower emotional intelligence combined with elevated linguistic risk factors suggests need for emotional regulation support")
        
        if not insights:
            insights.append("Assessment frameworks show generally consistent patterns across personality dimensions")
        
        return insights
    
    def _generate_personality_summary(self, results: Dict[str, Dict[str, Any]]) -> str:
        """Generate overall personality summary"""
        components = []
        
        # Enneagram component
        if "enneagram" in results and "error" not in results["enneagram"]:
            enneagram_data = results["enneagram"]
            if "assessment" in enneagram_data:
                top_type = enneagram_data["assessment"]["top_type"]
                components.append(f"Core personality: {top_type}")
        
        # Big Five component
        if "big_five" in results and "error" not in results["big_five"]:
            big_five_data = results["big_five"]
            if "summary" in big_five_data:
                components.append(f"Trait profile: {big_five_data['summary']}")
        
        # Values component
        if "values" in results and "error" not in results["values"]:
            values_data = results["values"]
            if "value_priorities" in values_data and values_data["value_priorities"]:
                top_value = values_data["value_priorities"][0][0]
                components.append(f"Primary value: {top_value}")
        
        if components:
            return " | ".join(components)
        else:
            return "Personality assessment completed with multiple frameworks"
    
    def _generate_development_recommendations(self, results: Dict[str, Dict[str, Any]]) -> List[str]:
        """Generate development recommendations from multiple frameworks"""
        recommendations = []
        
        # Collect recommendations from each framework
        for framework, data in results.items():
            if isinstance(data, dict) and "error" not in data:
                if "recommendations" in data:
                    recommendations.extend(data["recommendations"][:2])  # Top 2 from each
                elif "development_suggestions" in data:
                    recommendations.extend(data["development_suggestions"][:2])
        
        # Remove duplicates and limit
        unique_recommendations = list(dict.fromkeys(recommendations))
        return unique_recommendations[:8]  # Limit to 8 total recommendations
    
    def _generate_follow_up_questions(self, assessment_result: Dict[str, Any]) -> List[str]:
        """Generate follow-up questions based on assessment results"""
        questions = []
        
        # Default questions for interactive assessment
        default_questions = [
            "How do you typically handle stress or challenging situations?",
            "What motivates you most in life - personal achievement, relationships, or making a difference?",
            "When making important decisions, do you rely more on logic or intuition?",
            "How do you prefer to work - independently or as part of a team?",
            "What would others say is your greatest strength and your biggest growth area?"
        ]
        
        # Could add logic here to customize questions based on low-confidence areas
        # For now, return default questions
        return default_questions
    
    def _serialize_assessment_result(self, result: AssessmentResult) -> Dict[str, Any]:
        """Serialize AssessmentResult for JSON response"""
        return {
            "assessment_id": result.assessment_id,
            "user_input": result.user_input,
            "detected_language": result.detected_language,
            "translated_text": result.translated_text,
            "assessments": {
                "enneagram": result.enneagram_result,
                "big_five": result.big_five_result,
                "values": result.values_result,
                "emotional_intelligence": result.emotional_intelligence_result,
                "cognitive_style": result.cognitive_style_result,
                "clinical_language": result.clinical_language_result
            },
            "insights": {
                "cross_framework_insights": result.cross_framework_insights,
                "personality_summary": result.personality_summary,
                "development_recommendations": result.development_recommendations
            },
            "metadata": {
                "overall_confidence": result.overall_confidence,
                "processing_time_seconds": result.processing_time_seconds,
                "timestamp": result.timestamp.isoformat()
            }
        }
    
    def get_available_assessments(self) -> List[Dict[str, str]]:
        """Get list of available assessment frameworks"""
        return [
            {"id": "enneagram", "name": "Enneagram Types", "description": "9 personality types focused on core motivations"},
            {"id": "big_five", "name": "Big Five Traits", "description": "Five-factor model with personality dimensions"},
            {"id": "values", "name": "Personal Values", "description": "Schwartz's 10 universal human values"},
            {"id": "emotional_intelligence", "name": "Emotional Intelligence", "description": "Four-domain EQ assessment"},
            {"id": "cognitive_style", "name": "Cognitive Style", "description": "Thinking patterns and information processing"},
            {"id": "clinical_language", "name": "Clinical Language Analysis", "description": "Psycholinguistic markers and risk assessment"}
        ]


# Example usage and test functions
async def test_comprehensive_assessment():
    """Test the comprehensive assessment system"""
    system = ComprehensiveAssessmentSystem()
    
    # Test English input
    english_text = "I am a very organized person who likes to plan everything carefully. I value achievement and success, but I also care deeply about helping others. Sometimes I worry too much about making the right decisions."
    
    print("Testing English assessment...")
    result = await system.assess_complete(english_text)
    print(f"Assessment completed in {result.processing_time_seconds:.2f} seconds")
    print(f"Overall confidence: {result.overall_confidence:.2f}")
    print("Personality summary:", result.personality_summary)
    print("Top 3 recommendations:")
    for i, rec in enumerate(result.development_recommendations[:3], 1):
        print(f"  {i}. {rec}")
    
    # Test Hebrew input
    hebrew_text = "אני אדם יצירתי שאוהב לחקור דברים חדשים. חשוב לי להיות עצמאי ולעשות דברים בדרך שלי. לפעמים אני מתרגש מדי ומתקשה להתמקד."
    
    print("\nTesting Hebrew assessment...")
    hebrew_result = await system.assess_complete(hebrew_text)
    print(f"Detected language: {hebrew_result.detected_language}")
    print(f"Translated: {hebrew_result.translated_text}")
    print("Personality summary:", hebrew_result.personality_summary)
    
    # Test interactive session
    print("\nTesting interactive session...")
    session = await system.start_interactive_session("user123", english_text)
    print(f"Session started: {session['session_id']}")
    print(f"Next question: {session['next_question']}")
    
    # Continue session
    continued = await system.continue_interactive_session(
        session['session_id'], 
        "I handle stress by taking a step back and making a plan. I prefer to work independently most of the time."
    )
    print(f"Session status: {continued['status']}")
    print(f"Next question: {continued.get('next_question', 'Assessment complete')}")


if __name__ == "__main__":
    # Run test
    asyncio.run(test_comprehensive_assessment())