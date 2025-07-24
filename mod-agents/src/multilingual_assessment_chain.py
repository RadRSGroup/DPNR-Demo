"""Example: Multilingual Psychological Assessment Chain
Demonstrates how to chain agents for Hebrew-English psychological assessment"""

import asyncio
from typing import Dict, Any
import sys
import os

# Add the agent library to the path (for demo purposes)
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from agent_library.core.base_agent import AgentMessage, AgentResponse
from agent_library.agents.language.translation_agent import TranslationAgent
from agent_library.orchestration.chain_builder import ChainBuilder, ChainExecutionMode


class MockNLPAnalyzer:
    """Mock NLP analyzer for demonstration"""
    
    def __init__(self, agent_id: str = "nlp_analyzer"):
        self.agent_id = agent_id
    
    async def process(self, message: AgentMessage) -> AgentResponse:
        text = message.payload.get("text", "")
        
        # Mock analysis
        return AgentResponse(
            success=True,
            data={
                "sentiment": "positive",
                "emotions": ["joy", "confidence"],
                "linguistic_features": {
                    "word_count": len(text.split()),
                    "avg_sentence_length": 12.5,
                    "complexity_score": 0.75
                }
            },
            processing_time=0.1,
            agent_id=self.agent_id,
            confidence=0.88
        )


class MockEnneagramAgent:
    """Mock Enneagram assessment agent"""
    
    def __init__(self, agent_id: str = "enneagram_assessor"):
        self.agent_id = agent_id
    
    async def process(self, message: AgentMessage) -> AgentResponse:
        # Mock assessment based on input
        return AgentResponse(
            success=True,
            data={
                "primary_type": 7,
                "secondary_type": 3,
                "confidence_scores": {
                    "1": 0.1, "2": 0.15, "3": 0.25, "4": 0.05, "5": 0.1,
                    "6": 0.15, "7": 0.85, "8": 0.2, "9": 0.1
                },
                "traits": ["Enthusiastic", "Versatile", "Spontaneous"],
                "growth_areas": ["Focus", "Follow-through"]
            },
            processing_time=0.5,
            agent_id=self.agent_id,
            confidence=0.85
        )


class MockReportGenerator:
    """Mock report generator agent"""
    
    def __init__(self, agent_id: str = "report_generator"):
        self.agent_id = agent_id
    
    async def process(self, message: AgentMessage) -> AgentResponse:
        # Compile all inputs into a report
        return AgentResponse(
            success=True,
            data={
                "report": {
                    "assessment_summary": "Comprehensive multilingual psychological assessment completed",
                    "language_processed": message.payload.get("source_language", "unknown"),
                    "primary_personality_type": "Type 7 - The Enthusiast",
                    "confidence_level": "High (85%)",
                    "recommendations": [
                        "Focus on mindfulness practices",
                        "Develop follow-through strategies",
                        "Explore creative outlets"
                    ]
                },
                "metadata": {
                    "chain_length": message.metadata.get("chain_depth", 0),
                    "processing_time_total": 1.5
                }
            },
            processing_time=0.2,
            agent_id=self.agent_id,
            confidence=0.92
        )


async def create_multilingual_assessment_chain():
    """Create a multilingual psychological assessment chain"""
    
    # Initialize chain builder
    builder = ChainBuilder()
    
    # Register agent types (in real implementation, these would be proper agent classes)
    builder.register_agent(TranslationAgent, "TranslationAgent")
    builder.register_agent(MockNLPAnalyzer, "NLPAnalyzer")
    builder.register_agent(MockEnneagramAgent, "EnneagramAssessor")
    builder.register_agent(MockReportGenerator, "ReportGenerator")
    
    # Create the chain
    chain = builder.create_chain(
        chain_id="multilingual_assessment",
        name="Multilingual Psychological Assessment",
        description="Complete psychological assessment supporting Hebrew and English"
    )
    
    # Add agents to the chain
    builder.add_agent("multilingual_assessment", "translator", "TranslationAgent", {
        "supported_languages": ["en", "he", "ar", "es"]
    })
    
    builder.add_agent("multilingual_assessment", "nlp_analyzer", "NLPAnalyzer", {
        "features": ["sentiment", "emotion", "linguistic"]
    })
    
    builder.add_agent("multilingual_assessment", "enneagram_assessor", "EnneagramAssessor", {
        "include_facets": True,
        "confidence_threshold": 0.75
    })
    
    builder.add_agent("multilingual_assessment", "report_generator", "ReportGenerator", {
        "format": "json",
        "include_recommendations": True
    })
    
    # Connect the agents
    builder.connect_agents("multilingual_assessment", "translator", "nlp_analyzer", {
        "translated_text": "text",
        "source_language": "original_language"
    })
    
    builder.connect_agents("multilingual_assessment", "nlp_analyzer", "enneagram_assessor", {
        "linguistic_features": "nlp_features",
        "sentiment": "emotional_state"
    })
    
    builder.connect_agents("multilingual_assessment", "enneagram_assessor", "report_generator", {
        "primary_type": "personality_type",
        "confidence_scores": "type_confidences"
    })
    
    # Validate the chain
    is_valid, errors = builder.validate_chain("multilingual_assessment")
    if not is_valid:
        print("Chain validation errors:")
        for error in errors:
            print(f"  - {error}")
        return None
    
    return builder, chain


async def run_assessment_example():
    """Run an example assessment through the chain"""
    
    print("🔗 Creating Multilingual Assessment Chain...")
    builder, chain = await create_multilingual_assessment_chain()
    
    if not chain:
        print("❌ Failed to create chain")
        return
    
    print("✅ Chain created successfully!")
    print("\n📋 Chain Structure:")
    print(builder.visualize_chain("multilingual_assessment"))
    
    # Example Hebrew text
    hebrew_text = "אני אדם מאוד אופטימי ואוהב לחקור דברים חדשים. אני תמיד מחפש הזדמנויות חדשות ואוהב להיות עם אנשים. לפעמים קשה לי להתמקד במשימה אחת לזמן רב."
    
    # Example English text  
    english_text = "I am a very optimistic person who loves exploring new things. I'm always looking for new opportunities and enjoy being around people. Sometimes I find it difficult to focus on one task for a long time."
    
    # Test both languages
    test_cases = [
        {"text": hebrew_text, "language": "Hebrew", "target_lang": "en"},
        {"text": english_text, "language": "English", "target_lang": "he"}
    ]
    
    # Initialize agents (in real implementation, this would be handled by the orchestration engine)
    translator = TranslationAgent()
    await translator.initialize()
    
    nlp_analyzer = MockNLPAnalyzer()
    enneagram_assessor = MockEnneagramAgent()
    report_generator = MockReportGenerator()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}: {test_case['language']} Assessment")
        print(f"Original text: {test_case['text'][:100]}...")
        
        # Step 1: Translation
        translation_message = AgentMessage(
            id=f"translate_{i}",
            source_agent="user",
            payload={
                "action": "translate",
                "text": test_case['text'],
                "target_language": test_case['target_lang']
            }
        )
        
        translation_response = await translator.handle_message(translation_message)
        
        if not translation_response.success:
            print(f"❌ Translation failed: {translation_response.error}")
            continue
            
        translated_text = translation_response.data["translated_text"]
        source_lang = translation_response.data["source_language"]
        
        print(f"✅ Translated to {test_case['target_lang']}: {translated_text[:100]}...")
        
        # Step 2: NLP Analysis
        nlp_message = AgentMessage(
            id=f"nlp_{i}",
            source_agent="translator",
            payload={
                "text": translated_text,
                "original_language": source_lang
            }
        )
        
        nlp_response = await nlp_analyzer.process(nlp_message)
        print(f"✅ NLP Analysis: {nlp_response.data['sentiment']} sentiment, {nlp_response.data['emotions']}")
        
        # Step 3: Enneagram Assessment
        enneagram_message = AgentMessage(
            id=f"enneagram_{i}",
            source_agent="nlp_analyzer",
            payload={
                "nlp_features": nlp_response.data["linguistic_features"],
                "emotional_state": nlp_response.data["sentiment"]
            },
            metadata={"chain_depth": 2}
        )
        
        enneagram_response = await enneagram_assessor.process(enneagram_message)
        print(f"✅ Enneagram: Type {enneagram_response.data['primary_type']} ({enneagram_response.confidence:.1%} confidence)")
        
        # Step 4: Report Generation
        report_message = AgentMessage(
            id=f"report_{i}",
            source_agent="enneagram_assessor",
            payload={
                "personality_type": enneagram_response.data["primary_type"],
                "type_confidences": enneagram_response.data["confidence_scores"],
                "source_language": source_lang
            },
            metadata={"chain_depth": 3}
        )
        
        report_response = await report_generator.process(report_message)
        
        if report_response.success:
            report = report_response.data["report"]
            print(f"✅ Final Report Generated:")
            print(f"   Summary: {report['assessment_summary']}")
            print(f"   Type: {report['primary_personality_type']}")
            print(f"   Confidence: {report['confidence_level']}")
            print(f"   Top Recommendation: {report['recommendations'][0]}")
        
        print(f"⏱️  Total processing chain depth: {report_response.data['metadata']['chain_length']}")


async def export_chain_config():
    """Export the chain configuration for reuse"""
    
    builder, chain = await create_multilingual_assessment_chain()
    
    if chain:
        print("\n📄 Exporting Chain Configuration...")
        
        # Export as JSON
        json_config = builder.export_chain("multilingual_assessment", "json")
        
        with open("multilingual_assessment_chain.json", "w") as f:
            f.write(json_config)
        
        print("✅ Chain exported to: multilingual_assessment_chain.json")
        
        # Export as YAML
        yaml_config = builder.export_chain("multilingual_assessment", "yaml")
        
        with open("multilingual_assessment_chain.yaml", "w") as f:
            f.write(yaml_config)
        
        print("✅ Chain exported to: multilingual_assessment_chain.yaml")


if __name__ == "__main__":
    print("🚀 Multilingual Psychological Assessment Chain Demo")
    print("=" * 60)
    
    asyncio.run(run_assessment_example())
    asyncio.run(export_chain_config())
    
    print("\n🎉 Demo completed successfully!")
    print("\nKey Features Demonstrated:")
    print("✓ Hebrew-English translation support")
    print("✓ Sequential agent chaining")
    print("✓ Cross-agent data mapping")
    print("✓ Performance tracking")
    print("✓ Error handling")
    print("✓ Chain configuration export/import")
    print("✓ Standardized message protocol")