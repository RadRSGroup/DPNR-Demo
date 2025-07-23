"""
Lightning Flow Processor for DPNR Platform
Implements rapid full-tree sefirot activation for breakthrough therapeutic experiences
The Lightning Flash - instantaneous activation of all 10 sefirot in sacred sequence
Generated for Advanced Phase 2 Sefirot Integration
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from enum import Enum
import uuid

from .sefirot_orchestrator import SefirotOrchestrator
from .advanced_sefirot_patterns import AdvancedSefirotPatternEngine
from ..agents.assessment.sefirot_base_agent import SefirotType, SefirotFlow


class LightningIntensity(str, Enum):
    """Intensity levels for lightning flow processing"""
    GENTLE = "gentle"           # Gradual activation for sensitive users
    MODERATE = "moderate"       # Standard lightning flow
    INTENSE = "intense"         # Rapid, powerful activation
    BREAKTHROUGH = "breakthrough" # Maximum intensity for major breakthroughs


class LightningPathway(str, Enum):
    """Different pathways for lightning flow"""
    CLASSIC_FLASH = "classic_flash"       # Traditional Keter→Malchut lightning path
    ASCENDING_FLAME = "ascending_flame"   # Malchut→Keter ascending path  
    HEART_CENTERED = "heart_centered"     # Tiferet as starting point
    PILLAR_CASCADE = "pillar_cascade"     # Down each pillar sequentially
    SPIRAL_AWAKENING = "spiral_awakening" # Spiral pattern activation


class LightningFlowSession:
    """Represents a lightning flow processing session"""
    
    def __init__(self, session_id: str, user_id: str, pathway: LightningPathway, 
                 intensity: LightningIntensity):
        self.session_id = session_id
        self.user_id = user_id
        self.pathway = pathway
        self.intensity = intensity
        self.created_at = datetime.utcnow()
        
        # Flow state
        self.sefirot_sequence = self._determine_sefirot_sequence()
        self.activation_timings = self._calculate_activation_timings()
        self.current_phase = 0
        self.sefirot_activations: Dict[SefirotType, Dict[str, Any]] = {}
        self.breakthrough_threshold = 0.85  # Confidence threshold for breakthrough
        
        # Safety mechanisms
        self.max_processing_time = timedelta(minutes=30)
        self.safety_checks_enabled = True
        self.integration_pauses = self._determine_integration_pauses()
    
    def _determine_sefirot_sequence(self) -> List[SefirotType]:
        """Determine sefirot activation sequence based on pathway"""
        sequences = {
            LightningPathway.CLASSIC_FLASH: [
                SefirotType.KETER, SefirotType.CHOCHMAH, SefirotType.BINAH,
                SefirotType.CHESED, SefirotType.GEVURAH, SefirotType.TIFERET,
                SefirotType.NETZACH, SefirotType.HOD, SefirotType.YESOD, SefirotType.MALCHUT
            ],
            LightningPathway.ASCENDING_FLAME: [
                SefirotType.MALCHUT, SefirotType.YESOD, SefirotType.HOD, SefirotType.NETZACH,
                SefirotType.TIFERET, SefirotType.GEVURAH, SefirotType.CHESED,
                SefirotType.BINAH, SefirotType.CHOCHMAH, SefirotType.KETER
            ],
            LightningPathway.HEART_CENTERED: [
                SefirotType.TIFERET, SefirotType.CHESED, SefirotType.GEVURAH,
                SefirotType.YESOD, SefirotType.MALCHUT, SefirotType.BINAH, SefirotType.CHOCHMAH,
                SefirotType.NETZACH, SefirotType.HOD, SefirotType.KETER
            ],
            LightningPathway.PILLAR_CASCADE: [
                SefirotType.KETER, SefirotType.TIFERET, SefirotType.YESOD, SefirotType.MALCHUT,
                SefirotType.CHOCHMAH, SefirotType.CHESED, SefirotType.NETZACH,
                SefirotType.BINAH, SefirotType.GEVURAH, SefirotType.HOD
            ],
            LightningPathway.SPIRAL_AWAKENING: [
                SefirotType.MALCHUT, SefirotType.TIFERET, SefirotType.KETER,
                SefirotType.YESOD, SefirotType.CHESED, SefirotType.BINAH,
                SefirotType.HOD, SefirotType.GEVURAH, SefirotType.CHOCHMAH, SefirotType.NETZACH
            ]
        }
        return sequences.get(self.pathway, sequences[LightningPathway.CLASSIC_FLASH])
    
    def _calculate_activation_timings(self) -> List[float]:
        """Calculate timing intervals between sefirot activations"""
        base_intervals = {
            LightningIntensity.GENTLE: [3.0, 2.5, 2.0] * 4,      # Longer pauses
            LightningIntensity.MODERATE: [2.0, 1.5, 1.0] * 4,    # Standard timing
            LightningIntensity.INTENSE: [1.0, 0.8, 0.5] * 4,     # Rapid activation
            LightningIntensity.BREAKTHROUGH: [0.5, 0.3, 0.1] * 4  # Near-instantaneous
        }
        
        intervals = base_intervals.get(self.intensity, base_intervals[LightningIntensity.MODERATE])
        return intervals[:len(self.sefirot_sequence)]
    
    def _determine_integration_pauses(self) -> List[int]:
        """Determine where to pause for integration"""
        if self.intensity == LightningIntensity.GENTLE:
            return [2, 5, 7]  # More frequent pauses
        elif self.intensity == LightningIntensity.MODERATE:
            return [3, 6]     # Standard pauses
        elif self.intensity == LightningIntensity.INTENSE:
            return [5]        # One mid-point pause
        else:
            return []         # No pauses for breakthrough intensity


class LightningFlowProcessor:
    """
    Processes lightning flow sefirot activations for breakthrough experiences
    Manages rapid full-tree activation with safety mechanisms and integration support
    """
    
    def __init__(self, orchestrator: SefirotOrchestrator):
        self.orchestrator = orchestrator
        self.logger = logging.getLogger(__name__)
        self.active_lightning_sessions: Dict[str, LightningFlowSession] = {}
        self.pathway_descriptions = self._initialize_pathway_descriptions()
        self.safety_protocols = self._initialize_safety_protocols()
    
    def _initialize_pathway_descriptions(self) -> Dict[LightningPathway, Dict[str, Any]]:
        """Initialize descriptions for different lightning pathways"""
        return {
            LightningPathway.CLASSIC_FLASH: {
                "name": "Classic Lightning Flash",
                "description": "Traditional Keter-to-Malchut divine lightning path",
                "focus": "Channel divine wisdom into practical manifestation",
                "best_for": "Spiritual breakthroughs and divine connection",
                "caution_level": "high"
            },
            LightningPathway.ASCENDING_FLAME: {
                "name": "Ascending Sacred Flame", 
                "description": "Earth-to-heaven ascending spiritual fire",
                "focus": "Transform earthly experience into divine wisdom",
                "best_for": "Transmuting difficulties into spiritual gold",
                "caution_level": "moderate"
            },
            LightningPathway.HEART_CENTERED: {
                "name": "Heart-Centered Activation",
                "description": "Begin from heart center and radiate outward",
                "focus": "Love-based transformation and heart opening",
                "best_for": "Relationship healing and emotional integration",
                "caution_level": "low"
            },
            LightningPathway.PILLAR_CASCADE: {
                "name": "Pillar Cascade Flow",
                "description": "Sequential activation down each pillar",
                "focus": "Balanced development across all aspects",
                "best_for": "Comprehensive spiritual development",
                "caution_level": "moderate"
            },
            LightningPathway.SPIRAL_AWAKENING: {
                "name": "Spiral Awakening Pattern",
                "description": "Spiral pattern connecting all sefirot",
                "focus": "Integrated awakening and wholeness",
                "best_for": "Unity consciousness and integration",
                "caution_level": "high"
            }
        }
    
    def _initialize_safety_protocols(self) -> Dict[str, Any]:
        """Initialize safety protocols for lightning flow"""
        return {
            "max_session_duration": timedelta(minutes=45),
            "confidence_monitoring": True,
            "integration_checkpoints": True,
            "emergency_grounding": True,
            "user_consent_required": True,
            "therapist_supervision_recommended": True
        }
    
    async def initiate_lightning_flow(self, user_id: str, pathway: LightningPathway,
                                    intensity: LightningIntensity, user_input: str,
                                    context: Dict[str, Any],
                                    consent_confirmed: bool = False) -> Dict[str, Any]:
        """Initiate lightning flow processing session"""
        
        # Safety check - require explicit consent
        if not consent_confirmed:
            return {
                "success": False,
                "error": "Lightning flow requires explicit user consent due to intensity",
                "consent_required": True,
                "pathway_info": self.pathway_descriptions[pathway]
            }
        
        # Create lightning session
        session_id = str(uuid.uuid4())
        lightning_session = LightningFlowSession(session_id, user_id, pathway, intensity)
        
        # Create underlying orchestrator session
        orchestrator_session_id = await self.orchestrator.create_session(
            user_id=user_id,
            therapeutic_intent=f"Lightning Flow: {pathway.value} at {intensity.value} intensity",
            custom_sefirot=lightning_session.sefirot_sequence
        )
        
        lightning_session.orchestrator_session_id = orchestrator_session_id
        self.active_lightning_sessions[session_id] = lightning_session
        
        try:
            # Execute lightning flow
            result = await self._execute_lightning_flow(
                lightning_session, user_input, context
            )
            
            return {
                "success": True,
                "lightning_session_id": session_id,
                "pathway": pathway.value,
                "intensity": intensity.value,
                "result": result,
                "processing_summary": {
                    "sefirot_activated": len(result.get("sefirot_activations", [])),
                    "breakthrough_achieved": result.get("breakthrough_achieved", False),
                    "integration_quality": result.get("integration_quality", "unknown"),
                    "total_processing_time": result.get("total_processing_time", 0.0)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Lightning flow failed: {e}")
            
            # Emergency grounding
            await self._emergency_grounding(lightning_session, str(e))
            
            return {
                "success": False,
                "error": str(e),
                "lightning_session_id": session_id,
                "emergency_grounding_applied": True
            }
    
    async def _execute_lightning_flow(self, session: LightningFlowSession,
                                    user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the lightning flow activation sequence"""
        
        start_time = datetime.utcnow()
        sefirot_results = []
        cumulative_context = context.copy()
        breakthrough_achieved = False
        
        self.logger.info(f"Starting lightning flow: {session.pathway.value} at {session.intensity.value}")
        
        # Process each sefirot in sequence
        for i, sefirot_type in enumerate(session.sefirot_sequence):
            
            # Safety check - time limit
            if datetime.utcnow() - start_time > session.max_processing_time:
                self.logger.warning(f"Lightning flow time limit reached at sefirot {i+1}")
                break
            
            # Integration pause if scheduled
            if i in session.integration_pauses:
                await self._integration_pause(session, sefirot_results)
            
            # Prepare sefirot context
            sefirot_context = {
                **cumulative_context,
                "lightning_flow": True,
                "pathway": session.pathway.value,
                "intensity": session.intensity.value,
                "sequence_position": i + 1,
                "total_sefirot": len(session.sefirot_sequence),
                "previous_activations": sefirot_results,
                "lightning_energy": self._calculate_lightning_energy(i, session)
            }
            
            # Process through sefirot
            sefirot_result = await self._process_lightning_sefirot(
                sefirot_type, session, user_input, sefirot_context
            )
            
            sefirot_results.append(sefirot_result)
            
            # Update cumulative context
            cumulative_context[f"sefirot_{i+1}_result"] = sefirot_result
            
            # Check for breakthrough
            if sefirot_result.get("confidence", 0.0) >= session.breakthrough_threshold:
                breakthrough_achieved = True
                self.logger.info(f"Breakthrough achieved at {sefirot_type.value}")
            
            # Wait for next activation (if not last)
            if i < len(session.sefirot_sequence) - 1:
                await asyncio.sleep(session.activation_timings[i])
        
        # Final integration and synthesis
        lightning_synthesis = await self._synthesize_lightning_flow(
            sefirot_results, session, user_input, context
        )
        
        total_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "sefirot_activations": sefirot_results,
            "lightning_synthesis": lightning_synthesis,
            "breakthrough_achieved": breakthrough_achieved,
            "sefirot_completed": len(sefirot_results),
            "total_processing_time": total_time,
            "integration_quality": self._assess_integration_quality(sefirot_results),
            "pathway": session.pathway.value,
            "intensity": session.intensity.value
        }
    
    async def _process_lightning_sefirot(self, sefirot_type: SefirotType,
                                       session: LightningFlowSession, user_input: str,
                                       context: Dict[str, Any]) -> Dict[str, Any]:
        """Process single sefirot in lightning flow context"""
        
        # Get agent if available
        if sefirot_type not in self.orchestrator.agent_pool:
            return {
                "sefirot_type": sefirot_type.value,
                "success": False,
                "error": f"Sefirot {sefirot_type.value} not available",
                "confidence": 0.0,
                "lightning_energy": context.get("lightning_energy", 0.5)
            }
        
        agent = self.orchestrator.agent_pool[sefirot_type]
        
        # Create lightning-enhanced message
        from ..core.base_agent import AgentMessage
        
        message = AgentMessage(
            message_id=str(uuid.uuid4()),
            sender_id="lightning_flow_processor",
            recipient_id=agent.agent_id,
            message_type="lightning_flow",
            payload={
                "action": "process_therapeutic_request",
                "data": {
                    "user_input": user_input,
                    "context": context
                }
            }
        )
        
        # Process with timing
        process_start = datetime.utcnow()
        response = await agent.process(message)
        process_time = (datetime.utcnow() - process_start).total_seconds()
        
        return {
            "sefirot_type": sefirot_type.value,
            "success": response.success,
            "response": response.data if response.success else None,
            "confidence": response.confidence or 0.0,
            "processing_time": process_time,
            "lightning_energy": context.get("lightning_energy", 0.5),
            "error": response.error if not response.success else None
        }
    
    def _calculate_lightning_energy(self, position: int, session: LightningFlowSession) -> float:
        """Calculate lightning energy level for current position"""
        
        # Energy patterns based on pathway
        if session.pathway == LightningPathway.CLASSIC_FLASH:
            # High at beginning, moderate in middle, high at end
            total = len(session.sefirot_sequence)
            if position < total * 0.2:
                return 0.9  # High divine energy
            elif position > total * 0.8:
                return 0.85  # High manifestation energy
            else:
                return 0.7  # Moderate flow energy
        
        elif session.pathway == LightningPathway.ASCENDING_FLAME:
            # Gradually increasing energy
            return 0.5 + (position / len(session.sefirot_sequence)) * 0.4
        
        elif session.pathway == LightningPathway.HEART_CENTERED:
            # High at heart, moderate elsewhere
            return 0.9 if position == 0 else 0.7
        
        else:
            # Default moderate energy
            return 0.7
    
    async def _integration_pause(self, session: LightningFlowSession, 
                               results_so_far: List[Dict[str, Any]]):
        """Pause for integration during lightning flow"""
        
        self.logger.info(f"Integration pause at position {len(results_so_far)}")
        
        # Calculate pause duration based on intensity
        pause_durations = {
            LightningIntensity.GENTLE: 10.0,
            LightningIntensity.MODERATE: 5.0,
            LightningIntensity.INTENSE: 2.0,
            LightningIntensity.BREAKTHROUGH: 0.5
        }
        
        pause_duration = pause_durations.get(session.intensity, 5.0)
        await asyncio.sleep(pause_duration)
    
    async def _synthesize_lightning_flow(self, sefirot_results: List[Dict[str, Any]],
                                       session: LightningFlowSession, user_input: str,
                                       context: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize results from lightning flow"""
        
        successful_results = [r for r in sefirot_results if r.get("success")]
        
        # Calculate lightning synthesis
        lightning_narrative = await self._create_lightning_narrative(
            successful_results, session, user_input
        )
        
        # Extract unified insights
        all_insights = []
        for result in successful_results:
            response_data = result.get("response", {})
            insights = response_data.get("insights", [])
            all_insights.extend(insights)
        
        # Create lightning integration guidance
        lightning_guidance = await self._create_lightning_integration_guidance(
            successful_results, session
        )
        
        # Assess transformation level
        transformation_level = await self._assess_transformation_level(successful_results)
        
        return {
            "lightning_narrative": lightning_narrative,
            "unified_insights": self._unify_lightning_insights(all_insights),
            "lightning_integration_guidance": lightning_guidance,
            "transformation_level": transformation_level,
            "sefirot_activated": len(successful_results),
            "pathway_completion": len(successful_results) / len(session.sefirot_sequence),
            "average_confidence": sum(r.get("confidence", 0) for r in successful_results) / len(successful_results) if successful_results else 0,
            "breakthrough_points": [r["sefirot_type"] for r in successful_results if r.get("confidence", 0) >= session.breakthrough_threshold]
        }
    
    async def _create_lightning_narrative(self, results: List[Dict[str, Any]],
                                        session: LightningFlowSession, 
                                        user_input: str) -> str:
        """Create narrative for lightning flow experience"""
        
        pathway_name = self.pathway_descriptions[session.pathway]["name"]
        sefirot_names = [r["sefirot_type"] for r in results if r.get("success")]
        
        narrative = f"""
        ⚡ **{pathway_name} - Divine Lightning Activation**
        
        You have journeyed through the sacred lightning path, activating {len(sefirot_names)} sefirot 
        in rapid succession. This is the path of accelerated transformation, where divine energy 
        flows through all dimensions of your being simultaneously.
        
        **Lightning Path Traversed:** {' → '.join(sefirot_names[:5])}{'...' if len(sefirot_names) > 5 else ''}
        
        **Transformation Initiated:** The lightning flash has awakened dormant potentials within you. 
        Each sefirot activated contributes its unique wisdom to your accelerated growth journey.
        
        **Integration Phase:** Now begins the sacred work of integrating these lightning insights 
        into your daily life. The energy activated must be grounded and embodied for lasting transformation.
        
        **Lightning Wisdom:** Divine lightning moves through you not to overwhelm, but to awaken 
        what was always there - your unlimited potential for healing, love, and service.
        """
        
        return narrative.strip()
    
    def _unify_lightning_insights(self, all_insights: List[str]) -> List[str]:
        """Unify insights from lightning flow with special priority for breakthrough insights"""
        
        # Prioritize insights that mention transformation, breakthrough, or awakening
        breakthrough_insights = []
        regular_insights = []
        
        for insight in all_insights:
            if any(word in insight.lower() for word in ["breakthrough", "transformation", "awakening", "lightning", "divine"]):
                breakthrough_insights.append(insight)
            else:
                regular_insights.append(insight)
        
        # Return breakthrough insights first, then regular ones
        unified = breakthrough_insights[:4] + regular_insights[:3]
        return unified[:7]  # Maximum 7 unified insights
    
    async def _create_lightning_integration_guidance(self, results: List[Dict[str, Any]],
                                                   session: LightningFlowSession) -> List[str]:
        """Create integration guidance specific to lightning flow"""
        
        guidance = [
            f"Ground the lightning energy through daily practice and embodied action",
            f"Allow integration time - lightning insights unfold over days and weeks",
            f"Stay connected to your body and emotions as the energy settles",
            f"Share your experience with trusted friends or therapeutic support",
            f"Notice how the {session.pathway.value} energy continues to work within you"
        ]
        
        # Add intensity-specific guidance
        if session.intensity == LightningIntensity.BREAKTHROUGH:
            guidance.append("Powerful breakthrough energy requires extra self-care and integration support")
        elif session.intensity == LightningIntensity.GENTLE:
            guidance.append("Continue building on this gentle foundation with regular practice")
        
        return guidance
    
    async def _assess_transformation_level(self, results: List[Dict[str, Any]]) -> str:
        """Assess level of transformation achieved"""
        
        if not results:
            return "minimal"
        
        avg_confidence = sum(r.get("confidence", 0) for r in results) / len(results)
        completion_rate = len([r for r in results if r.get("success")]) / len(results)
        
        if avg_confidence >= 0.85 and completion_rate >= 0.8:
            return "profound"
        elif avg_confidence >= 0.75 and completion_rate >= 0.7:
            return "significant"
        elif avg_confidence >= 0.65 and completion_rate >= 0.6:
            return "moderate"
        else:
            return "developing"
    
    def _assess_integration_quality(self, results: List[Dict[str, Any]]) -> str:
        """Assess quality of lightning flow integration"""
        
        successful_count = sum(1 for r in results if r.get("success"))
        if successful_count == 0:
            return "poor"
        
        total_confidence = sum(r.get("confidence", 0) for r in results if r.get("success"))
        avg_confidence = total_confidence / successful_count
        completion_ratio = successful_count / len(results)
        
        if avg_confidence >= 0.8 and completion_ratio >= 0.8:
            return "excellent"
        elif avg_confidence >= 0.7 and completion_ratio >= 0.7:
            return "good"
        elif avg_confidence >= 0.6 and completion_ratio >= 0.6:
            return "adequate"
        else:
            return "needs_support"
    
    async def _emergency_grounding(self, session: LightningFlowSession, error: str):
        """Apply emergency grounding procedures"""
        
        self.logger.warning(f"Applying emergency grounding for session {session.session_id}: {error}")
        
        # Record emergency event
        session.emergency_grounding_applied = True
        session.emergency_timestamp = datetime.utcnow()
        session.emergency_reason = error
        
        # Could trigger grounding sequence through Malchut and Yesod
        # Implementation would depend on available agents and safety protocols
    
    async def get_lightning_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get lightning flow session information"""
        
        if session_id not in self.active_lightning_sessions:
            return None
        
        session = self.active_lightning_sessions[session_id]
        
        return {
            "session_id": session.session_id,
            "user_id": session.user_id,
            "pathway": session.pathway.value,
            "intensity": session.intensity.value,
            "created_at": session.created_at.isoformat(),
            "sefirot_sequence": [s.value for s in session.sefirot_sequence],
            "current_phase": session.current_phase,
            "breakthrough_threshold": session.breakthrough_threshold,
            "safety_checks_enabled": session.safety_checks_enabled,
            "emergency_grounding_applied": getattr(session, 'emergency_grounding_applied', False)
        }
    
    async def list_lightning_pathways(self) -> Dict[str, Dict[str, Any]]:
        """List available lightning flow pathways"""
        return self.pathway_descriptions.copy()
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for lightning flow processor"""
        return {
            "active_lightning_sessions": len(self.active_lightning_sessions),
            "available_pathways": len(LightningPathway),
            "intensity_levels": len(LightningIntensity),
            "safety_protocols_active": bool(self.safety_protocols),
            "max_session_duration": str(self.safety_protocols["max_session_duration"]),
            "status": "healthy"
        }