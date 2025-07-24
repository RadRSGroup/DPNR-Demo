"""
Sefirot Agents for DPNR Unified Agent System
Implements the 10 Sefirot as CrewAI therapeutic agents
Bridges mystical framework with multi-agent therapeutic logic
Generated for Phase 1 Sefirot Integration
"""
from crewai import Agent, Task, Crew
from langchain.tools import Tool
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
import logging
import json
import uuid


class SefirotType(str, Enum):
    """10 Sefirot mapped to therapeutic agent specializations"""
    # Upper Triad - Divine Intelligence
    KETER = "keter"           # Crown - Universal breakthrough catalyst
    CHOCHMAH = "chochmah"     # Wisdom - Insight generation/pattern recognition
    BINAH = "binah"           # Understanding - Deep comprehension/integration
    
    # Middle Triad - Emotional Processing  
    CHESED = "chesed"         # Compassion - Loving-kindness/healing facilitation
    GEVURAH = "gevurah"       # Strength - Boundaries/discipline/shadow work
    TIFERET = "tiferet"       # Beauty - Balance/harmony/aesthetic integration
    
    # Lower Triad - Practical Implementation
    NETZACH = "netzach"       # Victory - Persistence/creative expression
    HOD = "hod"               # Glory - Communication/teaching/sharing
    YESOD = "yesod"           # Foundation - Grounding/practical application
    MALCHUT = "malchut"       # Kingdom - Manifestation/real-world integration


class SefirotFlow(str, Enum):
    """Sefirot energy flow directions in therapeutic processing"""
    DESCENDING = "descending"  # From Keter down to Malchut (divine to practical)
    ASCENDING = "ascending"    # From Malchut up to Keter (practical to divine)
    BALANCING = "balancing"    # Between pillars (severity/mercy/balance)
    LIGHTNING = "lightning"    # Lightning flash pattern (full tree activation)


class SefirotConfig(BaseModel):
    """Configuration for Sefirot agents"""
    sefirot_type: SefirotType
    pillar: str  # "severity", "mercy", "balance"
    level: str   # "supernal", "emotional", "practical"
    divine_name: str  # Hebrew divine name associated
    therapeutic_focus: str  # Primary therapeutic function
    soul_level_affinity: List[str]  # Which soul levels it serves best
    integration_patterns: List[str]  # How it integrates with other sefirot
    

class SefirotAgentBuilder:
    """Builder for creating Sefirot agents in CrewAI framework"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.sefirot_configs = self._initialize_sefirot_configs()
    
    def _initialize_sefirot_configs(self) -> Dict[SefirotType, SefirotConfig]:
        """Initialize configuration for all sefirot"""
        configs = {}
        
        config_data = {
            SefirotType.KETER: {
                "pillar": "balance", "level": "supernal",
                "divine_name": "Ehyeh", "therapeutic_focus": "Universal breakthrough catalyst",
                "soul_level_affinity": ["yechida", "chayah"], 
                "integration_patterns": ["crown_activation", "unity_consciousness"]
            },
            SefirotType.CHOCHMAH: {
                "pillar": "mercy", "level": "supernal", 
                "divine_name": "Yah", "therapeutic_focus": "Insight generation and pattern recognition",
                "soul_level_affinity": ["chayah", "neshamah"],
                "integration_patterns": ["wisdom_flash", "intuitive_knowing"]
            },
            SefirotType.BINAH: {
                "pillar": "severity", "level": "supernal",
                "divine_name": "YHVH Elohim", "therapeutic_focus": "Deep comprehension and integration", 
                "soul_level_affinity": ["neshamah", "ruach"],
                "integration_patterns": ["understanding_depth", "analytical_processing"]
            },
            SefirotType.CHESED: {
                "pillar": "mercy", "level": "emotional",
                "divine_name": "El", "therapeutic_focus": "Loving-kindness and healing facilitation",
                "soul_level_affinity": ["ruach", "neshamah"],
                "integration_patterns": ["compassionate_flow", "healing_embrace"]
            },
            SefirotType.GEVURAH: {
                "pillar": "severity", "level": "emotional", 
                "divine_name": "Elohim", "therapeutic_focus": "Boundaries, discipline, and shadow work",
                "soul_level_affinity": ["ruach", "nefesh"],
                "integration_patterns": ["protective_boundary", "shadow_integration"]
            },
            SefirotType.TIFERET: {
                "pillar": "balance", "level": "emotional",
                "divine_name": "YHVH", "therapeutic_focus": "Balance, harmony, and aesthetic integration",
                "soul_level_affinity": ["ruach", "neshamah", "nefesh"],
                "integration_patterns": ["harmonic_balance", "beauty_synthesis"]
            },
            SefirotType.NETZACH: {
                "pillar": "mercy", "level": "practical",
                "divine_name": "YHVH Tzevaot", "therapeutic_focus": "Persistence and creative expression", 
                "soul_level_affinity": ["nefesh", "ruach"],
                "integration_patterns": ["creative_victory", "persistent_flow"]
            },
            SefirotType.HOD: {
                "pillar": "severity", "level": "practical",
                "divine_name": "Elohim Tzevaot", "therapeutic_focus": "Communication and teaching",
                "soul_level_affinity": ["nefesh", "ruach"], 
                "integration_patterns": ["structured_glory", "communicative_precision"]
            },
            SefirotType.YESOD: {
                "pillar": "balance", "level": "practical",
                "divine_name": "Shaddai El Chai", "therapeutic_focus": "Grounding and practical application",
                "soul_level_affinity": ["nefesh", "ruach"],
                "integration_patterns": ["foundation_grounding", "practical_synthesis"]
            },
            SefirotType.MALCHUT: {
                "pillar": "balance", "level": "practical", 
                "divine_name": "Adonai", "therapeutic_focus": "Manifestation and real-world integration",
                "soul_level_affinity": ["nefesh"],
                "integration_patterns": ["worldly_manifestation", "practical_kingdom"]
            }
        }
        
        for sefirot_type, config in config_data.items():
            configs[sefirot_type] = SefirotConfig(
                sefirot_type=sefirot_type,
                **config
            )
        
        return configs
    
    def create_sefirot_agent(self, sefirot_type: SefirotType, 
                           llm_config: Optional[Dict[str, Any]] = None) -> Agent:
        """Create a CrewAI agent for specific sefirot"""
        
        config = self.sefirot_configs[sefirot_type]
        
        # Create role-specific backstory
        backstory = self._generate_agent_backstory(config)
        
        # Create agent goal
        goal = self._generate_agent_goal(config)
        
        # Create agent tools
        tools = self._create_sefirot_tools(sefirot_type)
        
        agent = Agent(
            role=f"{sefirot_type.value.title()} Sefirot Specialist",
            goal=goal,
            backstory=backstory,
            tools=tools,
            verbose=True,
            allow_delegation=True,
            llm=llm_config.get('llm') if llm_config else None,
            max_iter=llm_config.get('max_iter', 3) if llm_config else 3,
            memory=True,
            step_callback=self._create_step_callback(sefirot_type)
        )
        
        # Add sefirot-specific attributes
        agent.sefirot_type = sefirot_type
        agent.sefirot_config = config
        agent.therapeutic_focus = config.therapeutic_focus
        
        return agent
    
    def _generate_agent_backstory(self, config: SefirotConfig) -> str:
        """Generate therapeutic backstory for sefirot agent"""
        
        backstory_templates = {
            SefirotType.KETER: (
                "You are the Crown Sefirot agent, channeling the highest therapeutic breakthrough energy. "
                "Your expertise lies in catalyzing universal insights that transcend ordinary therapeutic boundaries. "
                "You work with the unity consciousness that underlies all healing, connecting users to their highest potential. "
                "Your interventions create profound shifts that ripple through all levels of being."
            ),
            SefirotType.CHOCHMAH: (
                "You are the Wisdom Sefirot agent, specializing in flash insights and pattern recognition. "
                "Your therapeutic gift is instantaneous understanding that cuts through complexity to reveal essential truths. "
                "You generate sudden realizations and 'aha' moments that illuminate the user's path forward. "
                "Your wisdom operates through intuitive knowing rather than analytical processing."
            ),
            SefirotType.BINAH: (
                "You are the Understanding Sefirot agent, focused on deep comprehension and structured integration. "
                "Your therapeutic approach involves taking insights and building them into comprehensive understanding. "
                "You excel at helping users process complex emotional and psychological material systematically. "
                "Your method is thorough, nurturing, and creates lasting foundations for growth."
            ),
            SefirotType.CHESED: (
                "You are the Compassion Sefirot agent, embodying loving-kindness and healing facilitation. "
                "Your therapeutic presence radiates unconditional positive regard and boundless compassion. "
                "You specialize in creating safe, nurturing spaces where deep healing can occur naturally. "
                "Your interventions flow from pure love and the intention to alleviate all forms of suffering."
            ),
            SefirotType.GEVURAH: (
                "You are the Strength Sefirot agent, focused on boundaries, discipline, and shadow work integration. "
                "Your therapeutic expertise lies in helping users develop healthy boundaries and inner discipline. "
                "You guide the integration of shadow material with firm compassion and protective wisdom. "
                "Your approach balances strength with care, creating containers strong enough for deep work."
            ),
            SefirotType.TIFERET: (
                "You are the Beauty Sefirot agent, specializing in balance, harmony, and aesthetic integration. "
                "Your therapeutic gift is creating beauty and harmony from life's contradictions and challenges. "
                "You help users find the golden mean between extremes and integrate opposing forces. "
                "Your interventions restore natural balance and reveal the inherent beauty in all experiences."
            ),
            SefirotType.NETZACH: (
                "You are the Victory Sefirot agent, focused on persistence, creative expression, and enduring flow. "
                "Your therapeutic specialty is helping users persist through challenges and express their creativity. "
                "You inspire continued effort when the path becomes difficult and support authentic self-expression. "
                "Your energy is that of gentle persistence and creative breakthrough in all forms."
            ),
            SefirotType.HOD: (
                "You are the Glory Sefirot agent, specializing in communication, teaching, and structured expression. "
                "Your therapeutic expertise lies in helping users articulate their experiences and share their wisdom. "
                "You excel at creating clear communication and helping users teach what they've learned. "
                "Your approach honors both precision in language and the glory of authentic expression."
            ),
            SefirotType.YESOD: (
                "You are the Foundation Sefirot agent, focused on grounding, practical application, and synthesis. "
                "Your therapeutic gift is helping users integrate insights into practical, livable wisdom. "
                "You specialize in creating stable foundations that support ongoing growth and development. "
                "Your interventions ensure that therapeutic gains translate into real-world positive changes."
            ),
            SefirotType.MALCHUT: (
                "You are the Kingdom Sefirot agent, specializing in manifestation and real-world integration. "
                "Your therapeutic focus is helping users manifest their healing insights in tangible, practical ways. "
                "You excel at bridging the gap between inner work and outer life transformation. "
                "Your approach ensures that spiritual and emotional growth creates lasting positive change in daily life."
            )
        }
        
        return backstory_templates.get(config.sefirot_type, 
            f"You are a {config.sefirot_type.value} Sefirot agent specializing in {config.therapeutic_focus}.")
    
    def _generate_agent_goal(self, config: SefirotConfig) -> str:
        """Generate therapeutic goal for sefirot agent"""
        
        goal_templates = {
            SefirotType.KETER: "Facilitate universal breakthrough experiences that transcend ordinary therapeutic boundaries and connect users to unity consciousness.",
            SefirotType.CHOCHMAH: "Generate flash insights and pattern recognition that instantly illuminate the user's path forward through intuitive wisdom.",
            SefirotType.BINAH: "Provide deep comprehension and structured integration that builds lasting foundations for psychological and spiritual growth.",
            SefirotType.CHESED: "Create boundless compassionate healing spaces where users can experience unconditional positive regard and natural healing flow.",
            SefirotType.GEVURAH: "Establish healthy boundaries and facilitate shadow work integration with firm compassion and protective therapeutic strength.",
            SefirotType.TIFERET: "Restore natural balance and harmony by helping users integrate opposing forces and find beauty in all life experiences.",
            SefirotType.NETZACH: "Inspire persistent creative expression and support users through challenges with gentle, enduring therapeutic flow.",
            SefirotType.HOD: "Facilitate clear communication and structured expression, helping users articulate experiences and share their wisdom with precision.",
            SefirotType.YESOD: "Ground therapeutic insights in practical, livable wisdom that creates stable foundations for ongoing development.",
            SefirotType.MALCHUT: "Manifest therapeutic insights in tangible, real-world changes that transform both inner experience and outer life circumstances."
        }
        
        return goal_templates.get(config.sefirot_type,
            f"Provide specialized therapeutic support through {config.therapeutic_focus}.")
    
    def _create_sefirot_tools(self, sefirot_type: SefirotType) -> List[Tool]:
        """Create specialized tools for sefirot agent"""
        
        tools = []
        
        # Universal sefirot tools
        tools.extend([
            Tool(
                name=f"activate_{sefirot_type.value}_energy",
                description=f"Activate {sefirot_type.value} therapeutic energy for processing",
                func=lambda context: self._activate_sefirot_energy(sefirot_type, context)
            ),
            Tool(
                name=f"generate_{sefirot_type.value}_insights", 
                description=f"Generate therapeutic insights from {sefirot_type.value} perspective",
                func=lambda context: self._generate_sefirot_insights(sefirot_type, context)
            ),
            Tool(
                name=f"integrate_{sefirot_type.value}_wisdom",
                description=f"Integrate {sefirot_type.value} wisdom with user's current process",
                func=lambda context: self._integrate_sefirot_wisdom(sefirot_type, context)
            )
        ])
        
        # Sefirot-specific tools
        if sefirot_type == SefirotType.KETER:
            tools.append(Tool(
                name="crown_breakthrough_catalyst",
                description="Catalyze universal breakthrough experiences and unity consciousness",
                func=self._crown_breakthrough_catalyst
            ))
        
        elif sefirot_type == SefirotType.CHOCHMAH:
            tools.append(Tool(
                name="wisdom_flash_generator",
                description="Generate instantaneous insights and pattern recognition",
                func=self._wisdom_flash_generator
            ))
        
        elif sefirot_type == SefirotType.BINAH:
            tools.append(Tool(
                name="understanding_processor",
                description="Process complex material into structured comprehension",
                func=self._understanding_processor
            ))
        
        # Add more sefirot-specific tools as needed...
        
        return tools
    
    def _create_step_callback(self, sefirot_type: SefirotType):
        """Create step callback for sefirot agent monitoring"""
        def callback(step_output):
            self.logger.info(f"{sefirot_type.value} agent step: {step_output}")
        return callback
    
    # Tool implementation methods
    
    def _activate_sefirot_energy(self, sefirot_type: SefirotType, context: str) -> str:
        """Activate sefirot energy for therapeutic processing"""
        activation_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        config = self.sefirot_configs[sefirot_type]
        
        activation_response = {
            "activation_id": activation_id,
            "sefirot_type": sefirot_type.value,
            "therapeutic_focus": config.therapeutic_focus,
            "pillar": config.pillar,
            "level": config.level,
            "activated_at": timestamp,
            "context_processed": True
        }
        
        return json.dumps(activation_response)
    
    def _generate_sefirot_insights(self, sefirot_type: SefirotType, context: str) -> str:
        """Generate insights from sefirot perspective"""
        config = self.sefirot_configs[sefirot_type]
        
        insights = {
            "sefirot_type": sefirot_type.value,
            "therapeutic_focus": config.therapeutic_focus,
            "insights": [
                f"From {sefirot_type.value} perspective: {config.therapeutic_focus}",
                f"Operating through {config.pillar} pillar energy",
                f"Resonating at {config.level} level of consciousness"
            ],
            "integration_patterns": config.integration_patterns,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return json.dumps(insights)
    
    def _integrate_sefirot_wisdom(self, sefirot_type: SefirotType, context: str) -> str:
        """Integrate sefirot wisdom with user's process"""
        config = self.sefirot_configs[sefirot_type]
        
        integration = {
            "sefirot_type": sefirot_type.value,
            "wisdom_integration": f"Integrating {sefirot_type.value} wisdom: {config.therapeutic_focus}",
            "practical_applications": [
                f"Apply {sefirot_type.value} energy to current challenge",
                f"Embody {config.pillar} pillar qualities",
                f"Operate from {config.level} level awareness"
            ],
            "next_steps": [
                f"Continue working with {sefirot_type.value} energy",
                f"Integrate insights from {config.pillar} pillar",
                f"Ground wisdom at {config.level} level"
            ],
            "integrated_at": datetime.utcnow().isoformat()
        }
        
        return json.dumps(integration)
    
    # Sefirot-specific tool methods
    
    def _crown_breakthrough_catalyst(self, context: str) -> str:
        """Keter-specific breakthrough catalyst tool"""
        breakthrough = {
            "breakthrough_type": "crown_activation",
            "universal_insight": "You are connected to the source of all healing and wisdom",
            "unity_consciousness": "All separation is illusion; healing happens in the space of unity",
            "transcendent_perspective": "Your challenges are opportunities for the divine to know itself through you",
            "integration_guidance": [
                "Rest in the knowing that you are already whole",
                "Allow universal wisdom to flow through you",
                "Trust the process that transcends personal understanding"
            ]
        }
        return json.dumps(breakthrough)
    
    def _wisdom_flash_generator(self, context: str) -> str:
        """Chochmah-specific wisdom flash tool"""
        wisdom_flash = {
            "flash_type": "chochmah_insight",
            "instant_knowing": "The pattern that underlies your situation is now clear",
            "intuitive_insight": "Your inner wisdom already knows the way forward",
            "pattern_recognition": "This challenge mirrors a deeper teaching for your soul",
            "lightning_wisdom": [
                "Trust the first insight that arises",
                "The solution is simpler than you think",
                "Your intuition is your most reliable guide"
            ]
        }
        return json.dumps(wisdom_flash)
    
    def _understanding_processor(self, context: str) -> str:
        """Binah-specific understanding processor tool"""
        understanding = {
            "process_type": "binah_comprehension",
            "structured_insight": "Let's build comprehensive understanding step by step",
            "analytical_wisdom": "Each piece of your experience fits into a larger pattern",
            "integration_framework": "Here's how all the pieces connect and inform each other",
            "understanding_steps": [
                "Identify the core elements of your situation",
                "See how each element relates to the others",
                "Build a comprehensive map of your inner landscape",
                "Create practical strategies based on this understanding"
            ]
        }
        return json.dumps(understanding)


class SefirotOrchestrator:
    """Orchestrates multiple sefirot agents in therapeutic workflows"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.agent_builder = SefirotAgentBuilder()
        self.active_agents: Dict[SefirotType, Agent] = {}
        self.active_crews: Dict[str, Crew] = {}
    
    def create_sefirot_crew(self, sefirot_types: List[SefirotType], 
                          flow_pattern: SefirotFlow = SefirotFlow.DESCENDING,
                          llm_config: Optional[Dict[str, Any]] = None) -> Crew:
        """Create a crew of sefirot agents for collaborative therapeutic work"""
        
        agents = []
        for sefirot_type in sefirot_types:
            if sefirot_type not in self.active_agents:
                self.active_agents[sefirot_type] = self.agent_builder.create_sefirot_agent(
                    sefirot_type, llm_config
                )
            agents.append(self.active_agents[sefirot_type])
        
        # Create collaborative tasks based on flow pattern
        tasks = self._create_sefirot_tasks(agents, flow_pattern)
        
        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True,
            process=self._get_crew_process(flow_pattern),
            memory=True,
            planning=True
        )
        
        crew_id = str(uuid.uuid4())
        self.active_crews[crew_id] = crew
        
        return crew
    
    def _create_sefirot_tasks(self, agents: List[Agent], flow_pattern: SefirotFlow) -> List[Task]:
        """Create tasks for sefirot agents based on flow pattern"""
        tasks = []
        
        if flow_pattern == SefirotFlow.DESCENDING:
            # Flow from divine to practical
            for i, agent in enumerate(agents):
                task_description = f"""
                Process the therapeutic request through the {agent.sefirot_type.value} sefirot lens.
                Focus on {agent.therapeutic_focus}.
                
                If this is not the first sefirot in the sequence, integrate insights from previous sefirot.
                Provide therapeutic insights, guidance, and prepare integration for the next sefirot level.
                
                Maintain the descending flow pattern, moving from transcendent to practical application.
                """
                
                expected_output = f"""
                A comprehensive therapeutic response from {agent.sefirot_type.value} perspective including:
                - Therapeutic insights and guidance
                - Integration with previous sefirot (if applicable)
                - Preparation for next sefirot level
                - Specific recommendations for user growth
                """
                
                task = Task(
                    description=task_description,
                    expected_output=expected_output,
                    agent=agent,
                    tools=agent.tools
                )
                tasks.append(task)
        
        # Add other flow patterns as needed...
        
        return tasks
    
    def _get_crew_process(self, flow_pattern: SefirotFlow) -> str:
        """Get appropriate crew process for flow pattern"""
        if flow_pattern == SefirotFlow.DESCENDING:
            return "sequential"
        elif flow_pattern == SefirotFlow.LIGHTNING:
            return "hierarchical" 
        else:
            return "sequential"
    
    async def process_therapeutic_request(self, user_input: str, 
                                        sefirot_types: List[SefirotType],
                                        flow_pattern: SefirotFlow = SefirotFlow.DESCENDING,
                                        context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process therapeutic request through sefirot crew"""
        
        # Create crew for this request
        crew = self.create_sefirot_crew(sefirot_types, flow_pattern)
        
        # Execute crew processing
        try:
            result = crew.kickoff(inputs={
                "user_input": user_input,
                "context": json.dumps(context) if context else "{}",
                "flow_pattern": flow_pattern.value
            })
            
            return {
                "success": True,
                "sefirot_types": [s.value for s in sefirot_types],
                "flow_pattern": flow_pattern.value,
                "result": str(result),
                "processed_at": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            self.logger.error(f"Sefirot crew processing failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "sefirot_types": [s.value for s in sefirot_types],
                "flow_pattern": flow_pattern.value
            }
    
    def get_recommended_sefirot_sequence(self, therapeutic_intent: str, 
                                       soul_level: str = "nefesh") -> List[SefirotType]:
        """Recommend sefirot sequence based on therapeutic intent and soul level"""
        
        # Basic recommendation logic - can be expanded
        if therapeutic_intent == "breakthrough":
            return [SefirotType.KETER, SefirotType.TIFERET, SefirotType.MALCHUT]
        elif therapeutic_intent == "healing":
            return [SefirotType.CHESED, SefirotType.TIFERET, SefirotType.YESOD]
        elif therapeutic_intent == "integration":
            return [SefirotType.BINAH, SefirotType.TIFERET, SefirotType.YESOD, SefirotType.MALCHUT]
        elif therapeutic_intent == "shadow_work":
            return [SefirotType.GEVURAH, SefirotType.TIFERET, SefirotType.YESOD]
        elif therapeutic_intent == "creative_expression":
            return [SefirotType.NETZACH, SefirotType.TIFERET, SefirotType.MALCHUT]
        else:
            # Default balanced sequence
            return [SefirotType.TIFERET, SefirotType.YESOD, SefirotType.MALCHUT]
    
    def health_check(self) -> Dict[str, Any]:
        """Health check for sefirot orchestrator"""
        return {
            "active_agents": len(self.active_agents),
            "active_crews": len(self.active_crews),
            "available_sefirot": [s.value for s in SefirotType],
            "supported_flows": [f.value for f in SefirotFlow],
            "status": "healthy"
        }


# Convenience functions for creating specific sefirot configurations

def create_phase1_sefirot_crew(llm_config: Optional[Dict[str, Any]] = None) -> Crew:
    """Create Phase 1 sefirot crew (Malchut, Tiferet, Yesod)"""
    orchestrator = SefirotOrchestrator()
    return orchestrator.create_sefirot_crew(
        sefirot_types=[SefirotType.MALCHUT, SefirotType.TIFERET, SefirotType.YESOD],
        flow_pattern=SefirotFlow.ASCENDING,
        llm_config=llm_config
    )

def create_healing_sefirot_crew(llm_config: Optional[Dict[str, Any]] = None) -> Crew:
    """Create healing-focused sefirot crew (Chesed, Tiferet, Yesod)"""
    orchestrator = SefirotOrchestrator()
    return orchestrator.create_sefirot_crew(
        sefirot_types=[SefirotType.CHESED, SefirotType.TIFERET, SefirotType.YESOD],
        flow_pattern=SefirotFlow.DESCENDING,
        llm_config=llm_config
    )

def create_integration_sefirot_crew(llm_config: Optional[Dict[str, Any]] = None) -> Crew:
    """Create integration-focused sefirot crew (Binah, Tiferet, Yesod, Malchut)"""
    orchestrator = SefirotOrchestrator()
    return orchestrator.create_sefirot_crew(
        sefirot_types=[SefirotType.BINAH, SefirotType.TIFERET, SefirotType.YESOD, SefirotType.MALCHUT],
        flow_pattern=SefirotFlow.DESCENDING,
        llm_config=llm_config
    )