"""
Sefirot Integration Layer for DPNR Agent Library
Integrates sefirot agents with existing therapeutic agents
Creates unified therapeutic experience combining mystical framework with psychological modalities
Generated for Phase 1 Sefirot Integration
"""
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
import uuid

from .sefirot_orchestrator import SefirotOrchestrator, SefirotSession
from ..agents.assessment.sefirot_base_agent import SefirotType, SefirotFlow
from ..core.base_agent import BaseAgent, AgentMessage, AgentResponse


class TherapeuticIntegrationSession:
    """Session that combines sefirot processing with existing therapeutic agents"""
    
    def __init__(self, session_id: str, user_id: str, integration_intent: str):
        self.session_id = session_id
        self.user_id = user_id
        self.integration_intent = integration_intent
        self.created_at = datetime.utcnow()
        
        # Integration state
        self.sefirot_session_id: Optional[str] = None
        self.therapeutic_agents: Dict[str, BaseAgent] = {}
        self.processing_history: List[Dict[str, Any]] = []
        self.integration_mapping: Dict[str, List[SefirotType]] = {}
        self.synthesis_results: Dict[str, Any] = {}


class SefirotTherapeuticIntegrator:
    """
    Integrates sefirot agents with existing therapeutic agents
    Creates unified processing that combines mystical wisdom with psychological modalities
    """
    
    def __init__(self, sefirot_orchestrator: SefirotOrchestrator):
        self.sefirot_orchestrator = sefirot_orchestrator
        self.logger = logging.getLogger(__name__)
        self.active_sessions: Dict[str, TherapeuticIntegrationSession] = {}
        
        # Define integration mappings
        self.agent_sefirot_mappings = self._initialize_agent_sefirot_mappings()
        self.therapeutic_workflows = self._initialize_therapeutic_workflows()
    
    def _initialize_agent_sefirot_mappings(self) -> Dict[str, List[SefirotType]]:
        """Initialize mappings between therapeutic agents and sefirot"""
        return {
            # IFS (Internal Family Systems) - works with compassion and balance
            "ifs_agent": [SefirotType.CHESED, SefirotType.TIFERET, SefirotType.YESOD],
            
            # Shadow Work - works with strength and integration
            "shadow_work_agent": [SefirotType.GEVURAH, SefirotType.TIFERET, SefirotType.MALCHUT],
            
            # Growth Tracker - works with foundation and manifestation
            "growth_tracker_agent": [SefirotType.YESOD, SefirotType.MALCHUT],
            
            # Digital Twin - works with beauty and manifestation  
            "digital_twin_agent": [SefirotType.TIFERET, SefirotType.MALCHUT],
            
            # PaRDeS Reflection - works with understanding and wisdom
            "pardes_reflection_agent": [SefirotType.BINAH, SefirotType.CHOCHMAH, SefirotType.TIFERET],
            
            # Narrative Therapy - works with communication and manifestation
            "narrative_therapy_agent": [SefirotType.HOD, SefirotType.MALCHUT],
            
            # General therapeutic processing - balanced approach
            "general_therapy": [SefirotType.TIFERET, SefirotType.YESOD, SefirotType.MALCHUT]
        }
    
    def _initialize_therapeutic_workflows(self) -> Dict[str, Dict[str, Any]]:
        """Initialize integrated therapeutic workflows"""
        return {
            "ifs_integration": {
                "description": "IFS parts work enhanced with sefirot wisdom",
                "sequence": ["ifs_processing", "sefirot_integration", "synthesis"],
                "sefirot_flow": SefirotFlow.DESCENDING,
                "focus": "Integrate parts work with divine compassion and grounding"
            },
            "shadow_integration": {
                "description": "Shadow work enhanced with sefirot strength and balance",
                "sequence": ["shadow_processing", "sefirot_integration", "synthesis"],
                "sefirot_flow": SefirotFlow.BALANCING,
                "focus": "Balance shadow integration with compassionate strength"
            },
            "growth_manifestation": {
                "description": "Growth tracking enhanced with practical manifestation",
                "sequence": ["growth_analysis", "sefirot_integration", "synthesis"],
                "sefirot_flow": SefirotFlow.ASCENDING,
                "focus": "Ground growth insights in practical manifestation"
            },
            "holistic_reflection": {
                "description": "Comprehensive therapeutic processing with mystical integration",
                "sequence": ["therapeutic_processing", "sefirot_integration", "synthesis"],
                "sefirot_flow": SefirotFlow.DESCENDING,
                "focus": "Integrate all therapeutic modalities through sefirot wisdom"
            }
        }
    
    async def create_integration_session(self, user_id: str, integration_intent: str,
                                       therapeutic_agents: List[str],
                                       workflow_name: Optional[str] = None) -> str:
        """Create integrated therapeutic session"""
        
        session_id = str(uuid.uuid4())
        session = TherapeuticIntegrationSession(session_id, user_id, integration_intent)
        
        # Determine sefirot mapping for therapeutic agents
        relevant_sefirot = set()
        for agent_name in therapeutic_agents:
            if agent_name in self.agent_sefirot_mappings:
                relevant_sefirot.update(self.agent_sefirot_mappings[agent_name])
                session.integration_mapping[agent_name] = self.agent_sefirot_mappings[agent_name]
        
        # Create sefirot session with relevant sefirot
        if relevant_sefirot:
            session.sefirot_session_id = await self.sefirot_orchestrator.create_session(
                user_id=user_id,
                therapeutic_intent=f"Integrate with {', '.join(therapeutic_agents)}: {integration_intent}",
                custom_sefirot=list(relevant_sefirot)
            )
        
        self.active_sessions[session_id] = session
        
        self.logger.info(f"Created integration session {session_id} with agents {therapeutic_agents}")
        
        return session_id
    
    async def process_integrated_therapeutic_request(self, session_id: str, user_input: str,
                                                   therapeutic_agent: str,
                                                   context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process request through therapeutic agent enhanced with sefirot wisdom"""
        
        if session_id not in self.active_sessions:
            raise ValueError(f"Integration session {session_id} not found")
        
        session = self.active_sessions[session_id]
        context = context or {}
        
        try:
            # Step 1: Process through therapeutic agent (simulated - would call actual agent)
            therapeutic_result = await self._process_through_therapeutic_agent(
                therapeutic_agent, user_input, context
            )
            
            # Step 2: Enhance with sefirot processing
            if session.sefirot_session_id:
                # Add therapeutic context to sefirot processing
                sefirot_context = {
                    **context,
                    "therapeutic_agent": therapeutic_agent,
                    "therapeutic_result": therapeutic_result,
                    "integration_intent": session.integration_intent
                }
                
                sefirot_result = await self.sefirot_orchestrator.process_therapeutic_request(
                    session_id=session.sefirot_session_id,
                    user_input=user_input,
                    context=sefirot_context
                )
            else:
                sefirot_result = {"success": False, "error": "No sefirot session available"}
            
            # Step 3: Synthesize therapeutic and sefirot results
            integrated_result = await self._synthesize_integrated_results(
                therapeutic_result, sefirot_result, session, user_input
            )
            
            # Record processing event
            session.processing_history.append({
                "timestamp": datetime.utcnow().isoformat(),
                "therapeutic_agent": therapeutic_agent,
                "user_input_length": len(user_input),
                "therapeutic_success": therapeutic_result.get("success", False),
                "sefirot_success": sefirot_result.get("success", False),
                "integration_confidence": integrated_result.get("integration_confidence", 0.0)
            })
            
            return integrated_result
            
        except Exception as e:
            self.logger.error(f"Integration processing failed for session {session_id}: {e}")
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id
            }
    
    async def _process_through_therapeutic_agent(self, agent_name: str, user_input: str, 
                                               context: Dict[str, Any]) -> Dict[str, Any]:
        """Process through therapeutic agent (placeholder - would call actual agent)"""
        
        # This is a placeholder that simulates therapeutic agent processing
        # In real implementation, this would call the actual therapeutic agents
        
        agent_responses = {
            "ifs_agent": {
                "success": True,
                "agent_type": "ifs",
                "response": f"IFS processing of user input reveals parts work opportunities",
                "insights": ["Parts integration needed", "Self-energy cultivation"],
                "guidance": ["Practice parts dialogue", "Strengthen self-leadership"],
                "confidence": 0.82
            },
            "shadow_work_agent": {
                "success": True,
                "agent_type": "shadow_work",
                "response": f"Shadow work reveals projection patterns and integration opportunities",
                "insights": ["Shadow projections identified", "Integration pathways available"],
                "guidance": ["Own projections consciously", "Channel shadow energy creatively"],
                "confidence": 0.78
            },
            "growth_tracker_agent": {
                "success": True,
                "agent_type": "growth_tracker",
                "response": f"Growth analysis shows development patterns and next steps",
                "insights": ["Growth momentum identified", "Development areas clarified"],
                "guidance": ["Focus on key growth domains", "Create accountability structures"],
                "confidence": 0.85
            },
            "digital_twin_agent": {
                "success": True,
                "agent_type": "digital_twin",
                "response": f"Digital twin reflects current development stage and evolution potential",
                "insights": ["Soul archetype evolution ready", "Integration opportunities available"],
                "guidance": ["Embody current archetype fully", "Prepare for next evolution stage"],
                "confidence": 0.80
            }
        }
        
        return agent_responses.get(agent_name, {
            "success": True,
            "agent_type": agent_name,
            "response": f"Therapeutic processing through {agent_name}",
            "insights": ["General therapeutic insights"],
            "guidance": ["General therapeutic guidance"],
            "confidence": 0.75
        })
    
    async def _synthesize_integrated_results(self, therapeutic_result: Dict[str, Any],
                                           sefirot_result: Dict[str, Any],
                                           session: TherapeuticIntegrationSession,
                                           user_input: str) -> Dict[str, Any]:
        """Synthesize therapeutic and sefirot results"""
        
        # Check if both processing succeeded
        therapeutic_success = therapeutic_result.get("success", False)
        sefirot_success = sefirot_result.get("success", False)
        
        if not therapeutic_success and not sefirot_success:
            return {
                "success": False,
                "error": "Both therapeutic and sefirot processing failed",
                "session_id": session.session_id
            }
        
        # Extract key elements
        therapeutic_insights = therapeutic_result.get("insights", [])
        therapeutic_guidance = therapeutic_result.get("guidance", [])
        
        sefirot_synthesis = sefirot_result.get("synthesis", {}) if sefirot_success else {}
        sefirot_insights = sefirot_synthesis.get("unified_insights", [])
        sefirot_guidance = sefirot_synthesis.get("integration_guidance", [])
        
        # Create integrated synthesis
        integrated_synthesis = await self._create_integrated_synthesis(
            therapeutic_result, sefirot_result, session
        )
        
        # Calculate integration confidence
        therapeutic_confidence = therapeutic_result.get("confidence", 0.0)
        sefirot_confidence = sefirot_result.get("synthesis", {}).get("overall_confidence", 0.0)
        integration_confidence = (therapeutic_confidence + sefirot_confidence) / 2 if sefirot_success else therapeutic_confidence
        
        return {
            "success": True,
            "session_id": session.session_id,
            "integration_synthesis": integrated_synthesis,
            "therapeutic_component": {
                "agent_type": therapeutic_result.get("agent_type"),
                "insights": therapeutic_insights,
                "guidance": therapeutic_guidance,
                "confidence": therapeutic_confidence
            },
            "sefirot_component": {
                "synthesis_available": sefirot_success,
                "insights": sefirot_insights,
                "guidance": sefirot_guidance,
                "mystical_integration": sefirot_synthesis.get("synthesis_narrative", "")
            },
            "unified_insights": self._unify_insights(therapeutic_insights + sefirot_insights),
            "integrated_guidance": self._integrate_guidance(therapeutic_guidance + sefirot_guidance),
            "integration_confidence": integration_confidence,
            "next_steps": await self._recommend_integrated_next_steps(therapeutic_result, sefirot_result),
            "processing_summary": {
                "therapeutic_processing": therapeutic_success,
                "sefirot_processing": sefirot_success,
                "integration_quality": "high" if integration_confidence > 0.8 else "moderate"
            }
        }
    
    async def _create_integrated_synthesis(self, therapeutic_result: Dict[str, Any],
                                         sefirot_result: Dict[str, Any],
                                         session: TherapeuticIntegrationSession) -> str:
        """Create narrative synthesis of therapeutic and mystical processing"""
        
        agent_type = therapeutic_result.get("agent_type", "therapeutic")
        therapeutic_focus = therapeutic_result.get("response", "")
        
        sefirot_synthesis = sefirot_result.get("synthesis", {})
        mystical_narrative = sefirot_synthesis.get("synthesis_narrative", "")
        
        integration_narrative = f"""
        🌟 **Integrated Therapeutic & Mystical Synthesis**
        
        Your journey has been honored through both psychological wisdom and mystical understanding. 
        The {agent_type.replace('_', ' ').title()} work reveals the human dimension of your growth, 
        while the sefirot processing illuminates the divine intelligence working through your experience.
        
        **Therapeutic Dimension:**
        {therapeutic_focus[:200]}...
        
        **Mystical Dimension:**
        {mystical_narrative[:200] if mystical_narrative else "Sefirot wisdom processing not available"}...
        
        **Integration Wisdom:**
        When psychological insight meets mystical understanding, transformation becomes both deeply 
        human and divinely guided. Your therapeutic work is not separate from your spiritual evolution - 
        they are two faces of the same sacred journey toward wholeness.
        
        **Unified Path Forward:**
        Your path integrates practical psychological tools with timeless wisdom. This combination 
        creates more powerful and sustainable transformation than either approach alone could provide.
        """
        
        return integration_narrative.strip()
    
    def _unify_insights(self, all_insights: List[str]) -> List[str]:
        """Unify insights from therapeutic and sefirot processing"""
        # Remove duplicates and prioritize most comprehensive insights
        unique_insights = []
        for insight in all_insights:
            if not any(self._insights_similar(insight, existing) for existing in unique_insights):
                unique_insights.append(insight)
        
        return unique_insights[:7]  # Return top 7 unified insights
    
    def _integrate_guidance(self, all_guidance: List[str]) -> List[str]:
        """Integrate guidance from therapeutic and sefirot processing"""
        # Prioritize actionable guidance
        actionable_guidance = []
        reflective_guidance = []
        
        for guidance in all_guidance:
            if any(word in guidance.lower() for word in ["practice", "create", "implement", "start", "do"]):
                actionable_guidance.append(guidance)
            else:
                reflective_guidance.append(guidance)
        
        # Return mix of actionable and reflective guidance
        integrated = actionable_guidance[:4] + reflective_guidance[:3]
        return integrated[:6]
    
    async def _recommend_integrated_next_steps(self, therapeutic_result: Dict[str, Any],
                                             sefirot_result: Dict[str, Any]) -> List[str]:
        """Recommend next steps for integrated work"""
        next_steps = []
        
        # Add therapeutic next steps
        if "guidance" in therapeutic_result:
            next_steps.extend(therapeutic_result["guidance"][:2])
        
        # Add sefirot next steps
        sefirot_next_steps = sefirot_result.get("synthesis", {}).get("next_steps", [])
        next_steps.extend(sefirot_next_steps[:2])
        
        # Add integration-specific next steps
        next_steps.extend([
            "Continue integrating psychological and mystical dimensions of your work",
            "Notice how therapeutic insights are supported by sefirot wisdom",
            "Practice seeing your healing journey as both human and sacred"
        ])
        
        return next_steps[:5]
    
    def _insights_similar(self, insight1: str, insight2: str) -> bool:
        """Check if two insights are similar"""
        # Simple similarity check
        words1 = set(insight1.lower().split())
        words2 = set(insight2.lower().split())
        
        content_words1 = {w for w in words1 if len(w) > 3}
        content_words2 = {w for w in words2 if len(w) > 3}
        
        if not content_words1 or not content_words2:
            return False
        
        intersection = content_words1.intersection(content_words2)
        similarity_ratio = len(intersection) / min(len(content_words1), len(content_words2))
        
        return similarity_ratio > 0.4
    
    async def get_integration_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get integration session information"""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        sefirot_session_info = None
        
        if session.sefirot_session_id:
            sefirot_session_info = await self.sefirot_orchestrator.get_session(session.sefirot_session_id)
        
        return {
            "session_id": session.session_id,
            "user_id": session.user_id,
            "integration_intent": session.integration_intent,
            "created_at": session.created_at.isoformat(),
            "sefirot_session_id": session.sefirot_session_id,
            "sefirot_session_info": sefirot_session_info,
            "integration_mapping": session.integration_mapping,
            "processing_events": len(session.processing_history),
            "synthesis_available": bool(session.synthesis_results)
        }
    
    async def complete_integration_session(self, session_id: str) -> Dict[str, Any]:
        """Complete integration session"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Integration session {session_id} not found")
        
        session = self.active_sessions[session_id]
        
        # Complete sefirot session if exists
        sefirot_completion = None
        if session.sefirot_session_id:
            sefirot_completion = await self.sefirot_orchestrator.complete_session(session.sefirot_session_id)
        
        return {
            "session_id": session_id,
            "completed": True,
            "integration_summary": {
                "processing_events": len(session.processing_history),
                "integration_mapping": session.integration_mapping,
                "sefirot_integration": sefirot_completion is not None
            },
            "sefirot_completion": sefirot_completion
        }
    
    async def list_therapeutic_workflows(self) -> Dict[str, Dict[str, Any]]:
        """List available therapeutic integration workflows"""
        return self.therapeutic_workflows.copy()
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for integration layer"""
        sefirot_health = await self.sefirot_orchestrator.health_check()
        
        return {
            "active_integration_sessions": len(self.active_sessions),
            "agent_sefirot_mappings": len(self.agent_sefirot_mappings),
            "therapeutic_workflows": len(self.therapeutic_workflows),
            "sefirot_orchestrator_health": sefirot_health["status"],
            "integration_status": "healthy"
        }