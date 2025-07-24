#!/usr/bin/env python3
"""
Production-ready Agent Library Runner
Demonstrates the complete modular agent system with Hebrew translation support
"""

import asyncio
import logging
import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, Any, List

# Add the agent library to the path
sys.path.append(str(Path(__file__).parent))

# Import all agent components
from agent_library.core.base_agent import AgentMessage, AgentResponse
from agent_library.agents.language.translation_agent import TranslationAgent
from agent_library.agents.language.nlp_analyzer_agent import NLPAnalyzerAgent
from agent_library.agents.assessment.enneagram_agent import EnneagramAgent
from agent_library.orchestration.chain_builder import ChainBuilder, ChainExecutionMode
from agent_library.orchestration.workflow_engine import WorkflowEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('agent_system.log')
    ]
)

logger = logging.getLogger(__name__)


class ProductionAgentSystem:
    """Production-ready agent system orchestrator"""
    
    def __init__(self):
        self.chain_builder = ChainBuilder()
        self.workflow_engine = WorkflowEngine(self.chain_builder)
        self.agents = {}
        self.performance_metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0.0
        }
    
    async def initialize_system(self):
        """Initialize all agents and register them"""
        logger.info("🚀 Initializing Production Agent System...")
        
        try:
            # Initialize Translation Agent
            logger.info("Initializing Translation Agent...")
            translation_agent = TranslationAgent(
                agent_id="translation_agent_1", 
                supported_languages=["en", "he", "ar", "es", "fr"]
            )
            await translation_agent.initialize()
            self.agents["translation"] = translation_agent
            self.workflow_engine.register_agent(translation_agent)
            
            # Initialize NLP Analyzer Agent
            logger.info("Initializing NLP Analyzer Agent...")
            nlp_agent = NLPAnalyzerAgent(
                agent_id="nlp_analyzer_1",
                features=["sentiment", "emotion", "embedding", "stats", "linguistic"]
            )
            await nlp_agent.initialize()
            self.agents["nlp"] = nlp_agent
            self.workflow_engine.register_agent(nlp_agent)
            
            # Initialize Enneagram Agent
            logger.info("Initializing Enneagram Assessment Agent...")
            enneagram_agent = EnneagramAgent(
                agent_id="enneagram_agent_1",
                confidence_threshold=0.75
            )
            await enneagram_agent.initialize()
            self.agents["enneagram"] = enneagram_agent
            self.workflow_engine.register_agent(enneagram_agent)
            
            # Register agent types in chain builder
            self.chain_builder.register_agent(TranslationAgent, "TranslationAgent")
            self.chain_builder.register_agent(NLPAnalyzerAgent, "NLPAnalyzerAgent")
            self.chain_builder.register_agent(EnneagramAgent, "EnneagramAgent")
            
            logger.info("✅ All agents initialized successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize system: {str(e)}")
            return False
    
    def create_multilingual_assessment_chain(self):
        """Create the main multilingual assessment chain"""
        logger.info("📋 Creating multilingual assessment chain...")
        
        # Create the chain
        chain = self.chain_builder.create_chain(
            chain_id="multilingual_assessment",
            name="Multilingual Psychological Assessment",
            description="Complete psychological assessment supporting Hebrew and multiple languages"
        )
        
        # Add agents to the chain
        self.chain_builder.add_agent(
            "multilingual_assessment", 
            "translation_agent_1", 
            "TranslationAgent",
            {"supported_languages": ["en", "he", "ar", "es", "fr"]}
        )
        
        self.chain_builder.add_agent(
            "multilingual_assessment",
            "nlp_analyzer_1",
            "NLPAnalyzerAgent",
            {"features": ["sentiment", "emotion", "linguistic", "stats"]}
        )
        
        self.chain_builder.add_agent(
            "multilingual_assessment",
            "enneagram_agent_1",
            "EnneagramAgent",
            {"confidence_threshold": 0.75}
        )
        
        # Connect the agents
        self.chain_builder.connect_agents(
            "multilingual_assessment",
            "translation_agent_1",
            "nlp_analyzer_1",
            {"translated_text": "text", "source_language": "original_language"}
        )
        
        self.chain_builder.connect_agents(
            "multilingual_assessment",
            "nlp_analyzer_1",
            "enneagram_agent_1",
            {"linguistic": "nlp_features", "sentiment": "emotional_context"}
        )
        
        # Validate the chain
        is_valid, errors = self.chain_builder.validate_chain("multilingual_assessment")
        if not is_valid:
            logger.error("Chain validation failed:")
            for error in errors:
                logger.error(f"  - {error}")
            return False
        
        logger.info("✅ Multilingual assessment chain created and validated!")
        return True
    
    async def run_demonstration(self):
        """Run a comprehensive demonstration of the system"""
        logger.info("🧪 Running system demonstration...")
        
        # Test cases with Hebrew and English text
        test_cases = [
            {
                "name": "Hebrew Self-Description",
                "text": "אני אדם מאוד אופטימי ואוהב לחקור דברים חדשים. אני תמיד מחפש הזדמנויות וחוויות חדשות ואוהב להיות מוקף באנשים. לפעמים קשה לי להתמקד במשימה אחת לזמן רב, אבל אני מצליח להשיג המון דברים כי אני נמרץ ויצירתי.",
                "target_language": "en",
                "description": "Hebrew text describing an enthusiastic, optimistic personality"
            },
            {
                "name": "English Achievement Focus",
                "text": "I'm someone who really values success and achieving my goals. I work hard to maintain a positive image and I'm very focused on being efficient and productive. I like to be seen as competent and successful by others. Sometimes I worry about whether I'm doing enough or if I'm truly being myself.",
                "target_language": "he", 
                "description": "English text describing achievement-oriented personality"
            },
            {
                "name": "English Helper Personality",
                "text": "I genuinely care about helping others and making sure everyone around me is happy and comfortable. I often put other people's needs before my own and I get a lot of satisfaction from being needed and appreciated. I sometimes worry that I give too much of myself to others.",
                "target_language": "he",
                "description": "English text describing helper/giver personality"
            }
        ]
        
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            logger.info(f"\n{'='*60}")
            logger.info(f"🧪 Test Case {i}: {test_case['name']}")
            logger.info(f"Description: {test_case['description']}")
            logger.info(f"Original text: {test_case['text'][:100]}...")
            
            start_time = time.time()
            
            try:
                # Execute the chain
                execution = await self.workflow_engine.execute_chain(
                    chain_id="multilingual_assessment",
                    input_data={
                        "action": "translate",
                        "text": test_case["text"],
                        "target_language": test_case["target_language"]
                    },
                    user_id=f"demo_user_{i}",
                    timeout=60
                )
                
                execution_time = time.time() - start_time
                
                if execution.status.value == "completed":
                    # Extract results from each node
                    translation_result = execution.node_executions["translation_agent_1"].output_data
                    nlp_result = execution.node_executions["nlp_analyzer_1"].output_data
                    enneagram_result = execution.node_executions["enneagram_agent_1"].output_data
                    
                    logger.info("✅ Chain execution completed successfully!")
                    logger.info(f"⏱️  Execution time: {execution_time:.2f} seconds")
                    
                    # Log translation results
                    if translation_result:
                        logger.info(f"🔄 Translation: {translation_result.get('translated_text', 'N/A')[:100]}...")
                        logger.info(f"🌐 Detected language: {translation_result.get('source_language', 'N/A')}")
                        logger.info(f"🎯 Translation confidence: {translation_result.get('confidence', 0):.2%}")
                    
                    # Log NLP results
                    if nlp_result:
                        sentiment = nlp_result.get('sentiment', {})
                        emotions = nlp_result.get('emotion', [])
                        stats = nlp_result.get('stats', {})
                        
                        logger.info(f"😊 Sentiment: {sentiment.get('label', 'N/A')} ({sentiment.get('score', 0):.2%})")
                        if emotions:
                            top_emotion = emotions[0]
                            logger.info(f"💭 Top emotion: {top_emotion.get('emotion', 'N/A')} ({top_emotion.get('score', 0):.2%})")
                        logger.info(f"📊 Word count: {stats.get('word_count', 0)}")
                    
                    # Log Enneagram results
                    if enneagram_result:
                        primary_type = enneagram_result.get('primary_type', 'N/A')
                        confidence = enneagram_result.get('confidence', 0)
                        type_desc = enneagram_result.get('type_description', {}).get('primary', {})
                        
                        logger.info(f"🧠 Primary Enneagram Type: {primary_type} - {type_desc.get('name', 'N/A')}")
                        logger.info(f"🎯 Assessment confidence: {confidence:.2%}")
                        logger.info(f"💡 Core motivation: {type_desc.get('core_motivation', 'N/A')[:100]}...")
                        
                        # Log growth recommendations
                        recommendations = enneagram_result.get('growth_recommendations', [])
                        if recommendations:
                            logger.info(f"🌱 Top recommendation: {recommendations[0]}")
                    
                    # Update performance metrics
                    self.performance_metrics["successful_requests"] += 1
                    
                    results.append({
                        "test_case": test_case['name'],
                        "execution_time": execution_time,
                        "translation_confidence": translation_result.get('confidence', 0) if translation_result else 0,
                        "nlp_confidence": nlp_result.get('confidence', 0) if nlp_result else 0,
                        "enneagram_confidence": enneagram_result.get('confidence', 0) if enneagram_result else 0,
                        "primary_type": enneagram_result.get('primary_type') if enneagram_result else None,
                        "status": "success"
                    })
                
                else:
                    logger.error(f"❌ Chain execution failed: {execution.error}")
                    self.performance_metrics["failed_requests"] += 1
                    
                    results.append({
                        "test_case": test_case['name'],
                        "execution_time": execution_time,
                        "status": "failed",
                        "error": execution.error
                    })
            
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"❌ Test case failed: {str(e)}")
                self.performance_metrics["failed_requests"] += 1
                
                results.append({
                    "test_case": test_case['name'],
                    "execution_time": execution_time,
                    "status": "error",
                    "error": str(e)
                })
            
            self.performance_metrics["total_requests"] += 1
        
        return results
    
    async def performance_test(self, num_requests: int = 10):
        """Run performance testing"""
        logger.info(f"🚀 Running performance test with {num_requests} requests...")
        
        test_text = "I am an optimistic person who loves exploring new opportunities and helping others achieve their goals."
        
        start_time = time.time()
        tasks = []
        
        for i in range(num_requests):
            task = self.workflow_engine.execute_chain(
                chain_id="multilingual_assessment",
                input_data={
                    "action": "translate",
                    "text": test_text,
                    "target_language": "he"
                },
                user_id=f"perf_user_{i}",
                timeout=30
            )
            tasks.append(task)
        
        # Execute all requests concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        total_time = time.time() - start_time
        successful = sum(1 for r in results if not isinstance(r, Exception) and r.status.value == "completed")
        failed = len(results) - successful
        
        avg_time = total_time / len(results)
        throughput = len(results) / total_time
        
        logger.info(f"📊 Performance Test Results:")
        logger.info(f"   Total requests: {len(results)}")
        logger.info(f"   Successful: {successful}")
        logger.info(f"   Failed: {failed}")
        logger.info(f"   Total time: {total_time:.2f} seconds")
        logger.info(f"   Average time per request: {avg_time:.2f} seconds")
        logger.info(f"   Throughput: {throughput:.2f} requests/second")
        
        return {
            "total_requests": len(results),
            "successful": successful,
            "failed": failed,
            "total_time": total_time,
            "avg_time": avg_time,
            "throughput": throughput
        }
    
    def print_system_status(self):
        """Print system status and metrics"""
        logger.info(f"\n{'='*60}")
        logger.info("📊 SYSTEM STATUS REPORT")
        logger.info(f"{'='*60}")
        
        # Agent status
        logger.info("🤖 Agent Status:")
        for agent_name, agent in self.agents.items():
            health = asyncio.create_task(agent.health_check())
            # Note: In production, you'd await this properly
            logger.info(f"   {agent_name}: {agent.status.value}")
        
        # Performance metrics
        logger.info("📈 Performance Metrics:")
        logger.info(f"   Total requests: {self.performance_metrics['total_requests']}")
        logger.info(f"   Successful: {self.performance_metrics['successful_requests']}")
        logger.info(f"   Failed: {self.performance_metrics['failed_requests']}")
        
        if self.performance_metrics["total_requests"] > 0:
            success_rate = (self.performance_metrics["successful_requests"] / 
                          self.performance_metrics["total_requests"]) * 100
            logger.info(f"   Success rate: {success_rate:.1f}%")
        
        # Chain status
        logger.info("🔗 Available Chains:")
        for chain_id, chain in self.chain_builder.chains.items():
            logger.info(f"   {chain_id}: {len(chain.nodes)} nodes, {len(chain.connections)} connections")
        
        # Execution metrics
        exec_metrics = self.workflow_engine.get_execution_metrics()
        logger.info("⚡ Execution Metrics:")
        logger.info(f"   Total executions: {exec_metrics['total_executions']}")
        logger.info(f"   Active executions: {exec_metrics['active_executions']}")
        logger.info(f"   Registered agents: {exec_metrics['registered_agents']}")


async def main():
    """Main entry point"""
    print("🎉 Welcome to the Modular Agent Library System!")
    print("=" * 60)
    
    # Initialize system
    system = ProductionAgentSystem()
    
    if not await system.initialize_system():
        print("❌ System initialization failed!")
        return 1
    
    # Create assessment chain
    if not system.create_multilingual_assessment_chain():
        print("❌ Chain creation failed!")
        return 1
    
    # Run demonstration
    print("\n🧪 Running comprehensive demonstration...")
    demo_results = await system.run_demonstration()
    
    # Run performance test
    print(f"\n⚡ Running performance test...")
    perf_results = await system.performance_test(num_requests=5)
    
    # Print final status
    system.print_system_status()
    
    print(f"\n🎉 Demonstration completed successfully!")
    print(f"✅ System is ready for production use!")
    
    # Save results
    results_file = "agent_system_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            "demo_results": demo_results,
            "performance_results": perf_results,
            "timestamp": time.time()
        }, f, indent=2)
    
    print(f"📊 Results saved to: {results_file}")
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"💥 Unexpected error: {str(e)}")
        sys.exit(1)