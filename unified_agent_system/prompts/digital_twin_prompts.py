"""
Digital Twin Evolution Prompts for DPNR Platform
Soul archetype tracking and spiritual evolution
"""

SYSTEM_PROMPT = """You are a mystical architect who perceives soul essence and creates living digital representations. Your role is to:

1. Create comprehensive digital twins reflecting user's soul archetype
2. Track archetypal evolution through life experiences and insights
3. Generate symbolic representations of spiritual development
4. Support user's understanding of their unique soul signature

ARCHETYPAL FRAMEWORK:
- Major archetypes: Seeker, Healer, Creator, Warrior, Sage, Lover, Magician, Ruler
- Each archetype has shadow and light expressions
- Evolution occurs through integration of experiences and challenges
- Archetypes can shift and blend based on life phases and growth

EVOLUTION TRACKING:
- Significant life events trigger archetypal shifts
- Internal insights change soul expression patterns  
- Relationship experiences evolve the heart center
- Creative expressions unlock new archetypal facets
- Spiritual practices deepen essential nature connection

SYMBOLIC REPRESENTATION:
- Use rich metaphors from nature, mythology, alchemy
- Create visual/symbolic language for soul evolution
- Connect archetypal shifts to tangible life changes
- Honor both universal patterns and individual uniqueness
- Support user's sense of meaning and spiritual identity"""

ARCHETYPE_PROFILES = {
    "seeker": {
        "essence": "The eternal questioner, always searching for truth and meaning",
        "light_expression": "Curious, open, adventurous, growth-oriented",
        "shadow_expression": "Never satisfied, restless, avoiding commitment",
        "evolution_path": "From endless searching to finding home within",
        "symbols": ["compass", "winding path", "horizon", "open book"]
    },
    
    "healer": {
        "essence": "The wounded healer who transforms pain into medicine",
        "light_expression": "Compassionate, nurturing, intuitive, service-oriented",
        "shadow_expression": "Codependent, martyrdom, neglecting self-care",
        "evolution_path": "From fixing others to facilitating self-healing",
        "symbols": ["hands of light", "medicinal herbs", "sacred waters", "phoenix"]
    },
    
    "creator": {
        "essence": "The channel for divine creativity and new possibilities",
        "light_expression": "Innovative, expressive, visionary, generative",
        "shadow_expression": "Perfectionism, creative blocks, imposter syndrome",
        "evolution_path": "From ego creation to divine co-creation",
        "symbols": ["paintbrush", "loom", "seeds", "dancing flame"]
    },
    
    "warrior": {
        "essence": "The protector of boundaries and champion of causes",
        "light_expression": "Courageous, disciplined, protective, decisive",
        "shadow_expression": "Aggressive, controlling, inability to be vulnerable",
        "evolution_path": "From fighting against to fighting for",
        "symbols": ["sword of truth", "shield", "mountain", "oak tree"]
    },
    
    "sage": {
        "essence": "The wisdom keeper and teacher of eternal truths",
        "light_expression": "Wise, discerning, patient, illuminating",
        "shadow_expression": "Detached, intellectualizing, spiritual bypassing",
        "evolution_path": "From knowledge to embodied wisdom",
        "symbols": ["owl", "ancient tree", "crystal", "third eye"]
    },
    
    "lover": {
        "essence": "The embodiment of divine love and sacred connection",
        "light_expression": "Passionate, connected, sensual, devoted",
        "shadow_expression": "Addiction, losing self in other, jealousy",
        "evolution_path": "From needy love to whole love",
        "symbols": ["intertwined roses", "chalice", "heart flame", "infinity symbol"]
    },
    
    "magician": {
        "essence": "The alchemist who transforms reality through consciousness",
        "light_expression": "Transformative, intuitive, masterful, catalytic",
        "shadow_expression": "Manipulation, illusion, power misuse",
        "evolution_path": "From ego magic to divine alchemy",
        "symbols": ["wand", "cauldron", "spiral", "metamorphosis"]
    },
    
    "ruler": {
        "essence": "The sovereign who creates order and holds space for all",
        "light_expression": "Leadership, responsibility, benevolence, vision",
        "shadow_expression": "Tyranny, rigidity, need for control",
        "evolution_path": "From ruling over to serving the whole",
        "symbols": ["crown of light", "scepter", "throne", "mandala"]
    }
}

EVOLUTION_TRIGGER_PROMPTS = {
    "life_event": """A significant life event has occurred: {event_description}

How does this experience call forth new aspects of your soul archetype?
What dormant qualities are awakening?
What old patterns are ready to transform?""",
    
    "insight_integration": """A profound insight has emerged: {insight_description}

How does this realization shift your archetypal expression?
What new capacities are coming online?
What aspect of your soul signature is revealing itself?""",
    
    "relationship_catalyst": """A relationship dynamic has catalyzed growth: {relationship_description}

How is this connection evolving your capacity to love?
What shadow aspects are being illuminated?
What new relational archetype is emerging?""",
    
    "creative_emergence": """A creative expression has unlocked something: {creative_description}

What soul gifts are finding their voice?
How is your creative channel expanding?
What wants to be birthed through you?"""
}

SOUL_LEVEL_PROGRESSION = {
    "initiate": {
        "description": "Beginning to awaken to soul calling",
        "characteristics": ["Seeking identity", "Questioning purpose", "Early spiritual stirrings"],
        "evolution_focus": "Discovering authentic self"
    },
    
    "apprentice": {
        "description": "Learning to work with soul gifts",
        "characteristics": ["Developing abilities", "Finding mentors", "Practicing skills"],
        "evolution_focus": "Building spiritual muscles"
    },
    
    "journeyer": {
        "description": "Actively walking the soul path",
        "characteristics": ["Taking risks", "Following intuition", "Meeting challenges"],
        "evolution_focus": "Trusting the journey"
    },
    
    "alchemist": {
        "description": "Transforming self and helping others transform",
        "characteristics": ["Shadow integration", "Healing gifts emerging", "Service calling"],
        "evolution_focus": "Becoming the medicine"
    },
    
    "master": {
        "description": "Embodying soul wisdom in daily life",
        "characteristics": ["Natural authority", "Effortless service", "Living legacy"],
        "evolution_focus": "Being the teaching"
    }
}

VISUAL_REPRESENTATION_PROMPTS = {
    "soul_portrait": """Create a symbolic portrait of this soul:
- Primary archetype as the central figure
- Secondary archetypes as surrounding elements
- Current growth edge as emerging light
- Shadow work as roots/foundation
- Soul gifts as emanating rays""",
    
    "evolution_mandala": """Design a mandala showing soul evolution:
- Center: Core essence/true nature
- Inner ring: Primary archetype qualities
- Middle ring: Life experiences integrated
- Outer ring: Gifts offered to world
- Colors reflecting emotional/spiritual tone""",
    
    "journey_map": """Map the soul's journey:
- Starting point: Original wound/calling
- Milestone markers: Key transformations
- Current location: Present archetypal expression
- Horizon line: Emerging potential
- Path style: Spiral, labyrinth, or ascending"""
}

INTEGRATION_PROMPTS = {
    "daily_embodiment": "How can you embody your {archetype} nature in ordinary moments today?",
    "shadow_dialogue": "What would your {archetype}'s shadow like you to know?",
    "gift_activation": "What {archetype} gift is ready to be shared with others?",
    "evolution_prayer": "What is your soul's prayer for continued evolution?"
}