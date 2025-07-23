"""
Growth Tracker Prompts for DPNR Platform
Multi-domain progress monitoring and insights
"""

SYSTEM_PROMPT = """You are a skilled progress analyst and growth tracker. Your role is to:

1. Monitor psychological, emotional, and spiritual development patterns
2. Identify breakthrough moments and significant growth events
3. Provide encouraging, accurate assessment of progress  
4. Generate personalized recommendations for continued development

GROWTH DOMAINS:
- Emotional Regulation: Self-awareness, emotional intelligence, stress management
- Relationships: Communication, boundaries, intimacy, connection quality  
- Purpose & Meaning: Career alignment, spiritual growth, values clarity
- Personal Development: Self-compassion, authenticity, resilience building
- Creative Expression: Innovation, artistic pursuits, unique gifts sharing

ANALYSIS APPROACH:
- Look for both subtle shifts and major breakthroughs
- Acknowledge challenges as part of the growth process  
- Celebrate small wins and incremental progress
- Identify patterns across multiple life domains
- Provide hope-filled yet realistic assessments

RECOMMENDATIONS STYLE:
- Personalized to individual's unique journey
- Action-oriented with specific next steps
- Build on existing strengths and momentum
- Address current growth edges with compassion
- Support sustainable, integrated development"""

DOMAIN_ASSESSMENT_PROMPTS = {
    "emotional_wellbeing": {
        "assessment": "How would you describe your emotional landscape over the past week? What emotions have been most present?",
        "growth_indicators": [
            "Increased awareness of emotional patterns",
            "Quicker recovery from emotional triggers",
            "More self-compassion during difficult moments",
            "Better emotional vocabulary and expression"
        ],
        "breakthrough_signs": "Staying calm in previously triggering situations, choosing response over reaction"
    },
    
    "relationships": {
        "assessment": "How have your key relationships felt lately? Where are you experiencing flow vs. friction?",
        "growth_indicators": [
            "Setting clearer boundaries with kindness",
            "Expressing needs more directly",
            "Less people-pleasing behaviors",
            "Deeper intimacy and vulnerability"
        ],
        "breakthrough_signs": "Having difficult conversations with grace, maintaining boundaries without guilt"
    },
    
    "purpose_meaning": {
        "assessment": "How aligned do you feel with your purpose? What's bringing meaning to your days?",
        "growth_indicators": [
            "Clearer sense of personal mission",
            "Work feeling more aligned with values",
            "Increased sense of contribution",
            "Spiritual practices deepening"
        ],
        "breakthrough_signs": "Major life decisions aligning with authentic self, feeling 'on path'"
    },
    
    "personal_development": {
        "assessment": "What aspects of yourself are you actively developing? Where do you see growth?",
        "growth_indicators": [
            "More authentic self-expression",
            "Reduced perfectionism",
            "Increased self-acceptance",
            "Comfortable with vulnerability"
        ],
        "breakthrough_signs": "Being yourself without apology, embracing imperfection as human"
    }
}

TREND_ANALYSIS_PROMPTS = {
    "improving": """I'm noticing a beautiful upward trend in your {domain}. Specifically:
- {specific_improvements}
- {evidence_of_growth}

This shows real progress! What's supporting this positive momentum?""",
    
    "stable": """Your {domain} has been relatively stable, which can mean:
- You're in a integration phase, solidifying recent growth
- This area is currently balanced while you focus elsewhere
- You may be ready for the next growth edge here

What feels true for you about this stability?""",
    
    "declining": """I notice some challenges in your {domain} recently. This isn't failure - it's information:
- Growth often involves temporary dips
- You may be clearing old patterns
- External stressors might be impacting this area

What support would help you navigate this phase?""",
    
    "breakthrough": """🌟 Breakthrough alert in {domain}! This is significant:
- {breakthrough_description}
- This represents a new level of mastery
- You've crossed an important threshold

How does it feel to have made this leap?"""
}

PERSONALIZED_INSIGHTS_TEMPLATES = {
    "pattern_recognition": """Looking across your journey, I notice a pattern: {pattern_description}
This suggests {insight_about_growth_style}
Consider: {reflection_question}""",
    
    "strength_building": """Your superpower is emerging in {area}: {strength_description}
This is becoming a real gift that you can offer others.
How might you share this strength more fully?""",
    
    "growth_edge": """Your current growth edge appears to be {edge_description}.
This is exactly where transformation happens.
Small experiment to try: {gentle_suggestion}""",
    
    "integration": """You're in an integration phase where {integration_description}.
This is sacred work - letting new growth settle into your bones.
Be patient with the process."""
}

RECOMMENDATION_FRAMEWORKS = {
    "next_micro_step": """Based on your progress, one tiny next step could be:
{specific_micro_action}
This builds on what's already working and requires minimal effort.""",
    
    "stretch_goal": """You might be ready for this stretch:
{stretch_description}
This would challenge you in just the right way to catalyze growth.""",
    
    "support_structure": """To sustain your progress, consider:
{support_suggestions}
Growth happens best with the right support ecosystem.""",
    
    "celebration_practice": """Don't forget to celebrate:
{celebration_suggestions}
Acknowledging progress creates momentum for more."""
}

MILESTONE_RECOGNITION = {
    "weekly": "This week you've shown up for your growth in these ways: {weekly_wins}",
    "monthly": "This month's theme seems to be {monthly_theme}. You've grown by {growth_description}",
    "breakthrough": "This is a watershed moment. You've fundamentally shifted {fundamental_shift}",
    "anniversary": "A year ago, you {past_state}. Now you {current_state}. That's transformation!"
}