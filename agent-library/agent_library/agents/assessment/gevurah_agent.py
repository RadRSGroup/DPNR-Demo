"""
Gevurah (Strength) Sefirot Agent for DPNR Platform
Specializes in boundaries, discipline, shadow work, and protective strength
The severity pillar that creates structure and refines through loving discipline
Generated for Phase 2 Sefirot Integration
"""
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import uuid

from .sefirot_base_agent import (
    SefirotAgent, SefirotType, SefirotFlow, SefirotActivation, 
    SefirotResponse
)
from ...core.message_types import PersonalityScore


class GevurahAgent(SefirotAgent):
    """
    Gevurah (Strength) Sefirot Agent - Boundaries, Discipline, and Shadow Integration
    
    Specializes in:
    - Creating healthy boundaries and protective structures
    - Facilitating shadow work and difficult truth integration
    - Building discipline and inner strength through challenges
    - Refining character through loving but firm guidance
    """
    
    def __init__(self):
        super().__init__(
            sefirot_type=SefirotType.GEVURAH,
            agent_id="gevurah-strength-agent", 
            name="Gevurah Strength Discipline Agent"
        )
        self.boundary_frameworks = self._initialize_boundary_frameworks()
        self.shadow_work_modalities = self._initialize_shadow_work_modalities()
        self.discipline_structures = self._initialize_discipline_structures()
    
    def _initialize_boundary_frameworks(self) -> Dict[str, Dict[str, Any]]:
        """Initialize frameworks for different types of boundary work"""
        return {
            "protective_boundaries": {
                "description": "Boundaries that protect energy, time, and well-being",
                "core_principles": [
                    "No is a complete sentence",
                    "Your needs matter as much as others' needs",
                    "Boundaries are self-care, not selfish behavior",
                    "Healthy boundaries create space for authentic relationship"
                ],
                "practices": [
                    "Identify energy drains and create protective limits",
                    "Practice saying no without over-explanation or apology",
                    "Notice boundary violations and respond with firm kindness",
                    "Create physical and emotional space for your well-being"
                ],
                "common_challenges": [
                    "Guilt about disappointing others",
                    "Fear of abandonment or rejection",
                    "Confusion about what boundaries to set",
                    "Difficulty maintaining boundaries under pressure"
                ],
                "strength_building": "Build capacity to protect your sacred energy and space"
            },
            "relational_boundaries": {
                "description": "Boundaries that create healthy relationship dynamics",
                "core_principles": [
                    "Each person is responsible for their own emotions",
                    "Love doesn't require self-sacrifice",
                    "Boundaries improve intimacy by creating safety",
                    "You can love someone and still say no to them"
                ],
                "practices": [
                    "Stop trying to manage others' emotions or reactions",
                    "Express needs clearly without demanding others meet them",
                    "Allow others to experience consequences of their choices",
                    "Maintain your values even when others disagree"
                ],
                "common_challenges": [
                    "Codependent patterns and people-pleasing",
                    "Taking responsibility for others' happiness",
                    "Difficulty with conflict or disagreement",
                    "Fear of being seen as mean or uncaring"
                ],
                "strength_building": "Develop strength to be yourself in relationship"
            },
            "inner_boundaries": {
                "description": "Internal boundaries with thoughts, emotions, and impulses",
                "core_principles": [
                    "You are not your thoughts or emotions",
                    "You can observe patterns without being controlled by them",
                    "Inner discipline creates outer freedom",
                    "Structure supports creativity and spontaneity"
                ],
                "practices": [
                    "Notice thoughts and emotions without immediately acting on them",
                    "Create structure and routine that supports your goals",
                    "Practice delayed gratification and impulse control",
                    "Develop witness consciousness that observes inner experience"
                ],
                "common_challenges": [
                    "Reactive patterns and emotional overwhelm",
                    "Lack of structure or self-discipline",
                    "Addiction or compulsive behaviors",
                    "Difficulty with self-regulation"
                ],
                "strength_building": "Build inner authority and self-governance"
            },
            "spiritual_boundaries": {
                "description": "Boundaries that protect spiritual integrity and growth",
                "core_principles": [
                    "Your spiritual path is your own to walk",
                    "Discernment is a spiritual practice",
                    "Not all energy or influence serves your highest good",
                    "Spiritual boundaries protect your connection to the divine"
                ],
                "practices": [
                    "Trust your inner knowing about people and situations",
                    "Protect your energy from spiritual bypassing or manipulation",
                    "Create sacred space and time for your spiritual practice",
                    "Maintain authenticity even when others want you to be different"
                ],
                "common_challenges": [
                    "Spiritual bypassing or avoiding difficult truths",
                    "Giving away power to gurus or authority figures", 
                    "Confusion about spiritual and psychological boundaries",
                    "Difficulty saying no to spiritual or service requests"
                ],
                "strength_building": "Develop spiritual warriorship and divine discernment"
            }
        }
    
    def _initialize_shadow_work_modalities(self) -> Dict[str, Dict[str, Any]]:
        """Initialize shadow work modalities and approaches"""
        return {
            "projection_work": {
                "description": "Reclaiming projections to integrate disowned aspects",
                "process": [
                    "Notice strong emotional reactions to others",
                    "Ask: 'How might this quality exist in me?'",
                    "Own the projection with compassionate honesty",
                    "Integrate the energy constructively"
                ],
                "applications": [
                    "Relationship conflicts and triggers",
                    "Judgments about others' behavior",
                    "Intense attractions or repulsions",
                    "Repeating patterns with different people"
                ],
                "integration_focus": "Transform projected energy into personal power"
            },
            "inner_critic_work": {
                "description": "Transforming inner critic from enemy to ally",
                "process": [
                    "Recognize inner critic's voice and patterns",
                    "Understand critic's protective intention",
                    "Dialogue with critic to understand its fears",
                    "Transform critic into inner coach or guide"
                ],
                "applications": [
                    "Self-attack and harsh self-judgment",
                    "Perfectionism and fear of failure",
                    "Imposter syndrome and self-doubt",
                    "Comparison and not-good-enough patterns"
                ],
                "integration_focus": "Channel critical energy into constructive self-improvement"
            },
            "anger_integration": {
                "description": "Reclaiming healthy anger and assertiveness",
                "process": [
                    "Recognize anger as information about boundaries",
                    "Express anger cleanly without attack or blame",
                    "Use anger's energy for positive change and protection",
                    "Transform rage into righteous action for justice"
                ],
                "applications": [
                    "Suppressed anger and passive-aggression",
                    "Inability to stand up for yourself",
                    "Righteous anger at injustice or harm",
                    "Transforming victim energy into empowerment"
                ],
                "integration_focus": "Channel anger into healthy assertiveness and protection"
            },
            "power_shadow": {
                "description": "Integrating disowned power and authority",
                "process": [
                    "Recognize where you give away personal power",
                    "Reclaim authority over your choices and life direction",
                    "Use power in service of your highest values",
                    "Balance personal power with humility and service"
                ],
                "applications": [
                    "People-pleasing and inability to lead",
                    "Fear of being seen as bossy or demanding",
                    "Difficulty making decisions or taking action",
                    "Patterns of victimization or learned helplessness"
                ],
                "integration_focus": "Embody authentic power in service of love and truth"
            }
        }
    
    def _initialize_discipline_structures(self) -> Dict[str, Dict[str, Any]]:
        """Initialize discipline and structure-building approaches"""
        return {
            "daily_discipline": {
                "description": "Building consistent daily practices that support growth",
                "elements": [
                    "Morning routine that sets positive intention",
                    "Regular spiritual/therapeutic practice",
                    "Healthy habits for body, mind, and spirit",
                    "Evening reflection and gratitude practice"
                ],
                "benefits": [
                    "Increased self-trust and confidence",
                    "Greater resilience during challenging times",
                    "More energy and focus for important goals",
                    "Deeper sense of purpose and meaning"
                ]
            },
            "commitment_strength": {
                "description": "Building capacity to honor commitments to yourself and others",
                "elements": [
                    "Start with small, achievable commitments",
                    "Track progress and celebrate successes",
                    "Learn from failures without self-attack",
                    "Gradually increase commitment complexity"
                ],
                "benefits": [
                    "Stronger sense of personal integrity",
                    "Increased trust from others",
                    "Greater ability to manifest goals",
                    "Deeper self-respect and confidence"
                ]
            },
            "emotional_regulation": {
                "description": "Developing mastery over emotional reactions and responses",
                "elements": [
                    "Pause before reacting to emotional triggers",
                    "Use breathing and mindfulness for emotional balance",
                    "Express emotions appropriately rather than suppressing or exploding",
                    "Learn from emotional patterns and triggers"
                ],
                "benefits": [
                    "Better relationships and communication",
                    "Reduced drama and reactivity",
                    "Increased emotional intelligence",
                    "Greater inner peace and stability"
                ]
            },
            "character_building": {
                "description": "Strengthening moral courage and ethical behavior",
                "elements": [
                    "Act according to values even when difficult",
                    "Tell the truth with compassion and courage",
                    "Stand up for justice and protection of the vulnerable",
                    "Take responsibility for mistakes and make amends"
                ],
                "benefits": [
                    "Increased self-respect and authenticity",
                    "Greater trust and respect from others",
                    "Alignment between values and actions",
                    "Contribution to justice and healing in the world"
                ]
            }
        }
    
    async def _determine_therapeutic_intent(self, context: Dict[str, Any], soul_level: str) -> str:
        """Determine Gevurah-specific therapeutic intent"""
        boundary_issues = context.get("boundary_issues", [])
        shadow_patterns = context.get("shadow_patterns", [])
        discipline_challenges = context.get("discipline_challenges", [])
        
        if boundary_issues:
            return f"Strengthen boundaries and protective capacity: {', '.join(boundary_issues[:2])}"
        elif shadow_patterns:
            return f"Integrate shadow material with firm compassion: {', '.join(shadow_patterns[:2])}"
        elif discipline_challenges:
            return f"Build discipline and inner strength: {', '.join(discipline_challenges[:2])}"
        else:
            return "Develop healthy boundaries, inner discipline, and authentic strength"
    
    async def _generate_sefirot_response(self, activation: SefirotActivation, 
                                       context: Dict[str, Any], soul_level: str) -> SefirotResponse:
        """Generate Gevurah-specific therapeutic response"""
        
        # Identify primary strength need
        strength_need = await self._identify_strength_need(context)
        
        # Generate discipline approach
        discipline_approach = await self._create_discipline_approach(strength_need, context)
        
        # Create boundary guidance
        boundary_guidance = await self._create_boundary_guidance(context, soul_level)
        
        # Generate metaphors and symbols
        metaphors = await self._generate_gevurah_metaphors(context, strength_need)
        symbols = await self._generate_gevurah_symbols(context)
        
        response_content = f"""
        ⚔️ Gevurah Strength Center Activated
        
        Welcome to the forge where character is strengthened and refined. The Gevurah sefirot builds 
        protective boundaries, integrates shadow material, and develops the inner discipline necessary 
        for authentic spiritual and psychological growth.
        
        **Primary Strength Focus:** {strength_need}
        
        **Discipline Path:** {discipline_approach['method']}
        
        **Strength Wisdom:** "True strength isn't the absence of vulnerability - it's the courage 
        to protect what's sacred while remaining open to love. Your boundaries create the container 
        where authentic intimacy can flourish."
        """
        
        therapeutic_insights = [
            "Boundaries are not walls - they're the gates that let love in and keep harm out",
            "Your shadow contains not just what you fear, but also your unexpressed power",
            "Discipline is self-love expressed through consistent action aligned with values",
            "Saying no to what doesn't serve creates space to say yes to what does"
        ]
        
        integration_guidance = [
            f"Practice {discipline_approach['method']} to build inner strength",
            "Notice when you need to set a boundary and practice doing so with kind firmness",
            "Pay attention to your projections and strong reactions - they reveal shadow material",
            "Build one small discipline daily to strengthen your relationship with commitment"
        ]
        
        return SefirotResponse(
            sefirot_type=SefirotType.GEVURAH,
            response_content=response_content,
            therapeutic_insights=therapeutic_insights,
            integration_guidance=integration_guidance,
            confidence=0.87,
            depth_level=soul_level,
            next_sefirot_recommendations=[SefirotType.CHESED, SefirotType.TIFERET, SefirotType.YESOD],
            soul_level_resonance=soul_level,
            metaphors=metaphors,
            symbols=symbols
        )
    
    async def _process_through_sefirot_lens(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process user input through Gevurah strength and discipline lens"""
        
        # Identify strength opportunities
        strength_opportunities = await self._identify_strength_opportunities(user_input, context)
        
        # Create empowering reframe
        empowering_reframe = await self._create_empowering_reframe(user_input, context)
        
        # Generate boundary strategies
        boundary_strategies = await self._create_boundary_strategies(user_input, context)
        
        # Create discipline prescription
        discipline_prescription = await self._create_discipline_prescription(user_input, context)
        
        response = f"""
        ⚔️ **Gevurah Strength Response: Forging Your Inner Warrior**
        
        I honor your courage in facing this challenge. Within you lives a spiritual warrior capable 
        of both fierce protection and tender love. Let's strengthen your boundaries and refine your 
        character through this experience.
        
        **Empowering Reframe:**
        {empowering_reframe}
        
        **Strength Building Opportunities:**
        {self._format_list(strength_opportunities)}
        
        **Boundary Strategy:**
        {self._format_boundary_strategy(boundary_strategies)}
        
        **Discipline Prescription:**
        {self._format_discipline_prescription(discipline_prescription)}
        
        **Warrior Reminder:** You have the strength to protect what's sacred and the discipline 
        to become who you're meant to be. Your boundaries serve love, not fear.
        """
        
        insights = [
            "Your challenges are opportunities to develop spiritual and emotional muscle",
            "Healthy boundaries create the safety necessary for vulnerability and intimacy",
            "Your power is meant to serve love, not dominate or control",
            "Discipline is freedom - it creates space for what truly matters"
        ]
        
        guidance = [
            "Practice saying no to one thing daily that doesn't align with your values",
            "Notice when you feel triggered and ask what boundary might need strengthening",
            "Build one small daily discipline that supports your highest goals",
            "Remember that being strong doesn't mean being hard - stay open while staying firm"
        ]
        
        return {
            "response": response,
            "insights": insights,
            "guidance": guidance,
            "depth_level": "warrior_strength_building",
            "confidence": 0.86,
            "empowering_reframe": empowering_reframe,
            "boundary_strategies": boundary_strategies,
            "discipline_prescription": discipline_prescription
        }
    
    async def _identify_strength_need(self, context: Dict[str, Any]) -> str:
        """Identify the primary strength-building need"""
        boundary_issues = context.get("boundary_issues", [])
        relationship_patterns = context.get("relationship_patterns", [])
        self_discipline_level = context.get("self_discipline_level", "moderate")
        
        if "people-pleasing" in str(boundary_issues).lower():
            return "protective_boundaries"
        elif "codependent" in str(relationship_patterns).lower():
            return "relational_boundaries"
        elif self_discipline_level == "low":
            return "inner_boundaries"
        elif "power" in str(context.get("shadow_patterns", [])).lower():
            return "spiritual_boundaries"
        else:
            return "protective_boundaries"  # Default
    
    async def _create_discipline_approach(self, strength_need: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create specific discipline approach for strength need"""
        boundary_framework = self.boundary_frameworks.get(strength_need, 
                                                         self.boundary_frameworks["protective_boundaries"])
        
        return {
            "need": strength_need,
            "method": boundary_framework["description"],
            "principles": boundary_framework["core_principles"][:2],
            "practices": boundary_framework["practices"][:3],
            "strength_focus": boundary_framework["strength_building"]
        }
    
    async def _create_boundary_guidance(self, context: Dict[str, Any], soul_level: str) -> List[str]:
        """Create boundary guidance appropriate for soul level"""
        guidance = []
        
        # Basic boundary guidance
        guidance.extend([
            "Your energy is sacred - protect it wisely",
            "Practice saying 'let me think about it' instead of automatic yes",
            "Notice energy drains and create protective limits"
        ])
        
        # Soul level specific guidance
        if soul_level in ["ruach", "neshamah"]:
            guidance.extend([
                "Use boundaries to create space for deeper spiritual practice",
                "Recognize that serving others requires serving your own growth first"
            ])
        
        if soul_level in ["neshamah", "chayah", "yechida"]:
            guidance.append("Your boundaries serve the divine work you came here to do")
        
        return guidance[:5]
    
    async def _identify_strength_opportunities(self, user_input: str, context: Dict[str, Any]) -> List[str]:
        """Identify opportunities for building strength in user's situation"""
        opportunities = []
        input_lower = user_input.lower()
        
        # Boundary opportunities
        boundary_indicators = ["overwhelmed", "drained", "taken advantage", "can't say no"]
        if any(indicator in input_lower for indicator in boundary_indicators):
            opportunities.append("Strengthen protective boundaries to preserve your energy and well-being")
        
        # Shadow work opportunities
        trigger_indicators = ["irritated", "angry", "triggered", "judgmental", "can't stand"]
        if any(indicator in input_lower for indicator in trigger_indicators):
            opportunities.append("Use emotional triggers as doorways to reclaim projected shadow material")
        
        # Discipline opportunities
        discipline_indicators = ["procrastinate", "lack motivation", "can't stick to", "give up"]
        if any(indicator in input_lower for indicator in discipline_indicators):
            opportunities.append("Build inner discipline and commitment to support your goals")
        
        # Power opportunities
        power_indicators = ["powerless", "victim", "can't do anything", "helpless"]
        if any(indicator in input_lower for indicator in power_indicators):
            opportunities.append("Reclaim your personal power and authority over your life choices")
        
        # Default opportunities
        if not opportunities:
            opportunities = [
                "Strengthen your capacity to protect what's sacred to you",
                "Build discipline that supports your highest values and goals",
                "Develop healthy assertiveness and self-advocacy skills"
            ]
        
        return opportunities
    
    async def _create_empowering_reframe(self, user_input: str, context: Dict[str, Any]) -> str:
        """Create empowering reframe from Gevurah strength perspective"""
        input_lower = user_input.lower()
        
        if "overwhelmed" in input_lower:
            return "Your overwhelm is information about boundaries that need strengthening. This is an opportunity to build protective structures."
        elif "angry" in input_lower or "frustrated" in input_lower:
            return "Your anger contains important information about your values and boundaries. Channel this energy into positive change."
        elif "stuck" in input_lower or "powerless" in input_lower:
            return "This feeling of stuckness is the tension before breakthrough. Your power is gathering strength to create change."
        elif "conflict" in input_lower:
            return "Conflict is an opportunity to practice healthy boundaries and authentic self-expression."
        elif "failure" in input_lower or "mistake" in input_lower:
            return "This experience is strengthening your character and resilience. Warriors are forged through challenges."
        else:
            return "This situation is developing your inner strength and spiritual warriorship."
    
    async def _create_boundary_strategies(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create specific boundary strategies"""
        return {
            "immediate_boundaries": [
                "Identify one energy drain you can address today",
                "Practice saying 'I need to think about that' instead of immediate yes",
                "Notice physical sensations that signal boundary violations"
            ],
            "communication_boundaries": [
                "Use 'I' statements to express needs without attacking",
                "Set clear expectations about your availability and limits",
                "Practice saying no with kindness but without over-explanation"
            ],
            "energy_protection": [
                "Create physical and emotional space when overwhelmed",
                "Limit time with people who consistently drain your energy",
                "Establish rituals for clearing and protecting your energy field"
            ],
            "commitment_boundaries": [
                "Only make commitments you can keep with joy",
                "Review existing commitments and release what no longer serves",
                "Build in buffer time and space around important commitments"
            ]
        }
    
    async def _create_discipline_prescription(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create discipline prescription for building inner strength"""
        return {
            "daily_discipline": [
                "Choose one small daily practice and commit to it for 21 days",
                "Start your day with an empowering routine that sets positive intention",
                "Practice delayed gratification in small ways to build willpower muscle"
            ],
            "weekly_strength_building": [
                "Review your week: Where did you honor your commitments to yourself?",
                "Identify one area where you can strengthen your boundaries",
                "Practice having difficult conversations with love and firmness"
            ],
            "monthly_character_work": [
                "Reflect on your values and how well your actions align with them",
                "Notice patterns where you give away power and practice reclaiming it",
                "Work with a therapist or coach on shadow integration"
            ],
            "spiritual_warriorship": [
                "Remember that your strength serves love, not ego",
                "Use challenges as opportunities to develop spiritual muscle",
                "Balance fierce protectiveness with tender compassion"
            ]
        }
    
    async def _generate_gevurah_metaphors(self, context: Dict[str, Any], strength_need: str) -> List[str]:
        """Generate Gevurah-specific metaphors"""
        base_metaphors = [
            "You are a spiritual warrior whose sword cuts through illusion with truth",
            "Your boundaries are castle walls that protect the precious kingdom of your heart",
            "Like a master craftsman, challenges forge your character into something beautiful",
            "You are both the guard at the gate and the treasure being protected"
        ]
        
        need_specific = {
            "protective_boundaries": [
                "Your energy is a sacred flame that needs protection from harsh winds",
                "You are the wise gatekeeper who decides what enters your inner sanctuary"
            ],
            "relational_boundaries": [
                "In relationship, you are both individual stars and part of a constellation",
                "Your 'no' creates space for others to hear your authentic 'yes'"
            ],
            "inner_boundaries": [
                "Your mind is a garden where you choose which thoughts to cultivate",
                "Discipline is the loving parent within that guides your inner child"
            ],
            "spiritual_boundaries": [
                "Your discernment is a sacred gift that protects your connection to the divine",
                "You are a temple guardian protecting the holy space within"
            ]
        }
        
        specific_metaphors = need_specific.get(strength_need, [])
        return base_metaphors + specific_metaphors
    
    async def _generate_gevurah_symbols(self, context: Dict[str, Any]) -> List[str]:
        """Generate Gevurah-specific symbols"""
        return [
            "sword", "shield", "fortress", "fire", "mountain",
            "warrior", "gate", "boundary_stones", "protective_circle",
            "forge", "diamond", "lightning_rod"
        ]
    
    def _format_list(self, items: List[str]) -> str:
        """Format list items with strength symbols"""
        return "\n".join(f"⚡ {item}" for item in items)
    
    def _format_boundary_strategy(self, strategies: Dict[str, Any]) -> str:
        """Format boundary strategy for display"""
        formatted = ""
        for category, items in strategies.items():
            formatted += f"\n**{category.replace('_', ' ').title()}:**\n"
            formatted += self._format_list(items[:2]) + "\n"  # Top 2 per category
        return formatted
    
    def _format_discipline_prescription(self, prescription: Dict[str, Any]) -> str:
        """Format discipline prescription for display"""
        formatted = ""
        for timeframe, practices in prescription.items():
            formatted += f"\n**{timeframe.replace('_', ' ').title()}:**\n"
            formatted += self._format_list(practices[:2]) + "\n"  # Top 2 per timeframe
        return formatted
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for Gevurah agent"""
        base_health = await super().health_check()
        base_health.update({
            "boundary_frameworks": len(self.boundary_frameworks),
            "shadow_work_modalities": len(self.shadow_work_modalities),
            "discipline_structures": len(self.discipline_structures),
            "specialization": "Boundaries, discipline, and shadow integration",
            "primary_focus": "Build strength that serves love and protects what's sacred"
        })
        return base_health