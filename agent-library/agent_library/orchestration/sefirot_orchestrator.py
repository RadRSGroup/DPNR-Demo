"""
Sefirot Orchestrator for DPNR Agent Library
Orchestrates multiple sefirot agents in therapeutic workflows
Implements the Tree of Life flow patterns for comprehensive therapeutic processing
Generated for Phase 1 Sefirot Integration
"""
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import uuid
import json

from ..agents.assessment.sefirot_base_agent import (
    SefirotAgent, SefirotType, SefirotFlow, SefirotActivation, SefirotResponse
)
from ..agents.assessment.malchut_agent import MalchutAgent
from ..agents.assessment.tiferet_agent import TiferetAgent
from ..agents.assessment.yesod_agent import YesodAgent
from ..agents.assessment.chesed_agent import ChesedAgent
from ..agents.assessment.gevurah_agent import GevurahAgent
from ..agents.assessment.netzach_agent import NetzachAgent
from ..agents.assessment.hod_agent import HodAgent
from ..agents.assessment.chochmah_agent import ChochmahAgent
from ..agents.assessment.binah_agent import BinahAgent
from ..agents.assessment.keter_agent import KeterAgent
from ..core.base_agent import AgentMessage, AgentResponse


class SefirotSession(object):
    """Represents a sefirot therapeutic session"""
    
    def __init__(self, session_id: str, user_id: str, therapeutic_intent: str):
        self.session_id = session_id
        self.user_id = user_id
        self.therapeutic_intent = therapeutic_intent
        self.created_at = datetime.utcnow()
        self.active_agents: Dict[SefirotType, SefirotAgent] = {}
        self.processing_history: List[Dict[str, Any]] = []
        self.current_flow: Optional[SefirotFlow] = None
        self.synthesis_result: Optional[Dict[str, Any]] = None
        self.session_complete = False
    
    def add_processing_event(self, event: Dict[str, Any]):
        """Add processing event to session history"""
        event['timestamp'] = datetime.utcnow().isoformat()
        self.processing_history.append(event)
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of session"""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "therapeutic_intent": self.therapeutic_intent,
            "created_at": self.created_at.isoformat(),
            "active_agents": list(self.active_agents.keys()),
            "processing_events": len(self.processing_history),
            "current_flow": self.current_flow.value if self.current_flow else None,
            "session_complete": self.session_complete,
            "synthesis_available": self.synthesis_result is not None
        }


class SefirotWorkflow(object):
    """Defines a sefirot workflow pattern"""
    
    def __init__(self, name: str, sefirot_sequence: List[SefirotType], 
                 flow_pattern: SefirotFlow, therapeutic_intent: str):
        self.name = name
        self.sefirot_sequence = sefirot_sequence
        self.flow_pattern = flow_pattern
        self.therapeutic_intent = therapeutic_intent
        self.description = self._generate_description()
    
    def _generate_description(self) -> str:
        """Generate description of workflow"""
        sefirot_names = [s.value for s in self.sefirot_sequence]
        return f"{self.name}: {self.flow_pattern.value} flow through {' → '.join(sefirot_names)}"


class SefirotOrchestrator:
    """
    Orchestrates sefirot agents in therapeutic workflows
    Implements Tree of Life flow patterns and synthesis capabilities
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.active_sessions: Dict[str, SefirotSession] = {}
        self.agent_pool: Dict[SefirotType, SefirotAgent] = {}
        self.predefined_workflows = self._initialize_predefined_workflows()
        
        # Initialize Phase 1 agents
        asyncio.create_task(self._initialize_agent_pool())
    
    async def _initialize_agent_pool(self):
        """Initialize pool of all 10 sefirot agents"""
        try:
            # Initialize all 10 sefirot agents
            self.agent_pool[SefirotType.KETER] = KeterAgent()
            self.agent_pool[SefirotType.CHOCHMAH] = ChochmahAgent()
            self.agent_pool[SefirotType.BINAH] = BinahAgent()
            self.agent_pool[SefirotType.CHESED] = ChesedAgent()
            self.agent_pool[SefirotType.GEVURAH] = GevurahAgent()
            self.agent_pool[SefirotType.TIFERET] = TiferetAgent()
            self.agent_pool[SefirotType.NETZACH] = NetzachAgent()
            self.agent_pool[SefirotType.HOD] = HodAgent()
            self.agent_pool[SefirotType.YESOD] = YesodAgent()
            self.agent_pool[SefirotType.MALCHUT] = MalchutAgent()
            
            # Initialize all agents
            for sefirot_type, agent in self.agent_pool.items():
                success = await agent.initialize()
                if success:
                    self.logger.info(f"Initialized {sefirot_type.value} agent")
                else:
                    self.logger.error(f"Failed to initialize {sefirot_type.value} agent")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize agent pool: {e}")
    
    def _initialize_predefined_workflows(self) -> Dict[str, SefirotWorkflow]:
        """Initialize comprehensive therapeutic workflows for all 10 sefirot"""
        workflows = {}
        
        # Complete Tree Workflow
        workflows["complete_tree"] = SefirotWorkflow(
            name="Complete Tree of Life Integration",
            sefirot_sequence=[SefirotType.KETER, SefirotType.CHOCHMAH, SefirotType.BINAH, 
                            SefirotType.CHESED, SefirotType.GEVURAH, SefirotType.TIFERET,
                            SefirotType.NETZACH, SefirotType.HOD, SefirotType.YESOD, SefirotType.MALCHUT],
            flow_pattern=SefirotFlow.DESCENDING,
            therapeutic_intent="Complete mystical therapeutic integration from transcendence to manifestation"
        )
        
        # Lightning Flash Workflow
        workflows["lightning_breakthrough"] = SefirotWorkflow(
            name="Lightning Flash Breakthrough",
            sefirot_sequence=[SefirotType.KETER, SefirotType.CHOCHMAH, SefirotType.BINAH, 
                            SefirotType.CHESED, SefirotType.GEVURAH, SefirotType.TIFERET,
                            SefirotType.NETZACH, SefirotType.HOD, SefirotType.YESOD, SefirotType.MALCHUT],
            flow_pattern=SefirotFlow.LIGHTNING,
            therapeutic_intent="Rapid breakthrough activation across all sefirot for profound transformation"
        )
        
        # Wisdom Pillar Workflow
        workflows["wisdom_understanding"] = SefirotWorkflow(
            name="Wisdom and Understanding Integration",
            sefirot_sequence=[SefirotType.CHOCHMAH, SefirotType.BINAH, SefirotType.TIFERET],
            flow_pattern=SefirotFlow.DESCENDING,
            therapeutic_intent="Flash insights integrated through deep understanding into balanced wisdom"
        )
        
        # Emotional Healing Workflow
        workflows["emotional_healing"] = SefirotWorkflow(
            name="Emotional Healing and Integration",
            sefirot_sequence=[SefirotType.CHESED, SefirotType.GEVURAH, SefirotType.TIFERET],
            flow_pattern=SefirotFlow.BALANCING,
            therapeutic_intent="Balance compassion and boundaries for healthy emotional integration"
        )
        
        # Creative Expression Workflow
        workflows["creative_expression"] = SefirotWorkflow(
            name="Creative Expression and Communication",
            sefirot_sequence=[SefirotType.NETZACH, SefirotType.HOD, SefirotType.YESOD, SefirotType.MALCHUT],
            flow_pattern=SefirotFlow.DESCENDING,
            therapeutic_intent="Transform creativity through communication into grounded manifestation"
        )
        
        # Foundation Building Workflow
        workflows["foundation_building"] = SefirotWorkflow(
            name="Foundation Building",
            sefirot_sequence=[SefirotType.TIFERET, SefirotType.YESOD, SefirotType.MALCHUT],
            flow_pattern=SefirotFlow.DESCENDING,
            therapeutic_intent="Create harmony, ground insights, and manifest in practical life"
        )
        
        # Transcendence Integration Workflow
        workflows["transcendence_integration"] = SefirotWorkflow(
            name="Transcendence Integration",
            sefirot_sequence=[SefirotType.KETER, SefirotType.TIFERET, SefirotType.MALCHUT],
            flow_pattern=SefirotFlow.DESCENDING,
            therapeutic_intent="Integrate universal breakthrough through heart harmony into earthly manifestation"
        )
        
        # Pillar Balance Workflow
        workflows["pillar_balance"] = SefirotWorkflow(
            name="Three Pillar Balance",
            sefirot_sequence=[SefirotType.BINAH, SefirotType.TIFERET, SefirotType.CHOCHMAH, 
                            SefirotType.GEVURAH, SefirotType.CHESED, SefirotType.HOD, 
                            SefirotType.YESOD, SefirotType.NETZACH],
            flow_pattern=SefirotFlow.BALANCING,
            therapeutic_intent="Balance severity, mercy, and middle pillar energies for complete integration"
        )
        
        return workflows
    
    async def create_session(self, user_id: str, therapeutic_intent: str, 
                           workflow_name: Optional[str] = None,
                           custom_sefirot: Optional[List[SefirotType]] = None) -> str:
        """Create new sefirot therapeutic session"""
        
        session_id = str(uuid.uuid4())
        session = SefirotSession(session_id, user_id, therapeutic_intent)
        
        # Determine sefirot sequence
        if workflow_name and workflow_name in self.predefined_workflows:
            workflow = self.predefined_workflows[workflow_name]
            sefirot_sequence = workflow.sefirot_sequence
            session.current_flow = workflow.flow_pattern
        elif custom_sefirot:
            sefirot_sequence = custom_sefirot
            session.current_flow = SefirotFlow.DESCENDING  # Default
        else:
            # Default to foundation integration
            sefirot_sequence = [SefirotType.TIFERET, SefirotType.YESOD, SefirotType.MALCHUT]
            session.current_flow = SefirotFlow.DESCENDING
        
        # Initialize required agents in session
        for sefirot_type in sefirot_sequence:
            if sefirot_type in self.agent_pool:
                session.active_agents[sefirot_type] = self.agent_pool[sefirot_type]
            else:
                self.logger.warning(f"Agent for {sefirot_type.value} not available")
        
        self.active_sessions[session_id] = session
        
        session.add_processing_event({
            "event_type": "session_created",
            "workflow": workflow_name,
            "sefirot_sequence": [s.value for s in sefirot_sequence],
            "flow_pattern": session.current_flow.value if session.current_flow else None
        })
        
        self.logger.info(f"Created sefirot session {session_id} for user {user_id}")
        
        return session_id
    
    async def process_therapeutic_request(self, session_id: str, user_input: str, 
                                        context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process therapeutic request through sefirot workflow"""
        
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        context = context or {}
        context.update({
            "session_id": session_id,
            "user_id": session.user_id,
            "therapeutic_intent": session.therapeutic_intent
        })
        
        try:
            # Process through sefirot sequence
            sefirot_results = []
            processing_context = context.copy()
            
            # Determine processing order based on flow
            sefirot_sequence = list(session.active_agents.keys())
            if session.current_flow == SefirotFlow.ASCENDING:
                # Reverse order for ascending flow
                sefirot_sequence = list(reversed(sefirot_sequence))
            elif session.current_flow == SefirotFlow.LIGHTNING:
                # Special lightning pattern (skip for Phase 1)
                pass
            
            # Process through each sefirot
            for i, sefirot_type in enumerate(sefirot_sequence):
                agent = session.active_agents[sefirot_type]
                
                # Add previous results to context
                if sefirot_results:
                    processing_context["previous_sefirot_results"] = sefirot_results
                    processing_context["integration_guidance"] = [
                        r.get("integration_guidance", []) for r in sefirot_results
                    ]
                
                # Create agent message
                message = AgentMessage(
                    message_id=str(uuid.uuid4()),
                    sender_id="orchestrator",
                    recipient_id=agent.agent_id,
                    message_type="therapeutic_processing",
                    payload={
                        "action": "process_therapeutic_request",
                        "data": {
                            "user_input": user_input,
                            "context": processing_context,
                            "sequence_position": i + 1,
                            "total_sefirot": len(sefirot_sequence)
                        }
                    }
                )
                
                # Process through agent
                response = await agent.process(message)
                
                if response.success:
                    sefirot_results.append({
                        "sefirot_type": sefirot_type.value,
                        "response": response.data,
                        "confidence": response.confidence,
                        "processing_time": response.processing_time
                    })
                    
                    session.add_processing_event({
                        "event_type": "sefirot_processed",
                        "sefirot_type": sefirot_type.value,
                        "confidence": response.confidence,
                        "processing_time": response.processing_time
                    })
                else:
                    self.logger.error(f"Sefirot {sefirot_type.value} processing failed: {response.error}")
                    sefirot_results.append({
                        "sefirot_type": sefirot_type.value,
                        "error": response.error,
                        "confidence": 0.0
                    })
            
            # Synthesize results
            synthesis_result = await self._synthesize_sefirot_results(
                sefirot_results, session, user_input, context
            )
            
            session.synthesis_result = synthesis_result
            session.add_processing_event({
                "event_type": "synthesis_completed",
                "synthesis_confidence": synthesis_result.get("overall_confidence", 0.0),
                "integration_themes": len(synthesis_result.get("integration_themes", []))
            })
            
            return {
                "session_id": session_id,
                "success": True,
                "sefirot_results": sefirot_results,
                "synthesis": synthesis_result,
                "processing_summary": {
                    "sefirot_processed": len(sefirot_results),
                    "successful_processing": sum(1 for r in sefirot_results if "error" not in r),
                    "flow_pattern": session.current_flow.value,
                    "total_processing_time": sum(r.get("processing_time", 0) for r in sefirot_results)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Session {session_id} processing failed: {e}")
            session.add_processing_event({
                "event_type": "processing_error",
                "error": str(e)
            })
            
            return {
                "session_id": session_id,
                "success": False,
                "error": str(e),
                "partial_results": locals().get("sefirot_results", [])
            }
    
    async def _synthesize_sefirot_results(self, sefirot_results: List[Dict[str, Any]], 
                                        session: SefirotSession, user_input: str,
                                        context: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize results from multiple sefirot agents"""
        
        successful_results = [r for r in sefirot_results if "error" not in r]
        if not successful_results:
            return {"error": "No successful sefirot processing to synthesize"}
        
        # Extract insights and guidance from all sefirot
        all_insights = []
        all_guidance = []
        all_metaphors = []
        integration_themes = set()
        
        for result in successful_results:
            response_data = result.get("response", {})
            
            # Extract insights
            insights = response_data.get("insights", [])
            if isinstance(insights, list):
                all_insights.extend(insights)
            
            # Extract guidance
            guidance = response_data.get("guidance", [])
            if isinstance(guidance, list):
                all_guidance.extend(guidance)
            
            # Extract metaphors
            if "metaphors" in response_data:
                all_metaphors.extend(response_data["metaphors"])
            
            # Extract integration themes
            if "integration_guidance" in response_data:
                for guidance_item in response_data["integration_guidance"]:
                    integration_themes.add(self._extract_theme_from_guidance(guidance_item))
        
        # Create synthesis narrative
        synthesis_narrative = await self._create_synthesis_narrative(
            successful_results, session, user_input, context
        )
        
        # Calculate overall confidence
        confidences = [r.get("confidence", 0.0) for r in successful_results]
        overall_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        # Create integration roadmap
        integration_roadmap = await self._create_integration_roadmap(successful_results, context)
        
        return {
            "synthesis_narrative": synthesis_narrative,
            "integration_roadmap": integration_roadmap,
            "unified_insights": self._unify_insights(all_insights),
            "integration_guidance": self._prioritize_guidance(all_guidance),
            "therapeutic_metaphors": self._select_most_resonant_metaphors(all_metaphors),
            "integration_themes": list(integration_themes),
            "sefirot_synergies": await self._identify_sefirot_synergies(successful_results),
            "overall_confidence": overall_confidence,
            "synthesis_quality": self._assess_synthesis_quality(successful_results),
            "next_steps": await self._recommend_next_steps(successful_results, session)
        }
    
    async def _create_synthesis_narrative(self, results: List[Dict[str, Any]], 
                                        session: SefirotSession, user_input: str,
                                        context: Dict[str, Any]) -> str:
        """Create unified narrative from sefirot results"""
        
        sefirot_themes = []
        for result in results:
            sefirot_type = result["sefirot_type"]
            response_data = result.get("response", {})
            
            if sefirot_type == "malchut":
                sefirot_themes.append("manifestation and real-world integration")
            elif sefirot_type == "tiferet":
                sefirot_themes.append("harmony and beautiful balance")
            elif sefirot_type == "yesod":
                sefirot_themes.append("grounding and foundational synthesis")
        
        narrative = f"""
        🌟 **Unified Sefirot Synthesis**
        
        Your therapeutic journey has been processed through the sacred Tree of Life, revealing 
        a comprehensive path of transformation that encompasses {', '.join(sefirot_themes)}.
        
        **Core Integration Message:**
        The wisdom that has emerged shows you're ready to move from insight to embodied living. 
        Your path forward involves creating harmony within your contradictions, building solid 
        foundations for your insights, and manifesting your inner transformation in tangible, 
        real-world changes.
        
        **Unified Wisdom:**
        All the sefirot agree - you have the capacity for profound transformation. The key is 
        consistent, patient application of your insights through daily practice, authentic 
        relationship, and practical manifestation in your chosen life domains.
        
        **Sacred Reminder:**
        This synthesis represents the divine intelligence working through your human experience. 
        Trust the process, honor the journey, and remember that transformation happens in the 
        sacred space where heaven meets earth - in your daily choices and loving actions.
        """
        
        return narrative.strip()
    
    async def _create_integration_roadmap(self, results: List[Dict[str, Any]], 
                                        context: Dict[str, Any]) -> Dict[str, Any]:
        """Create integration roadmap from sefirot results"""
        
        roadmap = {
            "immediate_actions": [],
            "weekly_practices": [],
            "monthly_milestones": [],
            "ongoing_integration": []
        }
        
        for result in results:
            response_data = result.get("response", {})
            
            # Extract action-oriented guidance
            if "guidance" in response_data:
                for guidance_item in response_data["guidance"]:
                    if any(word in guidance_item.lower() for word in ["today", "now", "immediately"]):
                        roadmap["immediate_actions"].append(guidance_item)
                    elif any(word in guidance_item.lower() for word in ["weekly", "week", "regularly"]):
                        roadmap["weekly_practices"].append(guidance_item)
                    elif any(word in guidance_item.lower() for word in ["month", "long-term"]):
                        roadmap["monthly_milestones"].append(guidance_item)
                    else:
                        roadmap["ongoing_integration"].append(guidance_item)
        
        # Ensure each category has content
        if not roadmap["immediate_actions"]:
            roadmap["immediate_actions"].append("Choose one key insight to focus on implementing today")
        
        if not roadmap["weekly_practices"]:
            roadmap["weekly_practices"].append("Create weekly reflection practice to monitor integration progress")
        
        if not roadmap["monthly_milestones"]:
            roadmap["monthly_milestones"].append("Assess overall life satisfaction and growth progress monthly")
        
        return roadmap
    
    def _extract_theme_from_guidance(self, guidance: str) -> str:
        """Extract integration theme from guidance item"""
        guidance_lower = guidance.lower()
        
        if "relationship" in guidance_lower:
            return "relational_integration"
        elif "practice" in guidance_lower or "daily" in guidance_lower:
            return "daily_practice"
        elif "manifes" in guidance_lower or "action" in guidance_lower:
            return "practical_manifestation"
        elif "balance" in guidance_lower or "harmony" in guidance_lower:
            return "harmony_creation"
        elif "ground" in guidance_lower or "foundation" in guidance_lower:
            return "foundation_building"
        else:
            return "general_integration"
    
    def _unify_insights(self, insights: List[str]) -> List[str]:
        """Unify and deduplicate insights from multiple sefirot"""
        # Simple deduplication and selection of most impactful insights
        unique_insights = []
        for insight in insights:
            if not any(self._insights_similar(insight, existing) for existing in unique_insights):
                unique_insights.append(insight)
        
        # Return top 5 most comprehensive insights
        return unique_insights[:5]
    
    def _insights_similar(self, insight1: str, insight2: str) -> bool:
        """Check if two insights are similar enough to be considered duplicates"""
        # Simple similarity check based on shared key words
        words1 = set(insight1.lower().split())
        words2 = set(insight2.lower().split())
        
        # If they share more than 50% of content words, consider similar
        content_words1 = {w for w in words1 if len(w) > 3}
        content_words2 = {w for w in words2 if len(w) > 3}
        
        if not content_words1 or not content_words2:
            return False
        
        intersection = content_words1.intersection(content_words2)
        similarity_ratio = len(intersection) / min(len(content_words1), len(content_words2))
        
        return similarity_ratio > 0.5
    
    def _prioritize_guidance(self, guidance: List[str]) -> List[str]:
        """Prioritize and organize guidance from multiple sefirot"""
        # Prioritize based on action words and practical focus
        priority_words = ["start", "create", "establish", "practice", "implement"]
        
        prioritized = []
        remaining = []
        
        for guide in guidance:
            if any(word in guide.lower() for word in priority_words):
                prioritized.append(guide)
            else:
                remaining.append(guide)
        
        # Return prioritized first, then others, limited to top 7
        return (prioritized + remaining)[:7]
    
    def _select_most_resonant_metaphors(self, metaphors: List[str]) -> List[str]:
        """Select most resonant metaphors from sefirot results"""
        # Simple selection - return first 3 unique metaphors
        unique_metaphors = []
        for metaphor in metaphors:
            if metaphor not in unique_metaphors:
                unique_metaphors.append(metaphor)
            if len(unique_metaphors) >= 3:
                break
        
        return unique_metaphors
    
    async def _identify_sefirot_synergies(self, results: List[Dict[str, Any]]) -> List[str]:
        """Identify synergies between processed sefirot"""
        synergies = []
        sefirot_types = [r["sefirot_type"] for r in results]
        
        if "malchut" in sefirot_types and "yesod" in sefirot_types:
            synergies.append("Foundation and manifestation work together to create lasting change")
        
        if "tiferet" in sefirot_types and "yesod" in sefirot_types:
            synergies.append("Harmony creation and grounding synthesis create beautiful, stable integration")
        
        if "tiferet" in sefirot_types and "malchut" in sefirot_types:
            synergies.append("Balance and manifestation unite to create beauty in real-world expression")
        
        if len(sefirot_types) >= 3:
            synergies.append("The complete Phase 1 sefirot create a powerful foundation for transformation")
        
        return synergies
    
    def _assess_synthesis_quality(self, results: List[Dict[str, Any]]) -> str:
        """Assess quality of synthesis"""
        successful_count = len(results)
        avg_confidence = sum(r.get("confidence", 0) for r in results) / len(results)
        
        if successful_count >= 3 and avg_confidence > 0.85:
            return "excellent"
        elif successful_count >= 2 and avg_confidence > 0.75:
            return "good"
        elif successful_count >= 1 and avg_confidence > 0.65:
            return "adequate"
        else:
            return "needs_improvement"
    
    async def _recommend_next_steps(self, results: List[Dict[str, Any]], 
                                  session: SefirotSession) -> List[str]:
        """Recommend next steps based on synthesis"""
        next_steps = []
        
        # Based on session completion
        if len(results) >= 3:
            next_steps.extend([
                "Complete the integration of Phase 1 sefirot insights through daily practice",
                "Consider expanding to Phase 2 sefirot (Chesed, Gevurah) for deeper emotional work",
                "Create accountability structures to maintain momentum"
            ])
        else:
            next_steps.extend([
                "Continue with remaining Phase 1 sefirot for complete foundation",
                "Focus on implementing current insights before expanding",
                "Build support systems for ongoing integration"
            ])
        
        # Universal next steps
        next_steps.extend([
            "Schedule regular check-ins to monitor integration progress",
            "Share insights with trusted friends or therapeutic support",
            "Create celebration rituals for acknowledging growth milestones"
        ])
        
        return next_steps[:5]  # Limit to 5 next steps
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session information"""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        return session.get_session_summary()
    
    async def complete_session(self, session_id: str) -> Dict[str, Any]:
        """Complete and finalize session"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        session.session_complete = True
        
        session.add_processing_event({
            "event_type": "session_completed",
            "total_processing_events": len(session.processing_history),
            "synthesis_available": session.synthesis_result is not None
        })
        
        return {
            "session_id": session_id,
            "completed": True,
            "summary": session.get_session_summary(),
            "synthesis": session.synthesis_result
        }
    
    async def list_available_workflows(self) -> Dict[str, Dict[str, Any]]:
        """List available predefined workflows"""
        workflows = {}
        for name, workflow in self.predefined_workflows.items():
            workflows[name] = {
                "name": workflow.name,
                "description": workflow.description,
                "sefirot_sequence": [s.value for s in workflow.sefirot_sequence],
                "flow_pattern": workflow.flow_pattern.value,
                "therapeutic_intent": workflow.therapeutic_intent
            }
        
        return workflows
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for sefirot orchestrator"""
        agent_health = {}
        for sefirot_type, agent in self.agent_pool.items():
            agent_health[sefirot_type.value] = await agent.health_check()
        
        return {
            "active_sessions": len(self.active_sessions),
            "available_agents": len(self.agent_pool),
            "predefined_workflows": len(self.predefined_workflows),
            "agent_health": agent_health,
            "supported_flows": [f.value for f in SefirotFlow],
            "status": "healthy"
        }